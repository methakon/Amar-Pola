# Branching, Versioning, CI and Release Process

> **Document control:** M1 / 02-development-process · Proposed owner: Engineering lead (not assigned) · Registry: DOCUMENTED_REVIEW_PENDING; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

**Status:** Proposed process, not an implemented app release. Current GitHub `main` contains docs/M1 contract and synthetic PostgreSQL tests. No Android releases/APKs, OCI production deployments or signed distribution.

## Git branches
- `main`: protected and reviewed; all changes via PR when branch protection/ownership is enabled. The CODEOWNERS file is a proposed map; GitHub does not create users or branch rules automatically.
- `feature/<issue>-slug`, `fix/<issue>-slug`, `docs/<issue>-slug` for scoped work.
- `release/vMAJOR.MINOR.PATCH` only after releasable tested artifacts exist; `hotfix/<id>` from tagged release when necessary.
- Conventional Commit messages suggested: `feat(android):`, `fix(ingest):`, `docs(privacy):`, `test(auth):`.
- Merge after scope/security owner review and passing configured CI; never bypass review for SOS, media, child GPS, billing or access controls.

## Versioning
Semantic Versioning for backend/API; Android `versionName` aligned to release and strictly increasing Play `versionCode`. Independently version `schema_version` for child GPS JSON, enrolled-device events and DB migrations. M1's 11-operation `docs/openapi-m1.yaml` is a frozen planning/test scope; the extended `docs/openapi.yaml` is **design-only** until versioned implementation and tests. A new `durable_stage=INBOX_COMMITTED` receipt must be introduced as a client-compatible change and tested against retries.

## CI baseline (verified files, not execution proof)
`.github/workflows/m1-contract-and-tenant.yml`: Python stdlib JSON OpenAPI structural lint, PostgreSQL 16 migration and synthetic tenant-isolation test. This is not C++ compilation, Gradle APK, SBOM, SAST, penetration testing, Android device matrix or Play review.

## Required CI as modules become real
Android Kotlin lint/unit tests, dependency lock/Gradle verification, manifest permission diff, emulator/API matrix + physical devices, C++ clang-tidy/clang-format/CMake/ASAN/UBSAN, Drogon integration/postgres RLS; secret scan and code/dep scan; SAST; reproducible builds, SBOM (CycloneDX/SPDX) and artifact signatures. Keep test fixtures synthetic. Only official SDK/binaries from approved sources; pinned workflow actions and least GitHub Actions permissions.

## Promotion
`dev/synthetic → internal dogfood with adults/test devices → scoped pilot ONLY after legal/Play clearance → staged Play rollout`. Each promotion requires recorded release gate: approved publisher, age/territory, India children DPDP/Google Play permissions, guardian checks, OS behavior proof, penetration tests, uptime/backups/restore, on-call owner, data retention/policy public pages, Play Data Safety/Families declarations and reviewer video.

## Release / rollback
Tag immutable annotated release, note commit SHA, CI results, source provenance/SBOM, Android signing lineage, DB migration and backup snapshot, feature toggles and known issues. Roll back feature flags/client traffic first; app rollback depends on Play version rules and DB compatibility. Never assume SQL down migration can undo irreversible data shape changes; use expand/contract. GPS inbox must remain intact across workers/server upgrade and revert. Revoke compromised signing or device keys through a documented process.

## Signoff
Owner/product, Android/backend, security/privacy and legal/Play leads sign a release checklist. All roles **unassigned today**; no automatic approval inferred by writing this policy.


## Branch ownership, minimal branching and recovery (owner direction 2026-10-29)

**Purpose:** keep work discoverable and reduce the risk of abandoned work or mistaken branch deletion. Branch creation is **not** the default for every task, agent session or document change. Reuse the existing active work branch when the change fits its purpose, can be reviewed in its existing PR, and does not create avoidable conflicts. Use `main` as the integration target after PR review/CI; keep integration history and branch naming visible.

### Mandatory steps before creating any branch

