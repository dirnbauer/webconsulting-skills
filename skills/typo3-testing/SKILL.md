---
name: typo3-testing
description: >-
  TYPO3 extension testing (unit, functional, E2E, architecture, mutation). Use when
  setting up test infrastructure, writing tests, or configuring CI/CD.
compatibility: TYPO3 14.x
metadata:
  version: "1.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Testing Skill

Comprehensive testing infrastructure for TYPO3 extensions: unit, functional, E2E, architecture, and mutation testing.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## Test Type Selection

| Type | Use When | Speed | Framework |
|------|----------|-------|-----------|
| **Unit** | Pure logic, validators, utilities | Fast (ms) | PHPUnit |
| **Functional** | DB interactions, repositories | Medium (s) | PHPUnit + TYPO3 |
| **Architecture** | Layer constraints, dependencies | Fast (ms) | PHPat |
| **E2E** | User workflows, browser | Slow (s-min) | Playwright |
| **Mutation** | Test quality verification | CI only | Infection |

## Test Infrastructure Setup

### Directory Structure

```
Tests/
├── Functional/
│   ├── Controller/
│   ├── Repository/
│   └── Fixtures/
├── Unit/
│   ├── Service/
│   └── Validator/
├── Architecture/
│   └── ArchitectureTest.php
└── E2E/
    └── playwright/
```

### PHPUnit Configuration

> **Do not** run **functional** tests with `UnitTestsBootstrap.php`. Either split configs (recommended: `UnitTests.xml` + `FunctionalTests.xml` as below) or use a single `phpunit.xml` **only** for suites that share the same bootstrap.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/UnitTestsBootstrap.php"
         colors="true"
         cacheResult="false">
    <testsuites>
        <testsuite name="Unit">
            <directory>Tests/Unit</directory>
        </testsuite>
        <testsuite name="Architecture">
            <directory>Tests/Architecture</directory>
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
        <exclude>
            <directory>Classes/Domain/Model</directory>
        </exclude>
    </source>
</phpunit>
```

### Functional Test Configuration

```xml
<!-- FunctionalTests.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/FunctionalTestsBootstrap.php"
         colors="true">
    <testsuites>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

## Unit Testing

### Basic Unit Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit\Service;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;
use Vendor\MyExtension\Service\PriceCalculator;

final class PriceCalculatorTest extends TestCase
{
    private PriceCalculator $subject;

    protected function setUp(): void
    {
        parent::setUp();
        $this->subject = new PriceCalculator();
    }

    #[Test]
    public function calculateNetPriceReturnsCorrectValue(): void
    {
        $grossPrice = 119.00;
        $taxRate = 19.0;

        $netPrice = $this->subject->calculateNetPrice($grossPrice, $taxRate);

        self::assertEqualsWithDelta(100.00, $netPrice, 0.01);
    }

    #[Test]
    public function calculateNetPriceThrowsExceptionForNegativePrice(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionCode(1234567890);

        $this->subject->calculateNetPrice(-10.00, 19.0);
    }
}
```

### Mocking Dependencies

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit\Service;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\MockObject\MockObject;
use PHPUnit\Framework\TestCase;
use Psr\Log\LoggerInterface;
use Vendor\MyExtension\Service\ItemService;
use Vendor\MyExtension\Domain\Repository\ItemRepository;

final class ItemServiceTest extends TestCase
{
    private ItemRepository&MockObject $itemRepositoryMock;
    private LoggerInterface&MockObject $loggerMock;
    private ItemService $subject;

    protected function setUp(): void
    {
        parent::setUp();
        
        $this->itemRepositoryMock = $this->createMock(ItemRepository::class);
        $this->loggerMock = $this->createMock(LoggerInterface::class);
        
        $this->subject = new ItemService(
            $this->itemRepositoryMock,
            $this->loggerMock,
        );
    }

    #[Test]
    public function findActiveItemsReturnsFilteredItems(): void
    {
        $items = [/* mock items */];
        $this->itemRepositoryMock
            ->expects(self::once())
            ->method('findByActive')
            ->with(true)
            ->willReturn($items);

        $result = $this->subject->findActiveItems();

        self::assertSame($items, $result);
    }
}
```

