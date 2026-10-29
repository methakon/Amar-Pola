// Database helpers for handlers: awaited commit, explicit rollback, SQLSTATE to catalog mapping.
#pragma once
#include <coroutine>
#include <memory>
#include <string>

#include <drogon/drogon.h>
#include <drogon/orm/DbClient.h>

#include "http_support.h"

namespace ma {

inline constexpr const char* kDbClientName = "ma";

// Drogon commits when the last reference to a Transaction is released, and reports the outcome through a callback.
// Awaiting that callback means the handler never answers 2xx before the commit is confirmed by the server.
struct CommitAwaiter {
  std::shared_ptr<drogon::orm::Transaction> trans;
  bool ok{false};
  bool await_ready() const noexcept { return false; }
  void await_suspend(std::coroutine_handle<> h) {
    auto t = std::move(trans);
    t->setCommitCallback([this, h](bool success) {
      ok = success;
      h.resume();
    });
    t.reset();  // releases the last reference: Drogon sends COMMIT
  }
  bool await_resume() const noexcept { return ok; }
};

inline CommitAwaiter commit(std::shared_ptr<drogon::orm::Transaction> t) { return CommitAwaiter{std::move(t)}; }

inline void rollback_quietly(const std::shared_ptr<drogon::orm::Transaction>& t) noexcept {
  try {
    if (t) t->rollback();
  } catch (...) {
  }
}

// Maps a PostgreSQL SQLSTATE raised by our functions to a catalog response. Never forwards database text to the client.
inline drogon::HttpResponsePtr response_for_sqlstate(const std::string& state, const std::string& rid) {
  if (state == "55P03" || state == "40001")  // lock timeout, or a claim that raced with cleanup: retry the same request
    return error_response("CONFLICT", "another identical request is still in progress; retry", rid, true);
  if (state == "53400") return error_response("VALIDATION_FAILED", "account limit reached", rid);
  if (state == "23514") return error_response("VALIDATION_FAILED", "value out of range", rid);
  if (state == "22021" || state == "22P05") return error_response("INVALID_REQUEST", "invalid character in request", rid);
  return error_response("INTERNAL_ERROR", "unexpected server error", rid);
}

}  // namespace ma
