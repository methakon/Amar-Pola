# Amar-Pola — Subscription Plans, Hidden Charges, Compliance Rules and Revenue Model

**Document:** AP-SUB-PRICING-001  
**Version:** 1.0 | **Prepared:** 2026-10-26 | **Status:** PROPOSED FOR OWNER APPROVAL — not live Play Console products, not a binding quote, and not independently signed off by tax/legal counsel.  
**Scope:** India-first Android family safety service with a **price per enrolled paying child**, shared parent/guardian viewing, and Google Play Billing.  
**Financial references:** [Third-Party Cost Analysis](THIRD_PARTY_SERVICES_COST_ANALYSIS_2026.md) (old ₹149 sensitivity) and [Oracle Chicago Deployment & Hosting](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md). Those documents remain separate cost ledgers.  
**Requirement references:** [SRS](SRS.md) FR-012/022/039, [API](openapi.yaml), [Data Security](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md).

## 1. Decision and official product offer

**Amar-Pola's NEW recommended public price point is ₹50 per paying child per month OR ₹500 per paying child per year**, subject to Google Play Console validating the India offer/total displayed payable amount, merchant/tax setup, platform compliance and implementation of family-seat checkout.

| Term | Parent is charged | Covered service time | Renewing? | Equivalent per-child month | Effective benefit |
|---|---:|---|---|---:|---|
| Monthly | **₹50 per child** | One month | Propose **auto-renewing** | ₹50.00 | Cancel future renewal when desired |
| Annual | **₹500 per child** | Twelve months | Propose **auto-renewing** | ~₹41.67 *equivalent* | Saves ₹100 against 12 × ₹50 (16.67%) |

**Do not imply the annual plan is charged ₹41.67 monthly.** The actual recurring annual debit must be visibly shown as **₹500 every 12 months**, and the monthly as **₹50 every month**, including whether applicable taxes are already part of the visible price. The 15% fee assumption applies to an eligible **auto-renewing subscription** in India under Google's current remaining-market policy; **do not silently apply that fee to prepaid plans, alternative billing or other countries**.

No premium tier, paid camera/mic/remote capture, paid add-on or trial is approved in this document. Optional premium features must undergo separate platform/device, legal and cost gate.

## 2. What does one child subscription include?

**Proposed paid scope, subject to real Android and product release capability:** child enrollment under one approved family account, available location/latest status, observed route/trip history, parent-named places and supported alerts, child/device health/reliability information, authorized app-usage reports and manageable child-specific guardian grants. A guardian's viewing invitation does **not** add another paying child; payment attaches to a **child-seat capacity**, not a guardian login or the number of map views.

**Feature promises are gated by hardware and OS:** standard Android installation and fully managed DPC differ; OS permission rejection can make a feature unavailable even when subscription is paid. App must disclose capability before purchase; don't market unsupported controls as included.

**Noncommercial rights must always remain available regardless of payment:** view/cancel subscription, review disclosure/consent, report a problem, withdraw grants, protect/delete child data and account, request exported records where applicable, understand what monitoring is active and see accurate unsupported/offline states. Emergency/child-initiated SOS behavior must be safety-reviewed and transparent; do **not** block a previously advertised emergency feature solely because a payment retry failed without a clear plan for safe fallback.

**Not included without an explicit later plan:** guaranteed real-time location intervals or 24/7 emergency response, OS-bypass capabilities, Google Maps Roads street-level asset tracking, remote hidden mic/camera/video, bulk file extraction, watch-specific precision/SLA, Google Drive storage charges, or unlimited premium API usage.

## 3. Families with two or more children: Play Billing design blocker

**Critical constraint:** Multiple Play products can be bundled as add-ons, but **the same product ID cannot occur twice in one add-ons purchase**, and add-on items must share the same billing period and be auto-renewing; removing a single add-on independently has other lifecycle caveats. Do **not** assume one normal child subscription SKU can be purchased 2/3/4 times in the same Google billing account or repeated as identical line items.

### Recommended implementation: one family subscription with N child seats

**One paying family/account → one active family seat-count subscription** whose entitlement is an integer N. Owner selects capacity N, then securely assigns N active child profiles to those seats. A second parent/guardian can view authorized children without purchasing a second seat. This avoids duplicate identical product IDs and simplifies invoices.

**Candidate product catalog, all prices illustrative and subject to Play Console approval:**

