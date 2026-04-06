---
name: typo3-icon14
description: >-
  Migrate TYPO3 extension backend module icons from old solid-background style
  to TYPO3 v14 line-art style using currentColor, CSS custom properties, and the
  Icon API. Scans extensions for legacy icon SVGs, creates v14-conformant replacements,
  and updates Configuration/Icons.php registration. Use when working with icons, backend
  module icons, icon migration, icon update, module icon, TYPO3 v14 icons, icon redesign,
  SVG icons, icon registry, icon modernization.
compatibility: TYPO3 14.x
metadata:
  version: "1.1.1"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 v14 Icon Modernizer

> Migrate extension icons from the legacy solid-background style to the TYPO3 v14 line-art
> design language. Covers backend module icons, plugin icons, record icons, and the
> Extension icon.

## Quick Reference: Old vs New Style

| Aspect | Old Style (pre-v14) | New v14 Style |
|--------|---------------------|---------------|
| **Background** | Solid color rectangle (`<rect fill="#5BA34F"/>` or `<path fill="#5BA34F" d="M0,0h64v64H0V0z"/>`) | No background — transparent |
| **Primary shapes** | White `#FFFFFF` on colored bg | `currentColor` (adapts to theme) |
| **Accent color** | Hardcoded brand color (e.g. `#5BA34F`) | `var(--icon-color-accent, #ff8700)` |
| **Secondary elements** | `opacity="0.25"` / `0.75` with hardcoded fill | `opacity=".8"` with `currentColor` for module/sidebar icons; `opacity=".4"` for subtle content-area secondary layers |
| **ViewBox** | `0 0 64 64` (modules) or `0 0 32 32` (parent) | **Module / backend-module icons:** `0 0 64 64`. **Action, plugin, record, and similar small icons:** `0 0 16 16` — match the Core SVG you are replacing (do not mix module and plugin viewBoxes). |
| **SVG wrapper** | `version="1.1"`, `xmlns:xlink`, `enable-background`, generator comments | Minimal: `xmlns` + `viewBox` only |
| **Detail colors** | `#333333` for text lines, brand color for accents | `currentColor` + accent variable |

## Process

1. **Scan** — Find all icon files and registrations in the extension
2. **Classify** — Identify which icons use old style vs already v14-conformant
3. **Redesign** — Create new SVG icons following the v14 design language
4. **Register** — Ensure `Configuration/Icons.php` uses `SvgIconProvider`
5. **Verify** — Confirm module, plugin, and TCA references are correct
6. **Ask before saving** — Always present the plan and new SVGs to the user before writing files

## Step 1: Scan Extension for Icons

### File locations to check

| Location | Purpose |
|----------|---------|
| `Resources/Public/Icons/module-*.svg` | Backend module icons |
| `Resources/Public/Icons/plugin-*.svg` | Frontend plugin icons |
| `Resources/Public/Icons/record-*.svg` | Record type icons (TCA) |
| `Resources/Public/Icons/Extension.svg` | Extension icon (Extension Manager) |
| `Resources/Public/Icons/actions-*.svg` | Custom action icons |
| `Resources/Public/Icons/*.png` | Legacy bitmap icons (should migrate to SVG) |

### Configuration files to check

| File | What to look for |
|------|------------------|
| `Configuration/Icons.php` | Icon registration array — must exist for v14 |
| `Configuration/Backend/Modules.php` | `iconIdentifier` for each module |
| `Configuration/TCA/*.php` | `typeicon_classes`, `iconIdentifier` in ctrl/types |
| `Configuration/TCA/Overrides/*.php` | Plugin icons (`pluginIcon`), page type icons — do **not** instantiate `IconRegistry` here either; the deprecation covers bootstrap before `BootCompletedEvent` |
| `ext_localconf.php` | Do **not** bootstrap `IconRegistry` here in v14 ([Deprecation-104778](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104778-InstantiationOfIconRegistryInExtLocalconf.html)) — use `Configuration/Icons.php`. The `registerIcon()` **method** is not `@deprecated`; the anti-pattern is imperative registration during bootstrap files. |
| `ext_tables.php` | Should not contain icon registration |

### Default output paths (use these if user does not specify)

