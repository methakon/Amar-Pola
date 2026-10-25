# Full Implementation Technical Specification

**Amar-Pola | Revision 1.0 draft | 2026-10-25 | Architecture design (not implemented)**

Related: [SRS](SRS.md), [Feasibility and conditions](FEASIBILITY_CONDITIONS_AND_EVIDENCE.md), [Google Play requirements](GOOGLE_PLAY_PUBLISHING_REQUIREMENTS.md).

## 1. Objectives and boundaries

Build a parent-supervised, transparent Android management system with:
- Child Android app: a narrow Kotlin Android platform layer and an efficient C++20 core.
- Parent Android app: Jetpack Compose, Maps SDK, status, reports, eligible device policies.
- C++ backend: Drogon (recommended) + PostgreSQL, secure pairing, commands, policies, entitlement service and history.
- Optional Google Drive backup of media from approved, visible workflows.

The product will not conceal monitoring, suppress Android's privacy indicators, bypass permission checks, or claim unrestricted access to another app's private files. All conditional features are feature-flagged and must pass device and publication gates.

## 2. High-level architecture

```text
Parent Android client (Kotlin/Compose + Google Maps)
  | HTTPS + access token
  v
API gateway/TLS -> C++ Drogon service -> PostgreSQL
                  |    |      |
                  |    |      + Subscription verification / Google Play
                  |    + Command store + audit events
                  + Google Drive OAuth and upload coordination
  ^
  | HTTPS device credential, FCM signal optional
  |
Child Android agent
  Kotlin: onboarding, location adapter, usage adapter,
          WorkManager sync, lifecycle, optional DPC adapter
  JNI boundary
  C++: event validation, serialization, queue/coordinator, policy evaluation
  SQLCipher/Keystore-backed local encrypted queue
```

## 3. Technology baseline

- Build Android apps with Android Studio, Gradle, Android Gradle Plugin and Android NDK/CMake.
- Set **targetSdk=36 or higher** for a new Play submission as of 2026-10-25. Proposed minimum API is **29** (Android 10), subject to field support review; `minSdk` is not a Play-wide rule here.
- Use C++20 where NDK and chosen toolchain support it. JNI boundary should pass compact versioned data structures; never hold Android `Context` references inside native worker threads without lifecycle management.
- Android child: Kotlin coroutines/WorkManager for deferrable work; Fused Location Provider or Android LocationManager in a correctly configured location service for supported ongoing tracking; UsageStatsManager only with Usage Access.
- Server: Drogon asynchronous handlers, request size/rate limits, PostgreSQL migrations, stable structured JSON logs, OpenTelemetry metrics. Avoid home-grown crypto/TLS.
- Parent app: Kotlin, Compose, Google Maps SDK; maps API key restricted by Android package/signing certificate; UI handles freshness and accuracy.
- Build release **Android App Bundles (AAB)** with Play App Signing; inspect native `.so` compatibility with **16 KB page sizes**.

## 4. Target repository layout

```text
android/child-app/           Gradle application + Kotlin adapters
android/parent-app/          Gradle application + UI
shared/core/include/         Portable C++ public APIs
shared/core/src/             C++ implementation and tests
backend/src/                 C++ Drogon HTTP handlers/services
backend/migrations/          SQL schema migrations
backend/tests/               API/authorization/integration tests
infra/                       compose, deployment, monitoring (without secrets)
docs/                        SRS, feasibility, implementation, Play documents
.github/workflows/           unit tests, lint, build & security scans
```

## 5. Child app modules

| Module | Interface | Responsibility |
|---|---|---|
| OnboardingCoordinator | Kotlin | Pairing, consent/disclosure, permissions and diagnostics |
| PermissionRegistry | Kotlin | Read current permission/special-access state on every sensitive operation |
| LocationCollector | Kotlin | Timestamped fixes; foreground location service where supported |
| UsageCollector | Kotlin | UsageStatsManager, authorized sampling/aggregation |
| PolicyAgent | Kotlin | Managed-device package suspension, policy apply/rollback |
| SyncWorker | Kotlin | Compressed, idempotent batches using WorkManager |
| LocalQueue | C++/SQLite integration | Sequence numbers, bounds, retry metadata, encryption |
| CapabilityReporter | Kotlin + C++ model | Android API, management mode, permission state and feature support |
| MediaCapabilityAdapter | Platform integration | Optional authorized capture workflow only, behind explicit release flag |
| PrivacySurface | Kotlin | Clearly identifiable app, ongoing monitoring notice, revocation/settings UI |

