# Feature Feasibility Conditions

**Project:** Amar-Pola  
**Date:** 2026-10-25  
**Status:** Documentation review; no device tests completed

## Assessment definitions

- **Feasible:** supported through a public Android API with normal grants.
- **Conditional:** supported only with a qualifying device setup and verified Android behavior.
- **Partial:** a limited version can be implemented; full functionality is not promised.
- **Unsupported:** cannot be guaranteed through public Android APIs.

| Feature | Status | Why and conditions |
|---|---|---|
| No child login | Feasible | Short-lived pairing code and per-device credentials |
| Location and speed | Conditional | Location grants, OS background rules, accurate satellite/network fix; speed may be unavailable |
| Route history | Feasible | Store timestamped positions; show coverage gaps |
| App usage summaries | Conditional | Usage Access granted; server builds daily to yearly aggregates |
| Scheduled app suspension | Conditional | Supported managed-device policy controller using DevicePolicyManager; some packages cannot be suspended |
| Immediate termination of another app | Partial | Suspension restricts eligible packages; universal force-stop is not a public ordinary-app capability |
| File listing | Partial | App-controlled files and user-authorized collections, not other apps' private data |
| Camera/photo/video | Restricted/conditional | Permission alone does not guarantee background capture; compliant, disclosed workflows are required |
| Microphone/audio | Restricted/conditional | Permission alone does not guarantee background recording; compliant, disclosed workflows are required |
| App without open screen | Feasible | Android background components; platform notifications/indicators still apply |
| Hidden monitoring | Unsupported for a Play release | Monitoring must not be disguised; persistent notification and identifiable icon when running |
| Drive upload | Feasible | Parent OAuth authorization and resumable upload |
| Subscriptions | Feasible | Play Billing and verified backend entitlements |
| Low resource use | Test target | Adaptive collection and benchmarking |

## Decision gates

1. Confirm public Android API support and documented permissions.
2. Verify on the intended Android API levels and handset models.
3. Verify Google Play distribution requirements separately.
4. Record status as NOT_TESTED, PASS, PASS_WITH_CONDITIONS, or FAIL.

## Key technical distinctions

**Standard installation:** parents can grant location and Usage Access, but these grants do not make the app a device owner.

**Managed installation:** supported device-owner provisioning can authorize stronger package restrictions. Managed enrollment is a distinct provisioning operation, often requiring setup of a new or reset phone; it is not a permission toggle.

**Media:** camera and microphone requests need platform-compliant user authorization, visible system indicators and lifecycle permissions. Android documents specific exceptions to foreground-service starting rules, but they do not guarantee unrestricted background recording or Google Play acceptance. The product should return clear unsupported/permission-required/user-action-required outcomes rather than claiming success.

## References

- [Android foreground services](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start)
- [Android device policy](https://developer.android.com/reference/android/app/admin/DevicePolicyManager)
- [Android managed-device provisioning](https://developer.android.com/work/dpc/dedicated-devices)
- [Google Play monitoring policy](https://support.google.com/googleplay/android-developer/answer/9888380)
- [Play location declaration](https://support.google.com/googleplay/android-developer/answer/9799150)
