# Documentation Tools & Validation Scripts

This directory contains automated scripts and validation suites for maintaining documentation structure, link integrity, and reorganization compliance.

## Tools and Validators

- [`backend/tests/check_document_structure.py`](../../backend/tests/check_document_structure.py): Validates canonical document paths, relocation manifest integrity, phase index completeness, and navigation link resolution.
- [`backend/tests/check_erd_references.py`](../../backend/tests/check_erd_references.py): Enforces referential integrity across all entities and foreign key targets in the logical ERD models.
- [`backend/tests/lint_openapi_m1.py`](../../backend/tests/lint_openapi_m1.py): Verifies structural compliance and operation schemas for the M1 OpenAPI specification.
- [`backend/tests/lint_openapi_full.py`](../../backend/tests/lint_openapi_full.py): Cross-verifies the 171-operation whole-project OpenAPI specification against audited Figma screens and database tables.
