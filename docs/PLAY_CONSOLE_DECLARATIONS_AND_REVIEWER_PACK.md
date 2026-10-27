# Google Play Console Declarations, Families Outcome and Reviewer Demonstration Pack

**Status:** Preparation checklist only. No Play Console developer account/declarations, reviewer video, app bundle, package IDs or actual Families policy determination exist. No claim of Play approval. Date 2026-10-27.

## Products
Parent app **Madalasa**, child app **Alarka** if independently distributed. Both require separately accurate app purpose, target audience, app category, privacy notice, Data Safety answers, permissions and app behavior; child monitoring manifest and parental-use restrictions are distinct.

## Policy review gates
- Determine **eligible monitoring app category**, app identity and child monitoring declaration (`isMonitoringTool=child_monitoring` where required), recognizable launcher icon, prominent disclosure and monitoring notification. Covert activation/bypass/hidden indicator prohibited.
- Android current target SDK, background location declarations, prominent in-app disclosure, runtime permission screens, microphone/camera/background FGS and MediaProjection per-session consent. An initial setup grant doesn't permit silent remote media capture.
- Play **Families** and under-18 target audience determination: independent verification needed; privacy and advertising policies, third-party SDK requirements, account deletion and permissions/child data restrictions. A parent audience does not automatically remove all child-data obligations.
- App usage tracking and historical precise child location have separate India DPDP child monitoring risk. Keep prohibited/unapproved features OFF even if Android permissions granted.
- Play Billing subscription auto-renewal, upgrade/cancel, price and taxes; refund route should follow actual merchant/operator rules.
- API data safety include account/child IDs, device permission metadata, local GPS queue and temporary PostgreSQL inbox, app usage intervals, media-event audit metadata and admin access logs—**no VPS media files does not mean no user data**.

## Reviewer artifacts (must be created from real signed builds)
1. Alarka setup, adult verification and child/family device pairing, visible icon and purpose disclosure.
2. Live compatibility inventory (read-only) and Android-owned permission wizard with Android 11+ foreground → separate background location.
3. Accurate "supported/granted/conditional/unavailable/stale" screens; revocation/reapproval and device offline demonstration.
4. Parent Madalasa current and historical GPS route, 48h backfill **using approved synthetic/test device identities**; real p95/sync expectations and route gaps.
5. Media features OFF/research unavailable, no mock claim of working background microphone/camera in actual release.
6. Parent admin media audit names/scopes and child-safety privacy explanation, admin case gate if relevant.
7. Deletion/unpair/guardian revoke, consent, complaint contact, subscription cancellation and policy page links.
8. Screen recording and captions in appropriate language, signed build version, app bundle ID, review account, reviewer login (private secure channel), reviewer declaration IDs.

## Evidence register
| Artifact | Status |
|---|---|
| Parent and child package IDs and manifest permission matrix | MISSING |
| Signed AAB/APK, versionCode and release certificate | MISSING |
| Live Play Console declaration screenshots | MISSING |
| Families policy review/decision | NOT ASSESSED |
| Background location declaration/video | NOT SUBMITTED |
| Reviewer demo video and approved review credentials | NOT CREATED |
| Approved public privacy, terms, refunds, deletion pages | NOT PUBLISHED |
| Age/region/publisher legal signoff | BLOCKED |
| Verifiable parental consent and abuse reporting | NOT IMPLEMENTED |

## Release decision
Production NO-GO until owner/product, Android, security, India legal counsel and actual Google Play Console declarations/reviewer approval are on record. The Figma screens and reference policy docs are **not** reviewer video evidence.
