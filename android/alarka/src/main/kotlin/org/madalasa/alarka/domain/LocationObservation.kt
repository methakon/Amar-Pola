package org.madalasa.alarka.domain

/**
 * Design-only, Android-independent data contract. Not an application entry point.
 * Coordinates use fixed-point 1e-6 degrees. Never infer legal permission from DTO presence.
 * No Android Manifest or Gradle build is supplied yet.
 */
data class LocationObservation(
    val eventId: String,
    val observedAtEpochMs: Long,
    val latitudeE6: Int,
    val longitudeE6: Int,
    val accuracyMeters: Float,
    val speedMetersPerSecond: Float?,
    val sourceDeviceId: String
) {
    fun hasPlausibleCoordinates(): Boolean =
        latitudeE6 in -90_000_000..90_000_000 &&
        longitudeE6 in -180_000_000..180_000_000 &&
        accuracyMeters.isFinite() &&
        accuracyMeters >= 0f
}

enum class LocalUploadState {
    PENDING_LOCAL,
    IN_FLIGHT,
    DURABLY_ACKNOWLEDGED,
    REJECTED
}

/**
 * Conceptual inbox receipt. A server QUEUED response is not a GPS trip-completion signal.
 * Runtime auth, Android permission gating, encryption and network code are NOT implemented.
 */
data class DurableGpsReceipt(
    val batchId: String,
    val acceptedCount: Int,
    val processingStage: String
)
