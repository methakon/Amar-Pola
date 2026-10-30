plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "org.madalasa.alarka"
    compileSdk = 36

    defaultConfig {
        // Intentionally non-production. Replace only after confirmed package identity
        // and a completed release/permission review.
        applicationId = "org.madalasa.alarka.synthetic"
        minSdk = 29
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0-synthetic"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        buildConfig = false
    }
}

dependencies {
    testImplementation("junit:junit:4.13.2")
}
