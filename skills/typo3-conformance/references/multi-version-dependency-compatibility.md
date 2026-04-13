# Multi-Version Dependency Compatibility

> **Source**: Real-world conformance findings from extensions supporting multiple major versions of dependencies (e.g., `intervention/image ^3 || ^4`, `psr/http-message ^1 || ^2`)

## Problem Statement

When `composer.json` allows multiple major versions of a dependency (`^3 || ^4`), the extension code **must work with all allowed versions**. Direct usage of version-specific APIs is a conformance violation because:

1. Users on the older version get runtime errors
2. PHPStan may pass on one version but fail on another
3. CI may only test one version, hiding breakage

## Adapter/Interface Pattern (Required)

When a dependency's API differs between major versions, use an **adapter interface** to abstract the differences.

### Architecture

```
Classes/
├── Adapter/
│   ├── ImageProcessorInterface.php    # Version-agnostic contract
│   ├── ImageProcessorV3.php           # Implementation for v3 API
│   └── ImageProcessorV4.php           # Implementation for v4 API
```

### Interface Definition

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Adapter;

interface ImageProcessorInterface
{
    public function resize(string $path, int $width, int $height): string;
    public function getImageSize(string $path): array;
}
```

### Version-Specific Implementations

```php
// V3 implementation — uses v3-specific API
final class ImageProcessorV3 implements ImageProcessorInterface
{
    public function resize(string $path, int $width, int $height): string
    {
        $image = Image::make($path);  // v3 API
        // ...
    }
}

// V4 implementation — uses v4-specific API
final class ImageProcessorV4 implements ImageProcessorInterface
{
    public function resize(string $path, int $width, int $height): string
    {
        $manager = new ImageManager(new Driver());  // v4 API
        $image = $manager->read($path);
        // ...
    }
}
```

### Services.yaml Wiring

The interface **must** be wired in `Configuration/Services.yaml` to the correct implementation:

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true

  Vendor\Extension\Adapter\ImageProcessorInterface:
    factory: ['@Vendor\Extension\Adapter\ImageProcessorFactory', 'create']

  Vendor\Extension\Adapter\ImageProcessorFactory:
    public: true
```

Or with explicit alias:

```yaml
services:
  Vendor\Extension\Adapter\ImageProcessorInterface:
    alias: Vendor\Extension\Adapter\ImageProcessorV4
```

## Direct Version-Specific Usage (Violation)

```php
// ❌ WRONG: Direct usage of v4-only API when composer.json allows ^3 || ^4
use Intervention\Image\ImageManager;
use Intervention\Image\Drivers\Gd\Driver;

$manager = new ImageManager(new Driver());  // Fails on v3
$image = $manager->read($path);             // v4-only method
```

```php
// ❌ WRONG: Type-hinting concrete class instead of adapter interface
public function __construct(
    private readonly ImageProcessorV4 $processor  // Should be ImageProcessorInterface
) {}
```

## PHPStan Compatibility

### Version-Specific `@phpstan-ignore` Tags

When using `method_exists()` for version detection, PHPStan may require ignore tags. These tags **must not be version-specific** — they must work across all supported versions:

```php
// ❌ WRONG: @phpstan-ignore tag that only works on one version
/** @phpstan-ignore method.notFound */
$result = $object->v4OnlyMethod();  // Errors on v3 PHPStan analysis

// ✅ RIGHT: Use adapter pattern instead, no ignore tags needed
$result = $this->adapter->process();
```

### `method_exists()` with Typed Parameters

PHPStan narrows parameter types after `method_exists()` calls. When checking method existence for version detection, use `object` type to prevent narrowing issues:

```php
// ❌ WRONG: Typed parameter gets narrowed by method_exists()
public function process(ImageManager $manager): void
{
    if (method_exists($manager, 'read')) {
        // PHPStan narrows $manager type — may conflict across versions
        $manager->read($path);
    }
}

// ✅ RIGHT: Use object type for version detection bridges
public function process(object $manager): void
{
    if (method_exists($manager, 'read')) {
        $manager->read($path);  // No type narrowing conflict
    }
}

// ✅ BEST: Use adapter pattern, no method_exists() needed
public function process(ImageProcessorInterface $processor): void
{
    $processor->resize($path);  // Clean, testable, version-agnostic
}
```

### PHPStan Must Pass All Versions

PHPStan analysis **must pass against each supported major version** of the dependency. CI should test PHPStan with each version:

```yaml
# CI matrix example
strategy:
  matrix:
    include:
      - dependency-version: '^3'
        phpstan-config: 'Build/phpstan/phpstan.neon'
      - dependency-version: '^4'
        phpstan-config: 'Build/phpstan/phpstan.neon'
```

## Services.yaml / DI Wiring Rules

### Interface Must Be Wired

When using the adapter pattern, the interface **must** be wired in `Services.yaml`:

```yaml
# ❌ WRONG: Interface not wired — DI container cannot resolve it
services:
  _defaults:
    autowire: true

  Vendor\Extension\:
    resource: '../Classes/*'

# ✅ RIGHT: Interface explicitly wired
services:
  _defaults:
    autowire: true

  Vendor\Extension\:
    resource: '../Classes/*'

  Vendor\Extension\Adapter\ImageProcessorInterface:
    alias: Vendor\Extension\Adapter\ImageProcessorV4
```

### Constructor Type-Hints

Constructors **must** type-hint the interface, not the concrete class, when an adapter interface exists:

```php
// ❌ WRONG: Concrete class type-hint bypasses adapter pattern
public function __construct(
    private readonly ImageProcessorV4 $processor
) {}

// ✅ RIGHT: Interface type-hint enables version switching
public function __construct(
    private readonly ImageProcessorInterface $processor
) {}
```

## Conformance Checklist

- [ ] All dependencies with `||` multi-major constraints have adapter interfaces
- [ ] No direct usage of version-specific APIs outside adapter classes
- [ ] `Services.yaml` wires adapter interfaces to concrete implementations
- [ ] Constructors type-hint interfaces, not concrete adapter classes
- [ ] No `@phpstan-ignore` tags that are version-specific
- [ ] PHPStan passes against each supported major version
- [ ] CI matrix tests with each major version of multi-version dependencies
- [ ] `method_exists()` version detection uses `object` type, not concrete types

## Scoring Impact

| Finding | Severity | Points |
|---------|----------|--------|
| Direct version-specific API usage with multi-version constraint | error | -10 |
| Missing adapter interface for API-divergent dependency | error | -10 |
| Interface not wired in Services.yaml | error | -5 |
| Concrete class type-hint instead of interface | warning | -3 |
| Version-specific `@phpstan-ignore` tag | warning | -3 |
| PHPStan not tested against all dependency versions | warning | -3 |
| Adapter pattern properly implemented | excellence | +3 |
