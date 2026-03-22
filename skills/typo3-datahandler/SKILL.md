---
name: typo3-datahandler
description: >-
  Expert guidance on manipulating TYPO3 records via the DataHandler, ensuring
  transactional safety, correct extension points (SC_OPTIONS hooks and documented
  PSR-14 events), and reference index integrity. Use when working with database,
  datahandler, tcemain, records, content, pages.
compatibility: TYPO3 14.x
metadata:
  version: "2.1.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 DataHandler Operations

> **Compatibility:** TYPO3 v14.x
> All code examples in this skill are designed to work on TYPO3 v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## 1. The Prime Directive

**NEVER** use raw SQL (`INSERT`, `UPDATE`, `DELETE`) for `pages`, `tt_content`, or any TCA-configured table.

You **MUST** use the `DataHandler` to ensure:

- Reference Index updates (`sys_refindex`)
- Cache clearing
- Version history (`sys_history`)
- Workspace compatibility
- Correct hook/event integration where Core defines it (see §9)
- FlexForm handling
- MM relation management

### Exceptions (Raw SQL Allowed)

- Custom logging tables without TCA
- Bulk analytics/reporting queries (read-only)
- Migration scripts with explicit reference index rebuild

## 2. Structure of Arrays

### The DataMap ($data)

Used for **creating** or **updating** records.

**Syntax:** `$data[tableName][uid][fieldName] = value`

**Creating a New Record:**

Use a unique string starting with `NEW` as the UID:

```php
<?php
declare(strict_types=1);

$data = [
    'tt_content' => [
        'NEW_1' => [
            'pid' => 1,
            'CType' => 'text',
            'header' => 'My New Content Element',
            'bodytext' => '<p>Content goes here</p>',
            'sys_language_uid' => 0,
        ],
    ],
];
```

**Updating an Existing Record:**

Use the numeric UID:

```php
<?php
declare(strict_types=1);

$data = [
    'tt_content' => [
        123 => [
            'header' => 'Updated Header',
            'hidden' => 0,
        ],
    ],
];
```

**Referencing NEW Records:**

```php
<?php
declare(strict_types=1);

$data = [
    'pages' => [
        'NEW_page' => [
            'pid' => 1,
            'title' => 'New Page',
        ],
    ],
    'tt_content' => [
        'NEW_content' => [
            'pid' => 'NEW_page', // References the new page
            'CType' => 'text',
            'header' => 'Content on new page',
        ],
    ],
];
```

### The CmdMap ($cmd)

Used for **moving**, **copying**, **deleting**, or **undeleting** records.

**Syntax:** `$cmd[tableName][uid][command] = value`

**Delete a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => ['delete' => 1],
    ],
];
```

**Move a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => ['move' => 456], // Target page UID; use negative UID to place after record
    ],
];
```

**Copy a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => ['copy' => 1], // Target page UID
    ],
];
```

**Localize a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => [
            'localize' => 1, // Target language UID
        ],
    ],
];
```

## 3. Execution Pattern

TYPO3's public DataHandler API for TYPO3 v14 is simply:

1. Obtain a `DataHandler` via **`GeneralUtility::makeInstance(DataHandler::class)`** or **constructor DI** — avoid `new DataHandler()` so Core wiring (hooks, collaborators) stays consistent.
2. Call `start($data, $cmd[, $backendUser[, $referenceIndexUpdater]])` **before** any `process_*` call. The 4th parameter exists but is `@internal`; extension code should normally use only the first 2-3 arguments.
3. Call `process_datamap()` and / or `process_cmdmap()`
4. Inspect **`$dataHandler->errorLog`**, verify expected keys in **`$dataHandler->substNEWwithIDs`** for new records, and (in workspaces) review **`$dataHandler->autoVersionIdMap`** when you expect version rows.

**Cache:** Prefer `CacheManager` / cache groups or PSR-14 cache events instead of legacy DataHandler cache helpers.

