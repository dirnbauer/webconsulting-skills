---
id: upgrade-rector-fractor-gate
title: "Gate upgrades through Extension Scanner, Rector, Fractor and PHPStan"
category: upgrade-compat
severity: warning
appliesTo: ["**/Classes/**/*.php", "**/Configuration/**/*.php", "**/composer.json"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when bumping an extension's TYPO3 version constraint or migrating deprecated APIs."
---
# Gate upgrades through Extension Scanner, Rector, Fractor and PHPStan

Don't hand-migrate API changes ad hoc. Run the automated gate before merging an upgrade:
the **Extension Scanner** (finds removed/deprecated core API calls), **ssch/typo3-rector**
(rewrites PHP for the target version), **a9f/typo3-fractor** (migrates non-PHP files: TCA,
Fluid, TypoScript, YAML), and **PHPStan** (catches type/usage regressions).

**Do:** run scanner → typo3-rector → typo3-fractor → PHPStan, review diffs, then bump the version constraint.
**Don't:** bump `typo3/cms-core` and fix breakages reactively at runtime, skipping the automated tooling.

```bash
# typical upgrade gate (dev tools, installed as require-dev)
composer req --dev ssch/typo3-rector a9f/typo3-fractor phpstan/phpstan
vendor/bin/rector process Classes/        # PHP migrations
vendor/bin/typo3-fractor process .        # TCA / Fluid / TypoScript / YAML
vendor/bin/phpstan analyse Classes/
# plus: Backend → Admin Tools → "Scan Extension Files" (Extension Scanner)
```

> Why: the Extension Scanner reports removed APIs, Rector/Fractor mechanize the bulk of
> v12→v13→v14 migrations, and PHPStan gates the result. (Rector/Fractor are external dev
> dependencies; install them per project — they are not part of the core.)