When generating or updating icons, save files to these standard TYPO3 extension paths.
All paths are relative to the extension root (e.g. `packages/my_extension/` or
`vendor/vendor/my-extension/`).

```
EXT:my_extension/
├── Configuration/
│   ├── Icons.php                          ← Icon registration (create if missing)
│   ├── Backend/
│   │   └── Modules.php                    ← Module iconIdentifier references
│   ├── TCA/
│   │   ├── tx_myext_domain_model_*.php    ← Record typeicon_classes
│   │   └── Overrides/
│   │       ├── tt_content.php             ← Plugin pluginIcon
│   │       ├── pages.php                  ← Page type icons
│   │       └── sys_category.php           ← Category type icons
│   └── Sets/                              ← (no icon files here)
├── Resources/
│   └── Public/
│       └── Icons/
│           ├── Extension.svg              ← Extension Manager icon (64×64 viewBox)
│           ├── module-{extkey}.svg        ← Parent module icon (64×64)
│           ├── module-{extkey}-*.svg      ← Submodule icons (64×64)
│           ├── plugin-{extkey}-*.svg      ← Plugin icons (16×16)
│           ├── record-{extkey}-*.svg      ← Record type icons (16×16)
│           ├── record-folder-contains-{extkey}.svg  ← Folder icon (16×16)
│           └── actions-*.svg              ← Custom action icons (16×16)
└── ext_localconf.php                      ← Do not add icon registration here; use Configuration/Icons.php
```

#### Concrete example: `t3g/blog` extension

Generated/updated files for the blog extension (`EXT:blog`):

```
vendor/t3g/blog/
├── Configuration/
│   ├── Icons.php                                  ← Updated (added declare strict_types)
│   └── Backend/
│       └── Modules.php                            ← Unchanged (already v14 format)
└── Resources/
    └── Public/
        └── Icons/
            ├── Extension.svg                      ← Updated (64×64 viewBox, currentColor)
            │
            │  Module icons (64×64 viewBox)
            ├── module-blog.svg                    ← Book with accent spine
            ├── module-blog-posts.svg              ← Document with folded corner
            ├── module-blog-comments.svg           ← Overlapping speech bubbles
            ├── module-blog-setup.svg              ← Dual gears (large + small accent)
            │
            │  Plugin icons (16×16 viewBox, each unique)
            ├── plugin-blog-archive.svg            ← Archive box with accent top
            ├── plugin-blog-authorposts.svg         ← Person silhouette + document
            ├── plugin-blog-authors.svg            ← Two people (accent for secondary)
            ├── plugin-blog-category.svg           ← Tag shape with accent dot
            ├── plugin-blog-commentform.svg         ← Speech bubble outline + accent lines
            ├── plugin-blog-comments.svg           ← Two bubbles (accent + currentColor)
            ├── plugin-blog-demandedposts.svg       ← Document with accent text lines
            ├── plugin-blog-footer.svg             ← Page with accent footer area
            ├── plugin-blog-header.svg             ← Page with accent header area
            ├── plugin-blog-posts.svg              ← Document with accent title bar
            ├── plugin-blog-relatedposts.svg        ← Two linked documents (accent behind)
            ├── plugin-blog-sidebar.svg            ← Page with accent sidebar
            ├── plugin-blog-tag.svg                ← Tag outline with accent dot
            │
            │  Record icons (16×16 viewBox)
            ├── record-blog-author.svg             ← Person with accent body
            ├── record-blog-category.svg           ← Tag with accent dot + rotated rect
            ├── record-blog-comment.svg            ← Speech bubble with accent title
            ├── record-blog-page.svg               ← Page with accent header
            ├── record-blog-page-root.svg          ← Globe with accent ring
            ├── record-blog-post.svg               ← Document with fold + accent lines
            ├── record-blog-tag.svg                ← Tag outline with accent circle
            ├── record-folder-contains-blog.svg    ← Folder with accent tab
            │
            │  Action icons (16×16, kept as-is)
            ├── actions-approve.svg                ← Uses class="icon-color" (already v14)
            └── actions-decline.svg                ← Uses class="icon-color" (already v14)
```

#### ViewBox sizes by icon type

