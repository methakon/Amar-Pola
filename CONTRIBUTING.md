# Contributing to Madalasa–Alarka

The project is in **design/M1 contract and synthetic database test stage**. It is **not** a deployed child monitoring system. Before proposing work, read [SRS](docs/SRS.md), [Blockers](docs/BLOCKERS_AND_OWNER_DECISIONS.md), [Developer Onboarding](docs/DEVELOPER_ONBOARDING_AND_CODING_STANDARDS.md), [Security](SECURITY.md), and [License decision](docs/LICENSING_DECISION_AND_IP_REGISTER.md).

## Contributions
1. Open a scoped issue (feature/bug), referencing requirement ID, acceptance tests and a privacy/security impact statement. Do not post real children's information, GPS, screenshots or credentials.
2. Branch `feature/<issue>-slug`, `fix/<issue>-slug`, or `docs/<issue>-slug` from current `main`; keep patches reviewable.
3. Run existing M1 Python structural lint and PostgreSQL synthetic RLS tests following [Build and Run](docs/BUILD_AND_RUN.md). New Android/C++ tests become mandatory **when source projects exist**.
4. Update SRS/ADR, OpenAPI, SQL migration and test traceability together if you change behavior. Never weaken child-scoped grants or OS privacy controls.
5. Open a PR using the template, disclose dependencies/licenses, tests performed/not run, target-SDK impact, data collected and new permissions.
6. Obtain designated backend, mobile and security/privacy review as applicable; no self-approval of high-risk changes.

Do not add covert capture, Android permission bypasses, raw children's media/position to CI, or undocumented child-monitoring features. Report vulnerabilities **privately** via [SECURITY.md](SECURITY.md), not issues.

**Licensing:** root LICENSE is an interim rights-reserved notice, not an approved open-source contribution agreement. Ownership and contribution terms require owner/legal approval. Do not infer a CLA or assignment from this document.
