# Local PostgreSQL implementation package

Status: LOCAL_BLOCKED. This package documents synthetic local implementation work; it is not a production-readiness or legal-approval record.

## Reading order

1. [Current setup status and integration prerequisites](STATUS.md).
2. [Development, migrations, build, tests and recovery runbook](RUNBOOK.md).
3. [Current lineage convergence and 168-test checkpoint](../../../evidence/local/database/LINEAGE_CONVERGENCE_2026-10-29.md); [earlier 140-test checkpoint](../../../evidence/local/database/REVERIFICATION_2026-10-29.md); [historical interrupted run](../../../evidence/local/database/INTEGRATION_PENDING_2026-10-29.md).
4. [Owner decisions and acceptance boundaries](../../roadmap/SIX_GATE_OWNER_DECISIONS_AND_AGENT_HANDOFF_2026-10-29.md).
5. [Logical model reconciliation and enhancement security review](MODEL_RECONCILIATION_2026-10-29.md).
6. [Separate historical 18-table M1 catalog](../historical-m1/PHYSICAL_TABLE_CATALOG.md).

## Package ownership and layout

- `docs/data-model/local-postgresql/`: database-specific runbook, status, and catalog/traceability exports when generated and verified.
- `backend/persistence/migrations/`: versioned executable SQL, not duplicated in documentation.
- `backend/tests/database/`: synthetic database and HTTP integration acceptance.
- `tools/database/`: local lifecycle and catalog-export tooling.
- `evidence/local/database/`: redacted execution checkpoints, separate from specifications.
- `.local-db/`: ignored credentials, raw logs, database storage, build caches and backup archives. Never commit these files.

The [catalog](physical-schema.json), [physical ERD](PHYSICAL_ERD.md), [logical mapping](logical-to-physical.json), [operation/dependency matrix](api-to-table.json) and [migration manifest](migration-manifest.json) were generated and verified at the earlier checkpoint. Logical models are now versioned correctly and migration lineages converge; derived artifacts and retention/constraint metadata still need final regeneration/acceptance. They are schema/dependency evidence, not proof of every HTTP handler.

## Navigation

[Documentation home](../../README.md) · [Canonical project document index](../../phases/M0-foundation-and-approvals/01-project-governance/PROJECT_DOCUMENTS_INDEX_2026.md) · [M1 development-process index](../../phases/M1-secure-platform-foundation/02-development-process/README.md)
