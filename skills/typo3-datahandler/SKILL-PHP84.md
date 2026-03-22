---
name: typo3-datahandler-php84
description: PHP 8.4 patterns for TYPO3 DataHandler operations. Property hooks for commands, typed arrays, and modern service patterns.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "14.x"
related_skills:
  - typo3-datahandler
  - php-modernization
triggers:
  - datahandler php 8.4
  - datahandler property hooks
  - datahandler typed
---

# DataHandler with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v14.x
> 
> **Related Skills:** 
> - [typo3-datahandler](./SKILL.md) - Main DataHandler guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

This skill covers PHP 8.4 specific patterns for DataHandler operations.

---

## 1. Property Hooks for Command Objects

### DataHandler Command DTO with Validation

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\DataHandler;

final class CreateContentCommand
{
    public int $pid {
        set (int $value) {
            if ($value < 0) {
                throw new \InvalidArgumentException('PID must be positive');
            }
            $this->pid = $value;
        }
    }

    public string $cType {
        set (string $value) {
            // Example allowlist only — extend with your Content Block CTypes (e.g. myvendor_hero) or validate via ContentBlockRegistry.
            $allowed = ['text', 'textmedia', 'html', 'header'];
            if (!in_array($value, $allowed, true)) {
                throw new \InvalidArgumentException('Invalid CType: ' . $value);
            }
            $this->cType = $value;
        }
    }

    public string $header = '';
    public string $bodytext = '';

    /**
     * Build a datamap for one new tt_content row. Use a stable placeholder id (e.g. NEW_1)
     * per DataHandler::start() call — never regenerate the key on each property read.
     */
    public function toDataMap(string $newId = 'NEW_1'): array
    {
        return [
            'tt_content' => [
                $newId => [
                    'pid' => $this->pid,
                    'CType' => $this->cType,
                    'header' => $this->header,
                    'bodytext' => $this->bodytext,
                ],
            ],
        ];
    }
}
```

### Using the Command

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use Vendor\MyExtension\DataHandler\CreateContentCommand;

final class ContentService
{
    public function __construct(
        private readonly DataHandlerFactory $dataHandlerFactory,
    ) {}

    public function createContent(CreateContentCommand $command, string $newId = 'NEW_1'): int
    {
        $dataHandler = $this->dataHandlerFactory->create();
        $dataHandler->start($command->toDataMap($newId), []);
        $dataHandler->process_datamap();

        if ($dataHandler->errorLog !== []) {
            throw new \RuntimeException(
                'DataHandler errors: ' . implode(', ', $dataHandler->errorLog)
            );
        }

        return (int) ($dataHandler->substNEWwithIDs[$newId] ?? 0);
    }
}
```

Use the `DataHandlerFactory` from **section 5** (`readonly` + `GeneralUtility::makeInstance`) so each operation gets a clean `DataHandler` instance.

---

## 2. Asymmetric Visibility for DataHandler Results

### Result Object with Read-Only Public Access

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\DataHandler;

final class DataHandlerResult
{
    /**
     * Created record UIDs per table (a table may have multiple NEW_* placeholders in one run).
     *
     * @var array<string, list<int>>
     */
    public private(set) array $createdRecords = [];

    /** @var array<string> */
    public private(set) array $errors = [];

    public private(set) bool $success = true;

    public function addCreatedRecord(string $table, int $uid): void
    {
        $this->createdRecords[$table][] = $uid;
    }

    public function addError(string $error): void
    {
        $this->errors[] = $error;
        $this->success = false;
    }
}
```

### Service Using Result Object

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use Vendor\MyExtension\DataHandler\DataHandlerResult;

final class RecordService
{
    public function __construct(
        private readonly DataHandlerFactory $dataHandlerFactory,
    ) {}

    public function processDataMap(array $data): DataHandlerResult
    {
        $result = new DataHandlerResult();
        $dataHandler = $this->dataHandlerFactory->create();

        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        foreach ($dataHandler->substNEWwithIDs as $newId => $uid) {
            $table = $this->resolveTableForNewId($data, $newId);
            if ($table !== null) {
                $result->addCreatedRecord($table, (int) $uid);
            }
        }

        foreach ($dataHandler->errorLog as $error) {
            $result->addError($error);
        }

        return $result;
    }

    /**
     * Match placeholder id (e.g. NEW_1) to the table key from the submitted $data map.
     */
    private function resolveTableForNewId(array $data, string $newId): ?string
    {
        foreach ($data as $table => $records) {
            if (!is_array($records)) {
                continue;
            }
            if (array_key_exists($newId, $records)) {
                return (string) $table;
            }
        }

        return null;
    }
}

// Usage
$result = $recordService->processDataMap($data);

echo $result->success;        // ✅ Readable
print_r($result->createdRecords); // ✅ Readable nested array output
$result->success = false;     // ❌ Error: Cannot modify
```

---

