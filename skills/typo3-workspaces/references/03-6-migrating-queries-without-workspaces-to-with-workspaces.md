# 6. Migrating Queries: WITHOUT Workspaces to WITH Workspaces

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 6. Migrating Queries: WITHOUT Workspaces to WITH Workspaces

### Pattern A: Backend QueryBuilder (Before/After)

**BEFORE (no workspace awareness):**

```php
<?php
// WRONG: Does not respect workspaces
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tt_content');
$rows = $queryBuilder
    ->select('*')
    ->from('tt_content')
    ->where(
        $queryBuilder->expr()->eq('pid', $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT))
    )
    ->executeQuery()
    ->fetchAllAssociative();

// Rows may include workspace placeholders and miss workspace versions!
```

**AFTER (workspace-aware):**

```php
<?php

use TYPO3\CMS\Backend\Utility\BackendUtility;
use TYPO3\CMS\Core\Database\Connection;

$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tt_content');
$result = $queryBuilder
    ->select('*')
    ->from('tt_content')
    ->where(
        $queryBuilder->expr()->eq('pid', $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT))
    )
    ->executeQuery();

$rows = [];
while ($row = $result->fetchAssociative()) {
    // Apply workspace overlay
    BackendUtility::workspaceOL('tt_content', $row);
    if (is_array($row)) {
        $rows[] = $row;
    }
}
```

### Pattern B: Frontend with WorkspaceRestriction

**BEFORE (no workspace restriction):**

```php
<?php
// WRONG for frontend: Missing WorkspaceRestriction
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_news_domain_model_news');
$queryBuilder->getRestrictions()->removeAll()->add(
    GeneralUtility::makeInstance(DeletedRestriction::class)
);
```

**AFTER (proper frontend restrictions):**

```php
<?php

use TYPO3\CMS\Core\Database\Query\Restriction\FrontendRestrictionContainer;

// FrontendRestrictionContainer includes:
// - DeletedRestriction
// - WorkspaceRestriction  <-- automatically included!
// - HiddenRestriction
// - StartTimeRestriction
// - EndTimeRestriction
// - FrontendGroupRestriction
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_news_domain_model_news');
$queryBuilder->setRestrictions(
    GeneralUtility::makeInstance(FrontendRestrictionContainer::class)
);
```

### Pattern C: Adding WorkspaceRestriction Manually

```php
<?php

use TYPO3\CMS\Core\Database\Query\Restriction\DeletedRestriction;
use TYPO3\CMS\Core\Database\Query\Restriction\WorkspaceRestriction;
use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$workspaceId = GeneralUtility::makeInstance(Context::class)
    ->getPropertyFromAspect('workspace', 'id', 0);

$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_item');
$queryBuilder->getRestrictions()
    ->removeAll()
    ->add(GeneralUtility::makeInstance(DeletedRestriction::class))
    ->add(GeneralUtility::makeInstance(WorkspaceRestriction::class, $workspaceId));
```

> **Important:** `WorkspaceRestriction` only filters the SQL result to exclude wrong workspace records. You **still must call** `versionOL()` or `workspaceOL()` on each row to get the actual workspace content overlaid.

### Pattern D: Extbase Repository (Mostly Transparent)

Extbase repositories handle workspace overlays **automatically** via the persistence layer. No changes needed for standard `findBy*` methods.

> **CRITICAL: Extbase DataMapper does NOT populate `t3ver_*` system fields.**
> If you add `$t3verWsid`, `$t3verState`, or `$t3verOid` properties to an Extbase domain model, they will **always remain at their default value** (typically `0`). The `t3ver_*` columns are `ctrl` fields in TCA, not `columns` — Extbase's `DataMapFactory` does not create column maps for them.
>
> To inspect workspace state of Extbase model objects, query the database directly via `ConnectionPool`:
>
> ```php
> $row = GeneralUtility::makeInstance(ConnectionPool::class)
>     ->getConnectionForTable('pages')
>     ->select(['t3ver_wsid', 't3ver_state', 't3ver_oid'], 'pages', ['uid' => $post->getUid()])
>     ->fetchAssociative();
> ```

**However**, if you use custom QueryBuilder inside a repository:

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\Domain\Repository;

use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Domain\Repository\PageRepository;
use TYPO3\CMS\Extbase\Persistence\Repository;

final class ItemRepository extends Repository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
        private readonly PageRepository $pageRepository,
    ) {
        parent::__construct();
    }

    /**
     * Custom query that needs manual workspace handling.
     */
    public function findItemsWithCustomQuery(int $categoryId): array
    {
        $queryBuilder = $this->connectionPool
            ->getQueryBuilderForTable('tx_myextension_domain_model_item');

        // Use FrontendRestrictionContainer for proper workspace filtering
        $queryBuilder->setRestrictions(
            \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(
                \TYPO3\CMS\Core\Database\Query\Restriction\FrontendRestrictionContainer::class
            )
        );

        $result = $queryBuilder
            ->select('i.*')
            ->from('tx_myextension_domain_model_item', 'i')
            ->join(
                'i',
                'sys_category_record_mm',
                'mm',
                $queryBuilder->expr()->eq('mm.uid_foreign', $queryBuilder->quoteIdentifier('i.uid'))
            )
            ->where(
                $queryBuilder->expr()->eq(
                    'mm.uid_local',
                    $queryBuilder->createNamedParameter($categoryId, \TYPO3\CMS\Core\Database\Connection::PARAM_INT)
                )
            )
            ->executeQuery();

        $items = [];
        while ($row = $result->fetchAssociative()) {
            $this->pageRepository->versionOL('tx_myextension_domain_model_item', $row);
            if (is_array($row)) {
                $items[] = $row;
            }
        }

        return $items;
    }
}
```

### Pattern E: Migrating legacy queries (TYPO3 v10/v11 style to TYPO3 v14)

**BEFORE (deprecated -- old exec_SELECTquery pattern, no longer available):**

```php
<?php
// DEPRECATED: Do NOT use. Not available on TYPO3 v14.
// $res = $GLOBALS['TYPO3_DB']->exec_SELECTquery('*', 'tt_content', 'pid=' . (int)$pageId);
```

**AFTER (modern QueryBuilder with workspace support):**

```php
<?php

use TYPO3\CMS\Backend\Utility\BackendUtility;
use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
    ->getQueryBuilderForTable('tt_content');

$result = $queryBuilder
    ->select('*')
    ->from('tt_content')
    ->where(
        $queryBuilder->expr()->eq(
            'pid',
            $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT)
        )
    )
    ->executeQuery();

while ($row = $result->fetchAssociative()) {
    BackendUtility::workspaceOL('tt_content', $row);
    if (is_array($row)) {
        // Process the workspace-overlaid record
    }
}
```
