# Project Engineering, Security, Operations and Legal Document Index

**Reviewed 2026-10-27.** This index distinguishes **written documentation** from **operational implementation and approval**. All legal/commercial texts marked draft require an identified legal entity, final India/Play rules check and signatures.

## Current runnable baseline and developer process
- [Root README](../README.md), [Build and Run](BUILD_AND_RUN.md), [Developer Onboarding](DEVELOPER_ONBOARDING_AND_CODING_STANDARDS.md), [Contributing](../CONTRIBUTING.md), [Conduct](../CODE_OF_CONDUCT.md), [Changelog](../CHANGELOG.md).
- [Release, Branch and Version Policy](BRANCHING_VERSIONING_AND_RELEASE_PROCESS.md), [Release Readiness](DEPLOYMENT_RELEASE_READINESS_CHECKLIST.md), [About/Topics to apply](REPOSITORY_ABOUT_AND_TOPICS.md).
- Existing `.github/workflows/m1-contract-and-tenant.yml` only tests the **M1 11-operation structural API** and PostgreSQL 16 synthetic tenant isolation. Android `android/alarka` and `android/madalasa` are **non-runnable source scaffolds**, not deployed apps.

## System architecture
- [SRS](SRS.md), [Core Technical Specification](TECHNICAL_SPECIFICATION.md), [Implementation Specification](IMPLEMENTATION_TECHNICAL_SPECIFICATION.md), [Requirements Traceability](REQUIREMENTS_TRACEABILITY.md).
- [GPS Postgres Durable Inbox + 48h Device Queue and C++ Bulk ADR](POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md), [Data Authorization/Recovery](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md), [Tracking Runtime](TRACKING_RUNTIME_AND_ALGORITHM_CONTRACT.md), [Device Compatibility](ANDROID_COMPATIBILITY_MATRIX.md).
- [Parent/Child Capability and Permissions ADR](CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md), [Media Runtime ADR](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md), [Media Activity Logging ADR](MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md), [Admin Panel Spec](ADMIN_PANEL_SPECIFICATION_2026.md).
- Existing Figma diagrams/screens and companion node indexes under [Figma Handoff](ui/figma-functional-handoff/README.md). No assumption that diagrams are code.

## Security, quality, operations
- [Root SECURITY.md](../SECURITY.md), [STRIDE Threat Model](THREAT_MODEL_STRIDE.md), [Signing/Key Policy](APP_SIGNING_AND_KEY_MANAGEMENT_POLICY.md), [Dependency Register/SBOM Plan](THIRD_PARTY_DEPENDENCY_AND_SBOM_REGISTER.md).
- [Formal Test Strategy](TEST_STRATEGY_UNIT_INTEGRATION_LOAD_SECURITY.md), [Validation Plan](VALIDATION_AND_RELEASE_PLAN.md).
- [Deploy/Rollback/Restore Runbooks](OPERATIONS_RUNBOOKS.md), [Monitoring/SLOs](MONITORING_ALERTING_SLO_SLA.md), [Restore Test Evidence Template](BACKUP_RESTORE_TEST_EVIDENCE.md), [Incident and Breach Procedure](INCIDENT_AND_BREACH_RESPONSE_PROCEDURE.md), [Support/Escalation SOP](SUPPORT_AND_ESCALATION_SOP.md).
- [Licensing Decision](LICENSING_DECISION_AND_IP_REGISTER.md): root [LICENSE](../LICENSE) is **interim all-rights-reserved**, not an owner-approved open-source grant.

## Privacy, legal, partners and distribution
- [DPIA](DPIA.md), [Data Retention Draft](DATA_RETENTION_SCHEDULE.md), [Guardian Authority/Verifiable Consent](VERIFIABLE_PARENTAL_CONSENT_AND_GUARDIAN_AUTHORITY.md), [Grievance Officer/Redressal](GRIEVANCE_OFFICER_AND_REDRESSAL_PROCESS.md), [Vendor DPA/Processor Register](VENDOR_DPA_AND_PROCESSOR_REGISTER.md).
- [India Legal/Google Play Risk Assessment](INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md), [DPDP Child Gate](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md), [Play Console Declaration/Reviewer Pack](PLAY_CONSOLE_DECLARATIONS_AND_REVIEWER_PACK.md).
- [Public Legal Pages staging](../public/legal/README.md): `terms.html`, `privacy.html`, `refund-cancellation.html` remain **DRAFT noindex and not hosted**. Existing [Terms/Subscription Draft](TERMS_AND_SUBSCRIPTIONS_DRAFT.md) is not a final contract.
- Actual Oracle/Google/etc DPA signatures, Play Console declarations, published legal pages and independent security/restore test evidence **not obtained**.

## Document hygiene
All drafts remain subject to change and cannot be used to claim child-data processing authority, Android permission exceptions, Google Play approval, implemented features, or actual SLO/SLA. Update this index when modules or approval statuses change.
