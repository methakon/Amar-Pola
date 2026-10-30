// In-process HTTP handler integration with real ephemeral RSA signatures.
// This executable has no MA_SYNTHETIC_AUTH definition and is never deployed.
#include <cstdlib>
#include <iostream>
#include <memory>
#include <atomic>
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include "google_oidc.h"
#include "google_jwks.h"
#include "auth.h"
#include "families.h"

static int failures = 0;
#define CHECK(c) do { if (!(c)) { std::cerr << "FAIL line " << __LINE__ << ": " #c "\n"; ++failures; } } while (0)
static std::string encode(std::string_view bytes) {
  std::string out(4*((bytes.size()+2)/3)+4, '\0');
  const int n=EVP_EncodeBlock(reinterpret_cast<unsigned char*>(out.data()),
      reinterpret_cast<const unsigned char*>(bytes.data()), static_cast<int>(bytes.size()));
  out.resize(n);
  while (!out.empty() && out.back()=='=') out.pop_back();
  for (char& c:out) { if (c=='+') c='-'; else if(c=='/') c='_'; }
  return out;
}
static std::string sign(EVP_PKEY* key, const Json::Value& payload) {
  const std::string input=encode(R"({"alg":"RS256","kid":"http-fixture","typ":"JWT"})")+"."+encode(ma::canonical_json(payload));
  std::unique_ptr<EVP_MD_CTX, decltype(&EVP_MD_CTX_free)> ctx(EVP_MD_CTX_new(), EVP_MD_CTX_free);
  if (!ctx || EVP_DigestSignInit(ctx.get(),nullptr,EVP_sha256(),nullptr,key)!=1 ||
      EVP_DigestSignUpdate(ctx.get(),input.data(),input.size())!=1) throw std::runtime_error("fixture signing failed");
  std::size_t n=0;
  if (EVP_DigestSignFinal(ctx.get(),nullptr,&n)!=1) throw std::runtime_error("fixture signature size failed");
  std::string sig(n,'\0');
  if (EVP_DigestSignFinal(ctx.get(),reinterpret_cast<unsigned char*>(sig.data()),&n)!=1) throw std::runtime_error("fixture signature failed");
  sig.resize(n); return input+"."+encode(sig);
}
static drogon::HttpRequestPtr request(const std::string& authorization) {
  auto req=drogon::HttpRequest::newHttpRequest();
  req->setMethod(drogon::Post); req->setPath("/v1/families");
  req->setContentTypeCode(drogon::CT_APPLICATION_JSON);
  req->addHeader("idempotency-key","88a3cd84-a951-4c7b-a173-0cd0708d7fa1");
  if (!authorization.empty()) req->addHeader("authorization",authorization);
  req->setBody(R"({"label":"Synthetic signed OIDC HTTP fixture"})");
  return req;
}
int main() {
  using namespace ma;
  std::unique_ptr<EVP_PKEY_CTX, decltype(&EVP_PKEY_CTX_free)> keyctx(EVP_PKEY_CTX_new_from_name(nullptr,"RSA",nullptr),EVP_PKEY_CTX_free);
  EVP_PKEY* raw=nullptr;
  if (!keyctx || EVP_PKEY_keygen_init(keyctx.get())!=1 ||
      EVP_PKEY_CTX_set_rsa_keygen_bits(keyctx.get(),2048)!=1 || EVP_PKEY_generate(keyctx.get(),&raw)!=1) return 2;
  OidcPublicKey key(raw,EVP_PKEY_free);
  GoogleOidcConfig config{{"http-fixture-client"},{},0};
  auto lookup=[key](const std::string& kid) { return kid=="http-fixture"?key:OidcPublicKey{}; };
  Json::Value claims(Json::objectValue);
  claims["iss"]="https://accounts.google.com"; claims["sub"]="synthetic-opaque-subject";
  claims["aud"]="http-fixture-client"; claims["iat"]=Json::Int64(1700000000);
  claims["exp"]=Json::Int64(1700003600);
  auto now=[] { return std::int64_t{1700000100}; };
  auto auth=make_google_oidc_authenticator(config,lookup,{},now);
  auto signed_token=sign(key.get(),claims);
  auto req=request("Bearer "+signed_token);
  auto principal=auth(req);
  CHECK(principal && principal->issuer=="https://accounts.google.com" && principal->subject=="synthetic-opaque-subject");
  // An accepted identity reaches the real next stage (missing DB), not an invented 201.
  auto accepted=drogon::sync_wait(create_family(req,auth));
  CHECK(accepted->statusCode()==drogon::k503ServiceUnavailable);
  CHECK(accepted->getJsonObject() && (*accepted->getJsonObject())["code"]=="SERVICE_UNAVAILABLE");
  for (const auto& header:std::vector<std::string>{"", "Bearer", "Basic "+signed_token,
       "Bearer "+signed_token+",other", "Bearer "+signed_token+" ", "Bearer a.b.c"}) {
    auto rejected=drogon::sync_wait(create_family(request(header),auth));
    CHECK(rejected->statusCode()==drogon::k401Unauthorized);
  }
  auto denied=make_google_oidc_authenticator(config,lookup,[](const OidcIdentity&) {return false;},now);
  CHECK(drogon::sync_wait(create_family(req,denied))->statusCode()==drogon::k401Unauthorized);
  std::atomic<unsigned> fetch_calls{0};
  auto unavailable_cache=std::make_shared<GoogleJwksCache>([&fetch_calls](std::stop_token) {
    ++fetch_calls; return std::optional<GoogleJwksResponse>{};
  });
  auto unavailable=make_google_oidc_authenticator(config,
      [unavailable_cache](const std::string& kid) {return unavailable_cache->key(kid);}, {}, now);
  CHECK(drogon::sync_wait(create_family(req,unavailable))->statusCode()==drogon::k401Unauthorized);
  CHECK(unavailable_cache->wait_for_idle(std::chrono::seconds(1)));
  CHECK(fetch_calls==1);
  CHECK(drogon::sync_wait(create_family(req,unavailable))->statusCode()==drogon::k401Unauthorized);
  claims["parent"]=true; claims["guardian"]=true; claims["adult"]=true; claims["role"]="OWNER";
  auto authority_claims=auth(request("Bearer "+sign(key.get(),claims)));
  CHECK(authority_claims && authority_claims->subject==principal->subject);
  // Principal's only fields remain issuer and subject. No authority is derived.
  unsetenv("MA_GOOGLE_OIDC_AUDIENCE"); unsetenv("MA_GOOGLE_OIDC_PRESENTERS");
  setenv("MA_AUTH_MODE","synthetic_test",1);
  auto default_auth=select_authenticator();
  auto header_only=request(""); header_only->addHeader("x-synthetic-subject","cannot-authenticate-production-composition");
  CHECK(!default_auth(header_only)); CHECK(!default_auth(req));
  setenv("MA_GOOGLE_OIDC_AUDIENCE","client,",1);
  bool invalid=false;
  try { (void)select_authenticator(); } catch(const std::invalid_argument&) {invalid=true;}
  CHECK(invalid);
  unsetenv("MA_GOOGLE_OIDC_AUDIENCE"); unsetenv("MA_AUTH_MODE");
  if (failures) return 1;
  std::cout << "OIDC in-process HTTP integration PASS\n";
  return 0;
}