| Icon Type | ViewBox | Typical Size Rendered |
|-----------|---------|----------------------|
| `module-*` | `0 0 64 64` | 48–64px (sidebar menu) |
| `plugin-*` | `0 0 16 16` | 16–32px (content wizard, list view) |
| `record-*` | `0 0 16 16` | 16px (page tree, list view, TCA) |
| `actions-*` | `0 0 16 16` | 16px (buttons, toolbars) |
| `Extension.svg` | `0 0 64 64` | 16–32px (Extension Manager) |

### Detection: Is an icon old-style?

An SVG is **old-style** if it matches ANY of these patterns:

```
Solid background rectangle:
  <rect ... fill="#RRGGBB" ... />  covering full viewBox
  <path fill="#RRGGBB" d="M0,0h64v64H0V0z"/>

Hardcoded white for primary shapes:
  fill="#FFFFFF" or fill="#fff" or fill="white"

Hardcoded dark for details:
  fill="#333333" or fill="#333" or fill="black"

Legacy SVG attributes:
  version="1.1"
  xmlns:xlink="..."
  enable-background="..."
  xml:space="preserve"

Generator comments:
  <!-- Generator: Adobe Illustrator ... -->
  <!-- Generator: Sketch ... -->
```

## Step 2: V14 Icon Design Language

### SVG Template

Every v14-style module icon follows this structure:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <!-- Depth/fill layer — .8 opacity for strong fill mass in dark sidebar -->
  <path fill="currentColor" opacity=".8" d="..."/>
  <!-- Primary shape outline — full opacity, ring width ≥ 6px for module icons -->
  <path fill="currentColor" d="..."/>
  <!-- Accent color elements (1–2 key elements, ≥ 12 units in smallest dimension) -->
  <path fill="var(--icon-color-accent, #ff8700)" d="..."/>
</svg>
```

### XML comments (optional)

Short comments above layers (depth, outline, accent) help maintainers; they are not required for rendering.

**XML 1.0 comment rule:** The text inside `<!-- … -->` must not contain the substring `--` (two consecutive hyphens). That forbids spelling a CSS custom property with its leading `--` inside a comment—for example, `<!-- … --icon-color-accent … -->` is invalid and may confuse editors or strict parsers.

**Recommended phrasing:** Describe the accent without echoing the `--` prefix—for example, `<!-- Accent: theme accent color (matches fill on next element) -->`—or omit the comment and rely on `fill="var(--icon-color-accent, #ff8700)"` on the element itself. If you name the token in prose, use `icon-color-accent` without a leading `--`.

### Design Rules

1. **No background** — The SVG has a transparent background. No rectangles or paths covering the full viewBox.

2. **`currentColor` for primary shapes** — Use `fill="currentColor"` **and** `stroke="currentColor"` where applicable; strip hardcoded `#…` fills/strokes and inline `style="fill:…"` on children so the icon tracks the theme.

3. **`var(--icon-color-accent, #ff8700)` for accent** — One or two key elements use the TYPO3 accent color CSS variable. The fallback `#ff8700` ensures visibility when the variable is not set. TYPO3 overrides this variable per theme and context (see Dark/Light Mode section below).

4. **`opacity=".8"` for depth fill** — Use 80% opacity for the interior fill layer of module/sidebar icons. This provides strong visible fill mass against the dark Fresh theme sidebar while still leaving a 20% contrast step against the full-opacity ring outline. Validated in real TYPO3 v14 backend. Do not use `.4` for module icons — it renders too faint on dark backgrounds. Reserve `.4` only for subtle decorative elements in content-area icons.

5. **64×64 viewBox** — Backend **module** icons use `viewBox="0 0 64 64"`. For other icon types, copy the viewBox from the Core icon you are visually matching.

6. **Clean SVG markup** — No `version`, no `xmlns:xlink`, no `enable-background`, no `xml:space`, no generator comments, no `id` attributes unless needed for sprites.

7. **Semantic shape preservation** — The icon's meaning (gear = settings, speech bubble = comments, document = posts) must be preserved. Only the rendering style changes.

8. **Line-art aesthetic** — Prefer outlined shapes with consistent stroke weight (simulated via path outlines) over solid fills. The new style feels lighter and more modern.

### Contrast Rules for Sidebar Icons

