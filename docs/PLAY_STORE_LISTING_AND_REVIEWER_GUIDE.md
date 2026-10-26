# Play Store Listing, Reviewer Access and Submission Checklist

> **Product names:** **Madalasa** (parent app), **Alarka** (child app). Desired repository name **Madalasa-Alarka** is **completed GitHub repository rename**. Use the verified new repository URL for all current documentation and integrations. [Naming rationale](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | 2026-10-25 | Draft; must reflect actual shipped functionality**

## 1. Store listing copy — parent app (candidate, unapproved)

**Title candidate:** Madalasa — Family Safety

**Short description candidate:** Child location history and app-use insights for parents.

**Long description candidate:**

“Madalasa–Alarka helps parents and guardians review location history and device-usage information on a child's Android phone after it has been set up with the necessary permissions.

Available supported features may include:
- Last reported device location on a map, with accuracy and freshness.
- Trip history, route views and optional reported travel speed.
- Daily, weekly, monthly and yearly app usage summaries after Android Usage Access is granted.
- Supported device policies on appropriately managed phones.
- Device pairing, monitoring status and parent-controlled retention settings.

Setup requires access to the child's device. Madalasa–Alarka is an identifiable monitoring tool; the child-side app provides required disclosures and persistent monitoring notification while operating. Feature availability differs by Android version, permissions, phone manufacturer and whether the phone is managed. The app does not guarantee continuous GPS tracking, arbitrary app blocking or unannounced camera/microphone access.

A paid subscription may be required for certain features. Availability, price and terms are shown in the app.”

**Do not publish this paragraph until every included feature is actually released and verified.**

For a separately listed child agent, write a clear child-device setup listing that explicitly identifies data collection, parental monitoring purpose, permissions and the persistent notification.

## 2. Required graphic and content deliverables

- Real app icon, consistent developer brand and identifiable child app icon.
- Store feature graphic, appropriate aspect ratio and quality per latest Play specifications.
- Minimum required screenshot set per device category; each image must depict the **actual app**, not concepts.
- Localized description and privacy/disclosure text in supported languages.
- Support contact; public privacy-policy and account-deletion URLs.
- Screenshots for parent map/history, app usage, pairing, authorized policy controls, and monitoring disclosure (only when implemented).
- Subscription terms/price/free trial disclosure wherever shown.

Do not invent reviews, benchmark claims or screenshots of features not included in the uploaded release.

## 3. Reviewer instructions — to complete using real release candidates

```text
Package name(s):
Parent demo account username:
Parent demo access credentials or test login instructions:
Child pairing test code flow:
Test device(s) available to reviewer or test simulation workflow:
Exact steps to reach each declared monitoring feature:
Steps to view disclosure and persistent notification:
Background location demonstration video:
App restrictions test: standard mode vs managed mode:
Subscription demo/test entitlement steps:
Instructions for optional Google Drive consent:
Country/account access restrictions:
Support contact for review:
Features intentionally disabled in this build:
```

**Never put production passwords, permanent device enrollment keys, or private customer data in repo documentation.** Supply testing credentials through the secured Play Console reviewer-access entry.

## 4. Public communication boundaries

Allowed marketing themes: “family location history”, “parental device supervision”, “supported screen-time insights”, “managed-device restrictions”. Avoid “secret,” “invisible,” “spy,” “without the child knowing,” “guaranteed camera access,” “record without notification,” and unmeasured battery claims.

## 5. Publication workflow

1. Verify publisher identity/account prerequisites and app ownership.
2. Register unique package name(s) and app signing.
3. Upload release AAB to internal test.
4. Resolve pre-launch report crashes, permission and 16 KB page-size warnings.
5. Complete App content forms (ads, target audience, rating, privacy, Data safety, reviewer access and sensitive permission declarations).
6. Upload relevant real demonstration videos for background location and other selected declarations.
7. Verify in-app account deletion and public web deletion URL.
8. Run required closed testing, if account subject to production-access gate.
9. Validate billing products, pricing, taxes and subscriptions.
10. Submit for review, process findings, then staged rollout.
11. Reconcile Play listing, SDKs, permission/declaration forms and privacy policy on **every** update.

## Sources

- https://support.google.com/googleplay/android-developer/answer/9859455
- https://support.google.com/googleplay/android-developer/answer/9799150
- https://support.google.com/googleplay/android-developer/answer/9888380
- https://support.google.com/googleplay/android-developer/answer/14151465


## New two-app public names (owner-approved)

**Parent app:** **Madalasa — Family Safety** (candidate listing title). **Child companion:** **Alarka — Family Safety Companion** (candidate listing title). Each needs independent Play publisher and data disclosures. Alarka must display visible child-monitoring notifications and ask permissions on the child's phone. No guaranteed emergency dispatch or covert capture claims; app IDs and titles still require store verification.

## Conditional media features: no premature reviewer or listing claims (2026-10-26)

Owner accepts media and scoped-file **R&D** with exact parent-facing failure explanations. Do not advertise/bill these features as released, pretend media works on all Android devices, claim hidden listening or suppress system camera/mic indicators. Alarka main Activity normally stays closed after initial setup but monitoring notification, app icon, sensor indicators and required child-visible prompts remain. Android MediaProjection screen viewing requires fresh system consent for each session. If the feature is ever submitted, verify every relevant Android/OEM/standard/managed-device scenario, accurate monitoring disclosure, guardian verification, manifest/FGS permissions, children/Families eligibility, privacy and recording retention. [MA-MEDIA-ADR-001](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md). Commercial feature flag stays OFF until release gates pass.

## 2026-10-27 permission onboarding UX and reviewer evidence requirements

The proposed Alarka-first-launch compatibility scan must be **read-only** and explained: detect public hardware/API availability without turning on camera/microphone, collecting location or reading file contents. After verified family pairing, OS permission requests are staged with clear in-app purpose and user-controlled standard Android dialogs / Settings / Photo Picker / SAF selectors, followed by **actual Android recheck** and child-device report sync. Do not claim the parent can grant permissions remotely, force all optional permissions, hide Alarka after setup or offer screen sharing without new per-session Android consent.

If publicly released after policy clearance, reviewer video must show (a) Alarka's identifiable icon/notifications and disclosure, (b) appropriate foreground then separately requested background location for API30+, (c) denial/skipping and limited modes, (d) server acknowledgement and Madalasa accurate granted/conditional/offline indicator, and (e) later revocation/reapproval without false instant notification. A Figma screen is not compliance proof; submit real signed build/screens/permission declarations. Protected India child location/usage/media features remain blocked until official/purpose review. [MA-CAP-ADR-002](CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md); [Figma](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=23-2).
