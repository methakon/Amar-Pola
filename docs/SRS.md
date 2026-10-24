# Software Requirements Specification (SRS)

- **Version:** 0.1
- **Date:** 2026-10-25
- **Status:** Draft baseline

## 1. Purpose

Define initial software requirements for Amar-Pola, a parent-supervised Android monitoring and device-management platform. This draft must be validated against target Android releases, device behavior, applicable law, and distribution rules before production release.

## 2. Scope

The system includes:
- Child-side Android agent with C++ core and Kotlin/Java platform integration.
- Parent app/dashboard.
- C++ backend API and command service.
- Database, auditing, and optional Google Drive integration.
- Subscription-entitlement validation.

### Out of scope

- Bypassing Android permission or privacy safeguards.
- Hidden/covert audio or camera capture.
- Universal third-party app blocking on unmanaged phones.
- Access to arbitrary private app data or protected system files.
- Guaranteeing location when the OS, hardware, network, or user settings prevent it.

## 3. Roles

- **Parent/guardian:** pairs devices, configures permissions and policies, views reports, authorizes integrations, and manages retention/subscription.
- **Child device user:** uses the phone on which the agent is installed; OS permission prompts and indicators remain applicable.
- **Service operator:** maintains backend availability, security, billing integration, and incident response.
- **Authorized support/security staff:** handles support and security events under least-privilege access.

## 4. Assumptions and constraints

- Parent has authorization to configure the device.
- Capabilities vary by Android API level, OEM, permission state, app lifecycle, and management mode.
- Background location and Usage Access require the relevant grants/configuration.
- Camera/microphone access is subject to runtime permissions, service/lifecycle constraints, and privacy indicators.
- Device-owner/device-policy features require supported provisioning and are not implied by ordinary installation.
- Connectivity is intermittent; local buffering is required.
- Google Drive requires explicit parent OAuth authorization and suitable scopes.
- Google Play distribution, if chosen, requires policy review.

## 5. Functional requirements

Priority: **P0** foundational; **P1** first useful release; **P2** later/conditional.

### FR-001 Secure device pairing (P0)
The system shall pair a child device to a parent account using a short-lived, single-use code or equivalent secure enrollment.
- A separate child username/password is not required for the baseline.
- Codes shall expire, be rate-limited, and be single-use.
- Device credentials shall be unique and revocable.

### FR-002 Permission onboarding (P0)
The child app shall explain relevant permissions and guide the parent through runtime and special-access settings.
- It shall report current permission/capability state.
- It shall detect revoked/unavailable permissions and show degraded status.
- It shall not claim that initial setup removes OS restrictions.

### FR-003 Location collection (P1)
When permitted, the child agent shall collect location fixes with timestamp, latitude, longitude, accuracy, and optional speed/bearing/altitude when available.
- Respect background-location and foreground-service rules.
- Use adaptive sampling based on motion/policy.
- Expose location age and reported accuracy.

### FR-004 Travel history (P1)
The parent client shall show historic points and routes within the configured retention period.
- Gaps in data shall remain visible.
- Missing observations shall not be presented as actual recorded points.

### FR-005 App-usage reports (P1)
After Usage Access is granted, the agent shall collect available usage statistics through supported Android APIs.
- Parent reports shall cover daily, weekly, monthly, and yearly periods.
- UI shall explain data limitations where Android does not expose expected information.

### FR-006 Authenticated remote commands (P1)
The backend shall accept and deliver authorized commands to a paired device.
- Each command shall include unique ID, actor, target device, creation time, expiry, type, and status.
- Child agent shall reject expired, duplicate, unauthorized, and unsupported commands.
- Results shall accurately distinguish queued, delivered, completed, failed, unsupported, permission-required, OS-rejected, and user-action-required states.

### FR-007 App restrictions (P1/P2)
The parent client shall configure restrictions supported by the active device mode.
- Standard mode shall not claim universal prevention of other apps launching.
- Managed mode may use supported device-policy APIs after valid provisioning.
- Policies shall define target package, schedule, time zone, desired state, and policy version.
- The system shall report whether each policy is enforceable on the device.

### FR-008 File access (P2)
The agent may list or transfer files in app-owned storage or locations where appropriate access has been granted. It shall not claim access to arbitrary private app data or protected files.

### FR-009 Photo/video request (P2; capability gated)
The parent client may request photo/video capture only where a tested, authorized workflow is supported.
- Backend shall check reported OS/API level, app version, enrollment mode, and last-known capability profile before dispatch.
- Child agent shall revalidate permission and current OS/service constraints immediately before execution.
- If unsupported or rejected by Android, a specific failure state shall be returned.
- Operation is complete only after media creation and persistence are confirmed.
- The implementation shall not bypass privacy indicators or OS safeguards.

