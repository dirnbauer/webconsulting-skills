---
name: "typo3-icon14"
description: "Designs and migrates TYPO3 extension icons to the v14 line-art style, including source SVG cleanup, light/dark behavior, IconRegistry naming, backend module icons, and verification. Use when the user asks for TYPO3 v14 icons, backend module icon migration, extension icon modernization, SVG icon rules, or icon registration."
compatibility: "TYPO3 14.x"
metadata:
  version: "1.4.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 v14 Icon Modernizer

> Source: https://github.com/dirnbauer/webconsulting-skills

> Prefer live TYPO3 v14 references over bundled snapshots. Use the official Icon API
> docs for registration rules and the TYPO3.Icons catalog for the current Core SVG
> language. Use the local reference files only to keep this skill concise.

## What this skill is for

Use this skill to:

- migrate legacy extension icons to TYPO3 v14
- design new custom icons that fit the TYPO3 v14 backend
- update `Configuration/Icons.php` and all icon consumers
- keep module, plugin, record, action, and extension icons distinct

Do not invent a second icon system for the extension. Work with the icon identifiers,
file names, and render contexts that already exist in the codebase.

## Workflow

1. Inventory existing icon files and registrations.
2. Classify each icon by type and render context.
3. Infer the icon meaning from module names, TCA, plugin config, and current SVGs.
4. If the meaning is still unclear, ask one focused question: what should this icon
   communicate?
5. Load live TYPO3 v14 references for the matching icon family. See
   [references/live-sources.md](references/live-sources.md).
6. *(Optional)* Generate a raster **reference** with an image model (GPT Image 2 or
   Gemini) when a metaphor is non-obvious or you want to explore a family look. The
   raster is a guide only — see
   [references/image-reference-pipeline.md](references/image-reference-pipeline.md).
7. Redraw or modernize the SVG in the correct TYPO3 v14 style (author by hand to
   spec — never ship the raster or a naive auto-trace).
8. Run `scripts/verify-icon.sh <file> <type>` — it must print `RESULT: PASS`.
9. Update `Configuration/Icons.php` and every `iconIdentifier` / `pluginIcon` /
   `typeicon_classes` consumer.
10. Verify the icon in its real backend context (both light and dark) and clear
    TYPO3 cache plus browser local storage if the old SVG still appears.

## Start With Meaning, Not Shapes

When the user asks for new icons, first capture or infer:

- which identifiers or files need to exist
- what each icon represents
- whether several icons should form a visual family
- whether one icon is the parent and others are sub-variants

If the repository already makes the meaning obvious, proceed without stopping. If not,
ask for a short mapping such as:

- `module-myext` -> "main module for editorial planning"
- `record-myext-campaign` -> "campaign record"
- `plugin-myext-list` -> "frontend list plugin"

The user can describe usage, not geometry. Translate usage into icon semantics.

## Optional: Image-Model Reference Stage