1. Run `git status --short --branch`, `git branch -a -vv`, `git fetch --all --prune` (prunes stale local remote-tracking references, **not actual remote branches**), and review active GitHub PRs, bases, commits and CI.
2. Check this register and the active PR discussion. Choose an existing branch whose scope matches the work, or propose a change to an existing PR. Do not start a new branch merely because a task has a new title, date, agent, or conversation.
3. Create a new branch only for a distinct change that genuinely requires independent review/integration, conflict isolation, different release timing, or a safety-sensitive experiment. Record its base, owner/agent, scope, dependent PRs, expected integration target and cleanup status **at creation** in the register.
4. Before changing an existing branch, inspect any uncommitted/unpushed work and do not overwrite another agent's changes. Coordinate shared-branch writes; avoid force pushing shared branches or silently rebasing stacked PRs. Do not impose a blanket no-commit rule: commit work to the correct tracked branch.
5. Every working PR should cite its parent/base and its follow-up; update the register when created, retargeted, merged, abandoned or closed. Use descriptive commits and CI results as the evidence trail. A PR merged **into another feature branch** is not yet included in `main`.
6. Merge in dependency order; after each merge, verify downstream diffs, retarget stacked PRs to `main` when appropriate, rerun checks, and confirm commit ancestry. Delete only an *already merged and verified* redundant branch after owner/team review; preserve unresolved commits and document alternatives before cleanup.

### Current known branch and PR register (snapshot verified 2026-10-29)

| Branch | PR / base | Purpose | Status / action |
|---|---|---|---|
| `main` | integration base | Stable source of truth | No change without normal integration workflow |
| `fix/m1-lint-credential-lifecycle` | [#3](https://github.com/methakon/Madalasa-Alarka/pull/3) → `main` | Credential lifecycle, M1 migration 0002/0003, lints | **OPEN**; merge/review first |
| `feat/m1-backend-skeleton-idempotency` | [#4](https://github.com/methakon/Madalasa-Alarka/pull/4) → `fix/m1-lint-credential-lifecycle` | Migration 0004, Drogon skeleton, tests | **OPEN**; follows #3, then retarget/retest |
| `feat/m1-physical-table-catalog` | [#5](https://github.com/methakon/Madalasa-Alarka/pull/5) → `feat/m1-backend-skeleton-idempotency` | 18-table catalog, mapping and CI check | **MERGED into #4 branch**, NOT yet `main`; verify ancestry after #4 merge; do not recreate |
| `feat/m1-g6-lint` | [#6](https://github.com/methakon/Madalasa-Alarka/pull/6) → `feat/m1-backend-skeleton-idempotency` | G-6 lint | **OPEN**; retarget/retest after #4 integration |
| `docs/2026-10-29-six-gate-owner-handoff` | [#1](https://github.com/methakon/Madalasa-Alarka/pull/1) → `main` | Six architecture/release gates | **OPEN**; consolidate/review rather than duplicate |
| `audit/2026-10-29-final-screen-api-db-reconciliation` | [#2](https://github.com/methakon/Madalasa-Alarka/pull/2) → `main` | Figma/API/DB audit and these branch governance rules | **OPEN**; existing documentation branch reused |
| `docs/phase-category-reorganization-2026-10-27` | No open PR found at snapshot | Older documentation reorganization | **REVIEW REQUIRED**; inspect unique commits before merge/archive, do not assume obsolete |

**Recommended sequence:** review/merge #3 → retarget/review/merge #4 → confirm #5 commits appear in `main` via #4 (or separate remaining changes if missing) → retarget/review/merge #6. Documentation PRs #1/#2 can be integrated independently after conflict and duplication review. Do **not** automatically merge, close, retarget or delete branches because this document suggests the order.

### Ongoing maintenance

- Treat this table as a dated snapshot, not a live API. Reconcile against `git branch -r` and GitHub PR statuses before acting; update the table whenever status changes.
- Each task's evidence should include branch, base, PR, commit SHA, tests, and integration/merge status. An agent must never describe a feature as on `main` merely because an upstream/stacked PR closed.
- Keep one shared, searchable branch register here rather than independent spreadsheets per agent. Document branch conflicts, abandoned sessions, and recovery commits here before deleting anything.
