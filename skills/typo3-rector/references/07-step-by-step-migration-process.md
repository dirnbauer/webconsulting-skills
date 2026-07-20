# 7. Step-by-Step Migration Process

Continues `typo3-rector` from [full guide](full-guide.md).

## 7. Step-by-Step Migration Process

### 1. Prepare

```bash
# Create backup
ddev snapshot --name=before-migration

# Ensure tests pass
ddev exec vendor/bin/phpunit -c packages/my_extension/Tests/phpunit.xml

# Check deprecation log
tail -f var/log/typo3_deprecations_*.log
```

### 2. Configure Rector for TYPO3 v14

```php
<?php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;

return RectorConfig::configure()
    ->withPaths([__DIR__ . '/packages/my_extension/Classes'])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

### 3. Run Rector

```bash
# Dry run first
ddev exec vendor/bin/rector process --dry-run

# Apply changes
ddev exec vendor/bin/rector process

# Review changes
git diff
```

### 4. Manual Fixes

- Review Rector output for skipped files
- Check deprecation log for remaining issues
- Update TCA configurations manually
- Test all backend modules

### 5. Test on TYPO3 v14

```bash
ddev composer require "typo3/cms-core:^14.3" --no-update
ddev composer update
ddev typo3 cache:flush
ddev exec vendor/bin/phpunit
```

### 6. Commit

```bash
git add -A
git commit -m "feat: Apply Rector migrations for TYPO3 v14"
```
