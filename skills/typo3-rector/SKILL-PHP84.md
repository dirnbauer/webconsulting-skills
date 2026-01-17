---
name: typo3-rector-php84
description: Rector rules for PHP 8.4 migration. Automated refactoring for property hooks, implicit nullable, and deprecated functions.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-rector
  - php-modernization
triggers:
  - rector php 8.4
  - rector php84
  - rector property hooks
  - rector implicit nullable
---

# Rector for PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-rector](./SKILL.md) - Main Rector guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. PHP 8.4 Rector Configuration

### rector.php

```php
<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Rector\Php84\Rector\Param\ExplicitNullableParamTypeRector;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
        __DIR__ . '/Tests',
    ])
    ->withSets([
        LevelSetList::UP_TO_PHP_84,
    ])
    ->withRules([
        ExplicitNullableParamTypeRector::class,
    ]);
```

---

## 2. Key PHP 8.4 Rector Rules

### ExplicitNullableParamTypeRector

Fixes implicit nullable parameter deprecation.

```php
// Before
function process(string $value = null): void {}

// After
function process(?string $value = null): void {}
```

### Running Rector

```bash
# Dry run to see changes
ddev exec vendor/bin/rector process --dry-run

# Apply changes
ddev exec vendor/bin/rector process
```

---

## 3. TYPO3 + PHP 8.4 Combined Configuration

```php
<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
    ])
    ->withSets([
        // PHP 8.4 rules
        LevelSetList::UP_TO_PHP_84,
        // TYPO3 v14 rules
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ])
    ->withImportNames()
    ->withTypeCoverageLevel(0);
```

---

## 4. Manual Refactoring Patterns

### Convert Getters/Setters to Property Hooks

Rector doesn't yet auto-convert to property hooks. Manual pattern:

```php
// Before
class User
{
    private string $email;

    public function getEmail(): string
    {
        return $this->email;
    }

    public function setEmail(string $email): void
    {
        $this->email = strtolower(trim($email));
    }
}

// After (manual refactoring)
class User
{
    public string $email {
        get => $this->email;
        set (string $value) => $this->email = strtolower(trim($value));
    }
}
```

---

## 5. CI Integration

### GitHub Actions

```yaml
# .github/workflows/rector.yml
name: Rector

on: [push, pull_request]

jobs:
  rector:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.4'
      - run: composer install
      - run: vendor/bin/rector process --dry-run
```

---

## References

- [typo3-rector SKILL.md](./SKILL.md)
- [Rector Documentation](https://getrector.com/documentation)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