Module icons render at **32px (MEDIUM)** in the TYPO3 sidebar — half the 64-unit viewBox. Thin details that look fine at design size will disappear at render size. Apply these rules to all `module-*` and `Extension.svg` icons.

#### Ring / outline thickness

- Target a **minimum 6px ring width** for outlined shapes.
- Calculate as: `outer edge coordinate − inner cutout coordinate`. For a symmetric shape, both sides must be ≥ 6 units inset.
- A 4px ring (4 units in 64-unit viewBox) scales to 2px at 32px render — essentially invisible on a dark background.
- When building an outlined shape with two subpaths (outer minus inner cutout), if the outer top point is at y=6, the inner top point must be at y=12 or deeper (not y=10).

**Example — too thin (4px ring, avoid):**
```xml
<path fill="currentColor" d="M32 6 ...outer... Zm0 4 ...inner...Z"/>
<!--                                        ↑ only 4 units = ~2px at 32px render -->
```

**Example — correct (6px ring):**
```xml
<path fill="currentColor" d="M32 6 ...outer... Zm0 6 ...inner...Z"/>
<!--                                        ↑ 6 units = ~3px at 32px render, readable -->
```

#### Depth fill opacity

Use **`.8`** for module/sidebar icons. This was validated against the real TYPO3 v14 Fresh theme dark sidebar.

| Context | Opacity |
|---------|---------|
| Module icon depth fill (sidebar) | **`.8`** |
| Content-area icon secondary layer | `.4` |
| Plugin/record icon depth fill | `.8` |

#### Accent element minimum size

Accent shapes must be large enough to register at 32px:
- Minimum **12 units** in the smallest dimension for module icons (64×64 viewBox)
- Minimum **4 units** in the smallest dimension for plugin/record icons (16×16 viewBox)
- A tiny 4×4 accent shape in a 64-unit viewBox scales to 2×2px — indistinguishable from a rendering artifact

#### Contrast self-check before saving

Mentally render your icon at half size (32px for module icons, 8px for 16×16 icons). Ask:
- [ ] Is the primary outline still a readable, distinct shape?
- [ ] Is the depth fill visible as a separate layer (not invisible)?
- [ ] Is the accent element recognizable, not just a smudge?

If any answer is no → increase ring width, raise opacity, or enlarge the accent shape.

### Dark/Light Mode Support

TYPO3 v14 supports both dark and light color schemes. Icons MUST render correctly in both
modes. The TYPO3 **backend** documents theme via **`data-color-scheme`** and **`data-theme`** on the HTML element. The **`data-bs-theme`** attribute is not part of normal backend HTML output (it may appear in the **styleguide** extension’s frontend demos). Prefer inspecting real backend markup, not generic Bootstrap documentation. Color mode is
not controlled via `prefers-color-scheme` media queries in the backend UI.

#### How `currentColor` Adapts

`currentColor` inherits the CSS `color` property of the parent element:

| Context | Dark Mode | Light Mode |
|---------|-----------|------------|
| **Sidebar** (`.scaffold-sidebar`) | White/light text → icon is light | Dark text → icon is dark |
| **Content area** | Light text on dark bg → icon is light | Dark text on light bg → icon is dark |
| **Toolbar** | Adapts to toolbar text color | Adapts to toolbar text color |
| **List module** | Row text color | Row text color |

No extra CSS is needed — `currentColor` handles everything automatically.

#### How `--icon-color-accent` Cascades

The accent color follows a multi-level cascade with `light-dark()` CSS functions:

```
SVG: fill="var(--icon-color-accent, #ff8700)"
  ↓
CSS: --icon-color-accent: var(--typo3-icons-accent)
  ↓
Theme-specific values:
  Default:  light-dark(var(--token-color-primary-60), var(--token-color-primary-40))
  Classic:  #ff8700 (orange, same in both modes)
  Fresh sidebar: light-dark(#bf9aff, #b68cff) (purple!)
```

The `light-dark()` CSS function resolves based on the element's `color-scheme`:
- First value = light mode
- Second value = dark mode

**Result:** Icons automatically get the correct accent color for the active theme AND
color scheme without any SVG changes.

#### Theme-Specific Accent Colors

