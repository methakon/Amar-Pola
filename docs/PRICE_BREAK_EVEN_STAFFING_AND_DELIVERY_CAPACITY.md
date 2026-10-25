# Amar-Pola — ₹50/₹500 Break-Even, Staffing and Capacity Gate

**Status:** decision model; not validated profit forecast, not a hiring plan.  
**Date:** 2026-10-26 | **Authoritative sale-price proposal:** [Subscription Plans](SUBSCRIPTION_PLANS_PRICING_AND_RULES_2026.md).  
**Cost sources:** [OCI hosting](OCI_CHICAGO_DEPLOYMENT_AND_FINANCIAL_PLAN.md) and [Third-party provider SKU model](THIRD_PARTY_SERVICES_COST_ANALYSIS_2026.md). Old **₹149/month** in those reports is **historical sensitivity only**.

## 1. At 1,000 paying child seats the cash arithmetic

Assume 1,000 enrolled **paid** child seats (not necessarily 1,000 families), Google Play **15%** auto-renewing subscription service fee (subject to country/contract), modelled existing OCI hosting cash **reserve** ₹3,238.47 per month, and no paid Maps-overage/SMS/identity/HA/support/engineering. We do **not** know actual support costs or commercial production reliability costs.

| Twelve paid months normalized / per child | ₹50 monthly plan (12 successful cycles) | ₹500 annual plan |
|---|---:|---:|
| Customer face price for 12 months | **₹600.00** | **₹500.00** |
| Play 15% (simple before-tax example) | ₹90.00 | ₹75.00 |
| Budgeted OCI hosting/year (with reserves) | ~₹38.86 | ~₹38.86 |
| **Contribution before all other costs, pre-tax assumption** | **~₹471.14/year** | **~₹386.14/year** |
| Monthly contribution equivalent | **~₹39.26** | **~₹32.18** |

**Warning:** If selling prices are final consumer payments that *include* illustrative 18% GST, under the explicitly hypothetical Play-fee-on-net-of-GST arithmetic, the funds remaining after Play fee and **budgeted** OCI cost fall to about **₹32.78/child/month** on the monthly plan and **₹321.31/child/year**, or **₹26.78/month equivalent**, on annual. Actual India GST liability, collection, input credit and service-fee base require independent accountant/Play settlement verification.

### All-monthly and all-annual company picture (at 1,000 fully paid seats)

| View | All ₹50/month | All ₹500/year |
|---|---:|---:|
| Annual customer gross | ₹6,00,000 | ₹5,00,000 |
| Example Play 15% of gross | ₹90,000 | ₹75,000 |
| Model hosting *reserved budget* | ~₹38,862 | ~₹38,862 |
| **Unallocated balance before tax, staff, support, API, refunds and incidents** | **~₹4,71,138/year** | **~₹3,86,138/year** |
| Monthly-equivalent available **pre-tax case** | **~₹39,262** | **~₹32,178** |
| Monthly-equivalent available **illustrative tax-inclusive case** | **~₹32,778** | **~₹26,776** |

These balances are **not profit**. Income-tax or company expenses are additional; reserves are cash allocation, not already-paid invoices. If there are paying guardians beyond the child seats, count them as account-access usage but **not another subscription**.

## 2. Fixed operating expenses immediately challenge break-even

The following assumes 1,000 child seats stay paid for all 12 months; expense K is **additional fixed monthly operations and staffing** beyond the existing small OCI budget, Maps and modeled Play fees (and no other variable expenses). Illustrative tax-inclusive cash-available ceilings are about ₹32,778/month on all-monthly or ₹26,776/month on all-annual.

| Additional fixed monthly expense | Monthly-plan remainder, tax-inclusive illustration | Annual-plan monthly-equivalent remainder, tax-inclusive illustration | Viability before refunds/CAC/APIs |
|---:|---:|---:|---|
| ₹0 | +₹32,778 | +₹26,776 | Unpriced obligations still exist |
| ₹10,000 | +₹22,778 | +₹16,776 | Very little staffed coverage |
| ₹30,000 | +₹2,778 | **−₹3,224** | Annual plan already short |
| ₹50,000 | **−₹17,222** | **−₹23,224** | Not viable at 1,000 on assumptions |
| ₹1,00,000 | **−₹67,222** | **−₹73,224** | Major deficit |

For context, paying one engineer/operator **₹50,000/month** alone would exceed the modeled tax-inclusive contribution of **1,000** yearly-paying children. Multiple paid engineers plus security, customer support and independent audit would require more subscribers, a higher price, lower costs, founder financing or different scope. This is not advice about actual salary levels.

### Break-even formula, not invented profit

Let P = customer payment per child per month equivalent, t = included customer tax rate, f = actual Play fee applied to the validated fee base, V = other variable paid vendor cost per child, H(N) = cloud hosting allocation at N children, F = monthly fixed salaries + support + legal/security + incident/other overhead, C = monthly acquisition/churn/refunds cost.

**Illustrative tax-inclusive model only:**  
contribution per child = P/(1+t) × (1−f) − V − H(N)/N;  
monthly net operating remainder = N × [P/(1+t) × (1−f) − V] − H(N) − F − C.

Find **N** from real observed costs; H(N) is **not constant** as capacity, replication, retentions and API traffic scale. A closed-form “N=1,527” based on the 1,000-seat model is not reliable across server upgrades or legal support workload. Do not market “₹500/year profitable at 1,000 users” without the missing terms.

## 3. Explicit engineering staffing and accountability

A realistic team needs multiple skill domains even if one person fills several roles. **One person owning everything creates review/security and operational continuity risk**, especially for child location and 24-hour incident response. The following are **allocation proposals**, not project owner staffing commitments or actual employment contracts.

