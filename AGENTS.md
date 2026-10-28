# AGENTS.md — Madalasa–Alarka

This file is the **entrypoint for coding agents**. Work locally using synthetic data, not on production servers or live child devices.

## Read first

1. docs/roadmap/LOCAL_TASK_GRAPH_2026-10-28.json — 262 task IDs, dependencies, acceptance, source paths and evidence destinations.
2. docs/roadmap/LOCAL_AGENT_DEVELOPMENT_ROADMAP_2026-10-28.md — dependency-ordered phases, Figma/API/DB references, test gates.
3. docs/roadmap/AGENT_EXECUTION_AND_TEST_EVIDENCE.md — test and progress recording protocol.
4. docs/roadmap/SOURCE_REFERENCE_AND_CONFLICT_REGISTER_2026-10-28.md — authority and unresolved decisions.
5. docs/roadmap/DEPLOYMENT_AND_PLAY_RELEASE_PLAN_SEPARATE_2026-10-28.md — owner-only deployment and Play actions (DO NOT execute during local coding).

## Core commands (current vs future)

Current available structural check: python3 backend/tests/lint_openapi_m1.py docs/openapi-m1.yaml.
Current available DB baseline: backend/persistence/migrations/0001_m1_identity.sql and backend/tests/m1_tenant_isolation.sql; run only in disposable local PostgreSQL with proper non-superuser RLS tests.
Gradle Android builds, C++ Drogon build and admin web testing are tasks to CREATE, not assumed to work today.

## Hard stops

- Never process real child GPS, app usage, photos or media before lawful authority, retention and Google Play policy approval.
- No Play Console upload, developer account changes, actual billing, OCI deployment, device-owner provisioning or real-device wipe without explicit owner authorization.
- Never claim Family Link parent relationship verification is available from Google Sign-In. Sharing is exact-child scoped and disabled until verified.
- Keep admin owner authority tied to verified Google OIDC sub with role authorization; owner has no unrestricted child location/media access.
- No covert microphone/camera/screen recording, permission suppression or forced Android background capture.
- No secrets, private developer account ID, real household data or raw Play purchase tokens in Git.
- Never mark a task PASS without executed commands, actual exit code, redacted evidence and commit SHA.

## Task execution

Choose earliest dependency-ready task; prefer tests-first, minimal change, strict negative authorization tests and one PR/commit per small slice. Record progress in docs/roadmap/LOCAL_TASK_EXECUTION_STATUS.json and evidence/local/tasks/<TASK-ID>.md only once executed. Block external legal, physical-device and Play dependencies; continue unrelated tasks when explicit DAG allows. Review API/OpenAPI, DB/PostGIS RLS and Figma designs before implementation.

## Identity of the system

Parent app: Madalasa (Kotlin Android); child app: Alarka (Kotlin Android); backend: C++20 Drogon; database: PostgreSQL/PostGIS; admin: separate web panel. User-facing English first, Theme C pan-Indian Markandeya Purana interpretation, multilingual-ready.

Business: 48h first trial once; free live location + last 6h visible history; prepaid per selected child without auto-renew; first 1,008 distinct paid families founding price target; exact child-specific co-parent sharing, no automatic siblings; one premium concurrent viewer per paid child and optional ₹100 once for 100 days +30 pooled audio/video minutes, dormant during base-plan lapse.

End local development with evidence-based LOCAL_READY / LOCAL_BLOCKED / NOT_READY. **Deployment is separate.**

## Mandatory 2026-10-28 Figma/API/DB audit addendum

Before declaring LOCAL_READY, read [187-screen final audit](docs/audits/FINAL_FIGMA_SCREEN_BY_SCREEN_API_DB_REPORT_2026-10-28.md), [28 atomic gap remediation tasks](docs/roadmap/FIGMA_SCREEN_API_DB_REMEDIATION_TASKS_2026-10-28.json), [120 conceptual Figma database tables](docs/data-model/MADALASA_ALARKA_FIGMA_LOGICAL_ERD_V1_2026.json), and [real ap_m1 external co-parent FK/RLS blocker](docs/data-model/FIGMA_SCREEN_GAP_PHYSICAL_SCHEMA_REVIEW_2026-10-28.md). The original 262 tasks remain unchanged; 28 additional audit tasks apply before final local signoff. Run `python3 backend/tests/lint_openapi_full.py` after checking out the latest specification. The full OpenAPI contains **146 draft operations**, not 146 working handlers. No Figma screen is a verified Android build.
