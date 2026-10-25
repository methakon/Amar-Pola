# Verification, Test Evidence, and Release Roadmap

**Amar-Pola | 2026-10-25 | Plan — no tests executed**

## 1. Feature quality gates

A feature moves through:

`DESIGNED -> UNIT_TESTED -> INTEGRATION_TESTED -> DEVICE_VERIFIED -> SECURITY_REVIEWED -> POLICY_REVIEWED -> RELEASE_ENABLED`.

Each status is stored against the exact build, Android version and device model. Do not mark API support as a device pass. Mark unsupported conditional features disabled rather than silently simulating success.

## 2. Supported hardware matrix

First pass: Pixel (AOSP-like) + Samsung or other high-use OEM, Android API 29, 30, 31, 32, 33, 34, 35, 36 where possible. Test **standard** and **properly provisioned device-owner** enrollment separately. Final support list to be narrowed based on real evidence.

Evidence record per test:

```text
Test ID:
Requirement:
App commit SHA / signed build:
Parent/child package versions:
Phone make/model/build / security patch:
Android API, targetSdk, management mode:
Runtime permissions / special access / notification state:
Battery optimization and connectivity state:
Steps, expected result, actual result:
Screenshot / logs (redacted):
Status: NOT_TESTED | PASS | PASS_WITH_CONDITIONS | FAIL
Tester / date:
Bug / resolution:
```

## 3. Traceability and acceptance cases

| Requirement | Tests | Ship requirement |
|---|---|---|
| FR-001 Pairing | Unique one-time code, expiry, replay, code brute-force, revoke, parental account isolation | Zero cross-account device access |
| FR-002 Permissions | Onboard, deny/revoke, special access, app restart, manufacturer permission paths | Degraded status correct; no fake reporting |
| FR-003/004 Location/history | Screen off, move, stationary, offline, airplane mode, restart, low battery, imprecise grant, route gaps | Points timestamped/accurate; no invented live state |
| FR-005 Usage | Usage Access grant/revoke, aggregation, timezone, day/weekly/monthly/yearly boundaries | Reports reproducible from recorded data |
| FR-006 Commands | Offline, stale capability, expired TTL, retries, duplicate, reboot, fake device token | Terminal status truthful and idempotent |
| FR-007 Restriction | Managed enrollment, suspend eligible package, unsuspend, unsuspendable app, timezone reboot, expiry | Eligibility and rollback demonstrable |
| FR-008 Storage | Owned file, granted SAF file, revoked URI grant, unauthorized app-private path | No protected-path access |
| FR-009/010 Capture | Appropriate user-visible authorization and OS-permitted context, denial, session failure, privacy indicator | No unapproved or hidden capture; OS denial surfaced |
| FR-011 Drive | Parent OAuth, selective scope, access revoked, interrupted/resumable upload, duplicate | Uploaded bytes/checksum and deletion rules verified |
| FR-012 Subscription | Trial, renewal, grace, hold, refund, revoke, purchase replay | Backend entitlement authoritative |
| FR-013 Privacy | Account deletion, device disconnect, Drive unlink, backup queue/deletion, export | Retention and access tested |
| FR-014 Alerts | Connectivity, stale position, sensitive lockscreen details | Correct status with minimal disclosure |

## 4. Security verification

- Threat-model data flows between child, parent, backend, processors.
- Test IDOR/BOLA on every path containing a device ID.
- Validate JWT/OIDC audience and expiry, device signature/revocation, OAuth CSRF/PKCE as applicable.
- Device re-pairing hijack, brute-force enrollment, replay/duplicate command, token theft.
- SQL injection, oversized requests, malformed JSON, sensitive telemetry in logs.
- Backup restore, key rotation, secrets scanner, dependency scanning, privacy data deletion and least-privilege access.
- DPC policy rollback and avoidance of suspending critical system packages.

## 5. Performance verification

Benchmarks on real devices:
- 24-hour baseline idle battery and monitored stationary battery.
- Two-hour walking and vehicle movement reporting.
- 24-hour Wi-Fi versus mobile and unavailable-network queue growth.
- P50/P95 CPU, process PSS, network bytes/day, wakeups, crash/ANR.
- Policy scheduler while offline; process restarted and device rebooted.

Numeric thresholds become an engineering decision **after** measurement. Do not market an unsupported percentage of battery savings.

## 6. Play review evidence pack

| Artifact | Owner | Status |
|---|---|---|
| Production AAB(s), target API evidence | Build engineer | NOT STARTED |
| 16 KB native alignment checks | Android engineer | NOT STARTED |
| Child app identifiable icon and monitoring notification proof | Android engineer | NOT STARTED |
| Disclosure + background-location permission short video | Product/Android | NOT STARTED |
| Privacy policy public URL and data safety signoff | Privacy/legal | NOT STARTED |
| Account deletion in-app and web URL demonstration | Backend/product | NOT STARTED |
| Reviewer credentials, pairing/setup directions | Release owner | NOT STARTED |
| Policy declarations, target audience, content rating and ads | Release owner | NOT STARTED |
| Package visibility/FGS/other permission declarations if applicable | Android/release | NOT STARTED |
| Closed testing results + production access if required | QA/release | NOT STARTED |
| Subscription products and test payments | Billing engineer | NOT STARTED |
| Device/OS compatibility and security signoff | QA/security | NOT STARTED |

## 7. Roadmap tasks by milestone

