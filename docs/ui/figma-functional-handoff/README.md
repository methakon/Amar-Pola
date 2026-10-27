# Madalasa–Alarka — Complete Android Functional UI Developer Handoff (Figma)

> **Current product:** **Madalasa** (parent app) + **Alarka** (child app); the GitHub repository is now **[Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka)**. [English mythological inspiration](../../phases/M0-foundation-and-approvals/02-market-and-feasibility/BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

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
- [Project SRS](../../phases/M1-secure-platform-foundation/01-requirements-and-architecture/SRS.md)
- [Master M0–M9 roadmap](../../phases/M0-foundation-and-approvals/01-project-governance/MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md)
- [M1-only OpenAPI](../../openapi-m1.yaml)
- [India child-law gate](../../phases/M0-foundation-and-approvals/03-legal-and-privacy/INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md)
- [SOS fallback](../../phases/M4-usage-health-sos/01-usage-health-and-sos/SOS_ESCALATION_AND_INDEPENDENT_DELIVERY_DESIGN.md)
- [Original tldraw inventory](../tldraw/README.md)


## Current app launcher names and unsynced Figma sample labels

All new Android launcher/app listing work should use **Madalasa** (parent) and **Alarka** (child) as the current brand names. Screen JSON sources provide per-screen role metadata; legacy Figma headings/screenshot layers still need a separate visual-edit pass when integration rate limits allow. Do not interpret historical rendered captions as published app names. Repository is now [Madalasa-Alarka](https://github.com/methakon/Madalasa-Alarka).

## Legal/Google Play feature flag status from October 2026 assessment

All 81 Figma screens remain useful **UX design specifications**, but the [Government / Legal / Google Play assessment](../../phases/M0-foundation-and-approvals/03-legal-and-privacy/INDIA_GOVERNMENT_LEGAL_GOOGLE_PLAY_PROJECT_RISK_ASSESSMENT_2026.md) is the release gate. Alarka GPS/background location requires written Google Play eligibility under Families and qualified India counsel; route history, usage and behavioural insights default OFF; DPC controls lab-only; covert remote audio/video EXCLUDED; SOS only best-effort check-in until independently tested. **Do not implement a disabled mockup as a shipped permission or processing feature merely because its screen exists.**

## Conditional Media UI and HLD/LLD in Figma — 2026-10-26

**Actual Figma edit verified:** [Editable media HLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=21-3) and [editable command/media LLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=21-41) created on the new **ARCHITECTURE • Media HLD + LLD** page. They show Alarka closed-Activity / required visible indicators, verified consent and permission conditions, C++ Drogon signaling, WebRTC P2P first with encrypted TURN fallback, no VPS media file storage, optional encrypted Madalasa local recording, child-specific grants, command statuses and parent-visible reason codes. **These diagrams are R&D design, NOT device-proven or commercially approved.** The screenshots were rendered successfully through Figma.

Eight new editable prototype media screens are added on the existing Page 1, preserving its card-based visual style: [Media capability overview](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-2), [live audio](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-15), [camera](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-28), [unavailability reason](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-41), [screen-share consent](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-54), [encrypted connection/recording](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-67), [Alarka transparency](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-80), [Alarka session action](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=20-93). These eight are **additions to the pre-existing functional screens**, not proof all original 81 screens have been rebranded/rewired. Read [MA-MEDIA-ADR-001](../../phases/P3-deferred-research/01-media-and-administrator-research/MEDIA_CAPABILITY_PARENT_REASON_AND_RUNTIME_DECISION_2026.md) for the authoritative feature/status/reason requirements. Do not ship media because a design exists.

**Eraser sync status:** the original eight separate Eraser HLD/LLD diagrams remain unmodified; Eraser rejected the requested AI updates because the connected workspace exhausted its free AI credits. The new media HLD/LLD therefore live as **editable Figma-native architecture frames**, rather than inaccurately claiming the Eraser originals have been updated.

## 2026-10-27 supplemental capability discovery and permissions UI — 46 editable screens

**Actually saved and structurally read back in the existing Figma file:** [Capability Onboarding • Alarka + Madalasa page](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=23-2), with **24 new Alarka A-01–A-24** and **22 new Madalasa P-01–P-22** mobile screens, each paired with a native editable **implementation/acceptance note immediately below**. This is a **supplement to** the preexisting 81-screen functional developer handoff (which retains its separate P-01…P-60 and C-01…C-21 IDs); the supplemental A-/P- screen IDs belong to the separate capability page, not the original 81-screen ID namespace. Do not claim the original functional JSON files or the original 81 frames were overwritten.

**Version-controlled node-by-node source:** [06-capability-onboarding.json](06-capability-onboarding.json). Covers first-install read-only hardware/sensors scan, pairing to family, supported vs unsupported/unknown features, staged permission disclosure, foreground then separate background location, notifications, Usage Access Settings, selected photos/SAF folders, P3 research microphone/camera explanation, managed-device DPC and per-session screen-share approval; OS granted/denied/partial/temporary results, server upload pending vs ACKed, setup completion, later revoke/reapprove, Alarka transparency, parent feature list, permission granted/operational conditional, network offline, stale report, version conflict, latest history, wrong/limited guardian and safe reapproval instructions.

**Related two native editable Figma architecture frames:** [Capability synchronization HLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=27-2), [Permission wizard, revocation and reliable states LLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=27-40). Requirements and test references: [MA-CAP-ADR-002](../../phases/M1-secure-platform-foundation/03-security-and-permissions/CAPABILITY_DISCOVERY_PERMISSION_SYNC_ADR_2026-10-27.md), T-CAP-01…24. Status **DESIGN_ONLY/NOT_IMPLEMENTED/NOT_DEVICE_VERIFIED**, no runnable Android UI or actual permission prompts. The Figma drawings are illustrative and do not confer hardware/Android/Play permissions; Android system dialogs remain system-controlled.

## 2026-10-27 editable Media Activity History and Admin Console — 28 supplemental screens

**Actual Figma additions:** [Media Audit • Parent + Admin](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=32-2) holds **11 editable Madalasa Android history screens (PA-01…PA-11)** and **17 editable administrator browser screens (ADM-01…ADM-17)**, each with a native editable **DEVELOPER NOTES** panel directly below. This is **in addition** to the original 81 functional screens, 46 capability/permission screens and 8 earlier media R&D screens, not a replacement or deployed UI. All use sample guardian/child identifiers and design-only feature status.

**Parent:** [PA-01 Media History](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=32-3); child selector with names/masked IDs, date range, media/action/outcome/failure filter, cursor next/previous, viewed-only vs parent-local saved details, real OS error evidence, empty/offline/unauthorized and stable paging. **Admin:** [ADM-04 Media Activity Explorer](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=33-148); [ADM-03 case-based access request](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=33-98); parent/child name/ID autocomplete, date range, detail, failure, pagination, access audit, retention controls, expired/denied roles, exceptional export and audit-store fail-closed states. **Every admin detail read is case-scoped and independently audited**; no generic administrator can read all children.

**Two native editable architecture diagrams:** [media audit HLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=35-2), [media audit LLD](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=35-56) on existing architecture page. Source requirements: [FR-050/FR-051](../../phases/M1-secure-platform-foundation/01-requirements-and-architecture/SRS.md) and [media audit ADR](../../phases/P3-deferred-research/01-media-and-administrator-research/MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md), [admin console spec](../../phases/P3-deferred-research/01-media-and-administrator-research/ADMIN_PANEL_SPECIFICATION_2026.md); 22 planned audit tests and 14 admin tests. Exact node IDs and notes: [07-media-activity-audit.json](07-media-activity-audit.json). **DESIGN ONLY; no backend, web UI or Android navigation/actions are implemented**.

## 2026-10-27 accepted GPS 48h offline / Postgres durable inbox / bulk ingest architecture diagrams

Three native **editable** Figma system designs were added to the existing [architecture page](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=21-2):
1. [HLD · Alarka GPS local buffer → JSON batch → PostgreSQL inbox → C++ bulk workers → PostGIS/parent](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=41-2)
2. [LLD · inbox Tx A durable 202 / SKIP LOCKED worker / raw+dedup+outbox Tx B / crash recovery](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=41-60)
3. [Architecture tradeoff · durable inbox vs direct raw bulk INSERT / WAL & p95 benchmarks / no MVP Redis](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=41-126)

[Machine-readable node/coverage index](08-postgres-gps-batch-system-design.json) and [canonical owner acceptance ADR](../../phases/M2-location-collection/01-location-collection-and-ingestion/POSTGRES_DURABLE_INBOX_BULK_GPS_USAGE_INGESTION_ADR_2026-10-27.md). These are **new diagrams**; pre-existing 81 functional app screens, 46 capability screens, 28 audit screens and eight Eraser diagrams were not overwritten. **NOT_IMPLEMENTED / NOT_TESTED / NOT PLAY OR INDIA CHILD-DATA APPROVED.**


## Theme C selected by owner (2026-10-28)

Use [Theme C storybook & UI contract](../MADALASA_ALARKA_THEME_C_STORY_AND_UI_CONTRACT_2026.md) and [machine-readable Theme C mapping](09-theme-c-story-and-screens.json) for ST-01–ST-05 and P-05/P-15/P-24/P-28/P-39/P-48/P-58 samples. The existing 81 functional screen IDs, developer implementation descriptions and safety gates remain the legacy baseline; do not delete or replace them with flattened generative art. Introduce original folktale illustrations only as cropped decorative story assets; all UI text, buttons and cards must remain editable. Keep compact closable trial badge, prepaid-only billing, six-hour free visible history and conditional media release flags. Subsequent 81-screen migration needs coverage/visual verification; sample screens alone do not complete that migration.


## Verified Figma Theme C stage — 2026-10-28

**Actual editable Figma file:** [FUNCTIONAL HANDOFF • All Screens](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=6-2). **Readback QA:** original **81** P/C functional handoff tiles remain present; **14 NEW** Theme C phone frames added alongside them (5 story + 9 functional). Each uses Figma frame/auto-layout/text/shape controls; story panels embed **five Figma AI-generated original illustrations as image fills only**, with text/buttons separately editable; assets have dedicated off-screen positions on archival Page 1. The new sample UI is STATIC, navigation/close/toggles are not runnable, and no backend/Android implementation is implied. Screen heights fit 390×844 with no detected vertical content overflow. English screen headers are editable Figma text; Android typography and contrast need device validation. Future localization remains a separate scope.

**Story links:** [ST-01 teaching](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=46-164) · [ST-02 Alarka](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=46-177) · [ST-03 ring](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=46-190) · [ST-04 remembrance](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=46-203) · [ST-05 wisdom](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=46-216).

**Functional links:** [P-05 home/map](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-164) · [P-15 timeline](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-192) · [P-24 trip](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-212) · [P-28 places](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-237) · [P-39 family](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-263) · [P-48 prepaid](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-281) · [P-58 audio gate](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-303) · [P-31 usage gate](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-317) · [C-02 child disclosure](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=52-337).

[Exact machine-readable 14-screen node IDs and implementation association](09-theme-c-story-and-screens.json). Original `Po5FqFQQIfttFLrjO5qqvE` trial-design file is an earlier styling exploration, now superseded by this Theme C stage, not deleted. **Still required:** real map provider tiles/attribution, device integration, reusable Compose components, Android feature tests, bilingual QA, true dismissal/countdown behavior, Play prepaid offers, legal/security review, and systematic restyling of remaining 81 handoff screens.


**Final Theme C visual-integrity note (2026-10-28):** In addition to the 14 NEW themed sample frames, the *existing* P-01 welcome, P-05 dashboard and P-48 checkout phone frames received a non-destructive parchment/vermillion palette adjustment in-place; their accompanying developer handoff panels were preserved. Original 81-screen functional tile count remains 81. Figma readback found no vertical overflow in the new 14 390×844 frames. New dashboard and story-ending screenshots reviewed after the edits; artwork is contained within illustration slots, not flattened over editable interface elements. Remaining legacy frames await systematic migration and device/functional QA.



## Authoritative owner correction — 2026-10-28 (overrides any earlier regional/language wording)

**Source & visual identity:** Madalasa and Alarka belong to the **Mārkaṇḍeya Purāṇa** narrative, part of a pan-Indian Sanskrit Puranic tradition. Do **not** describe the narrative or the project's theme as a Bengali regional folk tale, or position regional patachitra as its required style. Chosen Theme C means an **original pan-Indian Puranic illustrated storybook**—classical manuscript/miniature/mural influences without claiming historical authenticity or monopolizing any one regional tradition. Original lotus, ring, tree and court/forest motifs are optional decorative inspiration; all monitoring UI remains modern and clear.

**Launch language is ENGLISH ONLY:** English headings, body copy, app controls, trial/banner, billing, child transparency and story pages. **No Bengali script and no language selector** in current prototype/release screens. Future multilingual enhancement remains planned technically (resource-keyed UI strings, flexible components, Unicode/font fallback, locale-safe dates/numbers, translation QA), but translated screens/content must not be implied ready or implemented.

**Preserve the user-provided screenshots and prior feature discussion:** See [reference workflow register](../REFERENCE_SCREENSHOTS_FEATURE_WORKFLOWS_2026.md) (relative link should be resolved from docs/ui when applicable). These supplied third-party screenshots are **functional references only**, capturing map/satellite style selection, collapsible/expanded dashboard, parent/child enrollment, place-specific toggles, timeline, route segments, quota-based sound, usage charts and managed-only restrictions. Copy neither imagery nor exact UI. Do not treat inferred third-party capabilities as certified Madalasa features.


## Superseding design clarification — 2026-10-28

Theme C now means an **original, pan-Indian Markandeya Purana–inspired illustrated storybook**, NOT a Bengali regional folk theme. **English-only screens at launch**: story headings/body, trial notices, map, family, billing, child transparency and controls. No Bengali text or language chooser in current UI; plan future internationalization using external strings, flexible layout, Unicode/font fallback and professionally reviewed translations. Screenshot workflow requirements remain retained in [Reference Screenshot Functional Workflow Register](https://github.com/methakon/Madalasa-Alarka/blob/main/docs/ui/REFERENCE_SCREENSHOTS_FEATURE_WORKFLOWS_2026.md): live map/map style, collapsible quick actions, family enrollment, per-place toggles, route and activity timelines, usage reporting, quota media UI and gated managed controls. The user-supplied screenshots inform behavior, never copied art/icons/layout or promises of restricted capabilities. Existing legal/Android/Play and prepaid gates unchanged.


### Verified visual correction — English-only pan-Indian Markandeya Purana theme (2026-10-28)

Actual Figma story frames ST-01–ST-05 now display **English headings, subtitles, body and controls only**, with no language chooser. Five distinct **original pan-Indian classical Puranic** illustrated scene assets replace the previous regional treatment; the superseded regional art asset frames are hidden/archived (not used in active story panels). All story controls and text are still separate, editable Figma layers. Original 81 functional handoff tiles and nine new Theme C function-screen samples remain, not completed Android code. The source narrative is the **Markandeya Purana** and should never be described as Bengali regional folklore. Future multilingual support remains an architecture requirement only—no translated UI is release-ready.

**The user's reference screenshots remain integral to the functional design**, not visual templates. [Read the screenshot workflow register](https://github.com/methakon/Madalasa-Alarka/blob/main/docs/ui/REFERENCE_SCREENSHOTS_FEATURE_WORKFLOWS_2026.md) for map/map styles, child status, expandable map sheet, add-guardian/child, per-place notifications, activity and route timelines, minute-metered audio, usage reports and managed-only app controls. These are inferred UI workflows; feature availability continues to require separate Android/Google Play/legal testing.


## 2026-10-28 — Two parents, one child payment; select paid children (supersedes conflicting assumptions)

**Owner working decision:** one verified prepaid **paid child entitlement** may be used by *both separately signed-in, explicitly authorized parent accounts* within the same Madalasa family. Second parent does **not** buy a second plan for the same child. Primary billing adult selects which child IDs are covered by N paid seats; nonselected siblings stay on free features. Permissions remain scoped per adult-child grant, shared quotas meter per child across both parents, and co-parent access is revoked independently of purchase. One family is counted once for first-1,008 founding-family eligibility. Prepaid/manual renewal only, no auto debit; when expired both parents revert to the child's free tracking/reduced frequency/six-hour visible history. Other rules unchanged.

**Google verification:** [Family Link supports a second adult parent](https://support.google.com/families/answer/7295768) but does NOT automatically authorize Madalasa or expose a verified public parent-relationship API to this app. [India does not support new Play Family Library/family payment signups](https://support.google.com/googleplay/answer/16719923), and [family payment methods exclude subscriptions](https://support.google.com/googleplay/answer/15775614). Google Play purchases stay with the paying Play account; backend verifies and binds unique purchase tokens to family capacities/child entitlements, NOT guardian devices. [Play prepaid add-ons are unavailable](https://developer.android.com/google/play/billing/subscription-with-addons) because add-ons are currently auto-renew-only. Play Console sandbox must prove suitable N-seat prepaid SKUs, explicit seat reassignment, upgrades, top-ups and founding offers before any launch pricing promise.

**Canonical implementation design:** [Two-parent Shared Child Entitlements and Seat Selection](https://github.com/methakon/Madalasa-Alarka/blob/main/docs/phases/M7-commercial-integrations/01-commercial-plans-and-costing/TWO_PARENT_SHARED_CHILD_PREPAID_ENTITLEMENTS_2026.md) (use an appropriate relative path from each document). Figma added [P-47 family child seats](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=81-179) and [P-49 covered by family](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=81-201), editable mockups only. Media and other restrictive Android features remain gated.


## Updated Figma portrait branding + co-parent seat assignment — 2026-10-28

**New active portrait symbols:** [Parent Madalasa face](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=68-164), [Child Alarka face](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=68-173), [website combined faces](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=68-179). Authentic Puranic likenesses do not exist in the verified book text, so these are original interpretations, not retrieved book images. Current English-only UI remains unchanged. [Portrait asset/Play release register](https://github.com/methakon/Madalasa-Alarka/blob/main/branding/CHARACTER_PORTRAIT_LOGOS_2026.md). New Figma [P-47 child coverage selection](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=81-179) and [P-49 covered co-parent](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=81-201) demonstrate two verified parents sharing one paid child entitlement and the payer selecting paid children. This is a design contract, not implemented Android functionality. [Shared prepaid parent/child seat specification](https://github.com/methakon/Madalasa-Alarka/blob/main/docs/phases/M7-commercial-integrations/01-commercial-plans-and-costing/TWO_PARENT_SHARED_CHILD_PREPAID_ENTITLEMENTS_2026.md). Google's Family Link second-parent support is distinct from Google Play Family Library, which is unavailable for new signups in India.
