# Madalasa–Alarka — Single Canonical Implementation and Release Milestone Plan

> **Product names:** **Madalasa** (parent app), **Alarka** (child app). Desired repository name **Madalasa-Alarka** is **completed GitHub repository rename**. Use the verified new repository URL for all current documentation and integrations. [Naming rationale](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Document:** AP-PLAN-001 | **Date:** 2026-10-26 | **Version:** 1.0 | **Status:** plans consolidated; NO implementation/releases certified.
**AUTHORITATIVE plan:** This milestone numbering M0–M9 replaces older inconsistent M0–M7, M0–M9 and workstream-only numbering in SRS, Technical Specification, Validation, M1 Android/C++ and Market Feedback. Older documents remain technical annexes, not parallel schedules.

## Global gates that apply to every stage

1. Synthetic/test adult data only until Indian under-18 legal purpose, guardianship and actual storage/subprocessor approval. Preferred OCI **Mumbai**; fallback **Hyderabad**, conditional on availability, home region and revised cost estimate. See [India region decision](INDIA_REGION_AND_M0_OWNER_DECISION_GATE.md) and [DPDP](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md).
2. Each stage needs owning person(s), source commit SHA, automated tests, device/software test evidence, identified risks, security/privacy signoff and rollback. A design row is not proof of implementation.
3. No feature claims real-time observation, emergency delivery or managed Android control beyond measured OS/provider behavior. Media capture remains research/deferred.
4. No paid pilot before production child-data authority, true emergency fallback labeling, restore procedure and an approved operating budget/support service.

## Canonical M0–M9 roadmap

| Milestone | Workscope | Hard dependencies | Exit deliverables and acceptance |
|---|---|---|---|
| **M0 — Owner/legal/cloud decisions** | Publisher entity and contacts B-01, India market/ages B-02, per-category retention B-07, guardian role grants B-09/18, identity method OCI-06, test-phone fleet, founder/team B-21, India OCI region/account, DPDP review | Owner + India qualified counsel + OCI account | Signed private decision register, purpose-by-purpose legal clearance, written provider inventory and cost budget; no real child data until passes |
| **M1 — Secure Android/C++ foundation** | Kotlin native parent sign-in and child profile UI, transparent child setup, Keystore key, one-time code, PoP enrollment, device revoke, capability/health, managed DPC lab proof; C++ Drogon API and versioned PostgreSQL + RLS | Synthetic identities, dev/test accounts and hardware | All **T-M1-01..14** with evidence, migration and cross-family isolation CI, strictly scoped M1 API lint; managed physical tests require expendable approved phone |
| **M2 — Compliant location observation** | Fused Location callbacks/FGS permissions, encrypted offline queue, durable C++ GPS intake, latest observed location/status and parent map | M1 auth/revocation; Android real phones; real-data legal gate for pilot | Real OEM lifecycle/instrumented tests or synthetic-only prototype, no false 'live', replay idempotence and RPO/RTO pilot proof |
| **M3 — C++ trips, stops and named places** | PostGIS event-time reconstruction, unknown gaps, provisional stops, versioned late-data corrections, saved place UI/geofence safety | M2 data and legally reviewed historical tracking | Labeled route/stop quality and revision tests, accuracy/battery evidence, no invented roads |
| **M4 — Usage/health/check-in and alert trust** | App Usage Access, reporting timezone/completeness, health center, best-effort check-ins, conditional SOS escalation | Separate India legal approval **for behavioural monitoring**; provider/fallback decisions for SOS | App usage OFF until reviewed; safe child-initiated status and ACK tests; no misleading emergency promise |
| **M5 — Managed Android policy controls** | DPC eligible package restriction and scheduling, rollback, protected-package handling, C++ rule simulation and managed enrollment guide | Device-owner proof from M1, OS/OEM matrix | Managed-device policy negative tests, factory provision/restore, STANDARD mode returns UNSUPPORTED |
| **M6 — Multi-guardian/erasure/security** | Expiring pickup viewer, delegated scopes, per-child access ledger, account and device deletion/retention across workers/cache/backups | B-09/18 and B-07 owner signoff; M1 DB RLS | Cross-family, revoked SSE, deletion/restore/no-resurrection tests |
| **M7 — Commercial integrations** | Google Play ₹50/month / ₹500/year proposed family child-seat plans, entitlements/reconciliation, Maps quotas, optional Drive (deferred until reviewed) | India tax/merchant decision, M6 privacy/security | Play sandbox token/hold/refund tests, public subscription and deletion guidance, no unsupported feature sold |
| **M8 — Operational readiness** | Battery/routing benchmarks, full load/HA/backup restore, support/incident/security/DPDP practice, regional budget | M2–M7 ready; India region provisioned after signoff | Quantified service SLO, RPO/RTO demonstrated, security pen-test, real staff/on-call, updated operating costs |
| **M9 — Play release and staged India launch** | Play child-monitoring disclosures/permission videos, target API, native 16 KB, public terms and privacy, closed track, staged rollout, watch/managed feature flags | M0–M8 release-scope tests and legal/policy signoff | Approved public URLs, Data Safety evidence, actual AAB, verified support/monitoring and staged crash/incident rollback |

**Research/P3 (not in launch)**: permission-compliant visible media capture experiments, corridor deviations, optional Google Roads commercial route matching, standalone Wear OS and other conditional features until independently approved. Research does not block an explicitly scoped safe product, but forbidden feature flags must remain off.

## M1 exact contract / 14 acceptance requirements

Use [M1 Detailed Plan](M1_ANDROID_CPP_ARCHITECTURE_AND_IMPLEMENTATION.md) as technical reference **but not separate milestone numbering**. Current M1 acceptance IDs:
- T-M1-01 real authorized parent pairing and correct child/device link
- T-M1-02 family B guessed child A denied, including no metadata
- T-M1-03 one-use/expired pairing code denied
- T-M1-04 missing key/spoofed challenge refused and requires re-enroll
- T-M1-05 revoke blocks subsequent heartbeat/device request
- T-M1-06 ordinary install reports STANDARD, not managed authority
- T-M1-07 real provisioned device reports actual MANAGED_DEVICE_OWNER
- T-M1-08 safely suspend and restore harmless test package
- T-M1-09 STANDARD/protected-package suspension yields safe unsupported/error
- T-M1-10 closing setup Activity does not create unpermitted stealth/background tracking
- T-M1-11 malformed/oversized/unauthorized requests rejected without crash
- T-M1-12 older/newer Android API capability probes truthful
- T-M1-13 native library packaging on 16 KB device and C++ smoke test
- T-M1-14 logs contain no secrets, pairing code or child location

**M1 API authority:** [OpenAPI M1](openapi-m1.yaml), a *subset* of [whole-project draft](openapi.yaml). Do not prematurely implement/deploy all later endpoints to pass M1. **Executable M1 DB:** backend/persistence/migrations/0001_m1_identity.sql and backend/tests/m1_tenant_isolation.sql. **Scenario steps/evidence:** backend/tests/M1_ACCEPTANCE_TEST_CASES.md.

## M1 sequencing and responsible roles

| Order | M1 action | Responsible candidate role | Evidence / block |
|---|---|---|---|
| 1 | Approve service legal/identity/region setup and synthetic-data boundaries | Founder, lawyer and product security | No real minors' data |
| 2 | Build parent OIDC sign-in and test credential validation | Parent Android + backend | Provider candidate; adult proof separate |
| 3 | Apply SQL v0001 schema, RLS and app role; run two-family negative test | Backend DB + independent security QA | PostgreSQL executable output required |
| 4 | Implement pairing/PoP/revoke/health from linted M1 OpenAPI | C++ backend | Auth, idempotent tests |
| 5 | Add Kotlin child setup, Keystore/proof, bounded capability snapshot | Child Android | No non-setup Activity required; Android OS decides service capability |
| 6 | M1 DPC lab proof, old/new Android and native 16 KB packaging | Android QA | Needs actual approved test phones |
| 7 | Record all T-M1-01..14 evidence, security regression and pilot readiness | QA + product | M1 cannot pass without physical proof |

## Change control and supersession table

| Old document/workstream | Now interpreted as |
|---|---|
| SRS v1.0 'M0–M9' and TSD stage 0–10 | Requirement-to-M0–M9 mapping above, not parallel schedules |
| Old M1 detailed document old M1–M7 follow-on sequence | M1 is foundation; M2 GPS; M3 geo; M4 usage/check-in; M5 policy; M6 governance; M7 billing; M8 hardening; M9 publication |
| Validation and Release Plan's old M0–M7 | Test-domain annex; canonical M0–M9 for staffing/go-no-go |
| Market features D01–D14 | Scoped by existing feasibility gate; not automatic launch milestone |
| OCI Chicago plan | Historical cost/architecture annex; India Mumbai preferred for new deployment, pending actual tenancy/repriced resources |

**No owner facts invented:** publisher, Indian age bands, retention policy, guardian policy, approved login provider, actual test devices and funded staffing remain pending owner decisions. These are **M0 blockers**, not reasons to simulate legal approval. Review [Blockers](BLOCKERS_AND_OWNER_DECISIONS.md).
