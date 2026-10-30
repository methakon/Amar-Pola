// Authentication and offline dependency failures for M1 listChildren.
// No simulated successful DB result; synthetic identity is confined to this test executable.
#include <drogon/drogon.h>
#include "children_read.h"
#include "parent_reads.h"
#include "children_create.h"
#include <iostream>
#include <optional>

int main() {
  auto request = [] {
    auto req = drogon::HttpRequest::newHttpRequest();
    req->setMethod(drogon::Get);
    req->setPath("/v1/families/00000000-0000-4000-8000-000000000001/children");
    return req;
  };
  ma::Authenticator allow = [](const drogon::HttpRequestPtr&) -> std::optional<ma::Principal> {
    return ma::Principal{"https://synthetic.invalid", "test-only-principal"};
  };
  ma::Authenticator deny = ma::reject_all_authenticator();
  const std::string good_id = "00000000-0000-4000-8000-000000000001";
  int failed = 0;
  auto check = [&](bool ok, const char* label) {
    if (!ok) { std::cerr << "FAIL " << label << '\n'; ++failed; }
  };
  auto invalid = drogon::sync_wait(ma::list_children(request(), "not-a-uuid", allow));
  check(invalid->statusCode() == drogon::k400BadRequest, "invalid family UUID");
  auto unauth = drogon::sync_wait(ma::list_children(request(), good_id, deny));
  check(unauth->statusCode() == drogon::k401Unauthorized, "unauthenticated family read");
  auto unavailable = drogon::sync_wait(ma::list_children(request(), good_id, allow));
  check(unavailable->statusCode() == drogon::k503ServiceUnavailable, "fail closed without DB");
  check(unavailable->getJsonObject() &&
        (*unavailable->getJsonObject())["code"] == "SERVICE_UNAVAILABLE",
        "catalog error, not invented family data");
  const auto fam = drogon::sync_wait(ma::list_families(request(), deny));
  check(fam->statusCode() == drogon::k401Unauthorized,"listFamilies requires ParentOIDC");
  const auto unavailable_fam = drogon::sync_wait(ma::list_families(request(), allow));
  check(unavailable_fam->statusCode() == drogon::k503ServiceUnavailable,"listFamilies denies without DB");
  const auto child_bad = drogon::sync_wait(ma::get_child(request(),"not-a-uuid",allow));
  check(child_bad->statusCode() == drogon::k400BadRequest,"getChild invalid UUID");
  const auto child_noauth = drogon::sync_wait(ma::get_child(request(),good_id,deny));
  check(child_noauth->statusCode() == drogon::k401Unauthorized,"getChild requires ParentOIDC");
  const auto child_offline = drogon::sync_wait(ma::get_child(request(),good_id,allow));
  check(child_offline->statusCode() == drogon::k503ServiceUnavailable,"getChild denies without DB");
  const auto devices_bad = drogon::sync_wait(ma::list_child_devices(request(),"not-a-uuid",allow));
  check(devices_bad->statusCode() == drogon::k400BadRequest,"listChildDevices invalid UUID");
  const auto devices_noauth = drogon::sync_wait(ma::list_child_devices(request(),good_id,deny));
  check(devices_noauth->statusCode() == drogon::k401Unauthorized,"listChildDevices requires ParentOIDC");
  const auto devices_offline = drogon::sync_wait(ma::list_child_devices(request(),good_id,allow));
  check(devices_offline->statusCode() == drogon::k503ServiceUnavailable,"listChildDevices denies without DB");
    // Frozen createChild negative matrix — synthetic identity only.
  auto create_req = [&] {
    auto q=request();
    q->setMethod(drogon::Post);
    q->setContentTypeCode(drogon::CT_APPLICATION_JSON);
    q->addHeader("idempotency-key","00000000-0000-4000-8000-000000000003");
    q->setBody(R"({"alias":"Synthetic profile"})");
    return q;
  };
  auto create_bad= drogon::sync_wait(ma::create_child(create_req(),"invalid",allow));
  check(create_bad->statusCode()==drogon::k400BadRequest,"createChild path check");
  auto create_anon= drogon::sync_wait(ma::create_child(create_req(),good_id,deny));
  check(create_anon->statusCode()==drogon::k401Unauthorized,"createChild requires ParentOIDC");
  auto create_offline= drogon::sync_wait(ma::create_child(create_req(),good_id,allow));
  check(create_offline->statusCode()==drogon::k503ServiceUnavailable,"createChild denies without DB");
  auto invalid_alias=create_req();
  invalid_alias->setBody(R"({"alias":"not","unexpected":1})");
  auto malformed=drogon::sync_wait(ma::create_child(invalid_alias,good_id,allow));
  check(malformed->statusCode()==drogon::k400BadRequest,"createChild unknown field rejected");
    if (failed) return 1;
  std::cout << "M1 children list negative tests PASS\n";
  return 0;
}
