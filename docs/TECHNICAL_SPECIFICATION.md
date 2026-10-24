# Technical Specification

- **Version:** 0.1
- **Date:** 2026-10-25
- **Status:** Proposed architecture

## 1. System architecture

```text
Child Android device
  Kotlin/Java platform layer
    - permission onboarding and capability checks
    - location foreground service + Android location APIs
    - UsageStatsManager integration
    - optional DevicePolicyManager (managed mode)
    - authorized capability-gated media adapter
    - WorkManager / push-assisted synchronization
               | JNI / stable C API
  C++ core
    - event model, validation, policy parsing, queue helpers
               |
  Encrypted local queue (SQLite) + HTTPS client
               |
               | TLS
               v
C++ backend (Drogon or Boost.Beast)
  Auth/pairing | Commands | Telemetry | Policies | Subscription adapter
  Audit        | Retention/deletion | Drive upload coordination
               |
      PostgreSQL / optional push provider
               |
       Parent app/dashboard
         - Google Maps
         - location and usage reports
         - supported remote controls
         - Google Drive authorized backup
```

## 2. Technology choices

### Child Android agent
- Kotlin for Android lifecycle-aware integration, services, permissions and platform API calls.
- C++17/20 via Android NDK for performance-sensitive/shared business logic.
- Keep JNI narrow and versioned; do not route every platform API through C++.
- WorkManager for deferrable synchronization, not as a replacement for a permitted continuous location service.
- Use a location foreground service only where needed and compliant with the relevant Android rules.
- UsageStatsManager after Usage Access is granted.
- DevicePolicyManager only in valid supported managed enrollment.
- Isolate camera/audio functionality behind tested capability interfaces.

### Parent interface
Initial recommendation: Kotlin + Jetpack Compose for a native Android parent app. A web dashboard can be added later on the same API. Google Maps SDK renders current/last-known position, accuracy, markers, polylines, and route playback.

### Backend
- C++17/20.
- Drogon for an asynchronous web framework, or Boost.Beast for a more controlled low-level HTTP implementation.
- PostgreSQL for multi-account production data.
- SQLite for local child queue; use a managed persistent database for the production backend.
- TLS termination, authentication, rate limiting, input validation, structured logs, metrics, backups, and security patching are required operational concerns.

## 3. Proposed repository layout

```text
Amar-Pola/
├── android/
│   ├── child-app/
│   └── parent-app/
├── backend/
│   ├── CMakeLists.txt
│   ├── src/
│   └── tests/
├── shared/
│   ├── include/amar_pola/
│   └── src/
├── infra/
├── docs/
└── scripts/
```

This is a future implementation layout; it does not imply that those implementation files exist yet.

## 4. Capability negotiation and platform compatibility

Do not infer support from Android version alone. At enrollment and periodically thereafter, the child agent should report:
- Android API level and app version.
- Standard versus managed enrollment mode.
- Current relevant runtime permissions and special-access state.
- Tested/supported feature flags with reason codes.
- Last capability refresh timestamp.
- OEM/model details only where needed for diagnostics, with data minimization.

Example capability flags:
- `background_location`
- `usage_stats`
- `managed_app_restrictions`
- `authorized_photo_capture`
- `authorized_video_capture`
- `authorized_audio_capture`

Parent-side Drive authorization is a separate server/integration state. Capability profiles are advisory and time-sensitive; the child agent must revalidate sensitive operations immediately before execution.

### Photo/video command lifecycle
1. Parent submits an action request.
2. Backend authenticates parent, authorizes target device, checks pairing/subscription/expiry and reported capability.
3. Backend stores a command with unique ID and expiry.
4. Child agent receives command using supported push/synchronization.
5. Agent rechecks permission, lifecycle/service requirements, enrollment mode, and current OS capability.
6. If blocked, return `UNSUPPORTED`, `PERMISSION_REQUIRED`, `OS_REJECTED`, or `USER_ACTION_REQUIRED` as appropriate.
7. Run only an authorized supported capture workflow.
8. Confirm media creation and local persistence before reporting `COMPLETED`.
9. Register metadata and upload only within configured authorization and retention policies.

A queued/delivered request is not a completed capture.

## 5. API proposal

All routes require TLS. Parent routes require parent authentication; device routes require device credentials and target-device authorization. Names are illustrative and should be finalized in OpenAPI before implementation.

### Parent API
- `POST /v1/pairing-codes` — issue a short-lived pairing code.
- `POST /v1/devices/{deviceId}/commands` — create a remote command.
- `GET /v1/devices` — list paired devices and state.
- `GET /v1/devices/{deviceId}/locations?from=&to=` — location history.
- `GET /v1/devices/{deviceId}/usage?period=` — usage aggregates.
- `GET /v1/devices/{deviceId}/commands/{commandId}` — command result.
- `DELETE /v1/devices/{deviceId}/pairing` — revoke pairing.
- `GET /v1/audit-events` — authorized audit history.
- `POST /v1/integrations/google-drive/revoke` — revoke Drive link.

### Child API
- `POST /v1/enroll` — redeem pairing code.
- `POST /v1/devices/{deviceId}/heartbeat` — connection/capability state.
- `POST /v1/devices/{deviceId}/locations:batch` — upload location points.
- `POST /v1/devices/{deviceId}/usage:batch` — upload usage aggregates.
- `GET /v1/devices/{deviceId}/commands` — poll pending commands where push is unavailable.
- `POST /v1/devices/{deviceId}/commands/{commandId}:result` — report command outcome.
- `POST /v1/devices/{deviceId}/media` — register authorized media metadata.

## 6. Logical data model

