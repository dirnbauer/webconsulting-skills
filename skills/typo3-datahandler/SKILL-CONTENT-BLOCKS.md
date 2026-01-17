---
name: typo3-datahandler-content-blocks
description: Using DataHandler with Content Blocks records. Creating, updating, and managing Content Blocks-based content programmatically.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-datahandler
  - typo3-content-blocks
triggers:
  - datahandler content blocks
  - create content block record
  - content blocks programmatic
---

# DataHandler with Content Blocks

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-datahandler](./SKILL.md) - Main DataHandler guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development
> - [typo3-content-blocks/SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md) - Migration guide

This skill covers using DataHandler to create and manage Content Blocks records programmatically.

---

## 1. Content Blocks vs Classic: DataHandler Differences

### CType Naming Convention

| Approach | CType Pattern | Example |
|----------|--------------|---------|
| Classic | `extkey_elementname` | `myext_hero` |
| Content Blocks | `vendor_name` | `myvendor_hero` |

### Field Naming Convention

| Approach | Field Pattern | Example |
|----------|--------------|---------|
| Classic | `tx_extkey_fieldname` | `tx_myext_subheadline` |
| Content Blocks (default) | `vendor_name_fieldname` | `myvendor_hero_subheadline` |
| Content Blocks (prefixFields: false) | `fieldname` or custom | `subheadline` |

---

## 2. Creating Content Blocks Elements via DataHandler

### Basic Content Element Creation

Given a Content Block:

```yaml
# ContentBlocks/ContentElements/hero/config.yaml
name: myvendor/hero
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
  - identifier: image
    type: File
    maxitems: 1
  - identifier: cta_link
    type: Link
```

Create via DataHandler:

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ContentBlocksService
{
    public function createHeroElement(
        int $pid,
        string $header,
        string $subheadline,
        string $ctaLink = ''
    ): int {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);

        // Content Blocks CType format: vendor_name
        $data = [
            'tt_content' => [
                'NEW_hero' => [
                    'pid' => $pid,
                    'CType' => 'myvendor_hero',  // Content Blocks CType
                    'header' => $header,
                    // Content Blocks field: vendor_name_fieldname
                    'myvendor_hero_subheadline' => $subheadline,
                    'myvendor_hero_cta_link' => $ctaLink,
                ],
            ],
        ];

        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        return (int) ($dataHandler->substNEWwithIDs['NEW_hero'] ?? 0);
    }
}
```

### With File References

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Resource\FileReference;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ContentBlocksMediaService
{
    public function createHeroWithImage(
        int $pid,
        string $header,
        int $sysFileUid
    ): int {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);

        $data = [
            'tt_content' => [
                'NEW_hero' => [
                    'pid' => $pid,
                    'CType' => 'myvendor_hero',
                    'header' => $header,
                    // File field creates sys_file_reference
                    'myvendor_hero_image' => 'NEW_image',
                ],
            ],
            'sys_file_reference' => [
                'NEW_image' => [
                    'uid_local' => $sysFileUid,
                    'tablenames' => 'tt_content',
                    'fieldname' => 'myvendor_hero_image',
                    'pid' => $pid,
                ],
            ],
        ];

        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        return (int) ($dataHandler->substNEWwithIDs['NEW_hero'] ?? 0);
    }
}
```

---

## 3. Creating Content Blocks Record Types

Given a Record Type:

```yaml
# ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_myvendor_team_member
labelField: name
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: photo
    type: File
    maxitems: 1
```

Create via DataHandler:

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class TeamMemberService
{
    public function createMember(
        int $pid,
        string $name,
        string $position,
        string $email
    ): int {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);

        // Content Blocks Record Type table name from config.yaml
        $data = [
            'tx_myvendor_team_member' => [
                'NEW_member' => [
                    'pid' => $pid,
                    // Fields use identifier directly (no prefix for Record Types)
                    'name' => $name,
                    'position' => $position,
                    'email' => $email,
                ],
            ],
        ];

        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        return (int) ($dataHandler->substNEWwithIDs['NEW_member'] ?? 0);
    }
}
```

---

## 4. Working with Collections (Inline/IRRE)

Given a Content Block with Collection:

```yaml
# ContentBlocks/ContentElements/accordion/config.yaml
name: myvendor/accordion
fields:
  - identifier: items
    type: Collection
    labelField: title
    fields:
      - identifier: title
        type: Text
      - identifier: content
        type: Textarea
        enableRichtext: true
```

Create with inline items:

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class AccordionService
{
    /**
     * @param array<int, array{title: string, content: string}> $items
     */
    public function createAccordion(int $pid, array $items): int
    {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);

        // Build inline items
        $inlineData = [];
        $inlineRefs = [];

        foreach ($items as $index => $item) {
            $newId = 'NEW_item_' . $index;
            $inlineRefs[] = $newId;

            // Collection child table: parenttable_fieldname
            $inlineData['myvendor_accordion_items'][$newId] = [
                'title' => $item['title'],
                'content' => $item['content'],
            ];
        }

        $data = [
            'tt_content' => [
                'NEW_accordion' => [
                    'pid' => $pid,
                    'CType' => 'myvendor_accordion',
                    // Reference inline records
                    'myvendor_accordion_items' => implode(',', $inlineRefs),
                ],
            ],
        ];

        // Merge inline data
        $data = array_merge_recursive($data, $inlineData);

        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        return (int) ($dataHandler->substNEWwithIDs['NEW_accordion'] ?? 0);
    }
}
```

---

## 5. Updating Content Blocks Records

