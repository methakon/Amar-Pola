# Madalasa–Alarka — Complete Requirement-to-Design-to-Test Traceability

> **Current product:** **Madalasa** (parent app) + **Alarka** (child app); the GitHub repository is now **[Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka)**. [English mythological inspiration](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Baseline:** SRS v1.0 (FR-001–FR-049, NFR-001–NFR-016)  
**Date:** 2026-10-25 | **State:** design mapping complete; all implementation evidence pending  
**Important:** Rows are explicit trace assignments, not passing test reports. IDs beginning T are planned test cases to be implemented.

## 1. Release traceability contract

- Every production-enabled FR has a code owner, a reviewed detailed design section/API/data model, and **at least one automated test evidence record** with matching build SHA.
- Every conditional FR records exact Android API/OEM/enrollment mode/permission/feature-flag evidence. A NOT_IMPLEMENTED or NOT_VERIFIED row **cannot** be counted as passed.
- Deferred research rows remain traceable for planning but are excluded from launch acceptance.
- CI should reject a release with an enabled FR that has missing/failed test IDs or unmatched OpenAPI/migration contract.
- Results: NOT_IMPLEMENTED, IMPLEMENTED_UNVERIFIED, DEVICE_TESTED, SECURITY_TESTED, POLICY_REVIEWED, RELEASE_APPROVED.

## 2. Functional requirement matrix (49 rows)

| Requirement | Scope | Owning module | Suggested owner | Planned test ID | Required release gate | Current evidence |
|---|---|---|---|---|---|---|

| FR-001 | Secure pairing | Auth / Enrollment | Security + Backend | T-FR-001 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-002 | Permission onboarding and transparency | Android permissions / disclosure | Android + QA | T-FR-002 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-003 | Location observations | Android Location / GPS ingest | Android + QA | T-FR-003 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-004 | Travel route/history | Geo reconstruction / Maps | C++ Geo + Parent UI + QA | T-FR-004 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-005 | App usage reports | UsageStats / Aggregator | Backend + QA | T-FR-005 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-006 | Authenticated commands | Command service | Backend + QA | T-FR-006 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-007 | Managed screen-time restrictions | DPC / Rules | Android + QA | T-FR-007 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-008 | Permitted file access | Storage adapter | Android + QA | T-FR-008 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-009 | Authorized photo/video (deferred) | Deferred capture adapter | Backend + QA | T-FR-009 | RESEARCH; no ship | NOT_IMPLEMENTED |
| FR-010 | Authorized audio (deferred) | Deferred capture adapter | Backend + QA | T-FR-010 | RESEARCH; no ship | NOT_IMPLEMENTED |
| FR-011 | Google Drive backup | Drive OAuth / Upload | Backend + Product | T-FR-011 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-012 | Subscription entitlements | Play Billing / Entitlements | Backend + Product | T-FR-012 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-013 | Privacy retention and account deletion | Privacy jobs / Account | Security + Backend | T-FR-013 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-014 | Status and notifications | Health and notification service | Backend + QA | T-FR-014 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-015 | Parent named places | Parent Map / NamedPlaces | C++ Geo + Parent UI + QA | T-FR-015 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-016 | Observed route reconstruction | Geo route rendering | C++ Geo + Parent UI + QA | T-FR-016 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-017 | Multiple trip legs and stops | C++ StopDetector / TripSegmenter | C++ Geo + Parent UI + QA | T-FR-017 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-018 | Adaptive battery profiles | Android MotionPolicy | Android + QA | T-FR-018 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-019 | Optional road matching | Optional Roads adapter | Backend + QA | T-FR-019 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-020 | Multi-device location provenance | Multi-device provenance | Backend + QA | T-FR-020 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-021 | Named-place notifications | Geofence / Alert engine | C++ Geo + Parent UI + QA | T-FR-021 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-022 | Child-specific guardian ACL | Guardian ACL / DB | Security + Backend | T-FR-022 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-023 | Durable idempotent event ingest | Ingest / DB outbox | Backend + QA | T-FR-023 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-024 | Event-time reconstruction/revisions | Reconstruction worker | Backend + QA | T-FR-024 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-025 | C++ workload isolation | API workload controller | Backend + QA | T-FR-025 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-026 | Parent view without extra GPS | Parent Map / read cache | C++ Geo + Parent UI + QA | T-FR-026 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-027 | Scoped retention/revocation | Retention/ACL | Security + Backend | T-FR-027 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-028 | Quality-aware map presentation | Geo quality / Parent UI | C++ Geo + Parent UI + QA | T-FR-028 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-029 | Scalable capacity/security verification | SRE / load/security tests | Backend + QA | T-FR-029 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-030 | Route Evidence confidence | Geo explainability | C++ Geo + Parent UI + QA | T-FR-030 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-031 | Tracking Reliability Center | Health classifier | Backend + QA | T-FR-031 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-032 | Offline correction history | Trip revision store | C++ Geo + Parent UI + QA | T-FR-032 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-033 | School commute confidence | Commute classifier | C++ Geo + Parent UI + QA | T-FR-033 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-034 | Temporary guardian/pickup access | Temporary grant + SSE | Security + Backend | T-FR-034 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-035 | Who-accessed-data ledger | Audit/event store | Security + Backend | T-FR-035 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-036 | Energy versus coverage | Power analysis / Android | Android + QA | T-FR-036 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-037 | Policy preview and rollback | C++ policy evaluator + DPC | Android + QA | T-FR-037 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-038 | Source handoff explanation | Source handoff / Android | Android + QA | T-FR-038 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-039 | Capability-before-purchase | Billing capability UI | Backend + Product | T-FR-039 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-040 | Privacy-safe support diagnostics | Support redaction service | Backend + Product | T-FR-040 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-041 | Child transparency center | Child UI and disclosures | Android + QA | T-FR-041 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-042 | Route-corridor alerts (research) | Corridor prototype (research) | Backend + QA | T-FR-042 | RESEARCH; no ship | NOT_IMPLEMENTED |
| FR-043 | Schedule-aware tracking pulse | Android schedule policy | Android + QA | T-FR-043 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-044 | Child SOS events | SOS / Notifications | Backend + QA | T-FR-044 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-045 | Find-device signal | Ring command | Backend + QA | T-FR-045 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-046 | Family check-ins | Check-in service | Backend + QA | T-FR-046 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-047 | Screen-time safe rules/tasks | DPC scheduling / task credits | Android + QA | T-FR-047 | Conditional device/policy test | NOT_IMPLEMENTED |
| FR-048 | Child device health heartbeat | Device health snapshots | Backend + QA | T-FR-048 | Core integration/security tests | NOT_IMPLEMENTED |
| FR-049 | Alert deduplication/quiet hours | Notification dedup and quiet hours | Backend + QA | T-FR-049 | Core integration/security tests | NOT_IMPLEMENTED |

## 3. Non-functional requirement matrix (16 rows)

| NFR | Verification objective | Test ID | Status |
|---|---|---|---|

| NFR-001 | Battery measurement / location power | T-NFR-001 | NOT_VERIFIED |
| NFR-002 | Bounded memory/CPU workers | T-NFR-002 | NOT_VERIFIED |
| NFR-003 | Durable replay and recovery | T-NFR-003 | NOT_VERIFIED |
| NFR-004 | Authentication and encryption | T-NFR-004 | NOT_VERIFIED |
| NFR-005 | Privacy and child data minimization | T-NFR-005 | NOT_VERIFIED |
| NFR-006 | API/OEM device compatibility | T-NFR-006 | NOT_VERIFIED |
| NFR-007 | Accessibility and uncertainty UX | T-NFR-007 | NOT_VERIFIED |
| NFR-008 | Versioned maintainability & contract tests | T-NFR-008 | NOT_VERIFIED |
| NFR-009 | Scalability and load testing | T-NFR-009 | NOT_VERIFIED |
| NFR-010 | Cross-tenant zero-access checks | T-NFR-010 | NOT_VERIFIED |
| NFR-011 | Route/stop/commute accuracy metrics | T-NFR-011 | NOT_VERIFIED |
| NFR-012 | On-call/restore/incident preparedness | T-NFR-012 | NOT_VERIFIED |
| NFR-013 | Honest error and freshness states | T-NFR-013 | NOT_VERIFIED |
| NFR-014 | Billing/OAuth provider reliability | T-NFR-014 | NOT_VERIFIED |
| NFR-015 | 16 KB native build/Play AAB support | T-NFR-015 | NOT_VERIFIED |
| NFR-016 | Erasure across all stores/backups | T-NFR-016 | NOT_VERIFIED |

## 4. Planned test suite definition

### T-FR common contract
Each test case must define: requirement ID, signed build and Git commit, Android API/OEM (when applicable), parent/child/family setup, permission state, initial DB state, action, expected API/UI/DB state, negative cases, screenshots/redacted logs, tester/date and outcome. For tests not requiring Android, provide isolated CTest/HTTP/PostgreSQL integration test command and seeded family fixture.

- Authentication tests (T-FR-001, 006, 022, 034–035): cross-family queries, revoked guardian, expired invitation, replayed enrollment token, unauthorized stream after revoke.
- Android runtime tests (T-FR-002–005, 018, 020–021, 036, 038, 041, 043): screen off, start restrictions, denied permission, device restart, stationary/vehicle/urban tunnel, optional watch and low battery.
- C++ geo correctness (T-FR-004, 015–017, 019, 024, 028, 030, 032–033, 042): labeled stop inference, red light, uncertainty, late replay, wrong road and time boundaries.
- Data durability (T-FR-013, 023, 025, 027, 029): commit/ack crash, cross-partition dedup, stale worker epoch, backup restore after deletion, capacity.
- Commercial/provider (T-FR-011–012, 039): OAuth grant/revoke, Play trial/hold/refund, subscription capability downgrade.
- Managed policies (T-FR-007, 037, 047): enrolled device owner, eligible vs protected package, DST schedule, next-transition preview, rollback.
- Child interaction/alerts (T-FR-014, 044–046, 048–049): authorized SOS and notification delivery, offline/pending receipts, check-in, bounded ring signal, dedup and quiet hours.
- Deferred media (T-FR-009/010): deliberately disabled, no manifest permissions shipped unless separately approved visible workflow has specific evidence.

### T-NFR contract
Battery test compares measured app-disabled/device baseline vs tracking modes; performance tests 1k/10k/100k synthetic devices; security tests use two tenant fixtures and revoked SSE, RLS bypass prevention, secrets in logs; native tests check 16KB ELF/zip, runtime on 16KB emulator/device; deletion tests verify no post-restore data resurrection.

## 5. Evidence ledger format

~~~yaml
test_id: T-FR-023
requirements: [FR-023, NFR-003]
scenario: device batch persisted then HTTP connection dropped before response
status: NOT_IMPLEMENTED
build_sha: null
environment: null
expected: exactly one logical accepted event on retry
actual: null
log_reference: null
owner: backend_qa
reviewer: null
review_date: null
~~~

Store actual evidence in protected CI/test storage and reference hashes/IDs here. Never store live child location or device secrets in an open repository.

## 6. Existing engineering design references

- [Canonical TSD](TECHNICAL_SPECIFICATION.md) (new architecture crosswalk).
- [Data and authorization](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md): schema, guardian ACL, RLS, transactional ingest, worker fencing and deletion.
- [Algorithm/runtime](TRACKING_RUNTIME_AND_ALGORITHM_CONTRACT.md): exact status vocabulary and candidate thresholds, Android lifecycle tests.
- [C++ server](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md): module topology, throughput/capacity and worker separation.
- [Feasibility](WHOLE_PROJECT_FEASIBILITY_GATE_2026.md): conditional/blocked features.
- [Blockers](BLOCKERS_AND_OWNER_DECISIONS.md): owner decisions and engineering/external gates.

**Current closure:** 49 FR + 16 NFR have planned coverage IDs. **Zero tests or release artifacts are evidenced by this document.**
