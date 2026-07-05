# Local Codex App Prompt: TYPO3 WCAG 2.2 AA Accessibility Skill

Use this prompt in the local Codex app from the root of the TYPO3 project you want to audit/fix.

---

You are working in a local TYPO3 repository. Use the webconsulting skill at:

```text
skills/typo3-wcag22-aa-agentic/SKILL.md
```

or, if this is a project-local scaffold only:

```text
.a11y/a11y.config.yml
```

## Task

Audit and improve this TYPO3 website/sitepackage for accessibility with a WCAG 2.2 AA technical target and generate a draft Erklärung zur Barrierefreiheit / accessibility statement. Use a small mandatory HITL review queue only for items that cannot be safely decided automatically.

## Project variables

Fill these before running:

```yaml
baseUrl: "https://PROJECT.ddev.site"
sitemapUrl: "https://PROJECT.ddev.site/sitemap.xml"
productionUrl: "https://www.example.at"
sitepackagePaths:
  - "packages/sitepackage"
  - "public/typo3conf/ext/sitepackage"
legalProfile: "at-public-wzg" # choose: at-public-wzg, at-private-bafg, de-public-bgg-bitv, de-private-bfsg, ch-public-behig-ech0059, voluntary-wcag22aa
dequeMcpAvailable: false
manualChromeReviewAvailable: true
manualReviewExportDir: ".a11y/manual-review"
```

## Required workflow

1. Read `skills/typo3-wcag22-aa-agentic/SKILL.md` if available. If not available, use the project-local `.a11y` files and references.
2. Inspect the TYPO3 project structure and identify sitepackage paths, Fluid templates, SCSS/CSS, JavaScript components, RTE/TCA config, and Composer/npm setup.
3. If the `.a11y` tooling is not scaffolded yet, scaffold or create the equivalent files from the skill template.
4. Configure `.a11y/a11y.config.yml` with the base URL, sitemap URL, sitepackage paths, contact placeholders and selected `legal.profile`.
5. Run or prepare these commands:

```bash
npm install
npx playwright install chromium
npm run a11y:discover
npm run a11y:test:report-only
npm run a11y:templates
npm run a11y:report
npm run a11y:statement
```

6. If Playwright/npm cannot run locally, still perform static inspection and prepare exact commands, patches and expected outputs. Be explicit about what did not run.
7. For each finding, map rendered selectors back to TYPO3 templates/components where possible. Prefer fixes in Fluid/SCSS/JS/TCA/RTE config, not only rendered HTML.
8. Apply safe fixes directly. Use native HTML before ARIA. Do not hide focus outlines. Do not add positive tabindex. Do not suppress axe rules without owner, reason and expiry.
9. Re-test the exact failing URL/state after each fix when possible.
10. Merge manual Chrome-helper findings when present:

```bash
npm run a11y:manual:merge
```

11. Generate or update:

```text
.a11y/url-inventory.json
.a11y/raw/*.json
.a11y/report.json
.a11y/report.md
.a11y/open-issues.yml
.a11y/template-lint.json
.a11y/template-lint.md
.a11y/accessibility-statement-draft.de.md
```


## Manual Chrome helper workflow

Use the bundled Chrome extension for human-only WCAG checks:

```text
manual-review/chrome-extension
```

The extension contains the full active WCAG 2.2 Level A + Level AA checklist and exports structured evidence. Treat these files as inputs:

```text
.a11y/checkpoints/wcag22-aa-checkpoints.yml
.a11y/manual-review/*.json
.a11y/manual-review/*-open-issues.yml
```

After a human reviewer exports files from the Chrome helper, merge them before generating the statement:

```bash
npm run a11y:manual:merge
npm run a11y:statement
```

Important rule: do not free-write the Erklärung zur Barrierefreiheit. The statement draft must be generated from `.a11y/open-issues.yml` and documented exceptions only. If an issue is not in `.a11y/open-issues.yml`, either add it structurally or do not mention it as a known non-conformity.

## Legal profile rules

Keep Austria examples and add Germany/Switzerland when relevant:

- `at-public-wzg`: Austrian public-sector WZG / EN 301 549 statement style.
- `at-private-bafg`: Austrian BaFG / EAA context only if the service/product is in scope.
- `de-public-bgg-bitv`: German public-sector BGG + BITV 2.0 context; verify Landesrecht for state/municipal projects.
- `de-private-bfsg`: German BFSG / EAA context only if the product/service is in scope.
- `ch-public-behig-ech0059`: Swiss public-sector BehiG/BehiV + eCH-0059 context; note that eCH-0059 v3 is WCAG 2.1 AA based, while WCAG 2.2 AA can remain the internal higher target.
- `voluntary-wcag22aa`: internal/contractual WCAG 2.2 AA target without statutory claim.

Do not give final legal advice. Mark generated statements as drafts and require HITL/legal approval before publication.

## Optional Deque axe MCP

If Deque axe MCP is configured and credentials are available, use it to accelerate analysis/remediation:

- Use `analyze` for rendered page states.
- Use `remediate` for targeted fix guidance.
- Use `igt` only if guided manual testing is explicitly useful and the subscription allows it.

The repeatable baseline remains Playwright + axe-core in this repo.

## HITL queue

Keep the human review small but mandatory for:

- meaningful alt text;
- keyboard flow and focus logic;
- Screenreader smoke test with VoiceOver/NVDA;
- PDFs, videos, maps and third-party embeds;
- legal profile, enforcement body, exceptions and final status wording;
- publication approval of the accessibility statement.

## Final response format

Return:

1. What you changed.
2. Commands run and their result.
3. Remaining blocking accessibility issues.
4. Generated files and where to find them.
5. HITL checklist, including which WCAG 2.2 A/AA checkpoints remain not tested.
6. Confirmation that the statement draft was generated from `.a11y/open-issues.yml`, not free-written.
7. One clear next step.

Never claim “fully WCAG compliant” from automated tests alone.
