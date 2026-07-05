# TYPO3 WCAG 2.2 AA Agentic Skill

Local agentic skill for auditing, fixing and documenting TYPO3 accessibility with WCAG 2.2 AA target.

It contains:

- `SKILL.md` — reusable agent instructions.
- `Skills.sh` — local installer/scaffolder.
- `project-template/` — runnable Playwright + axe-core setup.
- full WCAG 2.2 A/AA checkpoint base list for structured manual review.
- no-build Chrome extension for manual-only WCAG checks and `open-issues.yml` export.
- optional Deque axe MCP examples for Cursor and Claude Code.
- DACH/EAA-aware accessibility statement draft generator.
- legal reference examples for Austria, Germany and Switzerland.
- `prompts/local-codex-app-prompt.md` — ready-to-use prompt for the local Codex app.

## Add to webconsulting-skills repo

This bundle is prepared for `https://github.com/dirnbauer/webconsulting-skills`.

Unzip the repo-ready archive in the repository root so the skill lands here:

```text
skills/typo3-wcag22-aa-agentic/SKILL.md
```

Then regenerate/install the repository skills in the usual repo workflow, for example:

```bash
cd /path/to/webconsulting-skills
unzip /path/to/webconsulting-skills-typo3-wcag22-aa-agentic-final.zip
./install.sh --generate-only
./install.sh
```

## Fast use inside a TYPO3 project

```bash
cd skills/typo3-wcag22-aa-agentic
./Skills.sh scaffold --project /path/to/typo3-project
cd /path/to/typo3-project
cp .a11y/a11y.config.example.yml .a11y/a11y.config.yml
# edit baseUrl, sitemapUrl, contact data, legal.profile and sitepackage paths
npm install
npx playwright install chromium
npm run a11y:all
```


## Manual Chrome review helper

The skill now includes a local Chrome extension for manual WCAG checks:

```text
project-template/manual-review/chrome-extension/
```

After scaffolding into a TYPO3 project, load it in Chrome:

```text
chrome://extensions → Developer mode → Load unpacked → manual-review/chrome-extension
```

It contains the full active WCAG 2.2 A + AA checkpoint list:

```text
.a11y/checkpoints/wcag22-aa-checkpoints.yml
manual-review/chrome-extension/data/wcag22-aa-checkpoints.json
```

The list has 55 active checkpoints: 31 Level A and 24 Level AA. WCAG 2.2 removed 4.1.1 Parsing; it is included only as a legacy helper for WCAG 2.0/2.1 policies.

Use the extension to export manual review evidence and issue fragments:

```text
.a11y/manual-review/YYYY-MM-DD-page.json
.a11y/manual-review/YYYY-MM-DD-page-open-issues.yml
```

Then merge the manual review into the structured source of truth:

```bash
npm run a11y:manual:merge
# or for one exported file:
npm run a11y:manual:merge:file -- .a11y/manual-review/YYYY-MM-DD-page-open-issues.yml
```

The accessibility statement draft is generated from `.a11y/open-issues.yml` plus documented exceptions. Do not publish a statement that was free-written outside this structured issue/exception list.

## Legal profiles

The config supports example profiles for Austria, Germany, Switzerland and voluntary/internal WCAG targets:

```yaml
legal:
  # Austria
  # profile: "at-public-wzg"
  # profile: "at-private-bafg"

  # Germany
  # profile: "de-public-bgg-bitv"
  # profile: "de-private-bfsg"

  # Switzerland
  # profile: "ch-public-behig-ech0059"

  # Voluntary / contractual
  # profile: "voluntary-wcag22aa"
  profile: "at-public-wzg"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
```

The legal reference files are intentionally examples, not legal advice:

```text
project-template/references/legal-at-notes.md
project-template/references/legal-de-notes.md
project-template/references/legal-ch-notes.md
project-template/references/legal-framework-examples.md
```

## Local Codex app prompt

Use this file as the starting prompt in the local Codex app:

```text
prompts/local-codex-app-prompt.md
```

Fill in project URL, legal profile, sitepackage path and whether Deque axe MCP is available.

## Install as a local skill bundle

```bash
./Skills.sh install --skills-dir "$HOME/.skills"
```

This copies the full skill folder to:

```text
$HOME/.skills/typo3-wcag22-aa-agentic
```

You can then point a local coding agent at that folder or copy the `SKILL.md` into its skill editor.

## Optional Deque axe MCP

Deque axe MCP is optional and requires Deque access. The project template includes example config snippets in:

```text
project-template/mcp/cursor.mcp.example.json
project-template/mcp/claude-code.mcp.example.json
```

Use environment variables for credentials, not committed config files.

## Main commands after scaffold

```bash
npm run a11y:discover          # build URL inventory from sitemap/config
npm run a11y:test:report-only  # scan without failing the build
npm run a11y:test              # scan and fail on configured impact levels
npm run a11y:templates         # static Fluid/SCSS/JS checks
npm run a11y:report            # aggregate markdown/json reports
npm run a11y:statement         # draft Erklärung zur Barrierefreiheit
npm run a11y:manual:merge      # merge Chrome helper exports from .a11y/manual-review
npm run a11y:all               # full report-only pipeline
```

## What this does not replace

It does not replace final legal review or manual WCAG assessment. It intentionally creates a small HITL review queue for alt text, keyboard flows, screenreader sanity checks, PDFs/videos/maps and legal conformance wording.