| Active child-seat capacity | Proposed monthly family charge | Proposed annual family charge | Saving vs 12 monthly charges | Checkout representation |
|---:|---:|---:|---:|---|
| 1 | ₹50 / month | ₹500 / year | ₹100 / year | Proposed family seat product 1 |
| 2 | ₹100 / month | ₹1,000 / year | ₹200 / year | Proposed family seat product 2 |
| 3 | ₹150 / month | ₹1,500 / year | ₹300 / year | Proposed family seat product 3 |
| 4 | ₹200 / month | ₹2,000 / year | ₹400 / year | Proposed family seat product 4 |
| 5 | ₹250 / month | ₹2,500 / year | ₹500 / year | Proposed family seat product 5 |

- Create **separate Google Play subscription products for family capacity**, each with monthly and annual auto-renewing base plans. Suggested provisional IDs: family_children_1, family_children_2, ..., family_children_5. Final product IDs must be reviewed before activation; Play product IDs cannot be reused/changed after creation.
- **Initial family maximum candidate:** five child seats. Families with more than five children need product decision, new SKU(s), an approved family-wide pricing schedule or supported upgrade design. Don't imply no limit.
- A seat is activated for a verified, owner-approved child profile (not each phone/watch); multiple devices for one child still require capability, limits and fair-use design, not a second child subscription.
- Server's family active-seat count must never exceed the **current verified purchased capacity**; don't accept client text indicating more seats.
- **Increasing/decreasing N:** flow is a subscription product replacement/upgrade/downgrade. Google may calculate prorated charges or defer changes depending replacement mode; display **actual Play Billing purchase-screen amount and effective date** rather than promising a simple instant ₹50 increment.
- Mixed monthly and annual children in the *same family* are **not** included in the simple MVP seat catalog, because one family subscription has one period. Offer a clear period for the family; mixed billing requires a separate tested design.
- Canceling a family plan cancels renewal for **all child seats** after the paid period, without revoking anyone's privacy/deletion rights. Individual seat removal/child reassignment has owner confirmation, duplicate prevention and billing adjustment rules.
- Separate payment owner from child's guardian roles. Don't let a secondary guardian alter paid capacity unless delegated by the verified family owner.

**Feasibility gate:** create the products in a licensed Play Console test track and verify a real 1→2 seat upgrade, annual↔monthly switch, cancel, refund, trial/offer, resubscribe and multi-guardian access **before calling per-child billing implemented**. Alternative: distinct per-child products, but prove repeated purchase lifecycle and scalable SKU count in Play, not inferred.

## 4. Transparent charges and the difference between price and provider expense

Potentially confusing charge types must be disclosed distinctly:

| Charge or rule | Who pays / how billed | Included in ₹50 / ₹500 calculation? | Risk and control |
|---|---|---|---|
| Public subscription price | Parent payer | YES, customer-facing selected family capacity × per-child price | Display exact total at checkout and auto-renew |
| Google Play recurring service fee | **Developer** from eligible revenue; estimated **15%** India current model | Included as operating cost; **not extra charged on top of advertised app price** | Actual fee based on transaction, country and Play fee rules |
| GST / consumer tax on digital service | Responsibility depends on developer residency, market and Google tax rules | **NOT independently validated** whether chosen round number is final tax-inclusive user price | Finalize tax-inclusive Play checkout and payout reports |
| GST on Google's service fee / India tax obligations | Potential developer tax cash liability, sometimes input credit based on registration | **NOT included in flat 15%** | Check GSTIN/registration/invoices, input-credit eligibility with accountant |
| Withholding tax / GST TCS deducted or deposited by Google | Tax/compliance and payout/cash-flow item, may have reporting/credit implications | **NOT modeled as automatic extra permanent expense** | Reconcile actual settlement; don't double count TCS as a fee if creditable |
| Oracle hosting and backup | Developer pays Oracle | Separate [OCI forecast](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md) | Free allowances and capacity are unverified |
| Maps/Places/Geocoding | Developer via Google Maps billing | Lean India model currently ₹0 at 1k children | SKU rate, eligibility, field masks, session billing, abuse and quota |
| FCM push | No-cost messaging product under stated terms | ₹0 provider fee in model | Delivery not guaranteed; server/network cost elsewhere |
| Parent identity/login | Developer/provider | ₹0 **assumed** email/social login | Paid OIDC, guardians MAU, SMS OTP fees unresolved |
| Roads, Google Drive optional API/parent storage | Provider and/or parent storage purchaser | **Not enabled** | Asset-tracking license, quota/cost/consent unknown |
| Refunds, disputes, failed auto-renewals | Reduced developer collections, potential negative settlement | **NOT** guaranteed captured by the standard 15% deduction | Track reversal/refund and collection failures |
| Domain / third-party mail / support line | Developer | Domain already in OCI model; other vendor tools unpriced | Prevent double-counted domain; budget customer service |
| Play publisher registration | Developer | One-time onboarding; not recurring per-child | Google lists US$25 account registration fee in standard setup; confirm payment/country |
| Paid HA, audit, incident and support staffing | Developer | NOT included in cheap low-volume operating model | Production child-safety service needs separate signoff |

