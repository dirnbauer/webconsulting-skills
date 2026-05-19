# v14-Only Changes

Continues `typo3-datahandler` from [full guide](full-guide.md).

## v14-Only Changes

> The following DataHandler changes apply **exclusively to TYPO3 v14**.

### Removed Properties **[v14 only]**

- **`DataHandler->userid`** and **`DataHandler->admin`** properties removed (#107848). The DataHandler now uses the backend user from `$GLOBALS['BE_USER']` directly. Do not set these properties.
- **`DataHandler->storeLogMessages`** removed (#106118). Logging behavior is no longer configurable via this property.
- **`DataHandler->copyWhichTables`**, **`DataHandler->neverHideAtCopy`**, **`DataHandler->copyTree`** removed (#107856). These internal properties are no longer accessible.

### New `discard` cmdmap command **[v14 only]**

[Feature #107519](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107519-AddDiscardCommandToDataHandler.html) adds a **first-class `discard` command** on the **cmdmap** so you can drop workspace versions without the old `version` + `clearWSID` / `flush` workaround. Internal discard-related logic existed in Core before v14; what is **new** is this explicit public cmdmap API. Use the **versioned** record UID (`t3ver_wsid` > 0), not the live record.

The legacy `version` actions remain supported but are considered **deprecated in the changelog sense** in favor of `discard`. TYPO3 v14 does **not** emit a dedicated runtime deprecation notice for them.

```php
$cmd = [
    'tt_content' => [
        $versionedUid => ['discard' => true],
    ],
];
```

### ISO8601 Date Handling **[v14 only]**

DataHandler now accepts both qualified (`2026-03-09T12:00:00+01:00`) and unqualified (`2026-03-09T12:00:00`) ISO8601 date strings for datetime fields (#105549).

### Record API in List/Page Modules **[v14 only]**

The List Module and Page Module now use the **Record API** (#107356, #92434) instead of raw array data for rendering. Custom preview renderers and record transformations must adapt to `Record` objects.

### Reference Index Check Moved **[v14 only]**

The Reference Index check has been moved to the **Install Tool** (#107629). The previous backend module approach is no longer available.

---
