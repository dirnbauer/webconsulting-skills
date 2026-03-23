---
name: typo3-conformance
description: >-
  Evaluate TYPO3 extensions for conformance to TYPO3 v14 standards. Use when assessing
  quality, generating reports, or planning modernization.
compatibility: TYPO3 14.x
metadata:
  version: "1.0.0"
  file_triggers:
    - ext_emconf.php
    - ext_localconf.php
    - Configuration/TCA/**/*
    - *.typoscript
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Extension Conformance Checker

Evaluate TYPO3 extensions for standards compliance, architecture patterns, and best practices.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

### v14 wording precision (reviews)

- **`$GLOBALS['TSFE']`:** Access from extension code is removed in v14 (Breaking [#107831](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107831-DeprecatedTyposcriptFrontendControllerRemoved.html)). The `TypoScriptFrontendController` **class may still exist internally** until a later v14 release — prefer **request attributes** and public FE APIs instead of the old global.
- **TCA:** **Base** TCA files must be static (Important [#107328](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Important-107328-NoDynamicTCAInBaseConfigurationFiles.html)). **`Configuration/TCA/Overrides/`** remains the supported place for modifications — that is not a “ban on runtime TCA”. Programmatic TCA changes are also supported via PSR-14: `BeforeTcaOverridesEvent` and `AfterTcaCompilationEvent` (see [Core DataHandling / TCA events](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/Configuration/Index.html)).

## Skill Delegation

| Skill | Use For |
|-------|---------|
| **typo3-testing** | PHPUnit config, test patterns, coverage |
| **typo3-docs** | RST validation, documentation rendering |
| **php-modernization** | PHP 8.x patterns, PHPStan, type safety |

## Enforcement Behavior (Required)

When this skill states a quality gate (for example `PHPStan level 10`, blocking CI,
or no deprecations), treat it as an implementation requirement, not a suggestion.

1. **Check actual config files first** (`phpstan.neon`, `composer.json`, CI workflow).
2. **If a gate is unmet, fix it in code/config** in the same run whenever feasible.
3. **Run verification commands** and report the real result (pass/fail), not assumptions.
4. **Do not claim conformance** if required gates are not active.
5. **If immediate full remediation is too large**, apply a clearly documented
   transitional state (for example a baseline) and explicitly call out residual debt.

## Evaluation Workflow

1. **Initial Assessment** - Extension key, TYPO3 version, type
2. **File Structure** - composer.json, ext_emconf.php, required directories
3. **Coding Standards** - strict_types, types, PSR-12/PER
4. **Backend Module (TYPO3 v14)** - ES6 modules, Modal API, CSRF
5. **PHP Architecture** - Services.yaml, DI, PSR-14 events
6. **Testing** - PHPUnit, Playwright E2E, coverage >70%
7. **Best Practices** - DDEV, runTests.sh, quality tools, CI/CD

## Scoring System

### Base Score (0-100 points)

| Category | Max Points | Requirements |
|----------|------------|--------------|
| Architecture | 20 | Directory structure, namespace, autoloading |
| Coding Guidelines | 20 | PSR-12/PER, strict_types, documentation |
| PHP Quality | 20 | Types, PHPStan level 10 (transitional level 9 only with documented baseline), no deprecations |
| Testing | 20 | Unit tests, functional tests, 70%+ coverage |
| Best Practices | 20 | CI/CD, quality tools, documentation |

### Excellence Bonus (0-22 points)

| Feature | Points | Description |
|---------|--------|-------------|
| PHPat architecture tests | 5 | Layer constraints enforced |
| Mutation testing | 5 | Infection with 70%+ MSI |
| E2E tests | 4 | Playwright or Codeception |
| 90%+ code coverage | 4 | Exceptional test coverage |
| OpenSSF Scorecard | 4 | Security best practices |

## Required File Structure

```
my_extension/
├── Classes/
│   ├── Controller/
│   ├── Domain/
│   │   ├── Model/
│   │   └── Repository/
│   ├── Service/
│   └── EventListener/
├── Configuration/
│   ├── Backend/
│   │   └── Modules.php
│   ├── Icons.php
│   ├── Services.yaml
│   ├── TCA/
│   │   ├── Overrides/
│   │   └── tx_myext_*.php
│   └── TypoScript/
│       ├── setup.typoscript
│       └── constants.typoscript
├── Documentation/
│   ├── Index.rst
│   └── guides.xml
├── Resources/
│   ├── Private/
│   │   ├── Language/
│   │   ├── Layouts/
│   │   ├── Partials/
│   │   └── Templates/
│   └── Public/
│       ├── Css/
│       ├── Icons/
│       └── JavaScript/
├── Tests/
│   ├── Functional/
│   └── Unit/
├── composer.json
├── ext_emconf.php
├── ext_localconf.php
└── ext_tables.php
```

## Coding Standards Checklist

### PHP Files

- [ ] `declare(strict_types=1);` in every file
- [ ] PSR-4 namespace matching directory structure
- [ ] Full type declarations (parameters, returns, properties)
- [ ] `final` keyword on classes not designed for inheritance
- [ ] `readonly` on immutable classes (PHP 8.2+)
- [ ] Constructor property promotion used
- [ ] No `@var` annotations when type is declared

### Example: Conformant Service

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use Doctrine\DBAL\ParameterType;
use Psr\Log\LoggerInterface;
use TYPO3\CMS\Core\Database\ConnectionPool;

final readonly class ItemService
{
    public function __construct(
        private ConnectionPool $connectionPool,
        private LoggerInterface $logger,
    ) {}

    /**
     * @return array<int, array<string, mixed>>
     */
    public function findActiveItems(): array
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return $queryBuilder
            ->select('*')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'active',
                    $queryBuilder->createNamedParameter(1, ParameterType::INTEGER),
                ),
            )
            ->executeQuery()
            ->fetchAllAssociative();
    }
}
```

## Backend Module Standards (TYPO3 v14)

### Required Patterns

Compare keys (`parent`, `position`, `path`) with **your** TYPO3 version in `typo3/sysext/backend/Configuration/Backend/Modules.php`. On **v14**, primary web modules use `parent` => `content`; `web_info` was replaced by module id `content_status` (alias `web_info` may still exist).

Extbase submodules may still use `extensionName` + `controllerActions` (see EXT:form). Pure non-Extbase modules prefer `routes` + `target` (Core style).

```php
<?php
// Configuration/Backend/Modules.php
return [
    'web_myextension' => [
        'parent' => 'content',
        'position' => ['after' => 'records'],
        'access' => 'user',
        'iconIdentifier' => 'myextension-module',
        'path' => '/module/content/myextension',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExtension',
        'controllerActions' => [
            \Vendor\MyExtension\Controller\BackendController::class => [
                'index',
                'list',
            ],
        ],
    ],
];
```

### ES6 Module Requirements

```javascript
// Resources/Public/JavaScript/MyModule.js
import Modal from '@typo3/backend/modal';
import Notification from '@typo3/backend/notification';
import Severity from '@typo3/backend/severity';

export default class MyModule {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.querySelectorAll('[data-action="delete"]').forEach(element => {
            element.addEventListener('click', this.handleDelete.bind(this));
        });
    }

    handleDelete(event) {
        event.preventDefault();
        Modal.confirm(
            'Delete Item',
            'Are you sure?',
            Severity.warning,
            [
                { text: 'Cancel', trigger: (event, modal) => modal.hideModal() },
                {
                    text: 'Delete',
                    trigger: (event, modal) => {
                        this.performDelete();
                        modal.hideModal();
                    },
                    btnClass: 'btn-danger',
                }
            ]
        );
    }
}
```

> **v14 note:** `Modal.confirm()` still works; the implementation uses **native `<dialog>`** (Breaking [#107443](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107443-MigrateModalComponentFromBootstrapToNativeDialog.html)). Button callbacks use **`(event, modal) => modal.hideModal()`** (not `Modal.dismiss()`). Bootstrap-style **`btnClass`** values (e.g. `btn-danger`) may render differently — verify appearance or prefer TYPO3 button classes.

## PHP Architecture Requirements

### Services.yaml

```yaml
# Configuration/Services.yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\MyExtension\:
    resource: '../Classes/*'
    exclude:
      - '../Classes/Domain/Model/*'

  # Explicit public services if needed
  Vendor\MyExtension\Service\PublicApiService:
    public: true
