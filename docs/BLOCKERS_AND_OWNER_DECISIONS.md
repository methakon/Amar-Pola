# Madalasa–Alarka — Blockers, Decisions and Resolution Register

> **Current product:** **Madalasa** (parent app) + **Alarka** (child app); the GitHub repository is now **[Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka)**. [English mythological inspiration](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

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

## G. Oracle Chicago hosting selection and finance decision — 2026-10-25

The owner has selected **Oracle OCI US Midwest Chicago (us-chicago-1)** as the design/home-region target, prioritizing Always Free allowances and later PAYG scaling. Detailed deployment/cost assumptions are documented in [OCI Chicago Deployment and Financial Plan](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md).

| Existing ID | Updated decision status | Remaining blockage |
|---|---|---|
| **B-08** | **PARTIALLY DECIDED:** cloud provider Oracle, planned region Chicago | OCI account creation, real A1 capacity, US child-data hosting legality, hosting budget, backups |
| **B-21** | Cost model added for 100–10,000 children with one subscription per child | Expected actual enrollment, maximum monthly spend, staff/support/HA budget |
| **B-14** | Per-child subscription billing unit established by owner | Actual monthly price, Play fees/taxes/trial/refund policy; ₹149 is example only |
| **E-08** | Chicago hardware/load topology designed | Actual CPU/DB/queue synthetic load evidence absent |
| **X-03** | US database region made explicit | Jurisdiction, minor privacy, cross-border transfer/legal consent assessment |
| **X-08** | OCI resource selected on paper | Live VM and capacity not verified; OS/OEM test fleet still needed |

**Do not mark B-08 fully closed:** Oracle home-region selection is materially difficult to change after tenancy creation, capacity is not publicly guaranteed, and OCI requires an authorized account holder to create resources. No tenancy, instance, domain or payment method was accessed or changed by this documentation step.

**Subscription pricing direction changed on 2026-10-26:** Proposed ₹50/month or ₹500/year per child, **not** ₹149/month. See [Subscription Plans and Fees](SUBSCRIPTION_PLANS_PRICING_AND_RULES_2026.md) for SUB-01–SUB-16 approvals and unresolved tax/Play/family-seat checkout constraints. This specifically updates product direction for B-14; **pricing is not yet activated in Play Console**.

## H. Cumulative OCI paid-hosting cost decisions (2026-10-26)

The [deployment financial document §14](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md#14-cumulative-recurring-hosting-cost-beyond-free-tier--monthly-annual-and-scaling-sensitivity) now includes **priced monthly and annual hosting totals**, explicit boot/block and Object Storage usage, a separate 20% uncertainty allowance, a discretionary hosting budget and 7 hypothetical workload/VM shapes. These **do not certify child capacity** or a managed/HA production architecture.

| ID | Owner action needed | Why it matters |
|---|---|---|
| **COST-01** | Verify Oracle PAYG 3,000 OCPU-hour / 18,000 GB-hour monthly allowance in actual Chicago tenancy | Determines whether ~4 OCPU/24 GB incurs compute charge |
| **COST-02** | Confirm successful A1 shape allocation, storage free quota and account billing mode | Published list prices do not mean your VM exists |
| **COST-03** | Decide acceptable maximum paid hosting **budget per month** and annual cash ceiling | Planning contingency is not a payable line item |
| **COST-04** | Select raw GPS/derived trip/audit retention | Determines DB, Object backups and restore cost |
| **COST-05** | Decide whether single-node low-cost pilot is acceptable or paid HA/SLA required | Full HA/managed DB and on-call are **unpriced** |
| **COST-06** | Verify cost in OCI Cost Estimator / actual invoices, tax and invoice currency | INR list price is an estimate, not a bill |
| **COST-07** | Validate load/backup capacity before linking number of children to VM | Child counts are scenario labels only |

This supplements B-07, B-08, B-12, B-14 and B-21; do not mark them closed until choices and evidence exist.

## I. 2026-10-26 critical India/M2/pilot decisions and evidence blockers

**Status rule:** Proposed defaults are NOT your answers. No real child data collection until India DPDP/legal and US hosting review. Current confirmed direction: India-first pricing and Chicago target; legal identity, country/age policy and specific purposes still unsigned.

| Prior ID / new gate | Exact decision or evidence requested **now** | Provisional architectural default | May proceed without answer? |
|---|---|---|---|
| **B-01 / LG-01** | Publisher legal name, entity type, registration/jurisdiction and public support/privacy contact | Anonymous placeholder; synthetic data | **No real child data** |
| **B-02 / LG-02** | Sign off India-only first launch, exact child ages within under-18 group, guardian authority and languages | India-only *proposal*, under-18 legal review; no global launch | **No real child data** |
| **B-07 / LG-05** | Approve raw GPS, history, usage, SOS, audit, auth, backups and deletion retention after lawyer review | Raw 14 days; history 90 days **DISABLED** pending purpose review; app usage **OFF**; backups candidate 30d; audit 365d legal candidate | Synthetic design only |
| **B-09/B-18 / LG-07** | Who may invite, approve, revoke and view each child, including disputes and pickup scope? | Verified family owner **only** can invite/revoke; per-child grants; history opt-in, pickup current only 45m candidate, no role inheritance | SQL can use defaults; cannot enable real access before approval |
| **OCI-06 / AUTH-01** | Parent login provider, India onboarding age/identity provider and account recovery | **Google Sign-In through Android Credential Manager and backend ID-token verification** as M1 *engineering candidate*, not adult/parent identity proof; no SMS initially | Synthetic pairing allowed |
| **TEAM-04 / HW-01** | Real device inventory: model, Android API/OEM, parent test phone, older phone, and one **owner-approved factory-resettable spare** | Emulator/synthetic only, standard mode first; managed-DPC proof blocked | **M1 physical acceptance cannot pass** |
| **B-21 / TEAM-01–07** | Named engineer(s), independent QA/security/legal, OCI operator, monthly cash budget and funded runway | No staffing or operating capacity presumed | No credible paid pilot estimate |
| **FR-044 / SOS-B01–07** | Decide best-effort check-in vs public emergency SOS; trusted contacts, fallback SMS/vendor/cost, independent dispatch failure path | Best-effort check-in **only**; public emergency SOS OFF | M2 prototype only |
| **OCI-12 / DR-B01–07** | Approve pilot/production RPO/RTO and paid standby, backup/restore drills, support rota | Dev synthetic 24h RPO/48h RTO **targets only**; no production claims | **No real pilot without proof** |
| **SUB-16 / TEAM-06** | Verify ₹50/₹500 final tax-inclusive checkout, Play fee, refunds, churn, support and staff break-even | Prices PROPOSED; ₹149 historic model | Pricing design only |

**Related actionable designs:** [India child privacy law](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md), [SOS fallback](SOS_ESCALATION_AND_INDEPENDENT_DELIVERY_DESIGN.md), [OCI recovery](OCI_CHICAGO_RECOVERY_AND_PILOT_READINESS.md), [Price break-even/staffing](PRICE_BREAK_EVEN_STAFFING_AND_DELIVERY_CAPACITY.md).

**Answer format (any subset):** B-01 legal publisher identity; B-02 country and ages; B-07 proposed retention approved/edited; B-09/B-18 scope policy; OCI-06 login approved/changed; HW-01 devices safe for reset; B-21 team and monthly budget; SOS-B01 emergency vs check-in; DR-B01 pilot RPO/RTO and funding. Keep identity documents, passwords, child data, contact numbers and cloud keys OUT of public GitHub.

## J. Indian OCI preference and single M0–M9 / M1 validation execution (2026-10-26)

The owner has chosen **India-region preference** to avoid unnecessary primary OCI US location. **Preferred Mumbai ap-mumbai-1, alternative Hyderabad ap-hyderabad-1**; tenancy/home-region availability and price still require confirmation. **B-08 direction updated, not closed.** Chicago plan remains historical. See [India OCI region decision](INDIA_REGION_AND_M0_OWNER_DECISION_GATE.md).
Canonical milestones now [M0–M9](MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md). M1-only [OpenAPI](openapi-m1.yaml), [RLS migration](../backend/persistence/migrations/0001_m1_identity.sql), [two-family negative test](../backend/tests/m1_tenant_isolation.sql), [14 M1 test cases](../backend/tests/M1_ACCEPTANCE_TEST_CASES.md) and [CI workflow](../.github/workflows/m1-contract-and-tenant.yml) are committed. API structural validation is green; PostgreSQL actual execution, Kotlin/C++ code, hardware and Play/legal gates **are not** proven.

Owner answers still needed: legal publisher B-01; exact Indian children ages and guardian proof B-02; raw/location/history/audit/backup retention B-07; who can invite/revoke guardians and scope B-09/B-18; final login vendor/adult-verification plan OCI-06; actual test-device inventory/resettable handset HW-01; team size and monthly budget B-21. No secrets, identity scans or real child records in public GitHub.

## K. New government/Google Play release gate — 2026-10-26

See [MA-COMPLIANCE-001 Government/Legal/Play Risk Assessment](INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md).

| ID | Status | Owner decision / evidence |
|---|---|---|
| **G01 / R01** | **CRITICAL OPEN** | Verify Alarka exact Google Play audience and get product-specific Google Play interpretation of Families ban on precise location collection by solely child-targeted apps vs parental monitoring policy. Never falsely label age. **No child GPS release** before this. |
| **G02 / R02** | **CRITICAL OPEN** | Qualified India counsel confirms commercial real-time safety location Rule Part B item 4 scope separately from history, usage, behavioral inference, custody/parent verification. |
| **G03 / R12/R17** | **HIGH OPEN** | Decide data category retention plus CERT-In 6h incident reporting/180d India logs and prospective DPDP year logs/breach notice. |
| **G04 / R05/R19** | **HIGH OPEN** | Two accurate Play App Content/target audience/manifest/monitoring disclosure, privacy and Data Safety submissions with final package evidence. |
| **G05 / R22** | **HIGH OPEN** | Build/API 36, 16KB native ABI, Android permissions and device-owner physical acceptance, no fake success. |

These **add to**, and do not close, B-01 legal publisher, B-02 exact launch ages, B-07 retention, B-09/B-18 guardian grants, OCI-06 verifiable identity, HW-01 resettable phones, B-21 staffing/budget, SOS and disaster recovery blockers.

## B-16 clarification — owner accepted media R&D and reason-specific parent UX (2026-10-26)

**Owner decision:** CONDITIONAL media research is **accepted** for one-way live audio, optional authorized recording, remote live camera, front/rear photo snapshots, flash-off where possible, authorized video, per-session-consented screen view and permitted MediaStore/SAF files. Do not interpret "defer media" in B-16 as owner rejection of proof-of-concept work. **B-16 commercial release / Play inclusion remains OPEN and default OFF.** Standard installation and actual device-owner DPC mode must be tested separately. Alarka main Activity is normally closed after setup, but monitoring notification and OS sensor indicator remain visible.

**Product requirement:** Madalasa reports verified `Command.status + reason_code` and safe next action when a media/file request is unavailable, specifically Android background start blocked, permission revoked, user notification/system consent required, true managed enrollment required, unavailable hardware, phone offline, expired request, or network trouble. Unknown/offline must never be misdiagnosed as missing permission. Android MediaProjection must obtain system approval for each session.

**Still open:** legal publisher/guardian authority, India child-data purpose and Play/Families classification, managed-device real proof, physical OS/OEM test fleet, active session consent/retention, device encryption/key management, optional parent-local recordings, India OCI region relay bills/concurrency and funded security audits. [MA-MEDIA-ADR-001](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md).

## I. 2026-10-27 permission onboarding design accepted; implementation/release blockers still open

**Owner DECIDED design:** First-launch Alarka reads public hardware/OS compatibility; after trusted pairing it uploads a versioned device-authenticated report to backend, then offers a stepped Android OS grant wizard with clear "why", in-app post-grant verification, server durable ACK and Madalasa child-scoped feature list with positive permission confirmations. Later Android Settings revocation/reapproval is rechecked on next eligible app execution and sent with new revision. Distinguish user-facing **permission-granted green** from actual **operational-ready green**; no false live-media claim, and offline/stale cannot be diagnosed as permission revoked.

**Engineering blockers OPEN:** device scan allowlist/metadata minimization, manifest and target-SDK review, Android API29–36/OEM behavior (one-time permission, OS process kill, Usage Access, selected photos, scoped SAF, separate background location), genuinely managed-owner proof, Keystore device/replay, backend transaction/version model, parent VIEW_DEVICE_STATUS access, event/FCM drop resilience, complete T-CAP-01…24 evidence. **External blockers OPEN:** legal guardian verification, publisher/country/ages, India child-data purpose/legal counsel, Play background-location/Families/monitoring eligibility. M1 API stays narrow until separately approved contract migration. Owner decision does not unblock protected child processing. [MA-CAP-ADR-002](CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md).
