---
name: "typo3-datahandler"
description: "Guides transactional TYPO3 record manipulation with DataHandler, including datamaps, cmdmaps, backend user context, reference index handling, workspace-aware operations, hooks, and PSR-14 events. Use when creating, updating, moving, localizing, deleting, or extending TYPO3 records, pages, content, categories, IRRE children, or backend data operations."
compatibility: "TYPO3 14.x"
metadata:
  version: "2.1.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 DataHandler Operations

> Source: https://github.com/dirnbauer/webconsulting-skills

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
2. Call `start($dataMap, $commandMap[, $backendUser[, $referenceIndexUpdater]])` **before** any `process_*` call. The 4th parameter exists but is `@internal`; extension code should normally use only the first 2-3 arguments.
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

        if ($dataHandler->errorLog !== []) {
            throw new \RuntimeException(
                'DataHandler error: ' . implode(', ', $dataHandler->errorLog),
                1700000001
            );
        }
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


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
