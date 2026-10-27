# Madalasa–Alarka: illustrated face logo revision

Status: owner requested, design/export assets committed, **not Google Play approved or historically authenticated** (2026-10-28).

Source narrative: [1904 Markandeya Purana translation by F. Eden Pargiter](https://books.google.com/books?id=IdxKAQAAMAAJ), a pan-Indian Puranic text. It supplies the story but **no verified original face portraits** for Madalasa or Alarka. New faces are **original AI-generated interpretive artworks**, not copied from modern illustrated editions or claimed historical likenesses.

**Active Figma sources:** [Madalasa adult queen face](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=68-164), [Alarka boy prince face](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=68-173), [combined parent/child website mark](https://www.figma.com/design/TKiZXwjkWdkponF1zNsfli?node-id=68-179). Face art images are generated raster fills; wordmark, framing, background, and graphic layouts are editable Figma layers. Face art source nodes: 75:2 and 76:2. Figma feature graphic frames: 70:200 and 70:213.

**Active delivery assets:** 512x512 32bit full-bleed Play PNG files for both apps and 1024x500 feature JPEGs under `branding/play-store/`; all Android legacy `mipmap-` density PNGs and new transparent portrait foregrounds `android/{madalasa,alarka}/src/main/res/drawable-nodpi/ic_launcher_face.png` (432x432); adaptive XML now uses `@drawable/ic_launcher_face` with existing color backgrounds and geometric monochrome themed symbol. Website dual-face PNG mark, favicons, horizontal wordmark PNGs and 1200x630 social preview are updated under `public/brand/`.

**Legacy artwork retained:** `branding/archive/abstract-v1/` stores previous app/icon/feature assets for rollback. `branding/source/*.svg` and `public/brand/*.svg` are still **legacy geometric vector alternatives**, not portrait masters. To show the new portrait look on the website, use the PNG wordmarks and updated PNG favicons; do not claim matching vector SVG is ready. The small geometric monochrome themed launcher intentionally stays simple.

**Release checks:** Confirm icon 512x512 RGBA <=1MB, feature graphic 1024x500, Android adaptive safe-zone and mask with image at 432px foreground, actual Android manifests/resources/build, Google Play store tests, legal/trademark/AI-art rights and small-size readability. The completed files are artwork candidates, not a deployed application.

English only for initial product UI; future localization remains planned. No camera/mic monitoring claim is conveyed by the portraits.