The setup Activity may close after enrollment. Do not equate this with invisible monitoring. Always follow notification and privacy-indicator requirements.

## 6. Device enrollment and authentication design

1. Authenticated parent requests a short-lived pairing code.
2. Parent opens the child app and enters/scans that code during setup.
3. Child app generates a per-device key in Android Keystore where supported.
4. Backend atomically redeems code, binds device to parent, issues short-lived access token bound to device identity.
5. Device refreshes credentials through authenticated channel. Parent can revoke pairing; server rejects subsequent requests.
6. Managed-device mode has a **separate** provisioning workflow, with an explicit factory-reset/QR setup warning where applicable. A permission grant cannot silently enable device-owner status.

Failure handling: code expired, reused, wrong parent, lost network, revoked credentials and unsupported management mode.

## 7. Location and usage event design

```json
{
  "event_id": "uuid",
  "device_id": "uuid",
  "observed_at": "2026-10-25T10:00:00Z",
  "latitude": 26.0,
  "longitude": 88.0,
  "accuracy_m": 35,
  "speed_mps": null,
  "provider": "fused",
  "sequence": 123
}
```

The values above are sample schema values only, not actual device measurements. Require a timestamp and reported accuracy; speed and bearing optional. Reject invalid ranges, future clocks beyond allowed skew and duplicate `event_id` values. Never fabricate missing positions.

Usage events: package identifier where policy permits, collection interval, foreground duration, source and aggregation version. Establish daily UTC storage with explicit local-time reporting and DST/timezone rules. Persist aggregates regularly because the OS does not promise unlimited historical availability.

Local queue: encrypted SQLite, bounded by count/bytes/retention, transactional insert and acknowledgment; upload batches with idempotency keys; exponential retry and jitter. On permission loss, stop data collection for that feature, update capability state and preserve only authorized existing records per retention rules.

## 8. Parent/client API contracts (draft OpenAPI design)

All routes behind TLS; principal and object-level authorization on **every** read/write.

| Method and route | Identity | Function |
|---|---|---|
| POST /v1/pairing-codes | Parent | Issue short-lived token |
| POST /v1/enrollment | Device with code | Pair a device |
| GET /v1/devices | Parent | Paired-device list and last seen |
| POST /v1/devices/{id}/capabilities | Device | Permission/mode snapshot |
| POST /v1/devices/{id}/locations:batch | Device | Idempotent telemetry ingestion |
| GET /v1/devices/{id}/locations | Parent | Paginated time-range history |
| POST /v1/devices/{id}/usage:batch | Device | Aggregates |
| GET /v1/devices/{id}/usage | Parent | Daily/monthly/yearly totals |
| POST /v1/devices/{id}/policies | Parent | Versioned restriction rules |
| GET /v1/devices/{id}/policies | Device | Applicable policy delta |
| POST /v1/devices/{id}/commands | Parent | Supported remote control request |
| GET /v1/devices/{id}/commands | Device | Pending commands |
| POST /v1/devices/{id}/commands/{cid}:result | Device | Execution outcome |
| DELETE /v1/devices/{id}/pairing | Parent | Device revocation |
| GET /v1/audit-events | Parent | Authorized audit |
| POST /v1/account/deletion-request | Parent | Account/data erasure |
| POST /v1/subscriptions/provider-events | Verified provider | Entitlement lifecycle |

Pagination: cursor, limit <= 500, bounded query range. All write bodies validate size/schema and use request IDs. Commands accept `idempotency_key`, `expires_at`, typed parameters. Use a unique `(device_id,event_id)` constraint for ingestion.

## 9. Remote command state machine

```text
CREATED -> QUEUED -> DELIVERED -> ACCEPTED -> COMPLETED
   |         |           |          +-> FAILED
   +---------+-----------+----------+-> EXPIRED
                         +----------+-> PERMISSION_REQUIRED
                         +----------+-> USER_ACTION_REQUIRED
                         +----------+-> OS_REJECTED
                         +----------+-> UNSUPPORTED
```

