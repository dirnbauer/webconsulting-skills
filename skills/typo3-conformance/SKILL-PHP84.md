---
name: typo3-conformance-php84
description: PHP 8.4 coding standards for TYPO3 extension conformance. Property hooks, visibility, and modern patterns.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-conformance
  - php-modernization
triggers:
  - conformance php 8.4
  - extension standards php84
---

# Extension Conformance with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-conformance](./SKILL.md) - Main conformance guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. PHP 8.4 Coding Standards

### Recommended Patterns

| Pattern | Standard |
|---------|----------|
| Property hooks | Use for validation/transformation |
| Asymmetric visibility | Prefer over private + getter |
| New array functions | Use over manual loops |
| `#[\Deprecated]` | Mark legacy code properly |

---

## 2. PHP-CS-Fixer Configuration

```php
<?php
// .php-cs-fixer.dist.php

$config = new PhpCsFixer\Config();

return $config
    ->setRules([
        '@PER-CS' => true,
        '@PER-CS:risky' => true,
        'declare_strict_types' => true,
        'trailing_comma_in_multiline' => [
            'elements' => ['arguments', 'arrays', 'match', 'parameters'],
        ],
        'nullable_type_declaration_for_default_null_value' => true,
    ])
    ->setRiskyAllowed(true)
    ->setFinder(
        PhpCsFixer\Finder::create()
            ->in(__DIR__ . '/Classes')
            ->in(__DIR__ . '/Tests')
    );
```

---

## 3. PHPStan Level 10

```neon
# phpstan.neon
parameters:
    phpVersion: 80400
    level: 10
    paths:
        - Classes
    treatPhpDocTypesAsCertain: false
```

---

## 4. Conformance Checklist for PHP 8.4

- [ ] All nullable parameters explicitly typed (`?Type`)
- [ ] `declare(strict_types=1)` in all files
- [ ] No single underscore class names
- [ ] `#[\Deprecated]` on legacy methods
- [ ] PHPStan level 9+ passing
- [ ] PHP-CS-Fixer with PER-CS

---

## References

- [typo3-conformance SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)
- [PER Coding Style](https://www.php-fig.org/per/coding-style/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
