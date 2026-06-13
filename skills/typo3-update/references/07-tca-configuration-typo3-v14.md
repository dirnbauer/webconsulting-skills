# 7. TCA Configuration (TYPO3 v14)

Continues `typo3-update` from [full guide](full-guide.md).

## 7. TCA Configuration (TYPO3 v14)

### Static TCA Only

In v14, runtime TCA modifications are forbidden. Always use static files:

```php
<?php
// Configuration/TCA/tx_myext_domain_model_item.php
return [
    'ctrl' => [
        'title' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item',
        'label' => 'title',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        // v14: ctrl `searchFields` removed (Breaking #106972) — mark searchable columns in `columns` instead.
        'iconIdentifier' => 'myextension-item',
    ],
    'palettes' => [
        'visibility' => [
            'showitem' => 'hidden',
        ],
        'access' => [
            'showitem' => 'starttime, endtime',
        ],
    ],
    'types' => [
        '1' => [
            'showitem' => '
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
                    title, description,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
                    --palette--;;visibility,
                    --palette--;;access,
            ',
        ],
    ],
    'columns' => [
        'title' => [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item.title',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'description' => [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item.description',
            'config' => [
                'type' => 'text',
                'cols' => 40,
                'rows' => 5,
                'enableRichtext' => true,
                // All suitable fields are searchable by default in v14 —
                // set 'searchable' => false to EXCLUDE a field from backend search.
                'searchable' => false,
            ],
        ],
    ],
];
```

> **`searchable` in v14:** `ctrl.searchFields` was removed (#106972). All suitable fields are now searchable by default, so there is no opt-in `'searchable' => true`. The key is only used as `'searchable' => false` on the few columns you want to **exclude** from backend search (e.g. large richtext bodies or technical/identifier fields).

### Auto-Created Columns from ctrl

Since **TYPO3 v13.3+**, column definitions for fields referenced in `ctrl` are **auto-created** by the Core. You no longer need explicit `'columns'` entries for:

- `enablecolumns` fields: `hidden`/`disabled`, `starttime`, `endtime`, `fe_group`
- Language fields: `sys_language_uid`, `l10n_parent`, `l10n_diffsource`
- `editlock`, `description` (if set as `descriptionColumn`)

**Convention fields don't need `ext_tables.sql`** -- all fields referenced by `ctrl` properties (`deleted`, `hidden`, `starttime`, `endtime`, `fe_group`, `sorting`, `tstamp`, `crdate`, `sys_language_uid`, `l10n_parent`, `l10n_diffsource`) are added to the database automatically. Defining them in `ext_tables.sql` may cause problems.

**Fields that never need `columns` definitions:**
- `deleted` -- handled by DataHandler, not shown in forms
- `tstamp`, `crdate`, `t3_origuid` -- managed by DataHandler, never displayed
- `sorting` -- managed by DataHandler, should NOT be in `columns`

**Still required:**
- The `ctrl` properties themselves (`tstamp`, `crdate`, `delete`, `enablecolumns`, etc.)
- References in `showitem` / palettes (auto-created columns must still be added to types manually)
- Use dedicated palettes: `visibility` for `hidden`, `access` for `starttime, endtime`
- Your own custom column definitions

**Override auto-created columns** in `Configuration/TCA/Overrides/` if needed:

```php
<?php
// Configuration/TCA/Overrides/pages.php
// New pages are disabled by default
$GLOBALS['TCA']['pages']['columns']['disabled']['config']['default'] = 1;
```

> **Important:** Auto-creation only works for `ctrl` properties in base `Configuration/TCA/` files, NOT in `Configuration/TCA/Overrides/`.
>
> See: [Common fields](https://docs.typo3.org/permalink/t3tca:fields-for-datahandler) | [Auto-created columns](https://docs.typo3.org/m/typo3/reference-tca/main/en-us/Ctrl/AutoCreatedColumns.html)

### TCA Overrides

```php
<?php
// Configuration/TCA/Overrides/tt_content.php
defined('TYPO3') or die();

\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTcaSelectItem(
    'tt_content',
    'CType',
    [
        'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:ctype.title',
        'value' => 'myextension_element',
        'icon' => 'content-text',
        'group' => 'default',
    ]
);

$GLOBALS['TCA']['tt_content']['types']['myextension_element'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            bodytext,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
    ',
];
```
