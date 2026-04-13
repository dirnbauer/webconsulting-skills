# TYPO3 v14 Live Icon Sources

Use these live sources first when you need the current TYPO3 v14 icon language.

## 1. Official Icon API docs

Source:
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Icon/Index.html

Use this for:

- `Configuration/Icons.php`
- allowed icon providers
- icon usage in PHP, Fluid, and JavaScript
- TYPO3 v14 migration rules away from `ext_localconf.php`

Key points from the docs:

- TYPO3 v14 requires custom icons to be registered in `Configuration/Icons.php`
- TYPO3 v14 no longer allows registering icons in `ext_localconf.php`
- TYPO3 Core icons can be browsed via the TYPO3.Icons catalog

## 2. TYPO3.Icons live catalog

Catalog root:
https://typo3.github.io/TYPO3.Icons/

Category pages:

- module: https://typo3.github.io/TYPO3.Icons/icons/module.html
- actions: https://typo3.github.io/TYPO3.Icons/icons/actions.html
- content: https://typo3.github.io/TYPO3.Icons/icons/content.html
- default: https://typo3.github.io/TYPO3.Icons/icons/default.html
- apps: https://typo3.github.io/TYPO3.Icons/icons/apps.html
- mimetypes: https://typo3.github.io/TYPO3.Icons/icons/mimetypes.html
- overlay: https://typo3.github.io/TYPO3.Icons/icons/overlay.html
- status: https://typo3.github.io/TYPO3.Icons/icons/status.html

Use the matching category for the icon type you are designing. For example:

- `module-*` and `Extension.svg` -> `module`
- `actions-*` -> `actions`
- `plugin-*` -> usually `content`, `default`, or `apps`
- `record-*` -> usually `default`, `apps`, `mimetypes`, `overlay`, or `status`

## 3. Individual icon URL patterns

Preview page:

```text
https://typo3.github.io/TYPO3.Icons/icons/{set}/{identifier}.html
```

Example:

```text
https://typo3.github.io/TYPO3.Icons/icons/module/module-styleguide.html
```

Direct SVG download:

```text
https://typo3.github.io/TYPO3.Icons/dist/svgs/{set}/{identifier}.svg
```

Example:

```text
https://typo3.github.io/TYPO3.Icons/dist/svgs/module/module-styleguide.svg
```

Prefer the live catalog page first because it shows identifier, preview, inline markup, and
download link together.

## 4. EXT:styleguide as runtime validation

If the working TYPO3 instance has `EXT:styleguide`, use it to validate how icons behave in the
real backend theme and color scheme.

Use `EXT:styleguide` for:

- checking module-icon readability in the backend navigation
- checking how `currentColor` and `--icon-color-accent` behave in context
- validating that an icon family feels like TYPO3 v14 rather than an isolated SVG

Do not depend on `EXT:styleguide` as the only source of truth. The primary source for current
Core icons is still TYPO3.Icons.

## 5. Local fallback

If the project already contains `@typo3/icons`, you can read the shipped SVGs directly from the
package instead of fetching them from the web.

Typical local package path:

```text
node_modules/@typo3/icons/dist/svgs/
```

Prefer this only when it already exists in the project or when network access is unavailable.
