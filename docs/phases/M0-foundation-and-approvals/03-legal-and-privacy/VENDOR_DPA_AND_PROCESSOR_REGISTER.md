# Vendor DPA / Data Processor Register — Contract and Transfer Gate

> **Document control:** M0 / 03-legal-and-privacy · Proposed owner: Privacy counsel + owner (not assigned) · Registry: DRAFT_LEGAL_REVIEW_REQUIRED; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

**Status:** Draft vendor due-diligence register, no signed DPAs or selected deployment region verified. Reviewed 2026-10-27.

| Vendor or service | Planned use and personal data | Contract/DPA/compliance assessment | Actual status |
|---|---|---|---|
| Oracle Cloud Infrastructure (OCI) | C++ API, PostgreSQL raw child GPS/history, inbox/WAL/backups, security logs | Verify legal controller and OCI region (historical Chicago vs possible Mumbai), India transfer controls, DPA, support residency, subprocessor list, recovery, incident notice, encryption/key custody | NO VERIFIED TENANCY/DPA/FINAL REGION |
| Google OIDC | Guardian sign-in, account identifiers | Privacy terms, OpenID verification, scopes, retention, minors policy, OAuth app verification | DESIGN ONLY |
| Google Maps / Roads | Map tiles, optional road matching; potentially location requests/IP/device tokens | Exact SDK/APIs/Google Maps Platform terms, geospatial caching/storage restrictions and location disclosure | DESIGN ONLY |
| Firebase Cloud Messaging | Device push token, event notification hints (never raw child GPS in push) | Google/Firebase terms, transfer and processor details, minimum payload, authorization/revocation | DESIGN ONLY |
| Google Play Billing / Play Console | Parent subscriptions/receipts and installation/reviewer declarations | Developer/merchant terms, billing/revenue/refund obligations, account compliance and data safety | DESIGN ONLY |
| Google Drive API (optional) | Guardian-consented selected files or backups | OAuth restricted scopes, app verification, user-specific data deletion and transfer | DISABLED / DESIGN |
| WebRTC / coturn relay | Encrypted transient sensor media if ever permitted; metadata and IPs | Hosting/operator selection, processing terms, IP logging, no persisted media, legal and Play media gates | RESEARCH P3 OFF |
| SMS/email provider | SOS fallback, guardian verification, notices | DPA, local consent, delivery receipts, costs, support and deletion | UNSELECTED |
| SSO/MFA vendor for admin | Privileged staff identity, case-access logs | Data minimization, incident alerts, sign-in key privacy, review | UNSELECTED |
| Security/observability/backup provider | Redacted ops metrics, ICT logging, backup content | India 180-day ICT logs where covered, encryption/retention and no raw child coordinate leakage | UNSELECTED |

## Contract artifacts required per actual vendor
- [ ] Correct signed publisher legal entity / controller identity and processor legal name.
- [ ] Master service agreement, executed DPA (where applicable), privacy notice and relevant lawful transfer/legal basis.
- [ ] Scoped categories (parent IDs, child GPS, permissions, media metadata, usage events), purposes, subprocessors, region/transfers and technical measures.
- [ ] Roles, audit rights, security certifications **verified** (not assumed), encryption, key access, backup locations and deletion schedule.
- [ ] Incident notification time to enable CERT-In 6h triage and applicable phased DPDP notifications; named contact/backup.
- [ ] Actual access/inventory log, cost/exit plan, data export/revocation/deletion and test evidence.
- [ ] Counsel/security/vendor owner approval and signature reference stored privately, not uploaded to public GitHub.

Do **not** copy third-party vendor template terms into an unsigned pseudo-DPA and call them legally executed. This register is an owner assignment ledger; exact vendor contracts must be obtained, reviewed and signed through normal procurement.

Related: [DPIA](DPIA.md), [India/Play Risks](INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md), [Retention](DATA_RETENTION_SCHEDULE.md), [Security](../../M8-operational-readiness/02-operations-and-support/SECURITY_AND_OPERATIONS.md).
