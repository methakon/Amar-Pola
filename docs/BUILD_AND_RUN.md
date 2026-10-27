# Build, Run and Verify — Current M1 / Future Android & Drogon

**Reviewed 2026-10-27 against the repository CI and files.** There is **no runnable Android Gradle project or C++20 Drogon server yet**. The only executable project baseline is M1 API structural lint + PostgreSQL identity/child-scope synthetic test. These commands are for **synthetic test data**, not a live child-monitoring app.

## Available tools
- Python 3.10+ with standard library. `backend/tests/lint_openapi_m1.py` uses `json.loads` and requires **no pip/PyYAML**. The `docs/openapi-m1.yaml` file is JSON formatted in a YAML filename.
- PostgreSQL **16** for parity with `.github/workflows/m1-contract-and-tenant.yml` (M1 migration targets PostgreSQL 15+). PostGIS is NOT required for `0001_m1_identity.sql`. Future GPS schema will need PostGIS.
- Docker optional; `psql` and `pg_isready` required for SQL test.

## Developer quick-start

```bash
git clone https://github.com/methakon/Madalasa-Alarka.git
cd Madalasa-Alarka
python3 backend/tests/lint_openapi_m1.py docs/openapi-m1.yaml
```

Expected beginning: `M1 OpenAPI structural lint PASS`. This verifies 11 designated API operations and reference consistency, **not endpoint implementation or full OpenAPI validation**.

## Disposable PostgreSQL M1 isolation tests

```bash
docker run -d --name ma-m1-pg \
  -e POSTGRES_PASSWORD=synthetic_test_only_password \
  -e POSTGRES_DB=amar_pola_m1 \
  -p 127.0.0.1:5432:5432 postgres:16

export PGHOST=127.0.0.1 PGPORT=5432 PGUSER=postgres
export PGPASSWORD=synthetic_test_only_password
export PGDATABASE=amar_pola_m1
pg_isready -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE"
psql -v ON_ERROR_STOP=1 -f backend/persistence/migrations/0001_m1_identity.sql
psql -v ON_ERROR_STOP=1 -f backend/tests/m1_tenant_isolation.sql

docker rm -f ma-m1-pg
unset PGPASSWORD
```

Use only a local disposable DB; avoid port collision or public network binding. Test SQL must execute as migration/test administrator, **not the app's runtime PostgreSQL superuser**. CI service uses `postgres:16`, `amar_pola_m1` and same psql migrations and tenant test. Failures require investigation, never relax RLS to make CI green.

## Planned, NOT runnable commands

No `backend/CMakeLists.txt`, Gradle wrapper, `android/alarka` or `android/madalasa` actual compiled projects exist as of review. When implemented, proposed build steps will be:

```bash
# FUTURE ONLY; these will fail today:
cmake -S backend -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
# In android/ AFTER creating a real Gradle wrapper and modules:
./gradlew :alarka:assembleDebug
./gradlew :madalasa:assembleDebug
```

The `android/` directory currently contains scoping README files, not runnable source. Android OS permission and identity must not be fabricated to satisfy a test. C++20 Drogon, PostGIS location inbox, lease workers, media command endpoints, dashboard and admin portal are design only.

## Server GPS ingestion future contract
Alarka's encrypted up-to-48h offline capacity queue + adaptive GPS captures original event timestamps separately from conditional 1–2min JSON upload. Drogon must ACK HTTP 202 only **after** durable PostgreSQL inbox Tx A commit; C++ leased workers combine GPS points into multirow/COPY-staged bulk Tx B committing dedup+PostGIS raw+trip outbox+processed inbox. No Redis mandatory. This is [MA-INGEST-ADR-004](POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md), not implemented code.

## CI coverage and security
Current workflow `.github/workflows/m1-contract-and-tenant.yml` runs structural API lint, synthetic SQL migration and family/sibling grants. It does **not** run Android OEM instrumentation, C++ builds, SAST, penetration tests, release signing, backup tests or real DPDP/Play approval. Do not put real child data, credentials, GPS or recordings in GitHub; `.env.example` contains placeholders only.

**Legal and operational go/no-go:** [DPIA](DPIA.md), [Retention](DATA_RETENTION_SCHEDULE.md), [Incident Response](INCIDENT_AND_BREACH_RESPONSE_PROCEDURE.md), [Security](../SECURITY.md), [Signoff](DEPLOYMENT_RELEASE_READINESS_CHECKLIST.md). Verify exact Android/Play target API and India phased DPDP law at actual release.
