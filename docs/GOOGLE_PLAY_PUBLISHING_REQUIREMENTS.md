# Google Play Publishing and Compliance Specification

> **Product names:** **Madalasa** (parent app), **Alarka** (child app). Desired repository name **Madalasa-Alarka** is **completed GitHub repository rename**. Use the verified new repository URL for all current documentation and integrations. [Naming rationale](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | 2026-10-25 | Draft only — not a publication approval**

Applies separately to a parent client and a child agent if distributed as separate packages. Final answers must be based on the **actual shipped manifests, SDKs, backend behavior and every active Play track**.

## 1. Critical go/no-go conditions

1. **New standard Android apps/updates target Android 16, API 36+, from August 31, 2026** (specialized form-factor exceptions and extension arrangements are separate). Verify again at submission.
2. **Monitoring apps must be exclusively positioned for parental child monitoring or permitted enterprise management.** Display recognizable icon, clear tracking disclosures and a persistent notification while the app runs; do not cloak monitoring. Declare `isMonitoringTool` with `child_monitoring` value in each child-monitoring build on every Play track. Check exact manifest placement against current Android manifest documentation at build time.
3. Camera, audio and other sensitive capabilities may be technically conditionally possible, but **will not be shipped until the supported user-visible behavior and actual Play policy review have been satisfied**. Do not offer alternate noncompliant APK links from the listing or application.
4. Background location is a sensitive core feature; Play requires prominent in-app disclosure, a background location declaration and demonstration video when required, and a matching privacy policy.
5. If a parent account can be created, provide account deletion from within the app **and through a working web deletion-request URL**.
6. Complete accurate Data safety declarations, target audience, ads, access/reviewer instructions and permissions/foreground-service forms applicable to the final app.
7. Because the app contains native C++, validate 16 KB memory page size support on 64-bit devices and packaged native libraries.
8. Use Play Billing for paid digital capabilities sold in a Play-distributed Android app where the policy requires it; validate purchases server-side.

## 2. Application/package separation

| Package | Purpose | Suggested distribution |
|---|---|---|
| Parent app | Maps, reporting, controls and subscription | Standard Play listing |
| Child agent | Parentally configured monitoring and permitted device controls | Separate explicitly declared monitoring application; distribution path must pass Play review |
| Managed DPC variant | Fully managed device policies via explicit provisioning | Investigate appropriate device-management/enterprise distribution and Play eligibility separately; do not assume a consumer install can acquire device-owner authority |

Each application needs its own final package name, signing configuration, store listing, permissions, Data safety answers and policies where Play treats them separately.

## 3. Manifest and permission declaration worksheet

**Do not copy all permissions into an app. Include only permissions used by a released feature.**

| Capability | Android declaration / access to investigate | Play review / condition |
|---|---|---|
| Foreground / background location | `ACCESS_COARSE_LOCATION`, `ACCESS_FINE_LOCATION`, `ACCESS_BACKGROUND_LOCATION` as justified | Permission timing and prominent disclosure; background location form and video |
| Location foreground service | `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_LOCATION`, service type `location` where appropriate | Foreground-service type declaration and actual use-case demonstration as required |
| Notifications | `POST_NOTIFICATIONS` runtime permission on relevant versions; notification channel | Persistent monitoring notification must not be hidden; handle denial coherently |
| Usage access | `PACKAGE_USAGE_STATS` special access via Settings | Explain use clearly and map app activity to Data safety |
| Installed app visibility | Narrow `<queries>` where possible, possibly `QUERY_ALL_PACKAGES` only with a documented eligible core use | Broad package visibility is restricted and requires declaration/review when applicable |
| App suspension | DevicePolicyManager with valid device owner/profile owner/delegate state | Correctly provisioned DPC; ordinary permission onboarding is not sufficient |
| Photo/video | `CAMERA`, possible camera foreground-service type and related FGS permission only for a supported release workflow | Lifecycle/while-in-use restrictions, clear indication, permission disclosure; feature stays deferred without approval |
| Audio recording | `RECORD_AUDIO`, possible microphone foreground-service type and permission only for a supported release workflow | As above; no hidden, unannounced capture |
| Local media/files | MediaStore/SAF access and modern photo picker as appropriate | No arbitrary private app storage |
| Network | `INTERNET`, network state only if actually required | Encrypt transport; list third-party SDKs and data recipients |

**Monitoring flag candidate (verify exact position during manifest integration):**
```xml
<meta-data android:name="isMonitoringTool"
           android:value="child_monitoring" />
```
This alone does **not** certify compliance. Every version code on every active testing/release track must reflect the actual monitoring design.

## 4. Background location permission declaration package

**Core-feature rationale draft:**
“Madalasa–Alarka is a parent-configured child location history and safety application. Background location is needed to record journeys and update a parent's last-known location while the child-side setup screen is closed. Without background access, route history would have substantial gaps and location updates would be limited to the setup screen.”

**Draft prominent in-app disclosure** (validate exact shipped language):
“Madalasa–Alarka collects location data to provide your parent or guardian with your last reported position, travel history and movement alerts, including when this app is closed or not in use. Location reports are securely sent to the paired parent account. You can review monitoring information in Madalasa–Alarka and Android settings.”

Review the wording with legal/policy advisers for child audience and the actual feature list. Show this disclosure in the child app **before** requesting location permission, not solely in Terms or the privacy policy.

**Reviewer video storyboard** (record real device later):
1. Show named Madalasa–Alarka child app and prominent disclosure in normal onboarding.
2. Show Android permission and background-location setup.
3. Show monitoring notification.
4. Close the child setup Activity; move between test coordinates on test device.
5. Show the parent app's latest location/history and timestamps.
6. Provide a public/test-viewable unlisted video URL and exact test credentials or demo instructions; no fabricated evidence.

## 5. Play Console app content submission inventory

For **each** Play-distributed package, complete as applicable:
- App name, category, short/full description, high-resolution icon, feature graphic, appropriate screenshots and localization.
- Contact email, developer legal identity, published privacy policy URL, account deletion web URL.
- Ads declaration; in-app purchases/subscription settings; countries/pricing; content rating questionnaire.
- Target audience and applicable Families policies; parent-versus-child audience must be accurately described.
- Data safety questionnaire (collected/shared categories, encryption in transit, optional/required, deletion).
- App access / reviewer test credentials, pairing workflow and any hardware requirements.
- Background location declaration and short demonstration video.
- Foreground service declarations, high-risk permissions, package visibility declarations or other forms that the Console displays.
- Monitoring `isMonitoringTool=child_monitoring` where appropriate, non-cloaked UI/notification and transparent listing.
- Release signing, AAB upload, Play App Signing, software supply chain/SBOM review.
- Internal testing, closed testing and a production review, staged rollout and policy appeal/response process.

For personal developer accounts created **after November 13, 2023**, the currently documented production-access gate includes a closed test with **at least 12 opted-in testers for 14 continuous days**. Verify whether your actual developer account is subject to this requirement; do not assume exemption or completion.

## 6. Data safety prerequisites

Data safety must be generated from **the final binary and every SDK, service and backend**, not from a marketing aspiration. Relevant categories may include:
- Precise/approximate location and location history.
- App activity / installed apps / interaction events.
- Device identifiers, diagnostics, crash data.
- Parent identity and email/authentication IDs.
- Photos, videos and audio **only if the final released feature collects/transfers them**.
- Purchase/subscription metadata (not card numbers if processed exclusively by Play).
- Sharing with providers/processors and the parent recipient; classify “sharing” according to Play's exact definitions, not assumptions.

Use the [Data safety worksheet](DATA_SAFETY_WORKSHEET.md) for line-item review.

## 7. Native and build compliance

- `compileSdk`, `targetSdk >= 36` for current new/updated phone apps, tested Gradle/AGP and NDK revisions.
- `minSdk` selected from support matrix (proposed 29, not finalized).
- Rebuild native `.so` libraries with 16 KB page compatibility; verify ELF load alignment, zip packaging and tests in a 16 KB emulator/device.
- Reproducible builds, deterministic version codes, signed AAB, Play App Signing; protect upload key.
- Review imported SDKs for Play SDK Index warnings, dependency vulnerability reports and unintended data collection.

## 8. Privacy policy, deletion and user support

Public URLs must exist and be accessible without logging in:
- Privacy policy: specific entity/company, app name, feature/data collection, recipients, retention, security, contact and rights.
- Account deletion: clear request path, authentication/verification where justified, associated-data deletion and disclosed legally necessary exceptions.
- Support: real email/contact and dispute/refund instructions.

Drafts are in [Privacy policy](PRIVACY_POLICY_DRAFT.md) and [Data safety worksheet](DATA_SAFETY_WORKSHEET.md). **They are not ready for publication** until operator identity, actual retention, hosting, SDKs and release behavior are confirmed.

## 9. Store-listing draft guardrails

Use accurate descriptions like “Parentally configured family location history and app usage reports.” Explicitly describe monitoring and limitations. Do not claim “invisible,” “undetectable,” “remote listening without any indication,” or “works on every Android phone.” Avoid claims of universal blocking.

Create screenshots only from a real release candidate. List supported device requirements and managed enrollment restrictions. Provide reviewers a working sandbox/demo account and paired test device flow.

## 10. Release go/no-go checklist

- [ ] Parent and child binaries actually exist and build as AABs.
- [ ] Every manifest permission has justification and tested corresponding feature.
- [ ] No forbidden covert capture or cloaking.
- [ ] Monitoring identification, notification and disclosure verified on child device.
- [ ] Target API 36+ and native 16 KB page-size compatibility confirmed.
- [ ] Data safety matches the app, SDKs, backend and released feature flags.
- [ ] Privacy and account deletion URLs are public and operative.
- [ ] Play Billing/subscriptions integrated and server-validated.
- [ ] Background-location demo video and declarations ready.
- [ ] Reviewer onboarding and app access instructions tested.
- [ ] Functional and device matrix tests passed.
- [ ] Security/privacy/retention review signed off.
- [ ] Required testing-track/production-access prerequisites fulfilled.
- [ ] Play Console review approved, with no unresolved policy notices.

## Official sources

- Target SDK: https://support.google.com/googleplay/android-developer/answer/11926878
- Monitoring apps: https://support.google.com/googleplay/android-developer/answer/9888380
- Monitoring flag: https://support.google.com/googleplay/android-developer/answer/12955211
- Background location: https://support.google.com/googleplay/android-developer/answer/9799150
- App review: https://support.google.com/googleplay/android-developer/answer/9859455
- Account deletion: https://support.google.com/googleplay/android-developer/answer/13327111
- 16 KB page sizes: https://developer.android.com/guide/practices/page-sizes
- Closed testing: https://support.google.com/googleplay/android-developer/answer/14151465


## Separate named Play packages

**Madalasa** is the parent/guardian app and **Alarka** is the identifiable child companion. Prepare separate package IDs, launcher strings, listings, review scripts and Data Safety declarations; verify package IDs only after publisher/domain selection. Subscription or Google authentication does not prove lawful custody.

## 2026-10-26 Critical new Play Families location restriction and child app gate

**Read [MA-COMPLIANCE-001](INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md) before submitting either package.** Official [Google Play Families Policy](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en) states **apps solely targeted to children cannot request location permission or collect/use/transmit precise location**. Alarka is a child-installed monitoring companion; the [Play monitoring-app exception](https://support.google.com/googleplay/android-developer/answer/9888380?hl=en) and [isMonitoringTool flag](https://support.google.com/googleplay/android-developer/answer/12955211?hl=en) **do not, by themselves, provide a verified exemption** from that Families restriction. Product owner must obtain an actual Play policy clarification on truthful target audience and permissible Alarka functionality **before committing the child GPS Play business model**. Do not misdeclare ages, conceal monitoring or sideload a noncompliant alternate APK. Even favorable Play treatment does not solve Indian DPDP child legal purpose; and Android permission grants do not bypass background restrictions. No real-minor pilot or child GPS submission until these gates pass.

## 2026-10-26 conditional media research is not Play approval

The owner wants to study conditionally executable microphone listening/recording, camera view/photos/video, flash-off captures, scoped files, and MediaProjection with per-session consent. The Alarka main Activity should remain closed after setup during routine valid operation; Alarka must still have a recognizable icon, persistent monitoring notification and Android camera/microphone indicators. Ordinary initial permissions do not universally permit new background sensor startup; genuine device-owner FGS exception remains to be tested. Never disguise capture, suppress indicators, or publish a bypass APK.

Parent Madalasa must explain an unavailable action with a **verified runtime reason**, not hide refusal or pretend success. Child/guardian authorization and notice, target audience/Families review, DATA SAFETY truthfulness, media-specific manifest/FGS declarations, effective Indian child-data permission and final Google Play clearance remain prerequisites. Do not ship CAMERA/RECORD_AUDIO runtime paths, list a media feature as available, or advertise "always available listening" until the separate gated review passes. Encrypted P2P/no VPS recordings does not eliminate personal-data processing. Research [MA-MEDIA-ADR-001](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md); T-MEDIA-01–18.
