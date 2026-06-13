# Architecture Testing with phpat

PHP Architecture Tester (phpat) enforces architectural rules through automated tests.

## Installation

```bash
composer require --dev phpat/phpat
```

`phpat/phpat` is a PHPStan extension — it runs as part of PHPStan analysis, not as a standalone PHPUnit suite.

## Configuration

Create a rule class (e.g. `Tests/Architecture/ArchitectureTest.php`) using the PHPStan-extension API. Each test method returns a rule built with `PHPat::rule()`:

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Architecture;

use PHPat\Selector\Selector;
use PHPat\Test\Builder\BuildStep;
use PHPat\Test\PHPat;

final class ArchitectureTest
{
    public function testServicesDoNotDependOnControllers(): BuildStep
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\Extension\Service'))
            ->shouldNotDependOn()
            ->classes(Selector::inNamespace('Vendor\Extension\Controller'));
    }

    public function testDomainDoesNotDependOnInfrastructure(): BuildStep
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\Extension\Domain'))
            ->shouldNotDependOn()
            ->classes(Selector::inNamespace('Vendor\Extension\Infrastructure'));
    }

    public function testEventsAreReadonly(): BuildStep
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\Extension\Event'))
            ->shouldBeReadonly();
    }
}
```

Register the rule class as a PHPStan service and include the phpat extension in `phpstan.neon`:

```neon
includes:
    - .Build/vendor/phpat/phpat/extension.neon

services:
    -
        class: Vendor\Extension\Tests\Architecture\ArchitectureTest
        tags:
            - phpat.test
```

## TYPO3 Extension Rules

### Layer Constraints

```php
public function testDomainIsIsolated(): BuildStep
{
    return PHPat::rule()
        ->classes(Selector::inNamespace('Vendor\Extension\Domain'))
        ->shouldNotDependOn()
        ->classes(
            Selector::inNamespace('Vendor\Extension\Controller'),
            Selector::inNamespace('Vendor\Extension\Command'),
        );
}
```

### Service Layer Rules

```php
public function testServicesHaveInterface(): BuildStep
{
    return PHPat::rule()
        ->classes(Selector::classname('/.*Service$/', true))
        ->excluding(Selector::classname('/.*Interface$/', true))
        ->shouldImplement()
        ->classes(Selector::classname('/.*Interface$/', true));
}
```

## Running Tests

phpat rules are evaluated by PHPStan. Run them via the `phpstan` suite:

```bash
# Via runTests.sh
Build/Scripts/runTests.sh -s phpstan

# Directly
.Build/bin/phpstan analyse
```

## PHPStan Registration

phpat has no PHPUnit testsuite. Register the rule class as a PHPStan service and include the extension (see Configuration above):

```neon
includes:
    - .Build/vendor/phpat/phpat/extension.neon

services:
    -
        class: Vendor\Extension\Tests\Architecture\ArchitectureTest
        tags:
            - phpat.test
```

## Common Rules

| Rule | Purpose |
|------|---------|
| `shouldNotDependOn` | Prevent unwanted dependencies |
| `shouldImplement` | Enforce interface usage |
| `shouldBeReadonly` | Enforce immutability (PHP 8.2+) |
| `shouldBeFinal` | Prevent inheritance |
| `shouldNotExtend` | Restrict inheritance hierarchies |

## Security-Critical Extensions

For security-critical code, enforce:

1. Events are readonly
2. Services don't construct other services (use DI)
3. Domain layer is isolated
4. No circular dependencies
