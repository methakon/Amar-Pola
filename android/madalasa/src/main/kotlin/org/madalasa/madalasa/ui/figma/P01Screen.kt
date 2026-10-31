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
 * P-01 — Welcome
 * Canonical Figma handoff: docs/ui/figma-functional-handoff/
 * Requirements: FR-001/041; milestone M1.
 * TODO(INTEGRATION/API): Local navigation; no API before user action
 * TODO(INTEGRATION/SECURITY): No collection until lawful authority and child disclosure
 * TODO(INTEGRATION/ERROR): Offline; wrong role; policy unavailable
 * Acceptance: Both paths available; no child record created here.
 * Visual-only screen: actions deliberately disabled; no user records or permissions accessed.
 */
@Composable
fun P01Screen(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)
        .verticalScroll(rememberScrollState()).padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("MADALASA", style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.weight(1f))
            Text("P-01", style = MaterialTheme.typography.labelMedium)
        }
        Text("Welcome", style = MaterialTheme.typography.headlineMedium)
        Text("Welcome to Madalasa: family safety with transparency", style = MaterialTheme.typography.bodyLarge)
        OutlinedTextField(value = "", onValueChange = {}, enabled = false, readOnly = true,
            label = { Text("Preview only") }, modifier = Modifier.fillMaxWidth())
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("01", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("Parent or Child entry", style = MaterialTheme.typography.bodyMedium)
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
                    Text("privacy, support and language links", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Button(onClick = { /* TODO(INTEGRATION): connect verified action */ }, enabled = false,
            modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp)) {
            Text("Start parent setup")
        }
        Text("Preview only · no action or data access", style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