## Functional Testing

### Repository Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Functional\Repository;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;
use Vendor\MyExtension\Domain\Repository\ItemRepository;

final class ItemRepositoryTest extends FunctionalTestCase
{
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    private ItemRepository $subject;

    protected function setUp(): void
    {
        parent::setUp();
        
        $this->importCSVDataSet(__DIR__ . '/Fixtures/Items.csv');
        $this->subject = $this->get(ItemRepository::class);
    }

    #[Test]
    public function findByUidReturnsCorrectItem(): void
    {
        $item = $this->subject->findByUid(1);

        self::assertNotNull($item);
        self::assertSame('Test Item', $item->getTitle());
    }

    #[Test]
    public function findAllReturnsAllItems(): void
    {
        $items = $this->subject->findAll();

        self::assertCount(3, $items);
    }
}
```

### CSV Fixture Format

```csv
# Tests/Functional/Repository/Fixtures/Items.csv
"tx_myext_items"
,"uid","pid","title","active","deleted"
,1,1,"Test Item",1,0
,2,1,"Another Item",1,0
,3,1,"Inactive Item",0,0
```

### Frontend functional test (Extbase controller)

Calling `$controller->listAction()` directly **bypasses** Extbase routing, security, and view resolution. Prefer a **frontend sub-request** through the TYPO3 application stack:

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Functional\Controller;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\Framework\Frontend\InternalRequest;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class ItemControllerFrontendTest extends FunctionalTestCase
{
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    protected function setUp(): void
    {
        parent::setUp();
        $this->importCSVDataSet(__DIR__ . '/Fixtures/Pages.csv');
        $this->importCSVDataSet(__DIR__ . '/Fixtures/Items.csv');
        $this->setUpFrontendRootPage(
            1,
            ['EXT:my_extension/Configuration/TypoScript/setup.typoscript'],
        );
    }

    #[Test]
    public function listPageReturnsHtml(): void
    {
        $response = $this->executeFrontendSubRequest(
            (new InternalRequest())->withPageId(1),
        );

        self::assertSame(200, $response->getStatusCode());
        self::assertStringContainsString('text/html', $response->getHeaderLine('Content-Type'));
    }
}
```

## Architecture Testing with PHPat

### Installation

```bash
composer require --dev phpat/phpat
```

### Architecture Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Architecture;

use PHPat\Selector\Selector;
use PHPat\Test\Builder\Rule;
use PHPat\Test\PHPat;

final class ArchitectureTest
{
    public function testDomainModelsShouldNotDependOnInfrastructure(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Domain\Model'))
            ->shouldNot()
            ->dependOn()
            ->classes(
                Selector::inNamespace('Vendor\MyExtension\Controller'),
                Selector::inNamespace('Vendor\MyExtension\Infrastructure'),
            );
    }

    public function testServicesShouldNotDependOnControllers(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Service'))
            ->shouldNot()
            ->dependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Controller'));
    }

    public function testRepositoriesShouldImplementInterface(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::classname('/.*Repository$/', true))
            ->excluding(Selector::classname('/.*Interface$/', true))
            ->should()
            ->implement()
            ->classes(Selector::classname('/.*RepositoryInterface$/', true));
    }

    public function testRepositoriesShouldStayFreeOfControllers(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Domain\Repository'))
            ->shouldNot()
            ->dependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Controller'));
    }
}
```

### PHPat Configuration

```neon
# phpstan.neon
includes:
    - vendor/phpat/phpat/extension.neon

parameters:
    level: 9
    paths:
        - Classes
        - Tests
```

## E2E Testing with Playwright

### Setup

```bash
# Install Playwright
npm init playwright@latest

