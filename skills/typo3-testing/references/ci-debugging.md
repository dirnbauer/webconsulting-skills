# Debugging CI Test Failures

## Multi-Version Error Analysis

When tests fail in CI across multiple TYPO3 versions, **always check error messages from ALL matrix combinations** (v13 AND v14, all PHP versions). Different TYPO3 versions often fail with completely different errors for the same root cause.

### Common Error Pairs

| v13 Error | v14 Error | Root Cause |
|-----------|-----------|------------|
| `parseFunc without any configuration` | `No valid attribute "applicationType"` | Missing TSFE bootstrap |
| Method signature mismatch | Missing interface method | API change between versions |
| Deprecated function warning | Fatal: undefined method | Removed API |
| Test passes | `RuntimeException` in DI container | Singleton resolution order changed |

## Debugging Checklist

1. **Get error counts per matrix:**

   ```bash
   gh run view <RUN_ID> --log-failed 2>&1 | grep "There were"
   ```

2. **Compare v13 vs v14 errors** — different errors often mean different root causes

3. **Check regression scope:**
   - Only your new tests fail → your test setup is incomplete
   - Existing tests also fail → your change has side effects (e.g., `$GLOBALS` pollution)

4. **Get detailed errors per version:**

   ```bash
   gh run view <RUN_ID> --log-failed 2>&1 | grep "^build.*13.4.*8.5.*Functional.*) " | head -20
   gh run view <RUN_ID> --log-failed 2>&1 | grep "^build.*14.0.*8.5.*Functional.*) " | head -20
   ```

## Common Pitfalls

### `$GLOBALS['TYPO3_REQUEST']` Pollution

Setting `$GLOBALS['TYPO3_REQUEST']` in `setUp()` affects ALL tests in the class:

- **v14:** Requires `applicationType` attribute — missing it causes `RuntimeException` in PageRenderer/DI container resolution (63+ errors)
- **v13:** Enables additional processing paths — existing test assertions may no longer match (7+ failures)

**Fix:** Set the global only in specific test methods that need it, with `try/finally` cleanup:

```php
$GLOBALS['TYPO3_REQUEST'] = $this->request
    ->withAttribute('applicationType', ApplicationType::FRONTEND);

try {
    // test code
} finally {
    unset($GLOBALS['TYPO3_REQUEST']);
}
```

### Functional Tests Cannot Call `parseFunc()` with TypoScript References

`ContentObjectRenderer::parseFunc($html, null, '< lib.parseFunc_RTE')` requires:
- TypoScript configuration loaded (v13: `LogicException`)
- Full request with `applicationType` (v14: `RuntimeException`)
- `$GLOBALS['TYPO3_REQUEST']` for child cObj instances

**Solution:** Use unit tests (mock `parseFunc`) + E2E tests (real frontend). See `functional-testing.md` for details.

### Test Isolation Between Matrix Entries

Each matrix entry (PHP version × TYPO3 version) runs independently. A test passing on `8.2 + v13` but failing on `8.5 + v14` indicates version-specific behavior, not flakiness.

## Testing-Framework Version Mapping

| testing-framework | PHPUnit | TYPO3 Versions |
|-------------------|---------|----------------|
| v8                | 10      | 12.4, 13.4     |
| v9                | 11      | 13.4, 14.0+    |

## PHPUnit 11 Compatibility Issues

### Final TestCase Constructor

PHPUnit 11 makes `TestCase::__construct()` final. Extensions that override the constructor will fail:

```
Cannot override final method PHPUnit\Framework\TestCase::__construct()
```

**Fix:** Replace constructor-based initialization with property declarations:

```php
// ❌ PHPUnit 11: Fatal error
abstract class ExtensionTestCase extends FunctionalTestCase
{
    public function __construct(string $name = '')
    {
        parent::__construct($name);
        $this->coreExtensionsToLoad = ['install'];
        $this->testExtensionsToLoad = ['vendor/extension'];
    }
}

// ✅ Works with both PHPUnit 10 and 11
abstract class ExtensionTestCase extends FunctionalTestCase
{
    protected array $coreExtensionsToLoad = ['install'];
    protected array $testExtensionsToLoad = ['vendor/extension'];
}
```

### CGL vs PHPStan Conflict for Static Assertions

PHPUnit 11 marks assertion methods (`assertEquals`, `assertSame`, etc.) as non-static, but TYPO3 CGL (php-cs-fixer) enforces `self::assertEquals()` style.

**Resolution:** CGL is authoritative for code style. Suppress PHPStan false positives:

```yaml
# Build/phpstan/phpstan.neon
parameters:
    ignoreErrors:
        -
            message: '#Call to an undefined static method .+::(assert|fail|mark)#'
            reportUnmatched: false
```

`reportUnmatched: false` is essential — on TYPO3 12.4 with testing-framework v8 (PHPUnit 10), the pattern has no matches.

## Archived TYPO3-CI GitHub Actions

Several TYPO3 CI GitHub Actions have been archived and their Docker images return 403 Forbidden:

| Action | Status | Replacement |
|--------|--------|-------------|
| `TYPO3-CI-Xliff-Lint` | Archived (2021) | DIY `xmllint --schema xliff-core-1.2-strict.xsd` or remove if no `.xlf` files |
| Other `TYPO3-Continuous-Integration/*` | Check individually | May need replacement |

**Before adding an XLIFF linter:** Verify the extension actually has `.xlf` files:
```bash
find . -name '*.xlf' -not -path './.Build/*'
```
Many extensions don't ship translations and the CI job was added as boilerplate.

## Test Fixture Isolation from TYPO3 Core

When tests depend on TYPO3 core class docblocks (e.g., testing documentation generation), **use local fixture classes** instead:

**Problem:** TYPO3 core changes docblock wording between versions (e.g., "that" → "which"), causing test assertion failures across the matrix.

**Solution:** Create controlled fixture classes in `Tests/Functional/Fixtures/Extensions/`:

```php
// Local fixture with stable, controlled docblock
namespace TYPO3Tests\ExampleExtension;

class PropertyExample
{
    /**
     * This is set to the language that is currently running
     */
    public string $lang = 'default';
}
```

Update test config to reference the fixture class instead of the core class. This decouples tests from core docblock changes across TYPO3 versions.

## phpDocumentor Version Differences in Tests

phpDocumentor v8 and v9 differ in generic type rendering:
- **v8:** Preserves original spacing: `array<string,string>`
- **v9:** Normalizes with spaces: `array<string, string>`

**Fix:** Normalize generic type spacing in code that processes phpDoc output:

```php
// Strip spaces after commas inside angle brackets
preg_replace_callback('/<[^>]+>/', static function (array $match): string {
    return str_replace(', ', ',', $match[0]);
}, $type);
```

**Related bug:** Never use `explode(' ', $returnComment, 2)` to split type from description when generic types are involved — types like `array<string, string>` contain internal spaces. Use bracket-depth-aware parsing instead.
