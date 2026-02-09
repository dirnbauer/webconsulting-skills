---
name: typo3-records-list-types-custom-views
description: Complete guide for creating custom view types in Records List Types. Template variables, real-world examples, CSS/JS assets, PSR-14 registration, and page-scoped views.
version: 1.0.0
typo3_compatibility: "14.0 - 14.x"
related_skills:
  - typo3-records-list-types
triggers:
  - custom view type
  - records list template
  - backend view fluid
  - kanban view
  - timeline view
  - catalog view
---

# Custom View Types for Records List Types

> Zero-PHP extensibility: TSconfig + Fluid template + CSS. No PHP classes needed.

## Quick Start: 3 Steps

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

Copy `GenericView.html` from `EXT:records_list_types/Resources/Private/Templates/` and customize:

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:core="http://typo3.org/ns/TYPO3/CMS/Core/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="timeline-container">
    <f:for each="{tableData}" as="table">
        <div class="recordlist" id="t3-table-{table.tableName}">
            <!-- Table heading (uses base.css styles) -->
            <div class="recordlist-heading">
                <div class="recordlist-heading-row">
                    <div class="recordlist-heading-title">
                        <a href="{table.singleTableUrl}">
                            <span class="fw-bold">{table.tableLabel}</span>
                            <span>({table.recordCount})</span>
                        </a>
                    </div>
                    <div class="recordlist-heading-actions">
                        <f:if condition="{table.actionButtons.newRecordButton}">
                            <f:format.raw>{table.actionButtons.newRecordButton}</f:format.raw>
                        </f:if>
                    </div>
                </div>
            </div>

            <!-- Pagination (top) -->
            <f:render partial="Pagination"
                arguments="{paginator: table.paginator, pagination: table.pagination,
                paginationUrl: table.paginationUrl, tableName: table.tableName, position: 'top'}" />

            <!-- Your custom layout -->
            <div class="timeline-list">
                <f:for each="{table.records}" as="record">
                    <div class="timeline-item">
                        <div class="timeline-marker"></div>
                        <div class="timeline-content">
                            <strong>{record.title}</strong>
                            <f:for each="{record.displayValues}" as="field">
                                <f:if condition="{field.type} == 'datetime'">
                                    <span class="text-muted small ms-2">{field.formatted}</span>
                                </f:if>
                            </f:for>
                        </div>
                    </div>
                </f:for>
            </div>

            <!-- Pagination (bottom) -->
            <f:render partial="Pagination"
                arguments="{paginator: table.paginator, pagination: table.pagination,
                paginationUrl: table.paginationUrl, tableName: table.tableName, position: 'bottom'}" />
        </div>
    </f:for>
</div>

