---
name: php84-shared
description: Shared repository guide for PHP 8.4 features, migration patterns, and TYPO3-specific follow-ups. Use when a task is specifically about PHP 8.4 language features, deprecations, or upgrading PHP/TYPO3 code to 8.4.
---

# Shared PHP 8.4 Guide

Use this root guide when PHP 8.4 is the cross-cutting concern and you need one place to start before dropping into a more specific skill.

## Start Here

Reach for this guide when the task is about:

- property hooks
- asymmetric visibility
- new array helpers such as `array_find()`, `array_any()`, and `array_all()`
- migration planning for PHP 8.4
- TYPO3 code that should adopt PHP 8.4 features conservatively

Then route to the relevant primary skill:

| Need | Go to |
| --- | --- |
| General PHP modernization | `skills/php-modernization/SKILL.md` |
| TYPO3 upgrade planning | `skills/typo3-update/SKILL.md` |
| Automated TYPO3 refactoring | `skills/typo3-rector/SKILL.md` |
| Testing after migration | `skills/typo3-testing/SKILL.md` |
| Powermail-specific patterns | `skills/typo3-powermail/SKILL.md` |
| Core contribution or patch review | `skills/typo3-core-contributions/SKILL.md` |
| Extension quality review | `skills/typo3-conformance/SKILL.md` |

## Core PHP 8.4 Focus

Prioritize these topics:

1. Property hooks for controlled reads and writes.
2. Asymmetric visibility for public-read/private-write style APIs.
3. New array helper functions where they improve clarity over manual loops.
4. Conservative migration for framework-heavy code, especially when persistence, hydration, reflection, or serialization are involved.

## TYPO3-Specific Rule Of Thumb

Use PHP 8.4 features where they reduce noise without making TYPO3 integration harder.

- Prefer them first in DTOs, value objects, small services, and internal APIs.
- Be more careful in persistence-heavy models, extension APIs, and code that depends on framework hydration.
- Verify Rector, PHPStan, test coverage, and extension constraints before broad adoption.

## Migration Checklist

- Confirm project and extension constraints really allow PHP 8.4.
- Upgrade tooling first: PHPStan, Rector, PHPUnit, ECS/PHP-CS-Fixer, CI images.
- Convert low-risk classes before touching framework boundaries.
- Add or refresh tests before large mechanical refactors.
- Run static analysis after each migration slice.
- Keep behavior changes separate from syntax modernization where possible.

## Repository References

- `skills/php-modernization/references/php8-features.md`
- `skills/php-modernization/references/migration-strategies.md`
- `skills/php-modernization/references/static-analysis-tools.md`
- `skills/php-modernization/references/type-safety.md`

This file replaces the old per-skill `SKILL-PHP84.md` copies. Keep PHP 8.4 guidance centralized here and route into the domain skill that owns the actual implementation details.
