# Release Readiness & Owner Decision Gate — M0/M1 → Android Pilot

**State as of 2026-10-27:** All protected real-child data features **NO-GO**. Repository contains M1 contract/SQL test baseline, many architecture/UX documents, Android **source scaffolding only**, and no runnable C++/Android apps or production deployment.

## Ownership and corporate setup
- [ ] Legal publisher/controller, registered address, tax entity, Play merchant and legal IP/license decision **signed**.
- [ ] GitHub About description/topics, private vuln report channel, enforced CODEOWNERS review and branch protections set in GitHub UI.
- [ ] Named, funded security response lead/backups, Grievance Officer and confidential support contact.
- [ ] Staff responsibility roster and release/incident authorization matrix verified.

## Policy and child safety
- [ ] India counsel signs child-specific data purposes, DPDP phased commencement/exemptions and rights.
- [ ] Verifiable parental consent/authority and custody dispute/safe-report handling implemented and verified.
- [ ] Google Play Families/background location/monitoring/isMonitoringTool/usage/media/target-SDK approval from **actual Play Console**; signed reviewer demo and Data Safety.
- [ ] Final privacy, terms, cancellations/refunds and child deletion web pages **HTTPS-hosted and tested** (current public/legal pages are DRAFT, noindex).
- [ ] Actual data retention schedule signed; raw GPS 14-vs-30-day dispute resolved, local 48h capacity not mistaken for legal retention.

## Implementation and test
- [ ] Kotlin Alarka/Madalasa Gradle builds and Play-supported manifests, permissions, supported device matrix.
- [ ] C++20 Drogon API, Postgres/PostGIS migrations, device pairing, forced RLS child scopes.
- [ ] Durable PostgreSQL GPS inbox Tx A with committed 202, C++ leased bulk Tx B and 48h delayed/duplicate/deletion replay tests.
- [ ] Security leak prevention, admin MFA/case read audit, honest command and sensor statuses, SOS fallback.
- [ ] Test plan evidence: unit/integration/E2E, 1k/10k/100k scale, Android OEM, independent penetration/STRIDE, signing/SBOM/vendor.
- [ ] Report actual completed vs missing tests; design documents are not acceptance results.

## Infrastructure and operations
- [ ] OCI final region, backups/log region, processor DPAs, IAM/network/TLS/secret manager, encrypted storage.
- [ ] Off-host backup + restored test with recorded actual RPO/RTO; per-child tombstone restore, inbox durability.
- [ ] Monitored SLOs, paging/incident playbooks, CERT-In clock, applicable DPDP notice process, runbook and on-call coverage.
- [ ] Released app signing lineage, versionCode and staged rollout/rollback verified, vendor incident contacts.

## Go / No-Go record
Release type: [SYNTHETIC DEVELOPMENT / ADULT DOGFOOD / REAL CHILD PILOT / COMMERCIAL]. Legal entity: [TBD]. Release commit/build SHA: [TBD]. Approvers: Product [TBD], Android [TBD], Backend [TBD], Security [TBD], India counsel [TBD], Privacy/Grievance [TBD], Play reviewer evidence [TBD]. Decision: **NO-GO for real children until independently approved**. Date: [NOT APPROVED]. No placeholder constitutes a signature.

## 2026-10-27 uploaded governance document reconciliation — review does not equal approval

The six supplied governance files were reviewed/merged under \`docs/\` and recorded in [review ledger](UPLOADED_GOVERNANCE_DOCUMENTS_REVIEW_2026-10-27.md). This **does not close** the real-child/commercial NO-GO: retention 14-vs-30-day GPS and all other periods are unsigned; DPIA has no controller/India counsel signoff; security reporter email/PGP/private GitHub intake not verified; incident roster/24x7 escalation not verified or tabletop-tested; root licence has no identified rights-holder/publisher; Play/DPDP child collection remains feature gated; Android, C++ and Postgres location ingestion still not implemented. Owner must record each approval and evidence before this checklist can move to GO.

## 2026-10-27 repo-wide evidence gate

The [verified gap register](REPOSITORY_GAP_AND_DELIVERY_AUDIT_2026-10-27.md) distinguishes present governance/docs from missing actual approvals. Additional NO-GO checks: [ ] GitHub About/branch protection/private vulnerability reporting inspected and enabled by repo owner; [ ] all root policy contacts are reachable; [ ] Android source-to-build A1 runnable debug APKs, lint and signed artifact evidence filed; [ ] independent legal and security approvers assigned, not only default CODEOWNER; [ ] current partial M1 CI does not substitute for device/Play/penetration/restore tests. Documented repo sections cannot be counted as completed M0 gates.
