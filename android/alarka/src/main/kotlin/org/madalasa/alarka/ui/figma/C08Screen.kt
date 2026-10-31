package org.madalasa.alarka.ui.figma

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * C-08 — Notification Settings guide
 * Canonical Figma handoff: docs/ui/figma-functional-handoff/
 * Requirements: FR-002/014; milestone M1.
 * TODO(INTEGRATION/API): POST_NOTIFICATIONS as supported by OS; capability report
 * TODO(INTEGRATION/SECURITY): App may not force notification allowance or DND bypass
 * TODO(INTEGRATION/ERROR): Disabled channel; API old; OS_REJECTED
 * Acceptance: Reported notification status matches device truth.
 * Visual-only screen: actions deliberately disabled; no user records or permissions accessed.
 */
@Composable
fun C08Screen(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)
        .verticalScroll(rememberScrollState()).padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("ALARKA", style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.weight(1f))
            Text("C-08", style = MaterialTheme.typography.labelMedium)
        }
        Text("Notification Settings guide", style = MaterialTheme.typography.headlineMedium)
        Text("Allow visible status and alerts", style = MaterialTheme.typography.bodyLarge)
        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)) {
            Text("No device permissions or monitoring enabled in this design", Modifier.padding(16.dp),
                style = MaterialTheme.typography.bodyMedium)
        }
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("01", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("Android notification permission/channel list", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("02", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("test notice", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Button(onClick = { /* TODO(INTEGRATION): connect verified action */ }, enabled = false,
            modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp)) {
            Text("Open notification settings")
        }
        Text("Preview only · no action or data access", style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
