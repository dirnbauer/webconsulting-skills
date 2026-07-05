# TYPO3 WCAG 2.2 AA Manual Review Helper Chrome extension

This is a no-build Manifest V3 Chrome extension for manual accessibility checks that cannot be safely decided by automation alone.

It is designed to complement the TYPO3 WCAG 2.2 AA skill:

```text
Playwright/axe automated scan
+ TYPO3 template/static checks
+ Chrome manual helper evidence
→ .a11y/open-issues.yml
→ accessibility statement draft
```

## Install locally

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select this folder:

```text
manual-review/chrome-extension
```

5. Open a local/staging TYPO3 page.
6. Click the extension icon to open the side panel.
7. Click **Connect page**.

## What it does

- Loads the full WCAG 2.2 Level A + AA checkpoint list.
- Helps a human reviewer mark each criterion as pass/fail/not applicable/cannot determine.
- Runs a lightweight page helper scan for headings, landmarks, images, forms, links, focusable elements, small targets, duplicate IDs, iframes and videos.
- Highlights headings, landmarks, images, forms, links, focusable elements and small pointer targets on the current page.
- Records keyboard focus order while the reviewer tabs through the page.
- Exports a manual review session JSON file.
- Exports a structured `open-issues.yml` fragment that can be merged into `.a11y/open-issues.yml`.
- Copies a local Codex prompt for the next remediation step.

## It does not replace expert testing

The helper is not an accessibility scanner and does not prove WCAG conformance. It captures structured human evidence. Use it for manual-only or partly manual criteria such as:

- meaningful alternative text,
- keyboard operability and focus order,
- media captions/audio description quality,
- hover/focus behaviour,
- semantic quality of headings/labels,
- cognitive/login/process checks,
- legal exceptions for the accessibility statement.

## Exported files

The side panel downloads to suggested paths like:

```text
.a11y/manual-review/2026-07-05-example-page.json
.a11y/manual-review/2026-07-05-example-page-open-issues.yml
```

Merge confirmed failures into:

```text
.a11y/open-issues.yml
```

The accessibility statement must be generated from `.a11y/open-issues.yml`, not free-written from memory.

## Security

Use this helper on local, DDEV or staging sites where possible. For TYPO3 backend/login tests, use a dedicated test account and avoid real personal/customer data.
