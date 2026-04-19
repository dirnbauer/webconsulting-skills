# TYPO3 v14 Icon Design Notes

## Core visual rules

- No background rectangle or full-canvas fill.
- Use `currentColor` for the primary geometry.
- Use `var(--icon-color-accent, #ff8700)` for accent geometry.
- Keep SVG markup minimal.
- Preserve the icon's meaning even when the drawing changes.

## Light and dark mode

TYPO3 v14 backend supports auto / light / dark color schemes. The same SVG must work
in both. The TYPO3.Icons package defines the tokens on `:root` as:

```css
--icon-color-primary: currentColor;
--icon-color-accent: #ff8700;
```

Guidance:

- `currentColor` inherits the surrounding text color, so the silhouette flips with
  the scheme automatically — this is why you must never hardcode black or white.
- `#ff8700` (TYPO3 orange) stays the same in both schemes. Orange has sufficient
  contrast against the light and dark backend surfaces. Do not introduce a second
  scheme-specific accent hex; theme authors override the CSS variable if they want
  a different color.
- Opacity-based depth layered on top of `currentColor` is safe.
- Do not rely on `prefers-color-scheme` media queries inside the SVG; the Core
  drives the scheme via an attribute on the root element, and manual switches from
  User Settings would be missed.

## Match the Core icon family

Pick references from the Core family that matches the job:

| Situation | Prefer this family |
|-----------|--------------------|
| Backend module navigation | `module` |
| Inline action or toolbar control | `actions` |
| Content/plugin metaphor | `content`, `default`, `apps` |
| Record or TCA metaphor | `default`, `apps`, `mimetypes`, `overlay`, `status` |

Custom extension icons should feel native to TYPO3 v14, but they should still represent the
extension's own concepts. Do not copy a Core icon verbatim unless the extension is intentionally
reusing the exact same meaning.

## Module icon rules

Module icons render large in source SVG terms but small in the backend menu. Keep them simple:

- `viewBox="0 0 64 64"`
- strong silhouette
- minimum 6-unit outline width when using outlined shapes
- `.8` opacity for depth fills when needed
- one clear accent strategy, not several competing accents

Accent strategies that work well:

1. background companion shape
2. inner detail
3. outer ring or border

## Small icon rules

Plugin, record, and action icons usually render at 16px.

- Keep the `viewBox` consistent with the Core icon family you are matching.
- Remove tiny decorative details.
- Prefer one primary metaphor plus one accent at most.
- Avoid module-style multi-layer compositions in 16x16 icons.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `fill="#fff"` or `fill="white"` | Replace with `currentColor` (vanishes in light mode) |
| `fill="#000"` or `fill="#333"` | Replace with `currentColor` (vanishes in dark mode) |
| Solid colored background block | Remove it completely (breaks both schemes) |
| Hardcoded accent hex everywhere | Use `var(--icon-color-accent, #ff8700)` |
| Scheme-specific accent hex via `prefers-color-scheme` | Keep a single accent; Core switches schemes programmatically |
| Registering icons in `ext_localconf.php` | Move to `Configuration/Icons.php` |
| Treating every icon like a module icon | Respect the icon type and render size |
| Too many details in 16x16 icons | Simplify until the icon is still readable at 16px |