**Customer price rule:** Amar-Pola itself should not add undisclosed "location refresh", "guardian access", "GPS", "server", "SOS", or "activation" fees to these plans. Changes or optional charged add-ons need separate opt-in checkout and truthful price display. Google Play/payment method may apply payment terms or regional tax according to final checkout; verify final amounts before marketing as all-inclusive.

### Tax-inclusive example — NOT a tax determination

If the **₹500 annual payment includes an illustrative 18% consumer GST**, the pre-consumer-tax amount is about **₹423.73**, not ₹500. If the illustrative 15% Play fee is calculated on that assumed pre-tax amount, it is about **₹63.56** rather than ₹75. After the 1,000-child model's ~₹38.86/year allocated hosting budget, that leaves approximately **₹321.31 per child/year** before other costs and any tax on service fees.

Likewise a **₹50 tax-inclusive monthly charge** implies ~₹42.37 before consumer GST; subtract ~₹6.36 illustrative Play fee and ~₹3.24 hosting allocation, leaving about **₹32.78 per child/month** before other expenses. **Actual applicable GST classification, seller location, collection mechanics, Play service-fee base, input credits and exact settlement must be confirmed by accountant and real Play reports.** Do not assume 18% universally applies, add GST twice, or portray TCS as a lost fee when creditable.

For an **illustrative separate fee-tax sensitivity**, if 18% GST were additionally payable on a gross ₹75 Google service-fee invoice with **no usable tax credit**, that would be **₹13.50 further cost per ₹500 annual purchase**. This is a conditional example, **not** a statement of the actual tax payable. It must not be stacked blindly on the inclusive-tax model above.

## 5. Financial model at exactly 1,000 active paying children

**Assumptions:** stable 1,000 child seats for a full year; each subscription pays on time; all 1,000 on one term in first two rows; India 15% **auto-renew** Play service fee; per-year **budgeted hosting allocation ~₹38.86/child** (₹3,238.47/month for 1,000, or ~₹38,862/year total), not solely the ~₹2.39 direct hosting bill; lean Maps/Places no overage and no paid SMS. Gross revenues modeled **before tax**, refunds, customer acquisition and staffing. Parent family count can be below 1,000 if multiple child seats.

| Per paying child / 12-month normalized | Gross receipts if fully collected | Modeled Play 15% fee | Allocated hosting budget | **Remaining before additional costs** |
|---|---:|---:|---:|---:|
| Monthly: 12 paid cycles | ₹600 | ₹90.00 | ₹38.86 | **₹471.14** |
| Annual: one paid year | ₹500 | ₹75.00 | ₹38.86 | **₹386.14** |
| 50% annual / 50% monthly | ₹550 | ₹82.50 | ₹38.86 | **₹428.64** |

**Annual plan math:** ₹500 − ₹75 Play fee − ~₹38.86 hosting budget = **~₹386.14 per child/year**; at 1,000 child seats = **~₹3,86,138/year** remaining before unpriced expenses.

**Monthly plan math:** 12 × ₹50 = ₹600; 12 × ₹7.50 Play = ₹90; minus ~₹38.86 annual hosting budget = **~₹471.14 per child/year**, equivalent ~₹39.26 per child/month; at 1,000 = **~₹4,71,138/year** before unpriced expenses.

**50/50 seat mix at stable enrollment:** about **₹5,50,000/year gross collected** across 1,000 children, **₹82,500 Play fee**, ~**₹38,862 budgeted hosting**, leaving **~₹4,28,638/year**, with one half paying annually and the other paying every month. A mix of 1,000 *families* with multiple children is not the same as 1,000 *child subscriptions*.