### FR-010 Audio recording (P2; capability gated)
Any audio feature shall use a supported, authorized workflow and respect runtime permissions, background microphone restrictions, and privacy indicators.
- Product shall not promise unrestricted remote activation.
- User-action requirements and failures shall be reported.

### FR-011 Parent-authorized Drive backup (P2)
Parent shall authorize Drive through OAuth.
- Only selected/authorized media shall be uploaded.
- Tokens shall be securely stored and revocable.
- Upload progress, retries, and errors shall be recorded.
- Use resumable uploads where supported for large files.

### FR-012 Subscription entitlement (P1 for commercial release)
Backend shall validate entitlement through a trusted billing integration.
- Local client state alone shall not grant paid access.
- Handle renewal, expiry, cancellation, grace period, and revocation according to provider rules.

### FR-013 Privacy controls (P0)
Parent shall be able to review and revoke paired devices, disconnect integrations, request deletion, and configure retention within product policy.
- Sensitive actions shall be audit logged.
- Access shall be limited to authorized parent accounts.

### FR-014 Status and alerts (P1)
System shall expose configured alerts for connectivity loss, stale location, permission revocation, failed commands, and subscription state.
- Lock-screen notifications shall avoid unnecessary sensitive location/media details by default.

## 6. Non-functional requirements

### NFR-001 Battery
Use adaptive location sampling, batched network transfer, and bounded background work. Measure drain on representative devices; make no universal battery-life promise before testing.

### NFR-002 CPU and memory
Avoid busy loops, tight polling, and unbounded queues. Define numeric budgets after selecting target devices.

### NFR-003 Reliability
Local queue shall survive process restarts and transient network failure. Use idempotency and deduplication for commands/uploads.

### NFR-004 Security
Use TLS, avoid secrets in mobile binaries, and validate authorization server-side for every sensitive operation.

### NFR-005 Privacy
Minimize collection, document retention/deletion, and protect data access. Avoid logging raw sensitive payloads.

### NFR-006 Compatibility
Maintain a tested matrix by Android API level, OEM behavior, permission state, and standard/managed mode.

### NFR-007 Usability
Clearly distinguish live, stale, approximate, unavailable, and failed states. Permission setup must explain why access is needed.

### NFR-008 Maintainability
Separate Android platform integration, shared C++ core, backend, parent interface, and provider integrations behind documented interfaces.

## 7. External interfaces

- Android location and foreground-service APIs.
- UsageStatsManager / Usage Access settings.
- DevicePolicyManager in valid managed mode.
- Google Maps SDK/API.
- Google Drive API with parent OAuth.
- Billing-provider APIs.
- HTTPS APIs between child, parent, and backend.

## 8. Logical data requirements

- Parent identity/authentication references.
- Device enrollment, capability profile, permission state, and revocation.
- Location point: device, observed time, coordinates, accuracy, optional motion fields.
- Usage aggregate: package, interval, duration, collection time.
- Policy: target package, schedule/time zone, mode, state, version.
- Command: ID, actor, target, type, expiry, status, reason/result, timestamps.
- Media metadata: type, size, checksum, authorization context, upload state, optional Drive reference.
- Subscription entitlement/provider reference.
- Audit event and retention/deletion state.

Sensitive data shall be minimized and encrypted. Credentials and OAuth tokens must not be written to ordinary logs.

## 9. MVP acceptance criteria

1. Securely pair and revoke a test device.
2. Accurately reflect granted, denied, and revoked permissions.
3. Queue and synchronize timestamped location events without duplicate records.
4. Map shows location age/accuracy and makes gaps visible.
5. Usage reports are available only after required access is granted.
6. Every remote command has truthful status and reason codes.
7. Unsupported capture requests are rejected or require user action; they are never marked successful falsely.
8. Managed restrictions are tested on a properly provisioned device and not advertised as standard-mode behavior.
9. Sensitive endpoints enforce object-level authorization and produce audit events.
10. Tests cover offline recovery, duplicate commands, expiry, permission loss, and authorization failures.

## 10. Risks

- API/OEM variations in background execution.
- OS battery optimization delays.
- Device-owner setup complexity and possible enrollment/reset requirements.
- Distribution policy review.
- Elevated security/privacy risk from location and media.
- Third-party OAuth and billing token lifecycle/dependency risks.