| Theme | Context | Light Mode | Dark Mode |
|-------|---------|------------|-----------|
| **Default** | Everywhere | `--token-color-primary-60` | `--token-color-primary-40` |
| **Classic** | Everywhere | `#ff8700` (orange) | `#ff8700` (orange) |
| **Fresh** | Sidebar | `#bf9aff` (purple) | `#b68cff` (purple) |
| **Fresh** | Content | Primary token colors | Primary token colors |

#### Icon Variant Colors

TYPO3 provides additional icon color overrides via `--icon-color-primary`:

| Variant | CSS Variable |
|---------|-------------|
| Default | `currentColor` |
| Danger | `var(--typo3-text-color-danger)` |
| Success | `var(--typo3-text-color-success)` |
| Warning | `var(--typo3-text-color-warning)` |
| Info | `var(--typo3-text-color-info)` |
| Notice | `var(--typo3-text-color-notice)` |

These are applied by TYPO3 when rendering icons with a state or overlay — extension icons
do not need to handle these. Just use `currentColor` and let TYPO3 manage overrides.

#### Dark/Light Mode Design Checklist

- [ ] **NEVER hardcode colors** — No `#fff`, `#000`, `#333`, or any hex color in SVG
- [ ] **Use only `currentColor`** for primary/secondary shapes
- [ ] **Use only `var(--icon-color-accent, #ff8700)`** for accent elements
- [ ] **Depth fill opacity `.8` for module/sidebar icons** — validated against TYPO3 v14 Fresh theme dark sidebar; `.4` renders too faint
- [ ] **Outline ring ≥ 6px** — measure outer-minus-inner coordinate gap; thin rings disappear at 32px render size
- [ ] **Accent element ≥ 12 units** in smallest dimension for 64×64 module icons
- [ ] **Accent must contrast** against both light and dark backgrounds — TYPO3's cascade handles this, but verify the fallback `#ff8700` has sufficient contrast ratio
- [ ] **No `fill="white"`** — this breaks in light mode (invisible on white background)
- [ ] **No `fill="black"`** — this breaks in dark mode (invisible on dark background)
- [ ] **Clear browser localStorage** after changes — icons are cached client-side

#### Why NOT to Use `prefers-color-scheme`

The TYPO3 backend does NOT use `prefers-color-scheme` for its color mode. It uses
`data-color-scheme` and `data-theme` on the HTML element. Using
`prefers-color-scheme` in icon SVGs would cause them to be out of sync with the backend
theme when a user manually overrides the system preference.

### Color mapping from old to new

| Old Color | New Equivalent | Usage |
|-----------|----------------|-------|
| `#FFFFFF` (white on colored bg) | `currentColor` | Primary icon shapes |
| `#5BA34F` / `#3F7437` or any brand color background | REMOVE (no background) | — |
| `#5BA34F` accent elements (non-bg) | `var(--icon-color-accent, #ff8700)` | Accent highlights |
| `#333333` / `#333` detail lines | `currentColor` | Detail elements |
| `opacity="0.25"` | `opacity=".4"` | Secondary elements |
| `opacity="0.75"` | `opacity=".4"` or full opacity | Depends on visual weight |
| `fill="white"` | `currentColor` | NEVER hardcode white |
| `fill="black"` / `fill="#000"` | `currentColor` | NEVER hardcode black |

### Reference: TYPO3 v14 Core Module Icons

Study these core icons for the correct visual language:

**module-web** (Page/content module):
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path fill="currentColor" opacity=".4" d="M48 28.6H37.79c-1 0-2.04-1.09-2.04-2.1V16L48 28.6Z"/>
  <path fill="currentColor" d="M35.81 20 44 28.42V48H24V20h11.81m1.69-4H21.75c-.97 0-1.75.81-1.75 1.8v32.4c0 .99.78 1.8 1.75 1.8h24.5c.97 0 1.75-.81 1.75-1.8V26.8L37.5 16Z"/>
  <path fill="var(--icon-color-accent, #ff8700)" d="M20 17.8c0-.99.78-1.8 1.75-1.8H37.5l2.5 2.57V14c0-1.1-.9-2-2-2H14c-1.1 0-2 .9-2 2v32c0 1.1.9 2 2 2h6V17.8Z"/>
