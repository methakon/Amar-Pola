# Amar-Pola — Oracle Cloud Chicago Deployment, Capacity and Financial Plan

**Decision reference:** OCI-CHI-001  
**Revision:** 1.0 · **Research/pricing checked:** 2026-10-25  
**Selected target home region:** US Midwest Chicago, **us-chicago-1** (OCI commercial realm OC1; three availability domains).  
**Status:** **Deployment plan committed; Oracle tenancy/VM NOT created; no cloud credentials or active instance were available in this session.**  
**Project:** [Amar-Pola](../README.md), [Canonical Technical Specification](TECHNICAL_SPECIFICATION.md), [Secure M1 Implementation](M1_ANDROID_CPP_ARCHITECTURE_AND_IMPLEMENTATION.md), [Data/Security Contract](DATA_AUTHORIZATION_AND_RECOVERY_CONTRACT.md), [Blocker Register](BLOCKERS_AND_OWNER_DECISIONS.md).

## 1. Executive decision, why Chicago, and what is unverified

**Use Oracle OCI Ampere A1 (ARM64) in us-chicago-1 as the primary dev/MVP infrastructure target.** In the initial resource-constrained model, **Drogon C++ API, independent C++ reconstruction worker, PostgreSQL/PostGIS and HTTPS edge all run on one VM**, as separate processes with individual resource ceilings.

**Why Chicago:**
- Three availability domains (ADs); when an A1 Always Free instance receives an out-of-host-capacity error, retrying another AD within the selected home region is an Oracle-documented option.
- Same published OCI A1 price/free allowance as other eligible commercial regions; we are **not** claiming Chicago has higher A1 quotas or cheaper future paid compute.
- Longer-term PAYG expansion can use other ADs or request subscribed-region limits, subject to the actual account.
- User chose priority of free-quota and extensibility over local proximity.

**Unknown and cannot be confirmed from public information:** live free ARM capacity/placement in Chicago; actual tenancy shape limits; available AD placement on the day of enrollment; current account free entitlement; paid capacity/SLA terms. Oracle does **not** expose a reliable real-time public per-AD capacity inventory. Successful creation is the actual proof.

**Important child-data risk:** a US-hosted database for minors may require jurisdiction-specific consent, lawful cross-border transfer terms, processor notices and privacy/legal review. Chicago is a technical home-region decision **subject to B-02 and privacy signoff**; do not start real child-data production collection until that decision is resolved.

Official sources: [Oracle regions/ADs](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm) and [Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm).

## 2. Verified free-tier and PAYG charging rules

| Resource | Always Free tenancy | PAYG tenancy | Billing risks and notes |
|---|---|---|---|
| Ampere A1 VM | **1,500 OCPU-h + 9,000 GB-h/month**; typically 2 OCPU + 12 GB 24/7 | Published paid price list: **3,000 OCPU-h + 18,000 GB-h/month** equivalent ~4/24 for full month | Paid account entitlement **must be verified before relying on 4/24**; allowances shared across all A1 VMs/container instances in tenancy |
| E2.1.Micro AMD | Up to two micro VMs | Follow applicable entitlement | Only 1 GB each; do not depend on them for PostgreSQL |
| Boot + block volumes | **200 GB total** home-region | Same listed Always Free allotment | A 50 GB boot volume counts; **not 200 GB in addition to boot** |
| Volume backups | **Five** Always Free volume backups | Same listed allowance | Five objects, not unlimited historical backup storage/recovery promises |
| Object/archive storage | **20 GB combined** | **10 GB Standard + 10 GB Infrequent + 10 GB Archive** | Paid object capacity/bandwidth/API calls beyond quotas; free requests allowance subject to Oracle limits |
| Object storage requests | 50,000 requests/month | Same free requests allowance listed | Monitor large upload frequency |
| Outbound data transfer | 10 TB/month included | Follow OCI free transfer policy | Child telemetry is mostly inbound; map API responses/backup transfer are outbound |
| HTTPS/monitoring | Free-tier-compatible VCN, logging/monitoring and certificate quotas | Free allowances/paid excess | Public domain registration and outsourced alerting are separate costs |
| Service support | Always Free lacks enterprise SLA/standard Oracle Support | PAYG can offer support options | Single free VM **is not a high-availability child safety service** |

