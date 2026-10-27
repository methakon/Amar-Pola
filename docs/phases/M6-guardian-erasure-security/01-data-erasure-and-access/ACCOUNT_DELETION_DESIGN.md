# Account and Data Deletion: Functional and Technical Design

> **Document control:** M6 / 01-data-erasure-and-access · Proposed owner: Engineering lead (not assigned) · Registry: DOCUMENTED_REVIEW_PENDING; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

> **Current product naming:** **Madalasa** parent/guardian app, **Alarka** child companion; GitHub repository [Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka). [Brand and Markandeya Purana context](../../M0-foundation-and-approvals/02-market-and-feasibility/BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | Draft 2026-10-25 | Not yet implemented**

This document describes **mandatory planned behavior** for the parent app's account deletion path, a public account-deletion web entry point, child unpairing, retention and optional Drive data. Do not publish a deletion URL or claim deletion capabilities until the service exists.

## 1. Product requirements

- A signed-in parent can access `Settings > Account > Delete account` or a clear equivalent.
- An unauthenticated former user can request deletion from a public, identifiable web page without reinstalling Madalasa–Alarka.
- The service shall provide identity verification proportional to the deletion risk, without demanding that a user restore access to the deleted app.
- The page explains which data will be deleted, which could legally be retained and how long, and how subscriptions are canceled.
- Deletion of an account revokes linked device credentials, stops new telemetry ingestion, revokes delegated backend integration access where feasible, deletes or schedules erasure of attached historical data, and records minimal auditable request state.
- A parent can unpair an individual child device without necessarily deleting their entire parent account.
- Removal from our backend does not automatically erase a parent-created Google Drive copy unless the actual authorized API operation and parent approval cover it; explain this separately.

## 2. Proposed API

```text
POST /v1/account/deletion-request
  -> request_id, verification_state, created_at
POST /v1/account/deletion-request/{id}/verify
  -> verified | rejected
GET /v1/account/deletion-request/{id}/status
  -> requested | verifying | queued | processing | completed | failed
POST /v1/devices/{deviceId}/unpair
  -> revoked_at
POST /v1/integrations/google-drive/revoke
  -> revocation_result
```

Use authenticated parent identity where available and secure one-time verification for web requests. Rate-limit requests. Do not expose request status across accounts.

## 3. Deletion state machine

```text
REQUESTED -> VERIFIED -> ACCESS_REVOKED -> DELETING -> COMPLETED
    |            |             |
    v            v             v
  REJECTED    CANCELLED    FAILED_RETRYABLE
```

Access revocation is immediate once authorized; data deletion may be asynchronous and retried. Use durable job IDs and idempotency.

## 4. Data category workflow

| Category | Expected action | Verification |
|---|---|---|
| Parent profile/auth link | Deactivate and remove/retain minimal legal audit as appropriate | Cannot authenticate after completion |
| Device enrollment keys | Revoke and remove | Child API returns unauthorized |
| Location and route history | Delete per device/account in primary storage | Queries return no deleted events |
| Usage aggregates | Delete | Reports return empty |
| Policies and commands | Cancel execution, revoke pairing, minimize audit as legally appropriate | No new command delivered |
| Optional media metadata/files | Delete owned internal storage; handle Drive copies according to clear policy and parent choice | Object inaccessible and deletion receipt |
| Google Drive OAuth | Revoke stored token and unlink | Integration no longer works |
| Backups | Delete or expire under explicit documented schedule | Restore test does not resurrect deleted data after relevant retention |
| Security/billing records | Retain only as required under defined legal/fraud obligations | Retention exception documented |

## 5. Public request page content — draft

**Title:** Request deletion of your Madalasa–Alarka account

“Use this page to request deletion of your Madalasa–Alarka parent account and associated information, including paired devices, location history and app-usage reports. We may need to verify account ownership before acting. Some transaction or security records may be retained where legally required; see our Privacy Policy for the exact categories and periods.

If you have an active subscription through Google Play, follow the Play subscription cancellation process. Account deletion and subscription cancellation are separate actions. [SUPPORT CONTACT] can help with access or deletion requests.”

**Web destination:** `https://[PUBLIC DOMAIN]/account/delete` — placeholder only, **not live**.

## 6. Test cases

- Owner requests deletion while signed in; credentials revoked and children no longer sync.
- Unauthenticated web request with valid email verification, invalid email and replay.
- Subscription active; clear instruction and entitlement handling, no surprise billing promises.
- Device offline during deletion; later sync rejected.
- Interrupted deletion job resumes without recreating accounts.
- Google Drive previously unlinked, token expired, and uploaded copies handled according to published policy.
- Deleted account attempt to sign in/re-pair without re-registration.
- Private/deleted data absent from analytics/logs/backups according to documented schedule.

## 7. Publication blockers

- [ ] Final support email/operator identity
- [ ] Actual public HTTPS deletion page and working request workflow
- [ ] In-app deletion entry point
- [ ] Tested background deletion job and device credential revocation
- [ ] Defined backup/log/legal retention limits
- [ ] Live privacy policy reflecting this behavior
- [ ] Data safety declaration reconciled with actual deletion capabilities

## Official source

https://support.google.com/googleplay/android-developer/answer/13327111

## 8. India data retention, purpose revocation and backup-recovery legal gate

The India-first plan requires consent/authority and DPDP feature-purpose review before ingestion of any real child's data: a realtime safety location exemption may not extend to app-usage or historic route datasets. [India DPDP and Chicago transfer](../../M0-foundation-and-approvals/03-legal-and-privacy/INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md). Retention assumptions in old financial projections are not policy approval. Candidate design: raw 14d, history 90d, usage OFF, audit 365d, backups 30d; final periods require owner and legal signoff.

Erasure/restoration tests must cover **offline device queue**, replicated/bucket backups, token/SSE revocation, separate Drive account responsibilities and legally necessary record retention. A recovered snapshot may not resurrect erased child GPS; see [OCI DR and restore tests](../../M8-operational-readiness/01-cloud-infrastructure/OCI_CHICAGO_RECOVERY_AND_PILOT_READINESS.md). Public deletion web page still not deployed.

## 2026-10-27 capability metadata retention/deletion addition

The new [MA-CAP-ADR-002](../../M1-secure-platform-foundation/03-security-and-permissions/CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md) designs server-stored child device compatibility, Android permission scopes/statuses, enrollment generation and report version, last verified/received timestamps and a bounded event history. Treat these as linked child/family personal metadata: include latest snapshot, historical changes, cache/SSE copies, support diagnostics and backup restore protection in authenticated family/device deletion and export assessments. Old Alarka offline reports must not revive deleted capability records or previously revoked grant state. Final retention TTL and legal basis remain undecided; no raw sensor media collected by a read-only scan. Do not publicly promise immediate revocation broadcasts when Android may kill the app.

## 2026-10-27 deletion dependencies for media activity and administrative access audit

If the proposed FR-050/051 metadata-only features ship after approval, deletion and export scope shall include **media_activity** summary, **media_activity_events** append log, support/admin query caches, authorized parent histories and backups, child/guardian identity joins, plus separately classified **admin_access_audit** of privileged reads. Remove child-linked events under approved retention policy and ensure an offline Alarka/Madalasa retry cannot reintroduce them after deletion tombstone. Legally required preservation or security audit retention, if any, needs product-specific India counsel decision, segregated access and bounded TTL; do not invent retention lengths. Media files never sit in VPS audit tables. Server cannot promise deletion of a parent-local recording not under its control. [Media Activity Audit ADR](../../P3-deferred-research/01-media-and-administrator-research/MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md).

## 2026-10-27 deletion across accepted offline device buffer and PostgreSQL location inbox

[MA-INGEST-ADR-004](../../M2-location-collection/01-location-collection-and-ingestion/POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md) adds a temporary sensitive server `location_ingest_inbox` data store and local Alarka encrypted queued coordinates to the data lifecycle. When an authorized guardian removes device access or a child/family account is deleted, stop future ingestion **before** replay can import old 48h batches: revoked device enrollment generation/credential and server tombstone must reject all retry IDs. Apply deletion schedule to inbox PENDING/LEASED/PROCESSED/QUARANTINED, raw GPS partition rows, dedup ledger, reconstruction outbox, latest location/read caches, derived trip/usage records and backups/restore manifests. The service cannot promise to remotely wipe a force-stopped/offline physical phone instantly; on next eligible Alarka run enforce revoked grants and local queue purge under lawful policy. No unlimited deletion bypass because a worker is processing an inbox row; worker must check current authorization/tombstone before raw commit. Retention decisions and privacy audit tests T-ING-14/20 remain unresolved.
