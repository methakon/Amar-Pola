# Android Version and Device Compatibility Matrix

**Amar-Pola | 2026-10-25 | No device tests executed**

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
