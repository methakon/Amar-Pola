package org.madalasa.alarka

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

/**
 * Synthetic-only visible activity. No implicit permissions, sensors or live child-data access.
 */
class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(TextView(this).apply {
            text = getString(R.string.app_status)
            textSize = 18f
            setPadding(40, 80, 40, 40)
        })
    }
}
