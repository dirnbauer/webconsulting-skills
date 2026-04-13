# Test Environment Guards

Patterns for writing robust tests that handle different runtime environments gracefully (CI containers running as root, missing PHP extensions, filesystem permissions).

## GD/Imagick Extension Guard

Tests involving image processing (thumbnails, resizing, format conversion) must check for the GD or Imagick extension. CI environments may not have image libraries installed.

```php
protected function setUp(): void
{
    parent::setUp();

    if (!extension_loaded('gd') && !extension_loaded('imagick')) {
        self::markTestSkipped('GD or Imagick extension required for image processing tests.');
    }
}
```

For tests that specifically need GD (e.g., testing GD-specific behavior):

```php
if (!extension_loaded('gd')) {
    self::markTestSkipped('GD extension not available.');
}
```

**Where this matters:**
- `ImageService` tests
- Thumbnail generation tests
- Image dimension/metadata extraction
- Any class wrapping `GdImage` or Imagick objects

## Root User Guard for Permission Tests

Tests that use `chmod(0o000)` to simulate unreadable/unwritable files will always pass when running as root (UID 0), because root bypasses filesystem permissions. Docker CI containers often run as root.

```php
if (function_exists('posix_geteuid') && posix_geteuid() === 0) {
    self::markTestSkipped('Cannot test unreadable files when running as root.');
}
```

**Full pattern in context:**

```php
#[Test]
public function throwsExceptionForUnreadableFile(): void
{
    if (function_exists('posix_geteuid') && posix_geteuid() === 0) {
        self::markTestSkipped('Cannot test unreadable files when running as root.');
    }

    $path = $this->tempDir . '/unreadable.txt';
    file_put_contents($path, 'data');
    chmod($path, 0o000);

    $this->expectException(\RuntimeException::class);
    $this->subject->readFile($path);
}
```

**Where this matters:**
- Tests that verify error handling for permission-denied scenarios
- Filesystem security tests
- Configuration file access tests

## Filesystem tearDown Cleanup

Tests that create temporary files or directories MUST clean up in `tearDown()`. Use instance properties (not local variables) so `tearDown()` can always find and remove them, even when a test fails mid-execution.

### Pattern: Temp Directory Cleanup

```php
final class FileProcessorTest extends UnitTestCase
{
    private ?string $tempDir = null;

    protected function setUp(): void
    {
        parent::setUp();
        $this->tempDir = sys_get_temp_dir() . '/typo3_test_' . uniqid('', true);
        mkdir($this->tempDir, 0o777, true);
    }

    protected function tearDown(): void
    {
        if ($this->tempDir !== null && is_dir($this->tempDir)) {
            $this->removeDirectory($this->tempDir);
        }
        parent::tearDown();
    }

    private function removeDirectory(string $path): void
    {
        $items = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($path, \FilesystemIterator::SKIP_DOTS),
            \RecursiveIteratorIterator::CHILD_FIRST,
        );
        foreach ($items as $item) {
            // Restore permissions before removal (handles chmod 0o000 tests)
            chmod($item->getPathname(), 0o777);
            $item->isDir() ? rmdir($item->getPathname()) : unlink($item->getPathname());
        }
        rmdir($path);
    }
}
```

### Key Rules

1. **Use instance properties** (`$this->tempDir`) not local variables -- `tearDown()` must access them
2. **Check for null** in `tearDown()` -- `setUp()` may not have completed
3. **Restore permissions** before removal -- files made unreadable with `chmod(0o000)` cannot be deleted otherwise
4. **Always call `parent::tearDown()`** -- TYPO3 testing framework cleanup depends on it
5. **Use `sys_get_temp_dir()`** -- never hardcode `/tmp`, it varies across platforms

### Pattern: Single Temp File Cleanup

```php
private ?string $tempFile = null;

protected function tearDown(): void
{
    if ($this->tempFile !== null && file_exists($this->tempFile)) {
        // Restore permissions in case chmod tests made it unreadable
        chmod($this->tempFile, 0o644);
        unlink($this->tempFile);
    }
    parent::tearDown();
}
```

## PHPUnit Version Compatibility: createMock vs createStub

### AllowMockObjectsWithoutExpectations Is PHPUnit 12 Only

The `#[AllowMockObjectsWithoutExpectations]` attribute does NOT exist in PHPUnit 11, which is used in CI for PHP 8.2. Using it causes a fatal error on PHPUnit 11.

**Never use this attribute** in code that must run on PHPUnit 11 (PHP 8.2 CI environments).

### Solution: Use createStub() Instead

When a test double has no configured expectations (no `expects()` calls), use `createStub()` instead of `createMock()`:

```php
// BAD: createMock without expectations triggers PHPUnit notice
// Adding #[AllowMockObjectsWithoutExpectations] breaks PHPUnit 11
$dependency = $this->createMock(SomeInterface::class);

// GOOD: createStub() is designed for doubles without expectations
$dependency = $this->createStub(SomeInterface::class);
$dependency->method('getValue')->willReturn('test');
```

### When to Use Each

| Method | Use When | Supports expects() |
|--------|----------|-------------------|
| `createMock()` | You need to verify interactions (`expects()`, `with()`) | Yes |
| `createStub()` | You only need return values, no interaction verification | No |

### Decision Guide

```
Need to assert method was called with specific args?
├── Yes → createMock() + expects() + with()
└── No
    Need to assert call count?
    ├── Yes → createMock() + expects(self::once())
    └── No → createStub() + method()->willReturn()
```

## Acceptance Tests with DOMDocument

For testing rendered HTML output without a full TYPO3 frontend bootstrap, create acceptance tests that parse HTML with DOMDocument.

### Directory Structure

```
Tests/
├── Unit/              # Pure logic, no TYPO3 bootstrap
├── Functional/        # TYPO3 bootstrap, database
└── Acceptance/        # HTML output verification via DOMDocument
```

### Pattern: DOMDocument-Based HTML Verification

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Acceptance;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

final class RenderedOutputTest extends TestCase
{
    #[Test]
    public function renderedHtmlContainsExpectedStructure(): void
    {
        $html = $this->renderTemplate('EXT:my_ext/Resources/Private/Templates/List.html', [
            'items' => [['title' => 'Test Item']],
        ]);

        $doc = new \DOMDocument();
        @$doc->loadHTML($html, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
        $xpath = new \DOMXPath($doc);

        $items = $xpath->query('//ul[@class="item-list"]/li');
        self::assertNotFalse($items);
        self::assertSame(1, $items->length);
        self::assertSame('Test Item', trim($items->item(0)->textContent));
    }
}
```

**When to use acceptance tests:**
- Verifying ViewHelper output structure
- Testing that templates render expected DOM elements
- Checking accessibility attributes in rendered HTML
- Validating SEO meta tags in output

**When NOT to use (use functional tests instead):**
- Tests that need TYPO3 database
- Tests that need TypoScript configuration
- Tests that need site/routing configuration

## Infection Mutation Testing Configuration

When setting up Infection for a TYPO3 extension that uses `.Build/` for vendor dependencies:

```json5
{
    "$schema": ".Build/vendor/infection/infection/resources/schema.json",
    "source": {
        "directories": ["Classes"]
    },
    "timeout": 30,
    "mutators": {
        "@default": true
    }
}
```

**Key difference from generic setup:** The `$schema` path uses `.Build/vendor/` (TYPO3 convention) rather than `vendor/`. This enables IDE autocompletion and validation for the config file.

See [Mutation Testing](mutation-testing.md) for full configuration with log paths, MSI thresholds, and mutator customization.
