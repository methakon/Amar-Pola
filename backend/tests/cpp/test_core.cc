#include <cstdlib>
#include <iostream>

#include "error_catalog.h"
#include "idempotency_key.h"

static int failures = 0;
#define CHECK(c) do { if (!(c)) { std::cerr << "FAIL line " << __LINE__ << ": " #c "\n"; ++failures; } } while (0)

int main() {
  using namespace ma;
  // catalog
  CHECK(kErrors.size() == 12);
  CHECK(find_error("NOT_FOUND")->http_status == 404);
  CHECK(find_error("RATE_LIMITED")->retryable);
  CHECK(find_error("SERVICE_UNAVAILABLE")->retryable);
  CHECK(!find_error("CONFLICT")->retryable);
  CHECK(!find_error("NOPE").has_value());
  for (std::size_t i = 0; i < kErrors.size(); ++i)
    for (std::size_t j = i + 1; j < kErrors.size(); ++j) CHECK(kErrors[i].code != kErrors[j].code);

  // uuid normalisation
  CHECK(normalize_uuid("1D000000-0000-4000-8000-00000000000A") == std::string("1d000000-0000-4000-8000-00000000000a"));
  CHECK(!normalize_uuid("").has_value());
  CHECK(!normalize_uuid("1d000000000040008000-00000000000a").has_value());
  CHECK(!normalize_uuid("1d000000-0000-4000-8000-00000000000g").has_value());
  CHECK(!normalize_uuid("1d000000-0000-4000-8000-00000000000a ").has_value());

  // sha256 known vector: sha256("abc")
  auto h = sha256_bytes("abc");
  CHECK(h[0] == 0xba && h[1] == 0x78 && h[31] == 0xad);
  CHECK(to_pg_bytea(h).rfind("\\xba7816bf", 0) == 0 && to_pg_bytea(h).size() == 66);
  // same key in different case hashes identically; non-uuid is rejected
  CHECK(hash_idempotency_key("1D000000-0000-4000-8000-00000000000A") ==
        hash_idempotency_key("1d000000-0000-4000-8000-00000000000a"));
  CHECK(!hash_idempotency_key("not-a-uuid").has_value());
  CHECK(!hex_to_sha256(std::string(63, 'a')).has_value());

  if (failures) return 1;
  std::cout << "core tests PASS\n";
  return 0;
}
