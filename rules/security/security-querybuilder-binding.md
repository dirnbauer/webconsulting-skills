---
id: security-querybuilder-binding
title: "Use QueryBuilder with createNamedParameter for all custom SQL"
category: security
severity: error
appliesTo: ["**/Classes/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when writing any custom database query against TYPO3 tables."
---
# Use QueryBuilder with createNamedParameter for all custom SQL

Build custom queries with the Doctrine DBAL `QueryBuilder` and bind every dynamic value
through `createNamedParameter()`. Quote identifiers via `quoteIdentifier()`. Restrict
record sets by `pid`, and keep workspace/language overlays correct. Never concatenate
request input into SQL.

**Do:** bind values with `createNamedParameter()`; constrain by `pid`/workspace/language; let restrictions apply.
**Don't:** interpolate `$_GET`/`$_POST`/arguments into a query string, or strip default restrictions blindly.

```php
$qb = $connectionPool->getQueryBuilderForTable('tx_webconexample_item');
$rows = $qb
    ->select('uid', 'title')
    ->from('tx_webconexample_item')
    ->where(
        $qb->expr()->eq('pid', $qb->createNamedParameter($pageId, Connection::PARAM_INT)),
        $qb->expr()->in('category', $qb->createNamedParameter($categoryIds, Connection::PARAM_INT_ARRAY)),
    )
    ->executeQuery()
    ->fetchAllAssociative();
```

> Why: `createNamedParameter(mixed $value, ParameterType $type = STRING, ?string $placeHolder)`
> binds values safely against SQL injection (verified in core
> `Database/Query/QueryBuilder.php`); default restrictions enforce workspace/visibility.
