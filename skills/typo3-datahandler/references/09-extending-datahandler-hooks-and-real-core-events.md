# 9. Extending DataHandler: Hooks and Real Core Events

Continues `typo3-datahandler` from [full guide](full-guide.md).

## 9. Extending DataHandler: Hooks and Real Core Events

> **Facts for TYPO3 v14:** TYPO3 Core does **not** ship PSR-14 events named like `BeforeRecordOperationEvent`, `AfterDatabaseOperationsEvent`, or `ModifyRecordBeforeInsertEvent`. Those names are not part of Core. For datamap/cmdmap extension points beyond documented PSR-14 events, use **`SC_OPTIONS` hook classes** (below). Those hooks expose callbacks throughout the lifecycle (`*_beforeStart`, `*_preProcess`, `*_postProcess`, `*_afterDatabaseOperations`, `*_afterAllOperations` / `*_afterFinish`, etc.) — not a single “after everything” moment. Always confirm APIs in [TYPO3 Explained — Events (DataHandling)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/DataHandling/Index.html) and [`\TYPO3\CMS\Core\DataHandling\Event`](https://api.typo3.org/main/namespaces/typo3-cms-core-datahandling-event.html).

### 9.1 `SC_OPTIONS` hook classes (primary pattern for datamap/cmdmap)

Register classes on `t3lib/class.t3lib_tcemain.php` — e.g. `processDatamapClass` / `processCmdmapClass`. Core still invokes these on **TYPO3 v14**. Each registration receives **multiple** hook methods over the datamap/cmdmap lifecycle (before start, pre/post process, after DB, after all) — see your hook class naming pattern in Core’s `DataHandler`.

`ext_localconf.php`:

```php
<?php
declare(strict_types=1);

$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
    = \Vendor\Extension\Hooks\DataHandlerHook::class;

$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processCmdmapClass'][]
    = \Vendor\Extension\Hooks\DataHandlerHook::class;
```

Hook class (example: `processDatamap_afterDatabaseOperations` — one of several methods Core may call on the same class):

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Hooks;

use TYPO3\CMS\Core\DataHandling\DataHandler;

final class DataHandlerHook
{
    public function processDatamap_afterDatabaseOperations(
        string $status,
        string $table,
        string|int $id,
        array $fieldArray,
        DataHandler $dataHandler
    ): void {
        if ($table !== 'tt_content') {
            return;
        }

        if ($status === 'new') {
            $newUid = $dataHandler->substNEWwithIDs[$id] ?? $id;
            // …
        }

        if ($status === 'update') {
            // …
        }
    }
}
```

Other keys on the same `SC_OPTIONS` path include `moveRecordClass`, `processTranslateToClass`, `checkModifyAccessList`, `clearPageCacheEval`, `clearCachePostProc`, etc. — inspect `DataHandler` in Core for the full set.

### 9.2 Real PSR-14 events in `TYPO3\CMS\Core\DataHandling\Event`

Core currently documents **only** these events under that namespace (reference index / link parsing — **not** generic “before every save”):

| Event | Purpose |
|-------|---------|
| [`IsTableExcludedFromReferenceIndexEvent`](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/DataHandling/IsTableExcludedFromReferenceIndexEvent.html) | Exclude a table from the Reference Index |
| [`AppendLinkHandlerElementsEvent`](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/DataHandling/AppendLinkHandlerElementsEvent.html) | Extend SoftRef link-handler UI elements |

Example listener (Reference Index exclusion):

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\DataHandling\Event\IsTableExcludedFromReferenceIndexEvent;

#[AsEventListener(identifier: 'vendor-extension/skip-my-cache-table-from-refindex')]
final class ExcludeTableFromReferenceIndexListener
{
    public function __invoke(IsTableExcludedFromReferenceIndexEvent $event): void
    {
        if ($event->getTable() === 'tx_myext_cache') {
            $event->markAsExcluded();
        }
    }
}
```
