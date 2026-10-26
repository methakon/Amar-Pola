# Madalasa & Alarka — Application Naming, Mythological Inspiration and Developer Brand Contract

**Date:** 2026-10-26  
**Decision status:** Product/app display names **APPROVED BY OWNER REQUEST**; Google Play availability, trademark, Android package IDs, icon assets and publisher identity **NOT VERIFIED**.  
**Legacy repository and planning code name:** Amar-Pola — **unchanged** to preserve GitHub links, migration history, tests, documentation cross-references and stable IDs.

## 1. Product family and app names

| Surface | User-visible name (exact English spelling) | Role and purpose |
|---|---|---|
| **Parent/guardian Android application** | **Madalasa** | Family setup, verified guardians, secure child enrollment, available device observation, alerts, lawful child-purpose privacy controls, billing |
| **Child Android companion application** | **Alarka** | Transparent enrollment, device identity, on-device Android permission instructions, honest permission/health/synchronization states and child-initiated check-ins |
| **Connected service/product concept** | **Madalasa & Alarka** (or **Madalasa–Alarka Family Safety**) | Names of paired applications; neither app requires a religion, spiritual belief or faith assertion to use it |
| **Repository identifier / historical project working name** | **Amar-Pola** | Remains the actual repository path https://github.com/methakon/Amar-Pola and a legacy engineering identifier; **do not** present it as the current consumer app title |

**App launcher label:** “Madalasa” on guardian phone; “Alarka” on child phone.  
**Paired onboarding labels:** “Install Alarka on your child's Android phone”, “Open Alarka on the child phone”, “Pair Alarka with Madalasa”, “Continue with Google” in Madalasa (Google login remains a technical candidate; identity alone does not prove custody).  
**Internal API/DB/CI paths:** Keep existing stable backend paths and identifiers until a dedicated compatibility migration is approved. Renaming a brand does **not** authorize changing active identity, package IDs, applicationId, Firebase project, OAuth client, Play subscription product IDs, signing keys, token audiences, domain names or published store URL. Those are separate platform decisions.

## 2. English app concept — the story behind the names

### Madalasa and Alarka: Care, Foresight and Guidance Across Distance

In the **Markandeya Purana**, Queen **Madalasa**, wife of King **Ritadhvaja** (also rendered Ritudhvaja or Kuvalayashva), is remembered for educating her sons with wisdom, self-discipline and reflection. Her fourth son, **Alarka**, receives instruction about duty, leadership and the choices that sustain a good life.

As Madalasa and her husband prepare to retire to the forest, she gives Alarka a **ring containing a written message**, instructing him to read it if he later faces severe hardship. When Alarka encounters a grave crisis involving his brother Subahu and the king of Kashi, he remembers the ring, reads his mother's counsel and seeks the wisdom of **Dattatreya**. The story emphasizes the lasting value of a mother's guidance even when she is no longer physically beside her son.

**Our modern interpretation:** **Madalasa**, the guardian app, represents thoughtful parental care and informed responsibility. **Alarka**, the companion app on the child's device, represents a young person's safety, individuality and developing independence. Together, the apps seek to give families **truthful, permission-based information**, a way to stay in touch, and transparent support when they are apart — respecting the child's rights, dignity and privacy.

This is **a cultural and product-design inspiration**, not a claim that the original text describes smartphones, GPS, digital tracking or a technological mechanism for remote observation.

### Source accuracy / the “divine remote viewing” motif

Some modern retellings creatively evoke **yogic foresight, remote sight or an invisible protective shield** to describe Madalasa's maternal intuition. Those are **interpretive metaphors** for this product concept. In the checked English translation of the **Markandeya Purana, Cantos XXVI–XXVII and XXXVI–XXXVII**, the directly supported narrative describes her teaching Alarka, giving him a ring with written guidance, and his use of that message in distress. These passages **do not substantiate continuous supernatural remote viewing of his daily movements or mind**. Do not advertise a literal scriptural passage or divine power as if it described remote surveillance.

**Primary story references:**
- Markandeya Purana, Canto XXVI — the education and naming of Alarka: https://www.wisdomlib.org/hinduism/book/the-markandeya-purana/d/doc117059.html
- Canto XXVII — Madalasa's instruction to Alarka: https://www.wisdomlib.org/hinduism/book/the-markandeya-purana/d/doc117060.html
- Canto XXXVI — the ring and advice for future hardship: https://www.wisdomlib.org/hinduism/book/the-markandeya-purana/d/doc117072.html
- Canto XXXVII — Alarka in difficulty remembers the ring and seeks guidance: https://www.wisdomlib.org/hinduism/book/the-markandeya-purana/d/doc117073.html
- Translation reference: F. Eden Pargiter, *The Markandeya Purana* (1904). The ancient narrative has variant transliterations and retellings.

## 3. Why these names match functional responsibilities