```

### PSR-14 Event Listeners

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\DataHandling\Event\IsTableExcludedFromReferenceIndexEvent;

#[AsEventListener(identifier: 'myext/reference-index-example')]
final readonly class ReferenceIndexExampleListener
{
    public function __invoke(IsTableExcludedFromReferenceIndexEvent $event): void
    {
        if ($event->getTable() !== 'tx_myext_items') {
            return;
        }

        // Example: exclude a cache table from reference index (real Core event).
    }
}
```

## Testing Standards

### Required Tests

| Type | Requirement | Tool |
|------|-------------|------|
| Unit | Required, 70%+ coverage | PHPUnit |
| Functional | Required for DB operations | PHPUnit + TYPO3 Framework |
| Architecture | Required for full points | PHPat |
| E2E | Optional bonus | Playwright |

### PHPUnit Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/UnitTestsBootstrap.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>Tests/Unit</directory>
        </testsuite>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <report>
            <clover outputFile="var/log/coverage.xml"/>
            <html outputDirectory="var/log/coverage"/>
        </report>
    </coverage>
    <source>
        <include>
            <directory>Classes</directory>
        </include>
    </source>
</phpunit>
```

### PHPat Architecture Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Architecture;

use PHPat\Selector\Selector;
use PHPat\Test\Builder\Rule;
use PHPat\Test\PHPat;

final class ArchitectureTest
{
    public function testDomainModelIndependence(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Domain\Model'))
            ->shouldNot()
            ->dependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Controller'));
    }

    public function testServicesDoNotDependOnControllers(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Service'))
            ->shouldNot()
            ->dependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Controller'));
    }
}
```

