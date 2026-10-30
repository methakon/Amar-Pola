// POST /v1/children/{childId}/pairing-codes (issuePairingCode).
// Protected by ParentOIDC authentication. One unexpired code per child.
#pragma once
#include <optional>
#include <string>

#include <drogon/drogon.h>

#include "auth.h"
#include "crypto_support.h"
#include "db_support.h"
#include "http_support.h"
#include "idempotency_key.h"
#include "validation.h"

namespace ma {

inline constexpr const char* kPairingCodeNamespace = "POST /children/pairing-codes";

inline drogon::HttpResponsePtr pairing_code_response(const Json::Value& body, const std::string& rid) {
  auto resp = drogon::HttpResponse::newHttpJsonResponse(body);
  resp->setStatusCode(drogon::k201Created);
  resp->addHeader(kRequestIdHeader, rid);
  return resp;
}

inline drogon::Task<drogon::HttpResponsePtr> issue_pairing_code(
    drogon::HttpRequestPtr req, std::string child_id_param, Authenticator authenticate) {
  using namespace drogon;
  const std::string rid = request_id_of(req);

  // 413 check
  if (req->body().size() > kMaxBodyBytes) {
    co_return error_response("PAYLOAD_TOO_LARGE", "request body too large", rid);
  }

  // 400: childId path parameter validation
  auto normalized_child = normalize_uuid(child_id_param);
  if (!normalized_child) {
    co_return error_response("INVALID_REQUEST", "childId must be a valid UUID", rid);
  }

  // 400: Idempotency-Key validation
  auto key_hash = hash_idempotency_key(req->getHeader("idempotency-key"));
  if (!key_hash) {
    co_return error_response("INVALID_REQUEST", "Idempotency-Key must be a UUID", rid);
  }

  // 401: Authentication
  auto who = authenticate(req);
  if (!who) {
    co_return error_response("UNAUTHENTICATED", "missing, expired or invalid credential", rid);
  }

  // Check database configuration
  if (!app().hasDbClient(kDbClientName)) {
    co_return error_response("SERVICE_UNAVAILABLE", "database not configured", rid, true);
  }
  auto db = app().getDbClient(kDbClientName);
  if (!db) {
    co_return error_response("SERVICE_UNAVAILABLE", "database not configured", rid, true);
  }

  Json::Value empty_or_body;
  if (!req->body().empty()) {
    if (req->contentType() != CT_APPLICATION_JSON || !parse_json_strict(req->body(), empty_or_body)) {
      co_return error_response("INVALID_REQUEST", "malformed JSON body", rid);
    }
  }

  const std::string req_hash = to_pg_bytea(request_hash(empty_or_body));
  const std::string key_hex = to_pg_bytea(*key_hash);

  std::shared_ptr<orm::Transaction> trans;
  try {
    trans = co_await db->newTransactionCoro();
    co_await trans->execSqlCoro(
        "SELECT set_config('lock_timeout', $1, true), set_config('statement_timeout', $2, true)",
        std::to_string(db_limits().lock_ms), std::to_string(db_limits().statement_ms));

    auto pr = co_await trans->execSqlCoro(
        "SELECT ap_m1.resolve_parent_principal($1, $2)::text AS id", who->issuer, who->subject);
    const std::string principal = pr.at(0)["id"].as<std::string>();
    co_await trans->execSqlCoro("SELECT set_config('ap.principal_id', $1, true)", principal);

    // Idempotency claim
    auto claim = co_await trans->execSqlCoro(
        "SELECT outcome, response_status, response_body::text AS response_body "
        "FROM ap_m1.idempotency_claim($1::uuid, $2, $3::bytea, $4::bytea)",
        principal, std::string(kPairingCodeNamespace), key_hex, req_hash);
    const std::string outcome = claim.at(0)["outcome"].as<std::string>();

    if (outcome == "MISMATCH") {
      rollback_quietly(trans);
      co_return error_response(
          "IDEMPOTENCY_KEY_REUSED", "Idempotency-Key was already used with a different request", rid);
    }
    if (outcome == "PENDING") {
      rollback_quietly(trans);
      LOG_ERROR << "idempotency PENDING outcome, request_id=" << rid;
      co_return error_response("INTERNAL_ERROR", "unexpected server error", rid);
    }
    if (outcome == "REPLAY") {
      Json::Value stored;
      const bool usable = !claim.at(0)["response_body"].isNull() &&
                          parse_json_strict(claim.at(0)["response_body"].as<std::string>(), stored) &&
                          claim.at(0)["response_status"].as<int>() == 201;
      rollback_quietly(trans);
      if (!usable) {
        LOG_ERROR << "idempotency replay without usable stored body, request_id=" << rid;
        co_return error_response("INTERNAL_ERROR", "unexpected server error", rid);
      }
      co_return pairing_code_response(stored, rid);
    }
    if (outcome != "NEW") {
      rollback_quietly(trans);
      co_return error_response("INTERNAL_ERROR", "unexpected server error", rid);
    }

    // Check child existence and family
    auto child_res = co_await trans->execSqlCoro(
        "SELECT family_id::text AS family_id FROM ap_m1.children WHERE id = $1::uuid", *normalized_child);
    if (child_res.empty()) {
      rollback_quietly(trans);
      co_return error_response("NOT_FOUND", "child not found", rid);
    }
    const std::string family_id = child_res.at(0)["family_id"].as<std::string>();

    // Check PAIR_DEVICE authority scope
    auto scope_res = co_await trans->execSqlCoro(
        "SELECT ap_m1.has_child_scope_v2($1::uuid, 'PAIR_DEVICE') AS allowed", *normalized_child);
    if (scope_res.empty() || !scope_res.at(0)["allowed"].as<bool>()) {
      rollback_quietly(trans);
      co_return error_response("FORBIDDEN", "caller lacks PAIR_DEVICE scope for this child", rid);
    }

    // Check if an unexpired unconsumed code already exists (409 Conflict)
    auto active_res = co_await trans->execSqlCoro(
        "SELECT id::text AS id FROM ap_m1.pairing_codes "
        "WHERE child_id = $1::uuid AND consumed_at IS NULL AND expires_at > clock_timestamp()",
        *normalized_child);
    if (!active_res.empty()) {
      rollback_quietly(trans);
      co_return error_response("CONFLICT", "an unexpired pairing code already exists for this child", rid);
    }

    // Generate pairing code
    const std::string raw_code = generate_pairing_code();
    const Sha256 code_hash = sha256_bytes(raw_code);
    const std::string code_hex = to_pg_bytea(code_hash);

    auto ins_res = co_await trans->execSqlCoro(
        "INSERT INTO ap_m1.pairing_codes(family_id, child_id, code_sha256, expires_at, issued_by) "
        "VALUES($1::uuid, $2::uuid, $3::bytea, clock_timestamp() + interval '10 minutes', $4::uuid) "
        "RETURNING to_char(expires_at AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"') AS expires_iso",
        family_id, *normalized_child, code_hex, principal);

    const std::string expires_iso = ins_res.at(0)["expires_iso"].as<std::string>();

    Json::Value result;
    result["pairing_code"] = raw_code;
    result["expires_at"] = expires_iso;
    result["child_id"] = *normalized_child;

    auto rec = co_await trans->execSqlCoro(
        "SELECT ap_m1.idempotency_record($1::uuid, $2, $3::bytea, 201, $4::jsonb) AS ok",
        principal, std::string(kPairingCodeNamespace), key_hex, canonical_json(result));
    if (!rec.at(0)["ok"].as<bool>()) {
      rollback_quietly(trans);
      LOG_ERROR << "idempotency_record refused, request_id=" << rid;
      co_return error_response("INTERNAL_ERROR", "unexpected server error", rid);
    }

    if (!(co_await commit(std::move(trans)))) {
      LOG_ERROR << "commit failed, request_id=" << rid;
      co_return error_response("SERVICE_UNAVAILABLE", "database commit unavailable; retry the same request", rid, true);
    }
    co_return pairing_code_response(result, rid);

  } catch (const orm::SqlError& e) {
    rollback_quietly(trans);
    LOG_ERROR << "sql error state=" << e.sqlState() << " request_id=" << rid;
    co_return response_for_sqlstate(e.sqlState(), rid);
  } catch (const orm::TimeoutError&) {
    rollback_quietly(trans);
    co_return error_response("SERVICE_UNAVAILABLE", "database deadline exceeded", rid, true);
  } catch (const orm::BrokenConnection&) {
    rollback_quietly(trans);
    co_return error_response("SERVICE_UNAVAILABLE", "database unavailable", rid, true);
  } catch (const std::exception&) {
    rollback_quietly(trans);
    LOG_ERROR << "unexpected exception, request_id=" << rid;
    co_return error_response("INTERNAL_ERROR", "unexpected server error", rid);
  }
}

}  // namespace ma
