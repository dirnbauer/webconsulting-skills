---
name: "typo3-records-list-types"
description: "Configures TYPO3 v14 Records module list types and custom backend views, including grid, compact, teaser, kanban-style, timeline-style, TSconfig, Fluid templates, icons, and accessibility. Use when the user mentions records list types, backend record cards, custom Records module views, grid view, compact view, teaser view, or TSconfig-driven record presentation."
metadata:
  version: "1.0.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Records List Types

> Source: https://github.com/dirnbauer/webconsulting-skills

> **Compatibility:** TYPO3 v14.0+ / PHP 8.3+
> Extension key: `records_list_types` / Composer package name: `webconsulting/records-list-types`
> GitHub: https://github.com/dirnbauer/typo3-records-list-types
>
> **Extension version:** Use the **GitHub repository** / `composer.json` of `webconsulting/records-list-types` as the source of truth — this skill’s YAML `version` is for the **skill document** only.
>
> **Composer / Packagist:** Confirm on [Packagist](https://packagist.org/) whether `webconsulting/records-list-types` is published. If not, add a **`repositories` → `vcs`** entry in the **root** `composer.json` pointing at the GitHub repo, then `composer require vendor/package:dev-main` (or a tag). Plain `composer require webconsulting/records-list-types` **fails** until the package is registered or aliased.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## 1. Overview

Transforms the TYPO3 backend **Records** module with multiple view modes:

| View | Description | Best for |
|------|-------------|----------|
| **List** | Standard TYPO3 table (unchanged) | Data-heavy tables, system records |
| **Grid** | Card layout with thumbnails, drag-and-drop | News, products, team members, media |
| **Compact** | Dense single-line rows, fixed columns | Address books, logs, settings, bulk data |
| **Teaser** | Minimal cards with title, date, excerpt | Blog posts, events, press releases |
| **Custom** | Your own views via TSconfig + Fluid | Timeline, kanban, catalog, gallery |

All views include: pagination, sorting, search, record actions, workspace indicators, dark mode, WCAG 2.1 accessibility.

### Features

- **Grid View** -- Card-based layout with thumbnails, drag-and-drop reordering, and field display
- **Compact View** -- Dense single-line rows with fixed columns and horizontal scrolling
- **Teaser View** -- News-style cards with title, date, and description excerpt
- **Custom Views** -- Register your own view types via PSR-14 events or TSconfig
- **Drag & Drop** -- Mouse and keyboard reordering with full WCAG 2.1 accessibility
- **Language Flags** -- Language flag icons displayed per record in grid cards
- **Workspace Support** -- Color-coded indicators for new, modified, moved, and deleted records
- **Dark Mode** -- Full compatibility with TYPO3's dark mode (light/dark themes)
- **Per-Table Config** -- Configure title, description, image, and display fields via TSconfig
- **User Preferences** -- View mode is persisted per backend user via AJAX
- **Sorting Controls** -- Manual drag ordering and field-based sorting with direction toggle
- **Pagination** -- Matches TYPO3 Core: multi-table mode shows limited records with "Expand table" button, single-table mode shows full pagination (record range, page input, first/prev/next/last)
- **Image Preview Hint** -- Subtle notice below thumbnails reminding editors that the image may not appear on the frontend for certain record types
- **Zero-PHP Extensibility** -- Add new view types with just TSconfig + Fluid template + CSS, no PHP classes needed
- **Search** -- Client-side search filtering across all view modes
- **Accessibility** -- WCAG 2.1 compliant keyboard navigation, ARIA labels, and screen reader support

## 2. Installation

```bash
composer require webconsulting/records-list-types
./vendor/bin/typo3 extension:setup -e records_list_types
```

After activation, view mode toggle buttons appear in the Records module header.

## 3. View Mode Configuration

### Set Default and Allowed Views

```tsconfig
mod.web_list.viewMode {
    default = grid                          # Default for new users
    allowed = list,grid,compact,teaser      # Available in toggle
}
```

### Grid Column Count

```tsconfig
mod.web_list.gridView.cols = 4    # 2-6 columns (default: 4)
```

### View Mode Resolution Order

1. **URL parameter** (`?displayMode=grid`) -- highest priority
2. **User preference** (stored via AJAX, persisted per session)
3. **TSconfig default** (`mod.web_list.viewMode.default`)
4. **Fallback**: `list`

## 4. Per-Table Field Configuration

Configure which fields appear on cards for each table:

```tsconfig
mod.web_list.gridView.table.<tableName> {
    titleField = title              # Card title (default: TCA ctrl.label)
    descriptionField = teaser       # Card body text
    imageField = fal_media          # FAL field for thumbnail
    preview = 1                     # Enable thumbnails (1/0)
}
```

### Common Tables

```tsconfig
# News
mod.web_list.gridView.table.tx_news_domain_model_news {
    titleField = title
    descriptionField = teaser
    imageField = fal_media
    preview = 1
}

# Pages
mod.web_list.gridView.table.pages {
    titleField = title
    descriptionField = abstract
    imageField = media
    preview = 1
}

# Content Elements
mod.web_list.gridView.table.tt_content {
    titleField = header
    descriptionField = bodytext
    imageField = image
    preview = 1
}

# Frontend Users
mod.web_list.gridView.table.fe_users {
    titleField = name
    descriptionField = email
    imageField = image
    preview = 1
}
```

## 5. View Modes Detail

### Grid View

- **Card structure**: Header (icon, title, drag handle, actions), optional thumbnail image (16:9), field values body, footer (UID, PID, language flag)
- **Thumbnails**: Automatically resolved from FAL image fields (configurable per table)
- **Field display**: Type-aware formatting -- booleans as badges, dates in monospace, relations with count indicators, links as clickable, text truncated with ellipsis
- **Two-column field layout**: Small fields display side-by-side; text/richtext fields span full width
- **Drag-and-drop**: Both mouse and keyboard (Space to grab, arrows to move, Space to drop, Escape to cancel)
- **Record actions**: Inline visibility toggle, edit, delete, plus dropdown for info, history, copy, cut
- **State indicators**: Hidden records get amber headers; workspace records show blue/purple/cyan/red headers
- **Language flags**: Each card shows the record's language flag icon in the bottom-right corner
- **Responsive grid**: Auto-fills columns from 320px minimum, scales from 1 column on mobile to multiple on wide screens

### Compact View

- **Fixed columns**: Icon, UID, and title pinned on the left; status toggle, edit, delete pinned on the right
- **Scrollable middle**: Additional fields scroll horizontally between fixed columns
- **Scroll shadows**: Visual indicators when content extends beyond the visible area
- **Sortable headers**: Click column headers to sort ascending/descending via TYPO3's native dropdown API
- **Zebra striping**: Alternating row colors for readability
- **Hidden record styling**: Muted background and dimmed title for hidden records

### Teaser View

- **Clean design**: Title, date with calendar icon, description excerpt (2-line clamp)
- **Status badges**: UID pill and hidden/visible indicator
- **Compact actions**: Visibility toggle, edit, delete buttons
- **Hidden state**: Accent bar on hidden records
- **CSS `light-dark()`**: Native theme switching support

## 6. Pagination

Matches TYPO3 Core List View behavior:

- **Multi-table mode**: Limited records per table with "Expand table" button
- **Single-table mode**: Full pagination (record range, page input, first/prev/next/last)

```tsconfig
# Global default items per page
mod.web_list.viewMode.itemsPerPage = 100

# Per-type override
mod.web_list.viewMode.types.grid.itemsPerPage = 100
mod.web_list.viewMode.types.compact.itemsPerPage = 300
mod.web_list.viewMode.types.teaser.itemsPerPage = 100

# Disable pagination
mod.web_list.viewMode.types.grid.itemsPerPage = 0
```

## 7. Sorting

Tables with TCA `sortby` support two modes:

- **Manual**: Drag-and-drop reordering (default)
- **Field**: Sort by column with ascending/descending toggle

A segmented toggle switches between modes. Drag-and-drop supports both mouse and keyboard (Space to grab, arrows to move, Space to drop, Escape to cancel).

## 8. Custom View Types (Quick Start)

Add a view in **3 steps** -- zero PHP required.

### Step 1: Register via TSconfig

```tsconfig
mod.web_list.viewMode {
    allowed = list,grid,compact,teaser,timeline

    types.timeline {
        label = Timeline
        icon = actions-calendar
        template = TimelineView
        templateRootPath = EXT:my_sitepackage/Resources/Private/Backend/Templates/
        css = EXT:my_sitepackage/Resources/Public/Css/timeline.css
        displayColumns = label,datetime,teaser
        columnsFromTCA = 0
    }
}
```

### Step 2: Create Fluid Template

Copy `GenericView.html` from the extension as a starting point. Key variables: `tableData`, `tableData.records`, `record.title`, `record.displayValues`.

### Step 3: Add CSS (optional)

Use TYPO3 CSS variables for automatic dark mode:

```css
.timeline-item {
    /* TYPO3 Core fallbacks; `--gv-*` tokens are defined by this extension, not by TYPO3 Core */
    background: var(--typo3-component-bg, #fff);
    border: 1px solid var(--typo3-component-border-color, #d4d4d8);
}
```

> **Full documentation**: See [SKILL-CUSTOM-VIEWS.md](SKILL-CUSTOM-VIEWS.md) for complete reference including template variables, real-world examples, asset loading, PSR-14 registration, and page-scoped views.

### Reuse Built-in Templates

No new template needed -- reuse existing ones with custom columns:

```tsconfig
# Address book using CompactView with fixed columns
mod.web_list.viewMode.types.addressbook {
    label = Address Book
    icon = actions-user
    template = CompactView
    displayColumns = name,email,phone,company,city
    columnsFromTCA = 0
    itemsPerPage = 500
}
```

### Page-Scoped Views

Restrict views to specific pages:

```tsconfig
[traverse(page, "uid") == 42]
    mod.web_list.viewMode {
        allowed = list,timeline
        default = timeline
    }
[END]
```

## 9. Column Display

Two modes control which fields appear:

| Mode | Setting | Behavior |
|------|---------|----------|
| **Editor-controlled** | `columnsFromTCA = 1` | Respects editor's "Show columns" selection |
| **Fixed layout** | `columnsFromTCA = 0` | Uses `displayColumns` list exactly |

### `columnsFromTCA = 1` Resolution Order

1. **Editor's "Show columns" selection** (stored per-user per-table)
2. **This extension’s own TSconfig / template resolution** — not Core `mod.web_list.table.<table>.showFields` (that path is not a documented Core column picker). See extension docs and `GridConfigurationService` behaviour for your release.
3. **TCA `ctrl.label` and sensible text/date fallbacks** (see “Special Column Names” below) — TYPO3 v14 removed `ctrl.searchFields`; backend search now auto-includes suitable fields and can be tuned per-column via `searchable`, which is unrelated to this list display.
4. **Label field only** (final fallback)

### Special Column Names

| Name | Resolves to |
|------|-------------|
| `label` | TCA `ctrl.label` field (record title) |
| `datetime` | First date field (`datetime`, `date`, `starttime`, `crdate`) |
| `teaser` | First description field (`teaser`, `abstract`, `description`, `bodytext`, `short`) |

## 10. TSconfig Reference

### View Type Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `label` | string | *required* | Display name (supports `LLL:`) |
| `icon` | string | *required* | TYPO3 icon identifier |
| `description` | string | | Tooltip |
| `template` | string | `<Id>View` | Fluid template name |
| `partial` | string | `Card` | Default partial |
| `templateRootPath` | string | | Custom template path |
| `partialRootPath` | string | | Custom partial path |
| `layoutRootPath` | string | | Custom layout path |
| `css` | string | | CSS file (`EXT:` syntax) |
| `js` | string | | JS module (`@vendor/module.js`) |
| `columnsFromTCA` | bool | `1` | Use editor column selection |
| `displayColumns` | string | | Comma-separated field list |
| `itemsPerPage` | int | `100` | Records per page (`0` = no pagination) |

## 11. Workspace Support

Records display color-coded indicators in workspaces:

| State | Color | Visual |
|-------|-------|--------|
| New | Blue | Blue header + left border |
| Modified | Purple | Purple header + left border |
| Moved | Cyan | Cyan header + left border |
| Deleted | Red | Red header + strikethrough title |

Workspace overlays applied via `BackendUtility::workspaceOL()`.

> **Note:** Workspace support is experimental. Visual indicators work, but drag-and-drop within workspaces has limited testing.


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
