# Data Safety and Permission Inventory — Working Worksheet

> **Current product:** **Madalasa** (parent app) + **Alarka** (child app); the GitHub repository is now **[Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka)**. [English mythological inspiration](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Madalasa–Alarka | Draft | 2026-10-25**

**Do not submit these rows verbatim to Play Console.** Final declarations must be taken from the actual compiled parent and child apps, included SDKs, endpoints, storage behavior, and third-party recipients. Fill one worksheet **per package** and **per release track**. “Potentially collected” does not mean an enabled shipped feature.

## 1. Data inventory

| Data type | Collection source | Why needed | Recipient/storage | User control | Play disclosure review |
|---|---|---|---|---|---|
| Parent account identifier and email | Parent authentication | Pairing, account access, support | Auth provider and backend | Account deletion | Personal info / account |
| Child device identifier and app version | Enrollment | Pairing, support and security | Backend | Unpair/delete | Device or other IDs |
| Precise/approximate location and time | Child location API | Map and route history | Backend and authenticated parent | Turn off/revoke, retention/delete | Location; determine precise/approximate |
| Travel speed and movement | Location provider | Trip report | Backend and parent | Retention/delete | May be derived from location |
| App package usage duration | UsageStatsManager | App usage report | Backend and parent | Usage Access revoke, delete | App activity |
| Installed app package inventory | Scoped package query, only if feature ships | Configure app limits | Backend if transmitted | Disable feature/delete | App info/activity |
| Policy and command/audit metadata | Parent + child | Controls and security | Backend | Retention and deletion | App activity/device metadata |
| Crash logs/performance telemetry | Optional diagnostics SDK | Reliability | Backend or named vendor | Diagnostics preferences | App performance / device IDs |
| Authorized photos/videos | Only if a released media feature works | User-approved media backup | Backend temporary storage/Google Drive | Feature-specific delete | Photos/videos |
| Authorized audio | Only if a released audio feature works | Explicit approved recording | Backend/Drive if chosen | Feature-specific delete | Audio files |
| Subscription purchase token/entitlement | Play Billing backend verification | Entitlement and fraud prevention | Billing provider/backend | Account support/delete subject to legal retention | Purchases/financial category review |
| Drive OAuth token reference | Parent Google consent | Upload access | Encrypted secret store | Revoke integration | Authentication/integration data review |
| Push token | FCM if enabled | Wake/sync hints | Google FCM and backend | Re-pair/revoke | Device identifiers/SDK review |

## 2. Column-by-column Play Console investigation

For **every** shipped data category answer and document:
1. Collected from device? Transmitted off device? Stored only ephemerally? (Follow current Play definitions.)
2. Is transfer encrypted in transit?
3. Is collection required for core function or optional?
4. Purposes: app functionality, analytics, fraud prevention/security, account management, personalization or other (choose only truthful purposes).
5. Shared with whom? Evaluate processors/service providers and parent recipients using Play's official sharing definitions.
6. Is deletion request supported? Exact process and retention exceptions?
7. Is the feature on in the child package, parent package, both, or neither?

## 3. SDK/processors register (unresolved)

| Processor/SDK | Planned reason | Status | Before release |
|---|---|---|---|
| Google Maps SDK | Parent map | Planned, not integrated | Review data handling / Android SDK policies |
| Google Play services location | Child location | Candidate, not integrated | Audit services and data transmissions |
| Firebase Cloud Messaging | Command wake signals | Optional, not integrated | Audit SDK and registration tokens |
| Google Play Billing | Paid digital access | Planned | Audit purchase metadata and SDK data |
| Google Drive API | Parent media backup | Planned | OAuth scope and token storage review |
| Authentication provider | Parent sign-in | TBD | Name actual operator and vendor |
| Crash reporting | Reliability | TBD | Off by default in specification until selected |
| Hosting/database provider | Telemetry storage | TBD | Region, DPA, access and retention |

## 4. Permission mapping to function

| Permission/privilege | Required? | Feature | Review task |
|---|---|---|---|
| Fine/coarse location | Candidate P1 | Latest position, routes | Runtime prompt and disclosure |
| Background location | Candidate P1 | Background tracking | Separate grant + Play permission form/video |
| FGS location | Candidate P1 | Running location service | FGS declaration and notification |
| Usage Access | Candidate P1 | App usage history | Settings onboarding, revocation |
| POST_NOTIFICATIONS | Candidate | Status and monitoring notification | Permission state and required visibility |
| Device owner | Optional managed mode | App suspension | Managed enrollment + separate review |
| Camera | Deferred | Approved capture only | Feature not in manifest if not shipped |
| Record audio | Deferred | Approved capture only | Feature not in manifest if not shipped |
| Broad package visibility | Avoid by default | App discovery | Justification and Play permission form if requested |
| Read arbitrary private files | Not supported | None | Do not request or promise |

## 5. Retention and security blanks (must complete)

- Default location retention: **TBD**
- Default usage retention: **TBD**
- Media retention and Drive copy ownership: **TBD**
- Audit/security logs retention: **TBD**
- Backup deletion lag: **TBD**
- Primary hosting region: **TBD**
- Company/controller legal name and contact: **TBD**
- Subprocessors and DPAs: **TBD**
- Whether encryption covers all endpoints and backups: **Requires verification**
- Deletion request completion SLA and legal exceptions: **TBD**
- Parent authentication and age/authority verification policy: **TBD**

## 6. Final signoff record template

```text
Release version:
Package:
Build SHA / manifest SHA:
All runtime permissions verified: [ ]
SDK inventory verified: [ ]
Data category rows reconciled with network traffic: [ ]
Retention and deletion measured: [ ]
Public privacy policy URL verified: [ ]
Account deletion web URL verified: [ ]
Play Data safety responses saved:
Reviewer / approval:
Date:
```

## Source

https://support.google.com/googleplay/android-developer/answer/10787469

https://support.google.com/googleplay/android-developer/answer/13327111

https://support.google.com/googleplay/android-developer/answer/9859455

## India child data and cross-border review gate — 2026-10-26

The India-first deployment plans OCI Chicago (United States); do not answer Google Play Data Safety as if every child's information remains in India. Legal publisher/contact and purpose-by-purpose Indian DPDP Act s.9, Rule 10/12 (real-time safety exception **not blanket monitoring exemption**), section 16 transfer and retention are still undecided. Child historical GPS, app-usage/behavioural monitoring, guardian invitations and SOS messages need separate documented purpose and processor review before category declarations. Google Maps/FCM, Play Billing, parent login and optional SMS/Drive must be classified by **actual integrated SDK data flows**, not architectural possibilities.

Reference: [Indian minor privacy and Chicago legal gate](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md), [Privacy Policy Draft](PRIVACY_POLICY_DRAFT.md). Until adult parent identity verification, lawful-processing opinion and signed product scope exist, **do not collect real child data** or claim a completed Data Safety form.



## Package-specific naming

Prepare separate actual Google Play Data Safety submissions for **Madalasa** (guardian Android package) and **Alarka** (child companion), matching SDK/API behavior and declared purpose. Repository rename does not change applicationIds or publisher account identifiers automatically.

## 2026-10-26 proposed P2P media flow and parent explanations (research only)

The owner accepts conditionally feasible live audio/recording, remote camera/snapshots/video, MediaProjection consent per session, and scoped file/media access as **technical research**. A possible architecture encrypts capture on Alarka, sends direct P2P or via encrypted TURN, stores **no media files on VPS**, and optionally encrypts recordings on Madalasa. The **actual eventual released** Data safety inventory must still include capture/transmission, signaling/IP/session metadata, child disclosure and permission scope, device storage and backups, optional Google Drive transfers and subprocessors. No VPS media archive does **not** mean no collection or processing. Public disclosures require evidence of the delivered architecture.

Parent sees actual device-verified `Command.status + reason_code` for unavailable operation, including revoked media grant, permitted sensor context absent, or child screen-share consent needed. Alarka Activity normally closes after setup but monitoring notification and OS indicators remain visible. Commercial CAMERA/RECORD_AUDIO/MediaProjection permissions remain disabled/not included unless later approved by India legal, OS/OEM, security and Google Play gates. Reference: [MA-MEDIA-ADR-001](MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md).

## 2026-10-27 permission and capability metadata inventory (planning only)

Initial Alarka scan may create **device compatibility metadata** (model/manufacturer/API, reported camera/microphone/GPS support, permission and special-access states, managed role, last verified timestamp, selected-media *scope type* without filenames). Store only an allowlisted, minimum required subset **after device pairing**, not a hardware advertising/fingerprinting dossier. Authentication/signaling metadata and permission change history are potentially personal data and require data-category purpose/retention, rights/deletion, cross-border subprocessor and accurate Google Play Data Safety analysis. Raw media, sensor readings or child location should **not** be collected during scan. Child phone/parent phone/server each sees only authorized report projection; temporary pickup viewer should not automatically gain detailed sensor metadata.

OS grants remain in Android, **not** stored or conferred as permission tokens by Madalasa/VPS. Device authenticated snapshots + version/received timestamps are server data, permission revocation history requires bounded retention and restore-safe deletion. Negative statuses, selected-photo subsets and per-session MediaProjection approvals must be truthful. [MA-CAP-ADR-002](CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md). All protected child feature processing remains gated by counsel/Play; no real-minor media authorization implied.
