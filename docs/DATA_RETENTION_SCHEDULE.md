# Data Retention Schedule — Candidate Periods / Owner & Counsel Sign-off Pending

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

**Official refs:** https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf ; https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf. Related: [DPIA](DPIA.md) and [Account Deletion](ACCOUNT_DELETION_DESIGN.md).

**No retention or deletion job is authorized to execute on production from this draft.**
