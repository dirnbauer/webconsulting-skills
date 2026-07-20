# Visual regression harness

Two bundled scripts drive the skill's automated checks — self-contained Node.js, no external service and no remote repository required:

- [`scripts/run-tests.cjs`](../scripts/run-tests.cjs) — the main-loop harness: URL discovery from sitemaps, before/after screenshots, comparison, smoke navigation, and a quick Lighthouse pass. **Chromium only** (three device viewports, not multiple browsers).
- [`scripts/backend-module-sweep.cjs`](../scripts/backend-module-sweep.cjs) — the backend module sweep: proves every backend module opens without errors after the update.

The harness is used before the update as well: the Bootstrap 5 upgrade (Phase 2) shoots a reference set, then re-shoots after each small step and once across the full sample — there, intended differences are expected but must each be explained and approved. Site feature upgrades (Solr, Visual Editor, CKEditor RTE, security headers — Phase 7) run between the core upgrade and the final loop closure: re-shoot the affected sample pages after each feature and re-baseline only approved intentional changes.

## Setup

```bash
cd <skill-or-project>/scripts
npm install                # Node >= 20; installs Playwright, odiff, pixelmatch, Lighthouse, …
```

Run inside the DDEV web container so browsers, DNS, and the site share one environment. The public `codingsasi/ddev-playwright` add-on provides persistent in-container browsers:

```bash
ddev add-on get codingsasi/ddev-playwright
ddev restart
ddev install-playwright
```

Configuration comes from environment variables, which always win over the `.env`/`.env.local` files the scripts read from the directory above `run-tests.cjs`. The odiff binary is auto-detected from `scripts/node_modules`; set `ODIFF_BIN` to override.

## Actions

```bash
# 1. Discover URLs: main + per-language sitemap.xml (LANGUAGE_LIST), golden paths, random fill
node run-tests.cjs --action=get-urls --domain="https://site.ddev.site" --output="urls.txt"

# 2. Baseline screenshots (before the update)
node run-tests.cjs --action=take-screenshots --url-file="urls.txt" --output="shots/before/"

# 3. Post-update screenshots (identical URL file and settings)
node run-tests.cjs --action=take-screenshots --url-file="urls.txt" --output="shots/after/"

# 4. Compare
node run-tests.cjs --action=compare-screenshots \
  --before-dir="shots/before/" --after-dir="shots/after/" \
  --output-dir="shots/diff/" --json-output="visual-report.json"

# 5. Functional smoke pass (random link clicking)
node run-tests.cjs --action=smoke-test --domain="https://site.ddev.site" --json-output="smoke-test.json"

# 6. Quick Lighthouse pass (homepage + a few random sitemap pages per run)
node run-tests.cjs --action=lighthouse-test --domain="https://site.ddev.site" --json-output="lighthouse.json"
```

`lighthouse-test` picks its own small sample (homepage plus random sitemap pages) and does **not** read `--url-file`. For the up-to-100-page final audit, loop Lighthouse over the persisted `urls.txt` yourself and aggregate the reports.

## Backend module sweep

```bash
node backend-module-sweep.cjs --base-url="https://site.ddev.site" --output="backend-module-sweep.json"
```

Credentials come from `BE_USER` / `BE_PASSWORD` (environment or `.env` — use a dedicated local admin, never commit credentials). The sweep logs in, discovers every `[data-modulemenu-identifier]` entry in the module menu, opens each module, and fails on exception output, HTTP 5xx responses, or severe browser-console errors. It writes a JSON report (module → status/reasons) and exits non-zero when any module fails. Selector assumptions are documented in the script header — verify them against the installed TYPO3 version if login fails or zero modules are found.

## Sampling and devices

- URL discovery reads `https://<domain>/sitemap.xml` plus `https://<domain>/<lang>/sitemap.xml` for every language in `LANGUAGE_LIST` (comma-separated, default `en,de` — set it to the site's real language prefixes). Sitemap-index files are followed recursively. Validate the sitemaps first (Phase 2), or discovery inherits their gaps.
- `GOLDEN_PATH_URLS` (comma-separated absolute or `/`-relative URLs) adds must-test pages to every sample.
- Sampling defaults: 10 random URLs per sitemap (`RANDOM_URLS_PER_SITEMAP`), capped at 100 total (`MAX_URLS`). Persist `urls.txt` — the identical sample must run before and after the update.
- Screenshot matrix: Chromium with three device viewports — desktop 1920×1080, tablet 820×1180, phone 390×844 (device user agents, device scale factor 1) — full-page, after a 2 s stabilization wait following DOMContentLoaded.

## Comparison and thresholds

- Engine: `odiff` native binary by default, with an automatic `pixelmatch` fallback when odiff fails; `VISUAL_COMPARE_ENGINE=pixelmatch` forces the fallback.
- `VISUAL_THRESHOLD` (default `0.1`) is the per-pixel color-distance sensitivity passed to both engines. `VISUAL_MINOR_DIFF_PERCENT` (default `1.0`) classifies runs with at most that percentage of changed pixels as "minor" — they are still reported, not hidden. Anything above is a defect to fix — never raise thresholds or re-baseline to make a defect disappear.

## Tuning

| Variable | Default | Purpose |
|---|---|---|
| `LANGUAGE_LIST` | `en,de` | Language prefixes for per-language sitemaps |
| `GOLDEN_PATH_URLS` | (empty) | Must-test URLs added to every sample |
| `RANDOM_URLS_PER_SITEMAP` | `10` | Random sample size per sitemap |
| `MAX_URLS` | `100` | Overall URL cap |
| `SITEMAP_CONCURRENCY` | `4` | Parallel sitemap fetches |
| `SCREENSHOT_CONCURRENCY` | up to `6` (CPU-based) | Parallel screenshot workers |
| `SCREENSHOT_RETRIES` | `1` | Retry failed screenshot jobs |
| `SCREENSHOT_STABILIZE_MS` | `2000` | Wait after DOMContentLoaded |
| `COMPARE_CONCURRENCY` | up to `4` (CPU-based) | Parallel comparison workers |
| `COMPARE_WORKER_TIMEOUT_MS` | `120000` | Per-image comparison timeout |
| `VISUAL_TEST_MAX_WORKERS` | `8` | Safety cap for visual-test parallelism |
| `VISUAL_COMPARE_ENGINE` | `odiff` | `odiff` or `pixelmatch` |
| `ODIFF_BIN` | (auto-detected) | Explicit odiff binary path |
| `BROKEN_PAGE_STRINGS` | (built-in list) | Extra error markers for page checks |
| `BE_USER` / `BE_PASSWORD` | (none) | Backend credentials for the module sweep |

macOS note: Playwright's `chromium-headless-shell` can crash on newer macOS; both scripts detect Darwin and launch full Chromium with `--headless=new` automatically (`PLAYWRIGHT_CHANNEL=chrome` overrides).
