---
name: typo3-datahandler-php84
description: PHP 8.4 patterns for TYPO3 DataHandler operations. Property hooks for commands, typed arrays, and modern service patterns.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-datahandler
  - php-modernization
triggers:
  - datahandler php 8.4
  - datahandler property hooks
  - datahandler typed
---

# DataHandler with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
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
            $allowed = ['text', 'textmedia', 'html', 'header'];
            if (!in_array($value, $allowed, true)) {
                throw new \InvalidArgumentException('Invalid CType: ' . $value);
            }
            $this->cType = $value;
        }
    }

    public string $header = '';
    public string $bodytext = '';

    // Virtual property for DataHandler data array
    public array $dataMap {
        get => [
            'tt_content' => [
                'NEW_' . uniqid() => [
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
        private readonly DataHandler $dataHandler,
    ) {}

    public function createContent(CreateContentCommand $command): int
    {
        $this->dataHandler->start($command->dataMap, []);
        $this->dataHandler->process_datamap();

        if ($this->dataHandler->errorLog !== []) {
            throw new \RuntimeException(
                'DataHandler errors: ' . implode(', ', $this->dataHandler->errorLog)
            );
        }

        return (int) current($this->dataHandler->substNEWwithIDs);
    }
}
```

---

## 2. Asymmetric Visibility for DataHandler Results

### Result Object with Read-Only Public Access

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\DataHandler;

final class DataHandlerResult
{
    /** @var array<string, int> */
    public private(set) array $createdRecords = [];

    /** @var array<string> */
    public private(set) array $errors = [];

    public private(set) bool $success = true;

    public function addCreatedRecord(string $table, int $uid): void
    {
        $this->createdRecords[$table] = $uid;
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
        private readonly DataHandler $dataHandler,
    ) {}

    public function processDataMap(array $data): DataHandlerResult
    {
        $result = new DataHandlerResult();

        $this->dataHandler->start($data, []);
        $this->dataHandler->process_datamap();

        foreach ($this->dataHandler->substNEWwithIDs as $newId => $uid) {
            $table = $this->extractTableFromNewId($newId);
            $result->addCreatedRecord($table, (int) $uid);
        }

        foreach ($this->dataHandler->errorLog as $error) {
            $result->addError($error);
        }

        return $result;
    }

    private function extractTableFromNewId(string $newId): string
    {
        // Logic to extract table name
        return 'tt_content';
    }
}

// Usage
$result = $recordService->processDataMap($data);

echo $result->success;        // ✅ Readable
echo $result->createdRecords; // ✅ Readable
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
            // Check if any record is missing required fields
            $missingPid = array_any(
                $records,
                fn(array $fields) => !isset($fields['pid']) && str_starts_with((string) key($records), 'NEW')
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

final class LegacyContentService
{
    #[\Deprecated(
        message: 'Use ContentService::createContent() with CreateContentCommand instead',
        since: '2.0.0'
    )]
    public function createContentArray(array $data): int
    {
        trigger_error(
            'createContentArray() is deprecated, use createContent() with typed command',
            E_USER_DEPRECATED
        );

        $dataHandler = new DataHandler();
        $dataHandler->start(['tt_content' => ['NEW_1' => $data]], []);
        $dataHandler->process_datamap();

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

        return (int) ($dataHandler->substNEWwithIDs['NEW_1'] ?? 0);
    }
}

final readonly class DataHandlerFactory
{
    public function create(): DataHandler
    {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->bypassAccessCheckForRecords = false;
        return $dataHandler;
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
- [ ] Use `readonly` services where DataHandler is injected

---

## References

- [typo3-datahandler SKILL.md](./SKILL.md) - Main DataHandler guide
- [php-modernization SKILL-PHP84.md](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features
- [TYPO3 DataHandler Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Typo3CoreEngine/Database/Index.html)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
