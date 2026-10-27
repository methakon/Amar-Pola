# Data Retention Schedule — Candidate Periods / Owner & Counsel Sign-off Pending

> **Document control:** M0 / 03-legal-and-privacy · Proposed owner: Privacy counsel + owner (not assigned) · Registry: DRAFT_LEGAL_REVIEW_REQUIRED; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

**Document MA-RET-001 | 2026-10-27. Status DRAFT, NOT ADOPTED.** No real child data collection approved. Earlier docs propose **14 days raw GPS**; uploaded draft proposed **30 days**. These conflict; neither is an adopted retention policy. Date/time windows below are candidates for discussion and must be reconciled with purpose-specific India legal and Play disclosures before implementation.

## Retention principles
- Data purpose + guardian authority are separate from Android grants. Retention measured from **original observation/event time** where applicable, not later upload or batch queue acceptance.
- Offline 48-hour Alarka queue is a **device storage capacity design target**, not permission for unrestricted capture, a universal 48-hour data-retention policy, or a guarantee that the OS will gather data.
- A temporary PostgreSQL inbox contains actual precise child coordinates until worker Tx B; WAL/backups and dead-letter copies must be inventoried and safely minimized. No general admin direct inbox reader.
- Stop future intake with child/device revocation-generation/tombstones **before** deleting existing records so 48h offline retry cannot revive deleted child data.
- CERT-In 28 April 2022 Directions require **secured ICT logs rolling 180 days in India for covered entities**. Do not confuse this with storing **all raw child's GPS, media or app behavior for 180 days**.

## Category decision ledger

| Data | Candidate retention / outstanding decision | Clock start |
|---|---|---|
| Guardian and child identity/pairing/grants | Needed for account; deletion after verified closure, exceptions reviewed | Closure/revocation |
| GPS raw/accuracy/speed | **14 days earlier vs 30 days submitted; OWNER/COUNSEL MUST CHOOSE** | observed_at |
| Encrypted unsynced device GPS queue | Up-to-48h **capacity target**; ACK cleanup/overflow and legal TTL to specify | capture |
| PostgreSQL inbox pending/leased/failed | As short as durable recovery safely permits, specific bound TBD; never drop ACKed data before Tx B recovery | accepted_at |
| Inbox processed payload/WAL and outbox | Purge after verified raw commit/backup retention; bound TBD | processed_at |
| Device event dedup ledger | Minimum replay window including long offline attempts; scrub identifiers on deletion | event / receipt |
| Trip geometry/history/stops/named places | 90 days proposed but unapproved; derived details may require *shorter* period | trip end |
| App usage event/session/aggregates | 30 days proposed but **feature release OFF**, behavioral-monitoring gate | observed period |
| Capability/permission changes | Latest snapshot and limited change audit, candidate 90 days | device report time |
| Command/SOS status | 12 months proposed, justify incident/safety purpose | event |
| Media-activity metadata | 12 months proposed, no VPS media binary; highly sensitive | request/session |
| VPS media contents | **NOT STORED BY DESIGN** | N/A |
| Guardian local encrypted saved media | Parent device/provider's approved controls, not VPS guarantee | local save |
| Admin case/search/access log | Candidate 24 months, restricted and independent audit | audited event |
| ICT authentication/security logs | CERT-In minimum 180 days within India **where applicable** | logged event |
| Subscription/tax/GST invoices | Per actual applicable statutory retention verified by accountant/counsel | transaction |
| Encrypted backups/PITR | 35 days proposed, not verified against RPO/RTO or deletion rights | backup completion |
| Consent/authority verification receipts | Evidentiary purpose, period TBD; no excess documents | recorded decision |
| Data subject/grievance/incident records | Minimized separate legal need, scoped holds with review date | closure/event |
| Anonymous aggregates | Only demonstrably irreversible anonymity | aggregation |

## Rights, erasure and restore requirements
Authenticated guardian/child rights and custody conflicts need safe case handling; no broad co-parent disclosure by default. Revoke new API ingestion and device credentials, publish deletion tombstone, clear raw/inbox/derived data and role-limited caches, and apply deletion ledger on **all restored backups** before reopening APIs. Parent-local/Google Drive content cannot be erased from inaccessible devices instantly. Set realistic advertised processing deadlines *only after service implementation and counsel review*. Backup/WAL expiry and legal hold exceptions must be explained to the person requesting deletion.

## Implementation and gates
- [ ] Publisher/privacy lead and India counsel approve every data category, exact number of days, purpose and legal exception.
- [ ] Resolve **14 vs 30 day GPS** conflict in previous documents; compare storage and history route impact.
- [ ] Implement per-store TTL/partition cleanup, purged inbox payload, restore tombstone, dedup and encrypted backups.
- [ ] Test long offline Android queue, worker crash after 202, stopped child device, deleted child event re-ingestion, wrong-family audit access, and old backup restoration.
- [ ] Ensure privacy notice, Google Play Data Safety and processor agreements agree.
- [ ] Check relevant DPDP provisions' phased legal commencement at actual launch; do not state that every 2025 Rule applies in Oct 2026.

**Official refs:** https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf ; https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf. Related: [DPIA](DPIA.md) and [Account Deletion](../../M6-guardian-erasure-security/01-data-erasure-and-access/ACCOUNT_DELETION_DESIGN.md).

**No retention or deletion job is authorized to execute on production from this draft.**

## Uploaded MA-RET-001 candidate review and precise owner decision ledger — 2026-10-27