</html>
```

### Step 3: Add CSS

```css
/* EXT:my_sitepackage/Resources/Public/Css/timeline.css */
.timeline-list { padding: 1rem; }
.timeline-item {
    display: flex; gap: 1rem; padding: 0.5rem 0;
    border-bottom: 1px solid var(--typo3-component-border-color, #e5e7eb);
}
.timeline-marker {
    width: 12px; height: 12px; border-radius: 50%;
    background: var(--typo3-state-info-bg, #3b82f6);
    margin-top: 4px; flex-shrink: 0;
}
.timeline-content { flex: 1; color: var(--typo3-text-color-base, #18181b); }
```

## Template Variables Reference

### Top-Level Variables

| Variable | Type | Description |
|----------|------|-------------|
| `pageId` | int | Current page UID |
| `tableData` | array | Array of table data objects |
| `currentTable` | string | Filtered table name (or empty) |
| `searchTerm` | string | Current search term |
| `viewMode` | string | Active view type ID |
| `viewConfig` | array | View type configuration |

### Each `tableData` Entry

| Key | Type | Description |
|-----|------|-------------|
| `tableName` | string | Database table name |
| `tableLabel` | string | Human-readable table label |
| `tableIcon` | string | TYPO3 icon identifier |
| `records` | array | Enriched record objects |
| `recordCount` | int | Total record count |
| `actionButtons` | array | Rendered HTML action buttons |
| `sortingDropdownHtml` | string | Sorting dropdown HTML |
| `sortingModeToggleHtml` | string | Manual/field sorting toggle HTML |
| `sortableColumnHeaders` | string | Column headers for table views |
| `singleTableUrl` | string | URL to filter by this table |
| `clearTableUrl` | string | URL to show all tables |
| `displayColumns` | array | Columns to display |
| `sortField` | string | Current sort field |
| `sortDirection` | string | Current sort direction |
| `canReorder` | bool | Drag-drop enabled |
| `lastRecordUid` | int | Last record UID |
| `paginator` | object | `DatabasePaginator` (PaginatorInterface) |
| `pagination` | object | `SlidingWindowPagination` |
| `paginationUrl` | string | Base URL for pagination |

### Each Record

| Key | Type | Description |
|-----|------|-------------|
| `uid` | int | Record UID |
| `pid` | int | Page UID |
| `tableName` | string | Table name |
| `title` | string | Label field value |
| `iconIdentifier` | string | Record icon |
| `hidden` | bool | Hidden status |
| `rawRecord` | array | Full database row |
| `displayValues` | array | Formatted field values |

### Each `displayValues` Field

| Key | Type | Description |
|-----|------|-------------|
| `field` | string | Field name |
| `label` | string | Translated label |
| `type` | string | `text`, `datetime`, `boolean`, `number`, `relation`, `link` |
| `isLabelField` | bool | Whether this is the title field |
| `raw` | mixed | Raw database value |
| `formatted` | string | Formatted display value |
| `isEmpty` | bool | Whether value is empty |

## Configuration Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `label` | string | *required* | Display name (supports `LLL:` references) |
| `icon` | string | *required* | TYPO3 icon identifier |
| `description` | string | *(empty)* | Tooltip description |
| `template` | string | `<TypeId>View` | Fluid template name (without `.html`) |
| `partial` | string | `Card` | Default partial for record rendering |
| `templateRootPath` | string | *(extension)* | Custom Fluid template path |
| `partialRootPath` | string | *(extension)* | Custom Fluid partial path |
| `layoutRootPath` | string | *(extension)* | Custom Fluid layout path |
| `css` | string | *(none)* | CSS file (`EXT:my_ext/...` syntax) |
| `js` | string | *(none)* | JS module (`@vendor/module.js` syntax) |
| `columnsFromTCA` | bool | `1` | Use editor's column selection |
| `displayColumns` | string | *(empty)* | Comma-separated field list |
| `itemsPerPage` | int | `100` | Records per page (`0` = no pagination) |

### Special Column Names for `displayColumns`

| Name | Resolves to |
|------|-------------|
| `label` | TCA `ctrl.label` field (record title) |
| `datetime` | First date field (`datetime`, `date`, `starttime`, `crdate`) |
| `teaser` | First description field (`teaser`, `abstract`, `description`, `bodytext`, `short`) |

## Reusing Built-in Templates

No new Fluid template needed -- use existing ones with custom columns:

| Template | Best for |
|----------|----------|
| `GridView` | Visual content with images |
| `CompactView` | Dense data, many records |
| `TeaserView` | Content previews with dates |
| `GenericView` | Starting point for custom layouts |

## Real-World Examples

### Product Catalog

```tsconfig
mod.web_list.viewMode {
    allowed = list,grid,catalog
    types.catalog {
        label = Product Catalog
        icon = actions-viewmode-tiles
        template = GridView
        columnsFromTCA = 0
        displayColumns = label,teaser
        itemsPerPage = 24
    }
}

mod.web_list.gridView.table.tx_myshop_domain_model_product {
    titleField = name
    descriptionField = short_description
    imageField = images
    preview = 1
}
```

### Address Book (Compact, fixed columns)

```tsconfig
mod.web_list.viewMode.types.addressbook {
    label = Address Book
    icon = actions-user
    template = CompactView
    displayColumns = name,email,phone,company,city
    columnsFromTCA = 0
    itemsPerPage = 500
}
```

### Event Calendar (page-scoped)

```tsconfig
[page["uid"] == 55]
    mod.web_list.viewMode {
        allowed = list,eventlist
        default = eventlist
        types.eventlist {
            label = Event List
            icon = actions-calendar
            template = TeaserView
            displayColumns = label,datetime,teaser
            columnsFromTCA = 0
            itemsPerPage = 30
        }
    }
[end]
```

### Photo Gallery (48 items, no description)

```tsconfig
mod.web_list.viewMode.types.gallery {
    label = Photo Gallery
    icon = actions-image
    template = GridView
    columnsFromTCA = 0
    displayColumns = label
    itemsPerPage = 48
}

mod.web_list.gridView.table.sys_file_metadata {
    titleField = title
    imageField = file
    preview = 1
}
```

### Full List (no pagination)

```tsconfig
mod.web_list.viewMode.types.fulllist {
    label = Full List
    icon = actions-viewmode-list
    template = CompactView
    columnsFromTCA = 1
    itemsPerPage = 0
}
```

## Page-Scoped View Patterns

```tsconfig
# Grid-only for media folders
[page["doktype"] == 254]
    mod.web_list.viewMode.default = grid
    mod.web_list.viewMode.allowed = list,grid
[end]

# Compact for system records
[page["module"] == "system"]
    mod.web_list.viewMode.default = compact
    mod.web_list.viewMode.allowed = list,compact
[end]

# Custom view for page tree (uid=100 + children)
[page["uid"] == 100 || page["pid"] == 100]
    mod.web_list.viewMode {
        allowed = list,grid,catalog
        default = catalog
        types.catalog {
            label = Product Catalog
            icon = actions-viewmode-tiles
            template = CatalogView
            templateRootPath = EXT:my_sitepackage/Resources/Private/Backend/Templates/
            css = EXT:my_sitepackage/Resources/Public/Css/catalog.css
            columnsFromTCA = 1
        }
    }
[end]
```

## Asset Loading

### Automatic Assets (all views)

| Asset | Purpose |
|-------|---------|
| `base.css` | Shared heading, pagination, sorting styles |
| `GridViewActions.js` | Drag-drop, actions, pagination, sorting, search |
| `column-selector-button.js` | TYPO3 column selector web component |

### Loading Order

```
1. base.css              ← Always (shared)
2. your-view.css         ← Your css option
3. GridViewActions.js    ← Always (base JS)
4. your-module.js        ← Your js option
```

### Custom CSS (with dark mode)

```css
.kanban-column {
    background: var(--typo3-component-bg, #fff);
    border: 1px solid var(--typo3-component-border-color, #d4d4d8);
    color: var(--typo3-text-color-base, #18181b);
}
```

### Custom JavaScript

Register ES module in `Configuration/JavaScriptModules.php`:

```php
return [
    'imports' => [
        '@my-sitepackage/' => 'EXT:my_sitepackage/Resources/Public/JavaScript/',
    ],
];
```

Reference in TSconfig:

```tsconfig
mod.web_list.viewMode.types.kanban.js = @my-sitepackage/kanban-board.js
```

### Custom Icons

Register in `Configuration/Icons.php`:

```php
return [
    'my-kanban-icon' => [
        'provider' => \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
        'source' => 'EXT:my_sitepackage/Resources/Public/Icons/kanban.svg',
    ],
];
```

Then: `mod.web_list.viewMode.types.kanban.icon = my-kanban-icon`

## File Structure for Custom View

```
my_sitepackage/
├── Configuration/
│   ├── Icons.php                          # Custom icons (optional)
│   ├── JavaScriptModules.php              # ES modules (if using js)
│   └── TsConfig/Page/mod.tsconfig        # View type registration
├── Resources/
│   ├── Private/Backend/
│   │   ├── Templates/KanbanView.html      # Main template
│   │   └── Partials/KanbanCard.html       # Card partial (optional)
│   └── Public/
│       ├── Css/kanban.css                 # View styles
│       ├── JavaScript/kanban-board.js     # Custom JS (optional)
│       └── Icons/kanban.svg               # Custom icon (optional)
```

## PSR-14 Registration (for extensions)

Use the PSR-14 event instead of TSconfig when building distributable extensions:

```php
use TYPO3\CMS\Core\Attribute\AsEventListener;
use Webconsulting\RecordsListTypes\Event\RegisterViewModesEvent;

#[AsEventListener]
final class RegisterCustomViewListener
{
    public function __invoke(RegisterViewModesEvent $event): void
    {
        $event->addViewMode('kanban', [
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:viewMode.kanban',
            'icon' => 'actions-view-table-columns',
            'description' => 'Kanban board view',
            'template' => 'KanbanView',
            'css' => 'EXT:my_ext/Resources/Public/Css/kanban.css',
        ]);
    }
}
```

### Event API

```php
$event->addViewMode(string $id, array $config): void    // Add new view type
$event->removeViewMode(string $id): void                 // Remove (disable) a view type
$event->hasViewMode(string $id): bool                    // Check existence
$event->modifyViewMode(string $id, array $config): void  // Override config
$event->getViewModes(): array                            // Get all registered
```

## Companion Extension

For 6 ready-to-use example view types (Timeline, Catalog, Address Book, Event List, Gallery, Dashboard), install:

```bash
composer require webconsulting/records-list-examples
```

Source: [github.com/dirnbauer/typo3-records-list-examples](https://github.com/dirnbauer/typo3-records-list-examples)
