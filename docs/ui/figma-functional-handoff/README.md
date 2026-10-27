# Madalasa–Alarka — Complete Android Functional UI Developer Handoff (Figma)

> **Current product:** **Madalasa** (parent app) + **Alarka** (child app); the GitHub repository is now **[Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka)**. [English mythological inspiration](../../BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**Last updated:** 2026-10-26  
**Main Figma file:** https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli  
**Dedicated Figma functional handoff page:** https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=6-2  
**Status:** **81 distinct editable mockups saved and read-back verified in Figma**. **Screen designs only**: real navigation/interactions, Kotlin Compose code and API handlers are NOT implemented. Screenshot-based visual QA could not be completed because this Starter Figma workspace exhausted its MCP tool-call allowance.

## Final scope and completion evidence

The actual Figma page was inspected programmatically after authoring. It contains **81 top-level named screen tiles**, **60 parent** (`P-01`–`P-60`) and **21 child** (`C-01`–`C-21`); exact expected IDs were all present, no duplicate IDs, and every tile has two separate native, editable descendant FRAME nodes:

1. `EDITABLE ANDROID SCREEN` / `ANDROID / Parent|Child` — a single-style mobile mockup built from Figma text, shapes, cards and a reusable action component.
2. `DEVELOPER IMPLEMENTATION DESCRIPTION BELOW SCREEN` / `DEVELOPER IMPLEMENTATION DETAILS` — a **visible panel directly below that specific phone** containing the implementation contract.

The page is one **functional visual style** only, as newly requested; developers will implement light/dark/battery-saver themes from shared tokens and app states. Older 72 initial light/dark/battery-saver sketches remain on `Page 1` solely for historical reference.

### Screen design coverage

| Functional source document | Figma IDs | Count | Coverage |
|---|---|---:|---|
| [01-parent-foundation.json](01-parent-foundation.json) | P-01…P-18 | 18 | Welcome/sign-in/Google, child install, pairing, guardian proof, child permission coach, device validation, home and basics |
| [02-parent-operations.json](02-parent-operations.json) | P-19…P-36 | 18 | Alerts, reliability, quality-aware map/history/trip revisions, named places, commute, gated app usage, device commands and managed schedules |
| [03-parent-governance-billing.json](03-parent-governance-billing.json) | P-37…P-54 | 18 | DPC eligibility, devices, guardian scopes/expiry/audit, retention/erasure, support packets, price and child-seat billing, outage and notifications |
| [04-parent-conditional.json](04-parent-conditional.json) | P-55…P-60 | 6 | Optional Google Drive/SAF, legally deferred camera/microphone, watch sources and schedule-aware sampling |
| [05-child-app.json](05-child-app.json) | C-01…C-21 | 21 | Child disclosure, code entry and Keystore proof, guardian verification, OS permissions, battery management, DPC, transparency, offline queue, check-in, SOS, revocation and re-enrollment |
| **Total** | **P-01…P-60 / C-01…C-21** | **81** | All functional handoff entries committed and reflected in Figma |

## Developer handoff fields under EVERY screen

The same structured content appears in GitHub JSON and in the Figma description panel beneath the relevant Android phone:

- **PURPOSE** — what this screen communicates.
- **UI CONTENT** — visible controls/status indicators.
- **USER ACTION** — the primary CTA and expected transition.
- **BACKEND / DATA** — M1 endpoint when available, or an explicitly future planned API/data flow.
- **SECURITY / OS / LEGAL GATE** — child-specific scopes, India DPDP, Android permission/DPC constraints and user consent.
- **ERROR / EMPTY / OFFLINE** — truthful states and recovery.
- **ACCEPTANCE CHECK** — a developer/QA-observable result.

Each JSON record additionally tracks `id`, `actor`, `milestone`, `fr`, `type` and `phase`.

### How to build screens in Jetpack Compose

Use the Figma mockup as a layout/UX reference and JSON as behavior/acceptance contract. Start with common components: `APTopBar`, `APButton`, `ScreenState`, `ChildStatusCard`, `PermissionStepCard`, `ReportedCapability`, `LastObservedLocationCard`, `EvidenceLegend`, `DeviceHealthRow`, `GuardianGrantChip`, `SOSAcknowledgement`, `FamilySeatCard`. Implement a typed navigation graph for Parent setup and Child setup, rather than duplicating screens for appearance variants.

Suggested screenshot-to-code workflow:
1. Choose exact screen ID (`P-09` secure pairing or `C-07` Android Location guide).
2. Inspect native Figma layers and the notes immediately below the screen.
3. Read the corresponding JSON record and linked SRS FR/M0–M9 milestone.
4. Build Compose layout, ViewModel and state flows; replace screen examples with real authorized data.
5. Add valid loading/error/offline/permission-denied/OS-rejected states.
6. Wire to actual approved backend or leave gated features disabled; test acceptance criterion on allowed devices.
7. Add dark/normal/eco via shared ThemeTokens / configuration, not duplicate business logic.
8. Verify cross-family access, revoked grants, logs, real OEM permissions and user-visible transparency before pilot.

### Critical safety and scope boundaries

- **No child-location or usage collection in prototypes for real minors** until the India DPDP purpose and actual guardian-verification gates are signed off. Real-time safety location exception does not automatically cover history or usage monitoring.
- **Google Sign-In identifies an account, not legal custody.**
- **The parent app cannot directly grant Android permissions** on the child's phone: it only explains the Settings steps and displays device-reported evidence.
- The DPC-only managed features need actual device-owner provisioning on an owner-approved safe-to-reset phone.
- FCM provider acceptance is not human acknowledgement or emergency dispatch; SOS reliable fallback is unimplemented.
- Camera/mic, Google Drive, file/media, optional watch and historical app-usage features remain conditional or disabled until individually approved.
- Current ₹50 monthly / ₹500 annual child-seat prices are proposed and depend on actual Play Console/tax.
- OCI Mumbai is the preferred future region, subject to tenancy, legal, finance and backup recovery verification.
- These mockups are native editable layers, **not working clickable prototypes nor an Android AAB**.
- **Visual QA is pending**: Figma tool-call quota blocked the final screen screenshot; individual frames and presence of implementation panels were programmatically read back successfully.

## Source and reproducibility

[Figma renderer template](renderer-plugin-api.template.js) creates editable phone + notes tiles via Figma Plugin API (requires existing local component IDs and page context); replacing `__SCREEN_DATA__` and `__BAND_Y__` with selected JSON enables scripted regeneration. The Figma file itself is the design authority. **The JSON contracts are version controlled but do not auto-sync to Figma** after edits.

Related:
- [Project SRS](../../SRS.md)
- [Master M0–M9 roadmap](../../MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md)
- [M1-only OpenAPI](../../openapi-m1.yaml)
- [India child-law gate](../../INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md)
- [SOS fallback](../../SOS_ESCALATION_AND_INDEPENDENT_DELIVERY_DESIGN.md)
- [Original tldraw inventory](../tldraw/README.md)


## Current app launcher names and unsynced Figma sample labels

All new Android launcher/app listing work should use **Madalasa** (parent) and **Alarka** (child) as the current brand names. Screen JSON sources provide per-screen role metadata; legacy Figma headings/screenshot layers still need a separate visual-edit pass when integration rate limits allow. Do not interpret historical rendered captions as published app names. Repository is now [Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka).

## Legal/Google Play feature flag status from October 2026 assessment

All 81 Figma screens remain useful **UX design specifications**, but the [Government / Legal / Google Play assessment](../../INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md) is the release gate. Alarka GPS/background location requires written Google Play eligibility under Families and qualified India counsel; route history, usage and behavioural insights default OFF; DPC controls lab-only; covert remote audio/video EXCLUDED; SOS only best-effort check-in until independently tested. **Do not implement a disabled mockup as a shipped permission or processing feature merely because its screen exists.**

## Conditional Media UI and HLD/LLD in Figma — 2026-10-26

**Actual Figma edit verified:** [Editable media HLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=21-3) and [editable command/media LLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=21-41) created on the new **ARCHITECTURE • Media HLD + LLD** page. They show Alarka closed-Activity / required visible indicators, verified consent and permission conditions, C++ Drogon signaling, WebRTC P2P first with encrypted TURN fallback, no VPS media file storage, optional encrypted Madalasa local recording, child-specific grants, command statuses and parent-visible reason codes. **These diagrams are R&D design, NOT device-proven or commercially approved.** The screenshots were rendered successfully through Figma.

Eight new editable prototype media screens are added on the existing Page 1, preserving its card-based visual style: [Media capability overview](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-2), [live audio](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-15), [camera](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-28), [unavailability reason](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-41), [screen-share consent](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-54), [encrypted connection/recording](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-67), [Alarka transparency](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-80), [Alarka session action](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-93). These eight are **additions to the pre-existing functional screens**, not proof all original 81 screens have been rebranded/rewired. Read [MA-MEDIA-ADR-001](../../MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md) for the authoritative feature/status/reason requirements. Do not ship media because a design exists.

**Eraser sync status:** the original eight separate Eraser HLD/LLD diagrams remain unmodified; Eraser rejected the requested AI updates because the connected workspace exhausted its free AI credits. The new media HLD/LLD therefore live as **editable Figma-native architecture frames**, rather than inaccurately claiming the Eraser originals have been updated.

## 2026-10-27 supplemental capability discovery and permissions UI — 46 editable screens

**Actually saved and structurally read back in the existing Figma file:** [Capability Onboarding • Alarka + Madalasa page](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=23-2), with **24 new Alarka A-01–A-24** and **22 new Madalasa P-01–P-22** mobile screens, each paired with a native editable **implementation/acceptance note immediately below**. This is a **supplement to** the preexisting 81-screen functional developer handoff (which retains its separate P-01…P-60 and C-01…C-21 IDs); the supplemental A-/P- screen IDs belong to the separate capability page, not the original 81-screen ID namespace. Do not claim the original functional JSON files or the original 81 frames were overwritten.

**Version-controlled node-by-node source:** [06-capability-onboarding.json](06-capability-onboarding.json). Covers first-install read-only hardware/sensors scan, pairing to family, supported vs unsupported/unknown features, staged permission disclosure, foreground then separate background location, notifications, Usage Access Settings, selected photos/SAF folders, P3 research microphone/camera explanation, managed-device DPC and per-session screen-share approval; OS granted/denied/partial/temporary results, server upload pending vs ACKed, setup completion, later revoke/reapprove, Alarka transparency, parent feature list, permission granted/operational conditional, network offline, stale report, version conflict, latest history, wrong/limited guardian and safe reapproval instructions.

**Related two native editable Figma architecture frames:** [Capability synchronization HLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=27-2), [Permission wizard, revocation and reliable states LLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=27-40). Requirements and test references: [MA-CAP-ADR-002](../../CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md), T-CAP-01…24. Status **DESIGN_ONLY/NOT_IMPLEMENTED/NOT_DEVICE_VERIFIED**, no runnable Android UI or actual permission prompts. The Figma drawings are illustrative and do not confer hardware/Android/Play permissions; Android system dialogs remain system-controlled.

## 2026-10-27 editable Media Activity History and Admin Console — 28 supplemental screens

**Actual Figma additions:** [Media Audit • Parent + Admin](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=32-2) holds **11 editable Madalasa Android history screens (PA-01…PA-11)** and **17 editable administrator browser screens (ADM-01…ADM-17)**, each with a native editable **DEVELOPER NOTES** panel directly below. This is **in addition** to the original 81 functional screens, 46 capability/permission screens and 8 earlier media R&D screens, not a replacement or deployed UI. All use sample guardian/child identifiers and design-only feature status.

**Parent:** [PA-01 Media History](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=32-3); child selector with names/masked IDs, date range, media/action/outcome/failure filter, cursor next/previous, viewed-only vs parent-local saved details, real OS error evidence, empty/offline/unauthorized and stable paging. **Admin:** [ADM-04 Media Activity Explorer](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=33-148); [ADM-03 case-based access request](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=33-98); parent/child name/ID autocomplete, date range, detail, failure, pagination, access audit, retention controls, expired/denied roles, exceptional export and audit-store fail-closed states. **Every admin detail read is case-scoped and independently audited**; no generic administrator can read all children.

**Two native editable architecture diagrams:** [media audit HLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=35-2), [media audit LLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=35-56) on existing architecture page. Source requirements: [FR-050/FR-051](../../SRS.md) and [media audit ADR](../../MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md), [admin console spec](../../ADMIN_PANEL_SPECIFICATION_2026.md); 22 planned audit tests and 14 admin tests. Exact node IDs and notes: [07-media-activity-audit.json](07-media-activity-audit.json). **DESIGN ONLY; no backend, web UI or Android navigation/actions are implemented**.

## 2026-10-27 accepted GPS 48h offline / Postgres durable inbox / bulk ingest architecture diagrams

Three native **editable** Figma system designs were added to the existing [architecture page](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=21-2):
1. [HLD · Alarka GPS local buffer → JSON batch → PostgreSQL inbox → C++ bulk workers → PostGIS/parent](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=41-2)
2. [LLD · inbox Tx A durable 202 / SKIP LOCKED worker / raw+dedup+outbox Tx B / crash recovery](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=41-60)
3. [Architecture tradeoff · durable inbox vs direct raw bulk INSERT / WAL & p95 benchmarks / no MVP Redis](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=41-126)

[Machine-readable node/coverage index](08-postgres-gps-batch-system-design.json) and [canonical owner acceptance ADR](../../POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md). These are **new diagrams**; pre-existing 81 functional app screens, 46 capability screens, 28 audit screens and eight Eraser diagrams were not overwritten. **NOT_IMPLEMENTED / NOT_TESTED / NOT PLAY OR INDIA CHILD-DATA APPROVED.**
