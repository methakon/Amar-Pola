# Local PostgreSQL setup status

Status: migration/schema convergence verified locally; final metadata/export acceptance remains LOCAL_BLOCKED. No overall task PASS or production approval is recorded.

## Verified at the recorded checkpoint

- Both original historical M1 and clean V2 through 0018 replay successfully; populated upgrade and exact history adoption are verified without rewriting published SQL.
- Actual C++20/Drogon build and native CTest passed.
- The stable integration run passed 168 tests, including six actual HTTP integration tests and both real backup/restore tests. The metadata module was explicitly excluded pending its separate handoff; an unfiltered final run remains required.
- Historical `0001_m1_identity.sql` remained checksum-identical.

Commands, exit codes, actual catalog and implementation commits: [lineage convergence evidence](../../../evidence/local/database/LINEAGE_CONVERGENCE_2026-10-29.md). Persistent development was backed up, additively migrated from 0015 to 0018 and verified successfully. Test remains separately RAM-backed with fsync enabled; no reboot/power-loss durability certification is claimed.

## Open setup and synchronization work

1. Migration collisions are resolved with explicit checksummed lineages and additive bridges. The original 18-table M1 checkpoint/checker remains distinct from the converged 139-table application catalog.
2. Persistent development backup/migration/verification now succeed within bounded commands; the earlier I/O timeout is historical rather than the current blocker.
3. The [logical model reconciliation](MODEL_RECONCILIATION_2026-10-29.md) restores the 120-entity canonical baseline and preserves all 124 proposed entities separately; full contract lint and reference checks now pass without loosening the baseline. Derived mappings will be regenerated after the compatibility replay.
4. Reconcile the new physical-schema audit requirements, including per-table retention/ownership metadata, typed constraints and child-consistency evidence. Authored schema alone does not close those requirements.
5. Convergence is published as `4b4c4e85cebd3c35877d49e25fc2d7c11dc5f1a1`; additional historical restore routing/quarantine acceptance is committed as `50333c6dee6dfb45d6f56fd70501b8a4cb7a810f`. Final metadata integration, unfiltered regression and normal review/CI remain outstanding.
6. The two 0016 metadata authorization/child-consistency regressions now pass with additive 0018. Historical inspection restores remain quarantined; full V2 restore verifies suppression before reopening runtime.

## Admin API development assessment

Synthetic admin API development is permitted by the owner handoff; hosting, live Play verification and real-child legal approval are not prerequisites for local metadata-only coding. The migration collision no longer blocks that work; final setup/readiness acceptance still awaits the metadata exports and unfiltered regression.

Admin implementation must retain identity/approval/RBAC, immutable decisions, role revocation, redaction and denied-access tests. Existing SQL is not a running admin HTTP API. Real Google OIDC exchange and production authentication remain separate acceptance work. Owner authority must never imply unrestricted access to child location or media.

## Document control

[Package index](README.md) · [Runbook](RUNBOOK.md). This status is a workstream checkpoint, not a change to the approval state of historical specifications. The canonical document library remains organized by phase/category; implementation-specific database material is grouped here and linked from its indexes.
