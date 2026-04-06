# TYPO3 Icon Design Notes

## Accent Placement Strategy

Choose ONE of these accent strategies per icon:

1. **Background layer** — A secondary shape behind the main icon in accent color (like module-web's second document)
2. **Inner detail** — A small detail inside the main shape (for example the smaller gear detail in `module-config`)
3. **Border/outline** — The outer ring or border (like module-site's circle)

Do NOT use accent for the entire primary shape — that looks like the old solid style.

## @typo3/icons NPM Package

The official icon set is published as `@typo3/icons` on npm. Extensions should NOT copy core
icons but may reference them by identifier. Custom extension icons follow the same design
language but are unique to the extension.

Browse available icons: https://typo3.github.io/TYPO3.Icons/
Module icons: https://typo3.github.io/TYPO3.Icons/icons/module.html

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `fill="#ff8700"` directly | Use `var(--icon-color-accent, #ff8700)` for theme support |
| Using `fill="white"` or `fill="#fff"` | Replace with `currentColor` — hardcoded white is invisible in light mode |
| Using `fill="black"` or `fill="#333"` | Replace with `currentColor` — hardcoded dark is invisible in dark mode |
| Using `<rect fill="..."/>` as background | Remove entirely — icons must be transparent |
| Using `prefers-color-scheme` in SVG | Don't — TYPO3 uses `data-color-scheme`, not media queries |
| Keeping `xmlns:xlink` | Remove — not needed for modern SVG |
| Registering in `ext_localconf.php` | Move to `Configuration/Icons.php` |
| Calling `registerIcon()` from `ext_localconf.php` / bootstrap | Use the declarative array in `Configuration/Icons.php` instead — the **`registerIcon()` method is not deprecated**; imperative registration during bootstrap files is. |
| Forgetting to clear browser cache | Icons are cached in browser localStorage |
| Using 32×32 viewBox for parent module | Always use 64×64 for consistency |
| Assuming accent is always orange | Fresh theme uses purple (`#bf9aff`/`#b68cff`) in sidebar |
| Using inline `style` for colors | Use `fill` attribute with CSS variables — inline styles override the cascade |
| **Using `.4` fill opacity for module icons** | Use **`.8`** for depth fill in module/sidebar icons — `.4` renders too faint on the Fresh theme's dark purple sidebar. Validated in real TYPO3 v14 backend. |
| **Thin ring outlines (4px or less)** | **Use ≥ 6px ring width** — a 4-unit gap in a 64-unit viewBox scales to ~2px at the 32px MEDIUM render size. Invisible against a dark background. |
| **Tiny accent elements** | **Minimum 12 units** in smallest dimension for 64×64 module icons — small accents become unrecognizable dots at 32px render size. |

## Contrast in TYPO3 v14 Backend Sidebar

The TYPO3 Fresh theme sidebar has a **dark purple/navy background** (~`#1a1625` or similar). Module icons render at **32px (MEDIUM size)** in this sidebar. Two issues cause low-contrast icons in this context:

### Issue 1: Opacity too low

`opacity=".4"` on `currentColor` fill in a dark sidebar:
- `currentColor` resolves to a light/white color (sidebar text color)
- 40% white on dark purple = very faint, barely visible fill
- **Fix: use `.8`** for depth fill in module/sidebar icons (validated against real TYPO3 v14 backend)

### Issue 2: Ring too thin

A 4-unit outline ring in a 64-unit viewBox:
- Scales to exactly 2px at 32px render size
- 2px on a dark background is hard to see, especially with anti-aliasing
- **Fix: use ≥ 6-unit ring width** (outer y=6, inner y=12 minimum for top of shield/document shapes)

### The Math

```
Ring width in px at render size = (ring units / viewBox units) × render px
4 units at 32px render = (4 / 64) × 32 = 2px  ← too thin
6 units at 32px render = (6 / 64) × 32 = 3px  ← minimum readable
8 units at 32px render = (8 / 64) × 32 = 4px  ← comfortable
```
