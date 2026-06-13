---
id: tca-no-ext-tables-registration
title: "Define TCA in Configuration/TCA; register nothing in ext_tables.php"
category: tca
severity: error
appliesTo: ["**/ext_tables.php", "**/Configuration/TCA/**/*.php", "**/Configuration/TCA/Overrides/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when defining or extending a table's TCA, or editing ext_tables.php."
---
# Define TCA in Configuration/TCA; register nothing in ext_tables.php

Full table definitions go in `Configuration/TCA/<table>.php` (one file per table,
returning the array). Additions to existing tables go in `Configuration/TCA/Overrides/`.
`ext_tables.php` no longer registers tables, modules, or icons in v14 — those moved to
dedicated files (`Configuration/Backend/Modules.php`, `Configuration/Icons.php`).

**Do:** put new-table TCA in `Configuration/TCA/tx_webconexample_item.php`; overrides in `Configuration/TCA/Overrides/`.
**Don't:** assign `$GLOBALS['TCA'][...]`, register modules, or load icons from `ext_tables.php`.

```php
// Configuration/TCA/tx_webconexample_item.php
return [
    'ctrl' => [
        'title' => 'LLL:EXT:webcon_example/Resources/Private/Language/locallang_db.xlf:tx_webconexample_item',
        'label' => 'title',
    ],
    'columns' => [
        'title' => ['label' => 'Title', 'config' => ['type' => 'input']],
    ],
];
```

> Why: TCA is auto-loaded from `Configuration/TCA(/Overrides)`; backend modules and
> icons have their own configuration files (`Configuration/Backend/Modules.php`,
> `Configuration/Icons.php`, verified in core), so `ext_tables.php` registers nothing.
