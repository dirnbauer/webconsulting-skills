# Custom View Types - Full Reference

> Part of the [TYPO3 Records List Types](SKILL.md) skill.
> Extension: `webconsulting/records-list-types` / GitHub: https://github.com/dirnbauer/typo3-records-list-types

Adding a new view type requires **zero PHP**. You provide TSconfig + a Fluid template, and the extension handles the rest: record fetching, pagination, sorting, action buttons, and asset loading.

> **Want working examples?** Install the companion extension [Records List Examples](https://github.com/dirnbauer/typo3-records-list-examples) to get 6 ready-to-use view types (Timeline, Catalog, Address Book, Event List, Gallery, Dashboard) with full templates and CSS.

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

Copy `GenericView.html` from the extension and customize it:

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:core="http://typo3.org/ns/TYPO3/CMS/Core/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="timeline-container">
    <f:for each="{tableData}" as="table">
        <div class="recordlist" id="t3-table-{table.tableName}">
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

            <f:render partial="Pagination" arguments="{paginator: table.paginator, pagination: table.pagination, paginationUrl: table.paginationUrl, tableName: table.tableName, position: 'top'}" />

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

            <f:render partial="Pagination" arguments="{paginator: table.paginator, pagination: table.pagination, paginationUrl: table.paginationUrl, tableName: table.tableName, position: 'bottom'}" />
        </div>
    </f:for>
</div>

</html>
```

### Step 3: Add CSS (optional)

```css
.timeline-list { padding: 1rem; }
.timeline-item { display: flex; gap: 1rem; padding: 0.5rem 0; border-bottom: 1px solid #e5e7eb; }
.timeline-marker { width: 12px; height: 12px; border-radius: 50%; background: #3b82f6; margin-top: 4px; flex-shrink: 0; }
.timeline-content { flex: 1; }
```

## Page-Scoped Views

Restrict a view type to specific pages using TSconfig conditions:

```tsconfig
# Timeline only on the Events page (uid=42)
[page["uid"] == 42]
    mod.web_list.viewMode {
        allowed = list,timeline
        default = timeline
        types.timeline {
            label = Event Timeline
            icon = actions-calendar
            template = TimelineView
            templateRootPath = EXT:my_sitepackage/Resources/Private/Backend/Templates/
            css = EXT:my_sitepackage/Resources/Public/Css/timeline.css
            displayColumns = label,datetime,teaser
            columnsFromTCA = 0
            itemsPerPage = 50
        }
    }
[end]

# Grid-only for media folders (doktype 254 = sysfolder)
[page["doktype"] == 254]
    mod.web_list.viewMode.default = grid
    mod.web_list.viewMode.allowed = list,grid
[end]

# Custom view for an entire page tree (pid=100 and its children)
[page["uid"] == 100 || page["pid"] == 100]
    mod.web_list.viewMode {
        allowed = list,grid,catalog
        default = catalog
    }
[end]
```

## Real-World Examples

### Product Catalog

```tsconfig
mod.web_list.viewMode {
    allowed = list,grid,catalog
    types.catalog {
        label = Product Catalog
        icon = actions-viewmode-tiles
        template = CatalogView
        templateRootPath = EXT:my_sitepackage/Resources/Private/Backend/Templates/
        css = EXT:my_sitepackage/Resources/Public/Css/catalog.css
        displayColumns = label,teaser
        columnsFromTCA = 0
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

### Address Book (reuses CompactView)

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

### Event Calendar (reuses TeaserView)

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

### News Dashboard (editor-controlled columns)

```tsconfig
mod.web_list.viewMode.types.newsdash {
    label = News Dashboard
    icon = content-news
    template = TeaserView
    columnsFromTCA = 1
    itemsPerPage = 20
}
mod.web_list.viewMode.allowed = list,grid,newsdash
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

## Reusing Built-in Templates

| Template | Best for |
|----------|----------|
| `GridView` | Visual content with images (products, team members, portfolio) |
| `CompactView` | Dense data (addresses, system records, logs, settings) |
| `TeaserView` | Content previews (news, blog posts, events, press releases) |
| `GenericView` | Starting point for fully custom layouts |

## Configuration Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `label` | string | *required* | Display name in the view switcher (supports `LLL:`) |
| `icon` | string | *required* | TYPO3 icon identifier |
| `description` | string | *(empty)* | Tooltip description |
| `template` | string | `<TypeId>View` | Fluid template name (without `.html`) |
| `partial` | string | `Card` | Default partial for record cards |
| `templateRootPath` | string | *(extension default)* | Custom template path |
| `partialRootPath` | string | *(extension default)* | Custom partial path |
| `layoutRootPath` | string | *(extension default)* | Custom layout path |
| `css` | string | *(none)* | CSS file to include (`EXT:` syntax) |
| `js` | string | *(none)* | JavaScript module (`@vendor/module.js` syntax) |
| `columnsFromTCA` | bool | `1` | Use editor's column selection from TCA |
| `displayColumns` | string | *(empty)* | Comma-separated field list |
| `itemsPerPage` | int | `100` | Records per page (`0` = no pagination) |

## Column Display: `columnsFromTCA` vs `displayColumns`

**`columnsFromTCA = 1`** (default) -- resolution order:

1. **Editor's "Show columns" selection** (stored per-user per-table)
2. **TSconfig `showFields`** (`mod.web_list.table.<table>.showFields`)
3. **TCA `searchFields`**
4. **Label field only** (final fallback)

**`columnsFromTCA = 0`** -- uses the explicit `displayColumns` list exactly.

| View | `columnsFromTCA` | `displayColumns` | Result |
|------|:-:|---|---|
| Grid | `1` | *(not set)* | Editors choose columns via selector |
| Compact | `1` | *(not set)* | Editors choose columns |
| Teaser | `0` | `label,datetime,teaser` | Always title + date + description |

### Special Column Names

| Name | Resolves to |
|------|-------------|
| `label` | TCA `ctrl.label` field (record title) |
| `datetime` | First date field (`datetime`, `date`, `starttime`, `crdate`) |
| `teaser` | First description field (`teaser`, `abstract`, `description`, `bodytext`, `short`) |

## Template Variables

Your template receives these variables:

| Variable | Description |
|----------|-------------|
| `pageId` | Current page ID |
| `tableData` | Array of table data (see below) |
| `currentTable` | Filtered table name (or empty) |
| `searchTerm` | Current search term |
| `viewMode` | View type identifier |
| `viewConfig` | View type configuration array |
| `middlewareWarning` | Middleware diagnostic warning (if any) |
| `forceListViewUrl` | URL to force list view (if middleware issue) |

### Each item in `tableData`

| Key | Description |
|-----|-------------|
| `tableName` | Database table name |
| `tableLabel` | Human-readable table label |
| `tableIcon` | TYPO3 icon identifier |
| `records` | Array of enriched records |
| `recordCount` | Total number of records |
| `actionButtons` | Rendered action button HTML |
| `sortingDropdownHtml` | Sorting dropdown HTML |
| `sortingModeToggleHtml` | Manual/field sorting toggle HTML |
| `sortableColumnHeaders` | Sortable column header HTML (for table views) |
| `singleTableUrl` | URL to filter by this table |
| `clearTableUrl` | URL to show all tables |
| `displayColumns` | Columns to display |
| `sortField`, `sortDirection` | Current sorting state |
| `canReorder` | Whether drag-drop is enabled |
| `lastRecordUid` | Last record UID (for drag-drop end zone) |
| `paginator` | `DatabasePaginator` (PaginatorInterface) |
| `pagination` | `SlidingWindowPagination` (PaginationInterface) |
| `paginationUrl` | Base URL for pagination links |
| `formActionUrl` | Form action URL for multi-record selection |
| `hasMore` | Whether there are more records than shown (multi-table mode) |
| `multiRecordSelectionActionsHtml` | HTML for multi-record selection actions |

### Each record in `records`

| Key | Description |
|-----|-------------|
| `uid`, `pid` | Record identifiers |
| `tableName` | Table name |
| `title` | Label field value |
| `iconIdentifier` | Record icon |
| `hidden` | Hidden status |
| `rawRecord` | Full database row |
| `thumbnailUrl` | Resolved thumbnail URL (if configured) |
| `displayValues` | Array of formatted field values |

### Each field in `displayValues`

| Key | Description |
|-----|-------------|
| `field` | Field name |
| `label` | Translated label |
| `type` | Field type (`text`, `datetime`, `boolean`, `number`, `relation`, `link`) |
| `isLabelField` | Whether this is the title field |
| `raw` | Raw database value |
| `formatted` | Formatted display value |
| `isEmpty` | Whether value is empty |

## Assets: CSS, JavaScript, Images

### What is loaded automatically

| Asset | Source | Purpose |
|-------|--------|---------|
| `base.css` | Extension | Shared heading, pagination, sorting styles |
| `GridViewActions.js` | Extension | Drag-drop, record actions, pagination input, sorting, search |
| `column-selector-button.js` | TYPO3 Core | Column selector web component |

### CSS

```tsconfig
mod.web_list.viewMode.types.kanban {
    css = EXT:my_sitepackage/Resources/Public/Css/kanban.css
}
```

Use TYPO3 CSS variables for dark mode:

```css
.kanban-column {
    background: var(--typo3-component-bg, #fff);
    border: 1px solid var(--typo3-component-border-color, #d4d4d8);
    color: var(--typo3-text-color-base, #18181b);
}
```

### JavaScript

```tsconfig
mod.web_list.viewMode.types.kanban {
    js = @my-sitepackage/kanban-board.js
}
```

Register in `Configuration/JavaScriptModules.php`:

```php
<?php
return [
    'imports' => [
        '@my-sitepackage/' => 'EXT:my_sitepackage/Resources/Public/JavaScript/',
    ],
];
```

### Images and Icons

Register custom icons in `Configuration/Icons.php`:

```php
<?php
return [
    'my-kanban-icon' => [
        'provider' => \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
        'source' => 'EXT:my_sitepackage/Resources/Public/Icons/kanban.svg',
    ],
];
```

Reference in TSconfig: `mod.web_list.viewMode.types.kanban.icon = my-kanban-icon`

### Asset Loading Order

```
1. base.css                          ← Always (shared heading, pagination, sorting)
2. your-view.css                     ← Your css option
3. GridViewActions.js                ← Always (drag-drop, actions, pagination input)
4. column-selector-button.js         ← Always (TYPO3 column selector)
5. your-module.js                    ← Your js option
```

### Complete File Structure for a Custom View Type

```
my_sitepackage/
├── Configuration/
│   ├── Icons.php                          # Custom icon registration (optional)
│   ├── JavaScriptModules.php              # ES module paths (only if using js)
│   └── TsConfig/Page/
│       └── mod.tsconfig                   # View type TSconfig
├── Resources/
│   ├── Private/Backend/
│   │   ├── Templates/
│   │   │   └── KanbanView.html            # Main Fluid template
│   │   └── Partials/
│   │       └── KanbanCard.html            # Card partial (optional)
│   └── Public/
│       ├── Css/
│       │   └── kanban.css                 # View-specific styles
│       ├── JavaScript/
│       │   └── kanban-board.js            # Custom JS module (optional)
│       └── Icons/
│           └── kanban.svg                 # Custom icon (optional)
```

## Method 2: PSR-14 Event (for extensions)

```php
use TYPO3\CMS\Core\Attribute\AsEventListener;
use Webconsulting\RecordsListTypes\Event\RegisterViewModesEvent;

#[AsEventListener]
final class RegisterCustomViewListener
{
    public function __invoke(RegisterViewModesEvent $event): void
    {
        $event->addViewMode('kanban', [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:viewMode.kanban',
            'icon' => 'actions-view-table-columns',
            'description' => 'Kanban board view',
            'template' => 'KanbanView',
            'css' => 'EXT:my_extension/Resources/Public/Css/kanban.css',
        ]);
    }
}
```

Templates and CSS work exactly the same way as with TSconfig registration.
