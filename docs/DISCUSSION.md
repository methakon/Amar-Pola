# Project Discussion and Decisions

- **Project:** Amar-Pola
- **Document version:** 0.1
- **Date:** 2026-10-25
- **Status:** Initial baseline

## 1. Product concept

The product is a subscription-based parental monitoring and device-management system with three main parts:

1. A child-side Android app, configured by the parent on the child's device.
2. A parent-side app/dashboard for location, routes, usage reports, and supported controls.
3. A lightweight C++ backend that stores telemetry, handles paired-device commands, validates subscription entitlements, and coordinates optional media backup.

The child app should not need its main screen to remain open for all supported background features. Android may still impose foreground-service, notification, permission, privacy-indicator, lifecycle, and device-management requirements.

## 2. Requirements discussed

- Parent performs initial setup and grants applicable permissions on the child's phone.
- No separate child login is required in the initial design; securely pair the device to a parent account.
- Show the latest reported location on Google Maps, route history, and speed when available.
- Provide app-usage summaries by day, week, month, and year after Usage Access is granted.
- Support remote commands and scheduled restrictions where Android APIs permit them.
- App restrictions should be stronger in an appropriately provisioned managed-device mode; ordinary installation cannot universally prevent third-party apps from launching.
- Remote photo/video requests must be checked against Android version, permissions, enrollment mode, and supported capture mode. If the OS rejects an operation, return a truthful status rather than claiming success.
- Audio/camera use must follow applicable OS permissions, background restrictions, and privacy indicators.
- Only list or transfer files accessible through app-owned storage or appropriately granted access.
- Keep resource consumption low through adaptive sampling, batching, and bounded local queues.
- Allow parent-authorized Google Drive backup for selected media.
- Include secure pairing, encryption, retention controls, device revocation, audit logging, and paid subscriptions.

## 3. Decisions

### D-001 — Hybrid Android implementation
Use C++17/20 for shared/performance-sensitive logic and Kotlin/Java for Android lifecycle, services, runtime permissions, UsageStatsManager, location, camera integration, device policy, and WorkManager. A pure-C++ Android design is not recommended because the app still needs supported platform interfaces.

### D-002 — Permissions are not an OS bypass
The setup experience can guide the parent through runtime and special-access settings. Granting a permission does not remove all background-execution or device-policy restrictions, and permissions can later be revoked.

### D-003 — Two supported operating modes
- **Standard mode:** installed on an existing personal phone; feature availability is limited to APIs and permissions available to an ordinary app.
- **Managed mode:** phone is deliberately provisioned under Android device-management controls; stronger restrictions may be available.

The UI, backend capability profile, and documentation must not imply these modes provide identical functionality.

### D-004 — Capability-gated media requests
A parent-side photo/video request is only dispatched where the device's capability profile indicates a tested supported workflow. The child agent revalidates capability at execution time. Supported states include queued, accepted, completed, failed, unsupported, permission required, OS rejected, and user action required. Success requires confirmation of the resulting media.

### D-005 — Authorized and transparent capture
No covert capture, hidden indicators, permission bypasses, or techniques designed to evade Android safeguards. Implement only supported capture workflows with the required authorization and indicators.

### D-006 — Security and privacy by design
Use TLS, per-device credentials, least-privilege authorization, protected audit logs, encrypted sensitive data, revocation, configurable retention, and parent-authorized OAuth for Drive. Do not collect or store Google passwords.

### D-007 — Local-first reliability
Persist events locally in an encrypted queue and upload in batches. Expose location age and accuracy rather than presenting stale coordinates as live.

### D-008 — Honest command outcomes
Every command must have an ID, expiry, and auditable state. A queued or delivered request is not a completed operation.

## 4. Open questions

1. Minimum Android version and target API level.
2. Is managed-device enrollment optional or required for the first release?
3. Parent interface: native Android, web, or both?
4. Backend hosting environment, expected scale, and database choice.
5. Data-retention defaults and deployment/data-residency requirements.
6. Subscription regions, pricing, grace periods, refunds, and entitlements.
7. Google Play distribution and policy-review strategy.
8. Should media capabilities be deferred until compatibility tests complete?
9. Which phone manufacturers/models are in the first supported test matrix?

## 5. Acceptance principles

- Each feature has documented permission, enrollment, and compatibility requirements.
- Remote commands are authorized and have accurate execution status.
- The dashboard distinguishes live, stale, approximate, and unavailable data.
- The product does not promise universal app blocking or unrestricted background recording.
- Permission revocation, offline devices, and OS rejection produce clear degraded/error states.


## 6. Proposed feasibility assessment

This assessment records the initial planning view, not a guarantee that every feature works on every Android device. Final feasibility must be confirmed on target API levels, OEMs, permission states, distribution channel, and enrollment modes.

