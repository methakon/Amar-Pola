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
