# Phase 7: GitHub README Documentation

Continues `webconsulting-create-documentation` from [full guide](full-guide.md).

## Phase 7: GitHub README Documentation

Use the same assets (illustrations, video) to enrich your GitHub `README.md` with
visual documentation. This makes the repository professional and immediately
communicates value to contributors and potential users.

### Strategy

```
README.md documentation flow:
1. Re-use existing illustrations from public/help/
2. Generate additional screenshots/GIFs specific to README sections
3. Upload video to GitHub release or external host (too large for git)
4. Embed everything with standard Markdown + HTML
```

### Embedding screenshots in README

GitHub renders standard Markdown images. Place screenshots in a `docs/` or
`.github/` directory and reference them with relative paths:

```markdown
## Dashboard

![Dashboard overview](docs/screenshots/dashboard.png)

The main dashboard shows all monitored TYPO3 installations at a glance,
with health scores and security alerts.
```

**Best practices for README screenshots:**
- Use 1200px width (GitHub caps display at ~900px, 2× for retina)
- Prefer light theme or show both with `<picture>` for dark mode support
- Add a 1px border or subtle shadow so screenshots don't bleed into the page
- Keep file sizes under 500KB (PNG with compression or JPEG at 85%)

### Dark/light theme images

GitHub supports `<picture>` with `prefers-color-scheme` media queries:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/dashboard-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/screenshots/dashboard-light.png">
  <img alt="Dashboard overview" src="docs/screenshots/dashboard-light.png" width="800">
</picture>
```

### Generating screenshots for README

You have two approaches:

**1. AI-generated illustrations (fast, always available):**

```
GenerateImage({
  description: "Clean screenshot-style illustration of a TYPO3 monitoring
    dashboard. Dark theme, stat cards showing Total Clients: 42,
    Healthy: 38, Warning: 3, Critical: 1. Sidebar navigation visible.
    Modern, polished UI. 1200×675px, 16:9 aspect ratio.",
  filename: "docs/screenshots/dashboard.png"
})
```

**2. Real screenshots via Playwright (pixel-perfect):**

```typescript
// scripts/capture-screenshots.ts
import { chromium } from "playwright";

async function captureScreenshots() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 675 } });

  // Login if needed
  await page.goto("http://localhost:3001");

  // Capture each page
  const pages = [
    { url: "/", name: "dashboard" },
    { url: "/clients", name: "clients" },
    { url: "/extensions", name: "extensions" },
    { url: "/help", name: "help" },
  ];

  for (const p of pages) {
    await page.goto(`http://localhost:3001${p.url}`);
    await page.waitForTimeout(2000); // Let animations settle
    await page.screenshot({ path: `docs/screenshots/${p.name}.png` });
    // Also capture dark mode
    await page.emulateMedia({ colorScheme: "dark" });
    await page.screenshot({ path: `docs/screenshots/${p.name}-dark.png` });
    await page.emulateMedia({ colorScheme: "light" });
  }

  await browser.close();
}

captureScreenshots();
```

Add to `package.json`:
```json
"screenshots:capture": "tsx scripts/capture-screenshots.ts"
```

### Animated GIFs for README

Short GIFs are more engaging than static screenshots for interactive features
(wizard, sorting, filtering). Use Playwright to record and `ffmpeg` to convert:

```bash
# Record a video clip with Playwright (outputs .webm)
# Then convert to GIF:
ffmpeg -i recording.webm -vf "fps=12,scale=800:-1:flags=lanczos" -loop 0 docs/screenshots/wizard.gif
```

Keep GIFs under 5MB. For larger animations, use MP4 with GitHub's video support.

### Embedding the product tour video

GitHub Markdown supports video since 2021. You have three options:

**Option A: Upload to GitHub Release (recommended for open source)**

```bash
# Create a release and attach the video
gh release create v1.0.0 public/help/product-tour.mp4 \
  --title "v1.0.0" --notes "Initial release"
```

Then link in README:

```markdown
## Product Tour

https://github.com/your-org/your-repo/releases/download/v1.0.0/product-tour.mp4
```

GitHub auto-embeds the video player when the URL is on its own line.

**Option B: Drag-and-drop into GitHub Issue/PR**

1. Create a GitHub issue or PR
2. Drag the MP4 into the comment editor
3. Copy the resulting `user-attachments` URL
4. Paste into README

```markdown
## Product Tour

https://github.com/user-attachments/assets/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Option C: External host (YouTube, Vimeo)**

If the video is large (>25MB) or you want analytics, upload to YouTube/Vimeo
and embed a thumbnail with a play button:

```markdown
## Product Tour

[![Watch the product tour](docs/screenshots/video-thumbnail.png)](https://youtu.be/your-video-id)
```

### Full README template with documentation

Here's a recommended structure integrating all visual assets:

```markdown
# Project Name

> One-line description — aspirational, concise.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/hero-dark.png">
  <img alt="Project screenshot" src="docs/screenshots/hero-light.png" width="800">
</picture>

## Product Tour

https://github.com/your-org/repo/releases/download/v1.0.0/product-tour.mp4

## Features

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
Description of the dashboard...

### Client Management
![Clients](docs/screenshots/clients.gif)
Description of client features...

## Quick Start
...installation instructions...
```

### Updating documentation on changes

When the UI changes, re-run the documentation pipeline:

```bash
# 1. Capture fresh screenshots (if using Playwright)
npm run screenshots:capture

# 2. Regenerate illustrations (if using AI)
# → Use GenerateImage tool with updated descriptions

# 3. Update narration if features changed
# → Edit NARRATION_SCRIPT in remotion/ProductTour.tsx
npm run narration:generate

# 4. Re-render the product tour video
npm run remotion:render

# 5. Upload new video to GitHub release
gh release upload v1.x.x public/help/product-tour.mp4 --clobber

# 6. Commit updated screenshots
git add docs/screenshots/ README.md
git commit -m "docs: update screenshots and video for vX.Y.Z"
```

### Directory structure for README documentation

```
project/
├── README.md                          ← Main documentation with embedded visuals
├── docs/
│   ├── screenshots/
│   │   ├── dashboard.png              ← Light theme screenshot
│   │   ├── dashboard-dark.png         ← Dark theme screenshot
│   │   ├── clients.png
│   │   ├── wizard.gif                 ← Animated walkthrough
│   │   ├── hero-light.png             ← Hero image (light)
│   │   ├── hero-dark.png              ← Hero image (dark)
│   │   └── video-thumbnail.png        ← Video poster frame
│   └── SECURITY.md
├── public/help/
│   └── product-tour.mp4              ← Rendered Remotion video
└── scripts/
    ├── capture-screenshots.ts         ← Playwright screenshot automation
    ├── generate-narration.ts          ← TTS generation
    └── generate-music.ts             ← Background music generation
```
