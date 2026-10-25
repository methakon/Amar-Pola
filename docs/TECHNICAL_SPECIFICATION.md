# Amar-Pola — Canonical Whole-Project Technical Specification

**Document ID:** AP-TSD-001  
**Revision:** 1.0; consolidates the former v0.1 technical specification into one authoritative implementation overview.  
**Date:** 2026-10-25  
**Status:** Architecture/design sufficiently specified for prototype engineering; NOT production-verified.  
**Requirement source:** [SRS v1.0](SRS.md) (FR-001–FR-049 and NFR-001–NFR-016).  
**Feasibility source:** [Whole Project Feasibility Gate](WHOLE_PROJECT_FEASIBILITY_GATE_2026.md).  
**Blockers:** [Decisions and Resolution Register](BLOCKERS_AND_OWNER_DECISIONS.md).  
**Traceability:** [Full FR/NFR Test Matrix](REQUIREMENTS_TRACEABILITY.md).  
**Machine-readable API:** [OpenAPI 3.1 draft](openapi.yaml).  
**Deep implementation contracts:** [Data/Authorization/Recovery](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md), [Android/Geo Algorithms](TRACKING_RUNTIME_AND_ALGORITHM_CONTRACT.md), [C++ scaling](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md).

## 1. Decision authority and nonnegotiable invariants

This document is the project's current **canonical TSD**. Specialized annexes specify subdomains in greater detail. When two old documents conflict, the precedence is: latest approved **SRS** for what; **feasibility gate** for whether/where; this **TSD** for overall system design; named annex for algorithms/data/API; signed ADR for an explicit exception. No paragraph means a feature is implemented or a supported Android mode is proven.

- Privacy: transparent authorized parental monitoring, recognizable child app identity, user-visible disclosures, required monitoring notification and OS privacy indicators. Never introduce covert capture or Android permission bypass.
- Trust: parent/grant ownership evaluated for each action; device credential only operates on its own enrolled device; no request-body role/tenant trust.
- Truthful data: a stale GPS fix isn't live; a possible stop isn't a visit; an interpolated path isn't the actually observed street; command delivery isn't execution.
- Durability: 202 event batch success only **after durable transaction**; at-least-once transport with idempotent effect; rollback/replay doesn't double route length or stops.
- Concurrency: C++ HTTP request loop never runs heavy reconstruction or large blocking SQL. Bounded parallel work with backpressure and per-tenant fairness.
- Low energy: phone runs minimal Android location + data queue, not map rendering, geocoding or complex trip analysis. Parent viewer count does not increase child GPS sampling.
- Conditional mode: managed DPC device restrictions require real device-owner or other authorized managed provisioning, not merely grants from parent in Settings.
- Deferred: remote media capture, corridor alerts and broad web interception are not part of general Play release until separate evidence and signoffs.

## 2. Deployable architecture and communication

~~~text
Child Android app
 Kotlin: Onboarding / PermissionRegistry / LocationEngine
         UsageStats Adapter / TrackingPolicy / FGS / Notification
         WorkManager uploader / optional ManagedDPC / Child Actions
 C++20 NDK: bounded queue model, validation, compact event serializer
 Protected SQLite queue + Android Keystore
          | device-authenticated HTTPS, batched events and receipt
          v
Edge TLS / rate limits / request-size limits
          |
          +--> C++20 Drogon stateless API replicas
          |      Authentication / family-child grants / pairing
          |      Device ingest, places, location and history query
          |      SOS/commands / user management / entitlements
          |
          +--> PostgreSQL + PostGIS
                 Raw observations partitioned by observed time
                 Event dedup ledger, outbox/reconstruction jobs
                 Guardian grants, child/device map, named places
                 Trips/stops/revisions, usage and audit/deletion
                       |
             +---------+----------+----------------+
             |                    |                |
      C++ reconstruction      Usage/policy      Retention/billing/
      workers by device       alert workers     notification workers
             |                    |                |
             +--------------------+----------------+
                          |
                 Latest-position read table
                 + SSE fanout (parent only)
                          |
                 Parent Kotlin/Jetpack Compose
                 Google Maps + child history + status
~~~

Start with a **modular monolith**: one or two API replicas, one bounded C++ reconstruction process and one maintenance worker against managed PostgreSQL/PostGIS. Split workloads to distinct services or a durable broker only after a measured operational bottleneck, not reflexively.

Optional integrations: FCM as best-effort notification hint, Google Maps and optionally Places on the parent side, Google Drive OAuth when selected, Google Play Billing for applicable digital products. Push delivery must not be the source of truth for completion.