Oracle free account is not charged for paid services **unless deliberately upgraded or using time-limited promotional trial resources**. If Free Trial created excess A1 beyond 2/12, it may be disabled/removed after credits expire. Never rely on promotional $300 trial credits as recurring economics.

**Account documentation distinction:** The Always Free resource page says 2/12 for a free-only tenancy. Oracle India **paid price list** says PAYG first 3k/18k usage hours free. They are **not the same allowance**. Verify the individual PAYG account's billing screen and limits; if entitlement differs, revise all projections.

Sources: [Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm), [Oracle India price list](https://www.oracle.com/in/cloud/price-list/), [OCI Free Tier account lifecycle](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm), [OCI public price geography](https://www.oracle.com/cloud/economics/).

## 3. Architecture by stage

### Stage A — Always Free lab and controlled pilot

~~~text
Google Play native Parent Android (Kotlin, Compose, Maps)
  |
  | HTTPS/TLS, parent OIDC, child-specific grants
  v
OCI Chicago single A1 ARM64 VM — 2 OCPU, 12 GB
   Caddy/Nginx: TLS reverse proxy (443 only)
   Drogon C++20 API service (limits, JWT/device proof, data access)
   C++20 worker process (GPS event-time recon + usage + jobs)
   PostgreSQL + PostGIS (localhost/private socket ONLY)
   Background retention/backup tasks and metrics agents
       |
       +--> Free OCI Block Volume (database)
       +--> Encrypted daily logical backup to Object Storage
       +--> OCI Monitoring/Notifications (quota limited)
  ^
  |
Child Android Kotlin location/usage + small C++ NDK core
Encrypted local queue + batched authorized telemetry
~~~

**VM deployment candidates:**
- Region: us-chicago-1; AD: whichever of the 3 ADs actually provisions A1.
- Image: Ubuntu/Oracle Linux **arm64** Always Free eligible image, supported/patched.
- Shape: VM.Standard.A1.Flex, 2 OCPU / 12 GB.
- Boot: 50 GB; separately attached database block volume: **100 GB** initially; total 150 GB, leaving **50 GB** of free allocation unused as headroom.
- Public endpoint: one HTTPS reverse proxy on port 443. Keep PostgreSQL port 5432 closed to the internet. Admin through OCI Bastion or otherwise hardened management access. Firewall denies all unnecessary inbound traffic.
- Service manager: systemd/Podman with limits; do not need Kubernetes, external Redis, message broker or separately hosted workers on day 1.
- Data protection: encryption at rest through supported OCI volume encryption, TLS to clients, device Keystore signatures, family/child ACL and DB RLS, non-root least-privileged processes, protected secrets with approved rotation.
- Process budget candidate: OS/cache 1–2 GB, PostgreSQL 3–4 GB, Drogon API 0.5–1 GB, C++ worker ~0.5–1.5 GB, spare page cache/metrics. These are tuning budgets, not measured process footprints.
- Worker CPU concurrency 1 initially; Drogon event loop must never synchronously reconstruct trips. Parent latest position hits indexed qualified row; GPS uploads are batched and acknowledged after durable DB commit.

**Why single VM first:** eliminates separate C++ worker-hosting fees and cross-host queues. Backend grows by horizontal API/service scaling later, **without discarding the C++ domain architecture**. Single node is vulnerable to VM failure, maintenance, free-tier reclamation or database loss; don't market emergency uptime guarantees.

### Stage B — PAYG account, optimize without new architecture

- Upgrade deliberately to OCI PAYG only after confirming entitlement, payment/tax information and spending safeguards. PAYG is a billing mode: **it does not automatically resize the existing instance when subscribers grow**.
- Consider **4 OCPU / 24 GB** A1 equivalent if the paid-account quota is confirmed. Under the published 3k/18k monthly allowance this size has ~₹0 **A1 compute usage** for a full 730-hour planning month; storage, regional backup, paid networking, support, Maps and taxes can still cost.
- Upgrade VM shape/restart or provision additional VM and move load using tested migrations; dynamic autoscaling requires OCI instance pools/metrics and usually additional paid infrastructure, not an automatic free-VM feature.
- Separate Drogon API processes and C++ worker compute budgets first, then move DB to a private instance/managed database or add application replicas as latency, reliability and data growth demand.

### Stage C — Commercial high-availability topology (not costed in cheap single-VM model)

- Distinct API and reconstruction VM pools, managed/private database, replication/failover, off-machine encrypted backup and restore tests, load balancer, monitoring/on-call and region/AD fault plan.
- Set production SLA from actual testing; at least two failure domains for critical service and no single free VM for guaranteed emergency/SOS.
- PAYG 4/24 shared monthly allowance does not imply high availability; even two VMs within free hours will not make a standalone primary PostgreSQL highly available without database architecture work.
- Provider fees for load balancers/managed DB/extra backups/egress, and **human operations/support**, must be priced separately before promising a commercial SLA.

## 4. Deployment procedure and checkable steps

| Step | Exact planned action | Evidence/rollback |
|---|---|---|
| D-01 | Register/verify OCI account, select home region **US Midwest Chicago** at creation; configure MFA, billing admin and compartment | Screenshot/redacted region and account mode; do not share passwords/keys |
| D-02 | Check Limits/Quotas and Usage in Chicago; try VM.Standard.A1.Flex 2/12 on AD1, AD2 or AD3 if available | Live VM OCID, shape/AD; if out-of-host-capacity, no VM exists |
| D-03 | Create a dedicated compartment, VCN, subnet, ingress rules 443 and restricted admin, outbound as required | No 5432 to public internet; network scan |
| D-04 | Provision Always Free eligible ARM64 image, 50 GB boot and 100 GB attached DB block; keep remaining free capacity in reserve | Boot + block quota and volume attachment screenshot |
| D-05 | Set user/service accounts, automatic security updates, SSH/Bastion, firewall, systemd limits and time sync; avoid hard-coded secrets | Security baseline and recovery access tested |
| D-06 | Compile/build for aarch64: C++20 Drogon API and C++ worker, PostgreSQL/PostGIS, supported TLS reverse proxy | Native ARM compile, unit test, signed version hash |
| D-07 | Apply versioned SQL migrations, child/family ACL, authorized pairing and device keys, backup roles; no real child GPS before security tests | Migration/revert, two-family IDOR/RLS test |
| D-08 | Deploy HTTPS domain endpoint with free ACME certificate, healthcheck, failure statuses and limited log retention | TLS test; domain fee is external |
| D-09 | Enable encrypted daily PostgreSQL logical backup with WAL-safe strategy when applicable to OCI Object Storage; schedule restore drills | Test a **separate** restore environment; backups on same VM are insufficient |
| D-10 | OCI metrics/budget alarms for CPU, RAM, disk, egress, queue backlog, backup failures; do not inflate utilization to avoid idle reclamation | Test alert receipt and automatic rollback procedures |
| D-11 | Synthetic 10, 100, 300, 500 device workloads, then labeled/authorized device pilot | Measured latency, queue lag, retention, memory, battery, GPS trust |
| D-12 | Add paid account/resize only after budget approval and real trigger; test migration and downshift | Before/after costs, billing alerts, backup proof |
| D-13 | Final privacy/controller/region review, Play monitoring disclosure, live deletion URLs and release binary evidence | Policy approval; no “production-ready” claim before completion |

**No cloud resources are created by this document.** Provisioning requires authorized OCI account access and actual successful shape allocation. Avoid automatically upgrading to PAYG on capacity errors: only an informed owner should change billing mode.

## 5. Usage model: one subscription per active child, not per parent

| Variable | Planning assumption | Change sensitivity |
|---|---|---|
| Billable unit | **One actively enrolled child profile with tracking entitlement per subscription** | Parent with 3 children = 3 subscriptions; can link more than one source device to child under policy |
| Parent login count | One or several approved guardians per child | Increases parent reads, SSE/alerts but **not** child subscription count |
| Average GPS observations | **300 accepted fixes per child per day** | Frequency/accuracy and active travel significantly alter cost |
| Device API batches | ~30 fixes per HTTPS request | ~10 batch requests per child per day, before retries |
| Retention model | 30 days raw GPS, 90 days derived trips/usage as **financial scenario only** | Unapproved owner choice B-07; actual policy may be different |
| Raw + index footprint | 0.5–1.0 KB per stored GPS observation | Requires Postgres measured table/index/WAL storage, not guaranteed |
| Parent map/read traffic | Moderate; latest fix and paginated trips, one active viewer per account typically | Continuous live viewing, long replay and excess polls change memory/egress |
| Excluded heavy workload | No remote media streams, recordings, giant downloads or paid road matching | Such features create entirely different bandwidth/storage/provider bills |
| Hours per full month | 730 | Formula recompute for actual invoice/calendar month |

**Warning:** A child with a watch and phone may generate multiple tracking source streams. Subscription count by child does not guarantee resource consumption per child remains constant. Billing/limit policy must prevent disproportionate multi-device usage or account for it.

At 100 active children: 30,000 fixes/day, ~900,000 fixes/month, **0.45–0.9 GB raw+indexes** under the 0.5–1KB model. At 500 children: 150,000/day, 4.5 million/month and **2.25–4.5 GB raw+indexes**. At 1,000: 300,000/day, 9 million/month and **4.5–9 GB**. The figures exclude derived trip rows, usage, WAL, indexes beyond assumed budget, temporary files, backups and customer exports.

## 6. Actual prices and compute-only formula

**Oracle India price list at review:**
- Ampere A1 CPU **₹0.95545 per OCPU-hour** over applicable allowance.
- Ampere A1 RAM **₹0.1433175 per GB-hour** over applicable allowance.
- Block volume above free allowance **₹2.4363975/GB-month** storage, plus performance **₹0.1624265/VPU/GB-month** (10 VPUs ≈ ₹1.624265/GB-month), so **balanced block volume totals ~₹4.06/GB-month** when billed and excluding taxes. Use Basic/lower VPU only after measured I/O safety check.
- Object Storage Standard over applicable free allotment **₹2.4363975/GB-month**, plus operations/retrieval/other tier rules as applicable.
- These are published OCI India-list illustrations; actual invoice currency/contract/tax and region of purchased services require account confirmation. **Do not use a made-up exchange rate.**

**Monthly compute formula (PAYG 730 hours, after paid account benefit verification):**

~~~text
ocpu_billable_hours = max(0, (total_A1_OCPU × 730) − 3000)
ram_billable_gbh    = max(0, (total_A1_RAM_GB × 730) − 18000)
A1_compute_INR      = ocpu_billable_hours × 0.95545
                      + ram_billable_gbh × 0.1433175
AlwaysFree-only: use 1500 OCPU-h and 9000 GB-h instead.
~~~

For a real 31-day month, use actual 744 hours. Free hours and GB-hours apply to all A1 resources in tenancy combined. An additional always-on machine may begin charging when the **sum** exceeds the quota, even if the original machine remains unchanged.

**Compute is not a child-based Oracle price.** The following machine sizing is **illustrative scenario allocation only, NOT a benchmark proving each configuration can handle N children.**

## 7. Monthly infrastructure scenario projections in INR

Two separate columns prevent a false “free commercial operations” claim:
1. **A1 compute:** calculated against Oracle published allowances.
2. **Planning reserve:** illustrative **noncompute/operational contingency** set by Amar-Pola planning for domains, independent encrypted backups, monitoring, billing reconciliation and unmeasured external charges. **Not an OCI quoted charge and NOT a sufficient staffed 24/7 support budget.** Adjust it after provider bills.

**Scenarios (monthly 730-hour model):**

| Active subscribed children | Billing scenario | OCPU / RAM GB | Raw GPS 30d | Oracle A1 compute | Optional noncompute reserve | Illustrative infra budget | Infra budget / child |
|---:|---|---:|---:|---:|---:|---:|---:|

| 100 | Always Free | 2 / 12 | 0.5–0.9 GB | ₹0 | ₹1,500 | **₹1,500** | ₹15.00 |
| 300 | Always Free | 2 / 12 | 1.4–2.7 GB | ₹0 | ₹1,500 | **₹1,500** | ₹5.00 |
| 500 | Always Free | 2 / 12 | 2.3–4.5 GB | ₹0 | ₹2,000 | **₹2,000** | ₹4.00 |
| 1,000 | PAYG free A1 quota* | 4 / 24 | 4.5–9.0 GB | ₹0 | ₹3,000 | **₹3,000** | ₹3.00 |
| 2,500 | PAYG paid excess | 6 / 36 | 11.3–22.5 GB | ₹2,505 | ₹6,000 | **₹8,505** | ₹3.40 |
| 5,000 | PAYG paid excess | 8 / 48 | 22.5–45.0 GB | ₹5,156 | ₹12,000 | **₹17,156** | ₹3.43 |
| 10,000 | PAYG paid excess | 12 / 72 | 45.0–90.0 GB | ₹10,456 | ₹25,000 | **₹35,456** | ₹3.55 |

**Interpretation:** In an Always Free account, 100–500 is a **test-planning range**. At 1,000 the table assumes you **deliberately switched to PAYG** and verified the larger A1 allowance; 4/24 compute may remain ₹0 despite being a **paid account**. At 2,500–10,000 the CPU/RAM calculations are reliable arithmetic but actual infrastructure would likely require **multiple VMs, dedicated database, backup and HA**, so these figures **understate a production-grade deployment**.

Cost drivers increasing earlier than child count alone:
- Capturing every 5–15 seconds instead of adaptive 300 points/day.
- Large long-term raw GPS/history or media storage.
- Extended multi-device (phone/watch) records per subscribed child.
- Frequent real-time parent viewers and third-party geocoding/Roads API calls.
- Paid managed PostgreSQL, load balancing, disaster recovery regions, contractual support and professional security/operations.
- Need for cross-border compliance, customer support staffing and high service availability.

## 8. Paid subscription per child: revenue and unit economics

**Policy assumption:** each **child profile** requires its own monthly subscription; one parent may manage 1, 2, 3 or more children; all approved guardians share authorization, **not duplicate child subscription charges**. The suggested base price used here is **₹149 per child/month as a modelling example, not an approved product price**.

**Google Play recurring subscriptions:** official guidance lists a 15% service fee in currently applicable standard regimes, but the actual country/product agreement and payment scheme must be verified. Illustrations treat 15% of listed pre-tax price as an expense. The treatment of GST/VAT, taxes included/excluded in end-user price, payment declines, refunds/chargebacks, regional fees and alternative billing may change realized revenue.

| Charge or income per paying child | Example at ₹149/month |
|---|---:|
| Subscription collected (pre-tax **assumed**) | **₹149.00** |
| Play 15% fee (illustrative) | ₹22.35 |
| After illustrative Play fee, before tax/other costs | **₹126.65** |
| Allocated A1 compute cost at 2,500-child case | ~₹1.00 |
| Allocated full illustrative infra budget at 2,500-child case | ~₹3.40 |
| Additional app-store taxes/refunds, support, engineering, security, legal, marketing, extra APIs | **UNPRICED and potentially much larger** |

**Family billing examples:** parent with 1 child pays ₹149/month; parent with 2 children ₹298/month; parent with 3 children ₹447/month **before tax/discounts**, with one corresponding subscription per child. There is no separate Oracle per-parent fee, though parent traffic counts toward capacity.

### Revenue sensitivity at hypothetical ₹149/child

| Paying children | Gross pre-tax subscription sales | Illustrative Play fee (15%) | Sales after Play fee | Compute + modelled infra reserve | Remainder before tax, staff, marketing, legal, refunds, other APIs |
|---:|---:|---:|---:|---:|---:|

| 100 | ₹14,900 | ₹2,235 | ₹12,665 | ₹1,500 | ₹11,165 |
| 300 | ₹44,700 | ₹6,705 | ₹37,995 | ₹1,500 | ₹36,495 |
| 500 | ₹74,500 | ₹11,175 | ₹63,325 | ₹2,000 | ₹61,325 |
| 1,000 | ₹1,49,000 | ₹22,350 | ₹1,26,650 | ₹3,000 | ₹1,23,650 |
| 2,500 | ₹3,72,500 | ₹55,875 | ₹3,16,625 | ₹8,505 | ₹3,08,120 |
| 5,000 | ₹7,45,000 | ₹1,11,750 | ₹6,33,250 | ₹17,156 | ₹6,16,094 |
| 10,000 | ₹14,90,000 | ₹2,23,500 | ₹12,66,500 | ₹35,456 | ₹12,31,044 |

**This remainder is emphatically not net profit.** It omits application development salaries, ongoing support/operations, customer acquisition, GST/VAT/income tax, chargebacks/refunds, insurance, audits, security professionals, paid geocoding and other costs. Subscription cancellations reduce paid units but previously stored data may still incur permitted retention/deletion processing expense.

### Pricing variants for product discussion

| Hypothetical child plan/month pre-tax | Play fee at assumed 15% | Sales after fee before other costs |
|---:|---:|---:|
| ₹99 | ₹14.85 | ₹84.15 |
| ₹149 | ₹22.35 | ₹126.65 |
| ₹199 | ₹29.85 | ₹169.15 |

**Do not set a final subscription price from compute arithmetic alone.** Add full product economics, taxes, region differences, unit support cost, retention costs, premium features, refunds and Play Billing policy before launch.

## 9. Third-party and financial line items often forgotten

| Expense | Start estimate | Treatment and risks |
|---|---|---|
| OCI Always Free VM 2/12 | ₹0 compute if eligible/available | Shared CPU, potential reclamation, no SLA; needs recovery strategy |
| OCI PAYG 4/24 A1 | Potentially ₹0 A1 compute under verified 3k/18k benefit | PAYG account can incur chargeable services immediately |
| OCI block volumes first 200GB | ₹0 quota | Boot included; excess volume storage+performance billed |
| Encrypted Object Storage backup | Free only within applicable tier/requests | 20GB combined free-only; paid account separate 10GB per tier; replication/backup tests |
| OCI outbound transfer | 10 TB/month included | Check traffic billing in account; unusual media or sync can change |
| Domain name | **Budget ₹1,000–2,000/year** hypothetical | Registrar/TLD-specific; not Oracle compute |
| TLS certificates | Free ACME certificates can be used | Proper renewals/configuration still require admin effort |
| DNS hosting | Could be included by registrar; OCI DNS may add cost | Confirm zone/query charges for chosen setup |
| PostgreSQL/PostGIS/Drogon software | Open source, no per-child license fee in the proposed stack | Maintenance, admin and security operations are not free |
| Firebase Cloud Messaging | Listed as no-cost | Third-party dependency, delivery **not guaranteed** |
| Google Maps SDK for Android | Mobile Maps SDK usage listed as unlimited/no SKU charge, with billing project/key required | Dynamic Street View, Places, Routes, Roads, geocoding are distinct paid SKUs |
| Maps Places/Geocoding/Roads | **Excluded until separately estimated** | Quota/cost caps, Maps Terms, Roads tracking license review |
| Play developer account | **US$25 one-time** | Payment/currency/tax per country; separate from subscription service fees |
| Play Billing recurring subscription fee | Example 15% | Verify actual subscription agreement/taxes and country details |
| Google Drive backup | Optional OAuth; potentially parent pays Drive storage | API/authorization, media bandwidth, token/storage processor risks |
| Customer support/maintenance | **Not included** | Staff/consultant time can dominate at small subscriber counts |
| Legal/privacy/security reviews | **Not included** | Children's precise location and US data residency require independent review |
| App store refunds/taxes | **Not included** | Material to per-child contribution and profitability |
| Off-region disaster-recovery backup | **Not included** | Cross-region data movement, encryption/storage and legal implications |
| Managed PostgreSQL or HA load balancer | **Not included** | Reliability premium, separate quote and architecture |

Sources: [OCI price list India](https://www.oracle.com/in/cloud/price-list/), [Maps SDK Android usage](https://developers.google.com/maps/documentation/android-sdk/usage-and-billing), [Google Maps SKU pricing](https://developers.google.com/maps/billing-and-pricing/), [Firebase FCM pricing](https://firebase.google.com/pricing), [Play subscriptions service fee](https://support.google.com/googleplay/android-developer/answer/112622?hl=en-in), [Play Console registration](https://support.google.com/googleplay/android-developer/answer/6112435).

## 10. Real upgrade triggers: when billing actually starts

**Neither Oracle nor your architecture has an automatic “500 children = paid” threshold.** Start measuring with 10/100/300 child simulations, then take a product decision:
- **Consider upgrade or optimization** if CPU >65–70% sustained at representative peaks, PostgreSQL memory pressure/swap, DB disk >65–70% (with 30-day growth projection), API p95 >500ms or ingestion/reconstruction queues fall consistently behind; thresholds are **initial engineering candidates**.
- **Consider PAYG for service support/capacity**, even at 10 paying children, if you need reliable recovery/support or a critical SLA. Upgrading account alone doesn't remove single-node failure risk.
- **If OCI reclaims Always Free A1 or capacity is unavailable**, service downtime/data restore may force a paid resource regardless of subscriber count.
- **If heavy Maps/Roads/Places/media or paid storage** used, bill may be nonzero even with 2/12 A1 compute.
- **If free-only account**, no automatic PAYG overflow charge; a service may fail to allocate rather than silently expand. Never auto-upgrade without authorization.

**Suggested release planning, not capacity certification:**
- 0–100 children: small controlled pilot within free 2/12 if created and tested.
- 100–500: careful battery/server/DB and queue monitoring, begin backup and resilience improvement.
- 500–1,000: consider PAYG and 4/24 only with tenancy free-benefit confirmation and tested performance.
- 1,000+: benchmark distributed DB/workers, load and security; do not place all paid family safety workloads on a single free node.
- Re-estimate at every order-of-magnitude usage increase and when observation cadence or retention changes.

### Capacity review checklist for every +100 active child devices

1. 7-day p50/p95 ingest latency, failed receipts and queue lag.
2. Parent history query and simultaneous map viewers.
3. PostgreSQL connections/RSS, WAL, storage growth and free 200 GB remaining.
4. Device source count per child and actual observations/child/day.
5. Snapshot/object backup bytes, successful restore age and legal retention.
6. Oracle tenancy quota usage, paid service fees and budget alerts.
7. User-facing staleness and SOS delivery without guaranteed emergency response claims.

## 11. Reliability and privacy controls for a location-safety business

- This is a **single-node MVP**; it is not suitable for promises of guaranteed emergency availability. Provide child/parent last-seen, stale, offline and unavailable statuses clearly.
- Never bypass Android background/monitoring restrictions to satisfy server performance promises.
- Separate backend processes on same machine for predictable CPU and memory, but protect Postgres durability from worker overload using job budgets.
- Use encrypted off-machine backup, quarterly (or more frequent) restore tests, IAM least privilege, MFA, OCI budget alarm, credential rotation and documented incident response.
- Disable sensitive microphone/camera capture and arbitrary private file transfers in this hosting model; even when a separate authorized future feature is considered, its legal/power/storage budget must be recalculated.
- Hosting minors' precise location in a US region must be included in privacy policy, Data Safety disclosures, subprocessor registers and country/legal review. **Owner must decide data residency and acceptable retention before production.**
- A sample policy of raw location 30 days here is a **financial modelling assumption** only; current blocker B-07 is still open. If approved retention is longer, recompute and price storage/backup.

## 12. Current hard blockers and signoff ledger

| ID | Blocker | Who can resolve | Current state |
|---|---|---|---|
| OCI-01 | Create and verify Oracle tenancy **us-chicago-1** home region | Project owner with OCI credentials | **NOT CREATED** |
| OCI-02 | Obtain A1 2/12 in one of Chicago's 3 ADs | OCI capacity allocation/account | **NOT VERIFIED** |
| OCI-03 | Confirm Always Free and PAYG 4/24 benefit in **your** tenancy | Account billing dashboard/Oracle Support | **NOT VERIFIED** |
| OCI-04 | Select legal publisher, target markets, minors' data transfer legality and US residence | Project owner/privacy counsel | **BLOCKS production data** |
| OCI-05 | Approve raw/trip/usage/audit retention and backup deletion | Product/privacy owner | **OPEN** |
| OCI-06 | Choose real domain, support contact, DNS/certificate and identity provider | Product/operations | **OPEN** |
| OCI-07 | Implement C++ server, worker, migrations, SQL ACL and Android agent/parent | Developers | **NOT IMPLEMENTED** |
| OCI-08 | Load test 10–1,000 synthetic children and security/power/backup drills | QA/SRE | **NOT TESTED** |
| OCI-09 | Configure budgets, OCI IAM, encrypted off-machine backup and restore | Cloud engineer | **NOT CONFIGURED** |
| OCI-10 | Approve subscription price per child, taxes and Play Billing provider terms | Product/finance | **OPEN** |
| OCI-11 | Verify external Maps/Roads, FCM, third-party SDK fees before optional feature enabled | Finance/developers/legal | **OPEN** |
| OCI-12 | Define minimum SLA, production HA architecture and on-call staffing | Product/SRE | **OPEN** |

**Decision already made:** choose Chicago as the **target design**, prioritize Oracle Always Free 2/12 and C++ Drogon+PostGIS, keep worker on same VM initially. **No cloud VM, billing account, DNS/domain or runtime deployment has been provisioned.**

## 13. Source ledger and update policy

- OCI regions / 3 ADs / subscribed region limit: https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm
- OCI Always Free: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- OCI free account lifecycle and trial cap: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- OCI India current rate card: https://www.oracle.com/in/cloud/price-list/
- OCI price consistency worldwide: https://www.oracle.com/cloud/economics/
- Oracle paid account first 3k OCPU-h/18k GB-h: same published India rate card (verify in tenancy)
- Android Maps SDK billing: https://developers.google.com/maps/documentation/android-sdk/usage-and-billing
- Firebase FCM pricing: https://firebase.google.com/pricing
- Play subscription service fee: https://support.google.com/googleplay/android-developer/answer/112622?hl=en-in
- Google Play Console registration: https://support.google.com/googleplay/android-developer/answer/6112435

Re-run this financial model when Oracle changes free-tier limits, when account switches billing type, on new Maps provider quotas, when the product introduces extra media capture, or when the real tracking samples/day materially differ from **300**. All figures **exclude taxes unless clearly stated**.

**Document status:** researched deployment/cost design, not actual provisioning or a provider quote.