### Cash-flow timing is different

- **Annual**: ₹500 per child is charged upfront when each child-seat family plan is purchased (at the applicable family amount), then service is provided for 12 months. If 1,000 paid seats start in the same month, nominal gross upfront amount is ₹5,00,000; this money is **not 12 months of profit**. Revenue recognition, settlement delay, refund reserve and accrued future hosting/support are separate.
- **Monthly**: ₹50 per child every month *only while payment succeeds and renewal continues*. "₹600/year" requires **12 paid renewals/payment periods**; churn, account hold, failed payment, UPI/autopay setup and cancellation can reduce collected revenue.
- The annual ₹500 price is **16.67% below** 12 × ₹50. It may improve upfront cash and retention but increases refund/prepayment obligations.
- Never market ₹500/year as "₹41.67 charged monthly" or treat a current active child as guaranteed to renew for a whole year.

## 6. Scale scenarios: pricing sensitivity, external API usage and hosting **allocation**

Rows below combine **an existing OCI hosting budget with reserves** and **the lean non-Oracle paid Maps event estimate** (₹0 at or below 5k assumed Indian children, ~₹808/month at 10k), plus Play's modeled fee. These figures are **for total business revenue comparison only**: they are not extra provider bills, and Oracle/third-party costs remain in their own authoritative documents.

**Monthly column:** assumes all seats pay ₹50 each month.  
**Annual column:** assumes all seats pay ₹500 for each full year; annual remaining amount deducts **12 months** of hosting/Maps allocation.

| Paying child seats | Monthly gross @₹50 | Monthly Play fee | Hosting+Maps budget/month | **Remaining/month (all monthly)** | Annual gross @₹500 | Annual Play fee | **Remaining/year (all annual)** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 500 | ₹25,000 | ₹3,750 | ₹1,680 | **₹19,570** | ₹2,50,000 | ₹37,500 | **₹1,92,340** |
| 1,000 | ₹50,000 | ₹7,500 | ₹3,238 | **₹39,262** | ₹5,00,000 | ₹75,000 | **₹3,86,138** |
| 2,500 | ₹1,25,000 | ₹18,750 | ₹9,878 | **₹96,372** | ₹12,50,000 | ₹1,87,500 | **₹9,43,962** |
| 5,000 | ₹2,50,000 | ₹37,500 | ₹20,267 | **₹1,92,233** | ₹25,00,000 | ₹3,75,000 | **₹18,81,795** |
| 10,000 | ₹5,00,000 | ₹75,000 | ₹43,428 | **₹3,81,572** | ₹50,00,000 | ₹7,50,000 | **₹37,28,870** |

**At 10,000 seats, the loaned VM size and API traffic are scenario assumptions, not certified support for 10,000 children.** Product must measure raw GPS observation volume, server load, Maps billing, actual guardian usage and required high availability before accepting a final profit forecast.

### 6.1 Break-even price floor is NOT ₹38.86

The ~₹38.86/year reserve allocation is a **partial modeled infrastructure budget per child at 1,000 seats**, not the product's true full cost. A viable price floor needs: Play percentage of tax-adjusted sale, real hosting including backups and HA, paid Maps/SMS/identity, payment collection risk, real customer support, app security audits, compliance/legal, family onboarding, device/OS support, app maintenance salaries and customer acquisition. No honest fully loaded break-even or profit number exists yet.

## 7. Payment, renewal, cancellation and refund rules

