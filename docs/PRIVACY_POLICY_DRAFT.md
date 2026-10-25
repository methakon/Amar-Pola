# Privacy Policy — Publication Draft (NOT READY TO PUBLISH)

**Amar-Pola | draft 2026-10-25**

> **LEGAL/PRODUCT REVIEW REQUIRED.** Every bracketed field and TBD must be completed before hosting as a public policy. Do not claim an implemented feature, encryption measure or deletion SLA until it is actually verified. This is a template for the intended product, not the live policy of an operating service.

## 1. Who operates Amar-Pola?

Amar-Pola is planned as a parental device-safety and monitoring service operated by **[LEGAL BUSINESS NAME]** (“we”). Contact us at **[PUBLIC SUPPORT EMAIL]**, **[BUSINESS ADDRESS / RELEVANT LEGAL CONTACT]**. Last effective date: **[PUBLICATION DATE]**.

The service is intended for appropriately authorized parents and guardians to supervise their children's devices. It is not intended for covert monitoring of adults or other unauthorized individuals.

## 2. Information the service may collect

We expect to process only data needed for features the parent has activated and the child device has been configured to support:
- Parent account details and authentication identifiers.
- Paired device identity, capability state, version, pairing and security logs.
- Location, collection timestamp and accuracy, optionally reported speed, to show current/recent location and travel history.
- App usage identifiers and duration for usage reports, after required Android special access is granted.
- Remote-control policies and authenticated command execution status.
- Diagnostic events needed for security/reliability **[LIST ACTUAL SDKs]**.
- Subscription and entitlement metadata; payment card information is expected to be handled by the payment provider, not by our backend.
- Photos/video/audio only if a separate transparently authorized, released feature permits their creation and transfer; **not a promise that such functionality will be offered**.
- Parent-authorized Google Drive information needed to back up selected permitted media.

For a final live version, specify **exactly** which items are collected, whether optional, and any new SDK data collection.

## 3. How information is used

We intend to use information to provide the parent's requested map/history and app-usage reports, execute supported authorized controls, operate pairing/security, provide paid entitlements, detect outages and abuse, and comply with applicable legal obligations. We will not present monitoring as hidden or claim unsupported device privileges.

## 4. Background location and device indicators

Where enabled and permitted, Amar-Pola can collect location **when the setup screen is closed or the app is not actively open**, to provide parent-visible location and travel history. The child device may display a persistent monitoring notification or other Android privacy indicators, which Amar-Pola will not conceal. Android settings may allow permissions to be revoked. Certain features may then stop working.

## 5. Who receives information?

The authorized paired parent account can view supported child-device reports. Selected authorized information may be processed by **[ACTUAL CLOUD/HOSTING PROVIDER]**, **[AUTH PROVIDER]**, Google services used for map/notification/billing/Drive purposes, and **[OTHER NAMED SUBPROCESSORS]** subject to appropriate terms. Describe cross-border transfers and legal jurisdictions at release. **Do not claim “no sharing” without checking Play's definitions and all SDK flows.**

## 6. Security

The planned system uses encrypted transport, authenticated access controls, revocable device credentials and appropriate encryption at rest. **These are target controls and must be verified on the production build** before this paragraph becomes public.

## 7. Retention and deletion

Planned retention periods: location **[X DAYS]**, app usage **[Y DAYS]**, optional media **[Z DAYS]**, audit logs **[AUDIT RETENTION]**, backups **[BACKUP POLICY]**. Actual operations must implement and test these dates.

Parents may revoke a device, disconnect Google Drive and request account/data deletion within the app or at **[PUBLIC ACCOUNT DELETION URL]**. Explain which billing/fraud/legal records are retained, for what legal basis and for how long. Deleting Amar-Pola server data may not delete independently stored files in the parent's Google Drive; clarify and offer options.

## 8. Parental authority and child privacy

Only a person with the required legal authority should enroll a child's phone. Review regional consent/child privacy requirements before launch, including intended countries and age ranges **[TARGET JURISDICTIONS AND AGE POLICY]**. The child agent will have a recognizable identity and required disclosure and notifications.

## 9. Your choices

A parent may review enabled features, revoke pairing, manage the subscription, request deletion and revoke cloud integrations. Android permissions and some special-access settings can be changed in device Settings. Revoking access may prevent location or usage reports from updating.

## 10. Changes

We will update the policy and notify users where required if data handling or the feature set materially changes. Prior versions and effective dates will be archived **[POLICY VERSIONING PROCESS]**.

## Must-complete publication checklist

- [ ] Operator legal name/contact validated
- [ ] All SDKs and backend data recipients listed
- [ ] Actual retention and deletion behavior tested
- [ ] Play Data safety wording reconciled with collection
- [ ] In-app and store listing public privacy-policy links verified
- [ ] Child-specific disclosure, consent and legal review completed
- [ ] Account deletion web URL functional without requiring app install
- [ ] Accessibility/language review
- [ ] Public policy revised and approved by counsel
