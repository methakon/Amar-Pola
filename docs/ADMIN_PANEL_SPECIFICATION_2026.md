# Madalasa–Alarka — Administrator Console Functional & Technical Specification

**Document:** MA-ADMIN-001 | **Date:** 2026-10-27 | **Status:** NEW DESIGN / NOT IMPLEMENTED.  
**Requested module:** administrator access to **media activity metadata only**, with name/ID autocomplete, parent/child filters, date range, results with server pagination, verified failures, and audited access.  
**Companion:** [Media Activity Audit System ADR](MEDIA_ACTIVITY_AUDIT_LOGGING_AND_REPORTING_2026.md), [SRS FR-050/FR-051](SRS.md), [security and operations](SECURITY_AND_OPERATIONS.md), [whole-project draft API](openapi.yaml).  
**Implementation target:** Separate authenticated **web back office** backed by existing C++20 Drogon API + PostgreSQL; no bundled admin powers inside Alarka/Madalasa Android apps. UI technology remains TBD; Figma is implementation handoff.

## 1. Access model (non-negotiable)

| Role | Aggregate counts/health | Named parent/child media log | Log-detail | View admin access audit | Export |
|---|---|---|---|---|---|
| SUPPORT_AGENT | Limited anonymized aggregates for assigned queue | **NO** by default | NO | NO | NO |
| CASE_SUPPORT_REVIEWER | Scoped read under approved case and step-up | Only parent/child in case | Redacted reasons/size/duration | NO | NO by default |
| SECURITY_AUDITOR | Case-authorized incident scope only | Bounded investigative read | Read-only/redacted | Yes within security scope | Exceptional + second approval |
| PRIVACY_OFFICER | Lawful request / consent/deletion reviews | Per approved data-subject case | Redacted as required | Yes for appropriate case | Controlled data subject workflow |
| ROOT_OPERATOR | System operations/config only, not default data access | **NO** by role alone | NO | NO | NO |
| BREAK_GLASS | Exceptional, time-limited, MFA, justified and dual-authorized | Strictly emergency case scope | Read-only as necessary | Access recorded and reviewed | No automatic export |

Even product owner/root administrator does **not** automatically gain a universal list of children or recordings. Permission `MEDIA_AUDIT_READ` is additional to general admin login and requires case-bound scope. Never grant sensor activation or direct media viewing via this console. Enforce on every API request and parent/child autocomplete. No reliance on hiding UI elements or a browser-sent `role` field.

## 2. Screens and navigation (editable design)

Desktop navigation: **Overview | Media Activity | Cases & Access | Access Audit | Retention & Privacy | Settings (ops only)**. Every screen shows environment (`DESIGN / NOT LIVE` in mockups), current authorized role/case, last refresh, permissions and safe empty/error behavior.

Planned UI screens and behaviors:
- ADMIN-01 Login + MFA/step-up, session expiry and role.
- ADMIN-02 Limited overview (counts of requests/failures, no child identities by default).
- ADMIN-03 Case access selection/justification; support case ID, purpose code, expiry, supervisory approval where required; controlled submit.
- ADMIN-04 Media Activity table; searchable parent **name/ID** typeahead, child **name/ID** typeahead dependent on parent, date from/to, type, action, outcome, failure code, page size, cursor/page navigation and result count.
- ADMIN-05 Parent autocomplete dropdown, minimal matches restricted to approved case scope, disabled with explanatory state if access missing.
- ADMIN-06 Child autocomplete, parent-constrained options, names+masked IDs and no enumeration across families.
- ADMIN-07 Media record detail drawer with lifecycle timestamps, media_kind, duration, nullable size, bytes transferred, saved vs viewed, reason evidence, no playable file.
- ADMIN-08 Failure detail / reason code dictionary with source confidence (Android camera in use, silenced audio, service-start blocked, offline unknown).
- ADMIN-09 Filtered empty and no-permission results: disambiguate zero matching items vs case access denied.
- ADMIN-10 Page navigation and loading/network failure / cursor expiry/retry states.
- ADMIN-11 Admin access audit trail (authorized security/privacy role), filter by actor/case/date, no hidden audit disable.
- ADMIN-12 Role/purpose/retention controls (read-only until counsel/owner has chosen values; no unauthorized raw admin update).
- ADMIN-13 Session expired / step-up required security screen and re-authentication.
- ADMIN-14 Access denied / cross-tenant request and case expiry screen.

Parent mobile companion screens indexed separately cover name-based child dropdown, date range, pagination, result details, failure reasons, saved/viewed and offline/empty states.

## 3. Search & UX specifics

Parent selector: required or "All permitted parents in this *authorized case scope*" only if case type allows it; supports ID exact/prefix and name text. Child selector: required or "All children within selected/approved parent" and clears when parent changes. Date selector: default latest 7 days; date-time stored UTC; UI localized and server uses [from inclusive, to exclusive). Media type AUDIO / IMAGE / VIDEO_AV / SCREEN_SHARE; action LIVE_VIEW / SNAPSHOT / RECORD / SAVE / REQUEST; outcome VIEWED_ONLY / SAVED_PARENT_LOCAL / FAILED / CANCELLED / EXPIRED / UNKNOWN; reason code dropdown. Pagination: default 20, max 100, opaque keyset cursor and page number indicator per loaded cursor history. Search on server only; debounce 250–400ms, minimum 2 characters for names, exact UUID on ID, 10 suggestions max, match highlighting. When no authorization, do not enumerate users via timing/count differences. Admin pagination never allows access to children outside case.

