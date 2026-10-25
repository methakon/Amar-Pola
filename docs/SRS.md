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


## 11. Proposed feature feasibility and verification matrix

This is an initial engineering assessment, not a substitute for tests on the declared support matrix.

| Feature | Feasibility | Verification needed |
|---|---|---|
| Pairing without a separate child account | Feasible | Expiry, single use, revocation, and account authorization tests. |
| Background location and route history | Feasible with conditions | Background permission/service rules, OEM battery restrictions, offline recovery and location freshness. |
| Speed reporting | Feasible with conditions | Confirm speed availability/accuracy; show unavailable when missing. |
| App usage reports | Feasible with Usage Access | Verify onboarding, revocation, and daily through yearly aggregation. |
| Remote file listing | Partial | Limit to app-owned and explicitly accessible storage. |
| Remote app blocking | Conditional | Test ordinary mode separately from managed-device/device-owner policies. |
| Remote photo/video | Conditional, capability-gated | Test API level/device/enrollment; verify permissions, OS rejection, privacy indicators and status reporting. |
| Remote microphone recording | Restricted, needs validation | Verify supported authorized workflow and background restrictions; no guarantee of arbitrary remote activation. |
| Google Drive backup | Feasible | OAuth scopes, token revocation, retries, resumable uploads, and deletion behavior. |
| Subscription system | Feasible | Purchase verification, renewal, expiry, cancellation and server-side entitlement tests. |
| Low resource use | Target, not yet proven | Establish CPU/RAM/network/battery budgets and benchmark representative devices. |
| C++ backend | Feasible | Load, security, availability, recovery and operational tests. |

### Feasibility acceptance gate

Before release, each feature must have a supported Android/API/device/enrollment range and a recorded test result. Untested features must be marked **Not tested**, not assumed feasible. A remote command is successful only when the child agent confirms completion.

## 12. Requirements implementation and publication traceability

See [Implementation Technical Specification](IMPLEMENTATION_TECHNICAL_SPECIFICATION.md) for module responsibilities, API contract proposals and development milestones. [Feasibility Conditions and Evidence](FEASIBILITY_CONDITIONS_AND_EVIDENCE.md) records conditions for conditional requirements (FR-003, FR-005, FR-007, FR-008, FR-009 and FR-010). [Validation and Release Plan](VALIDATION_AND_RELEASE_PLAN.md) traces requirements to acceptance tests. [Google Play Publishing Requirements](GOOGLE_PLAY_PUBLISHING_REQUIREMENTS.md) captures publication gates and necessary declarations.

**Release gates:** Pass documented device tests; complete privacy/data safety and permissions review; no unsupported app blocking claims or covert media capture; ensure the release binary and its store disclosures match. The technical and publication docs do not represent implemented functionality.

## 13. New location, named-place and trip requirements (2026-10-25)

The full acceptance and design details for these requirements are in [Live Trip Route, Named Places and Battery Specification](LIVE_TRIP_ROUTE_NAMED_PLACES_BATTERY_SPECIFICATION.md).

- **FR-015 Named places (P1):** A parent shall add, edit, title, categorize, move and delete geolocated place markers for a paired child; labels shall appear near the observed position on the Google map without extra child location requests.
- **FR-016 Route history (P1):** The parent shall view chronological, timestamped observed location segments as Google Maps polylines. Coverage gaps and low-confidence segments shall be identified; fabricated directions routes shall not be represented as actual travelled paths.
- **FR-017 Trip and stops (P1):** The backend shall detect movement episodes, intermediate dwell stops, and start/end of observed trips; associate qualified stops with parent-saved places using spatial and accuracy-aware checks. Passing close to a place shall not automatically count as a visit.
- **FR-018 Adaptive battery profile (P1):** The child shall switch between stationary, movement and power-saving profiles based on available location/motion evidence and Android permission/service rules; target thresholds shall be measured on each supported device family.
- **FR-019 Conditional road geometry (P2):** Optional road matching shall be used only for sufficiently dense reliable vehicle tracks after third-party asset-tracking license, retention, pricing and policy checks. A raw-track fallback is mandatory.
- **FR-020 Multi-device location identity (P2):** Phone, tablet and Wear OS source observations shall retain separate device identity; no unverified stitching of tracks across devices.
- **FR-021 Place alerts (P2):** Optional enter/exit/dwell signals may use a limited, parent-selected set of Android geofences and must disclose delayed delivery and location uncertainty.

**New acceptance:** saved titled pins persist; observed route gaps are not bridged as though known; red-light pauses are not falsely counted as multi-minute stops; watch GPS absence is reported; parent map rendering does not itself increase child GPS sample frequency.

## 14. Cross-cutting adaptive tracking and scalable server requirements

See [Adaptive Movement and Multi-Tenant C++ Server Architecture](ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md) for the technical rationale, implementation steps and validation requirements.

- **FR-022 Multi-guardian privacy grants (P0):** Every parent/guardian action shall be authenticated and explicitly authorized for the exact family, child and device. Shared guardianship shall be revocable and audited.
- **FR-023 Durable GPS ingest (P0):** A child event shall be acknowledged only after durable server persistence; retries shall not duplicate events, stops or distance.
- **FR-024 Event-time reconstruction (P1):** Trip/stop analysis shall use observed timestamps, permit late/offline updates and publish versioned provisional/final/revised results.
- **FR-025 Server workload isolation (P0):** Child ingestion, C++ reconstruction, parent reads, usage aggregation and remote-command processing shall have separate bounded concurrency and service budgets.
- **FR-026 Parent viewing independent of sampling (P1):** Opening one or multiple map viewers shall not automatically multiply child location requests.
- **FR-027 Tenant-scoped data lifecycle (P0):** Device unpairing, guardian revocation, retention and account deletion shall invalidate authorization/caches and cover raw and derived history.
- **FR-028 Quality-aware trips (P1):** Stop/route data shall express accuracy, source device, time gaps and provisional/revision status; no invented travelled streets.
- **FR-029 Multi-device source attribution (P1/P2):** Phone/tablet/watch observations shall retain provenance and support explicit handoff policy.
- **NFR-009 Capacity and backpressure (P1):** Establish measured ingest, query, worker and DB SLOs using synthetic 1k/10k/100k device scenarios; enforce quotas and safe retries.
- **NFR-010 End-to-end access-control testing (P0):** Prevent object-level authorization leakage across families in API, RLS, caches, SSE and exports.

Current status: design and desk research only; no Android hardware measurements or server load tests have been run.