## 3. Project code structure and build strategy

~~~text
android/
  child-app/        Gradle Kotlin services, permissions, onboarding
  parent-app/       Gradle Kotlin Compose, Maps, usage, guardians, billing
  wear-app/         optional separate Wear OS module and source identity
shared/
  core/include/     C++20 stable domain types, portable validation
  core/src/         serialization and testable pure algorithms
backend/
  api/              Drogon controllers, auth filters and role checks
  domain/           plain C++ event and rule types
  ingest/           validated durable event writer and outbox
  geo/              quality filter, movement, stops, route, confidence
  workers/          reconstruction, usage, SOS, retention, deletion
  migrations/       versioned PostgreSQL/PostGIS SQL and rollback plan
  tests/            CTest, API, seeded DB, security, load fixtures
infra/              staging/prod configs, dashboards and backup runbooks
docs/               source specifications, ADRs, API and test evidence
.github/workflows/  lint, unit tests, integration tests, artifact scans
~~~

Recommended: Kotlin controls all Android runtime permissions and location lifecycle; only thin JNI interfaces connect C++ portable helpers. Native Kotlin interoperability is not a reason to run location directly from unmanaged NDK threads. Drogon asynchronous HTTP/SQL plus C++ testable geospatial workers; PostgreSQL for ACID and PostGIS indexed proximity. Avoid home-grown auth/TLS/crypto.

**Build/release:** pin compiler, NDK and dependencies; Android new standard app target SDK >=36 under 2026 Play rule (Wear OS has separate >=35); selected minSdk **candidate** 29. Bundle Android AAB, sign via Play App Signing, scan dependencies, test all native shared libraries for 16 KB ELF/zip alignment and runtime, protect CI secrets and signing keys. Parent, child and Wear application manifests/privacy declarations need separate review.

## 4. Feature implementation crosswalk — entire project

| Requirement group | Core method and owned module | Data and API | Test/reference |
|---|---|---|---|
| FR-001/002: pairing & permission onboarding | Parent identity; one-use code, device Keystore key; Kotlin disclosure wizard & capability snapshots | family/device/credential tables; pairing and capabilities endpoints | T-FR-001/002; authorization/data annex |
| FR-003/018: adaptive tracking | FusedLocationProvider LocationRequest modes, distance filter, Activity Recognition hint, lawful typed FGS, queue | device observations, policy version | T-FR-003/018, device runtime annex |
| FR-004/015–017/028: route, stops, saved places | Event-time C++ qualify → motion → dwell cluster → legs/gaps; PostGIS ST_DWithin; Maps polyline/markers | location_observations, trips, stops, places, segments | T-FR-004/015/016/017/028 |
| FR-005 and usage parts of FR-047 | Usage Access from Settings, interval aggregates and bounded sync | usage_aggregates, usage API | T-FR-005/047 |
| FR-006/007: commands and managed restrictions | Typed signed/authorized commands; on-device DPC package suspension only if eligible; local safe scheduler | commands/policies and execution receipts | T-FR-006/007 |
| FR-008/011: authorized files and Drive | Storage Access Framework/MediaStore only; OAuth least scopes & resumable transfer | media metadata and Drive grants | T-FR-008/011 |
| FR-009/010: optional media | **DISABLED** absent separately reviewed authorized visible capture workflow and OS/Play gate | no launch API/permission | T-FR-009/010 disabled |
| FR-012/039: billing and compatibility | Play Billing token verification at backend, product capability matrix before pay | entitlements, provider receipts, capability status | T-FR-012/039 |
| FR-013/027: privacy/erasure | Grant/device revocation, cache + live-stream invalidation, deletion tombstones and jobs | deletion API, family/device/raw/derived rows | T-FR-013/027 |
| FR-014/048–049: health and alerts | Piggyback battery/permission heartbeats; FCM only for hint, deduped notices and separate SOS priority | health snapshots, notification delivery | T-FR-014/048/049 |
| FR-019/020/021: road matching/Wear/geofence | Optional Roads adapter after legal review; device provenance; selected geofences (up to 100 active/device user) | source and geofence records | T-FR-019/020/021 |
| FR-022/034–035: family grants, temporary pickup & ledger | Child-specific scope/expiry, audited grants, RLS defense in depth, SSE invalidation | guardian_grants / access receipts | T-FR-022/034/035 |
| FR-023/024/032: durability and revisions | Atomic event dedup + raw + outbox; per-device worker fence and event-time replay | dedup/jobs/checkpoints/trip_revisions | T-FR-023/024/032 |
| FR-025/026/029: scaling and read separation | Bounded Drogon APIs + separate CPU workers, latest qualified position table, parent SSE with quota | health/latest/trips | T-FR-025/026/029 |
| FR-030/031: evidence and reliability | GPS quality classes and source timestamps, reason codes and parent diagnostic page | observation_quality, tracking_health | T-FR-030/031 |
| FR-033/042: commute and corridor | Confirmed dwell + schedule; distinguish UNKNOWN/ARRIVAL_NOT_CONFIRMED; corridor **research only** | commute plans and alert rules | T-FR-033 pilot, 042 deferred |
| FR-036/038/043: battery feedback, handoff, schedule | Real measured tracking coverage/energy; phone/watch source provenance and safe preference; schedule event hints | power profiles/source events | T-FR-036/038/043 conditional |
| FR-037: screen-time rule preview | Pure C++ schedule engine and DST, eligible package list and safe rollback | policy preview and result API | T-FR-037 managed conditional |
| FR-040/041: support diagnostics/child transparency | Sanitized opt-in diagnostic bundle and child-visible monitoring summary | support API + privacy disclosures | T-FR-040/041 |
| FR-044/045/046: SOS, ring, check-in | Child-visible action, urgent durable dispatch, device bounded ring command, check-in acknowledgement | SOS, command and check-in APIs | T-FR-044/045/046 |