</svg>
```

**module-config** (actual TYPO3 Core module icon reference):
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path fill="currentColor" d="M36.51 52c-.67 0-1.24-.49-1.32-1.14l-.39-3.02c-.29-.11-.56-.24-.82-.39s-.51-.31-.75-.49l-2.89 1.18c-.62.25-1.34.02-1.67-.55l-2.49-4.19c-.34-.57-.19-1.29.35-1.69l2.5-1.84c-.02-.15-.03-.3-.03-.44v-.88c0-.14.01-.29.03-.44l-2.5-1.84c-.54-.4-.69-1.12-.35-1.69l2.49-4.19c.34-.57 1.05-.8 1.67-.55l2.89 1.18c.24-.17.5-.34.77-.49.27-.15.53-.28.8-.39l.39-3.02c.08-.65.65-1.14 1.32-1.14h4.98c.67 0 1.24.49 1.32 1.14l.39 3.02c.29.11.56.24.82.39s.51.31.75.49l2.89-1.18c.62-.25 1.34-.02 1.67.55l2.49 4.19c.34.57.19 1.29-.35 1.69l-2.5 1.84c.02.15.03.3.03.44v.88c0 .14-.02.29-.07.44l2.5 1.84c.54.4.69 1.12.35 1.69l-2.49 4.19c-.34.57-1.06.8-1.68.55l-2.85-1.18c-.24.17-.5.34-.77.49s-.53.28-.8.39l-.39 3.02c-.08.65-.65 1.14-1.32 1.14H36.5Zm2.56-8.45c1.29 0 2.39-.44 3.3-1.33s1.37-1.96 1.37-3.22-.46-2.33-1.37-3.22-2.01-1.33-3.3-1.33-2.42.44-3.32 1.33c-.9.89-1.35 1.96-1.35 3.22s.45 2.33 1.35 3.22c.9.89 2.01 1.33 3.32 1.33Z"/>
  <path fill="currentColor" opacity=".4" d="M16 52c-1.1 0-2-.9-2-2V14c0-1.1.9-2 2-2s2 .9 2 2v36c0 1.1-.9 2-2 2Zm12.67-4.4-2.49-4.19c-.34-.57-.19-1.29.35-1.69l2.5-1.84c-.02-.15-.03-.3-.03-.44v-.88c0-.14.01-.29.03-.44l-2.5-1.84c-.54-.4-.69-1.12-.35-1.69l2.49-4.19c.28-.46.81-.69 1.33-.62V14c0-1.1-.9-2-2-2s-2 .9-2 2v36c0 1.1.9 2 2 2s2-.9 2-2v-1.78c-.52.07-1.05-.16-1.33-.62ZM41.49 26c.18 0 .35.04.51.1V14c0-1.1-.9-2-2-2s-2 .9-2 2v12h3.49Z"/>
  <rect width="12" height="8" x="10" y="36" fill="var(--icon-color-accent, #ff8700)" rx="1.33" ry="1.33"/>
  <path fill="var(--icon-color-accent, #ff8700)" d="M28.67 30.4c.34-.57 1.05-.8 1.67-.55l2.89 1.18c.24-.17.5-.34.77-.49v-3.21c0-.74-.6-1.33-1.33-1.33h-9.33c-.74 0-1.33.6-1.33 1.33v5.33c0 .74.6 1.33 1.33 1.33h3.2l2.14-3.6Z"/>
  <rect width="12" height="8" x="34" y="16" fill="var(--icon-color-accent, #ff8700)" rx="1.33" ry="1.33"/>
</svg>
```

**module-site** (Globe):
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path fill="var(--icon-color-accent, #ff8700)" d="M32 16c8.82 0 16 7.18..."/>
  <path fill="currentColor" d="M21.05 43.64c.11-.83..."/>
</svg>
```

**Key patterns in core icons:**
- Document icons: outlined rectangle with folded corner, accent for secondary document layer
- Settings/gear icons: gear outline in `currentColor`, smaller gear or inner element in accent
- Globe/site icons: circle outline in accent, landmass/detail in `currentColor`
- List/content icons: lines/rows in `currentColor`, header or sidebar accent in accent color

## Step 3: Icon Registration (v14)

### Configuration/Icons.php

Icons MUST be registered via `Configuration/Icons.php`. This file is auto-loaded by TYPO3.

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider;

return [
    'module-myext' => [
        'provider' => SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/module-myext.svg',
    ],
    'module-myext-list' => [
        'provider' => SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/module-myext-list.svg',
    ],
];
```

