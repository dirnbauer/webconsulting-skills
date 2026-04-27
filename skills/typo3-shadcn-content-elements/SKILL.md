---
name: typo3-shadcn-content-elements
description: Produce, audit, or overhaul TYPO3 Content Blocks content elements styled with shadcn/ui presets. Use this skill whenever the user asks to create, update, review, seed, restyle, iconize, or add backend previews for TYPO3 content elements, especially in EXT:desiderio, Fluid templates, ContentBlocks/ContentElements, shadcn/create preset ids, Tailwind v4 tokens, light/dark mode token behavior, no-hardcoded-style audits, Fluid atoms/molecules, TYPO3 layout module previews, or content element seed scripts.
compatibility: TYPO3 14.x
metadata:
  version: "1.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 shadcn Content Elements

> Source: https://github.com/dirnbauer/webconsulting-skills

## Purpose

Use this skill to build TYPO3 Content Blocks content elements that behave like a coherent shadcn/ui system: preset-driven tokens, shared Fluid atoms/molecules, complete field coverage, useful backend previews, semantic icons, and seed data that fills every editor field.

This skill assumes Content Blocks are the source of truth for schema and TYPO3 owns rendering. shadcn/ui is the source for theme tokens, component class contracts, data attributes, states, spacing, borders, radius, and typography.

The styling rule is strict: content elements should not hardcode colors or theme-specific visual values. Raw `oklch()`, `hsl()`, `rgb()`, hex colors, and fixed light/dark assumptions belong in the committed shadcn theme token source only. Templates, element CSS, backend preview CSS, generated icons, and chart scripts should consume semantic tokens or Tailwind/shadcn utility classes.

## Default Workflow

1. **Establish the preset source.**
   - If a shadcn/create URL or preset id is given, extract the id, for example `b4hb38Fyj`.
   - Use a scratch app to inspect shadcn output; do not install React components as TYPO3 runtime code.
   - Commit the preset as local CSS variables and Site Settings, for example `body[data-shadcn-preset="b4hb38Fyj"]`; do not add a runtime preset downloader or binary switcher.
   - Treat `:root` as the light-mode base and `.dark` as the dark-mode override, matching shadcn. Do not write content elements that only look correct in one mode.
   - Read `references/shadcn-preset-workflow.md` before changing theme tokens or primitive class strings.

2. **Audit before editing.**
   - Run `php <skill>/scripts/audit-content-elements.php <repo-root>` when working on a repo with `ContentBlocks/ContentElements`.
   - Use the output to prioritize missing previews, undeclared rendered fields, unused configured fields, missing labels, missing icons, and repeatable-field gaps.
   - Treat the audit as a starting point, then manually inspect high-risk templates.
   - Apply the Fluid safety checks from `references/content-element-contract.md`, especially for date/time formatting, `typolink` attributes, resource paths, and string-only ViewHelpers.

3. **Fix the shared component layer first.**
   - Update `Resources/Private/Components` atoms/molecules from generated shadcn class contracts before editing hundreds of individual templates.
   - Prefer shared Fluid components over bespoke content-element CSS.
   - Keep semantic shadcn tokens such as `bg-background`, `text-foreground`, `bg-card`, `border-border`, `ring-ring`, `text-muted-foreground`, `bg-primary`, and `text-primary-foreground`.
   - Read `references/styling-token-contract.md` before adding or changing element CSS, SVG icon colors, chart colors, shadows, overlays, or backend preview styling.

4. **Audit each content element against its contract.**
   - Read `references/content-element-contract.md`.
   - For every element, compare `config.yaml`, `templates/frontend.html`, `language/labels.xlf`, `assets/icon.svg`, CSS/JS assets, backend preview, and seed coverage.
   - Treat `config.yaml:title` as an editor-facing product name. Prefer names like `Text & Media`, `Image Call to Action`, and `Logo Cloud Hero` over raw slugs such as `textmedia`, `CTA With Image`, or `Hero Logo Cloud`.
   - Every configured editor field should be rendered or intentionally marked backend-only.
   - Every rendered field should exist in `config.yaml`.
   - Every Collection child field should be rendered or intentionally omitted.
   - File fields need alt text and copyright/source strategy in seed data and previews.
   - Date and time fields must be formatted to strings before they are passed to visual-editor text rendering or HTML attributes.

5. **Add backend previews for the page/layout module.**
   - Read `references/backend-preview-pattern.md`.
   - Add `templates/backend-preview.fluid.html` using Content Blocks `Preview` layout with `Header`, `Content`, and optionally `Footer`.
   - Show the most important data: title/headline, summary, bullets/repeatables, CTA/link, chart metrics, and thumbnails.
   - Never rely on TYPO3’s Core fallback preview for custom Content Blocks.

6. **Create or refresh icons.**
   - Read `references/icon-pattern.md`.
   - Each element gets a semantic `assets/icon.svg`.
   - Use TYPO3-style 16x16 SVGs: transparent background, `currentColor` primary, `var(--icon-color-accent,currentColor)` accent, readable in light and dark.

7. **Update seed scripts.**
   - Fill all top-level and repeatable fields for every element.
   - Add real dummy images from Unsplash or committed demo assets, with alt text and copyright/source fields where available.
   - Seed chart/data elements with valid JSON that the frontend template actually parses.

8. **Verify and commit in reviewable slices.**
   - Run CSS build, PHP unit/static checks, and Content Blocks/TYPO3 cache validation.
   - Scan content elements and shared generated preview code for raw color literals; allowed raw preset values should be confined to the shadcn theme token file and generated Tailwind output.
   - For large overhauls, commit by layer: preset/theme, primitives, generated previews, icons, per-element fixes, seed data.
   - Browser-check frontend pages and TYPO3 backend layout module previews.

## Quality Bar

- Preset changes must visibly change design through committed tokens and shared component classes.
- Content elements should look like shadcn/ui, not generic Bootstrap or one-off CSS.
- Content elements must be light/dark capable because they consume semantic tokens rather than fixed color values.
- Backend previews should help editors recognize content without opening the form.
- Icons should form a coherent family, not random drawings.
- Generated or bulk changes need deterministic scripts and tests where possible.

## References

- `references/shadcn-preset-workflow.md`: scratch-app preset workflow and token expectations.
- `references/styling-token-contract.md`: no-hardcoded-style rules, light/dark behavior, and verification scans.
- `references/content-element-contract.md`: field/template/label/seed audit contract.
- `references/backend-preview-pattern.md`: Content Blocks backend preview pattern.
- `references/icon-pattern.md`: TYPO3 backend icon rules.

## Scripts

- `scripts/audit-content-elements.php <repo-root>`: JSON audit for Content Blocks directories.