The official docs do **not** define a general transaction contract for DataHandler. In normal extension code, use the plain API first and only add your own transaction handling after carefully validating the database connections and side effects involved in your specific use case.

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ContentService
{
    public function createOrUpdateContent(array $data, array $cmd = []): array
    {
        /** @var DataHandler $dataHandler */
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, $cmd);

        if ($data !== []) {
            $dataHandler->process_datamap();
        }

        if ($cmd !== []) {
            $dataHandler->process_cmdmap();
        }

        if ($dataHandler->errorLog !== []) {
            throw new \RuntimeException(
                'DataHandler error: ' . implode(', ', $dataHandler->errorLog),
                1700000001
            );
        }

        return $dataHandler->substNEWwithIDs;
    }
}
```

## 4. Backend Context

DataHandler requires a valid **backend user context**. It does **not** require you to manually fake admin mode by mutating `$GLOBALS['BE_USER']->user`.

- In **CLI / scheduler** contexts, initialize backend authentication before using DataHandler
- TYPO3 commands use the `_cli_` backend user
- If you need another backend user, pass a proper `BackendUserAuthentication` object as the **third** argument to `start()`
- Use permission checks and a real backend user object instead of manually setting `$GLOBALS['BE_USER']->user['admin'] = 1`

### CLI Command Setup (TYPO3 v14)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use TYPO3\CMS\Core\Core\Bootstrap;

#[AsCommand(
    name: 'myext:import',
    description: 'Import data using DataHandler',
)]
final class ImportCommand extends Command
{
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        Bootstrap::initializeBackendAuthentication();

        // Your DataHandler logic here...

        return Command::SUCCESS;
    }
}
```

### Using an Alternative Backend User

```php
<?php
declare(strict_types=1);

use TYPO3\CMS\Core\Authentication\BackendUserAuthentication;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ImportService
{
    public function runAsUser(
        array $data,
        array $cmd,
        BackendUserAuthentication $backendUser
    ): void {
        /** @var DataHandler $dataHandler */
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, $cmd, $backendUser);
        $dataHandler->process_datamap();
        $dataHandler->process_cmdmap();
    }
}
```

## 5. Reference Index Handling

For **normal DataHandler writes**, TYPO3 keeps the Reference Index in sync automatically. You usually **do not** need to call `ReferenceIndex` manually after ordinary `process_datamap()` / `process_cmdmap()` usage.

Manual Reference Index updates are primarily relevant for:

- Deployments and TYPO3 upgrades
- Changes to TCA-defined relations
- Migrations or scripts that bypass DataHandler
- Repair / maintenance scenarios

### Rebuild the full Reference Index

```bash
vendor/bin/typo3 referenceindex:update
```

### Update a specific record manually (rare)

```php
<?php
declare(strict_types=1);

use TYPO3\CMS\Core\Database\ReferenceIndex;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$referenceIndex = GeneralUtility::makeInstance(ReferenceIndex::class);
$referenceIndex->updateRefIndexTable('tt_content', 123);
```

## 6. Common Pitfalls

### Pitfall 1: Missing PID for New Records

```php
// ❌ WRONG - Missing pid
$data = ['tt_content' => ['NEW_1' => ['header' => 'Test']]];

// ✅ CORRECT - Always include pid
$data = ['tt_content' => ['NEW_1' => ['pid' => 1, 'header' => 'Test']]];
```

### Pitfall 2: Assuming String vs Integer UIDs Matter (Usually They Do Not)

DataHandler uses `MathUtility::canBeInterpretedAsInteger()` for many UID checks. A **numeric string** such as `'123'` is treated like `123` for typical existing-record keys.

```php
// Both are valid for UID 123 in common cases
$data = ['tt_content' => [123 => ['header' => 'Int key']]];
$data = ['tt_content' => ['123' => ['header' => 'String key']]];

// ✅ Prefer integer keys for clarity and static analysis
$data = ['tt_content' => [123 => ['header' => 'Recommended style']]];
```

