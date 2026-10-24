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
