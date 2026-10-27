# Android workspace — initial source layout (NOT RUNNABLE)

The repository had **no Android Gradle projects** at this review. This skeleton reserves the implementation boundaries without declaring Android runtime permissions, shipping a noncompliant monitoring app, or implying functioning APKs.

- `alarka/`: enrolled child-device companion. Kotlin controls Android lifecycle, permission request/result readback, Fused Location/UsageStats where legally enabled, Keystore-protected encrypted 48-hour offline-capacity queue, 1–2-minute network batching when an eligible service is active, device-bound auth, authorized SOS. Main Activity may close after setup, but Android monitoring notification and sensor indicators remain. All live camera/microphone/media screen functions are **P3 research disabled**.
- `madalasa/`: authenticated guardian UI, child-scoped location, usage and compatible feature status, activity audit and consent/revoke flows; displays last-verified timestamps, does not fake GPS/live app/sensor availability.
- Shared network schema/API/versioning and Android CI **not yet created**. Android package IDs, target SDK, Gradle/AGP/Kotlin versions, Compose, flavor/product setup, signing keystores and manifest permissions require explicit owner/Play/platform decision.

Next engineering steps: establish two independently testable Android Gradle projects, Kotlin source, unit/instrumented tests, versioned API clients, dependency lockfiles, safe dummy fixtures and manifest review; test on Android API29–36+ and OEM/watch variants. Do NOT add raw child data to test fixtures.

Read [implementation spec](../docs/IMPLEMENTATION_TECHNICAL_SPECIFICATION.md), [Android compatibility matrix](../docs/ANDROID_COMPATIBILITY_MATRIX.md), [developer onboarding](../docs/DEVELOPER_ONBOARDING_AND_CODING_STANDARDS.md), [signing policy](../docs/APP_SIGNING_AND_KEY_MANAGEMENT_POLICY.md), [build guide](../docs/BUILD_AND_RUN.md).

**No `gradlew` or AndroidManifest exists today.** The folders are planning scaffolds, not functional code.