### M0 — Architecture/policy approval
Freeze release features, use cases, desired mode(s), `minSdk`, available test devices, package IDs, publisher identity, hosting location and retention. Review whether the child agent distribution strategy qualifies under Google Play monitoring policy. Deliver approved document set and issue backlog.

### M1 — Secure foundation
Create Gradle multi-app, shared C++ CMake library, CI, Drogon server skeleton, PostgreSQL migrations. Implement parent auth, short-lived one-time pairing, device keys, revocation and secure audit. Exit: reliable authenticated enrollment, negative security tests.

### M2 — Location MVP
Onboard permissions, persistent transparent monitoring notification, location collector with compliant lifecycle, local encrypted queue, server ingest and parent map/history; adaptive movement updates, speed optional. Exit: device movement/stationary/offline tests, stale UI.

### M3 — Usage reports
Usage Access setup and collection, aggregation jobs, per-app duration reports by requested periods, permission revocation and retention enforcement. Exit: tests across time boundaries.

### M4 — Managed control module
Separate DPC build/provisioning runbook and device compatibility list. Implement eligible package suspension/restore and local time-based policy evaluation with audit and rollback. Exit: test evidence for managed device; standard UI does not offer unsupported promises.

### M5 — Commercial foundations
Play Billing entitlement service, backend validation, purchase/refund lifecycle; Google Drive OAuth/backup if required for MVP. Exit: provider sandbox and security tests.

### M6 — Optional media research
Only evaluate clearly disclosed, authorized, permitted capture workflows on real device matrix. Verify all privacy indicators, lifecycle/service limitations, policy eligibility and distribution constraints. If these cannot be met, omit capture permissions and features from release.

### M7 — Publication
Freeze dependency/SDK inventory; complete Data safety from actual app, privacy/deletion live pages, store graphics/screenshots, declarations and reviewer demonstration; app signing/AAB 16 KB checks; testing tracks and rollout readiness; fix Play review findings.

## 8. Rollout and incident response

- Use internal testing, then closed testing, then staged production percentage as appropriate.
- Monitor crash/ANR, device sync failures, unauthorized API errors, location staleness, queue depth and subscription state.
- Establish kill switches for unsafe/misbehaving modules, server rollback and DB migration rollback/backups.
- Security incident path: triage, credential revoke, access audit, required regulatory/user notices, fix, retest and postmortem.

## 9. Release approval table

```text
Release:
Parent AAB:
Child AAB:
Backend build:
SRS traceability completed:
Security signoff:
Privacy/legal signoff:
Google Play policy declarations completed:
Device matrix signoff:
Billing/Drive verification:
Release manager approval:
Actual Play Console review status:
```

Anything left blank is a blocker for claims that the corresponding area is complete.

## 10. Additional M0/M1/M2 Indian-law, emergency and recovery go/no-go (2026-10-26)

| Gate | Required signoff and actual evidence | Stop condition |
|---|---|---|
| **M0-LAW** | India publisher, age scope, DPDP sections 9/16 and Rule 12 interpretation from India lawyer; consent/parent verification procedure; Chicago cross-border review | Synthetic data only until signed |
| **M0-POLICY** | Real owner authorizes B-07/B-09/B-18 retention and child guardian access; backend enforces scoped grants | No child-data onboarding |
| **M1-AUTH** | Google Sign-In/Credential Manager candidate independently verified; identity/person-age review separate | No production identity |
| **M1-DEVICE** | Older and newer Android real phones plus approved resettable DPC spare, manifest/FGS and device-owner actual evidence | Cannot claim M1 hardware ready |
| **M1-TEAM** | Named Android/C++/QA/security/SRE owner, legal counsel and support staffing cash budget | No delivery or release commitment |
| **M2-PRIVACY** | Separate lawful scope for current location, history, usage, geofences, SOS, apps; privacy notices and deletion tests | Location/usage for real minors OFF |
| **M2-SOS** | Tested guardian ACK and optional SMS + independent fallback path; or explicit **best-effort check-in** only | No emergency SOS promise |
| **M2-DR** | Approved, clocked RPO/RTO from failed-VM/restore tests, backup erasure and active on-call | No real child pilot |
| **COMMERCIAL** | 50/500 actual tax-inclusive-or-exclusive Play prices, real settlement, staff/support/HA, refund and churn break-even | No profitability assertion or paid launch |

Evidence docs: [India DPDP](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md), [SOS](SOS_ESCALATION_AND_INDEPENDENT_DELIVERY_DESIGN.md), [DR](OCI_CHICAGO_RECOVERY_AND_PILOT_READINESS.md), [Staffing/unit economics](PRICE_BREAK_EVEN_STAFFING_AND_DELIVERY_CAPACITY.md), [Owner decisions](BLOCKERS_AND_OWNER_DECISIONS.md). Never close a gate with this table alone.

## 11. Canonical M0–M9 and M1 test/CI authority

Use [single master milestones M0–M9](MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md) over the old M0–M7 table above. In particular M1 must pass [M1 OpenAPI](openapi-m1.yaml) structural lint, [migrations](../backend/persistence/migrations/0001_m1_identity.sql), [two-family negative RLS test](../backend/tests/m1_tenant_isolation.sql), and [T-M1-01…14 detailed cases](../backend/tests/M1_ACCEPTANCE_TEST_CASES.md). A [GitHub Actions CI](../.github/workflows/m1-contract-and-tenant.yml) defines a PostgreSQL 16 execution environment. Real phone/DPC, backend handlers, legal under-18 authority and actual OCI India tenancy remain blocked.