### `parent_accounts`
- `id` UUID primary key
- `auth_provider`, `provider_subject`
- `created_at`, `status`

### `devices`
- `id` UUID primary key
- `parent_account_id` foreign key
- `display_name`, `platform`, `android_api_level`, `app_version`
- `management_mode`, `capability_profile` JSONB
- `last_seen_at`, `paired_at`, `revoked_at`

### `location_points`
- `id` UUID primary key
- `device_id` foreign key
- `observed_at`, `latitude`, `longitude`, `accuracy_m`
- optional `speed_mps`, `bearing_deg`, `altitude_m`
- `ingested_at`; index `(device_id, observed_at)`

### `usage_aggregates`
- `id` UUID primary key
- `device_id`, `package_name`
- `period_start`, `period_end`, `foreground_duration_ms`
- `collected_at`

### `policies`
- `id` UUID primary key
- `device_id`, `policy_version`, `policy_type`, `policy_json`
- `created_by`, `created_at`, `enabled`

### `commands`
- `id` UUID primary key
- `device_id`, `parent_account_id`, `command_type`, `payload_json`
- `created_at`, `expires_at`, `status`, `result_code`, `result_summary`, `completed_at`
- unique idempotency key

### `media_objects`
- `id` UUID primary key
- `device_id`, `media_type`, `created_at`, `size_bytes`, `sha256`
- `authorization_context`, `upload_state`, optional Drive file reference
- Never store OAuth access tokens in this table.

### `audit_events`
- `id` UUID primary key
- `actor_type`, `actor_id`, `device_id`, `event_type`, `occurred_at`
- Minimal structured metadata; exclude secrets and unnecessary raw payloads.

Use retention/deletion jobs. Partition historical location data by time only when scale warrants it.

## 7. Security model

- TLS 1.2+; prefer TLS 1.3 where supported.
- Short-lived one-time pairing codes, rate limiting, and brute-force protections.
- Unique, revocable, rotatable device credentials.
- Parent authentication through a trusted identity provider or passkeys.
- Object-level authorization on every device/history/command/media endpoint.
- Server-side subscription entitlement validation.
- Secrets in a managed secret store, not source code or mobile binaries.
- Encrypt sensitive database volumes/backups; evaluate field-level encryption for high-risk fields.
- Minimize Google Drive OAuth scopes; prefer the narrowest suitable app-controlled storage scope.
- Never collect/store Google passwords.
- Audit security-sensitive actions; restrict audit-log access.
- Define threat model, incident response, backups, restore tests, and key rotation before production.

## 8. Privacy, retention and deletion

- Collect only data required for enabled functions.
- Publish retention defaults and allow configuration within product policy.
- Provide access review, device revocation, integration revocation, and deletion workflows.
- Cover primary records, derived reports, queued uploads, and backups under the documented retention/deletion schedule.
- Keep sensitive payloads out of ordinary logs, crash reports, analytics, and push messages.
- Define consequences of subscription expiry, unpairing, and account deletion.

## 9. Performance design

- Adaptive location intervals/distance thresholds; no busy-loop GPS polling.
- Batch location and usage records; compress where useful.
- Bounded local queues with backpressure and expiry.
- Exponential backoff with jitter for transient network failures.
- Separate critical location operation from deferrable reports and media uploads.
- Avoid frequent empty polling; use push where reliable and a periodic sync fallback.
- Measure idle/moving battery drain, CPU, resident memory, upload volume, and recovery time on a representative device matrix before defining budgets.
- Do not claim a fixed battery saving before testing.

## 10. Command states

Suggested states:
- `CREATED`
- `QUEUED`
- `DELIVERED`
- `ACCEPTED`
- `COMPLETED`
- `FAILED`
- `EXPIRED`
- `UNSUPPORTED`
- `PERMISSION_REQUIRED`
- `OS_REJECTED`
- `USER_ACTION_REQUIRED`
- `DEVICE_OFFLINE`
- `CANCELLED`

Validate transitions server-side and retain timestamps and concise reason codes. Do not log sensitive command payloads.

## 11. Testing strategy

- C++ unit tests for event validation, serialization, queue behavior, policy parsing, and command-state transitions.
- Android instrumentation tests for permission state, background services, usage access, location, and managed-device enrollment.
- Device matrix testing across supported API levels and selected OEMs.
- Integration tests for pairing, authorization, idempotency, offline recovery, command expiry, and Drive upload.
- Security tests for object authorization, token leakage, replay, brute force, revocation, and deletion.
- Performance tests for stationary/moving collection, network loss, memory pressure, and battery impact.
- Capture compatibility tests must verify real OS behavior and privacy indicators; do not infer availability from OS version alone.

## 12. Deployment and operations

- Containerize backend where appropriate; deploy behind a hardened TLS endpoint/reverse proxy.
- Use migrations and backward-compatible API versioning.
- Separate development/staging/production credentials.
- Configure database backups, restore tests, monitoring, rate limits, alerting, and patching.
- Do not expose a raw C++ server directly to the public internet without input validation, authentication, rate limiting, and operational monitoring.

## 13. Official documentation to re-check during implementation

- Android background location: https://developer.android.com/develop/sensors-and-location/location/background
- Android foreground services: https://developer.android.com/develop/background-work/services/foreground-services
- Android UsageStatsManager: https://developer.android.com/reference/android/app/usage/UsageStatsManager
- Android device policy: https://developer.android.com/work/dpc
- Google Maps SDK for Android: https://developers.google.com/maps/documentation/android-sdk
- Google Drive API: https://developers.google.com/drive/api/guides/about-sdk
- Google Play Billing: https://developer.android.com/google/play/billing
