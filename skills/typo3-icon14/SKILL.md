---
name: typo3-icon14
description: >-
  Design and migrate TYPO3 v14 extension icons with the Core Icon API and the
  current backend icon language. Use when working with module icons, plugin
  icons, record icons, action icons, Extension.svg, Configuration/Icons.php,
  iconIdentifier, pluginIcon, typeicon_classes, TYPO3.Icons, or styleguide icon
  references.
compatibility: TYPO3 14.x
metadata:
  version: "1.2.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 v14 Icon Modernizer

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
6. Redraw or modernize the SVG in the correct TYPO3 v14 style.
7. Update `Configuration/Icons.php` and every `iconIdentifier` / `pluginIcon` /
   `typeicon_classes` consumer.
8. Verify the icon in its real backend context and clear TYPO3 cache plus browser
   local storage if the old SVG still appears.

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
- for `module-*` and `Extension.svg`: prefer strong silhouettes, minimum 6-unit outline
  width, and `.8` opacity for depth fills when needed
- for 16x16 icons: reduce details aggressively; two clear ideas beat five tiny ones

See [references/design-notes.md](references/design-notes.md) for the visual rules and
anti-patterns.

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

- verify the file path matches the registered source
- verify the icon type uses the correct viewBox
- verify there is no solid background layer
- verify all consumers point to the intended identifier
- verify the icon remains readable at its real render size
- clear TYPO3 caches and browser local storage if rendering looks stale

## References

- [references/live-sources.md](references/live-sources.md): live TYPO3 v14 sources, catalog
  URLs, and fetch patterns
- [references/design-notes.md](references/design-notes.md): visual rules, icon-family
  guidance, and common mistakes
- [references/migration-steps.md](references/migration-steps.md): migration checklist
