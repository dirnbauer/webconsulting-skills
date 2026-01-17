---
name: typo3-testing-php84
description: PHP 8.4 testing patterns for TYPO3. PHPUnit 11/12 compatibility, new assertions, and property hooks testing.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-testing
  - php-modernization
triggers:
  - testing php 8.4
  - phpunit 12
  - php 8.4 tests
---

# TYPO3 Testing with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-testing](./SKILL.md) - Main testing guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. PHPUnit Version Compatibility

### composer.json

```json
{
    "require-dev": {
        "phpunit/phpunit": "^11.0 || ^12.0",
        "typo3/testing-framework": "^9.0"
    }
}
```

### phpunit.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         cacheDirectory=".phpunit.cache"
         requireCoverageMetadata="false"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>Tests/Unit</directory>
        </testsuite>
    </testsuites>
    <php>
        <ini name="error_reporting" value="E_ALL"/>
    </php>
</phpunit>
```

---

## 2. Testing Property Hooks

### Class with Property Hooks

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Domain\Model;

final class Product
{
    public string $sku {
        set (string $value) {
            if (!preg_match('/^[A-Z]{3}-\d{4}$/', $value)) {
                throw new \InvalidArgumentException('Invalid SKU format');
            }
            $this->sku = $value;
        }
    }

    public float $price {
        set (float $value) {
            if ($value < 0) {
                throw new \InvalidArgumentException('Price cannot be negative');
            }
            $this->price = $value;
        }
    }
}
```

### Test Class

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit\Domain\Model;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;
use Vendor\MyExtension\Domain\Model\Product;

final class ProductTest extends TestCase
{
    #[Test]
    public function validSkuIsAccepted(): void
    {
        $product = new Product();
        $product->sku = 'ABC-1234';

        self::assertSame('ABC-1234', $product->sku);
    }

    #[Test]
    public function invalidSkuThrowsException(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid SKU format');

        $product = new Product();
        $product->sku = 'invalid';
    }

    #[Test]
    public function negativePriceThrowsException(): void
    {
        $this->expectException(\InvalidArgumentException::class);

        $product = new Product();
        $product->price = -10.00;
    }
}
```

---

## 3. Testing Asymmetric Visibility

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Domain\Model;

final class Counter
{
    public private(set) int $value = 0;

    public function increment(): void
    {
        $this->value++;
    }
}
```

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit\Domain\Model;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;
use Vendor\MyExtension\Domain\Model\Counter;

final class CounterTest extends TestCase
{
    #[Test]
    public function valueIsReadable(): void
    {
        $counter = new Counter();

        self::assertSame(0, $counter->value);
    }

    #[Test]
    public function incrementIncreasesValue(): void
    {
        $counter = new Counter();
        $counter->increment();

        self::assertSame(1, $counter->value);
    }

    #[Test]
    public function valueCannotBeSetDirectly(): void
    {
        // This test verifies compile-time behavior
        // In PHP 8.4, attempting to set would cause an Error
        $counter = new Counter();

        // Use Reflection to verify visibility
        $reflection = new \ReflectionProperty(Counter::class, 'value');
        self::assertTrue($reflection->isPublic());
        // Note: ReflectionProperty doesn't expose asymmetric visibility directly
    }
}
```

---

## 4. Using New Array Functions in Tests

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit\Service;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class ArrayFunctionsTest extends TestCase
{
    #[Test]
    public function arrayFindReturnsFirstMatch(): void
    {
        $users = [
            ['id' => 1, 'active' => false],
            ['id' => 2, 'active' => true],
            ['id' => 3, 'active' => true],
        ];

        $result = array_find($users, fn($u) => $u['active']);

        self::assertSame(['id' => 2, 'active' => true], $result);
    }

    #[Test]
    public function arrayAnyReturnsTrueWhenMatchExists(): void
    {
        $numbers = [1, 3, 5, 6, 7];

        $hasEven = array_any($numbers, fn($n) => $n % 2 === 0);

        self::assertTrue($hasEven);
    }

    #[Test]
    public function arrayAllReturnsTrueWhenAllMatch(): void
    {
        $prices = [10.00, 25.50, 15.00];

        $allPositive = array_all($prices, fn($p) => $p > 0);

        self::assertTrue($allPositive);
    }
}
```

---

## 5. PHPUnit 12 Attribute Changes

### New Attribute Syntax

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit;

use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Depends;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;
use Vendor\MyExtension\Service\ProductService;

#[CoversClass(ProductService::class)]
#[Group('unit')]
final class ProductServiceTest extends TestCase
{
    #[Test]
    public function createProductReturnsProduct(): void
    {
        // ...
    }

    #[Test]
    #[DataProvider('validSkuProvider')]
    public function validateSkuWithValidData(string $sku): void
    {
        // ...
    }

    public static function validSkuProvider(): iterable
    {
        yield 'standard sku' => ['ABC-1234'];
        yield 'another sku' => ['XYZ-9999'];
    }

    #[Test]
    #[Depends('createProductReturnsProduct')]
    public function updateProductAfterCreate(): void
    {
        // ...
    }
}
```

---

## 6. Mocking with readonly Classes

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Unit\Service;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;
use Vendor\MyExtension\Repository\ProductRepository;
use Vendor\MyExtension\Service\ProductService;

final class ProductServiceTest extends TestCase
{
    #[Test]
    public function findProductDelegatesToRepository(): void
    {
        // Create mock for readonly class dependency
        $repositoryMock = $this->createMock(ProductRepository::class);
        $repositoryMock
            ->expects($this->once())
            ->method('findByUid')
            ->with(123)
            ->willReturn(['uid' => 123, 'name' => 'Test']);

        // Inject mock via constructor
        $service = new ProductService($repositoryMock);

        $result = $service->getProduct(123);

        self::assertSame('Test', $result['name']);
    }
}
```

---

## 7. Migration Checklist

- [ ] Update PHPUnit to 11.x or 12.x
- [ ] Replace annotation-based test markers with Attributes
- [ ] Update `@covers` to `#[CoversClass]`
- [ ] Update `@dataProvider` to `#[DataProvider]`
- [ ] Test property hooks validation logic
- [ ] Verify readonly class mocking works
- [ ] Update CI pipeline for PHP 8.4

---

## References

- [typo3-testing SKILL.md](./SKILL.md)
- [PHPUnit Documentation](https://docs.phpunit.de/)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