You can use an image model — **OpenAI GPT Image 2** or **Google Gemini ("Nano
Banana")** — to *ideate* an icon, then **redraw the result as a clean v14 SVG**.
The raster is a design reference, never the shipped asset: TYPO3 backend icons are
monochrome line-art (`currentColor`, transparent, dark-mode-safe), and shipping a
raster or a naive auto-trace produces fuzzy, scheme-breaking junk. This stage is
optional — for simple glyphs, authoring the SVG directly is faster and cleaner.

```bash
# 1. Generate a reference (auto-selects the model from whichever key is present:
#    OPENAI_API_KEY -> GPT Image 2, else GEMINI_API_KEY/GOOGLE_API_KEY -> Gemini)
scripts/generate-icon-reference.sh "agent streaming events into a UI bubble" \
    /tmp/module-agui.ref.png --accent "one spark mark, top-right" \
    --family "centered glyph, 8px padding on a 64 grid, 4px stroke"

# 2. Redraw it by hand as a conformant v14 SVG, then gate it:
scripts/verify-icon.sh packages/agui_integration/Resources/Public/Icons/module-agui.svg module
```

Key facts (verified mid-2026; re-check live docs):

- **`gpt-image-2`** is the current OpenAI image model but does **not** support
  transparent backgrounds — prompt it for a flat white background and drop it in the
  redraw. Use `--transparent` (→ `gpt-image-1-mini`) only when you truly need an alpha
  raster. GPT-image returns base64 at `data[0].b64_json`; the org may need API
  verification.
- **Gemini** returns base64 at `candidates[0].content.parts[].inlineData.data`, has
  no transparent option, and watermarks with SynthID.

No key? Skip this stage and author the SVG directly — the result is just as good for
line-art icons. Full details and the prompt template:
[references/image-reference-pipeline.md](references/image-reference-pipeline.md).

## Source Of Truth

Use sources in this order:

1. Official TYPO3 Icon API docs for registration, providers, and migration:
   [Icon API](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Icon/Index.html)
2. Live TYPO3.Icons catalog for current Core SVG references:
   [TYPO3.Icons](https://typo3.github.io/TYPO3.Icons/)
3. If the working TYPO3 instance has `EXT:styleguide`, inspect the real backend rendering
   there as a runtime check
4. Only fall back to local reference notes in this skill when live sources are unavailable

Prefer loading the current Core icons when needed. Do not ship copies of Core icons into
an extension unless the user explicitly wants vendored assets or the environment is offline.

## Respect The Icon Type

| Type | Typical file | Render context | ViewBox | Where to look for references |
|------|--------------|----------------|---------|-------------------------------|
| Parent / submodule | `module-*.svg` | Backend navigation, module menu | `0 0 64 64` | `module` catalog |
| Extension icon | `Extension.svg` | Extension Manager and related backend views | `0 0 64 64` | `module` catalog |
| Plugin icon | `plugin-*.svg` | New content element wizard, list view, plugin selectors | usually `0 0 16 16` | `content`, `default`, `apps` |
| Record icon | `record-*.svg` | TCA, page tree, list module | usually `0 0 16 16` | `default`, `apps`, `mimetypes`, `overlay`, `status` |
| Action icon | `actions-*.svg` | Buttons, toolbars, controls | usually `0 0 16 16` | `actions` |

Always match the render size and visual density of the icon type you are editing. Do not
force a 64x64 module composition into a 16x16 record or action icon.

## Minimal TYPO3 v14 SVG Rules

- transparent background only
- primary geometry uses `currentColor`
- accent geometry uses `var(--icon-color-accent, #ff8700)`
- remove hardcoded white, black, gray, and legacy brand-color backgrounds
- keep markup minimal: `xmlns` plus `viewBox` only unless a provider truly needs more
- preserve the semantic shape from the existing icon whenever possible
- for `module-*` and `Extension.svg`: prefer strong silhouettes, a 4px stroke on the
  64x64 canvas (renders 2px at 32x32), and `.4` opacity for depth fills when needed
- for 16x16 icons: reduce details aggressively; two clear ideas beat five tiny ones

See [references/design-notes.md](references/design-notes.md) for the visual rules and
anti-patterns.

## Light And Dark Mode Are Non-Negotiable

TYPO3 v14 ships auto / light / dark color scheme switching in the backend (introduced
as a Core feature in v13.3, carried into v14). Every custom icon must render correctly
in **both** schemes. There is no separate "dark icon" file — the same SVG is used.

The two CSS tokens that the Core ships on `:root` (from `TYPO3.Icons/assets/scss/icons.scss`)
are:

```css
:root {
    --icon-color-primary: currentColor;
    --icon-color-accent: #ff8700;
}
```

How to stay compatible with both schemes:

- Use `currentColor` (or `var(--icon-color-primary, currentColor)`) for the primary
  silhouette. It inherits the surrounding text color, which flips automatically when
  the user switches color scheme.
- Use `var(--icon-color-accent, #ff8700)` for the accent. TYPO3 orange `#ff8700` is the
  same fallback in both schemes because orange has sufficient contrast on both light
  and dark backend surfaces. Do **not** replace it with a scheme-specific hex — themes
  that want a different accent override the CSS variable, not the fallback.
- Never hardcode `fill="#000"`, `fill="#333"`, `fill="#fff"`, `fill="white"`, or
  `fill="black"`. Any one of these vanishes on one of the two backgrounds.
- Never draw a solid background rectangle behind the icon. The backend surface color
  must show through so the scheme flip works.
- Opacity-based depth (`opacity=".4"` on top of `currentColor`) is safe because the
  base tone flips with the scheme.
- Do not depend on `prefers-color-scheme` media queries inside the SVG. The Core drives
  the scheme via an attribute on the root element, and relying on
  `prefers-color-scheme` will miss manual switches from the User Settings dropdown.

Verify every icon in both schemes before shipping (see Verification below).

## Registration Rules

Register icons in `Configuration/Icons.php`. TYPO3 v14 requires this and no longer allows
registration in `ext_localconf.php`.

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider;

return [
    'module-myext' => [
        'provider' => SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/module-myext.svg',
    ],
    'record-myext-item' => [
        'provider' => SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/record-myext-item.svg',
    ],
];
```

Update every consumer after the SVG is in place:

- `Configuration/Backend/Modules.php` -> `iconIdentifier`
- `Configuration/TCA/*.php` -> `typeicon_classes`, `iconIdentifier`
- `Configuration/TCA/Overrides/*.php` -> `pluginIcon`, page-type or folder icons

The official docs state that icons must be registered in the icon registry through
`Configuration/Icons.php`, and that registration in `ext_localconf.php` is no longer
possible in TYPO3 v14.

## Migration Behavior

When legacy SVGs already exist:

- keep the existing identifier unless a rename is required
- modernize the current shape before replacing it with a completely new metaphor
- keep file paths stable where possible to reduce config churn
- verify every updated icon against the icon type it belongs to

Use [references/migration-steps.md](references/migration-steps.md) for the checklist.

## Verification

Before finishing:

- run `scripts/verify-icon.sh <file> <type>` and confirm `RESULT: PASS` (it gates
  viewBox, embedded raster, scheme-breaking fills, missing `currentColor`,
  background rects, and `prefers-color-scheme`)
- verify the file path matches the registered source
- verify the icon type uses the correct viewBox
- verify there is no solid background layer
- verify all consumers point to the intended identifier
- verify the icon remains readable at its real render size
- verify the icon works in **both** light and dark backend schemes — switch via the
  user dropdown at the top right or User Settings, and check the icon in its real
  render context (module menu, content wizard, list module, TCA icons)
- confirm no hardcoded `#000`, `#333`, `#fff`, `white`, or `black` fills remain
- clear TYPO3 caches and browser local storage if rendering looks stale

## References

- [references/live-sources.md](references/live-sources.md): live TYPO3 v14 sources, catalog
  URLs, and fetch patterns
- [references/design-notes.md](references/design-notes.md): visual rules, icon-family
  guidance, and common mistakes
- [references/migration-steps.md](references/migration-steps.md): migration checklist
- [references/image-reference-pipeline.md](references/image-reference-pipeline.md):
  optional GPT Image 2 / Gemini reference stage, model facts, prompt template, gates
- `scripts/generate-icon-reference.sh`: dual-model reference generator (GPT Image 2 / Gemini)
- `scripts/verify-icon.sh`: hard conformance gate for authored icons

Source: https://github.com/dirnbauer/webconsulting-skills
