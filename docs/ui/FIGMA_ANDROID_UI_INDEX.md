# Amar-Pola — Editable Figma Android UI Design

**Live Figma Design:** https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli

**Created:** 2026-10-26. **Status:** First-pass editable Figma screen designs, not a compiled Android application. Verified by reading back Figma document: **72 separate native Figma phone frames** — 24 Light, 24 Dark, 24 Battery Saver — each made of editable text, frames and individual card layers, not flat screenshots.

The 24 unique layouts consist of **12 parent** views (Welcome, Sign in with Google, Create account, Google identity handoff, Dashboard, Children, Child details, Child installation, Pair device, Permissions, Guardian access, Subscription and settings) and **12 child** views (visible welcome, device pairing, disclosures, location permission help, notification settings, battery help, health, offline queue, check-in, managed eligibility, transparency, settings). An overlap in the representative descriptions here is intentional: the Figma frame names are authoritative.

**Themes:** LIGHT = off-white/teal; DARK = charcoal/teal; BATTERY SAVER = muted cream/olive, reduced-update semantics. The design page groups all three modes and both roles because the authenticated Figma Starter workspace limits design files to three pages.

**Source traceability:** [SRS](../SRS.md), [Master milestones](../MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md), [tldraw full wireframe registry](tldraw/README.md). The existing tldraw board still holds **75 unique initial wireframe screens and 225 themed instances** and remains the broader coverage source. The native Figma file currently covers a **prioritized visual foundation**, not all 225 variants; broader transfer, production components/variants, tokens, and runnable Kotlin Compose remain future implementation work.

**Safety:** parent cannot silently grant permissions on the child phone. Indian minor historical routes and app-usage remain legally gated. Google account sign-in is not proof of adult guardianship. SOS check-in is not emergency dispatch.

**To edit:** open Figma; select a frame named `LIGHT / Parent / Welcome` or another screen; edit the text and cards independently. For Android implement with Material 3, Jetpack Compose Navigation, reusable Card/Buttons/PermissionCoach, state-driven OS capability reporting, and verified server-backed child permissions.

## 2026-10-26 Functional developer handoff — 81 distinct screens (current source of truth)

**Current primary Figma UI deliverable:** [Functional Handoff canvas — 81 screens](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=6-2) and [81-screen GitHub registry with per-screen implementation contracts](figma-functional-handoff/README.md). The latest user instruction is **one visual style**, not separate drawings per theme; developers will apply Light/Dark/Battery Saver through shared Jetpack Compose theme/state architecture. The original 72 light/dark/eco phone concepts in Figma's Page 1 and tldraw 225 instances are exploratory archives, not the current functional handoff.

The dedicated Figma page was **structurally read back**: exactly **60 parent (P-01–P-60)** + **21 child (C-01–C-21)** screen frames, zero missing/duplicate IDs, every screen with visible editable Android mockup AND developer implementation panel **directly beneath** specifying purpose, UI content, user action, backend/data, security/legal/OS gate, failure/empty/offline and acceptance check. Native Figma frame/text layers, not screenshot imports. [5 groups of structured JSON specs](figma-functional-handoff/README.md) plus the [renderer template](figma-functional-handoff/renderer-plugin-api.template.js) are committed for development and traceability.

**Caveat:** Figma Starter MCP tool-call allowance was exhausted during final screenshot validation, so visual polish/legibility review is still **PENDING**, even though full structural presence was confirmed. These are static editable designs, not Android code or functional prototypes.
