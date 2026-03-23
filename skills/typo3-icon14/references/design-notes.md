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
