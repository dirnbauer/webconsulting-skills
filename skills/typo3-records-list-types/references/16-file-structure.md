# 16. File Structure

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 16. File Structure

```
records_list_types/
├── Classes/
│   ├── Constants.php
│   ├── Controller/
│   │   ├── Ajax/ViewModeController.php        # AJAX preference persistence
│   │   └── RecordListController.php           # Main controller (XClass)
│   ├── Event/
│   │   └── RegisterViewModesEvent.php         # PSR-14: custom view registration
│   ├── EventListener/
│   │   ├── GridViewButtonBarListener.php      # Injects toggle buttons
│   │   ├── GridViewQueryListener.php          # Query modification bridge
│   │   └── GridViewRecordActionsListener.php  # Record action collection
│   ├── Pagination/
│   │   └── DatabasePaginator.php              # Paginator for pre-fetched records
│   ├── Service/
│   │   ├── GridConfigurationService.php       # TSconfig parsing
│   │   ├── MiddlewareDiagnosticService.php    # Middleware diagnostics
│   │   ├── RecordGridDataProvider.php         # Record fetching & enrichment
│   │   ├── ThumbnailService.php               # FAL image processing
│   │   ├── ViewModeResolver.php               # View mode determination
│   │   └── ViewTypeRegistry.php               # View type management
│   └── ViewHelpers/
│       └── RecordActionsViewHelper.php        # Record actions rendering
├── Configuration/
│   ├── Backend/AjaxRoutes.php
│   ├── Icons.php
│   ├── JavaScriptModules.php
│   ├── page.tsconfig
│   └── Services.yaml
├── Documentation/
├── Resources/
│   ├── Private/
│   │   ├── Language/ (en, de)
│   │   ├── Layouts/
│   │   ├── Partials/ (Card, CompactRow, Pagination, RecordActions, SortingDropdown, TeaserCard, ViewSwitcher)
│   │   └── Templates/ (CompactView, GenericView, GridView, TeaserView)
│   └── Public/
│       ├── Css/ (base, grid-view, compact-view, teaser-view, view-mode-toggle)
│       ├── Icons/
│       └── JavaScript/ (GridViewActions, view-switcher)
├── Tests/ (Unit, Functional, Architecture)
├── composer.json
├── ext_emconf.php
└── ext_localconf.php
```
