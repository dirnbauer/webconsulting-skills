# Styling Token Contract

Use this reference before creating or modifying content-element templates, element CSS,
backend-preview CSS, generated icons, chart scripts, or normalization scripts.

## Core Rule

Content elements consume the shadcn design system; they do not define their own theme.

- Put raw preset values only in the committed shadcn theme token source, such as
  `Resources/Public/Css/shadcn-theme.css`.
- Treat `:root` as the light-mode base token set and `.dark` as the override token set.
- Write Fluid templates, CSS, SVG, and JavaScript so switching the shadcn preset or toggling
  `.dark` changes the result through tokens.
- Generated Tailwind CSS may contain compiled values because it is build output. Do not
  manually edit generated output to fix source-level styling mistakes.

## Allowed In Content Elements

Prefer Tailwind/shadcn utility classes and semantic CSS variables:

- Surfaces: `bg-background`, `bg-card`, `bg-popover`, `bg-muted`, `bg-accent`
- Text: `text-foreground`, `text-card-foreground`, `text-muted-foreground`,
  `text-primary-foreground`
- Controls: `bg-primary`, `text-primary-foreground`, `border-border`, `border-input`,
  `ring-ring`
- Charts: `var(--chart-1)` through `var(--chart-5)`
- TYPO3 preview UI: TYPO3 component variables first, then shadcn tokens as fallback
- Icons: `currentColor` and `var(--icon-color-accent,currentColor)`
- Overlays: `color-mix()` with semantic tokens, for example
  `color-mix(in oklch, var(--foreground) 60%, transparent)`

## Avoid In Content Elements

Do not add these to `ContentBlocks/ContentElements`, shared component CSS, preview CSS,
icons, or generator templates:

- Hex colors such as `#fff`, `#000`, `#ff8700`
- Raw `rgb()`, `rgba()`, `hsl()`, `hsla()`, or `oklch()` color literals
- Fixed dark-only overlays such as `rgba(0,0,0,.7)`
- Fixed white text for image/nav overlays when a semantic foreground token can express it
- Shadow fallbacks with raw RGB values when `--shadow-*` or `--d-shadow-*` exists

The practical exception is migration tooling that maps known legacy literals to tokens.
Keep those mappings isolated and do not copy the legacy literals into live templates.

## Verification

Run a literal scan after styling changes:

```bash
rg -n "#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|hsl\(|oklch\(" \
  ContentBlocks/ContentElements \
  Resources/Public/Css/content-preview.css \
  Resources/Public/Css/components.css \
  Resources/Public/Css/desiderio.css \
  Build/Scripts/normalize-content-elements.php \
  -g '*.css' -g '*.html' -g '*.js' -g '*.svg' -g '*.php'
```

Expected source-level findings:

- HTML entities such as arrows or checkmarks are fine.
- shadcn token files may contain raw `oklch()` preset values.
- generated Tailwind output may contain compiled values.
- migration maps may contain legacy literals only as search keys.

Any live content-element color literal should be replaced with a semantic token or
Tailwind/shadcn utility.
