# Amar-Pola — Blockers, Decisions and Resolution Register

**Date:** 2026-10-25 | **Version:** 1.0 | **State:** OPEN | **Purpose:** actionable project-owner decisions and independently verifiable engineering/release gates.

Each blocker has an owner, decision or required evidence, and lifecycle: OPEN → DECIDED → IMPLEMENTED → VERIFIED → CLOSED. **Selecting a product option does not resolve software testing or Google Play review.**

## A. Decisions you can make now

| ID | Severity | Your question / choice | Conservative default until answered | What you can provide | Blocks |
|---|---|---|---|---|---|
| **B-01** | Critical | What legal person/company publishes the app? | Documentation drafts only; no public legal claims | Company/legal name, support email, business contact | Privacy/Play |
| **B-02** | Critical | Launch countries and child age range? | Internal testing only | Countries, ages, applicable parent authority expectations | Child privacy/legal |
| **B-03** | Critical | Confirm identifiable monitoring app, visible icon and required persistent notification? | Yes; **no stealth option** | Explicit acceptance | Play/Android UX |
| **B-04** | High | Exact first-release feature list? | Pairing, location, trip/stop/map, named places, usage, trust diagnostics and privacy; other modules staged | Core vs paid vs later list | Delivery budget |
| **B-05** | High | Normal consumer phones, managed-device edition, or both? | Standard installation first; optional separate managed edition | Whether device-owner provisioning/reset is acceptable | Device blocking and distribution |
| **B-06** | High | Is optional child SOS/check-in/widget UI acceptable while main tracking Activity stays closed? | No continuously open Activity; optional action UI | Child interaction preferences | SOS and child UX |
| **B-07** | High | Retention for raw GPS, trips, usage, audit and backups? | Planning candidates: raw 14d, derived 90d, usage 90d, audit 90d; **not approved** | Actual retention per category | Privacy/schema/cost |
| **B-08** | High | Server provider and hosting/data-residency region? | No production deployment before selection | Hosting region/provider, budget | Deployment/processors |
| **B-09** | High | Who may add/revoke guardians, and how long can pickup access last? | Family owner approves per-child; temporary 45min current-location only | Roles, scopes, TTL | ACL/security |
| **B-10** | High | Launch Android versions/manufacturers? | API29+ candidate; begin Pixel + Samsung testing | Phone models/versions you can test | Device certification |
| **B-11** | High | Standalone Wear OS watch at launch? | Phone-first; Wear beta after power tests | Watch brands and GPS/LTE capability | Wear architecture |
| **B-12** | High | Battery preservation vs detailed 5–15s route capture? | Balanced default; bounded user-authorized detail mode | Accuracy/freshness preference and context | Location tuning |
| **B-13** | Medium | What counts as a stop or confirmed school arrival? | Initial candidate 3–5min walking / 5–10min vehicle with multiple trustworthy fixes | Desired rule after field tests | Trip/commute semantics |
| **B-14** | High | Free/premium tiers, device count, trials and regions? | No pricing promises; use server-validated Play billing | Plans and entitlements | Billing/store |
| **B-15** | Medium | Does Google Drive backup ship in v1? What media and deletion behavior? | P2, opt-in only | Media type and retention/ownership | OAuth/data safety |
| **B-16** | High | Camera/video/microphone in Play launch or deferred? | **Defer**; only openly authorized, compliant research | Defer entirely or separately fund feasibility tests | Sensitive permissions |
| **B-17** | Medium | Which alerts are high-priority vs quiet hours? | SOS priority; ordinary alerts deduped | Desired critical/noncritical alert list | Notification logic |
| **B-18** | High | Does a guardian see full history, current only, or child-specific subset? | Explicit least privilege, owner configurable | Role/access policy | ACL and sharing |
| **B-19** | Medium | Parent Android app only or web too? | Android first, versioned API supports future web | Client platform choices | Frontend architecture |
| **B-20** | High | Approve observed vs inferred route transparency? | Show actual fixes and gaps, no invented streets | Confirm invariant | Geo algorithms |
| **B-21** | Medium | Expected families/devices, monthly infrastructure budget and team size? | Capacity test 1k/10k/100k synthetic; no SLA claim | Budget/scale and staffing | Sizing |
| **B-22** | Medium | Launch language(s), support contact, staff coverage? | English test version; no public support claim before staffing | Languages and real support channel | Localization/Play |

**You may answer incrementally:** for example, “B-05 standard first; B-07 GPS 14 days, trips 90 days; B-11 Wear later; B-16 media deferred.” Open entries remain pending; suggested defaults are design assumptions, not approval on your behalf.

## B. Engineering blockers — resolved by building and testing, not by guessing

