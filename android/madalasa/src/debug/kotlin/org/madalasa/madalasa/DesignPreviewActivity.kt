package org.madalasa.madalasa

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import org.madalasa.madalasa.ui.figma.ParentFigmaScreen
import org.madalasa.uicommon.MadalasaTheme
import org.madalasa.uicommon.ScreenId

/**
 * DEBUG BUILD ONLY: standalone navigation into all 60 Figma source screens.
 * Does not use the production NavHost, authentication, OS permissions or APIs.
 * TODO(INTEGRATION): connect reviewed final screen routes after visual/UX QA.
 * Launch through Android Studio's Run configuration or adb explicit activity.
 */
class DesignPreviewActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MadalasaTheme { DesignPreviewGallery() } }
    }
}

@Composable private fun DesignPreviewGallery() {
    var selected by remember { mutableStateOf<String?>(null) }
    BackHandler(enabled = selected != null) { selected = null }
    val active = selected
    if (active != null) {
        Column {
            TextButton(onClick = { selected = null }, modifier = Modifier.padding(8.dp)) {
                Text("All screen designs")
            }
            ParentFigmaScreen(ScreenId(active))
        }
    } else {
        val ids = (1..60).map { "P-%02d".format(it) }
        LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            item {
                Text("Madalasa parent design previews",
                    style = MaterialTheme.typography.headlineSmall)
                Text("DEBUG ONLY · No live device monitoring or API access")
            }
            items(ids) { id ->
                ElevatedCard(modifier = Modifier.fillMaxWidth().clickable { selected = id }) {
                    Text(id, modifier = Modifier.padding(18.dp), style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}
