# 7. Testing & Tools / WCAG 2.2 Audit Workflow

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 7.1 Agent-First WCAG 2.2 Audit Protocol

When a user asks for a WCAG 2.2 conformance audit, start the audit. Do not stop after saying that automation is incomplete.

### What the agent must do first

1. Scope the audit:
   - URLs, language variants, templates, forms, menus, dialogs, media, downloads, and third-party embeds.
   - Viewports to test. Use at least desktop and one narrow/mobile viewport for user-facing pages.
   - Target standard: WCAG 2.2 A/AA unless the user specifies another level.
2. Run automated browser checks with `axe-core` and WCAG tags.
3. Run deterministic DOM checks:
   - `<html lang>` matches the rendered language.
   - Exactly one main `<h1>`.
   - Heading levels do not skip.
   - `<main>`, `<header>`, and `<footer>` exist.
   - Skip link exists and points to the main content.
   - Images have `alt`; informative images have meaningful alt; decorative images have empty alt.
   - Images have width/height or otherwise avoid CLS.
   - `user-scalable=no` is absent.
   - Footer/header navigation links are present and localized.
4. Review all automated `violations` and `incomplete` results:
   - Fix clear defects in templates, CSS, JS, TCA, or content.
   - For color-contrast `incomplete`, use the script's computed foreground/background review where available, then manually inspect only unresolved cases. Do not count it as passed without evidence.
   - For target-size findings, check the 24x24 CSS px minimum and spacing exceptions.
5. Run a real browser keyboard probe:
   - Tab through the page.
   - Record focus order, missing focus indicators, trapped focus, and hidden/offscreen focused elements.
   - Fix obvious component issues immediately.
6. Produce a report:
   - Commands run, tool versions, URLs, viewport, and timestamp.
   - Pass/fail/incomplete findings per URL.
   - Code/content changes made.
   - Residual risks.
   - A short "Human/user follow-up only" list.

### What must remain human/user follow-up

Keep this list short and specific. Only include items the agent cannot honestly complete:

- Screen reader confirmation with the user's supported assistive technology and browser combinations, e.g. VoiceOver/Safari, NVDA/Firefox, JAWS/Chrome.
- Real-device touch testing where target-size exceptions depend on actual device input, spacing, or user behavior.
- Legal approval of the accessibility statement, organization identity, enforcement body, dates, and jurisdiction-specific wording.
- Captions/transcripts quality review for audio/video content.
- Accessibility review of PDFs, office documents, downloads, third-party widgets, maps, iframes, and embedded services the agent cannot inspect or control.
- User testing with disabled users when the requested conformance claim requires it.

## 7.2 Reusable Audit Script

Use `scripts/wcag22_audit.cjs` for rendered-page checks. It launches Chrome through Playwright, injects axe-core, runs WCAG 2.0/2.1/2.2 A/AA tags, performs structural checks, reviews resolvable color-contrast `incomplete` nodes, and runs a basic real-Tab keyboard probe.

Install temporary dependencies in the audited project when needed:

```bash
npm install --no-save playwright axe-core
```

Run against one or more DDEV URLs:

```bash
node /path/to/skills/typo3-accessibility/scripts/wcag22_audit.cjs \
  --url https://example.ddev.site/accessibility/ \
  --url https://example.ddev.site/de/barrierefreiheit/ \
  --out var/transient/wcag22-audit.json \
  --markdown var/transient/wcag22-audit.md
```

Interpretation:

- Exit `0`: no automated axe violations. Still review `incomplete`, script warnings, and human follow-up.
- Exit `2`: axe found violations. Fix or document each one.
- `incomplete` is evidence to review, not evidence to pass. `color-contrast` incomplete items include computed contrast evidence where Chromium exposes parsable foreground/background colors.
- The script separates likely inline-text target-size exceptions from unresolved small target candidates; inspect any remaining candidates before escalating them to the user.

## 7.3 Tools

### Automated Testing

| Tool | Use |
|------|-----|
| `axe-core` / `axe DevTools` | Automated WCAG checks; use tags for WCAG 2.2 A/AA where available |
| `pa11y` | CLI accessibility testing for CI/CD |
| `Lighthouse` | Chrome DevTools audit (Accessibility score) |
| `WAVE` | Browser extension for visual feedback |

### Manual Testing Checklist

1. **Keyboard only**: Navigate entire page using Tab, Shift+Tab, Enter, Escape, Arrow keys
2. **Screen reader**: Test with VoiceOver (macOS), NVDA/JAWS (Windows)
3. **Zoom**: Verify layout at 200% and 400% zoom
4. **Color**: Use browser dev tools to simulate color blindness
5. **Reduced motion**: Enable `prefers-reduced-motion: reduce` in OS settings

### Pa11y CI Integration

```bash
# Run against local DDEV instance
npx pa11y https://mysite.ddev.site --standard WCAG2AA --reporter cli
```

```json
// .pa11yci.json
{
    "defaults": {
        "standard": "WCAG2AA",
        "timeout": 30000,
        "wait": 2000
    },
    "urls": [
        "https://mysite.ddev.site/",
        "https://mysite.ddev.site/contact",
        "https://mysite.ddev.site/news"
    ]
}
```
