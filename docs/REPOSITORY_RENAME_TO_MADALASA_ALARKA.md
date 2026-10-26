# GitHub Repository Rename — Madalasa-Alarka

**Requested by project owner:** 2026-10-26  
**Status:** **REQUIRES GITHUB ADMIN — NOT EXECUTED**  
**Current working repository:** https://github.com/methakon/Amar-Pola  
**Desired repository:** `methakon/Madalasa-Alarka`  
**Parent Android launcher name:** **Madalasa**  
**Child Android launcher name:** **Alarka**

## Exact action for repository administrator

1. Open the actual repository: https://github.com/methakon/Amar-Pola.
2. Open **Settings** → **General** → **Repository name**.
3. Enter `Madalasa-Alarka` and select **Rename**.
4. Verify the new repository actually exists at `https://github.com/methakon/Madalasa-Alarka`. Do not update public repo references until verification.
5. Update local clone remotes: `git remote set-url origin https://github.com/methakon/Madalasa-Alarka.git`.
6. Recheck GitHub Actions, GitHub App permissions and connected links for the renamed repository. Any GitHub Actions configuration containing hardcoded old repo URLs must be reviewed; same for CI badges, external integrations, webhook endpoints, issue links and docs bookmarks.
7. Replace active GitHub links containing `github.com/methakon/Amar-Pola` with the verified new URL, including UI handoff, legal/pricing references, third-party docs and Eraser/Figma indexes. GitHub often provides redirects, but exact behavior should be verified.
8. Do **not** automatically change Android `applicationId`, signing keys, OAuth client IDs, Play Billing product IDs, backend auth audiences, database migrations or API paths; these require independent compatibility planning.
9. Keep a short note of the historical repository name for old citations and developer searchability.

## Why this is not executed automatically

The currently connected GitHub app can **edit files** and commit to the repository but the confirmed repository permission set is `admin:false, push:true`; there is no available repository rename tool. The new URL has **not been confirmed**, so this document deliberately uses the existing URL for working links until an admin renames the repository.

Brand rationale and English Markandeya Purana story: [Madalasa and Alarka product concept](BRAND_NAME_MADALASA_ALARKA_AND_MYTHOLOGY_CONCEPT.md).

**No repository recreation or copy is an equivalent substitute for an in-place rename:** copying creates a new repo with different issue/PR/history permissions and integrations and should not be undertaken as if it were a rename.
