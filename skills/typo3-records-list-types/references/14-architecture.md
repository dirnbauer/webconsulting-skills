# 14. Architecture

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 14. Architecture

### Services

| Service | Purpose |
|---------|---------|
| `RecordGridDataProvider` | Fetches records with thumbnails, icons, workspace state |
| `GridConfigurationService` | Parses TSconfig for per-table settings |
| `ThumbnailService` | Resolves FAL references, generates thumbnail URLs |
| `ViewModeResolver` | Determines active view from request/preference/TSconfig |
| `ViewTypeRegistry` | Registry for built-in + custom view types |
| `MiddlewareDiagnosticService` | Detects middleware interference with view rendering |

### ViewHelpers

| ViewHelper | Purpose |
|------------|---------|
| `RecordActionsViewHelper` | Renders cached record actions (`<gridview:recordActions>`). Register namespace in Fluid: `xmlns:gridview="http://typo3.org/ns/Webconsulting/RecordsListTypes/ViewHelpers"` (or rely on the extension’s shipped templates). |

### CSS Architecture

```
base.css            ← Always loaded (heading, pagination, sorting)
├── grid-view.css   ← Grid-only: cards, drag-drop, field types
├── compact-view.css← Compact-only: table, sticky columns
├── teaser-view.css ← Teaser-only: teaser cards, badges
└── view-mode-toggle.css ← DocHeader toggle buttons
```

Custom view types automatically receive `base.css`.

### JavaScript Modules

| Module | Purpose |
|--------|---------|
| `GridViewActions.js` | Drag-drop, record actions, sorting, search, pagination, ARIA |
| `HistoryOverlay.js` | Record history overlay in the backend |
| `RecordFilters.js` | Filter controls for record listings |

### AJAX Routes

| Route | Purpose |
|-------|---------|
| `records_list_types_set_view_mode` | Persist user's view mode preference |
| `records_list_types_get_view_mode` | Retrieve current view mode preference |
