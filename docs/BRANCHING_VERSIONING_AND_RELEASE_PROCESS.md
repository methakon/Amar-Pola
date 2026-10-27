# Branching, Versioning, CI and Release Process

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
