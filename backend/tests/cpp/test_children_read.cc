// Authentication and offline dependency failures for M1 listChildren.
// No simulated successful DB result; synthetic identity is confined to this test executable.
#include <drogon/drogon.h>
#include "children_read.h"
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
  if (failed) return 1;
  std::cout << "M1 children list negative tests PASS\n";
  return 0;
}