**Still wrong:** using non-numeric strings as placeholders **without** the `NEW` prefix (e.g. arbitrary slugs instead of `NEW_1`). New records must use `NEW…` placeholders as shown in §2. **Edge case:** strings that are not valid integer strings per `MathUtility::canBeInterpretedAsInteger()` (e.g. some leading-zero forms) — use integers or plain digit strings.

### Pitfall 3: Forgetting process_datamap() / process_cmdmap()

```php
// ❌ WRONG - Nothing happens
$dataHandler->start($data, $cmd);

// ✅ CORRECT - Actually process the data
$dataHandler->start($data, $cmd);
$dataHandler->process_datamap();
$dataHandler->process_cmdmap();
```

### Pitfall 4: Ignoring Error Log

```php
// ❌ WRONG - Silently ignoring errors
$dataHandler->process_datamap();

// ✅ CORRECT - Check for errors
$dataHandler->process_datamap();
if (!empty($dataHandler->errorLog)) {
    // Handle errors appropriately
    throw new \RuntimeException(implode(', ', $dataHandler->errorLog));
}
```

## 7. Retrieving New Record UIDs

After processing, get the real UIDs for NEW records:

```php
<?php
declare(strict_types=1);

$dataHandler->process_datamap();

// Get the real UID for 'NEW_1'
$newContentUid = $dataHandler->substNEWwithIDs['NEW_1'] ?? null;

if ($newContentUid === null) {
    throw new \RuntimeException('Failed to create content element');
}
```

## 8. Workspace-Aware Operations

When working with workspaces:

```php
<?php
declare(strict_types=1);

// Check if we're in a workspace
$workspaceId = $GLOBALS['BE_USER']->workspace;

if ($workspaceId > 0) {
    // In workspace - DataHandler will create versioned records
    // Use the wsol (workspace overlay) for reading
}

// Force live workspace for specific operations
$previousWorkspace = $GLOBALS['BE_USER']->workspace;
$GLOBALS['BE_USER']->setWorkspace(0);

// ... perform operations ...

$GLOBALS['BE_USER']->setWorkspace($previousWorkspace);
```

## 9. Extending DataHandler: Hooks and Real Core Events

> **Facts for TYPO3 v14:** TYPO3 Core does **not** ship PSR-14 events named like `BeforeRecordOperationEvent`, `AfterDatabaseOperationsEvent`, or `ModifyRecordBeforeInsertEvent`. Those names are not part of Core. To run code **after** datamap DB writes, use **`SC_OPTIONS` hook classes** (below). Always confirm APIs in [TYPO3 Explained — Events (DataHandling)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/DataHandling/Index.html) and [`\TYPO3\CMS\Core\DataHandling\Event`](https://api.typo3.org/main/namespaces/typo3-cms-core-datahandling-event.html).

### 9.1 `SC_OPTIONS` hook classes (primary pattern for datamap/cmdmap)

Register classes on `t3lib/class.t3lib_tcemain.php` — e.g. `processDatamapClass` / `processCmdmapClass`. Core still invokes these on **TYPO3 v14**; they are the supported extension point for many DataHandler reactions.

`ext_localconf.php`:

```php
<?php
declare(strict_types=1);

$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
    = \Vendor\Extension\Hooks\DataHandlerHook::class;

$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processCmdmapClass'][]
    = \Vendor\Extension\Hooks\DataHandlerHook::class;
```

Hook class (after database operations on the datamap — same signature Core calls):

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

## 10. Version Constraints for Extensions

When creating extensions that use DataHandler, ensure proper version constraints:

```php
<?php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '1.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '14.0.0-14.99.99',
            'php' => '8.2.0-8.4.99',
        ],
    ],
];
```

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

## Credits & Attribution


Source: https://github.com/dirnbauer/webconsulting-skills
Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.
