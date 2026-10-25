# Play Store Listing, Reviewer Access and Submission Checklist

**Amar-Pola | 2026-10-25 | Draft; must reflect actual shipped functionality**

## 1. Store listing copy — parent app (candidate, unapproved)

**Title candidate:** Amar-Pola Family Safety

**Short description candidate:** Child location history and app-use insights for parents.

**Long description candidate:**

“Amar-Pola helps parents and guardians review location history and device-usage information on a child's Android phone after it has been set up with the necessary permissions.

Available supported features may include:
- Last reported device location on a map, with accuracy and freshness.
- Trip history, route views and optional reported travel speed.
- Daily, weekly, monthly and yearly app usage summaries after Android Usage Access is granted.
- Supported device policies on appropriately managed phones.
- Device pairing, monitoring status and parent-controlled retention settings.

Setup requires access to the child's device. Amar-Pola is an identifiable monitoring tool; the child-side app provides required disclosures and persistent monitoring notification while operating. Feature availability differs by Android version, permissions, phone manufacturer and whether the phone is managed. The app does not guarantee continuous GPS tracking, arbitrary app blocking or unannounced camera/microphone access.

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
