// Madalasa-Alarka M1 backend skeleton. Implements only the cross-cutting rules (request id, error envelope, health).
// Business routes are added against docs/openapi-m1.yaml in later changes. SYNTHETIC DATA ONLY.
#include <cstdlib>
#include <iostream>

#include <drogon/drogon.h>

#include "http_support.h"

int main() {
  using namespace drogon;
  const char* port_env = std::getenv("MA_LISTEN_PORT");
  const char* addr_env = std::getenv("MA_LISTEN_ADDR");
  const int port = port_env ? std::atoi(port_env) : 8080;
  const std::string addr = addr_env ? addr_env : "127.0.0.1";

  // Every request gets a fresh server-generated id before routing; every response carries it.
  app().registerPreRoutingAdvice([](const HttpRequestPtr& req, AdviceCallback&&, AdviceChainCallback&& next) {
    req->getAttributes()->insert(ma::kRequestIdAttr, ma::new_request_id());
    next();
  });
  app().registerPreSendingAdvice([](const HttpRequestPtr& req, const HttpResponsePtr& resp) {
    resp->removeHeader(ma::kRequestIdHeader);
    resp->addHeader(ma::kRequestIdHeader, ma::request_id_of(req));
  });

  // Liveness only: no database access, no data. Readiness is added with the database layer.
  app().registerHandler(
      "/healthz",
      [](const HttpRequestPtr&, std::function<void(const HttpResponsePtr&)>&& cb) {
        Json::Value j;
        j["status"] = "ok";
        cb(HttpResponse::newHttpJsonResponse(j));
      },
      {Get});

  // Unknown route or wrong method -> catalog format, never Drogon's HTML page.
  app().setDefaultHandler([](const HttpRequestPtr& req, std::function<void(const HttpResponsePtr&)>&& cb) {
    cb(ma::error_response("NOT_FOUND", "no such route", ma::request_id_of(req)));
  });
  app().setExceptionHandler([](const std::exception&, const HttpRequestPtr& req,
                               std::function<void(const HttpResponsePtr&)>&& cb) {
    // Never echo exception text: it may contain SQL or identifiers.
    cb(ma::error_response("INTERNAL_ERROR", "unexpected server error", ma::request_id_of(req)));
  });
  app().setClientMaxBodySize(64 * 1024);  // 413 PAYLOAD_TOO_LARGE is mapped in the body-size handler when routes exist

  app().addListener(addr, static_cast<uint16_t>(port));
  std::cout << "madalasa backend listening on " << addr << ":" << port << std::endl;
  app().run();
  return 0;
}
