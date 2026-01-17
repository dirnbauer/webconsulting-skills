---
name: typo3-testing-content-blocks
description: Testing Content Blocks elements. Unit tests, functional tests, and E2E testing for Content Blocks-based content.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-testing
  - typo3-content-blocks
triggers:
  - testing content blocks
  - content blocks tests
  - test content element
---

# Testing Content Blocks

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-testing](./SKILL.md) - Main testing guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. Functional Testing Setup

### phpunit-functional.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/FunctionalTestsBootstrap.php"
         cacheDirectory=".phpunit.cache">
    <testsuites>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

---

## 2. Testing Content Element Rendering

### Test Fixture

```xml
<!-- Tests/Functional/Fixtures/ContentBlocks/hero.xml -->
<dataset>
    <pages>
        <uid>1</uid>
        <pid>0</pid>
        <title>Test Page</title>
        <slug>/test</slug>
    </pages>
    <tt_content>
        <uid>1</uid>
        <pid>1</pid>
        <CType>myvendor_hero</CType>
        <header>Hero Headline</header>
        <myvendor_hero_subheadline>Subheadline Text</myvendor_hero_subheadline>
        <myvendor_hero_cta_link>t3://page?uid=1</myvendor_hero_cta_link>
    </tt_content>
</dataset>
```

### Functional Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Functional\ContentBlocks;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class HeroContentBlockTest extends FunctionalTestCase
{
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    protected array $coreExtensionsToLoad = [
        'content_blocks',
    ];

    protected function setUp(): void
    {
        parent::setUp();
        $this->importCSVDataSet(__DIR__ . '/Fixtures/ContentBlocks/hero.csv');
        $this->setUpFrontendRootPage(1, [
            'EXT:my_extension/Configuration/TypoScript/setup.typoscript',
        ]);
    }

    #[Test]
    public function heroElementRendersCorrectly(): void
    {
        $response = $this->executeFrontendSubRequest(
            (new InternalRequest())->withPageId(1)
        );

        $content = (string) $response->getBody();

        self::assertStringContainsString('Hero Headline', $content);
        self::assertStringContainsString('Subheadline Text', $content);
        self::assertStringContainsString('class="hero', $content);
    }
}
```

---

## 3. Testing Record Types

### Test Fixture

```csv
# Tests/Functional/Fixtures/ContentBlocks/team-members.csv
"tx_myvendor_team_member"
,"uid","pid","name","position","email"
,1,1,"John Doe","Developer","john@example.com"
,2,1,"Jane Smith","Designer","jane@example.com"
```

### Repository Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Functional\Repository;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;
use Vendor\MyExtension\Repository\TeamMemberRepository;

final class TeamMemberRepositoryTest extends FunctionalTestCase
{
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    #[Test]
    public function findAllReturnsTeamMembers(): void
    {
        $this->importCSVDataSet(__DIR__ . '/Fixtures/ContentBlocks/team-members.csv');

        $repository = $this->get(TeamMemberRepository::class);
        $members = $repository->findAll();

        self::assertCount(2, $members);
    }
}
```

---

## 4. Testing Collection Fields

### Fixture with Inline Records

```xml
<!-- Tests/Functional/Fixtures/ContentBlocks/accordion.xml -->
<dataset>
    <tt_content>
        <uid>1</uid>
        <pid>1</pid>
        <CType>myvendor_accordion</CType>
        <myvendor_accordion_items>2</myvendor_accordion_items>
    </tt_content>
    <myvendor_accordion_items>
        <uid>1</uid>
        <pid>1</pid>
        <foreign_table_parent_uid>1</foreign_table_parent_uid>
        <title>First Item</title>
        <content>First content</content>
    </myvendor_accordion_items>
    <myvendor_accordion_items>
        <uid>2</uid>
        <pid>1</pid>
        <foreign_table_parent_uid>1</foreign_table_parent_uid>
        <title>Second Item</title>
        <content>Second content</content>
    </myvendor_accordion_items>
</dataset>
```

---

## 5. E2E Testing with Playwright

### Test Content Block Interaction

```typescript
// tests/e2e/content-blocks.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Content Blocks', () => {
    test('hero element displays correctly', async ({ page }) => {
        await page.goto('/test-page');

        const hero = page.locator('.hero');
        await expect(hero).toBeVisible();
        await expect(hero.locator('h1')).toHaveText('Hero Headline');
        await expect(hero.locator('.subheadline')).toHaveText('Subheadline Text');
    });

    test('accordion expands on click', async ({ page }) => {
        await page.goto('/accordion-page');

        const firstItem = page.locator('.accordion-item').first();
        const content = firstItem.locator('.accordion-content');

        // Initially collapsed
        await expect(content).not.toBeVisible();

        // Click to expand
        await firstItem.locator('.accordion-trigger').click();
        await expect(content).toBeVisible();
    });
});
```

---

## 6. Testing TCA Configuration

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Functional\Configuration;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class ContentBlocksTcaTest extends FunctionalTestCase
{
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    #[Test]
    public function heroContentBlockTcaIsRegistered(): void
    {
        $tca = $GLOBALS['TCA']['tt_content']['types']['myvendor_hero'] ?? null;

        self::assertNotNull($tca, 'Hero Content Block type not registered');
        self::assertArrayHasKey('showitem', $tca);
    }

    #[Test]
    public function heroFieldsExistInTca(): void
    {
        $columns = $GLOBALS['TCA']['tt_content']['columns'];

        self::assertArrayHasKey('myvendor_hero_subheadline', $columns);
        self::assertArrayHasKey('myvendor_hero_image', $columns);
    }
}
```

---

## 7. DataProvider for Content Block Variants

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Functional\ContentBlocks;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class ContentBlockRenderingTest extends FunctionalTestCase
{
    #[Test]
    #[DataProvider('contentBlockTypesProvider')]
    public function contentBlockRendersWithoutError(string $cType, string $fixture): void
    {
        $this->importCSVDataSet(__DIR__ . '/Fixtures/' . $fixture);

        $response = $this->executeFrontendSubRequest(
            (new InternalRequest())->withPageId(1)
        );

        self::assertSame(200, $response->getStatusCode());
    }

    public static function contentBlockTypesProvider(): iterable
    {
        yield 'hero' => ['myvendor_hero', 'hero.csv'];
        yield 'accordion' => ['myvendor_accordion', 'accordion.csv'];
        yield 'team-grid' => ['myvendor_team_grid', 'team-grid.csv'];
    }
}
```

---

## References

- [typo3-testing SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [TYPO3 Testing Framework](https://github.com/TYPO3/testing-framework)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