Compact form using `array_map` (when all icons use `SvgIconProvider`):

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider;

return array_map(
    static fn (string $source) => [
        'provider' => SvgIconProvider::class,
        'source' => $source,
    ],
    [
        'module-myext' => 'EXT:my_extension/Resources/Public/Icons/module-myext.svg',
        'module-myext-list' => 'EXT:my_extension/Resources/Public/Icons/module-myext-list.svg',
    ]
);
```

### Configuration/Backend/Modules.php

Module definitions reference icons by their registered identifier:

```php
return [
    'myext_main' => [
        'position' => ['after' => 'web'],
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'iconIdentifier' => 'module-myext',
    ],
    'myext_list' => [
        'parent' => 'myext_main',
        'access' => 'user',
        'iconIdentifier' => 'module-myext-list',
        // ...
    ],
];
```

### Avoid: `IconRegistry::registerIcon()` during `ext_localconf.php`

New and migrated extensions should register icons in **`Configuration/Icons.php`**. Calling
`IconRegistry::registerIcon()` from `ext_localconf.php` was disallowed for v14 ([Deprecation-104778](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104778-InstantiationOfIconRegistryInExtLocalconf.html)) — the method itself is still valid when used from supported contexts (e.g. rare dynamic registration), but not from bootstrap files such as `ext_localconf.php` or `Configuration/TCA/Overrides/*.php`.

```php
// Legacy — do not add this in new code; use Configuration/Icons.php instead
$iconRegistry = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(
    \TYPO3\CMS\Core\Imaging\IconRegistry::class
);
$iconRegistry->registerIcon(
    'module-myext',
    \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
    ['source' => 'EXT:my_extension/Resources/Public/Icons/module-myext.svg']
);
```

## Step 4: Using Icons

### In Fluid Templates

```html
<core:icon identifier="module-myext" size="small" />

<!-- Inline SVG (allows CSS color inheritance): -->
<core:icon identifier="module-myext" size="small" alternativeMarkupIdentifier="inline" />
```

### In PHP

```php
use TYPO3\CMS\Core\Imaging\IconFactory;
use TYPO3\CMS\Core\Imaging\IconSize;

public function __construct(
    private readonly IconFactory $iconFactory,
) {}

public function getIcon(): string
{
    // Optional 3rd/4th args: ?string $overlayIdentifier = null, ?IconState $state = null
    return $this->iconFactory
        ->getIcon('module-myext', IconSize::SMALL)
        ->render();
}
```

### In JavaScript (ES6)

```javascript
import Icons from '@typo3/backend/icons.js';

Icons.getIcon('module-myext', Icons.sizes.small).then((icon) => {
    document.querySelector('.target').innerHTML = icon;
});
```

### Icon Sizes (v14)

| Enum Value | Size | Use Case |
|------------|------|----------|
| `IconSize::MEGA` | 64px | New Content Element wizard, large previews |
| `IconSize::LARGE` | 48px | Wizard icons, large previews |
| `IconSize::MEDIUM` | 32px | Default **module menu / sidebar** module icons (top toolbar uses smaller icons — closer to `SMALL`) |
| `IconSize::SMALL` | 16px | Inline, lists, TCA |
| `IconSize::DEFAULT` | `1em` (CSS) / 16×16 (PHP `getDimensions()`) — actual rendered size depends on the parent element's `font-size` | Prefer `SMALL` when you need a fixed **16px** icon |
| `IconSize::OVERLAY` | 16×16 (PHP) / 68.75% of parent (CSS) | `@internal` — Core overlays (hidden/locked badges), not for extension icons |

When no size is passed to `IconFactory->getIcon()`, the default is `IconSize::MEDIUM` (32px).

## Appendix
For icon accent strategy, package notes, and common mistake tables, see [references/design-notes.md](references/design-notes.md). For the migration checklist and shape-transformation examples, see [references/migration-steps.md](references/migration-steps.md).
Source: https://github.com/dirnbauer/webconsulting-skills
Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.
