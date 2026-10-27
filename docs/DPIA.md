# Data Protection Impact Assessment (DPIA) — Madalasa–Alarka

**MA-DPIA-001 | Reviewed 2026-10-27 | DRAFT / NOT APPROVED.** Assessor [UNASSIGNED], security lead [UNASSIGNED], India counsel [UNASSIGNED], Product owner signoff [PENDING], controller legal entity [UNDECIDED], OCI deployment region [NOT VERIFIED]. **NO REAL-MINOR DATA PILOT.**

## Legal and policy interpretation
India's DPDP Act 2023 and 2025 Rules have **phased commencement**. Gazette notices dated 13 Nov 2025 specify many substantive child-data provisions 18 months after publication, subject to amendments. DPIA-specific statutory assessment obligations attach to **notified Significant Data Fiduciaries** under Act section 10; voluntarily drafting this DPIA does not prove this startup has that designation. Child behavioral monitoring is restricted under Act section 9 with **narrow, conditional exceptions**; a hypothesized real-time safety tracking exception must not be extended automatically to historical GPS profiles, app usage analytics, or remote camera/microphone capture. Android OS grants do not substitute for verified guardian authority, proper legal processing or Google Play policy.

Official sources: https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf ; https://www.meity.gov.in/static/uploads/2024/02/Digital-Personal-Data-Protection-Act-2023.pdf ; https://www.cert-in.org.in/Directions70B.jsp.

## Proposed processing and deployment reality
| Activity | Data/source | Status |
|---|---|---|
| Guardian pairing and child-specific grants | Adult identity/child/device and permission receipt | M1 contract+SQL test only |
| Location/live safety | GPS, time, accuracy, speed, phone/watch source | DESIGN, release gated |
| Detailed history/trips/named places | GPS path, school/home inferences | RESTRICTED, separately release gated |
| App usage sessions | Package name/activity timestamps, duration | P3/behavior monitoring gate OFF |
| Capability and permission report | OS sensors/support/Android grant scopes | DESIGN; read-only scan before grants |
| SOS and command receipts | Guardian action, location/event receipt | DESIGN, no emergency delivery guarantee |
| Remote mic/camera/screen/AV | Live media transport and local optional recordings | RESEARCH ONLY OFF, no VPS media files |
| Media metadata history | Who/when/requested/viewed/saved, duration/filesize/failure | DESIGN, child-linked sensitive |
| Administrator support | Parent/child name+ID autocomplete and media/event audit | DESIGN; case/MFA read audit required |
| Local location queue | Up-to-48h encrypted device capacity target | DESIGN, not always-on guarantee |
| GPS durable PostgreSQL inbox | Temporary raw JSON GPS and WAL/backup | DESIGN, additional sensitive copy |
| Derived trip/usage | PostGIS location, outbox, aggregated sessions | DESIGN, worker not implemented |
| Vendor services | OCI/Google/Maps/FCM/Drive/Play Billing, optional TURN/SMS | Not finally contracted |

There is **no deployed Android application, C++ backend, app signing configuration, production database or restored offsite backup** verified in repo. Historical OCI Chicago plans conflict with possible India/Mumbai; no final region or processor contract confirmed.

## Data flows and trust
Alarka OS → encrypted local queue → authenticated child-bound HTTPS → Drogon Tx A durable PostgreSQL inbox **after commit HTTP 202** → C++ leased bulk worker Tx B raw location+dedup+outbox → separate trip worker → authorized Madalasa. 202 inbox queued is not live GPS/trip completion. UsageStats is separate, may be delayed, and needs independent processing authority. All live content feature flags OFF. Admin roles by default see aggregate metrics; named child access needs MFA, approved case/purpose and separately logged reads.

## Risk register (initial qualitative; residual untested)
| ID | Threat | Baseline risk | Safeguard before pilot |
|---|---|---|---|
| R1 | Abusive/unauthorized adult links or tracks a child's device | CRITICAL | verifiable guardian identity/authority, safe dispute/grievance, visible Alarka |
| R2 | Cross-family or same-family wrong-child location leak | CRITICAL | app child scope + Postgres forced RLS, negative tests |
| R3 | Child behavioral/app usage profiling unlawfully processed | CRITICAL | India legal review, purpose gating, feature OFF |
| R4 | GPS history exposes school/home routes | HIGH | time/precision minimization, separate history retention and scope |
| R5 | Alarka stolen/rooted exposes 48h local coordinates | HIGH | actually encrypted queue/KeyStore, battery/OS evidence |
| R6 | Temporary Postgres inbox/WAL/backups leak GPS | CRITICAL | DB least privilege, encryption, TTL, backup/legal/region checks |
| R7 | Deleted child revived by offline queue or restored backup | CRITICAL | revoke generations/tombstones before ingestion/read, restore drill |
| R8 | Administrator enumerates or exports named child histories | CRITICAL | exceptional MFA case, audit fail-closed, no global root data rights |
| R9 | OS capture performed without lawful child transparency | CRITICAL | media P3 OFF, Android indicators and per-session consent |
| R10 | False live GPS/usage/SOS status makes guardian rely on missing service | HIGH | last observed/ingested/reconstructed indicators, unavailable reasons |
| R11 | No 24×7 incident owner or India CERT-In logs | HIGH | contact, 6-hour reportability triage, India ICT-log store |
| R12 | Insecure Android signing, supply chain or vendor transfer | HIGH | audited signing, SBOM, signed vendors/contracts, Play review |
| R13 | Ambiguous raw GPS 14 vs 30 day retention | HIGH | sign unified retention schedule, erase and restore tests |
| R14 | Multiple devices/proxy watch location misidentify child | HIGH | provenance/source selection, uncertainty and gaps |

## Necessity and less intrusive alternatives
- Prefer event-driven SOS/guardian initiated child check-in over indefinite high-resolution tracking where feasible.
- If lawful safety current-location scope qualifies, preserve a narrow version; do not assume unrestricted path history or UsageStats.
- App usage: on-device-only summary or disabled until independent India/Play judgment.
- Media: do not implement covert remote sensing; OS user action and visible indicators remain.
- Parent map draws actual verified points; optional road matching must be labelled estimated, never reconstruct invented turns.
- Raw media is **not stored on VPS**, but media metadata and parent-local saved content remain relevant personal processing.
- Minimize persistent child GPS copies, choose direct bulk if equal resilience with less resource use after benchmark; current accepted default durable inbox+bulk requires explicit TTL.

## Required approvals & acceptance evidence
- [ ] Named legal publisher/controller; India counsel confirms actual statutory commencement, exemptions, privacy notice and Play Families/monitoring restrictions.
- [ ] Verified guardian consent/authority with child safety complaint process; under-18 and adulthood transition handling.
- [ ] Data retention including 14 vs 30 day raw GPS conflict; inbox, WAL, backup purge; data subjects rights and deletion.
- [ ] OCI region, vendor DPAs and Indian ICT security log storage decided; restore and incident-reporting drill.
- [ ] STRIDE and independent security review, Android device permission/OEM proof, signed APK/CI/SBOM, RLS/sibling negative tests.
- [ ] T-ING-01…24, T-CAP-01…24, T-AUD-01…22, T-ADM-01…14 performed with synthetic/adult fixtures and recorded.
- [ ] Product owner, security lead, legal officer, grievance lead sign a GO decision with date/version.

**Risk disposition:** real-minor pilot **NO-GO** and commercial Play release **NO-GO**. Assessment to be revised on new feature/vendor/law, and annually after full ownership assigned.
