# Google Play Billing sandbox setup — safe owner handoff (no secrets)

**Date 2026-10-29. Status: setup checklist only; no API connection, license test, product or purchase verified.** Owner reports active Personal Play developer account. Never put account ID, private keys, OAuth refresh tokens or payment details in GitHub or chat.

## Phase A: No credentials needed

1. In [Play Console](https://play.google.com/console) open each Android app (Madalasa parent; Alarka child if billing depends on it). Record whether they exist, their **package names**, track readiness and whether developer account production access or closed-test requirement is pending. **Do not record the developer Account ID in public files.**
2. Under **Monetize with Play → Products → Subscriptions** (navigation varies), inspect support for **nonrenewing prepaid** base plans (public ₹99 monthly/₹999 yearly targets, qualifying first 1,008 paid families ₹50/₹500). Determine if eligible prepaid offers can be retained for added child seats or require distinct one-time/seat capacity products. Do not promise implementation before verified Console configuration.
3. Under **Monetize with Play → Products → In-app products / One-time products**, inspect a repeatable consumable for proposed ₹100 extra premium viewer lasting **100 calendar days managed on the backend**; Play native 100-day Rent period is not available. Do not purchase or activate unsupported audio/video functionality.
4. Under **Settings → License testing** (or current equivalent), add designated sandbox tester Google accounts. Billing test purchases require an installed test-track build linked to the real app/package and a compatible Play setup. Provide **test email aliases only if comfortable**, not credentials/passwords.

## Phase B: Backend purchase verification (needs owner-managed access, never pasted into chat)

1. In [Google Cloud Console](https://console.cloud.google.com/), create/select an isolated project. Go to **APIs & Services → Library** and enable **Google Play Android Developer API**.
2. In **IAM & Admin → Service Accounts**, create a dedicated service account for verification, not broad publisher/editor access.
3. In **Play Console → Users and permissions**, invite that **service-account email**. For server-side billing verification Google currently documents **View financial data, orders, and cancellation survey responses** plus **Manage orders and subscriptions**. Restrict to relevant apps where possible. Do not give account administrator/publishing capabilities.
4. Use **short-lived tokens through trusted server identity/workload identity** where supported, or securely hold any service-account key in a **local encrypted secret manager/outside Git**, never in conversation, Figma, public GitHub, screenshots or CI logs. Rotate and revoke a key if exposed.
5. To test, owner (or authorised operator) can run the app's Play Billing test purchases locally; backend verifies signed purchase tokens via Google Play Developer API using the protected service account. Google purchase tokens must be verified server-side with idempotency, refund/revocation and expiry handling; never grant entitlements solely from client billing callbacks.
6. Optional **Real-time developer notifications** require Google Cloud Pub/Sub topic, publisher permissions and receipt validation. Save only safe **project ID, topic name, subscription name**, not key material, in task planning.

## Safe nonsecret details to share with ChatGPT for planning

- App package name(s), whether apps have been created in Console and test tracks enabled.
- Personal account **creation-date category** (before/after 2023-11-13), any production-access/device-verification tasks showing in Console.
- Google Cloud **project ID** and **service account email** (not keys), if you want step-by-step review.
- Proposed Play product IDs and base plan IDs, and whether they are ACTIVE/DRAFT.
- Whether license tester configuration is finished; test outcome/error codes with token values redacted.

## No need to provide

Passwords, 2FA codes, developer account ID, service-account JSON, private keys, OAuth client secret/refresh token, raw purchase tokens, personal card or banking details, child/parent real profile data.

Official setup: https://developers.google.com/android-publisher/getting_started ; permissions: https://support.google.com/googleplay/android-developer/answer/9844686 ; billing test: https://developer.android.com/google/play/billing/test .
