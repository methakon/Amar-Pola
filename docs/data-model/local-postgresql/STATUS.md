# Local PostgreSQL setup status

Status: LOCAL_BLOCKED / integration incomplete. Updated for the 2026-10-29 documentation checkpoint; no task PASS is recorded.

## Verified at the recorded checkpoint

- Clean local migration replay applied the implementation's 0001–0015 chain successfully.
- Actual C++20/Drogon build and native CTest passed.
- The latest isolated full-suite attempt completed 69 passing tests, including six actual HTTP integration tests, before timing out during backup/restore. This is not a complete passing suite.
- Historical `0001_m1_identity.sql` remained checksum-identical.

Commands, exit codes and limitations: [execution evidence](../../../evidence/local/database/INTEGRATION_PENDING_2026-10-29.md). Subsequent source edits require re-verification; the checkpoint does not certify the current source tree as a whole.

## Open setup and synchronization work

1. Reconcile migration numbering with the existing stacked M1 credential/enrollment/idempotency work: that branch already has different migrations numbered 0002–0004. The local chain must not be published as if those versions were unallocated. Preserve historical migrations and account for the existing physical catalog/checkers.
2. Resolve host I/O pressure, confirm the interrupted restore's quarantine state, and complete serial database/recovery tests without weakening durability or authorization.
3. Generate and verify the final catalog, logical-to-physical mapping, physical ERD and operation/dependency matrix.
4. Reconcile the new physical-schema audit requirements, including per-table retention/ownership metadata, typed constraints and child-consistency evidence. Authored schema alone does not close those requirements.
5. Finish tested implementation commits and normal review/CI integration. This documentation checkpoint intentionally does not stage the unfinished implementation.

## Admin API development assessment

Synthetic admin API development is permitted by the owner handoff; hosting, live Play verification and real-child legal approval are not prerequisites for local metadata-only coding. However, this checkpoint does not establish a verified, integration-ready database baseline for admin APIs.

Before building on the database, reconcile the migration chain and verify admin identity/approval/RBAC, immutable decisions, role revocation, redaction and denied-access tests. Existing SQL is not a running admin HTTP API. Real Google OIDC exchange and production authentication remain separate acceptance work. Owner authority must never imply unrestricted access to child location or media.

## Document control

[Package index](README.md) · [Runbook](RUNBOOK.md). This status is a workstream checkpoint, not a change to the approval state of historical specifications. The canonical document library remains organized by phase/category; implementation-specific database material is grouped here and linked from its indexes.
