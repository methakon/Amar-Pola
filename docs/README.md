# Madalasa–Alarka — Project Documentation Library

**Organized:** 2026-10-27 · **Scope:** documentation-first planning, **not software implementation**. Canonical source documents are organized **by M0–M9 project phase, then by category** using the repository's [master milestone plan](phases/M0-foundation-and-approvals/01-project-governance/MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md). P3 research remains outside the launch milestones.

The 72 root-level compatibility pointers were consolidated into [legacy-root-links](legacy-root-links/README.md), while their canonical M0–M9 full documents and the two OpenAPI files remain in place. Old direct GitHub root-level pointers should now be replaced by canonical document links.

## Start here

[Master Document Control Register](MASTER_DOCUMENT_CONTROL_REGISTER.md) · [Document Control Policy](DOCUMENT_CONTROL_POLICY.md) · [Phase Coverage Matrix](PHASE_DOCUMENTATION_COVERAGE_MATRIX.md) · [Relocation Manifest](DOCUMENT_RELOCATION_MANIFEST.json) · [M1 OpenAPI contract](openapi-m1.yaml) · [Whole-project API design](openapi.yaml) · [Figma design handoff](ui/figma-functional-handoff/README.md)

## Repository Subfolder Structure

| Directory | Scope & Contents | Index |
|---|---|---|
| [`phases/`](phases/README.md) | Canonical M0–M9 phase specifications, architecture contracts, and governance | [Browse Phases](phases/README.md) |
| [`roadmap/`](roadmap/README.md) | Local task graph, DAG execution status, decision ledger, and test evidence rules | [Browse Roadmap](roadmap/README.md) |
| [`data-model/`](data-model/README.md) | Logical 11-domain ERD, physical schema mappings, and relational audit reports | [Browse Data Model](data-model/README.md) |
| [`audits/`](audits/README.md) | 187-screen Figma audits, 171 API contract crosswalks, and blocker reports | [Browse Audits](audits/README.md) |
| [`ui/`](ui/README.md) | Figma screen indexes, Theme C narrative, design tokens, and functional handoffs | [Browse UI](ui/README.md) |
| [`legacy-root-links/`](legacy-root-links/README.md) | Consolidated redirect pointers preserving historical root documentation links | [Browse Legacy Links](legacy-root-links/README.md) |
| [`tools/`](tools/README.md) | Automated document validation, reorganization verification, and check scripts | [Browse Tools](tools/README.md) |

## Milestones and folders

| Phase | Document category / purpose | Source documents | Browse |
|---|---|---:|---|
| **M0** | Project foundation, ownership, market feasibility, India privacy and legal decisions | 25 | [M0-foundation-and-approvals](phases/M0-foundation-and-approvals/README.md) |
| **M1** | Secure Android/C++ foundation, M1 requirements, developer standards and permissions | 16 | [M1-secure-platform-foundation](phases/M1-secure-platform-foundation/README.md) |
| **M2** | Android location collection, encrypted offline queue and durable GPS ingestion | 3 | [M2-location-collection](phases/M2-location-collection/README.md) |
| **M3** | Trip, stop and named-place geometry from recorded locations | 1 | [M3-trips-and-places](phases/M3-trips-and-places/README.md) |
| **M4** | UsageStats, check-ins, health and SOS delivery semantics | 2 | [M4-usage-health-sos](phases/M4-usage-health-sos/README.md) |
| **M5** | Eligible managed Android policies and Device Owner lifecycle | 0 | [M5-managed-android-controls](phases/M5-managed-android-controls/README.md) |
| **M6** | Per-child delegated access, account deletion, backups and recovery | 1 | [M6-guardian-erasure-security](phases/M6-guardian-erasure-security/README.md) |
| **M7** | Commercial integration, child-seat pricing and budgets | 3 | [M7-commercial-integrations](phases/M7-commercial-integrations/README.md) |
| **M8** | Operational readiness, cloud, backup, incident response, support and QA | 10 | [M8-operational-readiness](phases/M8-operational-readiness/README.md) |
| **M9** | Google Play launch, reviewer declarations, Data Safety and public contracts | 7 | [M9-play-release](phases/M9-play-release/README.md) |
| **P3** | Deferred media experiments, activity metadata and admin-panel research | 3 | [P3-deferred-research](phases/P3-deferred-research/README.md) |
| **CROSS** | Cross-milestone diagrams and existing Figma architecture indexes | 1 | [cross-milestone-references](phases/cross-milestone-references/README.md) |

**72 canonical full-text source documents**, plus [two root OpenAPI contracts](openapi-m1.yaml), existing [Figma/tldraw handoffs](ui/), and root repository governance files. The older `docs/<file>.md` entries are **short forwarding pages**, not duplicate authoritative versions; this deliberately keeps previously shared GitHub URLs usable.

## Professional control and approval approach

Filing into a phase/category is not a claim of internal sign-off. Every migrated document has a navigation-only header linking the [Master Document Control Register](MASTER_DOCUMENT_CONTROL_REGISTER.md), with a **proposed owner role** and conservative approval state. No individual has been assigned or signed a decision by this reorganization. The [Control Policy](DOCUMENT_CONTROL_POLICY.md) specifies IDs, versioning, accountability, review records, baselines and supersession.

**Critical open decisions:** India children's location/usage lawfulness and Play eligibility; publisher/guardian verification; GPS 14-vs-30-day raw retention; processor DPAs/region; production incident/support contacts; licensing; Android/C++ implementation; CI evidence. M5 has no dedicated standalone technical design and is explicitly flagged in its phase index. All real-child pilot/release gates remain blocked until actual evidence and approval.

**Stable paths:** `docs/openapi-m1.yaml` and `docs/openapi.yaml` remain unchanged so existing CI/requirements contracts are not silently broken. `docs/ui/` remains in its established Figma/tldraw handoff layout.

## Agent-ready local coding plan

Use [2026-10-28 local development roadmap](roadmap/LOCAL_AGENT_DEVELOPMENT_ROADMAP_2026-10-28.md) and [262-task dependency graph](roadmap/LOCAL_TASK_GRAPH_2026-10-28.json) with [evidence rules](roadmap/AGENT_EXECUTION_AND_TEST_EVIDENCE.md). This complements older M0–M9 milestones; it does not mark them completed. [Deployment and Google Play review remain separate](roadmap/DEPLOYMENT_AND_PLAY_RELEASE_PLAN_SEPARATE_2026-10-28.md).