# Configure for TYPO3
mkdir -p Tests/E2E/playwright
```

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './Tests/E2E',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'https://my-extension.ddev.site',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### E2E Test Example

```typescript
// Tests/E2E/item-list.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Item List', () => {
  test('displays items correctly', async ({ page }) => {
    await page.goto('/items');

    await expect(page.locator('h1')).toContainText('Items');
    await expect(page.locator('.item-card')).toHaveCount(3);
  });

  test('filters items by category', async ({ page }) => {
    await page.goto('/items');

    await page.selectOption('[data-testid="category-filter"]', 'electronics');
    await expect(page.locator('.item-card')).toHaveCount(1);
  });

  test('creates new item', async ({ page }) => {
    await page.goto('/items/new');

    await page.fill('[name="title"]', 'New Test Item');
    await page.fill('[name="description"]', 'Test description');
    await page.click('[type="submit"]');

    await expect(page).toHaveURL(/\/items\/\d+/);
    await expect(page.locator('h1')).toContainText('New Test Item');
  });
});
```

## Mutation Testing with Infection

### Installation

```bash
composer require --dev infection/infection
```

### Configuration

```json
// infection.json5
{
    "$schema": "vendor/infection/infection/resources/schema.json",
    "source": {
        "directories": ["Classes"],
        "excludes": ["Domain/Model"]
    },
    "logs": {
        "text": "var/log/infection.log",
        "html": "var/log/infection.html"
    },
    "mutators": {
        "@default": true
    },
    "minMsi": 70,
    "minCoveredMsi": 80
}
```

### Run Mutation Tests

```bash
vendor/bin/infection --threads=4
```

## Test Commands

```bash
# Unit tests
vendor/bin/phpunit -c Tests/UnitTests.xml

# Functional tests
vendor/bin/phpunit -c Tests/FunctionalTests.xml

# Architecture tests
vendor/bin/phpstan analyse

# All tests with coverage
vendor/bin/phpunit --coverage-html var/log/coverage

# E2E tests
npx playwright test

# Mutation tests
vendor/bin/infection
```

## CI/CD Configuration

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php-version: ['8.2', '8.3', '8.4']
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php-version }}
          coverage: xdebug
      - run: composer install
      - run: vendor/bin/phpunit -c Tests/UnitTests.xml --coverage-clover coverage.xml

  functional:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php-version: ['8.2', '8.3', '8.4']
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test
        ports:
          - 3306:3306
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php-version }}
      - run: composer install
      - run: vendor/bin/phpunit -c Tests/FunctionalTests.xml

  architecture:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php-version: ['8.2', '8.3', '8.4']
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php-version }}
      - run: composer install
      - run: vendor/bin/phpstan analyse
```

## Scoring Requirements

| Criterion | Requirement |
|-----------|-------------|
| Unit tests | Required, 70%+ coverage |
| Functional tests | Required for DB operations |
| Architecture tests | **PHPat required** for full conformance |
| PHPStan | Level 9+ (level 10 recommended) |
| E2E tests | Optional, bonus points |
| Mutation | 70%+ MSI for bonus points |

## v14-Only Testing Changes

> The following testing-related changes apply when testing against **TYPO3 v14**.

### Testing Framework Version **[v14 only]**

Pick **`typo3/testing-framework`** to match your **TYPO3 core line** (see [Packagist](https://packagist.org/packages/typo3/testing-framework) `require.typo3/cms-core` for each major). **`^9.0` supports TYPO3 v13 and v14** — use it for v14 projects (and v13+v14 dual-version trees with the appropriate CI matrix / locks):

```json
{
    "require-dev": {
        "typo3/testing-framework": "^9.0"
    }
}
```

Dual-version CI usually means **separate Composer lock files or CI matrix jobs** per core version, not a single constraint that spans incompatible testing-framework majors.

### Fluid 5.0 in Functional Tests **[v14 only]**

Functional tests rendering Fluid templates must account for Fluid 5.0 strict typing. ViewHelper arguments must match expected types exactly or tests will fail with type errors.

### TCA Read-Only in Tests **[v14 only]**

`$GLOBALS['TCA']` is read-only after boot in v14. Test fixtures that modify TCA at runtime must use `TcaSchemaFactory` or configure TCA in `Configuration/TCA/` fixtures instead.

### Deprecated Method Removal **[v14 only]**

Test code using deprecated TYPO3 APIs (e.g., `$GLOBALS['TSFE']`, Extbase annotations, `MailMessage->send()`) will fail in v14. Run tests against TYPO3 v14 in CI to catch these early.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-testing-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