| Customer event | Product promise and UI behavior | Backend rule |
|---|---|---|
| New purchase | Show total due now, covered seat capacity, term, next regular charge and auto-renewing disclosure **before** Google checkout | Verify Play purchase token/state on backend; allocate seats after PURCHASED |
| Successful renewal | Continue existing child seats and grant scope | Verify current subscriptionsv2 state and expiry; update entitlement idempotently |
| Pending payment | Show PENDING, don't silently claim paid entitlement | Do not unlock paid seats from pending token |
| Grace period / silent retry | Explain payment issue privately to payer, preserve access while Play reports entitlement active/grace | Follow current Play state; do not shorten recognized grace ad hoc |
| Account hold | Clearly show paid premium features unavailable; provide repair link | Remove paid entitlement during hold, protect child data and core privacy rights |
| Voluntary cancellation | **Stop future renewal**; normally retain purchased benefits until current paid expiry | Don't immediately delete data or revoke a still-paid term |
| Expiration after cancellation | No future charge; move premium functions to disclosed fallback | Revoke premium entitlement, preserve record access/deletion under retention policy |
| Refund without revoke | Explain that refunds and access depend on Play resolution and law | Follow verified order/purchase state; don't assume immediate expiry |
| Revocation or chargeback | Explain status and dispute/support path | Revoke affected entitlements, audit reason, don't destroy user data automatically |
| Monthly↔annual plan change | Show actual Play-calculated payable amount, proration and next renewal date | Handle linked purchase token/new SKU, prevent duplicate overlapping paid seats |
| 1→2 child seat upgrade | Price shown from actual Play checkout, no invented immediate amount | Change capacity only when new subscription state verified |
| Remove one child | Explain when reduction is effective and what happens to stored records | Seat reassignment or downgrade policy; no implicit partial refund claim |
| User deletes account | Show data deletion and **separate subscription cancellation action** as necessary | Revoke credentials, run deletion jobs, reconcile Play purchase and lawful refunds |

All subscription plans must have an in-app **Manage / Cancel subscription** route linked to Play's online management screen, transparent self-service information and working support path. On Android where Play owns payment, open Play subscription management via the correct purchased product id and application package; do not fabricate a third-party payment cancellation flow.

**Refunds:** Google Play and developer-specific refund rules, consumer law and Play API capabilities apply. We cannot declare "all sales final", deny refunds categorically, charge a made-up cancellation fee, or promise universal prorated refunds. Publish a reviewed refund policy with process and time expectations; reconcile chargebacks and refunded entitlements using Play APIs. A refund can create **negative developer payouts** and collection obligations.

**No automatic free trials at launch** as the safe default. If added later, Play requires prominent duration, post-trial charge, auto-renew, cancellation method and availability of a no-trial option.

## 8. Billing implementation in Kotlin Android + C++20 backend

### 8.1 Suggested server resources

- billing_accounts(family_id, payer_principal, play_package, store_country, current_verified_plan, store_subscription_product, seats_paid, period, expires_at, renewal_state, pricing_currency, auto_renew_flag, purchase_token_reference_hash, generation).
- verified_play_purchases(purchase_token_hash UNIQUE, package, play_product_id, base_plan_id, order_key, expiry, verification_at, raw_provider_state_ref, acknowledgment_at). Store encrypted raw tokens only in restricted secret-backed storage if required for API calls; hashes prevent duplicates.
- child_seat_assignments(family_id, child_id UNIQUE within family, seat_index, assigned_at, transferred_at), composite family/child foreign key and owner controls.
- provider_event_inbox(message_id/notification_id unique, received_at, verified_at, state, retry_count) and financial_order_ledger(order_id when available, event type, transaction currency, gross, tax, fee, net, settlement_ref), **all idempotent**.
- Seat_count consistency under transaction/lock: active assigned children <= verified seats for family, no sharing token between families.

### 8.2 Backend purchase protocol

1. Native parent selects count and billing period; fetch product details/price and offer token from **real Play Billing product catalog**; show exact Play totals and subscription renewal/cancellation information.
2. Google Play purchase is made by parent payer; client gives purchase token to backend over authenticated TLS, along with product hint (hint **never** authorizes).
3. Backend calls **Google Play Developer API purchases.subscriptionsv2.get** with authorized server credentials, verifies package name, line items, state, expiry, linked token/replacement and original purchase/account binding; reject tokens assigned to another family.
4. Record verified purchase and family capacity in one transactional, idempotent operation; apply verified paid state, then acknowledge any new purchased token promptly (Google documents an approximately **three-day** acknowledgment deadline for purchased subscriptions; missing it may lead to refund/revoke). Retrying ack is safe with dedup.
5. Configure Real-time Developer Notifications (RTDN) to an authenticated server-side ingestion path (transport infrastructure must be scoped, secured and priced). Treat notifications as **hints** to fetch actual Play state, not direct entitlement authority.
6. Handle PURCHASED, RENEWED, IN_GRACE_PERIOD, ON_HOLD, CANCELED, EXPIRED, RECOVERED, REVOKED and purchase-token replacements; synchronize in app login/restore and nightly reconciliation. Detect refund/voided purchases as separate lifecycle events.
7. Only user owner/payer can change plan; guardian child data access continues to require child-specific scopes in addition to active subscription/capability check. No server/client can make Android permissions appear by paying.
8. Parent UI shows paid child seats, assigned child names, Play-provided actual next billing date/price, payment status, manage link, and explanation of staleness/unsupported capabilities.
9. Billing events cannot create new family grants, increase device management rights, reactivate revoked child data or bypass deletion tombstones.
10. Reconciliation must distinguish **active paid child seats** from active parents, active families, concurrent devices and guardian members.