## Quality Tools

### Required Configuration

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          
      - name: Install dependencies
        run: composer install
        
      - name: PHPStan
        run: vendor/bin/phpstan analyse --level=10
        
      - name: PHP-CS-Fixer
        run: vendor/bin/php-cs-fixer fix --dry-run --diff
        
      - name: PHPUnit
        run: vendor/bin/phpunit --coverage-clover var/log/coverage.xml
```

### PHPStan Configuration

```neon
# phpstan.neon
includes:
    - vendor/phpstan/phpstan-strict-rules/rules.neon
    - vendor/saschaegerer/phpstan-typo3/extension.neon

parameters:
    level: 10
    paths:
        - Classes
        - Tests
    excludePaths:
        - Tests/Fixtures/*
```

### CI Enforcement Rule

- PHPStan in CI must be **blocking**. Do not set `continue-on-error: true` for the
  PHPStan step in `.github/workflows/ci.yml`.
- If PHPStan is temporarily non-blocking for migration reasons, mark the extension as
  **not fully conformant** and include a concrete remediation plan and owner.

## Scoring Interpretation

| Score | Grade | Status |
|-------|-------|--------|
| 90-122 | A+ | Excellent - Enterprise Ready |
| 80-89 | A | Production Ready |
| 70-79 | B | Development Ready |
| 60-69 | C | Basic - Needs Work |
| <60 | F | Not Conformant |

## v14-Only Conformance Changes

> The following conformance criteria apply when evaluating extensions for **TYPO3 v14**.

### v14 Conformance Requirements **[v14 only]**

- **No `$GLOBALS['TSFE']` usage** — access removed in v14 (class still exists internally, will be removed in a later v14 release). Use request attributes.
- **No Extbase annotations** — only PHP 8 attributes (`#[Validate]`, `#[IgnoreValidation]`).
- **Base TCA files must be static** — use `TCA/Overrides` for any modifications.
- **`composer.json` required** — even in classic (non-Composer) mode.
- **Fluid 5.0 compliance** — strict ViewHelper argument types, no underscore-prefixed variables.
- **Backend module parent identifiers** updated: `web` → `content`, `file` → `media`, `tools` → **`admin`** (Core alias maps the legacy `tools` parent to `admin`).
- **No deprecated localization hooks** — use Symfony Translation Component.

### Updated Backend Module Standards **[v14 only]**

Backend modules must use the new parent module identifiers and native `<dialog>` patterns instead of Bootstrap Modals.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-conformance-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
