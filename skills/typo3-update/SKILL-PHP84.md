---
name: typo3-update-php84
description: PHP 8.4 considerations for TYPO3 version updates. Breaking changes, compatibility, and migration strategies.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-update
  - php-modernization
triggers:
  - typo3 update php 8.4
  - v14 php 8.4
  - php 8.4 upgrade
---

# TYPO3 Updates with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-update](./SKILL.md) - Main update guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. TYPO3 Version PHP Requirements

| TYPO3 Version | PHP Minimum | PHP Maximum | PHP 8.4 Support |
|---------------|-------------|-------------|-----------------|
| v13.x | 8.2 | 8.4 | ✅ Supported |
| v14.x | 8.3 | 8.4 | ✅ Recommended |

---

## 2. Dual-Version Compatibility (v13 + v14 with PHP 8.4)

### composer.json

```json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.0 || ^14.0"
    }
}
```

### Using PHP 8.4 Features in Dual-Version Extensions

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

// PHP 8.4 features work on both v13 and v14 when PHP 8.4 is used

final readonly class ProductService
{
    // Asymmetric visibility (PHP 8.4)
    public private(set) int $processedCount = 0;

    public function __construct(
        private ProductRepository $repository,
    ) {}

    public function findActive(): array
    {
        $products = $this->repository->findAll();

        // PHP 8.4 array functions
        return array_filter(
            $products,
            fn($p) => array_any($p->getCategories(), fn($c) => $c->isActive())
        );
    }
}
```

---

## 3. PHP 8.4 Breaking Changes Affecting TYPO3

### Implicit Nullable Parameters

```php
// ❌ Deprecated in PHP 8.4
public function process(string $value = null): void {}

// ✅ Fix for all TYPO3 versions
public function process(?string $value = null): void {}
```

### Class Name Restrictions

```php
// ❌ Deprecated: Single underscore class name
class _ {}

// ✅ Use proper naming
class Helper {}
```

---

## 4. Upgrade Path

### From v13 + PHP 8.2/8.3 to v14 + PHP 8.4

```bash
# 1. Update PHP first (on v13)
ddev config --php-version=8.4
ddev restart

# 2. Run tests and fix deprecations
ddev exec vendor/bin/rector process
ddev exec vendor/bin/phpstan analyse

# 3. Update TYPO3
ddev composer require typo3/cms-core:^14.0

# 4. Run database updates
ddev typo3 extension:setup
ddev typo3 upgrade:run
```

---

## 5. Extension Compatibility

### ext_emconf.php

```php
<?php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
        ],
    ],
];
```

### PHP Version in composer.json

```json
{
    "require": {
        "php": "^8.2"
    },
    "config": {
        "platform": {
            "php": "8.2.0"
        }
    }
}
```

---

## References

- [typo3-update SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)
- [TYPO3 Changelog](https://docs.typo3.org/c/typo3/cms-core/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
