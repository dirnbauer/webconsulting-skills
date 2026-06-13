---
id: tca-searchable-not-searchfields
title: "Exclude fields with per-column 'searchable', not ctrl.searchFields"
category: tca
severity: error
appliesTo: ["**/Configuration/TCA/**/*.php", "**/Configuration/TCA/Overrides/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when controlling which fields the backend search includes for a table."
---
# Exclude fields with per-column 'searchable', not ctrl.searchFields

The `ctrl.searchFields` TCA option was removed in v14.0. All fields of suitable types
(input, text, email, link, slug, color, json, flex, datetime without custom dbType) are
searchable by default. To exclude one, set `'searchable' => false` in that field's `config`.

**Do:** add `'searchable' => false` to the columns you want kept out of backend search.
**Don't:** add or keep `'ctrl' => ['searchFields' => '...']` — it is no longer evaluated.

```php
return [
    'ctrl' => [
        // no 'searchFields' here
    ],
    'columns' => [
        'title' => ['config' => ['type' => 'input']],           // searchable by default
        'internal_note' => [
            'config' => ['type' => 'text', 'searchable' => false], // excluded
        ],
    ],
];
```

> Why: `ctrl.searchFields` removed and migrated away at runtime; the per-field
> `searchable` option replaces it (#106972). (Note: EXT:linkvalidator's
> `mod.linkvalidator.searchFields` Page TSconfig is unrelated and unaffected.)