### 8.3 Tests before launch

- Purchase, 1→2→3 family seat SKU upgrade; canceled purchase; pending state; duplicate/forged token across families; Play account differs from owner; 2+ guardians on one paid child.
- Monthly and annual renewal; annual downgrade; midperiod effective date/proration; declined UPI/autopay, silent grace, explicit grace, account hold, recovery, cancel, expire, re-subscribe and refund/revoke.
- Refund and payment withholding reconciliation; Play reporting amounts vs backend ledger; price country and tax totals; price changes and legacy price cohorts; bad/fraudulent receipts.
- Restore after parent-app reinstall and child-device transfer; lost payer Google account support scenario; owner change and temporary guardians.
- Open Manage Subscriptions and cancellation/online disclosure without hidden menu; pre-purchase capability check on standard Android vs DPC.
- Low-network/device clock-skew RTDN out of order; ack request timeout; callback replay and duplicate purchase token; no leaked payment or child identifiers in logs.

## 9. Google Play, Indian consumer and privacy compliance rules

| Rule | Project implementation |
|---|---|
| Play subscription transparency | Cost, billing frequency, auto-renew, included benefit, trial if any, and cancellation **shown upfront**; no misleading effective-monthly annual charge |
| Ongoing value | Charge recurring subscriptions only for sustained ongoing service, not a one-time child setup |
| Billing system | Use supported Play Billing for applicable in-app digital subscriptions; alternative billing in India has its own enrollment, reporting, processor, fee and compliance obligations and is **OFF by default** |
| 15% fee | As of reviewed October 2026 India auto-renewing subscription default for remaining markets; re-check regional rollouts before publishing, never assume worldwide |
| Tax obligations | Registered seller/controller location and exact GST/withholding/TCS need accountant review; obtain service-fee tax invoices and reconciled country reports |
| Offers and price changes | Correct Play base-plan/offer eligibility, price cohorts and user notices/consent when needed; do not silently migrate existing users to a higher price |
| Refund policy | Clearly available to purchaser; apply mandatory consumer rules and Google refunds; use provider APIs for proper entitlement updates |
| Monitoring/child data policy | Payment doesn't authorize secret capture, background permission bypass, inaccessible privacy controls or indefinite child-data retention |
| Parent cancellation and data deletion | Independent flows and disclosures; no loss of right to revoke child access or erase eligible records on cancellation |
| Family seat billing | Don't silently bill each guardian; parent payer approves N children and sees full amount before checkout |
| Overseas customers | **Not priced or enabled by this India-only plan**; country pricing, fee/tax, supported platforms and legal requirements require separate approval |

**Potential hidden fee conditions to monitor:** (a) Google fees on changed price/country, (b) GST on customer service or Google's invoice, (c) payout withholding/TCS, (d) payment failures/refund clawback and negative balances, (e) Identity/SMS verification traffic, (f) Places Pro API and Google Roads, (g) additional storage/HA/operating staff, (h) a charged alternative billing processor, (i) currency conversion and foreign markets, (j) Google Play registration/verification, and (k) legal security/support costs needed to operate minors' safety data responsibly.

## 10. Release decisions and blockers (specific owner checklist)

