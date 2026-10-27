# Privacy Policy — Publication Draft (NOT READY TO PUBLISH)

> **Document control:** M9 / 02-public-legal-drafts · Proposed owner: Privacy counsel + owner (not assigned) · Registry: DRAFT_LEGAL_REVIEW_REQUIRED; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

> **Product names:** **Madalasa** (parent app), **Alarka** (child app). Desired repository name **Madalasa-Alarka** is **completed GitHub repository rename**. Use the verified new repository URL for all current documentation and integrations. [Naming rationale](../../M0-foundation-and-approvals/02-market-and-feasibility/BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | draft 2026-10-25**

> **LEGAL/PRODUCT REVIEW REQUIRED.** Every bracketed field and TBD must be completed before hosting as a public policy. Do not claim an implemented feature, encryption measure or deletion SLA until it is actually verified. This is a template for the intended product, not the live policy of an operating service.

## 1. Who operates Madalasa–Alarka?

Madalasa–Alarka is planned as a parental device-safety and monitoring service operated by **[LEGAL BUSINESS NAME]** (“we”). Contact us at **[PUBLIC SUPPORT EMAIL]**, **[BUSINESS ADDRESS / RELEVANT LEGAL CONTACT]**. Last effective date: **[PUBLICATION DATE]**.

The service is intended for appropriately authorized parents and guardians to supervise their children's devices. It is not intended for covert monitoring of adults or other unauthorized individuals.

## 2. Information the service may collect

We expect to process only data needed for features the parent has activated and the child device has been configured to support:
- Parent account details and authentication identifiers.
- Paired device identity, capability state, version, pairing and security logs.
- Location, collection timestamp and accuracy, optionally reported speed, to show current/recent location and travel history.
- App usage identifiers and duration for usage reports, after required Android special access is granted.
- Remote-control policies and authenticated command execution status.
- Diagnostic events needed for security/reliability **[LIST ACTUAL SDKs]**.
- Subscription and entitlement metadata; payment card information is expected to be handled by the payment provider, not by our backend.
- Photos/video/audio only if a separate transparently authorized, released feature permits their creation and transfer; **not a promise that such functionality will be offered**.
- Parent-authorized Google Drive information needed to back up selected permitted media.

For a final live version, specify **exactly** which items are collected, whether optional, and any new SDK data collection.

## 3. How information is used

We intend to use information to provide the parent's requested map/history and app-usage reports, execute supported authorized controls, operate pairing/security, provide paid entitlements, detect outages and abuse, and comply with applicable legal obligations. We will not present monitoring as hidden or claim unsupported device privileges.

## 4. Background location and device indicators

Where enabled and permitted, Madalasa–Alarka can collect location **when the setup screen is closed or the app is not actively open**, to provide parent-visible location and travel history. The child device may display a persistent monitoring notification or other Android privacy indicators, which Madalasa–Alarka will not conceal. Android settings may allow permissions to be revoked. Certain features may then stop working.

## 5. Who receives information?

The authorized paired parent account can view supported child-device reports. Selected authorized information may be processed by **[ACTUAL CLOUD/HOSTING PROVIDER]**, **[AUTH PROVIDER]**, Google services used for map/notification/billing/Drive purposes, and **[OTHER NAMED SUBPROCESSORS]** subject to appropriate terms. Describe cross-border transfers and legal jurisdictions at release. **Do not claim “no sharing” without checking Play's definitions and all SDK flows.**

## 6. Security

The planned system uses encrypted transport, authenticated access controls, revocable device credentials and appropriate encryption at rest. **These are target controls and must be verified on the production build** before this paragraph becomes public.

## 7. Retention and deletion

Planned retention periods: location **[X DAYS]**, app usage **[Y DAYS]**, optional media **[Z DAYS]**, audit logs **[AUDIT RETENTION]**, backups **[BACKUP POLICY]**. Actual operations must implement and test these dates.

Parents may revoke a device, disconnect Google Drive and request account/data deletion within the app or at **[PUBLIC ACCOUNT DELETION URL]**. Explain which billing/fraud/legal records are retained, for what legal basis and for how long. Deleting Madalasa–Alarka server data may not delete independently stored files in the parent's Google Drive; clarify and offer options.

## 8. Parental authority and child privacy

Only a person with the required legal authority should enroll a child's phone. Review regional consent/child privacy requirements before launch, including intended countries and age ranges **[TARGET JURISDICTIONS AND AGE POLICY]**. The child agent will have a recognizable identity and required disclosure and notifications.

## 9. Your choices

A parent may review enabled features, revoke pairing, manage the subscription, request deletion and revoke cloud integrations. Android permissions and some special-access settings can be changed in device Settings. Revoking access may prevent location or usage reports from updating.

## 10. Changes

We will update the policy and notify users where required if data handling or the feature set materially changes. Prior versions and effective dates will be archived **[POLICY VERSIONING PROCESS]**.

## Must-complete publication checklist

- [ ] Operator legal name/contact validated
- [ ] All SDKs and backend data recipients listed
- [ ] Actual retention and deletion behavior tested
- [ ] Play Data safety wording reconciled with collection
- [ ] In-app and store listing public privacy-policy links verified
- [ ] Child-specific disclosure, consent and legal review completed
- [ ] Account deletion web URL functional without requiring app install
- [ ] Accessibility/language review
- [ ] Public policy revised and approved by counsel

## 11. India child-data and US hosting publication blockers (2026-10-26)

**DO NOT PUBLISH as compliant terms or begin real Indian child-data collection yet.** The planned India-first product has unresolved India DPDP Act 2023 s.9 children's data processing and behavioural-monitoring prohibitions, Rule 10 adult parent consent mechanism, Rule 12 narrow real-time child-safety purpose exception, and section 16/Rule 15 US hosting transfer issues. Most provisions are phased toward approximately May 2027 under November 2025 Gazette; this timing is **not** blanket permission today. [Detailed primary-source legal gate](../../M0-foundation-and-approvals/03-legal-and-privacy/INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md).

Provider wording must list **Oracle OCI Chicago, United States** *if actually deployed there*, plus Google Maps/FCM/Billing, identity service and any SMS fallback/other processor with actual subprocessor purposes. Real age scope, adult/guardian verification, lawful collection purposes, each live-vs-history-vs-app-usage retention and legal transfer approval are **NOT DETERMINED**.

**Safe defaults:** no real child data in development; app-usage history and historical tracking disabled for minors pending signed counsel advice; owner-specific guardian invitations, purpose notices and erasure tests; never imply a Play permission or purchase proves parent authority. Publisher identity, support/grievance contact and real public deletion page remain blank until supplied. Retention 14/90/365/30 are engineering candidates, **not approved published dates**.



## Explicit app identities (2026-10-26)

**Madalasa** is the parent/guardian Android application and **Alarka** is the child-device companion. Final policy must disclose each app's actual information processing, monitoring permissions, third parties and rights separately. The draft is NOT approved or published; legal publisher, retention and India DPDP basis remain open.

## Internal media architecture option — not a published privacy policy (2026-10-26)

Owner accepted research of conditionally supported audio listening/recording, live camera/snapshot/video, per-session-consented screen viewing and authorized files. Proposed encrypted P2P/TURN transfer without **VPS media-file storage**, with optional encrypted Madalasa-local recording, is **not** a representation that the service does not collect/process/transmit personal media data. Any real release policy must disclose device capture, bystanders, endpoint storage and backup, transfer, processors/IP metadata, retention, deletion, who can access, purpose-specific child/guardian authority and indicators. Alarka Activity normally stays closed after setup while monitoring notification/system privacy indicators remain. No minor-media pilot or media marketing until counsel/Play/device/security signoff. [MA-MEDIA-ADR-001](../../P3-deferred-research/01-media-and-administrator-research/MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md).

## 2026-10-27 capability/permission metadata review (not publishable text)

A proposed first-run read-only hardware/OS compatibility scan may create sensitive or identifying **device model/API/sensor presence, device management mode, Android grants and their changes, report versions and timestamps**. These are personal-data-related metadata when linked to a child device/family; need purpose limitation, collection/retention schedules, access restriction, processor cross-border mapping, deletion and Play Data safety analysis before public wording. Scanning itself should not read/capture sensor media, private files, location or contacts. Capability upload occurs only after authenticated pairing and parent receives an authorized, redacted child-scoped projection; temporary pickup guardians have no implicit detailed sensor-state access.

"Permission granted" in a design is Android-observed status, **not** proof of current operational sensor access or legal processing approval. OS may terminate app on revoke so parent reports can be stale. New disclosure must truthfully cover how/when state updates, actual monitoring notification, optional purpose-by-purpose grants, and Android system controls; no promise that revocation is immediately reflected on parent screen. See [MA-CAP-ADR-002](../../M1-secure-platform-foundation/03-security-and-permissions/CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md). This policy remains an internal draft, not counsel-approved or published.

## 2026-10-27 proposed media activity metadata and administrator access-audit disclosures — legal draft only

If permission-compliant media features are ever legally released, proposed backend data collection includes child-linked **media activity metadata**, not media files: who requested activity, type (audio/image/video+audio/screen), request and verified session times/duration, viewed-only vs encrypted parent-local saved receipt, measured saved file bytes if available, network bytes separately and truthful Android/network failure reason. Parent-local recording may be deleted or backed up independent of VPS. Logs do not contain recording contents, image previews, filenames/paths or transcripts. Audited, case-authorized admin support/security lookups can reveal who reviewed the metadata and when; detailed named child lookups are exceptional.

All actual retention periods, purpose-specific lawfulness, DPO/privacy controls, family/child access rights, admin-access audit retention, backups and deletion/legal hold are **TBD for India privacy counsel and owner**. Do not claim instantaneous parent logging, unbreakable audit integrity or no collection of data simply because media binaries are absent. This is NOT a publishable policy and no real-minor media monitoring approval is implied. [Media Activity Audit ADR](../../P3-deferred-research/01-media-and-administrator-research/MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md), [Admin Console Specification](../../P3-deferred-research/01-media-and-administrator-research/ADMIN_PANEL_SPECIFICATION_2026.md).

## 2026-10-27 proposed GPS device-buffer/inbox/raw storage transparency text — NOT PUBLISHABLE

Accepted technical architecture [MA-INGEST-ADR-004](../../M2-location-collection/01-location-collection-and-ingestion/POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md) introduces up-to-48h **encrypted Alarka device-local unsent location cache** and a **temporary PostgreSQL inbox with raw device location coordinates**, followed by final raw PostGIS observations, derived movement histories and potentially backups/WAL. HTTPS JSON batches every 1–2min are a conditional networking target, not guaranteed last-known location freshness. A user should be told the actual collection/storage/disclosure periods for device-local queue, inbox, final raw routes and backups, which child/guardians can see, how offline data is uploaded later, and how deletion/revocation prevents reingest. UsageSessions are independently lawful-purpose and permission constrained. We must not tell users 'only one location data copy is stored' or '48h GPS always guaranteed'. Retention values, India children's lawfulness, storage region and Play disclosures remain unresolved and this is still a counsel-unapproved internal draft.