Case state pill always visible; CTA "Request case access" when missing. Record detail has explanatory "No recording or media file is stored on the server." A saved marker denotes historical parent confirmation, not a retrievable server media file. Render nullable size as "Not applicable" or "Not confirmed", never 0 B unless a verified zero byte result.

## 4. Data access, audit and backend

Proposed APIs (whole-project **draft**, not M1): `GET /v1/admin/media-activity`, `GET /v1/admin/media-activity/{id}`, `GET /v1/admin/media-activity/parents/suggest?q=...`, `GET /v1/admin/media-activity/children/suggest?q=...&parent_id=...`, `GET /v1/admin/media-activity/access-audit`. Admin token is separate `AdminBearer`, with audience `madalasa-admin`, step-up MFA signal, server-owned role/case and time-limited access. A case-service grant is stored server-side, never in user query params alone. The server may return 403 for case denied, 401 for expired session, 422 for invalid date, 429 for autocomplete throttling; clients show corresponding safe screen.

Admin detailed parent/child lookup and suggestion/read APIs must insert an **admin access audit**: actor, case/purpose, query scope (minimized), UTC time, status, result count, request ID. Audit writes should not be suppressible by the administrator accessing records; on audit persistence failure, fail closed for detailed reads. Root operator may work on infrastructure without inheriting child data privileges. Routine support only redacted aggregate views. IP addresses and session device metadata are restricted separately and should not be default analytics columns.

Architecture: web UI ─[short-lived admin session, CSP, MFA]─> Drogon admin authorization middleware ─> case/purpose gate ─> PostgreSQL RLS/authorized query views ─> projection-only metadata. Append-only access audit on privileged lookup; no `SELECT *` across family datasets. Admin endpoint never accesses TURN media buffers, local parent files, or child sensor activation.

## 5. Operator functionality outside the media log

This document establishes the **new admin-console foundation** to avoid assuming that a broader panel already exists. Initial scope should include admin user/role provisioning (authorized), support case access approval/expiry, privacy/retention settings **read-only until signed decision**, media metadata log list and access audit, system health/redacted support diagnostics. Billing administration, family transfer, user deletion, incident response and app-content policy review are **future separate modules**, not implied by this media-log request.

## 6. Security, privacy and operational gates

- Audit support case justification, access request, approvals, detailed searches, suggestions, exports, incident logs and break-glass. Retain searchable admin audit separately from media-session event log.
- Step-up access, expiring case grants and dual control for unusual breadth; never infer guardian authority from an admin credential. Support customer identity resolution without exposing child name suggestions to an ordinary operator.
- Server-side least privilege, anti-CSRF (for cookie-based admin), safe Content Security Policy, rate limiting, query budgets, no media files or URLs, strict HTML escaping and authorized sort/filter columns.
- Purpose limitation, India DPDP child-data law counsel review, audit retention, account deletion and break-glass process must be decided before real data is collected. DO NOT ship admin media search just because synthetic Figma mockups exist.
- Operational: request-bound query timeouts, parent/child/time indexes, safe max row-size, keyset pagination and automated tests for cross-family access. No arbitrary wildcard admin exports.

## 7. Test cases (design, NOT TESTED)

- T-ADM-01 login, MFA and step-up enforce admin session audience.
- T-ADM-02 routine SUPPORT_AGENT cannot enumerate named parent/child records.
- T-ADM-03 case-scoped role may view only approved parent-child IDs within active case.
- T-ADM-04 parent autocomplete by masked ID/name honors case scope, min-length and rate limit.
- T-ADM-05 child autocomplete is parent-constrained and denied out of case.
- T-ADM-06 date UTC bounds, type/action/outcome/failure filters and pagination work together.
- T-ADM-07 record detail never includes binaries/file URLs/content/filename.
- T-ADM-08 admin search, read, suggestion and export attempts create access-audit row.
- T-ADM-09 audit-store failure fails closed on detailed read.
- T-ADM-10 expired case, role removal, session expiry and guardian revoke invalidate pagination/caches.
- T-ADM-11 exports require legal basis/dual approval or stay disabled.
- T-ADM-12 break-glass requires a separate bounded grant and post-incident review.
- T-ADM-13 denied/no results/load failure distinguishable and accessible.
- T-ADM-14 no raw child data pilot before counsel/Play approval.

## 8. Developer handoff

The existing Figma file will contain a separate **MEDIA AUDIT • Parent + Admin** page with editable parent mobile screens and administrator desktop views, plus HLD/LLD on the shared architecture page. A node-level index belongs in [07-media-activity-audit.json](ui/figma-functional-handoff/07-media-activity-audit.json). No existing admin Figma panel was found in the inspected file; these admin screens are a **new design**, not an already deployed dashboard. Existing 81 functional Android screens and capability onboarding designs remain unchanged.

**Owners to assign:** Backend/security, Android parent app, admin web frontend, database, QA, product, privacy counsel, Google Play review. **Release:** research gated; no release claims.