FR-001–FR-049 and all NFR-001–NFR-016 are individually enumerated and assigned to test IDs in [Traceability](REQUIREMENTS_TRACEABILITY.md); do not rely solely on grouped table for release coverage.

## 5. Data model and family isolation

Canonical ownership: **family → child profiles → enrolled devices**, with independent authenticated guardian memberships and **explicit guardian-to-child action grants**. Device enrollment to a child can be transferred only through a deliberate revoke/verify/re-enroll process; don't silently reassign a credential. A child may have phone and watch, but each record preserves source device identity.

Minimum core persisted domain: family/parent_principal/guardian_membership/child/guardian_child_grant/device/device_key_record, location_event_dedup, time-partitioned location_observations, latest_position, named_places, trips/legs/segments/stops/revisions, device reconstruction jobs and epochs, usage aggregates, policies/commands, SOS/notifications, billing, audit, media grants and deletion tombstones.

**PostgreSQL correctness:** Raw time partitions require partition key in unique constraint; maintain separate ledger for global per-device event ID idempotence. Authenticated request context is set transaction-locally for RLS using low-privilege non-owner runtime roles. Always check exact child scope in controllers and SSE/cache, not merely family membership.

**Executable schema path:** engineer generates migrations from [Data Contract](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md), tests apply/rollback on isolated PostgreSQL and signs review. The annex's SQL fragments are **illustrative**, not a production migration set.

## 6. Full data journey and state lifecycles

### Enrollment
Parent logs in → requests one-use pairing code → physical child setup enters code → device creates Keystore key → backend verifies code and binds identity to one child → reports permissions/capability. Reuse/expiry/unauthorized transfer rejected.

### Position capture and synchronization
Kotlin LocationEngine receives a valid OS fix → local encrypted queue transaction persists stable event ID and time → WorkManager batch upload when allowed → C++ API authenticates and commits per-device dedup ledger + raw event + outbox in one transaction → HTTP durable receipt → child deletes acknowledged queue records → separate C++ worker calculates provisional/updated trips and emits parent read update.

### C++ geo processing
Per device/affected interval: sort/dedup by observation time; quality/clock/accuracy check; motion inference with hysteresis; dwell clustering and stop qualification; derive trips/legs/segmented gaps; match saved places via PostGIS; version/revision upsert guarded by worker lease epoch; parent sees computed route **only with confidence and provenance**. Late offline batches trigger bounded revision/backfill.

### Parent view
Parent bearer token → check active family/child grant for specific action → fetch latest qualified position or paginated history, no device wake merely for viewing → parent Google Maps renders position/accuracy halo, labeled markers, observed polyline segments, stop timeline and unknown gaps. An SSE stream is optional while parent opens the screen, with active authorization/revocation, bounded subscriber quota.

### Managed app rule
Parent rule form → pure C++ schedule simulator checks timezone, DST and essential-package exclusions → backend stores versioned authorized policy → child verifies actual managed authority and package eligibility → Android DevicePolicyManager applies only permitted restrictions → child returns per-package results. Standard mode reports unsupported enforcement, not success.

