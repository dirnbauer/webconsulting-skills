---
name: typo3-core-contributions-php84
description: PHP 8.4 patterns for TYPO3 Core contributions. Using new language features in Core patches.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-core-contributions
  - php-modernization
triggers:
  - core php 8.4
  - contribute php84
---

# TYPO3 Core Contributions with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-core-contributions](./SKILL.md) - Main contributions guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. Core PHP 8.4 Adoption

### TYPO3 v14 PHP Requirements

TYPO3 v14 requires PHP 8.3+ and fully supports PHP 8.4 features.

### When to Use PHP 8.4 Features in Core

| Feature | Core Usage |
|---------|------------|
| Property hooks | For value objects and DTOs |
| Asymmetric visibility | For immutable services |
| New array functions | For collection operations |
| `#[\Deprecated]` | For deprecating Core methods |

---

## 2. Example Core Patch Patterns

### Using Property Hooks

```php
<?php

declare(strict_types=1);

namespace TYPO3\CMS\Core\Configuration;

final class SiteConfiguration
{
    public string $identifier {
        set (string $value) {
            if (!preg_match('/^[a-z][a-z0-9_-]*$/', $value)) {
                throw new \InvalidArgumentException(
                    'Site identifier must be lowercase alphanumeric',
                    1234567890
                );
            }
            $this->identifier = $value;
        }
    }
}
```

### Using #[\Deprecated]

```php
<?php

declare(strict_types=1);

namespace TYPO3\CMS\Core\Utility;

final class GeneralUtility
{
    #[\Deprecated(
        message: 'Use native array_find() instead',
        since: 'TYPO3 14.0'
    )]
    public static function arrayFind(array $array, callable $callback): mixed
    {
        trigger_error(
            'GeneralUtility::arrayFind() is deprecated. Use array_find().',
            E_USER_DEPRECATED
        );
        return array_find($array, $callback);
    }
}
```

---

## 3. Commit Message for PHP 8.4 Changes

```
[TASK] Use PHP 8.4 array_find() in ContentRepository

Replace manual loop with native array_find() function
introduced in PHP 8.4.

Resolves: #12345
Releases: main
```

---

## 4. Testing PHP 8.4 Changes

```bash
# Run Core tests with PHP 8.4
Build/Scripts/runTests.sh -p 8.4 -s functional

# Check for deprecations
Build/Scripts/runTests.sh -s checkDeprecations
```

---

## References

- [typo3-core-contributions SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)
- [TYPO3 Contribution Guide](https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