| ID | Priority | Work and reason it blocks completion | Evidence required | Responsible role |
|---|---|---|---|---|
| **E-01** | Critical | Family/child/guardian grants, server authorization + RLS | Cross-family API, worker, cache and live-stream negative tests | Backend/security |
| **E-02** | Critical | Complete versioned OpenAPI and real handlers | Contract lint, schema-negative and role tests | Backend |
| **E-03** | Critical | Durable GPS idempotence, partition dedup, per-device worker fences | Crash/duplicate/offline/late replay passes | C++/DB |
| **E-04** | Critical | Revocation and deletion spanning raw/derived data, backups and offline devices | Restore and no-reingest proofs | Backend/privacy |
| **E-05** | High | Android permission, typed FGS, foreground/background and OEM life cycle | Device API/OEM instrumentation evidence | Android |
| **E-06** | High | Stop/arrival/route quality thresholds and confidence | Labeled journey precision and recall tests | Geo/QA |
| **E-07** | High | Real battery and sampling behavior (phone, tablet, watch) | Comparative controlled-device measurements | Mobile QA |
| **E-08** | High | Drogon/Postgres scaling, backup recovery and failure handling | 1k/10k/100k synthetic tests plus recovery exercise | SRE |
| **E-09** | Critical | Parent OIDC, per-device secure keys, secret/key rotation | Security review/rotation and auth tests | Security |
| **E-10** | High | Actual parent/child AAB, API 36 standard Play target and native 16KB support | Signed builds + device installation checks | Android release |
| **E-11** | High | SOS/command receipts, expiration, fallback and priority | Offline, replay, revoked guardian tests | Backend/QA |
| **E-12** | Medium | Parent map paging, named-place optimistic edits, uncertain state UX | Multi-guardian and stale-state UI tests | Parent UI |
| **E-13** | Medium | Play Billing and optional Drive/provider integrations | Sandbox payment and OAuth revocation results | Integrations |
| **E-14** | High | End-to-end FR-to-test traceability and CI evidence | All release-scope requirements traceable to passing tests | QA/architect |

## C. External blockers and third-party approvals

| ID | Blocker | What must happen | Who can unblock |
|---|---|---|---|
| **X-01** | Play publisher identity and package ownership | Verify developer account, company identity and signing setup | You / Play |
| **X-02** | Sensitive background-location/monitoring policy | Real app disclosure, persistent notification, video, permission declarations, reviewer access and approval | Release / Play |
| **X-03** | Country-specific child privacy/guardianship | Independent legal review of launch territories, age and authority | Legal counsel |
| **X-04** | Public privacy and account deletion URLs | Functioning pages matching real data operations | Product/backend |
| **X-05** | Optional Google Roads asset-tracking terms | Written provider license/caching/attribution review | Legal/Maps provider |
| **X-06** | Cloud/SDK subprocessors | Region choices and processor contract/data safety evaluation | Operations/legal |
| **X-07** | Play testing gate | Determine whether your developer account requires closed testing and complete it | You / release |
| **X-08** | Physical Android/OEM/watch devices | Obtain test fleet or representative access | You / QA |

## D. Documentation versus implementation states

This documentation refresh can remediate **design gaps** AG-001/002/003/006/007/008/009/012/013/017/020/025 in writing, but cannot mark their implementation or verification complete. Every E- item stays open until tested; X- items need appropriate outside evidence. Do not equate a document with an APK, an app test, a legal review or Play permission approval.

## E. Recommended next actions for you

1. Most blocking decisions: **B-01, B-02, B-03, B-05, B-07, B-08, B-10, B-11, B-12, B-14, B-16**.
2. Approve role sharing **B-09 and B-18** before multi-guardian data tables are implemented.
3. Identify available real phones/watches, developer account status and desired launch region; the design can proceed using synthetic data while answers are pending.
4. Keep **remote hidden capture, protected private-file access, and Android security bypass** excluded.

Related: [Feasibility](WHOLE_PROJECT_FEASIBILITY_GATE_2026.md) · [Audit](TECHNICAL_DOCUMENT_AUDIT_GAPS_2026.md) · [SRS](SRS.md).

## F. Newly confirmed architecture constraints — 2026-10-25

The project owner has supplied these additional instructions. They update the **design direction** but do not certify platform capabilities or legal compliance:

| Blocker | New information | Decision status | What remains open |
|---|---|---|---|
| **B-05** | Managed-device provisioning is available | **DIRECTION DECIDED:** plan optional fully managed child DPC path in addition to STANDARD app | Exact enrollment approach, factory reset acceptance and physical proof of device-owner authority |
| **B-10** | A mix of older and newer Android versions must be supported | **PARTIALLY DECIDED:** implement API-aware Android compatibility path, proposed minSdk 29 | Exact supported Android versions/OEM models, test fleet and capability pass evidence |
| **B-19** | Parent interface is a **native Android app** | **DECIDED:** Kotlin/Jetpack Compose native client, no web parent client in M1 | None for architecture choice; production UI remains to be coded |
| **B-03** | Transparent, permission-based monitoring is prioritized | **DIRECTION DECIDED:** identifiable child app and system monitoring notification are nonnegotiable | Exact localized disclosure, jurisdiction/consent and Play Console approval |

The implementation plan and acceptance tests are now specified in [M1 Android/C++ Architecture and Implementation](M1_ANDROID_CPP_ARCHITECTURE_AND_IMPLEMENTATION.md). This is a design status update only. Device-owner provisioning and supported Android behavior remain engineering verification tasks.
