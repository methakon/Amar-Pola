# Local PostgreSQL implementation package

Status: LOCAL_BLOCKED. This package documents synthetic local implementation work; it is not a production-readiness or legal-approval record.

## Reading order

1. [Current setup status and integration prerequisites](STATUS.md).
2. [Development, migrations, build, tests and recovery runbook](RUNBOOK.md).
3. [Executed partial verification checkpoint](../../../evidence/local/database/INTEGRATION_PENDING_2026-10-29.md).
4. [Owner decisions and acceptance boundaries](../../roadmap/SIX_GATE_OWNER_DECISIONS_AND_AGENT_HANDOFF_2026-10-29.md).

## Package ownership and layout

- `docs/data-model/local-postgresql/`: database-specific runbook, status, and catalog/traceability exports when generated and verified.
- `backend/persistence/migrations/`: versioned executable SQL, not duplicated in documentation.
- `backend/tests/database/`: synthetic database and HTTP integration acceptance.
- `tools/database/`: local lifecycle and catalog-export tooling.
- `evidence/local/database/`: redacted execution checkpoints, separate from specifications.
- `.local-db/`: ignored credentials, raw logs, database storage, build caches and backup archives. Never commit these files.

Catalog exports, the physical ERD and API-to-table matrix are pending final successful integration; their absence must not be represented as verified coverage. Migration numbering also needs reconciliation with the existing stacked M1 work before publication of the implementation.

## Navigation

[Documentation home](../../README.md) · [Canonical project document index](../../phases/M0-foundation-and-approvals/01-project-governance/PROJECT_DOCUMENTS_INDEX_2026.md) · [M1 development-process index](../../phases/M1-secure-platform-foundation/02-development-process/README.md)