### SOS / check-in
Child initiates a clear, visible action → device queues urgent event → backend durable intake, authenticates source → priority notification to authorized guardians with delivery/ack states. Offline “queued” is not delivered. Find-phone sound obeys Android audio/DND permissions and explicit expiry.

### Account deletion
Verified owner initiates app/web deletion request → server revokes credentials/grants/streams first, writes tombstone → bounded idempotent jobs remove raw and derived records, caches, processor tokens, optional app-owned media and legally allowed audit → backup restore respects erasure ledger. Do not mark COMPLETED before actual deletion phase passes.

## 7. API and error contract

The canonical planned endpoint catalog is the **OpenAPI 3.1 draft**, currently expanded with 39 operations for pairing, location, trip revisions, places, usage, SOS, grants, diagnostics, commands, policy preview, billing, and deletion. Every route has per-principal security declaration plus required object/action scope and a shared error shape.

### Universal transport rules

- HTTPS only, short-lived parent token/device proof, bounded body (default candidates: <=500 events/batch and compressed/uncompressed request limits), structured correlation ID.
- Parent routes must check exact child/family action scope in authoritative DB. Device routes bind path deviceId to authenticated enrolled key; body device IDs never grant rights.
- Inputs finite and bounded, observed_at UTC, supported API schema version, conservative request timeouts.
- Idempotency-Key for parent command writes; stable event_id for device observations and SOS; well-defined 409 conflict and 429 Retry-After for quotas.
- Use pagination/cursors and bounded date windows; parent read results contain observation timestamp, source, quality, completeness/revision.
- State changes are event-sourced/audited; **queued** and **delivered** not equivalent to **completed**.
- API/OpenAPI currently design-level: **lint, tests, generated types and actual handlers are future implementation gates**.

Command terminal states: COMPLETED, FAILED, EXPIRED, OS_REJECTED, UNSUPPORTED, PERMISSION_REQUIRED, USER_ACTION_REQUIRED, CANCELLED. DEVICE_OFFLINE can be a nonterminal reported state while expiry clock runs. Server forbids transitions back from terminal states, except a separate explicit corrective audit event; versioned policy commands enforce idempotence.

## 8. Security architecture

Threats: parent account takeover, cross-family BOLA/IDOR, unauthorized guardian invites, device spoofing, stale SSE stream after revoke, exposed precise GPS in logs, compromised backup keys, malicious payload, expensive historical query, coerced monitoring and misuse of managed power.

Mandatory controls:
- OIDC/PKCE or passkeys for parents, optional MFA/step-up on critical operations; unique device Keystore-bound credentials with expiry/revocation.
- Strict child action grants and PostgreSQL tenant RLS as defense-in-depth with non-owner DB role; guard SSE and cache with same scope.
- Managed secret store; strong TLS; protected backup encryption and access logs; no hardcoded shared private keys in mobile binaries.
- Cross-family negative tests across every endpoint and derived data object, including errors, exports, logs and cache.
- Data minimization: no raw location in standard request logs, crash payloads or push notifications; publish retention/deletion policy and implement verified erasure.
- Support diagnostic bundle requires explicit parent opt-in, redaction and short retention; “who viewed data” ledger itself must not expose coordinates.
- Feature flags restrict managed controls, capture, corridor and road matching; never allow old client to force-enable unsupported feature via unsigned JSON.

Security exception and privacy owner decisions are recorded in [Blockers](BLOCKERS_AND_OWNER_DECISIONS.md). No production privacy promise until operator and processors are selected.

## 9. Location accuracy, battery and resource optimization

Android child uses motion-aware candidate profiles: STILL ~5–15 min/passive, WALKING 30–90s, VEHICLE_BALANCED 30–60s, time-limited VEHICLE_DETAIL adaptive 5–15s, and watch lower-rate defaults. Numbers are **tuning hypotheses**, not guaranteed or measured intervals. Apply distance threshold, permitted maxUpdateDelay batching, cool-down/hysteresis, GPS permission revalidation and energy downgrade.

Server efficiency:
- C++ domain algorithms with bounded per-device processing windows; no heavy work in Drogon I/O loop.
- Durable work outbox and per-device lease fencing, coalesce intervals when offline backlog arrives.
- Postgres partitions by observation timestamp, indexed device/time filters, per-parent read limits, latest qualified position materialization.
- Parent position SSE at viewing session only; a map open doesn't trigger child GNSS.
- Upload compression only when genuinely reducing bytes without decompression DoS; bounded offline queue and retries.
- Geofence subset limited to 100 active per app/device user, event responsiveness can be delayed; server handles saved pins without child geofence count expansion.
- Roads API reserved for sufficiently dense reliable vehicle fixes, subject to provider legal cost/licensing and data retention.

