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
