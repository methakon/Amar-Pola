# M1 stack PR #9 — independent review and PostgreSQL16 evidence

**Date:** 2026-10-30. **Status:** REVIEW_COMPLETE / FINDINGS_OPEN; owner merge approval NOT_REQUESTED_BY_AUTOMATION / NOT_GRANTED. **Scope:** source review, verified hosted CI and independent synthetic local SQL execution; not production, legal, Android or authentication acceptance. Proposed review owners: backend/security; independent sign-off unassigned. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md) · [Current blockers](../../M0-foundation-and-approvals/01-project-governance/BLOCKERS_AND_OWNER_DECISIONS.md).

[Machine-readable execution record](../../../../evidence/local/reviews/PR9_REVIEW_2026-10-30.json) preserves commands, exit codes, source SHA and local/hosted scope; no private logs or credentials are committed.

## 1. Baseline and verdict

- Repository: `methakon/Madalasa-Alarka`.
- [PR #9](https://github.com/methakon/Madalasa-Alarka/pull/9): OPEN, head `c693899e4b411cbadd1639f0bcb642844af50ea9`, base main `0a6be11ca811e842cc9839ab623ec118514020dd`. Rechecked unchanged during review. GitHub reports mergeable/CLEAN; **mergeability is not approval**.
- Reused documentation branch `audit/2026-10-29-final-screen-api-db-reconciliation` / existing [PR #2](https://github.com/methakon/Madalasa-Alarka/pull/2). Its newer owner decisions were locally merged without dropping the pre-existing index commit or signing work. No new branch or PR merge occurred.
- PR9's tree equals `feat/m1-purge-jobs`; 37 files changed against main, +3,041/−106. It carries the intended #3–#8 **content**, but not all historical merge nodes.
- **Verdict:** useful, tested M1 stack integration, not complete M1/product readiness. Report and fix/review the findings below before owner decides on merge. Do not imply that default-deny authentication is working ParentOIDC, that synthetic headers prove identity, or that this schema supports approved blended-family V2.

## 2. Stack ancestry and source preservation

All local/remote branch refs and open PRs were inspected after fetch. Local branch named `main` is stale; every comparison here uses fetched `origin/main`, not that local branch.

| PR | Content head is ancestor of PR9? | Recorded merge node in PR9 ancestry? | What actually happened |
|---|---|---|---|
| #3 credential/enrollment | `3f6cd01`: yes | `0a6be11`: no | Main includes #3; PR9 contains its content without main's merge node |
| #4 backend/idempotency | `ddbb25a`: yes | `2821a8a`: no | Merged into #3 branch after #3 had already merged |
| #5 physical catalog | `976805d`: yes | `ddbb25a`: yes | Included through #4's ancestry; not independently on main |
| #6 G-6 lint | `48318b2`: yes | `58ba650`: no | Merged into backend feature branch |
| #7 createFamily | `92d4803`: yes | `62a33a6`: no | Merged into G-6 feature branch |
| #8 purge jobs | `6106542`: yes | `c693899`: yes | Merged into createFamily; this is PR9 head |

`git merge-base origin/main <PR9 head>` is `3f6cd01`; migrations 0001–0003 are unchanged against main; 0004 and 0005 are additions. Thus PR9 solves the intended missing-content problem; a closed stacked PR did not by itself place that content on main. #1 six-gate handoff and #2 documentation audit remain separate open PRs, each with successful current documentation check.

## 3. Findings requiring attention

Line references below bind to PR9 head, not this documentation worktree. Static findings are explicitly not reported as locally reproduced HTTP failures.

| Severity / ID | Evidence | Consequence and proposed correction | Verification state |
|---|---|---|---|
| HIGH / PR9-01 | `backend/tests/integration_families.sh:17`: `kill ${PID:-0} ${PID2:-0}` | Before either child PID is assigned, or before PID2 starts, cleanup can signal process group 0, terminating the caller/siblings and interrupting DB cleanup. Kill/wait only validated positive PIDs actually started by this script. Run failure-path tests in a separate process group until repaired | STATIC_CONFIRMED; dangerous failure path deliberately not executed locally |
| MEDIUM / PR9-02 | `backend/src/families.h:52–53`; `main.cc:40–58` | `getDbClient("ma")` is called before testing existence. The pinned dependency asserts a missing named client in assertion-enabled builds; the null check and later try do not protect this path. Check `hasDbClient()` first and add authenticated-valid-request/no-DB regression | STATIC_REVIEW; no local binary reproduction. Existing second HTTP instance stops at 401, so does not exercise promised 503 |
| MEDIUM / PR9-03 | `.github/workflows/m1-contract-and-tenant.yml:137–139` | `strings binary \| grep -q synthetic_test` inside `if`, under Bash pipefail, can receive SIGPIPE upstream and skip its failure branch even when marker exists. Consume all output or inspect captured output; add a known-synthetic negative control | **REPRODUCED LOCALLY** using a large synthetic marker fixture: existing pattern exits 0 (miss); full-consumption grep alternative detects it (sentinel exit42). This demonstrates a gate defect, not that deployed auth is bypassed |
| MEDIUM / PR9-04 | `main.cc:49–54`, `families.h:59–60` | Client timeout is unset (`-1.0`); only DB lock_timeout is set after acquiring a transaction. No effective bounded acquisition/request/statement deadline for unavailable DB or pool exhaustion. Introduce finite deadlines and retryable dependency errors with unavailable-DB/slow-query/pool tests | STATIC_CONFIRMED configuration gap; no local outage/load run |
| MEDIUM / M1-INHERITED-01 | `0003_m1_enrollment_and_credential_hardening.sql:133–145`; `0002_m1_device_credentials.sql:23–37` | Distinct consumed challenges lock different rows. Parallel renewal can each insert a live credential without a common device lock or unique live-device constraint, violating documented one-live-credential invariant. Serialize on device and add two-session distinct-challenge test | SOURCE_REVIEW; existing sequential rotation tests pass, concurrent invariant NOT_PROVEN. Inherited from main, not newly introduced by PR9 |
| MEDIUM / M1-INHERITED-02 | `0002_m1_device_credentials.sql:97–110` | Count-before-insert five-open-challenge bound has no per-device serialization; concurrent callers may exceed it. Add device-scoped serialization plus burst regression; this does not replace rate limiting | SOURCE_REVIEW; inherited from main; no concurrent reproduction claimed |
| RETENTION GAP / M1-RET-01 | `0003_m1_enrollment_and_credential_hardening.sql:173–180`; `docs/M1_PURGE_JOBS_RUNBOOK.md:19` | Enrollment cleanup is limited to abandoned PENDING_PROOF devices. Completed enrollment challenges on active/revoked devices and pairing-code rows lack equivalent cleanup here. Do not call two purge jobs complete artifact/data retention; align lifecycle wording and approved per-category TTLs | SOURCE_CONFIRMED; current narrow purge tests pass |

The inherited use of transaction-frozen `now()` in credential/challenge windows also deserves the real-elapsed-time/row-lock regressions listed in T-PEND-04. Published SQL must not be silently edited to hide review findings; reconcile additive fixes with the existing namespaced migration policy.

## 4. Authentication, authorization and createFamily trace

`backend/src/auth.h` explicitly lacks JWT issuer/audience/signature/JWKS/expiry validation. Normal build selects reject-all, not a permissive production identity provider. `MA_SYNTHETIC_AUTH` defaults OFF; test-only header authentication additionally needs its runtime switch. The CI exclusion test's flaw above weakens assurance, but is **not evidence of a production JWT bypass**. Provider validation is engineering work that need not wait for Payments identity verification; real-provider acceptance needs separately authorized configuration.

The database trusts the verified backend: `resolve_parent_principal` accepts asserted issuer/subject; session GUCs and idempotency actor IDs are supplied by the DB caller. SQL helpers do not independently authenticate an adult, verify age, establish parenthood or legal guardian authority. Google Sign-In does not supply Family Link relationship proof.

Positive createFamily flow: body limit → strict syntax/idempotency UUID/JSON shape → authentication → label bounds → principal resolution → transaction-local principal → claim → family plus OWNER membership → recorded 201 response → awaited database commit. Values are bound parameters; raw key is hashed, mismatch response does not expose stored data, replay precedes cap and receives a fresh request ID. Family cap uses a transaction advisory lock. Error text is not leaked. These are source/CI-supported properties, not a claim of all 11 M1 HTTP operations implemented.

Only `/healthz` and `POST /v1/families` are registered in this PR. The whole-project 171-operation OpenAPI and 120 conceptual entities remain design scope, not implemented handler/table counts. No admin application or broad HMVC domain/worker implementation is established by a small header-based skeleton; maintain the approved C++20 Drogon modular/SOLID boundaries as work expands.

## 5. Fresh PostgreSQL16 execution — independent local evidence

Source was exported from the exact Git commit with `git archive`, without checking out or altering PR9. A newly created disposable database was used; the existing V2 development/test data was not contacted or reset.

Environment: PostgreSQL **16.15**, cached image ID `sha256:1a6ab3f5345eb6dbe04a1349529caabdb0ab09293a09590fad07b2246bfa4b54`; isolated container `madalasa-pr9-review-pg16`, network mode **none**, **no published ports**, local Unix socket, 1 CPU/512MiB RAM, 384MiB tmpfs database. Durability options were not disabled. SQL was invoked with `psql -X -v ON_ERROR_STOP=1` against `madalasa_pr9_review`. Test roles/password literals in upstream scripts are public synthetic fixtures, not generated production credentials.

Explicit replay order (not a directory-wide V2 glob):

1. `0001_m1_identity.sql`
2. `0002_m1_device_credentials.sql`
3. `0003_m1_enrollment_and_credential_hardening.sql`
4. `0004_m1_idempotency.sql`
5. `0005_m1_family_provisioning.sql`

| Command/check | Local result |
|---|---|
| `python3 backend/tests/lint_openapi_m1.py docs/openapi-m1.yaml` | Exit0 |
| `python3 backend/tests/check_physical_catalog.py` | Exit0 |
| `python3 backend/tests/lint_openapi_full.py` | Exit0: 171 draft operations,155 paths,187 screens,120 conceptual tables |
| `/usr/bin/python3 -m unittest backend.tests.test_physical_catalog backend.tests.test_lint_openapi_m1 backend.tests.test_deploy_units backend.tests.test_error_catalog_sync -v` | **61 tests PASS**, exit0 |
| Five explicit migration commands above | All exit0 |
| `m1_tenant_isolation.sql`, `m1_credential_lifecycle.sql`, `m1_enrollment.sql`, `m1_idempotency.sql`, `m1_family_provisioning.sql` | All five exit0 |
| `bash backend/tests/m1_idempotency_concurrency.sh` | Exit0: block→replay, rollback ownership handover, lock timeout |
| `bash backend/tests/purge_job.sh` | Exit0: expired/recent, repeat, exact grants, denied role, unreachable DB, bounded lock wait |
| New [m1_security_catalog_acceptance.sql](../../../../backend/tests/m1_security_catalog_acceptance.sql) | Exit0: catalog assertions and three deliberate drift controls detected/rolled back; wrong-database invocation exit3 before catalog mutation |

Initial local tooling attempts are not concealed: the default tool Python lacked PyYAML and one shell lacked psql on PATH. The first mixed unittest run had 58 tests/one import error; system Python with existing PyYAML and explicit rootless client paths produced the successful 61-test run above. No application test was weakened. Local native rebuild/outage tests were not attempted while system-wide I/O pressure was high; verified exact-head hosted evidence is reported separately below.

Observed live catalog: **18 ap_m1 base tables**, each ENABLE+FORCE RLS and owned by `ap_m1_owner`. `ap_m1_api`: NOLOGIN in migrations, NOSUPERUSER/NOBYPASSRLS/no role membership. `ap_m1_auth`: intentionally BYPASSRLS, but NOLOGIN/NOSUPERUSER, constrained function ownership/grants and fixed `pg_catalog, ap_m1` search path. PUBLIC has no application function EXECUTE or table grants. Do not claim every role is NOBYPASSRLS, or that superuser-run assertions alone prove tenant isolation: separate suites actually SET ROLE for denied behavior.

The new rollback-only controls remove FORCE RLS, grant PUBLIC create_family execution and grant runtime BYPASSRLS one at a time; each is detected and rolled back, then the clean catalog is rechecked. They validate the detector, not a product migration. The script refuses databases outside its dedicated review naming scope.

## 6. Hosted Actions evidence and older failures

[Run 41014540240](https://github.com/methakon/Madalasa-Alarka/actions/runs/41014540240), head `c693899e4b411cbadd1639f0bcb642844af50ea9`, pull_request event, 2026-10-30: **SUCCESS**. Job step metadata and logs were read, not inferred from a badge.

- `contracts-and-isolation`: five migrations, tenant/credential/enrollment/idempotency/family SQL, idempotency concurrency, purge, deploy-unit and error-catalog checks all successful.
- `backend-build`: pinned dependency build, backend compile, CTest **1/1**, HTTP smoke, deployable-marker gate, separate synthetic test build and end-to-end createFamily all successful. HTTP integration logs cover validation, replay/mismatch, principal separation, hashed keys, eight-way duplicate concurrency, cap and error envelopes. These synthetic results do not validate ParentOIDC. The marker gate's negative-control defect remains despite its successful check.
- [Documentation run 41014540218](https://github.com/methakon/Madalasa-Alarka/actions/runs/41014540218): SUCCESS.

Inspection of the latest **100 runs** found three older failures: run `40882818566` on DB branch revision `3d3e285` failed the full-contract conceptual DB table count; runs `40831057258` and `40831051347` on old catalog revision `31573ae` failed catalog checks. Logs from the DB failure and one duplicate catalog failure were inspected. These do not make the current PR9 head red; conversely PR9 green does not certify the separate latest V2 branch or erase historical failures. Its newer local evidence must remain separately scoped.

## 7. Canonical contract/schema conflicts and six gates

The six-gate handoff was read at existing PR1 head `59125d402b07c20aaf6ecb13d69542997223bedf`, where it lives; it is not silently claimed merged into the documentation branch. [Pinned handoff source](https://github.com/methakon/Madalasa-Alarka/blob/59125d402b07c20aaf6ecb13d69542997223bedf/docs/roadmap/SIX_GATE_OWNER_DECISIONS_AND_AGENT_HANDOFF_2026-10-29.md).

- M1 `child_guardian_grants` remains family-membership-bound, incompatible with the approved [exact-child blended-family V2 ADR](../03-security-and-permissions/ADR_2026_10_28_BLEND_FAMILY_V2_AND_NO_FAMILY_LINK_DEPENDENCY.md). It is a historical baseline, not safe external co-parent release behavior.
- Separate DB branch `b507e5f` contains the existing explicit namespaced manifest and additive V2 through0019. PR9's original M1 **0005 family provisioning** is newer than that manifest's historical M1 tail0004, and collides numerically with V2's 0005 location migration. Integrate semantically through the existing manifest/bridge model; never alphabetically combine files, renumber published SQL or assume the different backend/catalog implementations already agree.
- The catalog's 18 physical tables are not 120 conceptual tables to auto-generate. PR9's full-contract lint passing verifies draft joins/counts only.
- Auth, consent/authority, retention/deletion, prepaid seat/provider acceptance and Android evidence remain separate gaps. Hosting/egress choices are deployment gates, not prerequisites for portable synthetic engineering.
- G-7 parser-level oversized requests above1MiB still receive Drogon's bare413 before ordinary request advice; the comment/test documents this. A future deployed proxy/body-size normalization contract needs actual acceptance, not an assumption that all errors already share one envelope.

## 8. Required follow-up and prohibited inference

1. Fix guarded positive-PID cleanup and prove failure cleanup cannot signal the caller.
2. Fix fail-open marker pipeline and prove the actual synthetic binary is rejected.
3. Guard absent DB client and bound acquisition/statement/request time; add outage/pool tests.
4. Add serialized credential renewal/challenge-limit regressions and clarify artifact purge coverage using additive migration discipline.
5. Review real ParentOIDC/JWKS implementation and separate legal guardian authority; no Family Link API dependency.
6. Owner reviews these findings before any PR9 merge. Reconcile M1 0005, V2 grants/manifests and backend/contracts without duplicating published histories.

No infrastructure deployment, Android implementation, new production credentials, real-child processing, Console declaration/payment change, Android app build, purchase or PR merge was performed. Product/production/legal/Play readiness remains **NOT_READY**; the tested local/CI slices are **VERIFIED only within their stated scope**.