Initial performance sizing scenario: 300 observations/device/day; at 100,000 devices ~30 million/day, or ~347 observations/s average. Bursts, WAL, index size and parent reads can dominate. These are **calculated assumptions** not measured server capacity. See [C++ scaling annex](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md).

## 10. Development phases and dependency logistics

| Stage | Implement and review | Gating proof | Dependencies |
|---|---|---|---|
| 0 — Decisions | Family owner/child data policy, target countries/age, retention, hosting, modes/devices, privacy threat model | Owner decisions logged | Blockers B-01 onward |
| 1 — Contracts | Full OpenAPI DTOs, SQL migration set, guardian ACL and grants, C++ core CMake and Gradle skeleton | CI contract lint, tenant cross-access tests | Stage 0 scoped defaults |
| 2 — Secure foundation | Parent auth, one-use pairing, device Keystore IDs, consent UI, revocation, audit | Replay/spoof and parent isolation tests | Stage 1 |
| 3 — Location pipeline | Android compliant FGS and tracking, encrypted queue, durable batch API/dedup/outbox | Real device lifecycle and crash/retry tests | Stage 2 |
| 4 — Route engine | C++ event-time quality/motion/stop/trips and PostGIS named places, map playback | Labeled truth/failure/late replay tests | Stage 3 |
| 5 — Trust UI | Route evidence, Reliability Center, offline revision history, battery/coverage baseline | UI explanation, real device sample and quality tests | Stage 4 |
| 6 — Family & activity | Usage Access/aggregation, guardian pickup grants, audit access ledger, SOS/check-in, notifications | Scoped access, replay and DST/alert tests | Stages 2–5 |
| 7 — Commercial features | Backend Play Billing, child capability-before-purchase, account deletion, optional Drive | Sandbox billing, account deletion/backup rehearsal | Stage 6 |
| 8 — Conditional expansion | Managed DPC restrictions, policy simulator, commute alerts, Wear source handoff and schedule tuning | Actual eligible device tests/false-alarm rate | Product selections |
| 9 — Release hardening | Battery/load/pen tests, monitoring disclosure, 16 KB native build, AAB, Store Data safety, live URLs and Play review | All release-scope FR tests passed + Play approved | Prior stages |
| 10 — Research | Corridor deviation, optional Roads and visible authorized media workflows only if separately approved | Independent feasibility/policy/license gates | Outside baseline launch |

**Deployment:** private dev/staging first with synthetic fixtures, nightly tests, monitored CI. Release to internal testers only after core security and privacy basics; proceed to applicable closed testing and staged production when legal/Play requirements met.

## 11. Validation evidence and definition of done

All 49 FR and 16 NFR are enumerated by ID in [Traceability](REQUIREMENTS_TRACEABILITY.md). Every release-enabled FR needs build SHA, tested hardware or software environment, inputs, expected and actual behavior, security coverage, reviewer and date. Never mark a documentation link as test evidence.

**High severity security:** zero cross-family reads/exports/streams, successful revoke and deletion.  
**Location:** no false live timestamp, no uncertain gaps rendered as actual streets, labeled stop precision/recall and battery drain measured on supported phones.  
**Server:** per-device dedup across retries/partitions, proper lease fencing, bounded memory and accepted-event durability under simulated crashes, documented recovery time.  
**Commercial:** subscription entitlements server-authoritative; parent sees unsupported features before pay.  
**Play:** signed AAB, release manifests/disclosure, background-location permission video, persistent monitoring notification, proper metadata flag, Data safety, account deletion app+web, 16 KB native binaries and policy review.

Actual SLOs (for example p95 ingestion/parent read latency), permissible battery budget, location freshness, reliability and costs become signed test thresholds after owner/product choices and baseline benchmarks. No guaranteed “live every 5 seconds” or “100k devices supported” claim from planning alone.

## 12. Project-wide open decisions and current evidence status

See [Blockers and Owner Decisions](BLOCKERS_AND_OWNER_DECISIONS.md) for 22 owner questions B-01–22, engineering blockers E-01–14, and external blockers X-01–08. **Most urgent:** publisher/territories/ages, transparent monitoring agreement, standard vs managed release, retention, hosting region, test devices/Wear, tracking detail tradeoff, subscription scope and media deferral.

