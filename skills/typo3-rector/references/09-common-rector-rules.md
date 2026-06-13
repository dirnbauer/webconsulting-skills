# 9. Common Rector Rules

Continues `typo3-rector` from [full guide](full-guide.md).

## 9. Common Rector Rules

### Namespace Changes (Auto-Migrated)

Rector automatically handles namespace changes between versions.

### Utility Method Changes

```php
<?php
// ❌ Old (deprecated since v14.3)
GeneralUtility::getIndpEnv('TYPO3_REQUEST_HOST');

// ✅ New (TYPO3 v14) — inject the PSR-7 request, don't read $GLOBALS
public function doSomething(ServerRequestInterface $request): void
{
    $normalizedParams = $request->getAttribute('normalizedParams');
    $host = $normalizedParams->getRequestHost();
}
```

### ObjectManager Removal

```php
<?php
// ❌ Old (removed in TYPO3 v14 migration path)
$objectManager = GeneralUtility::makeInstance(ObjectManager::class);
$service = $objectManager->get(MyService::class);

// ✅ New (Dependency Injection)
public function __construct(
    private readonly MyService $myService,
) {}
```
