package org.madalasa.madalasa.di

import org.madalasa.madalasa.api.MadalasaApiClient
import org.madalasa.madalasa.api.SyntheticMadalasaApiClient
import org.madalasa.madalasa.repository.MadalasaRepository
import org.madalasa.madalasa.repository.SyntheticMadalasaRepository

/**
 * Lightweight manual Dependency Injection container.
 */
interface AppContainer {
    val apiClient: MadalasaApiClient
    val repository: MadalasaRepository
}

class DefaultAppContainer : AppContainer {
    override val apiClient: MadalasaApiClient by lazy {
        SyntheticMadalasaApiClient()
    }

    override val repository: MadalasaRepository by lazy {
        SyntheticMadalasaRepository(apiClient)
    }
}