| Feature | Initial feasibility | Key condition / limitation |
|---|---|---|
| Pairing without a separate child account | Feasible | Short-lived pairing and revocable device credentials. |
| Background location, position, route history and speed | Feasible with conditions | Appropriate permissions, compliant background execution, connectivity, and accuracy/freshness reporting. |
| Daily/weekly/monthly/yearly app usage | Feasible with special access | Usage Access must be granted; available data depends on Android APIs. |
| Remote commands and file listing | Partial | Command delivery is feasible; file access is limited to app-owned or explicitly accessible storage. |
| Scheduled app blocking | Conditional | Strong enforcement generally requires supported device-policy controls and managed-device provisioning. Ordinary apps cannot universally block all other apps. |
| Remote photo/video requests | Conditional and capability-gated | Check OS/API level, permission, service/lifecycle restrictions, enrollment mode, and tested device behavior; report OS rejection or user-action-required states truthfully. |
| Remote audio recording | Restricted / requires validation | Runtime permission alone does not guarantee arbitrary background activation; use supported authorized workflows and honor privacy indicators. |
| Parent-authorized Google Drive backup | Feasible | OAuth authorization, least-privilege scopes, secure token handling, and upload retry/resume. |
| Subscription billing | Feasible | Trusted provider integration and server-side entitlement validation. |
| Low CPU/RAM/battery use | Goal, not yet measured | Adaptive sampling, bounded queues, batching, and real-device performance tests are required. |
| Lightweight C++ backend | Feasible | Production-grade TLS, authentication, rate limiting, secure storage, monitoring, and operations are required. |

### Feasibility validation plan

1. Select a minimum Android API level and representative devices/OEMs.
2. Test standard installation and managed-device enrollment separately.
3. Verify each permission/special-access flow, including later revocation.
4. Test location in background, stationary/moving states, offline recovery, and battery impact.
5. Test Usage Access and usage aggregation.
6. Test app restrictions on a properly provisioned managed test device.
7. Test camera/audio requests against actual OS behavior; verify indicators and truthful command statuses.
8. Validate Google OAuth/Drive upload, subscription entitlement, security, and retention.
9. Record results as **Pass**, **Pass with conditions**, **Fail**, or **Not tested**, including OS/device/build details.

No feature should be described as production-supported until this validation is complete.

## 7. Follow-up conditional feasibility review — 2026-10-25

The initial matrix in section 6 was a preliminary assessment. A more detailed, source-linked review is maintained in [Feature Feasibility Conditions and Evidence](FEASIBILITY_CONDITIONS_AND_EVIDENCE.md). Treat the newer document as authoritative for **why** features work, **what conditions** are needed and **what remains unsupported**. In particular:

- Eligible applications may be suspended under correctly provisioned managed-device policy APIs; ordinary runtime permissions alone do not confer that authority.
- Camera/microphone access is not universally impossible but is highly conditional on permitted platform execution context, privacy/disclosure requirements and independent distribution approval. Unrestricted or concealed remote recording is not a product promise.
- The initial parent-granted-permissions assumption remains, but permission grants do not override background execution constraints.
- Proposed roadmap, Play declaration and validation details are in [Implementation Technical Specification](IMPLEMENTATION_TECHNICAL_SPECIFICATION.md), [Google Play Publishing Requirements](GOOGLE_PLAY_PUBLISHING_REQUIREMENTS.md) and [Validation and Release Plan](VALIDATION_AND_RELEASE_PLAN.md).
- **No Android device compatibility results or Google Play approvals have yet been obtained.**

## 8. New product request: parent-labeled addresses, road history and multiple stops (2026-10-25)

The parent shall be able to create arbitrary address/coordinate pins with titles and see these labels near the observed child position on Google Maps. Historical movement shall be shown as a segmented, time-ordered travelled track with multiple dwell-stop markers, not a computed directions route presented as a fact.

**Decision D-013:** Evaluate stops and named-place matches on the C++ backend so the child need not run geocoding or map rendering. Parent place markers require no additional child GPS sampling.

**Decision D-014:** Use adaptive location modes and define the measurable battery/accuracy trade-off. Default to lower-power, potentially sparse tracks; reserve time-limited high-detail recording for genuine need.

**Decision D-015:** Apply road matching only to sufficiently dense, reliable vehicle observations **after** checking Google Roads API commercial tracking license and content retention terms. Sparse segments and unknown gaps shall remain explicitly approximate/unknown.

**Decision D-016:** Preserve independent device provenance when watches/tablets/phones may report the same child's position. Watch GNSS absence and disconnects must not be hidden.

Detailed conditions, technical approach, schemas, API endpoints and device tests: [Live Trip Route, Named Places and Battery Specification](LIVE_TRIP_ROUTE_NAMED_PLACES_BATTERY_SPECIFICATION.md).
