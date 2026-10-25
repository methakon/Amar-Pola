# Amar-Pola — C++ Android Parental Monitoring

**Status:** Requirements and architecture planning  
**Documentation baseline:** SRS and canonical technical specification v1.0; deployment plan is not deployed  
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
- [Oracle Chicago Deployment, Capacity and Financial Plan](docs/OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md) — planned architecture, deployment sequence, finances and OCI-01–OCI-12 blockers (not provisioned)
- [Audit Remediation Status](docs/AUDIT_REMEDIATION_STATUS.md) — documentation fixes versus open implementation/deployment proof

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

## Route tracking, named places and stop detection

See [Live Trip Route, Named Places and Battery Specification](docs/LIVE_TRIP_ROUTE_NAMED_PLACES_BATTERY_SPECIFICATION.md) for the implementation design: parent-titled address markers, live map, raw GPS route polylines, multi-stop trip timeline, motion-aware low-battery collection, phone/tablet/Wear OS support, conditional Google Roads matching and device verification. This is a **proposed** implementation; no hardware tests have been executed.

## Adaptive movement tracking and scalable C++ reconstruction architecture

See [Adaptive Movement and Multi-Tenant C++ Server Architecture](docs/ADAPTIVE_MOVEMENT_CPP_SERVER_ARCHITECTURE.md) for a researched implementation specification: low-battery Android collection, durable batched ingestion, multi-guardian/child authorization, stateless Drogon API replicas, C++ per-device trip/stop reconstruction workers, PostgreSQL/PostGIS schema and security controls, capacity modelling, operations, tests, and phased delivery. **Engineering design only; not a measured production implementation.**

## Competitive product review (October 2026)

[Comparison of Findmykids, Find my Phone – Family Locator, Pinardin, FamiSafe and Kids360](docs/COMPETITOR_FEATURE_COMPARISON_AND_ADOPTION_2026.md) documents verified advertised features, Amar-Pola gaps, conditional Android feasibility and a proposed adoption backlog. **Proposals are not automatically approved product requirements or implemented features.**

## Feedback-led differentiation study (October 2026)

[Market Feedback, Competitive Gaps & Feasible Differentiation](docs/MARKET_FEEDBACK_GAPS_AND_DIFFERENTIATION_2026.md) reviews the original five Play apps plus Life360, Qustodio, Bark and Family Link against sampled Play reviews, feedback aggregators, Reddit parent discussions and official Android/Play guidance. It proposes confidence-aware trips, a device reliability center, offline trip repair, time-limited guardian grants, low-noise commute alerts, privacy access receipts and policy previews. **These are research proposals, not verified competitor absences or approved SRS features.**

## Documentation quality audit (2026-10-25)

[Technical Specification and Whole-Project SRS Gap Audit](docs/TECHNICAL_DOCUMENT_AUDIT_GAPS_2026.md) records **26 prioritized findings** after reviewing the current consolidated SRS, older canonical technical specification, C++ architecture, feasibility, OpenAPI, Android compatibility, privacy and Play documents. **Most urgent:** replace outdated canonical technical spec, formalize all endpoint/tenant/deletion contracts, complete FR-to-test traceability, and validate Android, battery and server failure cases. This is a documentation audit, **not** a code, hardware or Play Console certification; corrective changes have not yet been implemented.

## Canonical project specification and blocker review — 2026-10-25

**Read in this order:**

1. [Consolidated SRS v1.0](docs/SRS.md) — what the product must do; 49 FR and 16 NFR.
2. [Whole-project Feasibility Gate](docs/WHOLE_PROJECT_FEASIBILITY_GATE_2026.md) — where Android/security/policy permits each feature.
3. [Canonical Whole-Project Technical Specification v1.0](docs/TECHNICAL_SPECIFICATION.md) — authoritative system architecture, algorithms, API/data responsibilities, security, delivery.
4. [Decisions & Blockers for the Project Owner](docs/BLOCKERS_AND_OWNER_DECISIONS.md) — **22 owner questions**, 14 engineering blockers and 8 external release gates.
5. [Requirements Traceability](docs/REQUIREMENTS_TRACEABILITY.md) — every FR-001–049 and NFR-001–016 mapped to planned test IDs.
6. [Audit Remediation Status](docs/AUDIT_REMEDIATION_STATUS.md) — documentation fixes and real implementation/evidence still missing.

**Implementation annexes:** [Data/Authorization/Event Recovery](docs/DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md), [Android Runtime/Tracking Algorithms](docs/TRACKING_RUNTIME_AND_ALGORITHM_CONTRACT.md), [Commands/SOS/Usage/Queue](docs/COMMAND_SOS_USAGE_QUEUE_CONTRACT.md), and [expanded OpenAPI 3.1 draft](docs/openapi.yaml).

These are **engineering design documents**, not executed code, verified device compatibility, legally approved privacy terms or Google Play publication approval. Older documentation reflects the historical exploration; use the above canonical sources for new implementation decisions.

## First implementation milestone — Android + C++ (2026-10-25)

The project owner selected **native parent Android**, **managed-device provisioning support**, and **mixed Android OS versions**. The new [M1 Architecture and Implementation Contract](docs/M1_ANDROID_CPP_ARCHITECTURE_AND_IMPLEMENTATION.md) defines Kotlin/Compose parent and child platform services, portable C++20 NDK library, C++20 Drogon API, PostgreSQL identity/grant schema, test DPC owner provisioning and safe eligible app suspension/restore. It specifies the 10 M1 work packages, 14 test scenarios, and next milestones. It does **not** claim Android apps, backend code or DPC tests have already been implemented. [Updated owner blockers](docs/BLOCKERS_AND_OWNER_DECISIONS.md) record what is decided versus still open.

## Oracle Chicago hosting and per-child finances (2026-10-25)

**Hosting decision (plan, not provisioned):** Oracle OCI home region **US Midwest Chicago, us-chicago-1**, first attempting Always Free Ampere A1 **2 OCPU / 12 GB** with C++20 Drogon API, C++ reconstruction worker, and PostgreSQL/PostGIS on the **same ARM64 VM**. [OCI Chicago Deployment and Financial Plan](docs/OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md) documents provider sources, account/AD availability blockers, free vs paid A1 allowances, estimated monthly compute/storage/contingencies, one-subscription-per-child finances and upgrade triggers. PAYG 4/24 may remain inside the **paid-account** published A1 free-hour allowance if independently confirmed. This is a forecast, **not a billed deployment or observed capacity benchmark**.

**New cumulative hosting numbers:** [OCI paid usage: monthly, annual and planning-budget tables](docs/OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md#14-cumulative-recurring-hosting-cost-beyond-free-tier--monthly-annual-and-scaling-sensitivity). Separates priced OCI usage from discretionary reserve, models 500–50,000 illustrative children without asserting VM capacity, and lists cloud-account/cost verification blockers.
