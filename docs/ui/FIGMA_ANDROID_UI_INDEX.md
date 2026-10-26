# Amar-Pola — Editable Figma Android UI Design

**Live Figma Design:** https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli

**Created:** 2026-10-26. **Status:** First-pass editable Figma screen designs, not a compiled Android application. Verified by reading back Figma document: **72 separate native Figma phone frames** — 24 Light, 24 Dark, 24 Battery Saver — each made of editable text, frames and individual card layers, not flat screenshots.

The 24 unique layouts consist of **12 parent** views (Welcome, Sign in with Google, Create account, Google identity handoff, Dashboard, Children, Child details, Child installation, Pair device, Permissions, Guardian access, Subscription and settings) and **12 child** views (visible welcome, device pairing, disclosures, location permission help, notification settings, battery help, health, offline queue, check-in, managed eligibility, transparency, settings). An overlap in the representative descriptions here is intentional: the Figma frame names are authoritative.

**Themes:** LIGHT = off-white/teal; DARK = charcoal/teal; BATTERY SAVER = muted cream/olive, reduced-update semantics. The design page groups all three modes and both roles because the authenticated Figma Starter workspace limits design files to three pages.

**Source traceability:** [SRS](../SRS.md), [Master milestones](../MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md), [tldraw full wireframe registry](tldraw/README.md). The existing tldraw board still holds **75 unique initial wireframe screens and 225 themed instances** and remains the broader coverage source. The native Figma file currently covers a **prioritized visual foundation**, not all 225 variants; broader transfer, production components/variants, tokens, and runnable Kotlin Compose remain future implementation work.

**Safety:** parent cannot silently grant permissions on the child phone. Indian minor historical routes and app-usage remain legally gated. Google account sign-in is not proof of adult guardianship. SOS check-in is not emergency dispatch.

**To edit:** open Figma; select a frame named `LIGHT / Parent / Welcome` or another screen; edit the text and cards independently. For Android implement with Material 3, Jetpack Compose Navigation, reusable Card/Buttons/PermissionCoach, state-driven OS capability reporting, and verified server-backed child permissions.
