# Test Strategy — Unit, Integration, Android, Load, Security and Recovery

> **Document control:** M8 / 03-quality-and-evidence · Proposed owner: QA + security (not assigned) · Registry: DOCUMENTED_REVIEW_PENDING; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

**Status:** Formal proposed QA strategy, separate from current validation/test-case docs. No claim that these test suites run yet. Current CI executes M1 structural OpenAPI + PostgreSQL synthetic cross-tenant test only.

## Test pyramid
| Level | Coverage and tooling (planned) | Mandatory release evidence |
|---|---|---|
| Unit: Kotlin | Permission state reducer, location queue/TTL, media reason mapping, UsageStats interval reconstruction, date/cursor logic | Deterministic synthetic tests, Android fake OS boundaries |
| Unit: C++20 | Batch parsing, time/lat/lon normalization, child scope, digest/replay, statuses, lease fencing, trip simplification | CTest/gtest or approved C++ harness, sanitizers |
| DB/integration | M1 forced RLS; ungranted sibling, revoke; Tx A inbox ACK, Tx B bulk insert/rollback/outbox; retention/tombstones | Real disposable Postgres 16/PostGIS when relevant, seeded synthetic families |
| Android device/OEM | API29–36+ Pixel/Samsung/OEM, separate foreground/background location, Android 11+ one-time permissions, FGS/notifications, managed vs ordinary install; watch phone-proxied GPS | Build/version and screenshots/logs without child data |
| API/E2E | Signed Android enrollment, child-scoped reads, parent UI stale/offline, app usage quality, SOS status, admin case/search auditing | Reproducible synthetic fixture/signed build/test account |
| Load/soak | 1k/10k/100k simulated devices, 48h backlog reconnection, GPS 1–2min upload target when eligible, query p95, WAL/IOPS, direct bulk vs inbox | Measured environment sizing, dashboards, reproducible seed |
| Security | STRIDE, SAST/SCA/SBOM, fuzz malformed JSON, BOLA/IDOR, mobile MASVS, key handling, scoped admin tests and penetration tests | Independent reviewed findings and remediations |
| Operations | Worker restart, disk-full, postgres failover, backup restore RPO/RTO, inbox 202 receipt/Tx B loss/dedup, deletion after restore | Dated evidence file, SQL counts, RPO/RTO result and responsible signature |
| Legal/policy | Explicit features-off tests for under-18 India/Play blocked functions; reviewer material validity | Counsel and Play decision, release signoff |

## Quality gates
Security blocker when cross-family child data leaks, precise GPS revealed to ungranted sibling, unsupported covert capture, admin case bypass, invalid 202 before durable commit, deleted child data resurrected from 48h local queue, insecure keys, missing visible monitoring. Don't treat flaky tests as passed. Pin OS emulator snapshots and record real device OS/OEM.

**Evidence format:** test ID, requirement ID, commit SHA, environment build OS/device, synthetic data seed, exact commands, expected and actual, pass/fail/blocked, screenshots/logs (no PII), issue link, reviewer. Rate-limit and fuzz test in isolated env only.

## CI growth
Existing `.github/workflows/m1-contract-and-tenant.yml` stays intact. Add per-PR C++20 formatting/ASAN, Kotlin lint/test, full OpenAPI validator, secret scanning, vulnerability and SBOM checks **after corresponding projects/manifests exist**. Add dedicated staging workflow for migrations/backups and nightly synthetic load; no prod secret in fork PRs. All new T-ING/T-CAP/T-ADM/T-AUD test IDs are **planned NOT_TESTED**; never infer implementation from test-case files.

## Release evidence
Publish per-release test summary and explicitly enumerate not run tests, risk exceptions approved by owner/security/legal (none auto-approved), Play declarations, signed artifact hash, backup restore evidence, rollout and rollback proof. No real-minor pilot before gates.