| Workstream | Accountable owner / scope | Candidate effort | Can one person hold multiple roles? |
|---|---|---|---|
| Product/commercial/privacy decisions | Founder/product owner, legal publisher and budget approvals | 0.5–1.0 person equivalent initially | Yes, but needs legal/finance reviewers |
| Kotlin child Android/permission + DPC test | Android engineer, real OEM lifecycle, Keystore, battery/perms | 1.0 engineer equivalent | May share Android parent work but slows timeline |
| Kotlin parent app/Maps/Billing | Android engineer, UX, guardian grants, child status, revenue | 1.0 engineer equivalent | Yes only with rescope |
| C++ Drogon API/PostGIS/worker/geospatial | C++ backend and data/geo engineer, auth and event-time worker | 1.0–1.5 engineer equivalents | Strong test discipline required |
| Independent QA/test automation | QA/integration engineer, real phone/managed hardware and API contract tests | 0.5–1.0 equivalent | Cannot self-approve security release alone |
| Security/privacy architecture review | Qualified security reviewer | 0.2–0.5 external/fractional equivalent + independent signoff | Separate reviewer for BOLA/secret handling |
| OCI SRE/backup/on-call | Cloud engineer/operator, recoveries, alerts, incidents, budgets | 0.2–0.5 before launch; staffed rota for production | Founder can administer dev but not guarantee 24/7 |
| India legal/DPDP counsel and tax accountant | Licensed external professionals | Project-based; ongoing updates and audits | **Not replaceable by code or documents** |
| Customer support/escalation | Named support person/team, custody disputes, deletion and SOS contact questions | Depends on customers and service promises | Requires published hours and escalation rules |

**Initial staffed MVP reference:** approximately **3–5 engineering person equivalents plus fractional QA/SRE/security**, with separate Indian legal/tax review; actual schedule depends on reuse, team seniority, managed-DPC scope, compliance and outsourcing. **Not financed by the current 1k-seat cash-flow assumptions.** A founder-led one-person build may have lower *cash* burn but does not eliminate opportunity cost, peer review or operational duty.

## 4. Financial staffing scenarios (not quotes)

| Candidate direct monthly people/operations cash budget | Annual cash budget | Extra cost per paying child/month at 1,000 seats |
|---:|---:|---:|
| ₹30,000 | ₹3,60,000 | ₹30.00 |
| ₹50,000 | ₹6,00,000 | ₹50.00 |
| ₹1,00,000 | ₹12,00,000 | ₹100.00 |
| ₹2,50,000 | ₹30,00,000 | ₹250.00 |
| ₹5,00,000 | ₹60,00,000 | ₹500.00 |

At 1,000 seats and ₹50/month face price, **₹50,000 monthly staffing alone is ₹50/child/month**, before Play, tax, hosting and other provider fees. Therefore low subscription pricing may only work with a **deliberately constrained feature/support/service-level scope**, adequate scale, external funding or higher-margin tiers. SOS resilience, privacy legal review and real Android QA are **not optional budget omissions** if those features are sold.

## 5. Hardware and M1/M2 capacity checklist

| Requirement | Decision/proof |
|---|---|
| At least one non-managed older Android phone | OS version, API, brand/model, permission/FGS/Doze test log |
| At least one recent Android phone | API 34–36 candidate, typed FGS/permission/backgr-start test results |
| One Samsung/other mainstream OEM phone if available | Battery and reboot/OEM-kill behavior |
| **One spare phone safe to factory-reset** | Owner's written approval after backups; eligible Android fully managed DPC provisioning and actual device-owner proof |
| Child-side and parent-side separate devices/accounts | Pairing, revoked guardian, network loss and app permission flows |
| Managed device failure fallback | Standard mode remains functional; do not claim DPC restriction on a nonmanaged phone |

No real phone inventory has been supplied to the repo. Accept **emulators/synthetic GPS** for initial architecture tests only; M1 hardware proof and M2 device test acceptance remain blocked without devices. **Do not ask anyone to factory reset a phone before its data has been backed up and the device owner has approved.**

## 6. Mandatory decisions and execution logistics

| Blocker | Needed from owner | Consequence |
|---|---|---|
| TEAM-01 | Team roster/count and who actually owns child Android, parent Android, C++, QA/security and OCI | Schedule and definition of done cannot be committed |
| TEAM-02 | Monthly cash payroll/contractor budget and development runway | Cannot conclude break-even |
| TEAM-03 | Support channels, response hours, custody/legal escalations and planned paid SOS scope | Cannot price support/incident coverage |
| TEAM-04 | Real hardware list/API/OEM plus safe-to-reset device | Cannot pass Android lifecycle/DPC acceptance |
| TEAM-05 | India-qualified DPDP lawyer/tax accountant and paid review budget | Cannot pass real child data legal gate |
| TEAM-06 | Subscription collection reality: ₹50/₹500 tax inclusive, free trials, churn, refunds and actual Play settlements | Revenue estimates unverified |
| TEAM-07 | Maximum hosting+provider+staff spend for pilot, and go/no-go thresholds | No credible release cash plan |
| TEAM-08 | Phone-first vs managed DPC vs Wear in launch; fixed milestone responsibilities | Avoid costly spread of thin team |

**Recommended gate order:** decide legal entity/India purpose/Chicago; approve limited child/guardian/retention scope and login; list hardware and owner/QA engineers; implement synthetic-data vertical slice; fund independent security/Android/device testing and real backup recovery; pilot with written consent/counsel; reprice only after measured invoices and churn.

This document answers the specific gap: **₹50/month and ₹500/year are proposed product prices, not demonstrated sustainable all-in costs.**
