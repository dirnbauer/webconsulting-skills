# Visual regression harness

The bundled harness at [`scripts/run-tests.cjs`](../scripts/run-tests.cjs) drives the skill's main loop: URL discovery from sitemaps, before/after screenshots, comparison, smoke navigation, and Lighthouse runs. It is self-contained Node.js — no external service and no remote repository required.

## Setup

```bash
cd <skill-or-project>/scripts
npm install                # installs Playwright, odiff, pixelmatch, Lighthouse, …
```

Run it inside the DDEV web container so browsers, DNS, and the site share one environment. The public `codingsasi/ddev-playwright` add-on provides persistent in-container browsers:

```bash
ddev add-on get codingsasi/ddev-playwright
ddev restart
ddev install-playwright
```

Environment variables win over `.env`/`.env.local`, which the script reads from the directory above `run-tests.cjs`.

## Actions

```bash
# 1. Discover URLs: main + per-language sitemap.xml, golden-path URLs, random fill
node run-tests.cjs --action=get-urls --domain="https://site.ddev.site" --output="urls.txt"

# 2. Baseline screenshots (before the update)
node run-tests.cjs --action=take-screenshots --url-file="urls.txt" --output="shots/before/"

# 3. Post-update screenshots (identical URL file and settings)
node run-tests.cjs --action=take-screenshots --url-file="urls.txt" --output="shots/after/"

# 4. Compare
node run-tests.cjs --action=compare-screenshots \
  --before-dir="shots/before/" --after-dir="shots/after/" \
  --output-dir="shots/diff/" --json-output="visual-report.json"

# 5. Functional smoke pass (random link clicking) and Lighthouse
node run-tests.cjs --action=smoke-test --domain="https://site.ddev.site"
node run-tests.cjs --action=lighthouse-test --url-file="urls.txt" --json-output="lighthouse.json"
```

## Sampling and devices

- URL discovery reads `https://<domain>/sitemap.xml` plus `https://<domain>/<lang>/sitemap.xml` for every configured language — validate the sitemaps first (Phase 2), or discovery inherits their gaps.
- Sampling defaults: 10 random URLs per sitemap, capped at 100 total, combined with golden-path URLs. Persist `urls.txt` — the identical sample must run before and after the update.
- Screenshot matrix: desktop 1920×1080, tablet 820×1180, phone 390×844 (Playwright device profiles), full-page, after a 2 s stabilization wait.

## Comparison and thresholds

- Engine: `odiff` native binary, with `pixelmatch` as automatic fallback.
- `VISUAL_THRESHOLD` (default `0.1`) is the per-pixel sensitivity; `VISUAL_MINOR_DIFF_PERCENT` (default `1.0`) tolerates sub-percent diffs such as font anti-aliasing. Anything above the tolerance is a defect to fix — never raise thresholds or re-baseline to make a defect disappear.

## Tuning

| Variable | Default | Purpose |
|---|---|---|
| `TEST_BROWSERS` | `chromium,firefox,webkit` | Browser matrix |
| `SITEMAP_CONCURRENCY` | `4` | Parallel sitemap fetches |
| `SCREENSHOT_CONCURRENCY` | `6` | Parallel screenshot workers |
| `SCREENSHOT_RETRIES` | `1` | Retry failed screenshot jobs |
| `COMPARE_CONCURRENCY` | `4` | Parallel comparison workers |
| `SCREENSHOT_STABILIZE_MS` | `2000` | Wait after DOMContentLoaded |
| `SMOKE_TEST_TIMEOUT_SECONDS` | `300` | Smoke-test hard timeout |
| `LIGHTHOUSE_TEST_TIMEOUT_SECONDS` | `600` | Lighthouse hard timeout |

macOS note: Playwright's `chromium-headless-shell` can crash on newer macOS; the script detects Darwin and launches full Chromium with `--headless=new` automatically (`PLAYWRIGHT_CHANNEL=chrome` overrides).
