---
name: php-modernization-php84
description: PHP 8.4 specific features, deprecations, and migration patterns. Property hooks, asymmetric visibility, new array functions, and breaking changes.
version: 1.0.0
php_compatibility: "8.4+"
related_skills:
  - php-modernization
triggers:
  - php 8.4
  - php84
  - property hooks
  - asymmetric visibility
  - array_find
  - array_any
  - array_all
  - deprecated attribute
  - php upgrade
---

# PHP 8.4 Modernization Guide

> **Compatibility:** PHP 8.4+ (released November 2024)
> 
> **Related Skill:** [php-modernization](./SKILL.md) - General PHP 8.x patterns
> 
> **TYPO3:** v14 supports PHP 8.4, v13 supports PHP 8.2-8.4

This skill covers PHP 8.4 specific features, deprecations, and migration patterns.

---

## 1. Property Hooks (RFC: Property Hooks)

The most significant PHP 8.4 feature. Define `get` and `set` hooks directly on properties.

### Basic Property Hooks

```php
<?php

declare(strict_types=1);

// ❌ OLD: Explicit getter/setter methods
class User
{
    private string $email;

    public function getEmail(): string
    {
        return $this->email;
    }

    public function setEmail(string $email): void
    {
        $this->email = strtolower(trim($email));
    }
}

// ✅ NEW: Property hooks
class User
{
    public string $email {
        get => $this->email;
        set (string $value) => $this->email = strtolower(trim($value));
    }
}
```

### Virtual Properties (No Backing Store)

```php
<?php

declare(strict_types=1);

class Rectangle
{
    public function __construct(
        public int $width,
        public int $height,
    ) {}

    // Virtual property - computed on access, no storage
    public int $area {
        get => $this->width * $this->height;
    }
}

$rect = new Rectangle(10, 20);
echo $rect->area; // 200
```

### Validation with Set Hooks

```php
<?php

declare(strict_types=1);

class Product
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

### Lazy Initialization

```php
<?php

declare(strict_types=1);

class ExpensiveService
{
    private ?Connection $connection = null;

    public Connection $db {
        get => $this->connection ??= $this->createConnection();
    }

    private function createConnection(): Connection
    {
        return new Connection(/* expensive setup */);
    }
}
```

### Property Hooks in Interfaces

```php
<?php

declare(strict_types=1);

interface HasFullName
{
    // Require readable property
    public string $fullName { get; }
}

class Person implements HasFullName
{
    public function __construct(
        public string $firstName,
        public string $lastName,
    ) {}

    public string $fullName {
        get => $this->firstName . ' ' . $this->lastName;
    }
}
```

---

## 2. Asymmetric Visibility

Control read and write visibility separately.

### Public Read, Private Write

```php
<?php

declare(strict_types=1);

// ❌ OLD: Private property + public getter
class Counter
{
    private int $value = 0;

    public function getValue(): int
    {
        return $this->value;
    }

    public function increment(): void
    {
        $this->value++;
    }
}

// ✅ NEW: Asymmetric visibility
class Counter
{
    public private(set) int $value = 0;

    public function increment(): void
    {
        $this->value++;
    }
}

$counter = new Counter();
echo $counter->value; // ✅ Reading allowed
$counter->value = 5;  // ❌ Error: Cannot modify private(set) property
```

### Protected Set

```php
<?php

declare(strict_types=1);

class Entity
{
    public protected(set) int $id;
    public protected(set) \DateTimeImmutable $createdAt;

    public function __construct()
    {
        $this->createdAt = new \DateTimeImmutable();
    }
}

class User extends Entity
{
    public function setId(int $id): void
    {
        $this->id = $id; // ✅ Allowed in child class
    }
}
```

### Readonly Alternative

```php
<?php

declare(strict_types=1);

// These are equivalent for immutable data:

// Option 1: readonly
final readonly class UserDTO
{
    public function __construct(
        public int $id,
        public string $name,
    ) {}
}

// Option 2: Asymmetric visibility (more flexible)
final class UserDTO
{
    public function __construct(
        public private(set) int $id,
        public private(set) string $name,
    ) {}
}
```

---

## 3. New Array Functions

### array_find()

Find the first element matching a callback.

```php
<?php

declare(strict_types=1);