| Blocker ID | Required decision/evidence | Owner | Status |
|---|---|---|---|
| SUB-01 | Approve actual retail price **₹50 monthly / ₹500 yearly per child** and country India | Project owner | **PROPOSED** |
| SUB-02 | Decide whether displayed price is **final tax-inclusive payable** and tax/GST legal setup | Project owner + accountant | **OPEN — important** |
| SUB-03 | Verify Play Console accepts exact ₹50 and ₹500 as base-plan prices after tax/localized price setup | Play publisher | **NOT TESTED** |
| SUB-04 | Confirm existing/new account's actual India Play subscription fee/merchant and settlements | Publisher/finance | **UNVERIFIED** |
| SUB-05 | Confirm **one family capacity subscription** design (1–5 child seats) and what to do for 6+ | Owner + Android billing engineer | **PENDING APPROVAL** |
| SUB-06 | Choose seat upgrades/downgrades effective dates, refund/support and multi-owner transfers | Owner + billing engineer | **OPEN** |
| SUB-07 | Choose which capabilities are included in base price, fair use, Wear and managed feature boundaries | Owner/product/legal | **OPEN** |
| SUB-08 | Confirm launch login provider, whether SMS OTP is used and guardian-per-family allowance | Owner/security | **OPEN** |
| SUB-09 | Agree India Maps billing eligibility, API quotas, fee caps and optional Roads/Drive OFF | Owner/Maps project | **UNVERIFIED** |
| SUB-10 | Check actual OCI and device scalability, backup and production HA/support costs for 1k child seats | Backend/SRE/QA | **NOT BENCHMARKED** |
| SUB-11 | Verify Play Billing Library compatibility, sandbox products, RTDN, purchase ack, refunds and cases | Developers/QA | **NOT IMPLEMENTED** |
| SUB-12 | Publish legal Terms, Privacy, subscription disclosure, online cancel guidance and refund rules | Publisher/legal | **NOT PUBLISHED** |
| SUB-13 | Decide minimum customer support and incident/SOS promises and monthly spend | Owner/operations | **UNPRICED** |
| SUB-14 | Determine country rollout, prices beyond India, FX, taxes and 2026/2027 new Play fee applicability | Owner/finance | **DEFERRED** |
| SUB-15 | Decide trial (default NONE), prepaid (default NONE), coupons and alternative billing (default NONE) | Owner | **DEFAULT DISABLED** |
| SUB-16 | Final signoff on 1k subscription per-child economics from real invoices, refunds, taxes and retention | Finance | **NOT VERIFIED** |

**Recommendation:** Approve **₹50 monthly / ₹500 annual per child as the proposed entry tier**, with **1 family subscription containing paid seats**, **no trial or surprise paid add-ons**, Google Play as the only billing rail for launch, India only, and **tax-inclusive final checkout amounts if accountant/Play allow these exact prices**. Do not declare the remaining modeled ₹386–₹471/year per child to be profit; those figures omit important fixed and variable costs.

## 11. Sources checked for the 2026-10-26 plan

- Google Play subscription transparency and ongoing value requirements: https://support.google.com/googleplay/android-developer/answer/9900533
- Create subscriptions, base plans/offers, cancellation method and tax price settings: https://support.google.com/googleplay/android-developer/answer/140504
- Google Play regional subscription fee and India remaining-market 15%: https://support.google.com/googleplay/android-developer/answer/112622
- Play Billing family add-on limitations (distinct product IDs, shared periods): https://developer.android.com/google/play/billing/subscription-with-addons
- Subscription pricing, prepaid/auto-renew, billing period switch: https://developer.android.com/google/play/billing/subscriptions
- Play subscription lifecycle: https://developer.android.com/google/play/billing/lifecycle/subscriptions
- Billing Library acknowledgment and updates: https://developer.android.com/google/play/billing/integrate
- Real-time developer notifications: https://developer.android.com/google/play/billing/rtdn-reference
- Play refunds, price-change and developer obligations: https://support.google.com/googleplay/android-developer/answer/2741495
- India digital-sale GST, Google service-fee GST, TCS/withholding responsibilities: https://support.google.com/googleplay/android-developer/answer/138000
- Play India user choice billing conditions (not a free 4-point saving): https://support.google.com/googleplay/android-developer/answer/13306652
- Oracle baseline and per-child reserve at 1,000: [Hosting Financial Plan §14.10](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md)
- External API and earlier illustrative ₹149 pricing: [Third Party Cost Analysis](THIRD_PARTY_SERVICES_COST_ANALYSIS_2026.md)

**Document precedence for pricing:** THIS document is the **new proposal baseline** for Amar-Pola subscription prices. The ₹149/month figures in older cost analyses are **historical price sensitivity examples only**, not official or recommended public prices. No price, billing SKU, tax-inclusive status or merchant configuration has yet been activated in Play Console.
