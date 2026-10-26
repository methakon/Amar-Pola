# Security Architecture, Threat Model and Operations

> **Current app names:** **Madalasa** (guardian/parent), **Alarka** (child companion). GitHub repository [Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka), renamed 2026-10-26. [Source story and naming contract](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | Draft 2026-10-25**

## 1. Security priorities

Protect the child's precise location, activity, media (if ever released), parent identity, command execution and billing. A compromised parent credential or backend is a high-severity privacy event. Default authorization is deny, with smallest useful permission scope.

## 2. Trust boundaries

1. Child Android sandbox / Android OS and permission state.
2. Local encrypted queue / Android Keystore-backed device identity.
3. Public Internet / HTTPS API ingress and push service.
4. Backend API / authorization logic / persistent PostgreSQL.
5. Parent Android app / parent auth identity provider.
6. Third-party Google Maps, Play Billing, Drive, cloud hosting and monitoring processors.
7. Optional managed DPC commands, separate from ordinary install.

Never trust a client-supplied `parent_id`, device management flag or subscription status without server verification. Capability reports are hints and must be revalidated on the device at execution.

## 3. Threat inventory and mitigations

| Risk | Attack | Controls | Test |
|---|---|---|---|
| Parent account takeover | Unauthorized device history/control | OIDC/passkeys, step-up auth for sensitive actions, session revoke, login anomaly alerts | Token reuse and session revoke |
| Device pairing hijack | Attacker redeems code | Short-lived one-use codes, rate limiting, parent confirmation, device bound key | Replay, brute force, code expiry |
| Insecure direct object reference | Parent queries another family's location | Per-request ownership authorization, strict tenant scoping | Cross-account negative tests |
| Device impersonation | Fake location/usage upload | Per-device cryptographic credential, signature or mTLS as appropriate, key rotation | Forged device ID |
| Command replay/abuse | Duplicate or expired instruction | Unique command ID, TTL, idempotency, least privilege, signed policy version | Duplicate delivery and expiry |
| Location exposure | Leaked logs/database/backups | Encryption, data minimization, separate secrets, retention, redacted logs | Log/backup inspection |
| Unsafe DPC rule | Critical app blocked | Protected-package denylist plus Android policy eligibility check and recoverability | Recovery from rejected suspension |
| OAuth theft | Drive access | Encrypted protected token store, PKCE, narrow scopes, revocation | Token log/leak test |
| Billing bypass | Fake purchase token | Verify provider server-side, deduplicate provider notifications | Fake/refunded purchase |
| Denial of service | Flood command/data endpoints | Rate limits, request bounds, quotas, bounded queue, circuit breakers | Load and malformed body tests |
| Release supply-chain compromise | Malicious SDK/native library | Dependency/SBOM scans, reproducible build, signed tags, limited CI secrets | Tamper test |
| Retention failure | Restored erased data | Deletion ledger, retention jobs, controlled backups and restore protocol | Restore of deleted tenant |

## 4. Minimum cryptographic and credential plan

- Strong TLS, current ciphers, strict HTTPS and verified hostnames.
- Parent OIDC with PKCE on public clients; never embed server secret in APK.
- Child private key preferably non-exportable in Android Keystore, unique per pairing, rotated/revoked after compromise.
- Backend asymmetric signing keys/rotating key IDs and protected secret manager.
- Database encrypted disks plus tightly scoped DB roles; consider field-level protection for high-risk attributes.
- Backups encrypted and access logged; restore instructions never restore revoked credentials to active state.
- CI secrets isolated from untrusted pull requests; release signing/upload key never stored in Git.

## 5. Security alerts and incidents

Severity examples:
- **Critical:** unauthorized access to multiple families, credential exfiltration, covert recording defect.
- **High:** improper device pairing, unexpected command execution, sensitive access control bypass.
- **Medium:** prolonged telemetry backlog or subscription state error.
- **Low:** non-sensitive UI error.

Incident response: contain (disable remote commands if necessary), revoke credentials, preserve redacted audit evidence, assess exposure and legal notice obligations, patch and test, restore service, document root cause.

## 6. Operations runbook

### Availability
Use health/readiness endpoints; monitor p95 latency, DB connections, queues, location lag, request failures, app crashes/ANRs. Alert on sustained degradation, not every offline phone.

### Backups
Encrypted daily/incremental according to SLA; perform periodic restoration tests. Distinguish disaster recovery from account-deletion obligations.

### Rotations
Document key rotation, cert renewal, API key restrictions, OAuth token revocation and Play Billing webhook/authentication changes.

### Deployment
Staging data is synthetic. Promote container by immutable digest; migrate database with reviewed reversible changes; use gradual deployment with rollback and feature switches.

### Feature shutdown
Backend can disable a risky operation, but child-app controls must not depend on concealment or blocked user-facing permissions. Respect device owner and Android policy lifecycles.

## 7. Security release checklist

- [ ] Document actual auth provider and device credential implementation.
- [ ] Complete API authorization (including cross-tenant negative tests).
- [ ] Review crash/log data for personal location/media leakage.
- [ ] Penetration test pairing, policy control, billing and account deletion.
- [ ] Review mobile app signing and third-party SDKs.
- [ ] Test DPC safe recovery and policy cancellation.
- [ ] Test retention, revocation, backup and restore.
- [ ] Complete operator on-call and incident communication contacts.
- [ ] Complete age/privacy/legal and Google Play monitoring policy review.

### Further reference
- https://mas.owasp.org/
- https://owasp.org/API-Security/
- https://developer.android.com/privacy-and-security/security-best-practices

## 8. Scalable location infrastructure and family authorization supplement

See [Adaptive Movement and Multi-Tenant C++ Server Architecture](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md) for the guardian/family/child ACL model, PostgreSQL row-level security with transaction-scoped context, protection of location event/outbox queues, strict API IDOR/BOLA tests, per-tenant SSE and cache isolation, accepted-but-late data handling, synthetic load tests and individual account deletion across raw partitions and derived trips. Security signoff remains blocked until this design is implemented and tested.

## 9. 2026-10-26 India-law, recovery and operational staffing additions

**India DPDP:** under-18 parent verification, Rule 12 limited real-time safety exception, app-usage/history scope and US Chicago transfer require counsel opinion before real children's data. See [legal gate](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md). Identity/permissions alone do not confer legal custody.

**Resilience:** OCI one-VM architecture has unproven RPO/RTO. [Recovery readiness](OCI_CHICAGO_RECOVERY_AND_PILOT_READINESS.md) proposes clocked backup/rebuild tests, RPO/RTO targets by dev/pilot/prod tier, off-host erasure ledger and separate SOS fallback. A single-VM process restart does not satisfy HA or guarantee guardian alerts.

**Staffing:** [Delivery capacity & break-even](PRICE_BREAK_EVEN_STAFFING_AND_DELIVERY_CAPACITY.md) assigns explicit accountable Android parent, Android child, C++/DB, QA, security/legal and OCI ops ownership. All remain **unassigned** pending owner roster, actual cash/runway and on-call coverage; do not claim round-the-clock monitoring/support.

## 10. Conditional media threat modeling and parent error protection (2026-10-26)

The owner accepts **conditional media engineering research**, not production recording or commercial authorization. The design candidate is encrypted direct P2P media or a TURN relay **without VPS media files** plus optional encrypted Madalasa-local recording. This reduces central archive exposure but not threats from compromised parent/child endpoints, impersonated device keys, rogue signaling, TURN abuse, stolen guardian sessions, bystanders and metadata leakage. Require authenticated pairing and key binding, session-limited credentials, short session TTL, strict child-scoped guardian permissions, immediate live-stream termination on revoke, protected crash/diagnostic logs, bounded buffers, no automatic deferred uploads and deletion testing.

Madalasa must present **device-verified command reason and safe action** if audio/camera/files/screen access is unavailable; never tell an offline parent that a child sensor permission is definitely denied, and never leak another family's device state. Alarka main Activity normally stays closed after setup while identifiable monitoring notification and Android camera/microphone indicators remain. MediaProjection consent is fresh each session; real managed-device exception and OS lifecycle behavior require physical-device tests. See [MA-MEDIA-ADR-001](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md) and T-MEDIA-01–18. **No child media pilot/production enablement** until India legal, Play, security and device release gates pass.
