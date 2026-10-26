# Android Version and Device Compatibility Matrix

> **Current product naming:** **Madalasa** parent/guardian app, **Alarka** child companion; GitHub repository [Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka). [Brand and Markandeya Purana context](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | 2026-10-25 | No device tests executed**

## 1. Testing policy

Android API level alone is **not sufficient** to determine success. For every cell, record manufacturer, OS build/security patch, app version/targetSdk, permission state, device-owner status, FGS type, notification/indicator observation, result and log reference.

Legend: `N/T` = not tested; `P` = passed on named device; `C` = passed with conditions; `F` = failed; `N/A` = platform unsupported.

## 2. Device support candidates

| Android | API | Standard location | Usage Access | Managed app suspension | Authorized camera/audio mode | Status |
|---|---|---|---|---|---|---|
| Android 10 | 29 | Test needed | Test needed | Test only after owner provisioning | Test permitted visible workflow | N/T |
| Android 11 | 30 | Test needed | Test needed | Test only after owner provisioning | Test permitted visible workflow | N/T |
| Android 12 | 31 | Test needed | Test needed | Test only after owner provisioning | Test permitted visible workflow | N/T |
| Android 12L | 32 | Test needed | Test needed | Test only after owner provisioning | Test permitted visible workflow | N/T |
| Android 13 | 33 | Test needed | Test needed | Test only after owner provisioning | Test permitted visible workflow | N/T |
| Android 14 | 34 | Test needed; typed foreground services | Test needed | Test only after owner provisioning | Typed FGS and while-in-use restrictions require careful validation | N/T |
| Android 15 | 35 | Test needed; power restrictions | Test needed | Test only after owner provisioning | Test permitted visible workflow | N/T |
| Android 16 | 36 | Test needed; target new Play apps | Test needed | Test only after owner provisioning | Test permitted visible workflow, privacy indicator | N/T |

`minSdk=29` is a **proposed** engineering choice; no supported device range is finalized. New standard phone app submissions target API **36+** under current Play requirements. Android/OEM service behavior can vary by OS version and target SDK; rerun after every major change.

## 3. Per-feature prerequisites

| Feature | Standard app prerequisite | Managed-mode prerequisite | Must measure |
|---|---|---|---|
| Background location | Foreground/background grants where appropriate, location enabled, compliant service | Same; DPC does not replace permission/OS location rules | Fix timestamp, accuracy, stale state, battery |
| Usage collection | User grants Usage Access in Settings | Same or policy-supported equivalent if documented | Aggregation, access loss, coverage |
| App suspension | Not universally supported | Properly provisioned DPC with authorized policy APIs | Eligible app suspended/restored; excluded packages; restart/rollback |
| File browsing | Owned files, MediaStore/SAF authorized locations | Policy-specific access does not automatically defeat sandbox | Deny other apps' private files |
| Camera/mic recording | Explicit authorized visible workflow and permitted lifecycle | Validate documented owner exceptions as *test candidates*, without concealing recording | Permission denial, privacy indicators, service start, OS error, session result |
| Monitoring identity | Identifiable icon/disclosures/notifications | Same | Notification visibility and listing accuracy |

## 4. Test form

```yaml
case_id: AP-ANDROID-001
device_model: TBD
manufacturer: TBD
android_api: 36
build_fingerprint: TBD
target_sdk: 36
app_build: TBD
enrollment_mode: STANDARD
permissions: {}
network: WIFI
battery_saver: false
screen_state: OFF
test_action: background_location
expected: compliant timestamped fix or explicit unavailable
actual: NOT_TESTED
android_privacy_indicators: NOT_TESTED
app_notification: NOT_TESTED
logs_reference: null
result: NOT_TESTED
reviewer: null
```

## 5. Specific test scenarios

- Fresh install, normal disclosure, permission denied/granted and later revoked.
- Background vs foreground location, device restart, app force-stop, network loss, GPS unavailable.
- Motion transitions and timestamp freshness with power saver/OEM optimization.
- Usage report under time zone changes and midnight boundaries.
- DPC first enrollment vs standard install; suspend and restore permitted targets.
- Explicit supported media flow: visible indicator, interruption, OS rejection, correct command status.
- Managed mode must be tested on an actual appropriately provisioned physical device; do not treat a simulated role as device owner.
- Parent map freshness, route gaps, account unlink, storage deletion and remote command replay.

## 6. Promotion to supported status

Promote a configuration from `N/T` to `P`/ `C` only with a reproducible test, matching build hash, evidence and owner approval. Product feature flags must be computed from actual verified combination; don't infer that “Android 14 supports X” simply from an API's existence.

## 7. Conditional media and reason-UX test expansion (2026-10-26)

**RESEARCH / NOT TESTED:** Alarka main Activity stays closed after setup, but monitoring notification and Android camera/microphone indicators must remain discoverable. Run `T-MEDIA-01–18` from [MA-MEDIA-ADR-001](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md) independently on STANDARD and genuine MANAGED_DEVICE_OWNER physical devices across Android 10–16 candidates; normal Device Administrator cannot be treated as fully managed. Test start vs continuation of camera/microphone FGS, OS 14+ while-in-use checks, on-device notification interaction, denied/revoked permissions, camera/mic system toggle, locked/offline/killed phone, power saver, sensor busy, network switch and explicit session stop.

**Parent proof:** capture `Command.status`, actual `reason_code`, parent-facing copy and safe next step for every outcome; do not infer permission failures from offline/stale capability snapshots. Validate per-session Android MediaProjection consent, FLAG_SECURE exclusion, MediaStore/SAF allowed roots/revocation, snapshot flash-off on actual devices, no VPS stored media and guardian-revocation stop. Extend every device-test record with `requested_feature`, `fgs_type`, `actual_permission_at_execution`, `enrollment_mode`, `parent_status`, `parent_reason`, `indicator_visible`, `command_receipt`, `stream_stopped`, and `evidence_id`. Remain N/T until physical proof.

## 8. 2026-10-27 first-install capability scan and permission change matrix

**New physical-device test program:** See [MA-CAP-ADR-002](CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md). Record `T-CAP-01…24` in STANDARD and truly provisioned MANAGED_DEVICE_OWNER mode on Android API 29–36/OEMs with exact model/build/targetSdk, initial hardware scan, grant scope (denied, one-time, selected media, partial/approximate, foreground/background), sensor runtime context, release flag, `checked_at`, `report_version`, durable server ACK and Madalasa output. A device's camera hardware detection does **not** verify camera open/background FGS eligibility; `DevicePolicyManager` owner is distinct from legacy administrator. No child location/usage/media actually collected during read-only hardware discovery.

**Lifecycle verification:** permission flow triggers a system-owned dialog/Settings; Android 11+ foreground location must be granted **before** background location step. On dialog result, onResume, process restart/revocation, feature execution and legitimate WorkManager sync Alarka rechecks OS state. Simulate one-time grant expiration, Android permission auto-reset, app process termination on revoke, notifications disabled, locked/force-stopped device, Doze, network outage, Wi-Fi→mobile transitions, concurrent screen-share per-session prompts and SAF URI revocation. Madalasa shows verified GRANTED for permission only, not unverified active sensor, and STALE/UNKNOWN for offline/no ACK. Parent green operational requires matching supported OS, **fresh** access, permitted execution and enabled release flag. All T-CAP results remain NOT_TESTED.
