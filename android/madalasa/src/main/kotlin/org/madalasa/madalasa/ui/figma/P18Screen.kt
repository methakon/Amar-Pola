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
 * P-18 — Plans and app settings
 * Canonical Figma handoff: docs/ui/figma-functional-handoff/
 * Requirements: FR-012/039; milestone M7.
 * TODO(INTEGRATION/API): Play product details and backend verified subscriptionsv2
 * TODO(INTEGRATION/SECURITY): Prices proposed; checkout governs tax, period and amount
 * TODO(INTEGRATION/ERROR): Payment pending; unsupported child capability
 * Acceptance: No seats granted until verified paid state.
 * Visual-only screen: actions deliberately disabled; no user records or permissions accessed.
 */
@Composable
fun P18Screen(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)
        .verticalScroll(rememberScrollState()).padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("MADALASA", style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.weight(1f))
            Text("P-18", style = MaterialTheme.typography.labelMedium)
        }
        Text("Plans and app settings", style = MaterialTheme.typography.headlineMedium)
        Text("Family subscription options", style = MaterialTheme.typography.bodyLarge)
        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)) {
            Text("Plan eligibility and prices need verified Play response", Modifier.padding(16.dp),
                style = MaterialTheme.typography.bodyMedium)
        }
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("01", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("₹50 monthly", style = MaterialTheme.typography.bodyMedium)
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
                    Text("₹500 yearly per child", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("03", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("seats", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(shape = CircleShape, color = MaterialTheme.colorScheme.secondaryContainer, modifier = Modifier.size(34.dp)) {
                    Box(contentAlignment = Alignment.Center) { Text("04", style = MaterialTheme.typography.labelMedium) }
                }
                Column(Modifier.weight(1f)) {
                    Text("theme preference", style = MaterialTheme.typography.bodyMedium)
                    Text("Not connected", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        Button(onClick = { /* TODO(INTEGRATION): connect verified action */ }, enabled = false,
            modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp)) {
            Text("Review actual Play checkout")
        }
        Text("Preview only · no action or data access", style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