## 3. New Array Functions for DataHandler Operations

### Finding Records with array_find()

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\Database\ConnectionPool;

final class ContentFinder
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    /**
     * @return array<string, mixed>|null
     */
    public function findFirstPublishedContent(int $pid): ?array
    {
        $records = $this->connectionPool
            ->getConnectionForTable('tt_content')
            ->select(
                ['*'],
                'tt_content',
                ['pid' => $pid, 'deleted' => 0]
            )
            ->fetchAllAssociative();

        // PHP 8.4: Find first non-hidden record
        return array_find($records, fn(array $r) => $r['hidden'] === 0);
    }

    /**
     * @param array<int, array<string, mixed>> $records
     */
    public function hasAnyDraftContent(array $records): bool
    {
        return array_any($records, fn(array $r) => ($r['t3ver_state'] ?? 0) > 0);
    }

    /**
     * @param array<int, array<string, mixed>> $records
     */
    public function allHaveRequiredFields(array $records): bool
    {
        return array_all($records, fn(array $r) => 
            $r['header'] !== '' && $r['pid'] > 0
        );
    }
}
```

### Validating DataMap Entries

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Validator;

final class DataMapValidator
{
    /**
     * @param array<string, array<string|int, array<string, mixed>>> $dataMap
     */
    public function validate(array $dataMap): ValidationResult
    {
        $result = new ValidationResult();

        foreach ($dataMap as $table => $records) {
            // Check if any NEW_* row is missing pid (array_any passes value, key per PHP 8.4)
            $missingPid = array_any(
                $records,
                fn(array $fields, string|int $recordKey): bool =>
                    !isset($fields['pid'])
                    && is_string($recordKey)
                    && str_starts_with($recordKey, 'NEW')
            );

            if ($missingPid) {
                $result->addError("Table '$table' has NEW records without PID");
            }

            // Check if all records have valid structure
            $allValid = array_all(
                $records,
                fn(array $fields) => is_array($fields) && $fields !== []
            );

            if (!$allValid) {
                $result->addError("Table '$table' has invalid record structure");
            }
        }

        return $result;
    }
}
```

---

## 4. #[\Deprecated] for Legacy DataHandler Patterns

### Deprecating Legacy Methods

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use Vendor\MyExtension\DataHandler\CreateContentCommand;

final class LegacyContentService
{
    #[\Deprecated(
        message: 'Use ContentService::createContent() with CreateContentCommand instead',
        since: '2.0.0'
    )]
    public function createContentArray(array $data): int
    {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start(['tt_content' => ['NEW_1' => $data]], []);
        $dataHandler->process_datamap();

        if ($dataHandler->errorLog !== []) {
            throw new \RuntimeException(
                'DataHandler error: ' . implode(', ', $dataHandler->errorLog),
                1700000001
            );
        }

        return (int) ($dataHandler->substNEWwithIDs['NEW_1'] ?? 0);
    }

    /**
     * Modern replacement
     */
    public function createContent(CreateContentCommand $command): int
    {
        // Type-safe implementation
    }
}
```

---

## 5. Readonly Services with DataHandler

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final readonly class ImmutableRecordService
{
    public function __construct(
        private DataHandlerFactory $dataHandlerFactory,
    ) {}

    public function createRecord(string $table, array $data): int
    {
        // Create fresh DataHandler instance for each operation
        $dataHandler = $this->dataHandlerFactory->create();

        $dataMap = [
            $table => [
                'NEW_1' => $data,
            ],
        ];

        $dataHandler->start($dataMap, []);
        $dataHandler->process_datamap();

        if ($dataHandler->errorLog !== []) {
            throw new \RuntimeException(
                'DataHandler error: ' . implode(', ', $dataHandler->errorLog),
                1700000001
            );
        }

        return (int) ($dataHandler->substNEWwithIDs['NEW_1'] ?? 0);
    }
}

final readonly class DataHandlerFactory
{
    public function create(): DataHandler
    {
        // Fresh instance per operation — DataHandler keeps submission state on the object.
        return GeneralUtility::makeInstance(DataHandler::class);
    }
}
```

---

## 6. Migration Checklist

### Upgrading DataHandler Code to PHP 8.4

- [ ] Replace array-based commands with typed Command DTOs
- [ ] Add property hooks for validation in command objects
- [ ] Use asymmetric visibility for result objects
- [ ] Replace manual array loops with `array_find()`, `array_any()`, `array_all()`
- [ ] Add `#[\Deprecated]` to legacy helper methods
- [ ] Prefer a small `DataHandlerFactory` (or `GeneralUtility::makeInstance` per call) instead of injecting a shared `DataHandler` singleton

---

## References

- [typo3-datahandler SKILL.md](./SKILL.md) - Main DataHandler guide
- [php-modernization SKILL-PHP84.md](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features
- [TYPO3 DataHandler Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/DataHandler/Database/Index.html)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
