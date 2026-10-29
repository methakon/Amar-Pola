// Authentication seam for ParentOIDC routes.
//
// NOT IMPLEMENTED: validation of real OIDC JWTs (issuer, audience, signature via JWKS, expiry). That needs the identity
// provider decision and its client registration, and it is the single most security-critical piece still missing.
// Until it exists the production default REJECTS EVERY REQUEST (401), so nothing can be done with a forged identity.
//
// A header-based authenticator for tests is compiled only with -DMA_SYNTHETIC_AUTH=ON (CMake option, default OFF) and is
// additionally switched on at run time by MA_AUTH_MODE=synthetic_test. A production build therefore cannot contain it.
#pragma once
#include <cstdlib>
#include <functional>
#include <optional>
#include <string>

#include <drogon/drogon.h>

namespace ma {

struct Principal {
  std::string issuer;
  std::string subject;
};

using Authenticator = std::function<std::optional<Principal>(const drogon::HttpRequestPtr&)>;

inline Authenticator reject_all_authenticator() {
  return [](const drogon::HttpRequestPtr&) -> std::optional<Principal> { return std::nullopt; };
}

#ifdef MA_SYNTHETIC_AUTH
// Test only: identity taken from X-Synthetic-Subject. Issuer is fixed and clearly fake.
inline Authenticator synthetic_authenticator() {
  return [](const drogon::HttpRequestPtr& req) -> std::optional<Principal> {
    const std::string& s = req->getHeader("x-synthetic-subject");
    if (s.empty() || s.size() > 200) return std::nullopt;
    return Principal{"https://synthetic.invalid", s};
  };
}
#endif

inline Authenticator select_authenticator() {
#ifdef MA_SYNTHETIC_AUTH
  const char* mode = std::getenv("MA_AUTH_MODE");
  if (mode && std::string(mode) == "synthetic_test") {
    LOG_WARN << "SYNTHETIC AUTHENTICATION ENABLED: test build only, never deploy";
    return synthetic_authenticator();
  }
#endif
  LOG_WARN << "OIDC validation is not implemented: all authenticated routes answer 401";
  return reject_all_authenticator();
}

}  // namespace ma
