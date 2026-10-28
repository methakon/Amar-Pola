# Madalasa–Alarka Local Coding Roadmap

Planning status: 20 phases and 262 atomic tasks. Tasks are not yet implemented. Local development uses synthetic test data.

- [Local development roadmap](LOCAL_AGENT_DEVELOPMENT_ROADMAP_2026-10-28.md)
- [Machine-readable task dependency graph](LOCAL_TASK_GRAPH_2026-10-28.json)
- [Task execution status ledger](LOCAL_TASK_EXECUTION_STATUS.json)
- [Agent testing and evidence protocol](AGENT_EXECUTION_AND_TEST_EVIDENCE.md)
- [Source references and conflict register](SOURCE_REFERENCE_AND_CONFLICT_REGISTER_2026-10-28.md)
- [Separate deployment and Play release plan](DEPLOYMENT_AND_PLAY_RELEASE_PLAN_SEPARATE_2026-10-28.md)
- [Agent entrypoint](../../AGENTS.md)

Dependency checks passed: 262 task IDs, dependencies present and acyclic, all statuses initialized NOT_STARTED. This is not evidence of code, physical-device validation, regulatory approval or production readiness.

## Figma 187-screen and API/database audit amendment

[Full screen-by-screen audit](../audits/FINAL_FIGMA_SCREEN_BY_SCREEN_API_DB_REPORT_2026-10-28.md) · [machine-readable exact screen mapping](../audits/FIGMA_SCREEN_API_DB_AUDIT_2026-10-28.json) · [96 new draft API operations](../audits/FIGMA_API_GAP_OPERATIONS_2026-10-28.json) · [28 additional local remediation tasks](FIGMA_SCREEN_API_DB_REMEDIATION_TASKS_2026-10-28.json) · [11-domain 120-table Figma database](../data-model/MADALASA_ALARKA_FIGMA_LOGICAL_ERD_V1_2026.json) · [proposed physical schema / external-parent RLS correction](../data-model/FIGMA_SCREEN_GAP_PHYSICAL_SCHEMA_REVIEW_2026-10-28.md). Original 262 tasks + 28 new audit tasks = **290 planned tasks**, all requiring actual implementation/testing; none of the new audit tasks is marked PASS.