### Update Content Element

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ContentBlocksUpdateService
{
    public function updateHero(int $uid, string $newHeader, string $newSubheadline): void
    {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);

        $data = [
            'tt_content' => [
                $uid => [
                    'header' => $newHeader,
                    'myvendor_hero_subheadline' => $newSubheadline,
                ],
            ],
        ];

        $dataHandler->start($data, []);
        $dataHandler->process_datamap();
    }
}
```

### Update Record Type

```php
<?php

declare(strict_types=1);

public function updateTeamMember(int $uid, array $updates): void
{
    $dataHandler = GeneralUtility::makeInstance(DataHandler::class);

    $data = [
        'tx_myvendor_team_member' => [
            $uid => $updates,
        ],
    ];

    $dataHandler->start($data, []);
    $dataHandler->process_datamap();
}
```

---

## 6. Querying Content Blocks Records

### Finding Content Elements by CType

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Repository;

use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Database\Query\QueryBuilder;

final class ContentBlocksRepository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    /**
     * @return array<int, array<string, mixed>>
     */
    public function findHeroElements(int $pid): array
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tt_content');

        return $queryBuilder
            ->select('*')
            ->from('tt_content')
            ->where(
                $queryBuilder->expr()->eq('pid', $pid),
                $queryBuilder->expr()->eq('CType', $queryBuilder->createNamedParameter('myvendor_hero')),
                $queryBuilder->expr()->eq('deleted', 0)
            )
            ->executeQuery()
            ->fetchAllAssociative();
    }
}
```

### Finding Record Types

```php
<?php

declare(strict_types=1);

/**
 * @return array<int, array<string, mixed>>
 */
public function findTeamMembers(int $pid): array
{
    $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myvendor_team_member');

    return $queryBuilder
        ->select('*')
        ->from('tx_myvendor_team_member')
        ->where(
            $queryBuilder->expr()->eq('pid', $pid),
            $queryBuilder->expr()->eq('deleted', 0)
        )
        ->orderBy('sorting')
        ->executeQuery()
        ->fetchAllAssociative();
}
```

---

## 7. Field Name Reference

### Content Elements (tt_content)

| config.yaml identifier | Database Column | DataHandler Field |
|----------------------|-----------------|-------------------|
| `header` (useExistingField) | `header` | `header` |
| `subheadline` | `myvendor_hero_subheadline` | `myvendor_hero_subheadline` |
| `image` | `myvendor_hero_image` | `myvendor_hero_image` |

### Record Types (custom table)

| config.yaml identifier | Database Column | DataHandler Field |
|----------------------|-----------------|-------------------|
| `name` | `name` | `name` |
| `position` | `position` | `position` |
| `email` | `email` | `email` |

### With prefixFields: false

```yaml
name: myvendor/hero
prefixFields: false
fields:
  - identifier: subheadline
    type: Text
```

| config.yaml identifier | Database Column | DataHandler Field |
|----------------------|-----------------|-------------------|
| `subheadline` | `subheadline` | `subheadline` |

---

## 8. Best Practices

### Use a Dedicated Service Class

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;

final class ContentBlocksRecordService
{
    public function __construct(
        private readonly DataHandler $dataHandler,
    ) {}

    /**
     * Generic method for creating any Content Blocks element
     *
     * @param array<string, mixed> $fields
     */
    public function createContentElement(
        int $pid,
        string $cType,
        array $fields
    ): int {
        $data = [
            'tt_content' => [
                'NEW_1' => array_merge(
                    ['pid' => $pid, 'CType' => $cType],
                    $fields
                ),
            ],
        ];

        $this->dataHandler->start($data, []);
        $this->dataHandler->process_datamap();

        return (int) ($this->dataHandler->substNEWwithIDs['NEW_1'] ?? 0);
    }
}
```

### Validate CType Exists

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\CMS\ContentBlocks\Registry\ContentBlockRegistry;

public function validateCType(string $cType): bool
{
    $registry = GeneralUtility::makeInstance(ContentBlockRegistry::class);

    foreach ($registry->getAll() as $contentBlock) {
        if ($contentBlock->getName() === str_replace('_', '/', $cType)) {
            return true;
        }
    }

    return false;
}
```

---

## 9. Migration: Classic to Content Blocks

When migrating existing DataHandler code from classic extensions to Content Blocks:

### Before (Classic)

```php
$data = [
    'tt_content' => [
        'NEW_1' => [
            'pid' => $pid,
            'CType' => 'myext_hero',
            'tx_myext_subheadline' => $subheadline,
            'tx_myext_image' => $imageRef,
        ],
    ],
];
```

### After (Content Blocks)

```php
$data = [
    'tt_content' => [
        'NEW_1' => [
            'pid' => $pid,
            'CType' => 'myvendor_hero',  // Changed CType
            'myvendor_hero_subheadline' => $subheadline,  // Changed field name
            'myvendor_hero_image' => $imageRef,  // Changed field name
        ],
    ],
];
```

### Using prefixFields: false for Compatibility

If using `prefixFields: false` in Content Blocks config, field names remain unchanged:

```php
// With prefixFields: false, only CType changes
$data = [
    'tt_content' => [
        'NEW_1' => [
            'pid' => $pid,
            'CType' => 'myvendor_hero',
            'tx_myext_subheadline' => $subheadline,  // Same field name
            'tx_myext_image' => $imageRef,
        ],
    ],
];
```

---

## References

- [typo3-datahandler SKILL.md](./SKILL.md) - Main DataHandler guide
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md) - Content Blocks development
- [typo3-content-blocks SKILL-MIGRATION.md](../typo3-content-blocks/SKILL-MIGRATION.md) - Migration guide
- [Content Blocks Documentation](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
