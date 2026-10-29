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

## PR integration sequence (verified 2026-10-29)

Live state, ancestry and per-ref contents were checked with read-only Git and GitHub API calls. Nothing below was merged, retargeted or closed by this review.

| PR | Base → Head | State | Consequence |
|---|---|---|---|
| [#3](https://github.com/methakon/Madalasa-Alarka/pull/3) | `main` `861ab630` → `fix/m1-lint-credential-lifecycle` `3f6cd01` | OPEN, MERGEABLE | Supplies the M1 API conventions/error catalog and contract lint; a narrow `type: http` lint fix already exists on the database branch |
| [#4](https://github.com/methakon/Madalasa-Alarka/pull/4) | #3 → `feat/m1-backend-skeleton-idempotency` `ddbb25a` | OPEN, MERGEABLE | Carries #5; supplies the request-ID/idempotency helpers and the historical credential/enrollment/idempotency migrations |
| [#5](https://github.com/methakon/Madalasa-Alarka/pull/5) | #4 → `feat/m1-physical-table-catalog` `976805d` | MERGED into #4 | `976805d` is an ancestor of `ddbb25a` and is **not** on `main`; do not treat MERGED as landed |
| [#6](https://github.com/methakon/Madalasa-Alarka/pull/6) | #4 `ddbb25a` → `feat/m1-g6-lint` `48318b2` | OPEN, MERGEABLE | G-6 per-response error-code lint; depends on #3's contract |

`feat/local-postgresql-physical-schema` shares only the verified `main` base `861ab630` with that stack: none of `3f6cd01`, `ddbb25a`, `976805d` or `48318b2` is its ancestor, and `git cherry` reports all seven stack commits as not patch-equivalent.

**Earlier blocking note is superseded.** An audit snapshot recorded a versions 0002–0004 collision with an instruction to renumber. That is no longer the state of this branch: `backend/persistence/migration-lineages.json` now pins both published chains under distinct identities (`m1:0002`–`m1:0004`, `v2:0002`–`v2:0018`, `common:0001`, `compat:m1_pre_v2_0016`), the runner refuses unknown or drifting history, and replay on both paths is recorded in `evidence/local/database/`. Do not renumber either published chain.

Recommended order, each step requiring its own review and green CI:

1. Review/merge #3 into `main`.
2. Retarget #4 onto `main`; confirm `976805d` is still an ancestor after retarget and review/merge #4.
3. Retarget #6 onto the merged #4 state and review/merge #6.
4. Rebase `feat/local-postgresql-physical-schema` onto the resulting `main`, resolving only genuine overlaps: keep this branch's database-backed `main.cc`, CMake targets, migration manifest and adapted historical-catalog checker; adopt the stack's centralized error/request-ID handling, error catalog and contract lint rather than replacing the backend with the historical skeleton.

The database branch already preserves the historical migration and test-source bytes, so step 4 must not re-add or renumber those files. Local reconciliation is complete; public integration is gated on the #3 → #4 → #6 sequence.
