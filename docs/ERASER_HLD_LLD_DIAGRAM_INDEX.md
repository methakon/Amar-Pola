# Amar-Pola — Eraser.io HLD & LLD Diagram Registry

**Date:** 2026-10-26 · **Status:** 8 diagrams created and verified in connected Eraser team workspace, design diagrams only (not implemented).\n
**Eraser project file:** https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv

| Diagram | Eraser link | Coverage |
|---|---|---|
| HLD — System Context & Trust Boundaries | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=jQyWLWJX9S69ShFULHE3&layout=canvas) | Full ecosystem, Android, C++ backend, data stores, trust boundaries and India DPDP gating |
| HLD — OCI Mumbai Deployment & Disaster Recovery | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=omtR3y1WBROQklllz6Hq&layout=canvas) | Single VM risk, backup/WAL, RPO/RTO targets and third-party transfer caveats |
| LLD — M1 Secure Enrollment & Key Proof | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=QeyVOP0EH8QoyQ3BNQE2&layout=canvas) | Kotlin + Android Keystore PoP, pairing-code replay rejection and device revocation |
| LLD — M1 PostgreSQL Tenant-Isolation ERD | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=k9ZQ2ixfKvGhhPO78e9f&layout=canvas) | M1 family/child/guardian grants, devices and forced RLS relationships |
| LLD — GPS Ingestion & Event-Time Reconstruction | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=ghgtwzh38ovFtivtUg6h&layout=canvas) | Encrypted queue, durable ACK, C++ geo worker, uncertain route rendering, deletion |
| LLD — Guardian Authorization & Revocation | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=Besc1tErcBahsMebk29v&layout=canvas) | Child-specific ACL, cross-family negative cases, pickup TTL, active stream invalidation |
| LLD — SOS Alert & Independent Fallback | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=os70bsdV1d49u7CF93xd&layout=canvas) | FCM provider vs human acknowledgement, conditional SMS, offline limitations |
| LLD — Family Billing & Entitlements | [Open live diagram](https://app.eraser.io/workspace/dP8nMbuaxaFXBkBzUHCv?diagram=6ZY6KKV8Af9b2q27v3Q1&layout=canvas) | Proposed 50/500 family child-seat plans, Play verification, RTDN and refunds |

## Design caveats

- M1 design/migration exists; backend and Android runtime have not passed live implementation tests. No OCI account/VM or high availability service is provisioned.
- Preferred primary hosting OCI Mumbai ap-mumbai-1, alternate Hyderabad; legacy Chicago report is historical cost planning.
- India DPDP legal child-purpose, ages, publisher identity, guardian approvals and app-usage/history lawful processing remain **OPEN**; no real minor data authorized.
- SOS is at most a best-effort child-initiated check-in until funded independent fallback and tested guardian human acknowledgement.
- ₹50 monthly / ₹500 annual per child are **proposed**, not settled Play Console prices nor demonstrated fully-loaded profitable prices.
- M1 ERD is a logical visual of migration table relationships and authorizations, not proof that Postgres CI has passed. Diagram DSL remains editable in Eraser; source SQL and OpenAPI in repository are authoritative.

## Cross-reference

- [Single master milestone roadmap](MASTER_MILESTONE_IMPLEMENTATION_AND_RELEASE_PLAN.md)
- [M1-only API](openapi-m1.yaml)
- [M1 PostgreSQL schema](../backend/persistence/migrations/0001_m1_identity.sql)
- [Legal gate](INDIA_DPDP_CHILD_PRIVACY_AND_CROSS_BORDER_GATE.md)
- [OCI India selection](INDIA_REGION_AND_M0_OWNER_DECISION_GATE.md)
- [SOS fallback](SOS_ESCALATION_AND_INDEPENDENT_DELIVERY_DESIGN.md)