A device response can also indicate OFFLINE/RETRYABLE. Server enforces legal transitions and expiry. A request is never considered completed on mere push delivery.

Camera/audio functionality: **deferred optional module**. Parent UI exposes only feature categories certified for the enrolled device and approved distribution. An authorized user-visible operation re-checks Android permission/state and reports unsupported/OS rejection honestly. No design for undisclosed recording or bypassing system indicators is included.

## 10. Managed-device application restrictions

Provide a DPC-enabled build variant only for appropriately enrolled devices. Use `DevicePolicyManager.setPackagesSuspended` for eligible installed packages. The API reports unsuspendable packages; store a per-package outcome. Do not promise universal instant force-stop.

Policy example:

```json
{
  "policy_id": "uuid",
  "version": 4,
  "target_packages": ["org.example.game"],
  "timezone": "Asia/Kolkata",
  "days_of_week": [1, 2, 3, 4, 5],
  "start_local": "20:00",
  "end_local": "06:00",
  "desired_state": "SUSPENDED"
}
```

Parse overnight windows, reboot persistence, clock/timezone changes and next transition calculation using on-device time-aware scheduling. Never suspend emergency, provisioning, admin, permission controller or other system-critical packages. Parent can revoke/roll back a policy; offline device applies last authorized policy until its expiry.

## 11. Backend relational model (initial migration)

Tables:
- `parent_accounts(id, auth_subject, created_at, deletion_status)`
- `devices(id, owner_id, mode, api_level, app_version, last_seen_at, revoked_at)`
- `device_keys(id, device_id, key_fingerprint, issued_at, revoked_at)`
- `capabilities(device_id, observed_at, payload_json, capability_version)`
- `location_events(device_id, event_id, observed_at, lat, lon, accuracy_m, speed_mps, received_at)`
- `usage_aggregates(device_id, package, start_at, end_at, foreground_ms)`
- `policies(id, device_id, revision, payload_json, validity, created_by)`
- `commands(id, device_id, actor_id, type, payload_json, created_at, expires_at, state, reason)`
- `audit_events(id, actor, action, target, occurred_at, metadata_json)`
- `subscriptions(account_id, provider_ref, plan, status, valid_until)`
- `drive_grants(parent_id, encrypted_token_reference, scope_set, revoked_at)`
- `media_metadata(id, device_id, captured_at, kind, size, checksum, storage_ref, deletion_at)`

Indexes `(device_id, observed_at DESC)` for locations; partition if scale warrants. Keep audit metadata minimal. Database credentials, OAuth tokens and payment secrets remain out of app binaries and normal logs.

## 12. Privacy and security implementation

Threats: account takeover, device spoofing, abusive re-pairing, insecure IDOR endpoints, media leakage, lost phones, compromised infrastructure, replayed commands, unbounded collection.

Controls:
- Parent passkeys/OIDC + MFA option; server-side parent/device ownership checks.
- Device credentials in Android Keystore; expiration/rotation; strict pairing rate limits.
- HTTPS TLS 1.2+ (prefer 1.3), secure backend secret manager; no embedded server master key.
- Encryption at rest for sensitive data, audited access, bounded retention, export/deletion endpoints.
- Strong server-side validation for all media and attachment metadata; malware/type/size handling.
- Security logs exclude raw coordinates, media and OAuth tokens.
- Do not use AccessibilityService to bypass restrictions or conceal monitoring.
- Publish privacy policy, account deletion path and a recognizable monitoring app identity.

## 13. Cloud and subscriptions

**Drive:** Authorize the parent with Google OAuth and narrow scopes, preferably app-created files only. Backend stores protected token references, never parent password. Make upload resumable with checksums, backoff and explicit revocation; mark failures and separate Drive deletion from internal data deletion.

**Billing:** Parent Android app uses Play Billing if selling access to digital services via Play; backend validates purchase tokens/notifications and maps to entitlements. Track trial, grace period, active, hold, canceled, expired, refund/revoke. Child device never decides subscription access from local UI alone.

## 14. Performance targets (proposed, not guaranteed)

