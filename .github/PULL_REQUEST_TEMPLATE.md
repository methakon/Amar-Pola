## Summary
Describe the change, target requirement/ADR ID and expected safe user outcome.

## Scope and reality
- [ ] Feature implementation / bug fix / docs only clearly identified
- [ ] Does not imply unimplemented Android, C++ or media capability exists
- [ ] No real child/family identifiers, GPS or media in code, tests, logs or screenshots

## Verification
- [ ] Existing M1 OpenAPI structural lint checked when relevant
- [ ] Synthetic PostgreSQL family/child RLS tests checked when relevant
- [ ] Android/C++ unit/integration tests run if projects exist
- [ ] Explicitly note tests NOT RUN and why
- [ ] Figma and documentation/API/SQL traceability updated as needed

## Security, privacy, compatibility
- [ ] Scope and permission gates maintained; cross-family/same-family-negative tests included
- [ ] Indian DPDP / Google Play/Families release gates considered
- [ ] Signing keys and credentials not committed
- [ ] New external dependencies and licenses entered into dependency/SBOM register
- [ ] Backup, incident response and retention/deletion implications noted

## Approval
Identify backend, Android, security/privacy and owner review as required by CODEOWNERS and branch rules. No automatic claim of signoff.
