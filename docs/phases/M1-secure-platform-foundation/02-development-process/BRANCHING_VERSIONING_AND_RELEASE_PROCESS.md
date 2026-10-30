# Branching, Versioning, CI and Release Process

> **Document control:** M1 / 02-development-process · Proposed owner: Engineering lead (not assigned) · Registry: DOCUMENTED_REVIEW_PENDING; approval not recorded. [Master register](../../../MASTER_DOCUMENT_CONTROL_REGISTER.md).

**Status:** process and integration record, not an app release. Current `main` contains the scoped Drogon M1 backend, independently reviewed Google OIDC/JWKS implementation and synthetic PostgreSQL acceptance. No genuine Google-user login, Android release, OCI production deployment, Play approval or signed distribution is certified by this record.

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

### Historical pre-consolidation branch register (superseded by the current register below)

| Branch | PR / base | Purpose | Status / action |
|---|---|---|---|
| `main` | integration base | Stable source of truth | `0a6be11ca811e842cc9839ab623ec118514020dd`; includes #3, not complete #4–#8 stack |
| `fix/m1-lint-credential-lifecycle` | [#3](https://github.com/methakon/Madalasa-Alarka/pull/3) → `main` | Credential lifecycle, M1 migration 0002/0003, lints | **MERGED** into main as `0a6be11`; branch later advanced to `2821a8a` via #4, which is NOT thereby on main |
| `feat/m1-backend-skeleton-idempotency` | [#4](https://github.com/methakon/Madalasa-Alarka/pull/4) → `fix/m1-lint-credential-lifecycle` | Migration 0004, Drogon skeleton, tests | **MERGED** into feature branch as `2821a8a`; branch later advanced to `58ba650` via #6 |
| `feat/m1-physical-table-catalog` | [#5](https://github.com/methakon/Madalasa-Alarka/pull/5) → `feat/m1-backend-skeleton-idempotency` | 18-table catalog, mapping and CI check | **MERGED** as `ddbb25a`; included in PR9 ancestry, not current main |
| `feat/m1-g6-lint` | [#6](https://github.com/methakon/Madalasa-Alarka/pull/6) → `feat/m1-backend-skeleton-idempotency` | G-6 lint | **MERGED** as `58ba650`; #7 later merged into this branch as `62a33a6` |
| `feat/m1-create-family` | [#7](https://github.com/methakon/Madalasa-Alarka/pull/7) → `feat/m1-g6-lint`; [#9](https://github.com/methakon/Madalasa-Alarka/pull/9) → `main` | createFamily, M1 0005 provisioning, final stack integration | #7 **MERGED into feature branch**; #9 **OPEN** at `c693899e4b411cbadd1639f0bcb642844af50ea9`; detailed review and explicit owner merge approval required |
| `feat/m1-purge-jobs` | [#8](https://github.com/methakon/Madalasa-Alarka/pull/8) → `feat/m1-create-family` | Restricted purge role, jobs, units and tests | **MERGED** as `c693899`; its tree equals PR9 head; nothing scheduled/deployed |
| `docs/2026-10-29-six-gate-owner-handoff` | [#1](https://github.com/methakon/Madalasa-Alarka/pull/1) → `main` | Six architecture/release gates | **OPEN**; consolidate/review rather than duplicate |
| `audit/2026-10-29-final-screen-api-db-reconciliation` | [#2](https://github.com/methakon/Madalasa-Alarka/pull/2) → `main` | Figma/API/DB audit and these branch governance rules | **OPEN**; existing documentation branch reused |
| `feat/local-postgresql-physical-schema` | No open PR found at snapshot | Synthetic V2 DB through 0019; original M1 and namespaced lineage/checksum adoption | `b507e5f`; preserve published bytes and existing manifest, **do not renumber or replay alphabetically**. PR9's historical M1 0005 and conflicting backend/catalog still need semantic integration |
| `docs/phase-category-reorganization-2026-10-27` | No open PR found at snapshot | Older documentation reorganization | **REVIEW REQUIRED**; inspect unique commits before merge/archive, do not assume obsolete |

**Historical sequence:** this described the review before the owner's consolidation authorization. It is preserved as history, not a current assertion that PR9/PR2 remain open. The current register and evidence below supersede its integration/deletion states; legal and production release gates remain separate.

### Current consolidation register — owner authorization 2026-10-30

The owner explicitly requested integration into `main`, followed by deletion of successfully integrated redundant remote branches. **No new working branches; preserve existing names; no force push or rewriting main; never delete main or unique/unverified work.** Source references were captured in a verified, private local Git bundle before operations. [Full original heads, deletion readbacks and verification record](../../../../evidence/local/integration/BRANCH_CONSOLIDATION_2026-10-30.json).

| Original branch | Current disposition | Content / evidence |
|---|---|---|
| `main` | RETAINED — consolidated integration target | Runtime integration `9c5b9bd2ff2a4a789e54e1fdf37377dd68d125fc`; backend and documentation CI successful; later documentation/tooling checkpoints do not imply production readiness |
| `audit/2026-10-29-final-screen-api-db-reconciliation` | **merged and deleted** remotely | PR2 merged as `de135f5`; full merged tree matched tested audit `3377338` |
| `docs/2026-10-29-six-gate-owner-handoff` | **merged and deleted** remotely | Exact handoff preserved by `b91d0d0`; no owner decisions promoted to legal/Play approval |
| `feat/google-oidc` | **merged and deleted** remotely | Independently reviewed `a0527a7`, integrated by `9c5b9bd`; five CTests, HTTP and marker exclusion gates passed |
| `feat/m1-create-family` | **consolidated and deleted** remotely | Tip `7c8e2dc` has exactly the same full Git tree as OIDC `a0527a7`; no duplicate cherry-pick or competing authenticator introduced |
| `feat/m1-backend-skeleton-idempotency` | **already integrated and deleted** remotely | No unique non-merge patches beyond tested M1 source `b1df657`, already represented in the pre-consolidation main foundation and later tested implementation |
| `feat/m1-g6-lint` | **already integrated and deleted** remotely | Same patch-coverage proof; current contract lint retained |
| `feat/m1-physical-table-catalog` | **already integrated and deleted** remotely | Same patch-coverage proof; current 18-table catalog includes additive hold columns and strict checks |
| `feat/m1-purge-jobs` | **already integrated and deleted** remotely | Same patch-coverage proof; current restricted runner/role and retention/concurrency tests retained |
| `fix/m1-lint-credential-lifecycle` | **already integrated and deleted** remotely | Same patch-coverage proof; published historical SQL unchanged and later additive fixes retained |
| `docs/phase-category-reorganization-2026-10-27` | **consolidated and deleted** remotely | All12 source-only artifacts hash-checked and accounted for; 22 parser/negative tests, 72-row current register, navigation fixes and historical archive integrated. [Current proof and CI](../../../../evidence/local/integration/DOCUMENTATION_CONSOLIDATION_2026-10-30.json) at `1312dac`; remote deletion read back |
| `feat/local-postgresql-physical-schema` | **ACTIVE INTEGRATION — PR [#11](https://github.com/methakon/Madalasa-Alarka/pull/11)** | Source `b507e5f` merged with `main`; convergence completed additively (`compat:m1_pre_v2_0017`, `v2:0020`, manifest coverage of `m1:0005`/`0006`) with every published migration byte-identical. Executed on isolated PostgreSQL 16.9/PostGIS 3.5.2: fresh V2, M1 suites, populated 0004/0006→V2 upgrades with retention holds preserved, 232-test suite, restore/quarantine drill. Production `ma_backend` stays on historical M1 authorization; V2 production session issuance remains an explicit blocker. [Acceptance record](../../../../evidence/local/database/PR11_RECONCILIATION_ACCEPTANCE_2026-10-30.md). Delete only after merge and verification on `main` |

OIDC identity contains only issuer/subject; it does not prove adulthood, legal guardianship, consent or child access. Its public-key fetch/cache tests and a positive public Google JWKS fetch are not genuine Google ID-token or adversarial live-TLS certification. The retained V2 database branch was source-reviewed only during this consolidation: its dated 205-test evidence is not current integrated acceptance, and no published migration was altered to force convergence.

### Ongoing maintenance

- Treat this table as a dated snapshot, not a live API. Reconcile against `git branch -r` and GitHub PR statuses before acting; update the table whenever status changes.
- Each task's evidence should include branch, base, PR, commit SHA, tests, and integration/merge status. An agent must never describe a feature as on `main` merely because an upstream/stacked PR closed.
- Keep one shared, searchable branch register here rather than independent spreadsheets per agent. Document branch conflicts, abandoned sessions, and recovery commits here before deleting anything.

### Superseded DB-source integration decisions (source `b507e5f`, PR11 review)

The source branch's 2026-10-29 #3 → #4 → #6 sequencing and its instruction
to prefer the DB branch backend/CMake over the then-historical skeleton are
**superseded**, not current implementation instructions: the current integration
must preserve main's production Drogon/OIDC backend and M1 through0006. The
historical lineage/checksum decision remains valid: published overlapping M1 and
V2 migration numbers are distinct namespaced identities; do not renumber either
chain or execute their alphabetical union. Existing published migration/test bytes
and the source-through0004 catalog/mapping remain provenance, not substitutes for
current acceptance. The source's earlier non-ancestry/patch-equivalence snapshot
against `861ab630` does not describe the post-consolidation branch state.

PR11 reuses the retained database branch; neutral file-by-file conflict review and
additive compatibility are in progress against `4a1fda5`. No merge, branch deletion
or readiness is asserted here. Main's completed cleanup rows above are unchanged;
all current-M1/fresh/old/restore equivalence, security and integration gates must
pass before engineering merge. Owner authorization for engineering integration
is not legal, Play, deployment, guardian-authority or pricing approval.
