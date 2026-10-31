package org.madalasa.madalasa.ui.figma

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
 * P-22 — Map evidence legend
 * Canonical Figma handoff: docs/ui/figma-functional-handoff/
 * Requirements: FR-028/030; milestone M3.
 * TODO(INTEGRATION/API): Quality codes and source timestamps in route result
 * TODO(INTEGRATION/SECURITY): Parent can flag interpretation, not change raw GPS
 * TODO(INTEGRATION/ERROR): Unknown source; missing accuracy
 * Acceptance: Accessible map colors and legend agree.
 * Visual-only screen: actions deliberately disabled; no user records or permissions accessed.
 */
@Composable
fun P22Screen(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)
        .verticalScroll(rememberScrollState()).padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("MADALASA", style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.weight(1f))
            Text("P-22", style = MaterialTheme.typography.labelMedium)
        }
        Text("Map evidence legend", style = MaterialTheme.typography.headlineMedium)
        Text("Every marker has a meaning", style = MaterialTheme.typography.bodyLarge)
        Card(Modifier.fillMaxWidth(), shape = RoundedCornerShape(20.dp)) {
            Box(Modifier.fillMaxWidth().height(208.dp).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("MAP PREVIEW", style = MaterialTheme.typography.labelMedium)
                    Text("Position unknown • no verified observation", style = MaterialTheme.typography.bodySmall)
                }
            }
        }
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("01", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("OBSERVED, APPROXIMATE, GAP, STOP_CONFIRMED", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Button(onClick = { /* TODO(INTEGRATION): connect verified action */ }, enabled = false,
            modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp)) {
            Text("Inspect evidence")
        }
        Text("Preview only · no action or data access", style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