$users = [
    ['id' => 1, 'name' => 'Alice', 'active' => false],
    ['id' => 2, 'name' => 'Bob', 'active' => true],
    ['id' => 3, 'name' => 'Charlie', 'active' => true],
];

// ❌ OLD
$activeUser = null;
foreach ($users as $user) {
    if ($user['active']) {
        $activeUser = $user;
        break;
    }
}

// ✅ NEW
$activeUser = array_find($users, fn($user) => $user['active']);
// ['id' => 2, 'name' => 'Bob', 'active' => true]
```

### array_find_key()

Find the key of the first matching element.

```php
<?php

declare(strict_types=1);

$products = [
    'apple' => ['price' => 1.50, 'stock' => 100],
    'banana' => ['price' => 0.75, 'stock' => 0],
    'cherry' => ['price' => 3.00, 'stock' => 50],
];

$outOfStockKey = array_find_key($products, fn($p) => $p['stock'] === 0);
// 'banana'
```

### array_any()

Check if ANY element matches a condition.

```php
<?php

declare(strict_types=1);

$numbers = [1, 2, 3, 4, 5];

// ❌ OLD
$hasEven = false;
foreach ($numbers as $n) {
    if ($n % 2 === 0) {
        $hasEven = true;
        break;
    }
}

// ✅ NEW
$hasEven = array_any($numbers, fn($n) => $n % 2 === 0);
// true
```

### array_all()

Check if ALL elements match a condition.

```php
<?php

declare(strict_types=1);

$prices = [10.00, 25.50, 15.00, 30.00];

// ❌ OLD
$allPositive = true;
foreach ($prices as $price) {
    if ($price <= 0) {
        $allPositive = false;
        break;
    }
}

// ✅ NEW
$allPositive = array_all($prices, fn($price) => $price > 0);
// true
```

### Practical TYPO3 Examples

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use Vendor\MyExtension\Domain\Model\Product;

final class ProductService
{
    /**
     * @param Product[] $products
     */
    public function findFirstAvailable(array $products): ?Product
    {
        return array_find($products, fn(Product $p) => $p->isInStock());
    }

    /**
     * @param Product[] $products
     */
    public function hasAnyOnSale(array $products): bool
    {
        return array_any($products, fn(Product $p) => $p->isOnSale());
    }

    /**
     * @param Product[] $products
     */
    public function allHaveImages(array $products): bool
    {
        return array_all($products, fn(Product $p) => $p->getImages()->count() > 0);
    }
}
```

---

## 4. #[\Deprecated] Attribute

Mark code as deprecated with structured metadata.

### Basic Usage

```php
<?php

declare(strict_types=1);

#[\Deprecated(
    message: 'Use NewService instead',
    since: '2.0.0'
)]
class OldService
{
    #[\Deprecated('Use processV2() instead', since: '2.0.0')]
    public function process(): void
    {
        // Legacy implementation
    }
}
```

### Deprecating Constants and Properties

```php
<?php

declare(strict_types=1);

class Configuration
{
    #[\Deprecated('Use DEFAULT_TIMEOUT instead', since: '1.5.0')]
    public const TIMEOUT = 30;

    public const DEFAULT_TIMEOUT = 30;

    #[\Deprecated('Access via getSettings() instead')]
    public array $settings = [];
}
```

### Conditional Deprecation

```php
<?php

declare(strict_types=1);

class LegacyAdapter
{
    #[\Deprecated(
        message: 'This method will be removed in v3.0. Use the new API.',
        since: '2.5.0'
    )]
    public function legacyMethod(): mixed
    {
        trigger_error(
            'legacyMethod() is deprecated, use newMethod() instead',
            E_USER_DEPRECATED
        );
        return $this->newMethod();
    }

    public function newMethod(): mixed
    {
        // New implementation
    }
}
```

---

## 5. New in Initializers Enhancement

Use `new` expressions in more places.

```php
<?php

declare(strict_types=1);

class Service
{
    // ✅ NEW: Default object in property declaration
    public Logger $logger = new NullLogger();

    // ✅ NEW: Default object in parameter
    public function __construct(
        private CacheInterface $cache = new ArrayCache(),
        private LoggerInterface $logger = new NullLogger(),
    ) {}
}

// ✅ Static property initialization
class Config
{
    public static Options $defaults = new Options(timeout: 30, retries: 3);
}
```

---

