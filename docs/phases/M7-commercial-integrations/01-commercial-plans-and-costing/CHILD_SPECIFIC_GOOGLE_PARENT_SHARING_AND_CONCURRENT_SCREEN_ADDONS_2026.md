# Child-Scoped Google-Parent Sharing, Concurrent Viewer Screens and ₹100 Manual Add-on

**Owner requirement 2026-10-28. Status: product design direction; GOOGLE AUTHORITY VERIFICATION, Play pricing and Android capability are UNPROVEN. No billing/stream enforcement is implemented.** Supersedes earlier family-wide implicit sharing language; see [Two-parent prepaid baseline](TWO_PARENT_SHARED_CHILD_PREPAID_ENTITLEMENTS_2026.md). Launch UI English only; pan-Indian Markandeya Purana-inspired Theme C graphics.

## A. No automatic sharing across blended families

The payer may have multiple children attached to their profile from different parental relationships. **Never** automatically reveal all payer-linked children to a co-parent, other spouse, or another Google family group member. Sharing is **per verified child ID AND per permitted adult ID**. Default for new child is **no co-parent access**, including previously invited parents, unless approved for that specific child.

- Primary paying parent chooses one or several children to assign **paid seats** up to verified prepaid child-seat capacity, and **separately** selects which child can be shared with which verified co-parent. Payment is NOT a permission grant.
- Share flow lists only payer-authorized children. Each row includes **Paid seat selected?** and **Share with Parent B?** as separate settings. Parent B only sees allowed children, not total family roster or undisclosed siblings.
- Co-parent account must have a personal Google Account signed in (OAuth ID token verified server-side, audience/issuer/expiry checks). Google Sign-In **proves identity only**, not parental authority or a Family Link parent role.
- [Google Family Link supports an additional designated parent in a Google family group](https://support.google.com/accounts/answer/7295768), but **no independently verified supported public API for arbitrary third-party apps to query/attest the parent–child Family Link relationship has been found**. **HARD LAUNCH GATE:** product owner requested *only Google-supported parent accounts*. Until we have an approved evidence/verification method that establishes the **specific adult + specific child's** current parent status, the "Share access" action must remain **Unavailable — verification integration pending**. Do not pretend that Google Sign-In, email similarity, family surname, a screenshot alone, group membership or manually asserted relationship is proof. Evaluate permitted official integration or a lawful independent authority process with product-owner signoff before enabling. If Google does not expose that integration, inform owner that strict automated enforcement is impossible and request an explicit policy change; do not silently relax eligibility.
- Google families can generally belong to **one family group at a time**; verify practical Family Link support for blended families across groups and age/region restrictions. Never assume a biological or legal parent is automatically in the same Google group.
- On any verified parent-role removal, divorce/authority change, guardian grant revocation, child removal or account deletion: revoke only affected adult-child grants, sessions, signed URLs and cached snapshots; **other children and the payer's prepaid billing remain independent**.
- Child-side transparency: when child is capable of seeing it, show the specific authorized guardian names and effective data/capture privileges. Legal adult authority and child privacy constraints still require independent review.

## B. What "one screen at a time" means here

**Working implementation interpretation:** The included plan allows **one concurrent active premium remote-monitoring *viewer screen/session* per paid child** across all authorized guardians/devices. A "screen" is NOT a paid child seat, not a whole Android handset, and not a Google Family Link screen-time restriction. Switching between app tabs within the same signed-in device does NOT consume extra slots. Viewing static account settings, trial purchase details, parental safety notices, child-initiated SOS or other essential free/accessible features must NOT be blocked by this cap. Capturing/streaming the child's device screen is a SEPARATE Android MediaProjection-per-session feature and remains gated.

- On an active premium live-map or authorized live-media screen, acquire a server-issued **viewer lease** scoped to `child_id`; one lease per active viewer principal/device. Leases are not client-created entitlements.
- Capacity: `1 included + purchased_valid_additional_slots(child_id, now)`; **never** multiply the included slot just because a second parent logs in.
- For a second simultaneous viewer beyond capacity, display **“Another authorized viewer is active for this child.”** Actions: **Retry**, **Ask to take over** (send in-app request; do not silently eject the other parent), or **Add another screen** (payer only, if add-on eligible/available). A connected session may voluntarily release on page close/switch. Prefer clear `VIEWER_LIMIT_REACHED` API response, not fake network or media failure.
- Server's atomic lease algorithm must reject racing device requests. Candidate SQL transaction/Redis Lua: verify child-specific grant/feature flag/base plan active, count unique nonexpired leases by child, compare with eligible capacity, insert lease with 60–90s TTL and unique `child_id, adult_id, device_session_id`. Clients heartbeat every ~20s; disconnect/revoke/expiry releases or TTL expires. Lease renewal always rechecks payment, adult-child grant, child status and capture legality.
- No sharing authenticated tokens or devices to bypass slots; use per-device sessions, playback signed URLs with audience/session binding, WSS authentication, expiring child-scoped WebRTC tokens and relay admission control. Do not count idle/settings pages as live sessions, and do not hold a lease through background app inactivity. On app reconnection preserve same lease identity without double charging; close stale sockets.
- For locations/history, the **one-concurrent-screen limit is a premium viewer policy**, not permission to deny universally promised free live location or emergency access. Define exactly what is premium monitoring and what remains free before release. If the owner instead intends *one stream per whole family* vs per child, update the model and financial calculations before implementation.

## C. Optional ₹100 additional simultaneous viewer screen — working commercial assumption

**Price target: ₹100 for EACH +1 simultaneous monitoring screen slot, for up to 30 days, manually purchased, NO recurring charge.** As the owner did not specify its duration, **30 days is an implementation proposal, NOT a final approved term**. A purchased slot ends at `min(purchase_activated_at + 30 days, relevant_paid_child_prepaid_expiry)` under this candidate model. The UI must show exact expiry and **unexpired remaining validity before checkout** to avoid misleading parents with a full-month promise when their base entitlement expires sooner. No rollover; do not automatically extend or charge. Price is only final if the actual Play purchase offer shows ₹100 inclusive/exclusive of applicable taxes.

**Extra media allowance:** each extra paid concurrent screen purchase grants **30 additional combined audio+video minutes** (a single pooled balance, **NOT 30 audio + 30 video**). Shared by all authorized viewers of the **selected eligible child**; consumed after the ordinary per-child media quotas (existing paid Balanced: audio 60 min, video 20 min monthly). Additional balance and viewer slot expire together; refund/void revokes unused allowance. Screen-viewing time and photo snapshots are **not** increased by this add-on. Live audio/video/screen are still restricted features pending legal, Android and Google Play gates; the add-on must not be sold as an audio/video unlock unless those capabilities actually ship.

**No paid add-ons during the free 48h intro or when paid child entitlement is expired**, unless a different explicit product is approved. On base plan expiry, all parent premium sessions and additional screen slots stop; parents retain approved free tracking. Extra screens are not purchased per adult; capacity floats between **authorized** guardians for only that specific paid child.

**Google Play integration candidate:** A separate repeatable **one-time consumable** SKU `extra_viewer_30d_plus30_av_100_inr` using Play Billing; server verifies PURCHASED, amount/offer, purchaser account and unique purchase token, binds purchased unit to specified paid child with idempotent grant, consumes on backend after delivery, and processes RTDN, refunds, chargebacks and expiry. Google also supports time-bound one-time *rent* products; evaluate which method handles stacking multiple units and the shorter of 30 days/base entitlement. **Subscription add-ons are NOT suitable because Google currently limits them to auto-renew plans**. A non-consumable/permanent SKU is wrong. Multiple quantities or one-time repeatability need Play sandbox verification; do not rely on a purchase count solely from the Android client.

**Pricing economics gate:** ₹100 is a proposed total customer price, *not net proceeds*. Recalculate GST/Google fee, TURN/WebRTC fan-out (each extra viewer increases egress), concurrency, abuse and support. Establish maximum extra slots per child after load tests (candidate hard cap two add-ons, giving 3 total viewers), no unlimited sessions.

## D. Quota and lease examples

| Scenario | Concurrent premium viewers allowed for Child A | Audio/video extra pool | Effect |
|---|---:|---:|---|
| Parent A pays for Child A; one permitted guardian | 1 | 0 | Either parent may use the slot, not both simultaneously |
| Both parents open Child A at once, no add-on | 1 | 0 | Second gets viewer-limit explanation and takeover request |
| Payer buys one ₹100 slot add-on for Child A | 2 | +30 min shared combined | Both authorized parents can simultaneously view approved premium screens |
| Payer buys second eligible ₹100 slot add-on for Child A | 3 | +60 min shared combined | Only if approved max capacity/Play allows |
| Parent B is authorized for Child A but not Child B | Child B: 0 regardless of purchase | Child B: 0 | Child B never appears in Parent B's accessible roster |
| Base prepaid plan expires for Child A | 0 premium; free basic allowed | 0 paid extra | No auto charge or automatic trial reset |

## E. Suggested API and storage extension (implementation not performed)

```text
guardian_child_grant(child_id, adult_id, relationship_verification_status,
  verification_method, verification_expiry, scopes, revocation_epoch)
paid_child_entitlement(child_id, family_id, purchased_capacity, expiry)
concurrent_screen_addon(id, child_id, purchase_token_hash, payer_id,
  slots=1, extra_av_seconds=1800, activated_at, expires_at, state)
viewer_lease(id, child_id, adult_id, device_session_id, screen_type,
  acquired_at, renewed_at, lease_expires_at, entitlement_revision)
child_media_pool(child_id, period_key, base_audio_seconds, base_video_seconds,
  extra_flexible_av_seconds, consumed_flexible_av_seconds)
```

Server admission must check both **eligible viewer screen capacity** and **guardian-child permission**. Use one atomic metering ledger for both parents; split duration use with continuous verified server evidence, never deduct for rejected OS requests. Abort live capture at revocation/expiry/permission change; minimize data and do not increase storage retention due to extra viewer payment.

## F. Screen acceptance (Theme C English only)

- **SH-01 Child selection & co-parent sharing:** per-child separate toggles for paid seat and adult-specific sharing. Child B not automatically shared; disabled verified Google-parent-only gate.
- **SH-02 Verification pending:** Google Sign-In completed, parental relationship unverified; no premium data shared and no simulated Google-connected green check. Explain why.
- **SH-03 Viewer in use:** one included slot; parent A viewing; parent B requests takeover or payer reviews extra-screen option. No cross-child names/leaks to unapproved adult.
- **SH-04 Add extra screen:** exact Play checkout price (₹100 target), count +1 simultaneous viewer, 30 combined audio/video minutes, expiration, no auto-renew, explicit parent confirmation, child assignment.
- **SH-05 Family coverage summary:** permitted parents view only approved children and remaining shared quota; other children stay unshared/free.
- Preserve existing P-39/P-40/P-47/P-48/P-49/P-54 contract; do not replace existing Figma handoff or imply functional UI from mockups.

**Google policy references:** [Family Link parent privileges](https://support.google.com/accounts/answer/7295768), [Google family groups](https://families.google/intl/en_in/families/), [Google Play prepaid subscriptions and add-ons](https://developer.android.com/google/play/billing/subscription-with-addons), [one-time products](https://developer.android.com/google/play/billing/one-time-products), [one-time purchase lifecycle](https://developer.android.com/google/play/billing/lifecycle/one-time), [secure purchase verification](https://developer.android.com/google/play/billing/security).