**What is closed at documentation level by this revision:** canonical architecture version conflict, grouped FR mapping, normalized role/tenant design decisions, the event-time transaction algorithm, provisional location quality rules, Android runtime decision table, API endpoint catalog and traceability assignments.

**What remains open in reality:** runnable SQL migrations, actual generated SDK/API handlers, cloud deployment, child/parent code, device and security tests, battery and route quality data, legal/Play approvals, billing and public privacy/deletion pages. Never mark these “done” based on prose.

## 13. Annexes, official sources and change control

- [Data Auth, SQL and Recovery](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md).
- [Android Runtime and Movement Algorithm](TRACKING_RUNTIME_AND_ALGORITHM_CONTRACT.md).
- [C++ Server Capacity and Security](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md).
- [Route, Stops, Maps and Wear](LIVE_TRIP_ROUTE_NAMED_PLACES_BATTERY_SPECIFICATION.md).
- [OpenAPI v1 Draft](openapi.yaml).
- [Requirements Traceability](REQUIREMENTS_TRACEABILITY.md).
- [Blockers](BLOCKERS_AND_OWNER_DECISIONS.md).
- [Google Play Publication](GOOGLE_PLAY_PUBLISHING_REQUIREMENTS.md).
- [Audit Findings](TECHNICAL_DOCUMENT_AUDIT_GAPS_2026.md).

Authoritative references:
- Android background typed FGS/while-in-use: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start
- Android location battery: https://developer.android.com/develop/sensors-and-location/location/battery
- DevicePolicyManager: https://developer.android.com/reference/android/app/admin/DevicePolicyManager
- PostgreSQL RLS: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- Partitioned primary key: https://www.postgresql.org/docs/current/ddl-partitioning.html
- Google Play parental-monitoring policy: https://support.google.com/googleplay/android-developer/answer/9888380
- Play target SDK: https://support.google.com/googleplay/android-developer/answer/11926878
- Account deletion: https://support.google.com/googleplay/android-developer/answer/13327111
- Native 16KB: https://developer.android.com/guide/practices/page-sizes

**Change history:** v1.0 on 2026-10-25 replaces outdated canonical technical document while preserving prior Git history. Every future change requires an explicit design decision record for changed permissions, child data, roles, API schemas or platform capabilities.

## 14. M1 detailed implementation decision — mixed Android and managed provisioning

The project owner confirmed **managed-device provisioning available**, **mixed older/newer Android versions**, and **native Android parent app**. The baseline architecture keeps Kotlin Android adapters and a bounded C++ NDK core for child agent, with C++20 Drogon API and PostgreSQL; the DPC adapter is explicitly separate from normal personal phone mode. The authoritative milestone implementation contract is [M1 Android/C++ Architecture and Implementation](M1_ANDROID_CPP_ARCHITECTURE_AND_IMPLEMENTATION.md): code layout, pairing challenge/proof, guardian security, Android API29–36 candidate matrix, on-device role checks, safe package suspension/restore and 14 M1 tests.

M1 requires real debug binaries and secure pairing proof, not continuous location/history or year-long usage reports. [OpenAPI](openapi.yaml) now includes explicit enrollment proof and device-pairing revoke endpoints, while generated clients/formal validation and real backend handlers remain unimplemented. [Owner decisions](BLOCKERS_AND_OWNER_DECISIONS.md) track remaining supported-device, hosting, age, retention and release concerns.

## 15. Chosen Oracle Cloud deployment baseline and cost governance (2026-10-25)

**Region planning decision:** Oracle Cloud US Midwest Chicago (us-chicago-1). Implement the initial modular C++20 Drogon API, C++ workers and PostgreSQL/PostGIS as separate processes **on one Ampere A1 ARM64 VM**, not on separately billed worker servers. Initial shape candidate 2 OCPU / 12 GB Always Free, 50 GB boot and 100 GB DB block volume with remaining quota reserved; production legality/security and backup reviews remain gates.

See [OCI Chicago Deployment and Financial Plan](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md) for official free-hour and paid-account rate comparison, storage/transfer quota, ingress/backup/restore checklist, hardware and ARM64 compilation requirements, estimated throughput assumptions, one-subscription-per-child unit economics and optional PAYG/resilience topology. **Neither successful free capacity allocation nor OCI provisioning has occurred**. Do not promise 500/1,000/10,000 children from these hypothetical CPU/RAM tiers without benchmark evidence. OCI Paid account does not automatically resize VMs; source metrics and owner-approved upgrade are required.