Capture baseline measurements on supported phones with tracking disabled/enabled; sample 24h stationary and 2h moving scenarios. Measure p50/p95 CPU, PSS memory, GPS usage, wakelocks, background data volume and battery delta. Initial engineering objective: avoid continuous polling, bound queue <= configurable byte limit, batch network transfers and provide configurable location update profiles. Do not publish battery percentage claims until observed on hardware.

## 15. CI/CD and release engineering

- Pull request checks: `ktlint`/Android lint, Detekt optional, C++ clang-tidy, unit tests, Gradle release assemble, CMake/CTest.
- Security: dependency/SBOM scan, secrets scan, SAST and dependency license review.
- Backend: reproducible container, migrations, integration tests with ephemeral PostgreSQL, load tests, rollback plan.
- Android: AAB signing with Play App Signing; inspect Android manifest, target API and 16 KB native library alignment/support. Keep release signing/upload keys out of Git.
- Staged Play release after internal and closed testing, with monitoring for crashes/ANRs/permission denial.

## 16. Milestones with acceptance gates

| Milestone | Deliverables | Exit condition |
|---|---|---|
| M0: Policy/platform research | This document pack, target-device list, Play permissions plan | Team approves standard/managed product scope |
| M1: Foundation | Monorepo Gradle/CMake, auth, pairing, encrypted queue, backend skeleton | Integration tests pass and revocation works |
| M2: Location MVP | Location service, events API, Maps UI, route history | Offline recovery and clear freshness/accuracy |
| M3: Usage analytics | Usage onboarding, aggregation, reports | Reports handle permission revocation/time boundaries |
| M4: Managed controls | Explicit provisioning runbook, DPC policies, schedule | Suspension tested on physical managed device; safe rollback |
| M5: Media/Drive | Only authorized Play-compatible media workflow; parent Drive consent | Permission/policy review and device test gates; otherwise defer |
| M6: Subscription | Billing validation, lifecycle, entitlement UI | Refund/grace/revoke integration tests |
| M7: Play release | AAB, listing, declarations, privacy/deletion URL, screenshots, reviewer demo | All required Play Console forms complete and review approved |

## 17. Traceable verification

See [release and test plan](VALIDATION_AND_RELEASE_PLAN.md). Every SRS functional requirement maps to a test, owner, severity, supported API range and recorded results. **There is currently no executable app and no tested hardware result.** Publication documents are drafts, not evidence of Google Play approval.

## 18. References

- https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start
- https://developer.android.com/about/versions/14/changes/fgs-types-required
- https://developer.android.com/reference/android/app/admin/DevicePolicyManager
- https://developer.android.com/work/dpc/dedicated-devices
- https://support.google.com/googleplay/android-developer/answer/11926878
- https://developer.android.com/guide/practices/page-sizes

## 19. Live route tracking and named places expansion (2026-10-25)

[Live Trip Route, Named Places and Battery Specification](LIVE_TRIP_ROUTE_NAMED_PLACES_BATTERY_SPECIFICATION.md) is the detailed feature-level implementation plan for the parent Google Map: labeled places and optional geofence alerts, adaptive child location collection, event-time ingest, C++ trip/stop clustering, route segmentation, conditional Google Roads API, multi-device provenance, endpoint/data-model additions and reproducible battery testing. Treat that document's 8-milestone feature roadmap as a workstream **within** the existing main M1–M7 milestones, not evidence that implementation is complete.

**Important:** Low-power history and accurately road-matched vehicle paths have competing sampling requirements. Do not offer automatic high-confidence road snapping for sparse vehicle observations. Comply with Google Roads API asset-tracking licensing, caching and attribution requirements before enabling in a commercial tracking product.

## 20. Consolidated C++ multi-tenant backend and adaptive tracking architecture

[Adaptive Movement and Multi-Tenant C++ Server Architecture](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md) contains the detailed **how and why** behind the proposed server design: family/guardian/child/device grants, battery-aware Android motion state machine, C++ Drogon service boundaries, durable ingestion and outbox processing, C++ reconstruction pseudocode, PostGIS spatial matching, time-partitioned SQL, event-time late-data revisions, RLS, capacity and database/storage cost model, usage/command workload isolation, testing and delivery roadmap.

This supersedes overly simple assumptions that a single HTTP server should perform GPS ingestion and trip analysis synchronously. Maintain separate bounded CPU and database workloads. All performance/SLO numbers in that document are **design hypotheses until measured**.
