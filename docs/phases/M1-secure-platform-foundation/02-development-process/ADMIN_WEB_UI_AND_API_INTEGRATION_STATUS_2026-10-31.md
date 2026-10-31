# Admin-web implementation status — 2026-10-31

**Branch**: [admin-web](https://github.com/methakon/Madalasa-Alarka/tree/admin-web) (workstream only, not merged to dev/main). **Data**: exclusively local synthetic examples in opt-in development preview, no child data or real credentials. **Status**: React/TypeScript UI **implemented**, typed admin OpenAPI request adapter, UI build/testing; **backend authentication and admin CRUD integration NOT implemented**. No claim of usable production administration.

## Figma screen alignment

The real [Figma back-office page](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=105-2) has **10 screen variants**: BO-01, BO-02, BO-02V, BO-03, BO-04–BO-09. The implementation draws on primary Figma design-context observations of BO-04, BO-06 and BO-09, plus the checked-in [admin page registry](../../../ui/figma-functional-handoff/10-admin-back-office.json): navy #223952 sidebar; cream #fbf7ee workspace; pale-green summary and peach security panels; accessible cards and responsive layout.

| Figma screen | Frontend route/view | Data integration |
|---|---|---|
| BO-01 | Google entry and no-access screen | Google GIS callback is wired to POST /v1/admin/auth/google but unavailable until trusted backend bootstrap, CSRF cookie and OIDC verification exist |
| BO-02 / BO-02V / BO-03 | Applicant profile, email verification, request status | Typed PUT/POST access-profile and email endpoints; submit remains **disabled** until backend verified profile revision and allowed action exist |
| BO-04 | Owner access requests/decision pane | GET/POST admin owner routes; app never grants roles based on UI input. Live approval needs MFA and authoritative revision |
| BO-05 | FAQ list/editor/revision publishing | GET/POST/PUT, publish endpoint adapter; publish disabled in synthetic mode and needs server revision handling |
| BO-06 | Ticket inbox/reply | GET and ticket reply adapter; no private child media |
| BO-07 | Subscribers and billing | GET metadata list, no raw payment secrets; deeper payment screen pending backend |
| BO-08 | Parent service usage | Privacy summary and access boundary; detailed usage list **NOT implemented** pending correct response/pagination contract |
| BO-09 | Security overview/audit/roles | Audit endpoint adapter, strict roles and child-private-data wall |

No direct admin device/location media routes are permitted in the frontend API client. Read requests only run after an authenticated server session is accepted. Empty/failed server responses are **never replaced with fixtures** in normal mode. Synthetic preview needs VITE_ADMIN_SYNTHETIC_PREVIEW=true **AND** Vite DEV; mutations are disabled and examples are visibly labeled.

## Technical files

- [React application](https://github.com/methakon/Madalasa-Alarka/blob/admin-web/admin-web/src/main.tsx)
- [CSS and responsive design](https://github.com/methakon/Madalasa-Alarka/blob/admin-web/admin-web/src/styles.css)
- [Admin API adapter](https://github.com/methakon/Madalasa-Alarka/blob/admin-web/admin-web/src/api.ts)
- [Synthetic-only fixtures](https://github.com/methakon/Madalasa-Alarka/blob/admin-web/admin-web/src/fixtures.ts)
- [Run instructions](https://github.com/methakon/Madalasa-Alarka/blob/admin-web/admin-web/README.md)
- [Node build workflow](https://github.com/methakon/Madalasa-Alarka/blob/admin-web/.github/workflows/admin-web.yml)

## Genuine integration work still required (not waived)

1. C++ Drogon admin-session authentication: cryptographically verify Google ID token signature, exact issuer/client audience, expiration, nonce, email_verified, provision verified owner *issuer + sub* through secure bootstrap; HttpOnly Secure SameSite admin session and CSRF token. Do not use unverified email in the UI as authority. Separate owner MFA step-up for admin approvals.
2. Versioned authoritative admin APIs/database policies for applicant/profile/email status, owner review and staff grants, FAQ revisions, ticket interactions/delivery, subscriber masked ledger, parent usage and append-only access audit. These endpoints currently live in **docs/openapi.yaml** (design only), not the 14 registered M1 Drogon routes.
3. Fix contract mismatches before asserting complete integration: GET owner requests currently documents one AdminAccessRequest but list screen expects a page; GET parent usage returns one event; owner decision needs a server revision; FAQ publish requires a distinct versioned revision_id. No browser-only workaround that fabricates success.
4. Test API errors, unauthorized staff/owner, stolen/revoked sessions, forged CSRF, wrong tenant, masked billing and no child private-data responses. No production admin release before these tests pass and code is reviewed into dev.
5. For visual QA, locally run Vite and compare screenshots to Figma. Source-level color/layout comparison is documented, not pixel-by-pixel browser acceptance.

## Synthetic local commands

From repository root: cd admin-web; npm install --no-audit --no-fund; VITE_ADMIN_SYNTHETIC_PREVIEW=true npm run dev. Run npm test and npm run build. No secret or real user-data fixture required.
