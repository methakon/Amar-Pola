# Madalasa–Alarka — India DPDP Child Privacy, Consent and Chicago Cross-Border Legal Gate

> **Document control:** M0 / 03-legal-and-privacy · Proposed owner: Privacy counsel + owner (not assigned) · Registry: DRAFT_LEGAL_REVIEW_REQUIRED; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

> **Current app names:** **Madalasa** (guardian/parent), **Alarka** (child companion). GitHub repository [Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka), renamed 2026-10-26. [Source story and naming contract](../02-market-and-feasibility/BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Status:** ENGINEERING/LEGAL ISSUE BRIEF — NOT LEGAL ADVICE OR APPROVAL  
**Reviewed:** 2026-10-26 | **Applies to:** India-first launch, children under 18, parent/guardian app, Oracle OCI Chicago (US)  
**Release decision:** **NO real child's location, usage events, guardian identity evidence or other real child personal data may be ingested into development or production infrastructure until owner identity, lawful processing scope, parental authority, deployment jurisdiction, provider and counsel signoffs are recorded.** Synthetic GPS fixtures only until then.

## 1. Official legal instruments and exact time status

- Digital Personal Data Protection Act, 2023, section 9: special processing of children's personal data, verifiable parental consent before processing, restriction on tracking/behavioural monitoring and targeted advertising, subject to narrow regulations and exemptions; child means person under 18 per Act definitions.
- November **13, 2025** Gazette G.S.R. **843(E)**: sections 3–5, 6(1–8,10), **7–10**, **11–17**, among others commence **18 months after Gazette publication**. That computes to **approximately 13 May 2027** using the printed Gazette date, but a counsel must confirm official date/corrigenda and changes. Other provisions commenced immediately or after 1 year, so don't describe the entire Act as uniformly unenforced now.
- November **13, 2025** Gazette G.S.R. **846(E)**, rule 1: rules 3, 5–16, 22 and 23 (including **rules 10/12**) commence 18 months after Gazette publication; initial and other rule blocks follow different phases. Source government publication/web portals sometimes label the gazette 14 November; resolve any one-day official effective-date issue before launch.
- Rule **10**: where applicable, adult parent verification and verifiable consent are more than checking an app permission or relying solely on a child's assertion.
- Rule **12** / Fourth Schedule, Part B item 4: purpose-specific exception from **section 9(1) and (3)** for determination of a child's **real-time location** restricted to such tracking in the interest of the child's **safety and protection or security**. It does not dispense with all data obligations, nor is it proof that any commercial parent monitoring service qualifies.
- Section **16**, read with rule **15** and other Indian/sectoral laws: India-to-US processing requires a separate transfer assessment, current restrictions check, contracts, notices, data subject rights, retention, security and US recipient/processors review. Do **not** assert Chicago is illegal per se or automatically permitted.
- Other Indian laws, Play monitoring policy, Android permission constraints and rules for guardianship remain independent controls even prior to DPDP child-rule commencement.

**Authoritative primary documents:**  
G.S.R. 843(E): https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf  
G.S.R. 846(E): https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf  
MeitY Act/Rules library: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025

## 2. Do not apply the real-time-safety exception indiscriminately

| Data product / feature | Candidate DPDP interpretation issue | Safe implementation default until written counsel advice |
|---|---|---|
| Parent-requested **current device location** solely for immediate child safety | May be within limited Rule 12 Fourth Schedule Part B purpose; qualification of consumer service requires review | **Disabled for real minors** pending verified authority and lawyer approval; use synthetic data |
| Continuous periodic location collection for later analysis | Not identical to real-time determination; necessity/proportionality, surveillance and retention issues | **OFF** for minors until separate purpose-by-purpose review |
| Stored raw GPS 14–30 days, reconstructed trip and school stop history for 90 days | Historical reconstruction and profiling may fall outside real-time exception | **OFF** for real minors pending lawful basis and proportionate retention approval |
| App-usage history, per-app time, app-blocking schedules and screen-time profiling | Potential **behavioural monitoring**; not safely covered by real-time location exception | **DISABLED** for minors pending dedicated Indian legal opinion; no broad category collection in pilot |
| Geofences, route corridor deviations and prediction | Depends on feature purpose, inference/profiling, false alarms and children tracking rules | **OFF** for pilot unless specifically approved |
| SOS initiated by child / emergency check-in | Emergency safety purpose; guardian receipts and history are still personal data | Prototype only with synthetic/test adults or counsel-approved guardian participants, explicit disclosures and fallback |
| Identifiable child account, enrolled device and parent authorization records | Account creation and access evidence may contain child data | Require separately approved minimal fields and parental authority validation |
| Pickup guardian invitations, access history and location exports | Disclosure to additional adult is not automatically lawful | Owner authority, recipient verification, scope, expiry, revocation and access trail; no links without authorization |
| Google Maps, Drive, FCM, SMS vendors, analytics | Independent disclosure to processors, subcontractor purpose & cross-border risk | Data minimization, provider review and no raw child GPS/SOS text in generic logs/push |

**A technical consent checkbox or Android permission is not equivalent to DPDP verifiable parental consent.** Conversely, the existence of a purpose-specific statutory exception does not justify secret background data capture, indefinite storage, or exposing child GPS to all relatives.

## 3. Verifiable parent/legal guardian design that counsel must approve

1. Guardian starts from identifiable Android application with clear age and monitoring disclosure in supported Indian languages. Require parent account login, initial verification and documented authority to supervise each child/device.
2. Before real child data collection: display purpose-specific notices for live location, history, app usage, share/temporary pickup access, SOS, optional wear/watch and third-party processors. Default **OFF** where no reviewed lawful basis/exemption exists.
3. If relying on verifiable consent, choose a legally reviewed adult verification/identity-age proof approach: e.g. approved identity attributes or regulated virtual token. Minimize identity document storage and third-party transfer. A Gmail sign-in proves an account, **not automatically adult/guardian authority**.
4. Maintain versioned consent/authority receipt (guardian subject, child alias/reference, verified adult method/reference, relationship evidence/attestation, purpose, document/version, timestamp, status, revocation); encrypt and scope access. No raw government ID scans by default.
5. Show currently authorized adults and each purpose to the child in age-appropriate terms, preserve visible OS monitoring notification and user-friendly revocation/grievance mechanisms.
6. Child/guardian disputes, custody changes and alleged misuse: **freeze new sharing and potentially collection**, require documented escalation and identity reassessment; do not automatically accept a payment-holder as lawful custodian.
7. Parent withdrawal stops further relevant collection and sharing promptly; records/backup erasure follows approved policy while preservation requirements are independently assessed.
8. Test with fake identity and synthetic child data: forged/replayed consent, expired relationship, child transfer, 2 guardians in conflict, revoked parent and erased profile.

## 4. Required India + US Chicago privacy assessment before production/pilot

Legal counsel must produce a **dated, signed memorandum** addressing:
- Data Fiduciary/controller and processor identity: legal entity, registered/operations location, India point of contact, grievance mechanism; guardian identity and age policy; whether Indian legal obligations apply prior to/full May 2027 rollout.
- Written construction of section 9(1–4), Rules 10 and 12, Fourth Schedule Part B real-time location purpose. **Does a consumer parent tracking app qualify?** If yes, exact necessary fields/time window and residual section 9(2) and general obligations.
- Separate lawful-purpose table for **historical routes/trips**, stop/school arrival, app usage/behavioural monitoring, managed DPC controls, predictive alerts, geofences, SOS, watch, access logs; green/yellow/red feature scope.
- Consent, adult age verification, custodial authority, conflict and withdrawals; accessibility and other applicable child-protection law.
- Section 16/Rule 15 cross-border transfer, **US Midwest Chicago** OCI, Google processors, backups, support access, potential government notifications, any sector-specific restrictions, incident response and subprocessor agreements.
- Review of data security safeguards, breach reporting, retention/deletion including backup/log requirements, data minimization and identity verification data.
- Privacy notice, Terms, Data Safety, Play monitoring declaration, exact child-facing transparency and audit; counsel signoff/review cadence as notifications evolve.

**Decision output:** LEGAL_APPROVED_CORE_PURPOSES only for enumerated, signed feature scopes; LEGAL_BLOCKED others. No implied blanket authorization. Store signoff reference/review date and counsel contact in **private** governance repository, not public child PII.

## 5. Data retention decision gate (B-07)

**Unapproved architectural trial candidates, NEVER a live processing promise:**

| Category | Engineering *candidate* retention | Pending legal/product decision |
|---|---|---|
| Raw GPS fix events | **14 days** | Does history qualify? Can collection start? Necessity and supported storage region |
| Derived trip/stop history | **90 days** | Explicit separate purpose, retention necessity; otherwise **disabled** |
| Child app usage raw/aggregate | **OFF** in India minor pilot | Require independent lawful basis; if approved candidate no more than **30 days** initially, final period signed |
| Device heartbeat and non-location diagnostics | 7–30 days candidates | Remove unique child identifiers when possible |
| Significant audit/security/parent authorization receipts | **365 days compliance-planning candidate** | Specific statutory retention obligations, start/end dates and exceptions require counsel |
| Backups of permissible data | Daily encrypted, **max 30-day rolling candidate** | Restore tombstone, paid provider restrictions, legal necessity and test evidence |
| Parent age/authority evidence | Minimal verifiable reference only | Avoid raw ID; decide valid lawful minimum and deletion exceptions |
| SOS delivery metadata | **30-day candidate**, redacted | Distinguish incident record from retained GPS and emergency evidence |
| Unapproved usage / Roads / media | **0** | No data captured until independently approved |

Retention does **not** start automatically merely because a number appears in a database spec. Confirm all subprocessor copies, cache, export, device offline queue, replication, log and backup expiry. In particular, OCI financial modelling's **30-day raw GPS** is **a cost-only assumption**, not an approved retention policy.

## 6. Binding engineering stop conditions

- **LG-01:** B-01 legal publisher identity verified → otherwise **BLOCK REAL CHILD DATA**.
- **LG-02:** B-02 India initial launch + defined under-18 ages/custodial relationship formally approved → otherwise **BLOCK**.
- **LG-03:** India lawyer legal memo for all planned data purposes (live location, history, app usage separately) → otherwise **BLOCK**.
- **LG-04:** Chicago US transfer counsel review + list of all data processors, agreements and current applicable Government restrictions → otherwise **BLOCK**.
- **LG-05:** B-07 retention/backup and delete/restore tests → otherwise **BLOCK**.
- **LG-06:** Parental verification + notice + consent/exception by purpose in code (backend denies missing authority) → otherwise **BLOCK**.
- **LG-07:** Child-specific guardian scope and role management approved; identity/relationship disputes and revocation tested → otherwise **BLOCK**.
- **LG-08:** Google Play and independent Android monitoring disclosures + all real provider policies completed → otherwise **BLOCK PUBLIC RELEASE**.

**M0 may use synthetic traces. M1 enrollment may be tested only with fabricated participants or legally reviewed adult volunteers. M2/pilot involving real minors remains blocked until LG-01 through LG-07 pass.** Even after all those gates, Play release needs LG-08, working privacy/deletion pages and platform tests.

## 7. Relation to other docs / ownership

- [Owner Decisions and Blockers](../01-project-governance/BLOCKERS_AND_OWNER_DECISIONS.md) B-01/B-02/B-07/B-09/B-18, X-03; legal reviewer accountable.
- [Data/Authorization/Recovery](../../M1-secure-platform-foundation/03-security-and-permissions/DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md) implements scoped grants, erasure and source audit once approved.
- [Privacy Policy Draft](../../M9-play-release/02-public-legal-drafts/PRIVACY_POLICY_DRAFT.md) is not a published lawful notice.
- [India-first Subscription](../../M7-commercial-integrations/01-commercial-plans-and-costing/SUBSCRIPTION_PLANS_PRICING_AND_RULES_2026.md) cannot justify extra monitoring merely because purchased.
- [OCI Deployment](../../M8-operational-readiness/01-cloud-infrastructure/OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md) region decision is conditional, not legal clearance.

**Research caveat:** This memo summarizes primary legislative instruments verified on 2026-10-26. It does not offer legal advice; lawyer review must also check any changes after that date and other sectoral, consumer, employment and cross-border obligations.

## 8. India-primary region option supersedes original Chicago preference

The user has selected **India OCI location as preferred** for new infrastructure: Mumbai (ap-mumbai-1), Hyderabad fallback, subject to tenancy home-region/availability/pricing. The original Chicago-specific analysis is retained as a contingency in case of US processing or third-party transfer, **not** the current recommended deployment. Domestic OCI hosting may simplify the primary storage transfer question, but Google/Firebase/identity processors, support, backup replication and any cross-border handling still need mapping. Section 9, Rule 10/12 under-18 consent/behavioral-monitoring questions and exact ages/lawful guardian proof remain open. [India region decision](INDIA_REGION_AND_M0_OWNER_DECISION_GATE.md).

## 2026-10-26 Cross-policy assessment addendum

The [MA-COMPLIANCE-001 official-source assessment](INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md) adds: **(1)** Google Play Families restriction on location collection by apps solely targeted to children and unresolved compatibility with the parental-monitoring-app exception; **(2)** CERT-In incident reporting six-hour and ICT-log 180-day India obligations for covered entities; **(3)** future DPDP Rule 6/8 processing/log retention reconciliation; **(4)** Android API36 and background while-in-use policy. **Narrow DPDP real-time location allowance does not override Google Play or Android security rules.**

## 2026-10-27 children’s media-activity metadata and administrator-search gate

A design with **zero VPS audio/video/photo files** can still process child-linked metadata (who viewed or saved media, when, for how long, child/parent IDs, failed reasons, local file-size receipt and administrator access to activity). Treat this as a distinct sensitive processing purpose requiring India DPDP children's requirements/exemptions analysis, documented guardian authority and data minimization. Administrator access is not inherently justified by infrastructure ownership: require MFA, case-based purpose and child/parent scope, accountable searches, audited denied attempts and redacted aggregate support by default. Set explicit retention, deletion, access rights and cross-border backup/processor handling with counsel before deploying. No change to original M0 legal NO-GO or camera/mic P3 release status. See [Media Activity Audit ADR](../../P3-deferred-research/01-media-and-administrator-research/MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md) and [Administrator Console Specification](../../P3-deferred-research/01-media-and-administrator-research/ADMIN_PANEL_SPECIFICATION_2026.md).
