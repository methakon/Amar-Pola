package org.madalasa.madalasa.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.madalasa.madalasa.ui.theme.ThemeCTokens

@Composable
fun AuthenticationScreen(
    onAuthenticated: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(ThemeCTokens.Parchment)
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = ThemeCTokens.PaleWarmSurface),
            shape = RoundedCornerShape(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "Guardian Sign-In",
                    style = MaterialTheme.typography.titleLarge,
                    color = ThemeCTokens.DeepIndigo,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "Sign in to view authorized child telemetry. In accordance with DPDP rules, only exact-child invitations accepted by verified guardians are authorized.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = ThemeCTokens.Ink,
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(24.dp))
                Button(
                    onClick = onAuthenticated,
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = ThemeCTokens.DeepIndigo)
                ) {
                    Text("Continue with Synthetic Login", color = ThemeCTokens.Parchment)
                }
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "Synthetic demo mode. No production credentials or real child telemetry.",
                    fontSize = 11.sp,
                    color = ThemeCTokens.MutedText,
                    textAlign = TextAlign.Center
                )
            }
        }
    }
}
