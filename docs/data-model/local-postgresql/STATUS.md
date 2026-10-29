# Local PostgreSQL setup status

Status: LOCAL_BLOCKED for canonical integration; the isolated V2 test baseline is now verified. No overall task PASS or production approval is recorded.

## Verified at the recorded checkpoint

- Fresh isolated local replay applied the implementation's 0001–0016 chain successfully.
- Actual C++20/Drogon build and native CTest passed.
- The latest isolated full suite passed all 140 tests, including six actual HTTP integration tests and both real backup/restore tests. The prior 69-test timeout is historical, not the current suite result.
- Historical `0001_m1_identity.sql` remained checksum-identical.

Commands, exit codes, actual catalog and implementation commit: [re-verification evidence](../../../evidence/local/database/REVERIFICATION_2026-10-29.md). The test instance is separately RAM-backed with fsync enabled; this does not certify persistent-disk durability, performance or the development database upgrade.

## Open setup and synchronization work

1. Reconcile migration numbering with the existing stacked M1 credential/enrollment/idempotency work: that branch already has different migrations numbered 0002–0004. The local chain must not be published as if those versions were unallocated. Preserve historical migrations and account for the existing physical catalog/checkers.
2. Host I/O pressure is bypassed for isolated tests without touching development storage; persistent-development upgrade and its recovery state still need verification.
3. The [logical model reconciliation](MODEL_RECONCILIATION_2026-10-29.md) restores the 120-entity canonical baseline and preserves all 124 proposed entities separately; full contract lint and reference checks now pass without loosening the baseline. Derived mappings will be regenerated after the compatibility replay.
4. Reconcile the new physical-schema audit requirements, including per-table retention/ownership metadata, typed constraints and child-consistency evidence. Authored schema alone does not close those requirements.
5. Verified test-isolation fixes are committed and pushed as `3d3e285cbf92f0583749cb239d9e3c0bd74e903f`. Canonical migration integration and normal review/CI remain outstanding.
6. Subsequent enhancement review reproduced two metadata authorization/child-consistency defects in 0016. Additive 0018 and focused tests are authored; their coordinated GREEN run is still pending. The earlier 140-test checkpoint does not close these newly identified cases.

## Admin API development assessment

Synthetic admin API development is permitted by the owner handoff; hosting, live Play verification and real-child legal approval are not prerequisites for local metadata-only coding. However, this checkpoint does not establish a verified, integration-ready database baseline for admin APIs.

Before building on the database, reconcile the migration chain and verify admin identity/approval/RBAC, immutable decisions, role revocation, redaction and denied-access tests. Existing SQL is not a running admin HTTP API. Real Google OIDC exchange and production authentication remain separate acceptance work. Owner authority must never imply unrestricted access to child location or media.

## Document control

[Package index](README.md) · [Runbook](RUNBOOK.md). This status is a workstream checkpoint, not a change to the approval state of historical specifications. The canonical document library remains organized by phase/category; implementation-specific database material is grouped here and linked from its indexes.
