---
name: typo3-extension-upgrade-php84
description: Extension upgrade patterns for PHP 8.4. Rector rules, PHPStan configuration, and compatibility fixes.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-extension-upgrade
  - php-modernization
triggers:
  - extension php 8.4
  - upgrade extension php84
---

# Extension Upgrade to PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-extension-upgrade](./SKILL.md) - Main extension upgrade guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. Extension Compatibility Check

### composer.json Update

```json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.0 || ^14.0"
    },
    "require-dev": {
        "phpstan/phpstan": "^1.10",
        "rector/rector": "^1.0"
    }
}
```

### ext_emconf.php

```php
<?php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '3.0.0',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
        ],
    ],
];
```

---

## 2. Rector Configuration for PHP 8.4

```php
<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
        __DIR__ . '/Tests',
    ])
    ->withSets([
        LevelSetList::UP_TO_PHP_84,
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

---

## 3. Common PHP 8.4 Fixes

### Implicit Nullable

```bash
# Find all occurrences
grep -rn "= null" Classes/ | grep -v "?.*= null"
```

```php
// Fix pattern
// Before
public function setUser(User $user = null): void

// After
public function setUser(?User $user = null): void
```

### Deprecated Functions

Check for deprecated function usage:

```bash
ddev exec vendor/bin/phpstan analyse --level=9
```

---

## 4. PHPStan for PHP 8.4

### phpstan.neon

```neon
parameters:
    phpVersion: 80400
    level: 9
    paths:
        - Classes
    excludePaths:
        - Classes/Domain/Model/*
```

---

## 5. Testing Matrix

### GitHub Actions

```yaml
jobs:
  test:
    strategy:
      matrix:
        php: ['8.2', '8.3', '8.4']
        typo3: ['^13.0', '^14.0']
        exclude:
          - php: '8.2'
            typo3: '^14.0'
```

---

## 6. Upgrade Checklist

- [ ] Update composer.json PHP constraint
- [ ] Run Rector with PHP 8.4 rules
- [ ] Fix implicit nullable parameters
- [ ] Run PHPStan at level 9
- [ ] Test on PHP 8.4 environment
- [ ] Update CI matrix

---

## References

- [typo3-extension-upgrade SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