| Narrative inspiration | Madalasa guardian app | Alarka child app | Important boundary |
|---|---|---|---|
| Madalasa's wisdom and foresight | Quality-aware, **last-observed** family information; explain uncertainty | Report observations only with actual Android and lawful purpose authorization | No magical “always live”/hidden tracking claim |
| Thoughtful preparation for future distress | Parent sees permission/connection reliability and clear check-in acknowledgements | Child can initiate a visible check-in and contact a trusted adult | No guaranteed emergency response until tested independent fallback |
| Ring carrying guidance | Parent gives clear **visible setup steps** and reviewable guardian permissions | Child receives an explicit setup/instruction flow on their own device | A paired code is not legal guardian verification; parent cannot grant OS permissions remotely |
| Alarka's independence | Scoped guardians and temporary grants, audit and deletion | Child transparency center and access information | The child is a person, not an object to be secretly watched |
| Support across distance | Privacy-aware family connection with real status timestamps | OS-governed, verifiable and revocable device participation | History and app-usage behavioural monitoring disabled for Indian minors pending separate legal review |

**Suggested optional marketing tagline (not approved final store copy):** “Thoughtful care. Honest connection.”  
**Alternative concept line:** “Inspired by a mother's lasting guidance; designed for modern family safety with transparency and choice.”  
Avoid “divine remote seeing”, “watch every step in secret”, “unbreakable protection”, “guaranteed rescue”, “track without knowing” and similar unsupported or unsafe claims.

## 4. UI/UX text and release specifications

- **Parent splash:** “Madalasa” and an optional small description, “Family Safety”. Primary: “I'm a parent or guardian” and “Set up Alarka on a child's device”.
- **Parent sign-in:** “Sign in to Madalasa”; “Continue with Google”; “Verify your authority to manage this child's device” separately when legally required.
- **Parent setup journey:** “Step 1 — Install Alarka”; “Step 2 — Pair Alarka securely”; “Step 3 — Review child-data purposes”; “Step 4 — Follow permissions on the Alarka phone”; “Step 5 — Check Alarka device status”.
- **Child splash:** “Alarka”; “Companion app for visible, authorized family safety setup”; “Who can access my information?”.
- **Child permissions:** “On this phone, open Android Settings”; report GRANTED/DENIED/UNSUPPORTED/OS_REJECTED based on actual OS state; do not claim that Madalasa changed these permissions remotely.
- **Parent dashboard:** “Children” labels are ordinary generic concepts; “Alarka” is the **app**, not the child's name, account display alias, or a claim every enrolled child is Alarka.
- **App switch / pairing:** “Alarka device” is the child-device endpoint; authenticated paired Madalasa guardian accounts can read only approved child scopes.
- **Store descriptions and Data Safety:** use app names with separate app roles and accurate declared data flows; do not claim guaranteed background tracking, emergency dispatch or remote camera/mic bypass.
- **English is canonical spelling for developer strings:** Madalasa / Alarka. Sanskritized forms Madālasā / Alarka and Bengali/other script localization can be added via Android \`strings.xml\` translations without changing English brand IDs.
- **App icon and imagery:** cultural motif may reference a ring or guiding light **abstractly**, but avoid inventing a religious endorsement, depicting a specific deity as a tracker, or demanding religious affiliation of users. Logos, trademarks and publication assets require independent validation.

## 5. Developer migration checklist and unresolved public-release matters

**Documentation-only rename:** User-visible names are specified; code packages have not been authored/renamed as part of this update. Plan a later atomic Android implementation migration:
1. Separate Gradle app modules \`parent-android\` and \`child-android\` (or chosen names); launcher strings use **Madalasa** and **Alarka**.
2. Choose **two unique immutable application IDs** **before first Play upload**. Example placeholders may be \`<approved.domain>.madalasa\` and \`<approved.domain>.alarka\` only after publisher domain approval; **do not use a guessed owner domain**.
3. Establish parent OIDC OAuth app identity, Alarka Android Keystore enrollment identity, matching package signature pinning and Google Play Console app declarations. Never assume changing display label changes authorization/crypto.
4. Android parent-to-child walkthrough and any FCM/SMS notifications use actual brand strings; capability and OS notification disclosure identify **Alarka** explicitly on the child's device.
5. Update parent/child Figma screen titles and linked Eraser/tldraw visuals during next connected visual-design sync. **Existing saved visual canvases still contain legacy “Amar-Pola” text**, since documentation changes do not automatically update Figma/Eraser/tldraw. Their current links remain valid.
6. Google Play listings and legal notices must name the correct publisher and app separately, and cover India DPDP child-age, purpose, storage/processor, deletion and grievance rules.
7. Check name availability/trademark/IP and pronunciation; approved publishing name and support URL still open (B-01/B-02).
8. Preserve historical citations, GitHub repository URLs and stable M1 OpenAPI data contracts. Any future consumer-domain or GitHub repo rename needs a separate migration/redirect plan.

## 6. Documentation precedence and scope

This naming and narrative policy **supersedes older use of “Amar-Pola” as a consumer application title** in the README, SRS, technical specs, architecture diagrams, SRS labels, onboarding and Play/privacy draft descriptions. It **does not** replace repo/org names, filenames, paths, historical references, or code/SQL/OpenAPI identifiers by default. When an old file says “Amar-Pola Parent App”, read **Madalasa**. When it says “Amar-Pola Child App”, read **Alarka**.

**The design remains a transparent, legally constrained family-safety product. Naming inspired by mythology does not change the Android security model, children's consent and privacy duties, or the product's approved feature set.**
