# 8. Database Operations (TYPO3 v14)

Continues `typo3-update` from [full guide](full-guide.md).

## 8. Database Operations (TYPO3 v14)

### QueryBuilder

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Repository;

use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Database\Query\QueryBuilder;

final class CustomRepository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    public function findByStatus(string $status): array
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return $queryBuilder
            ->select('*')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'status',
                    $queryBuilder->createNamedParameter($status)
                )
            )
            ->orderBy('title', 'ASC')
            ->executeQuery()
            ->fetchAllAssociative();
    }

    public function countByPid(int $pid): int
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return (int)$queryBuilder
            ->count('uid')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'pid',
                    $queryBuilder->createNamedParameter($pid, Connection::PARAM_INT)
                )
            )
            ->executeQuery()
            ->fetchOne();
    }
}
```

### Extbase Repository

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Domain\Repository;

use TYPO3\CMS\Extbase\Persistence\QueryInterface;
use TYPO3\CMS\Extbase\Persistence\Repository;

final class ItemRepository extends Repository
{
    protected $defaultOrderings = [
        'sorting' => QueryInterface::ORDER_ASCENDING,
    ];

    public function findPublished(): array
    {
        $query = $this->createQuery();
        $query->matching(
            $query->logicalAnd(
                $query->equals('hidden', false),
                $query->lessThanOrEqual('starttime', time()),
                $query->logicalOr(
                    $query->equals('endtime', 0),
                    $query->greaterThan('endtime', time())
                )
            )
        );
        
        return $query->execute()->toArray();
    }
}
```