## 6. Deprecations & Breaking Changes

### Implicit Nullable Types Deprecated

```php
<?php

declare(strict_types=1);

// ❌ DEPRECATED in 8.4 (will error in 9.0)
function process(string $value = null): void {}

// ✅ CORRECT: Explicit nullable
function process(?string $value = null): void {}

// ✅ ALSO CORRECT: Union type
function process(string|null $value = null): void {}
```

### E_STRICT Removed

`E_STRICT` error level is removed. All former E_STRICT notices are now regular notices or warnings.

### Underscore as Class Name Reserved

```php
<?php

// ❌ DEPRECATED: Single underscore as class name
class _ {}

// ✅ OK: Underscore with other characters
class _Helper {}
class My_Class {}
```

### Deprecated Functions

```php
<?php

// ❌ DEPRECATED
$result = strtoupper(implode('', $array));  // Works but check for deprecations

// Functions deprecated in 8.4:
// - Various edge cases in date/time functions
// - Some LDAP functions
// - mysqli_ping() (use mysqli_query() instead)
```

---

## 7. Other PHP 8.4 Features

### Improved HTML5 Parsing

```php
<?php

declare(strict_types=1);

// New DOM\HTML5 classes for proper HTML5 parsing
$doc = DOM\HTMLDocument::createFromString($html);
$doc = DOM\HTMLDocument::createFromFile('page.html');
```

### BCMath Improvements

```php
<?php

declare(strict_types=1);

// New BcMath\Number class for object-oriented arbitrary precision
use BcMath\Number;

$a = new Number('123.456');
$b = new Number('789.012');
$sum = $a + $b;  // Operator overloading!
```

### PDO Driver-Specific Subclasses

```php
<?php

declare(strict_types=1);

// New driver-specific PDO classes
$pdo = new Pdo\Mysql($dsn, $user, $pass);
$pdo = new Pdo\Sqlite($dsn);
$pdo = new Pdo\Pgsql($dsn, $user, $pass);
```

---

## 8. Migration Checklist for PHP 8.4

### Pre-Migration

- [ ] Update PHP to 8.4 in development environment
- [ ] Run test suite with PHP 8.4
- [ ] Check composer.json for PHP version constraint
- [ ] Review deprecated function usage

### Code Updates

- [ ] Fix implicit nullable parameters (`= null` without `?`)
- [ ] Replace legacy getters/setters with property hooks (optional)
- [ ] Use asymmetric visibility where appropriate
- [ ] Replace manual array searches with `array_find()`, `array_any()`, `array_all()`
- [ ] Add `#[\Deprecated]` attributes to legacy code

### Rector Rules for PHP 8.4

```php
<?php
// rector.php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
    ])
    ->withSets([
        LevelSetList::UP_TO_PHP_84,
    ]);
```

### PHPStan for PHP 8.4

```neon
# phpstan.neon
parameters:
    phpVersion: 80400
    level: 10
```

### composer.json Update

```json
{
    "require": {
        "php": "^8.4"
    },
    "config": {
        "platform": {
            "php": "8.4.0"
        }
    }
}
```

---

## 9. TYPO3 v14 & PHP 8.4

TYPO3 v14 officially supports PHP 8.4 and uses several new features:

### Core Usage Examples

```php
<?php

declare(strict_types=1);

// TYPO3 Core is adopting property hooks for configuration
// Example pattern (conceptual):
class SiteConfiguration
{
    public string $identifier {
        get => $this->identifier;
        set (string $value) {
            if (!preg_match('/^[a-z][a-z0-9_-]*$/', $value)) {
                throw new \InvalidArgumentException('Invalid site identifier');
            }
            $this->identifier = $value;
        }
    }
}
```

### Extension Compatibility

```php
<?php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
            'php' => '8.2.0-8.4.99',
        ],
    ],
];
```

---

## References

- **PHP 8.4 Release**: https://www.php.net/releases/8.4/
- **Property Hooks RFC**: https://wiki.php.net/rfc/property-hooks
- **Asymmetric Visibility RFC**: https://wiki.php.net/rfc/asymmetric-visibility-v2
- **Array Find RFC**: https://wiki.php.net/rfc/array_find
- **Deprecated Attribute RFC**: https://wiki.php.net/rfc/deprecated_attribute

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.

Based on official PHP 8.4 RFCs and documentation.
