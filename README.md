# Amar-Pola — C++ Android Parental Monitoring

**Status:** Requirements and architecture planning  
**Documentation baseline:** 0.1  
**Repository:** `methakon/Amar-Pola`

Amar-Pola is a privacy-conscious parental monitoring and device-management platform planned around three components:

1. **Child Android agent** — a permission-based app with a C++ native core and Kotlin/Java integration with Android APIs.
2. **Parent app/dashboard** — map, location history, speed when available, app-usage summaries, and supported remote controls.
3. **C++ backend** — device pairing, authenticated synchronization, command delivery, telemetry storage, subscription checks, auditing, and optional parent-authorized Google Drive backup.

The child app's main activity does not need to remain open for every background feature. However, Android may require foreground services, persistent notifications, privacy indicators, specific Settings grants, or user interaction for particular capabilities.

## Documentation

- [Discussion and decisions](docs/DISCUSSION.md)
- [Software Requirements Specification (SRS)](docs/SRS.md)
- [Technical Specification](docs/TECHNICAL_SPECIFICATION.md)

## Design principles

- Verify actual platform capability before offering a remote action.
- Show honest command states; never report success until execution is confirmed.
- Treat standard installation and managed-device enrollment as separate modes.
- Minimize CPU, RAM, network traffic, and battery use.
- Protect location and media data with authentication, encryption, audit records, and retention controls.
- Do not bypass Android permissions, privacy indicators, or platform safeguards.

## Proposed first milestones

1. Confirm supported Android versions and device setup modes.
2. Implement pairing, capability reporting, permission onboarding, location capture, and an encrypted local queue.
3. Deliver location history and parent map.
4. Add usage reports and tested managed-device restrictions.
5. Add capability-gated, authorized media workflows, Drive integration, subscriptions, and release hardening.

The documents are an initial design baseline, not a claim that the application is already implemented or that every feature works on every device.

## Expanded documentation (2026-10-25 review)

The following documents supplement the initial v0.1 baseline. They are architecture, validation, and Play-submission drafts—not proof of device tests or approval:

- [Feature feasibility, reasons and precise conditions](docs/FEASIBILITY_CONDITIONS_AND_EVIDENCE.md)
- [Implementation technical specification and roadmap](docs/IMPLEMENTATION_TECHNICAL_SPECIFICATION.md)
- [Google Play publishing and permission requirements](docs/GOOGLE_PLAY_PUBLISHING_REQUIREMENTS.md)
- [Play Data safety and Android permission worksheet](docs/DATA_SAFETY_WORKSHEET.md)
- [Privacy policy publication draft](docs/PRIVACY_POLICY_DRAFT.md)
- [Account and data deletion design](docs/ACCOUNT_DELETION_DESIGN.md)
- [Store listing and Play reviewer guidance](docs/PLAY_STORE_LISTING_AND_REVIEWER_GUIDE.md)
- [Verification, testing and release roadmap](docs/VALIDATION_AND_RELEASE_PLAN.md)
- [Security architecture and operations](docs/SECURITY_AND_OPERATIONS.md)

**Publication warning:** There are not yet release AABs, live privacy/deletion web pages, Play Console declarations, reviewer demonstration videos, or verified Android device test results. These must be created and validated before publishing either app.

Additional implementation and release references:
- [Android 10–16 compatibility test matrix](docs/ANDROID_COMPATIBILITY_MATRIX.md)
- [Draft machine-readable OpenAPI contract](docs/openapi.yaml)
- [Subscription and terms disclosure template](docs/TERMS_AND_SUBSCRIPTIONS_DRAFT.md)