The uploaded retention document proposed numbers for **R-01…R-18**. It was **not signed by the controller/owner or India counsel**. This section preserves its numbered categories and offers its numbers as *options* without silently replacing this file's legal/no-go state. In particular **14-day raw GPS from earlier project drafts versus 30-day raw GPS in the upload remains unresolved**.

| Source ID | Category (uploaded draft) | Uploaded **candidate** | Project-aligned decision / new surface |
|---|---|---|---|
| R-01 | Guardian account | Account life + 30 days after closure | Owner/counsel approval and lawful account/security exceptions required. |
| R-02 | Child profile and paired devices | Until removal + 30 days | Revoke device grants and reject 48-hour delayed uploads **before** row deletion. |
| R-03 | Raw GPS | 30-day rolling | **CONFLICT: older 14 days; neither approved.** Applies final PostGIS observations measured from \`observed_at\`. |
| R-04 | Trips and stops | 90-day rolling | Derived geometry may expose school/home; purpose and shorter alternative to be assessed. |
| R-04a | Named places | Until manually deleted/child removal | Home/school should be handled as especially sensitive locations. |
| R-05 | App usage summaries | 30-day rolling | Separate raw UsageEvents, sessions, daily aggregate TTL; **feature OFF pending India/Play review**. |
| R-06 | Capability and permission change reports | Latest + 90 days history | Keep current authoritative snapshot and bounded revisions, child scopes. |
| R-07 | Command/SOS lifecycle | 12 months | Safety-purpose justification, truthful failure receipts and legal hold handling. |
| R-08 | Media request/session **metadata** | 12 months | No VPS media files; actor/child/time/size/reason metadata are still sensitive. |
| R-08a | Media content | Never stored on VPS | Parent-local encrypted recording and TURN transient traffic are **separate**; no VPS media archive. |
| R-09 | Payments/invoices/GST | Draft "commonly 6–8 years" | **No fixed number adopted**; accountant/counsel must identify each applicable statute. |
| R-10 | ICT/security logs | 180 days direction; 12 months proposed | CERT-In **rolling 180 days within Indian jurisdiction for covered ICT logs**; do NOT apply this to all raw GPS. |
| R-11 | Admin case/read-access audit | 24 months proposed | Strong access restrictions, immutable-style append evidence and deletion/legal holds separate. |
| R-12 | Backups | 35 days proposed | Actual RPO/RTO, PITR/WAL/offsite retention and deletion tombstone restore must be tested. |
| R-13 | Child turns 18 | Consent/authority reset and 30-day deletion proposed | **Verify lawful rights and transition design**; no unilateral silent extension of guardian monitoring. |
| R-14 | Support/grievance | 24 months after closure | Needs grievance rules and risk-based minimization. |
| R-15 | Incident records | 5 years after closure proposed | Depends on incident law, litigation hold and restricted evidence store. |
| R-16 | Parental consent/verification records | Account life + 3 years proposed | Purpose/evidence period and identity-document minimization unresolved. |
| R-17 | Guardian's optional Drive backup | Guardian-controlled | Cannot promise remotely deleting a guardian's inaccessible or copied Drive/phone files. |
| R-18 | Irreversibly anonymous aggregates | No fixed limit suggested | Must confirm non-reidentifiability; home/school routes cannot be deemed anonymous on assertion. |

### Stores added by the accepted GPS ingestion and admin-console architecture

| Surface | Specific proposed retention control required before release |
|---|---|
| Alarka encrypted **48-hour offline capacity** | Size/time quota, durable server receipt, legal TTL, overflow notification; no guaranteed 48-hour GPS capture or unconditional collection. |
| **PostgreSQL durable inbox** | Temporary GPS JSON payload; restrict read roles; process/retry/quarantine safely; purge PROCESSED payload promptly after durable Tx-B/approved retention, not before. |
| PostgreSQL WAL/PITR/offsite backups | Bound each copy's actual lifetime, prohibit restoration of deleted users without tombstone reapplication, verify India hosting/processor scope. |
| Dedup and idempotent device-event ledger | Retain enough for retry/replay window; on child deletion tombstone must block reingest even if local offline queue still exists. |
| Reconstruction jobs/route geometries and latest-location cache | Tie to original GPS purpose and child/grant rights; expire all derived copies as well as raw rows. |
| App usage raw events/sessions/daily aggregates | Treat as separately restricted behavioral data; do not assume summary TTL also covers raw event cache. |
| Independent admin-access audit | Separate case scope, access controls and law-based schedule; staff may not self-erase sensitive audit records. |

### Executable retention gate — NOT YET IMPLEMENTED

The owner must sign a category-specific decision with **retention days, start clock, legal purpose, deletion method, backups/WAL bound, exceptions, reviewer and effective date**. Verify delete jobs using partitions where appropriate and strict transactional tombstones for revoked/deleted children. Test a 48h delayed Alarka upload **after** family deletion to prove it is rejected. If backup restoration or worker replay reintroduces a deleted child's location, the release test **fails**. Do not turn any candidate period above into a production TTL before that signed decision.

The uploaded draft's suggestion to delay a deletion request indefinitely whenever another guardian objects is **not approved**; custody/abuse reports require a confidential, case-based legal decision, not routine sharing or automatic denial. Operational request response targets in the upload (3 business days acknowledgement and 30 days completion) also remain product commitments **to be validated**, not existing statutory SLAs.

Cross references: [Account Deletion](../../M6-guardian-erasure-security/01-data-erasure-and-access/ACCOUNT_DELETION_DESIGN.md), [Data authorization/recovery](../../M1-secure-platform-foundation/03-security-and-permissions/DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md), [GPS Inbox ADR](../../M2-location-collection/01-location-collection-and-ingestion/POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md), [DPIA](DPIA.md).

