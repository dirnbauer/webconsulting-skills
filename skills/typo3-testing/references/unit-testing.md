# Unit Testing in TYPO3

Unit tests are fast, isolated tests that verify individual components without external dependencies like databases or file systems.

## When to Use Unit Tests

✅ **Ideal for:**
- Testing pure business logic
- Validators, calculators, transformers
- Value objects and DTOs
- Utilities and helper functions
- Domain models without persistence
- **Controllers with dependency injection** (new in TYPO3 13)
- **Services with injected dependencies**

❌ **Not suitable for:**
- Database operations (use functional tests)
- File system operations
- Methods using `BackendUtility` or global state
- Complex TYPO3 framework integration
- Parent class behavior from framework classes

## Base Class

All unit tests extend `TYPO3\TestingFramework\Core\Unit\UnitTestCase`:

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Domain\Validator;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Domain\Validator\EmailValidator;

/**
 * Unit tests for EmailValidator.
 *
 * @covers \Vendor\Extension\Domain\Validator\EmailValidator
 */
final class EmailValidatorTest extends UnitTestCase
{
    private EmailValidator $subject;

    protected function setUp(): void
    {
        parent::setUp();
        $this->subject = new EmailValidator();
    }

    #[Test]
    public function validEmailPassesValidation(): void
    {
        $result = $this->subject->validate('user@example.com');

        self::assertFalse($result->hasErrors());
    }

    #[Test]
    public function invalidEmailFailsValidation(): void
    {
        $result = $this->subject->validate('invalid-email');

        self::assertTrue($result->hasErrors());
    }
}
```

> **Note:** TYPO3 13+ with PHPUnit 11/12 uses PHP attributes (`#[Test]`) instead of `@test` annotations.
> Use `private` instead of `protected` for properties when possible (better encapsulation).

## Key Principles

### 1. No External Dependencies

Unit tests should NOT:
- Access the database
- Read/write files
- Make HTTP requests
- Use TYPO3 framework services

### 2. Fast Execution

Unit tests should run in milliseconds:
- No I/O operations
- Minimal object instantiation
- Use mocks for dependencies

### 3. Test Independence

Each test should:
- Be runnable standalone
- Not depend on execution order
- Clean up in tearDown()

## Test Structure

### Arrange-Act-Assert Pattern

```php
#[Test]
public function calculatesTotalPrice(): void
{
    // Arrange: Set up test data
    $cart = new ShoppingCart();
    $cart->addItem(new Item('product1', 10.00, 2));
    $cart->addItem(new Item('product2', 5.50, 1));

    // Act: Execute the code under test
    $total = $cart->calculateTotal();

    // Assert: Verify the result
    self::assertSame(25.50, $total);
}
```

### setUp() and tearDown()

```php
protected function setUp(): void
{
    parent::setUp();
    // Initialize test subject and dependencies
    $this->subject = new Calculator();
}

protected function tearDown(): void
{
    // Clean up resources
    unset($this->subject);
    parent::tearDown();
}
```

### Test Method Naming Convention

Use **camelCase** consistently for test method names. The recommended pattern is:

```
{methodUnderTest}{Scenario}{ExpectedResult}
```

**Examples:**

```php
// CORRECT - clear camelCase with {method}{Scenario}{ExpectedResult}
public function setPriorityAboveMaxClampsToHundred(): void
public function getUserByEmailWhenNotFoundReturnsNull(): void
public function calculateTotalForDomesticOrdersIncludesTax(): void

// WRONG - inconsistent capitalization at word boundaries
public function setPriorityClampsTohundred(): void  // "hundred" not capitalized
public function getuserByEmail(): void               // "user" not capitalized
```

**Guidelines:**
- Capitalize every word boundary in camelCase (no lowercase words after the first)
- Start with the method name being tested when possible
- Include the scenario/condition and expected outcome
- Prefer using the `#[Test]` attribute (PHPUnit 12+) instead of the `@test` annotation or `test` prefix in new or updated tests
- Existing test suites that still use `@test` annotations remain valid on older PHPUnit versions; plan to migrate them when upgrading to PHPUnit 12

## Testing with Dependency Injection (TYPO3 13+)

Modern TYPO3 13 controllers and services use constructor injection. Here's how to test them:

### Basic Constructor Injection Test

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Controller;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\MockObject\MockObject;
use TYPO3\CMS\Core\Resource\ResourceFactory;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Controller\ImageController;

final class ImageControllerTest extends UnitTestCase
{
    private ImageController $subject;

    /** @var ResourceFactory&MockObject */
    private ResourceFactory $resourceFactoryMock;

    protected function setUp(): void
    {
        parent::setUp();

        /** @var ResourceFactory&MockObject $resourceFactoryMock */
        $resourceFactoryMock = $this->createMock(ResourceFactory::class);

        $this->resourceFactoryMock = $resourceFactoryMock;
        $this->subject             = new ImageController($this->resourceFactoryMock);
    }

    #[Test]
    public function getFileRetrievesFileFromFactory(): void
    {
        $fileId = 123;
        $fileMock = $this->createMock(\TYPO3\CMS\Core\Resource\File::class);

        $this->resourceFactoryMock
            ->expects(self::once())
            ->method('getFileObject')
            ->with($fileId)
            ->willReturn($fileMock);

        $result = $this->subject->getFile($fileId);

        self::assertSame($fileMock, $result);
    }
}
```

### Multiple Dependencies with Intersection Types

PHPUnit mocks require proper type hints using intersection types for PHPStan compliance:

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Controller;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\MockObject\MockObject;
use TYPO3\CMS\Core\Log\LogManager;
use TYPO3\CMS\Core\Resource\ResourceFactory;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Controller\ImageController;
use Vendor\Extension\Utils\ImageProcessor;

final class ImageControllerTest extends UnitTestCase
{
    private ImageController $subject;

    /** @var ResourceFactory&MockObject */
    private ResourceFactory $resourceFactoryMock;

    /** @var ImageProcessor&MockObject */
    private ImageProcessor $imageProcessorMock;

    /** @var LogManager&MockObject */
    private LogManager $logManagerMock;

    protected function setUp(): void
    {
        parent::setUp();

        /** @var ResourceFactory&MockObject $resourceFactoryMock */
        $resourceFactoryMock = $this->createMock(ResourceFactory::class);

        /** @var ImageProcessor&MockObject $imageProcessorMock */
        $imageProcessorMock = $this->createMock(ImageProcessor::class);

        /** @var LogManager&MockObject $logManagerMock */
        $logManagerMock = $this->createMock(LogManager::class);

        $this->resourceFactoryMock = $resourceFactoryMock;
        $this->imageProcessorMock  = $imageProcessorMock;
        $this->logManagerMock      = $logManagerMock;

        $this->subject = new ImageController(
            $this->resourceFactoryMock,
            $this->imageProcessorMock,
            $this->logManagerMock,
        );
    }

    #[Test]
    public function processImageUsesInjectedProcessor(): void
    {
        $fileMock = $this->createMock(\TYPO3\CMS\Core\Resource\File::class);
        $processedFileMock = $this->createMock(\TYPO3\CMS\Core\Resource\ProcessedFile::class);

        $this->imageProcessorMock
            ->expects(self::once())
            ->method('process')
            ->with($fileMock, ['width' => 800])
            ->willReturn($processedFileMock);

        $result = $this->subject->processImage($fileMock, ['width' => 800]);

        self::assertSame($processedFileMock, $result);
    }
}
```

**Key Points:**
- Use intersection types: `ResourceFactory&MockObject` for proper PHPStan type checking
- Assign mocks to properly typed variables before passing to constructor
- This pattern works with PHPUnit 11/12 and PHPStan Level 10

### Handling $GLOBALS and Singleton State

Some TYPO3 components still use global state. Handle this properly:

```php
final class BackendControllerTest extends UnitTestCase
{
    protected bool $resetSingletonInstances = true;

    #[Test]
    public function checksBackendUserPermissions(): void
    {
        // Mock backend user
        $backendUserMock = $this->createMock(BackendUserAuthentication::class);
        $backendUserMock->method('isAdmin')->willReturn(true);

        $GLOBALS['BE_USER'] = $backendUserMock;

        $result = $this->subject->hasAccess();

        self::assertTrue($result);
    }

    #[Test]
    public function returnsFalseWhenNoBackendUser(): void
    {
        $GLOBALS['BE_USER'] = null;

        $result = $this->subject->hasAccess();

        self::assertFalse($result);
    }
}
```

**Important:** Set `protected bool $resetSingletonInstances = true;` when tests interact with TYPO3 singletons to prevent test pollution.

## Mocking Dependencies

Use PHPUnit's built-in mocking (PHPUnit 11/12):

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Service;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\MockObject\MockObject;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Domain\Model\User;
use Vendor\Extension\Domain\Repository\UserRepository;
use Vendor\Extension\Service\UserService;

final class UserServiceTest extends UnitTestCase
{
    private UserService $subject;

    /** @var UserRepository&MockObject */
    private UserRepository $repositoryMock;

    protected function setUp(): void
    {
        parent::setUp();

        /** @var UserRepository&MockObject $repositoryMock */
        $repositoryMock = $this->createMock(UserRepository::class);

        $this->repositoryMock = $repositoryMock;
        $this->subject        = new UserService($this->repositoryMock);
    }

    #[Test]
    public function findsUserByEmail(): void
    {
        $email = 'test@example.com';
        $user  = new User('John');

        $this->repositoryMock
            ->expects(self::once())
            ->method('findByEmail')
            ->with($email)
            ->willReturn($user);

        $result = $this->subject->getUserByEmail($email);

        self::assertSame('John', $result->getName());
    }

    #[Test]
    public function throwsExceptionWhenUserNotFound(): void
    {
        $email = 'nonexistent@example.com';

        $this->repositoryMock
            ->method('findByEmail')
            ->with($email)
            ->willReturn(null);

        $this->expectException(\RuntimeException::class);
        $this->expectExceptionMessage('User not found');

        $this->subject->getUserByEmail($email);
    }
}
```

> **Note:** TYPO3 13+ with PHPUnit 11/12 uses `createMock()` instead of Prophecy.
> Prophecy is deprecated and should not be used in new tests.
>
> **Multi-version dependencies:** When mocking interfaces from dependencies with `^major1 || ^major2` constraints, verify mocked methods exist on the interface in all supported versions. See `mock-validity.md` for patterns including callback signature verification and adapter pattern testing.

## PHPUnit 12 Compatibility

PHPUnit 12 introduces stricter defaults. Follow these patterns to avoid notices and deprecations.

### Mock vs Stub Discipline (PHPUnit 12+)

PHPUnit 12 reports notices when mock objects have no expectations configured. The correct fix is to use the right test double for the job.

**Rule:** Use `createStub()` when you only need return values. Use `createMock()` only when you need to verify method calls with `expects()`.

```php
// WRONG - creates a mock but sets no expectations (triggers PHPUnit notice)
$model = $this->createMock(Model::class);
$model->method('getName')->willReturn('test');

// CORRECT - use stub when no expectations needed
$model = $this->createStub(Model::class);
$model->method('getName')->willReturn('test');

// CORRECT - use mock when verifying calls
$logger = $this->createMock(LoggerInterface::class);
$logger->expects(self::once())->method('warning');
```

**Detection:** Run tests with `--display-phpunit-notices` flag. Any "No expectations were configured for the mock object" notice indicates a mock that should be a stub.

**Decision guide:**

| Scenario | Use | Method |
|----------|-----|--------|
| Only need return values (`->method()->willReturn()`) | `createStub()` | No expectations |
| Satisfying a type hint for DI | `createStub()` | No expectations |
| Verifying a method was called | `createMock()` | `->expects(self::once())` |
| Verifying call count or arguments | `createMock()` | `->expects()->with()` |

**Example with stubs and mocks in the same test class:**

```php
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\MockObject\MockObject;
use PHPUnit\Framework\MockObject\Stub;

#[CoversClass(MyController::class)]
final class MyControllerTest extends UnitTestCase
{
    private MyController $subject;

    /** @var SomeDependency&Stub */
    private SomeDependency $dependencyStub;

    /** @var LoggerInterface&MockObject */
    private LoggerInterface $loggerMock;

    protected function setUp(): void
    {
        parent::setUp();
        // Stub - only provides return values, no expectations
        $this->dependencyStub = $this->createStub(SomeDependency::class);
        $this->dependencyStub->method('getValue')->willReturn('test');

        // Mock - will verify method calls in tests
        /** @var LoggerInterface&MockObject $loggerMock */
        $loggerMock = $this->createMock(LoggerInterface::class);
        $this->loggerMock = $loggerMock;

        $this->subject = new MyController($this->dependencyStub, $this->loggerMock);
    }

    #[Test]
    public function processLogsWarningOnEmptyInput(): void
    {
        $this->loggerMock->expects(self::once())->method('warning');

        $this->subject->process('');
    }
}
```

> **Note:** Stubs created with `createStub()` do not need `MockObject` intersection types in PHPDoc. The `&MockObject` intersection is only for objects created with `createMock()`. If you want static analysis tools (PHPStan, Psalm) to understand calls like `method()` / `willReturn()` on a stub variable, you can add an explicit intersection with `Stub`, for example:
> `/** @var SomeDependency&\PHPUnit\Framework\MockObject\Stub $dependencyStub */`.

**Fallback - `#[AllowMockObjectsWithoutExpectations]`:**

> **Warning:** The `#[AllowMockObjectsWithoutExpectations]` attribute is only available in PHPUnit 12+. It does **not** exist in PHPUnit 11 (used in CI for PHP 8.2) and will cause a fatal error. Only use this fallback when the project runs PHPUnit 12 exclusively.

When migrating existing test classes with many mocks, you can temporarily suppress the notice with the class-level attribute instead of converting all mocks to stubs at once:

```php
use PHPUnit\Framework\Attributes\AllowMockObjectsWithoutExpectations;

#[AllowMockObjectsWithoutExpectations]
final class LegacyControllerTest extends UnitTestCase
{
    // Existing mocks without expectations are allowed
    // TODO: Migrate createMock() to createStub() where no expects() is used
}
```

This attribute should be treated as **technical debt** and removed once the test class is migrated to use `createStub()` properly.

### Deprecated Type Assertions

PHPUnit 12 deprecates generic `isType()` in favor of specific methods:

| Deprecated | Use Instead |
|------------|-------------|
| `$this->isType('string')` | `$this->isString()` |
| `$this->isType('int')` | `$this->isInt()` |
| `$this->isType('array')` | `$this->isArray()` |
| `$this->isType('bool')` | `$this->isBool()` |
| `$this->isType('float')` | `$this->isFloat()` |
| `$this->isType('null')` | `$this->isNull()` |
| `$this->isType('object')` | `$this->isInstanceOf(ClassName::class)` |

### Constructor Dependency Drift

When a class constructor gains new dependencies, all tests instantiating it will fail with `TypeError`. Use a factory method pattern to centralize instantiation:

```php
final class MyControllerTest extends TestCase
{
    private MyController $subject;
    private DependencyA&MockObject $depAMock;
    private DependencyB&MockObject $depBMock;
    private DependencyC&MockObject $depCMock; // Added later

    protected function setUp(): void
    {
        parent::setUp();

        $this->depAMock = $this->createMock(DependencyA::class);
        $this->depBMock = $this->createMock(DependencyB::class);
        $this->depCMock = $this->createMock(DependencyC::class);

        // Single point of instantiation - update here when constructor changes
        $this->subject = $this->createSubject();
    }

    /**
     * Factory method - single place to update when dependencies change.
     */
    private function createSubject(): MyController
    {
        return new MyController(
            $this->depAMock,
            $this->depBMock,
            $this->depCMock, // Add new dependencies here
        );
    }
}
```

**Benefits:**
- One place to update when constructor signature changes
- Tests clearly show all dependencies
- Easy to create subject with custom mocks in specific tests

## Assertions

### Common Assertions

```php
// Equality
self::assertEquals($expected, $actual);
self::assertSame($expected, $actual); // Strict comparison

// Boolean
self::assertTrue($condition);
self::assertFalse($condition);

// Null checks
self::assertNull($value);
self::assertNotNull($value);

// Type checks
self::assertIsString($value);
self::assertIsInt($value);
self::assertIsArray($value);
self::assertInstanceOf(User::class, $object);

// Collections
self::assertCount(3, $array);
self::assertEmpty($array);
self::assertContains('item', $array);

// Exceptions
$this->expectException(\InvalidArgumentException::class);
$this->expectExceptionMessage('Invalid input');
$subject->methodThatThrows();
```

### Specific Over Generic

```php
// ❌ Too generic
self::assertTrue($result > 0);
self::assertEquals(true, $isValid);

// ✅ Specific and clear
self::assertGreaterThan(0, $result);
self::assertTrue($isValid);
```

## Data Providers

Test multiple scenarios with data providers:

```php
/**
 * @test
 * @dataProvider validEmailProvider
 */
public function validatesEmails(string $email, bool $expected): void
{
    $result = $this->subject->isValid($email);
    self::assertSame($expected, $result);
}

public static function validEmailProvider(): array
{
    return [
        'valid email' => ['user@example.com', true],
        'email with subdomain' => ['user@mail.example.com', true],
        'missing @' => ['userexample.com', false],
        'missing domain' => ['user@', false],
        'empty string' => ['', false],
    ];
}
```

## Testing Private/Protected Methods

**Preferred Approach**: Test through public API whenever possible:

```php
// ✅ Best approach - test through public interface
$result = $subject->publicMethodThatUsesPrivateMethod();
self::assertSame($expected, $result);
```

**When Reflection is Acceptable**: Sometimes protected methods contain complex logic that deserves dedicated testing (e.g., URL validation, attribute resolution). In these cases, use a helper method:

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Controller;

use PHPUnit\Framework\Attributes\Test;
use ReflectionMethod;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Controller\ImageController;

final class ImageControllerTest extends UnitTestCase
{
    private ImageController $subject;

    /**
     * Helper method to access protected methods.
     *
     * @param array<int, mixed> $args
     */
    private function callProtectedMethod(string $methodName, array $args): mixed
    {
        $reflection = new ReflectionMethod($this->subject, $methodName);
        $reflection->setAccessible(true);

        return $reflection->invokeArgs($this->subject, $args);
    }

    #[Test]
    public function isExternalImageReturnsTrueForHttpsUrls(): void
    {
        $result = $this->callProtectedMethod('isExternalImage', ['https://example.com/image.jpg']);

        self::assertTrue($result);
    }

    #[Test]
    public function isExternalImageReturnsFalseForLocalPaths(): void
    {
        $result = $this->callProtectedMethod('isExternalImage', ['/fileadmin/images/test.jpg']);

        self::assertFalse($result);
    }
}
```

**Important Considerations**:
- Only use reflection when testing protected methods with complex logic worth testing independently
- Never test private methods - refactor to protected if testing is needed
- Prefer testing through public API when the logic is simple
- Document why reflection testing is used for a specific method

## Coverage Attribution with #[CoversClass]

When `beStrictAboutCoverageMetadata` is enabled (recommended), PHPUnit restricts coverage reporting to classes listed in `#[CoversClass]`. Code executed during a test but not listed in `#[CoversClass]` will not appear in the coverage report for that test.

If your test exercises DTOs or value objects indirectly (e.g., a service test creates DTO instances), add `#[CoversClass]` for ALL exercised classes:

```php
// DiagnosticServiceTest creates DiagnosticCheck and DiagnosticResult
// instances via DiagnosticService — list them all for coverage
#[CoversClass(DiagnosticService::class)]
#[CoversClass(DiagnosticCheck::class)]
#[CoversClass(DiagnosticResult::class)]
#[CoversClass(Severity::class)]
final class DiagnosticServiceTest extends TestCase
```

Without this, coverage tools (e.g., codecov) may report 0% for the DTOs even though they are fully exercised by the service test.

## Configuration

### PHPUnit XML (Build/phpunit/UnitTests.xml)

```xml
<phpunit
    bootstrap="../../vendor/autoload.php"
    cacheResult="false"
    beStrictAboutTestsThatDoNotTestAnything="true"
    beStrictAboutOutputDuringTests="true"
    failOnDeprecation="true"
    failOnNotice="true"
    failOnWarning="true"
    failOnRisky="true">
    <testsuites>
        <testsuite name="Unit tests">
            <directory>../../Tests/Unit/</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

### Coverage Exclusion Review

When `phpunit.xml` excludes directories from coverage (like `Domain/Model`), verify the exclusion is justified:

1. **Justified exclusions**: Truly trivial getters/setters, pure data containers (DTOs/Value Objects with no logic)
2. **Unjustified exclusions**: Models with business logic, validation, computed properties, or state transitions
3. **Cross-check with mutation testing**: The same exclusion in `infection.json5` / `infection.json.dist` should also be justified

**Audit command:**

```bash
# Check what's excluded from coverage
grep -A 5 '<exclude>' Build/phpunit.xml Build/phpunit/UnitTests.xml 2>/dev/null

# Check what's excluded from mutation testing
grep -A 10 '"excludePaths"' infection.json5 infection.json.dist 2>/dev/null

# Find models with non-trivial logic that might be wrongly excluded
grep -rn 'function [a-z].*(' Classes/Domain/Model/ | grep -v 'get\|set\|is\|has'
```

## Best Practices

1. **One Assert Per Test**: Focus tests on single behavior
2. **Clear Test Names**: Describe what is tested and expected result
3. **Arrange-Act-Assert**: Follow consistent structure
4. **No Logic in Tests**: Tests should be simple and readable
5. **Test Edge Cases**: Empty strings, null, zero, negative numbers
6. **Use Data Providers**: Test multiple scenarios efficiently
7. **Mock External Dependencies**: Keep tests isolated and fast
8. **Use `createStub()` over `createMock()`**: Default to stubs; only use mocks when verifying calls
9. **Use `self::` for assertions**: PHPUnit 12 convention (`self::assertSame()`, not `$this->assertSame()`)

## Testing PHP Syntax Variants

When testing code that parses or analyzes PHP (like Extension Scanner matchers), test all syntax variants that PHP allows. Different syntaxes may be parsed differently.

### Dynamic Method Calls

PHP supports multiple forms of dynamic method calls:

```php
// DataProvider for testing dynamic call handling
public static function dynamicCallSyntaxDataProvider(): array
{
    return [
        // Standard dynamic method call - variable holds method name
        'dynamic method call with variable' => [
            '<?php
            $methodName = "someMethod";
            $object->$methodName();',
            [], // no match expected, must not crash
        ],
        // Expression-based dynamic call - expression evaluated for method name
        'dynamic method call with expression' => [
            '<?php
            $object->{$this->getMethodName()}();',
            [], // no match expected, must not crash
        ],
        // Curly brace syntax with variable
        'dynamic method call with curly brace variable' => [
            '<?php
            $object->{$methodName}();',
            [], // no match expected, must not crash
        ],
    ];
}
```

**Why This Matters**: PhpParser represents these differently:
- `$obj->$var()` → `$node->name` is `PhpParser\Node\Expr\Variable`
- `$obj->{$expr}()` → `$node->name` is `PhpParser\Node\Expr\MethodCall` or other expression
- `$obj->method()` → `$node->name` is `PhpParser\Node\Identifier`

Code assuming `$node->name` is always an `Identifier` will crash on dynamic calls.

### Dynamic Function Calls

```php
'dynamic function call' => [
    '<?php
    $func = "myFunction";
    $func();',
    [],
],
'variable function with call_user_func' => [
    '<?php
    call_user_func($callback, $arg);',
    [],
],
```

### Static Method Variants

```php
'dynamic static method call' => [
    '<?php
    $method = "staticMethod";
    SomeClass::$method();',
    [],
],
'variable class static call' => [
    '<?php
    $class = "SomeClass";
    $class::staticMethod();',
    [],
],
```

### Testing Pattern

Always include regression tests with clear comments:

```php
// Regression test for issue #108413: $object->$var() syntax must not crash
'no match for dynamic method call with variable' => [
    [
        'Foo->aMethod' => [
            'numberOfMandatoryArguments' => 0,
            'maximumNumberOfArguments' => 2,
            'restFiles' => ['Foo-1.rst'],
        ],
    ],
    '<?php
    $methodName = "someMethod";
    $someVar->$methodName();',
    [], // no match, must not crash
],
```

## Common Pitfalls

❌ **Testing Framework Code**
```php
// Don't test TYPO3 core functionality
$this->assertTrue(is_array([])); // Useless test
```

❌ **Slow Tests**
```php
// Don't access file system in unit tests
file_put_contents('/tmp/test.txt', 'data');
```

❌ **Test Interdependence**
```php
// Don't depend on test execution order
/** @depends testCreate */
public function testUpdate(): void { }
```

✅ **Focused, Fast, Isolated Tests**
```php
/**
 * @test
 */
public function calculatesPriceWithDiscount(): void
{
    $calculator = new PriceCalculator();
    $price = $calculator->calculate(100.0, 0.2);
    self::assertSame(80.0, $price);
}
```

## Running Unit Tests

```bash
# Via runTests.sh
Build/Scripts/runTests.sh -s unit

# Via PHPUnit directly
vendor/bin/phpunit -c Build/phpunit/UnitTests.xml

# Via Composer
composer ci:test:php:unit

# Single test file
vendor/bin/phpunit Tests/Unit/Domain/Validator/EmailValidatorTest.php

# Single test method
vendor/bin/phpunit --filter testValidEmail
```

## Troubleshooting Common Issues

### PHPStan Errors with Mocks

**Problem**: PHPStan complains about mock type mismatches.
```
Method expects ResourceFactory but got ResourceFactory&MockObject
```

**Solution**: Use intersection type annotations:
```php
/** @var ResourceFactory&MockObject */
private ResourceFactory $resourceFactoryMock;

protected function setUp(): void
{
    parent::setUp();

    /** @var ResourceFactory&MockObject $resourceFactoryMock */
    $resourceFactoryMock = $this->createMock(ResourceFactory::class);

    $this->resourceFactoryMock = $resourceFactoryMock;
    $this->subject = new MyController($this->resourceFactoryMock);
}
```

### Undefined Array Key Warnings

**Problem**: Tests throw warnings about missing array keys.
```
Undefined array key "fileId"
```

**Solution**: Always provide all required keys in mock arrays:
```php
// ❌ Incomplete mock data
$requestMock->method('getQueryParams')->willReturn([
    'fileId' => 123,
]);

// ✅ Complete mock data
$requestMock->method('getQueryParams')->willReturn([
    'fileId' => 123,
    'table'  => 'tt_content',
    'P'      => [],
]);
```

### Tests Requiring Functional Setup

**Problem**: Unit tests fail with cache or framework errors.
```
NoSuchCacheException: A cache with identifier "runtime" does not exist.
```

**Solution**: Identify methods that require TYPO3 framework infrastructure and move them to functional tests:
- Methods using `BackendUtility::getPagesTSconfig()`
- Methods calling parent class framework behavior
- Methods requiring global state like `$GLOBALS['TYPO3_CONF_VARS']`

Add comments explaining the limitation:
```php
// Note: getMaxDimensions tests require functional test setup due to BackendUtility dependency
// These are better tested in functional tests
```

### Singleton State Pollution

**Problem**: Tests interfere with each other due to singleton state.

**Solution**: Enable singleton reset in your test class:
```php
final class MyControllerTest extends UnitTestCase
{
    protected bool $resetSingletonInstances = true;

    #[Test]
    public function testWithGlobals(): void
    {
        $GLOBALS['BE_USER'] = $this->createMock(BackendUserAuthentication::class);
        // Test will clean up automatically
    }
}
```

### Exception Flow Issues

**Problem**: Catching and re-throwing exceptions masks the original error.
```php
// ❌ Inner exception caught by outer catch
try {
    $file = $this->factory->getFile($id);
    if ($file->isDeleted()) {
        throw new RuntimeException('Deleted', 1234);
    }
} catch (Exception $e) {
    throw new RuntimeException('Not found', 5678);
}
```

**Solution**: Separate concerns - catch only what you need:
```php
// ✅ Proper exception flow
try {
    $file = $this->factory->getFile($id);
} catch (Exception $e) {
    throw new RuntimeException('Not found', 5678, $e);
}

if ($file->isDeleted()) {
    throw new RuntimeException('Deleted', 1234);
}
```

## Testing DataHandler Hooks

DataHandler hooks (`processDatamap_*`, `processCmdmap_*`) require careful testing as they interact with TYPO3 globals.

### Example: Testing processDatamap_postProcessFieldArray

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Database;

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\MockObject\MockObject;
use TYPO3\CMS\Core\Configuration\ExtensionConfiguration;
use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Http\RequestFactory;
use TYPO3\CMS\Core\Log\LogManager;
use TYPO3\CMS\Core\Log\Logger;
use TYPO3\CMS\Core\Resource\DefaultUploadFolderResolver;
use TYPO3\CMS\Core\Resource\ResourceFactory;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Database\MyDataHandlerHook;

/**
 * Unit tests for MyDataHandlerHook.
 *
 * @covers \Vendor\Extension\Database\MyDataHandlerHook
 */
final class MyDataHandlerHookTest extends UnitTestCase
{
    protected bool $resetSingletonInstances = true;

    private MyDataHandlerHook $subject;

    /** @var ExtensionConfiguration&MockObject */
    private ExtensionConfiguration $extensionConfigurationMock;

    /** @var LogManager&MockObject */
    private LogManager $logManagerMock;

    /** @var ResourceFactory&MockObject */
    private ResourceFactory $resourceFactoryMock;

    /** @var Context&MockObject */
    private Context $contextMock;

    /** @var RequestFactory&MockObject */
    private RequestFactory $requestFactoryMock;

    /** @var DefaultUploadFolderResolver&MockObject */
    private DefaultUploadFolderResolver $uploadFolderResolverMock;

    /** @var Logger&MockObject */
    private Logger $loggerMock;

    protected function setUp(): void
    {
        parent::setUp();

        // Create all required mocks with intersection types for PHPStan compliance
        /** @var ExtensionConfiguration&MockObject $extensionConfigurationMock */
        $extensionConfigurationMock = $this->createMock(ExtensionConfiguration::class);

        /** @var LogManager&MockObject $logManagerMock */
        $logManagerMock = $this->createMock(LogManager::class);

        /** @var ResourceFactory&MockObject $resourceFactoryMock */
        $resourceFactoryMock = $this->createMock(ResourceFactory::class);

        /** @var Context&MockObject $contextMock */
        $contextMock = $this->createMock(Context::class);

        /** @var RequestFactory&MockObject $requestFactoryMock */
        $requestFactoryMock = $this->createMock(RequestFactory::class);

        /** @var DefaultUploadFolderResolver&MockObject $uploadFolderResolverMock */
        $uploadFolderResolverMock = $this->createMock(DefaultUploadFolderResolver::class);

        /** @var Logger&MockObject $loggerMock */
        $loggerMock = $this->createMock(Logger::class);

        // Configure extension configuration mock with willReturnCallback
        $extensionConfigurationMock
            ->method('get')
            ->willReturnCallback(function ($extension, $key) {
                if ($extension === 'my_extension') {
                    return match ($key) {
                        'enableFeature' => true,
                        'timeout'       => 30,
                        default         => null,
                    };
                }

                return null;
            });

        // Configure log manager to return logger mock
        $logManagerMock
            ->method('getLogger')
            ->with(MyDataHandlerHook::class)
            ->willReturn($loggerMock);

        // Assign mocks to properties
        $this->extensionConfigurationMock = $extensionConfigurationMock;
        $this->logManagerMock             = $logManagerMock;
        $this->resourceFactoryMock        = $resourceFactoryMock;
        $this->contextMock                = $contextMock;
        $this->requestFactoryMock         = $requestFactoryMock;
        $this->uploadFolderResolverMock   = $uploadFolderResolverMock;
        $this->loggerMock                 = $loggerMock;

        // Create subject with all dependencies
        $this->subject = new MyDataHandlerHook(
            $this->extensionConfigurationMock,
            $this->logManagerMock,
            $this->resourceFactoryMock,
            $this->contextMock,
            $this->requestFactoryMock,
            $this->uploadFolderResolverMock,
        );
    }

    #[Test]
    public function constructorInitializesWithDependencyInjection(): void
    {
        // Verify subject was created successfully with all dependencies
        self::assertInstanceOf(MyDataHandlerHook::class, $this->subject);
    }

    #[Test]
    public function processDatamapPostProcessFieldArrayHandlesFieldCorrectly(): void
    {
        $status     = 'update';
        $table      = 'tt_content';
        $id         = '123';
        $fieldArray = ['bodytext' => '<p>Content with processing</p>'];

        /** @var DataHandler&MockObject $dataHandlerMock */
        $dataHandlerMock = $this->createMock(DataHandler::class);

        // Mock TCA configuration for RTE field
        $GLOBALS['TCA']['tt_content']['columns']['bodytext']['config'] = [
            'type'        => 'text',
            'enableRichtext' => true,
        ];

        // Test the hook processes the field
        $this->subject->processDatamap_postProcessFieldArray(
            $status,
            $table,
            $id,
            $fieldArray,
            $dataHandlerMock,
        );

        // Assert field was processed (actual assertion depends on implementation)
        self::assertNotEmpty($fieldArray['bodytext']);
    }

    #[Test]
    public function constructorLoadsExtensionConfiguration(): void
    {
        /** @var ExtensionConfiguration&MockObject $configMock */
        $configMock = $this->createMock(ExtensionConfiguration::class);
        $configMock
            ->expects(self::exactly(2))
            ->method('get')
            ->willReturnCallback(function ($extension, $key) {
                self::assertSame('my_extension', $extension);

                return match ($key) {
                    'enableFeature' => true,
                    'timeout'       => 30,
                    default         => null,
                };
            });

        new MyDataHandlerHook(
            $configMock,
            $this->logManagerMock,
            $this->resourceFactoryMock,
            $this->contextMock,
            $this->requestFactoryMock,
            $this->uploadFolderResolverMock,
        );
    }
}
```

**Key Testing Patterns for DataHandler Hooks:**

1. **Intersection Types for PHPStan**: Use `ResourceFactory&MockObject` for strict type compliance
2. **TCA Globals**: Set `$GLOBALS['TCA']` in tests to simulate TYPO3 table configuration
3. **Extension Configuration**: Use `willReturnCallback` with `match` expressions for flexible config mocking
4. **DataHandler Mock**: Create mock for `$dataHandler` parameter (required in hook signature)
5. **Reset Singletons**: Always set `protected bool $resetSingletonInstances = true;`
6. **Constructor DI**: Inject all dependencies via constructor (TYPO3 13+ best practice)

## Testing Time-Dependent Code

Time-dependent code (scheduled tasks, cache expiration, date validation) requires special testing patterns to ensure determinism and avoid flaky tests.

### The Problem

```php
// ❌ Non-deterministic - test results depend on when tests run
public function isExpired(): bool
{
    return time() > $this->expiresAt;
}

public function getAge(): int
{
    return (new \DateTimeImmutable())->diff($this->createdAt)->days;
}
```

### Solution 1: Clock Interface (Recommended)

Create an injectable clock dependency for deterministic time control.

**The Interface:**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Service;

interface ClockInterface
{
    public function now(): \DateTimeImmutable;
}
```

**Production Implementation:**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Service;

final class SystemClock implements ClockInterface
{
    public function now(): \DateTimeImmutable
    {
        return new \DateTimeImmutable();
    }
}
```

**Test Implementation (FakeClock):**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Service;

use Vendor\Extension\Service\ClockInterface;

final class FakeClock implements ClockInterface
{
    private \DateTimeImmutable $currentTime;

    public function __construct(\DateTimeImmutable $initialTime)
    {
        $this->currentTime = $initialTime;
    }

    public function now(): \DateTimeImmutable
    {
        return $this->currentTime;
    }

    public function setTime(\DateTimeImmutable $time): void
    {
        $this->currentTime = $time;
    }

    public function advance(\DateInterval $interval): void
    {
        $this->currentTime = $this->currentTime->add($interval);
    }

    public function advanceSeconds(int $seconds): void
    {
        $this->advance(new \DateInterval("PT{$seconds}S"));
    }

    public function advanceMinutes(int $minutes): void
    {
        $this->advance(new \DateInterval("PT{$minutes}M"));
    }

    public function advanceHours(int $hours): void
    {
        $this->advance(new \DateInterval("PT{$hours}H"));
    }

    public function advanceDays(int $days): void
    {
        $this->advance(new \DateInterval("P{$days}D"));
    }
}
```

**Using the Clock in Production Code:**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Domain\Model;

use Vendor\Extension\Service\ClockInterface;

final class Token
{
    private \DateTimeImmutable $expiresAt;

    public function __construct(
        private readonly ClockInterface $clock,
        int $ttlSeconds = 3600,
    ) {
        $this->expiresAt = $this->clock->now()->modify("+{$ttlSeconds} seconds");
    }

    public function isExpired(): bool
    {
        return $this->clock->now() > $this->expiresAt;
    }

    public function getSecondsRemaining(): int
    {
        $diff = $this->expiresAt->getTimestamp() - $this->clock->now()->getTimestamp();
        return max(0, $diff);
    }
}
```

**Testing with FakeClock:**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Domain\Model;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Domain\Model\Token;
use Vendor\Extension\Tests\Unit\Service\FakeClock;

final class TokenTest extends UnitTestCase
{
    private FakeClock $clock;

    protected function setUp(): void
    {
        parent::setUp();
        // Start at a known, fixed time
        $this->clock = new FakeClock(new \DateTimeImmutable('2026-01-15 10:00:00'));
    }

    #[Test]
    public function newTokenIsNotExpired(): void
    {
        $token = new Token($this->clock, ttlSeconds: 3600);

        self::assertFalse($token->isExpired());
    }

    #[Test]
    public function tokenExpiresAfterTtl(): void
    {
        $token = new Token($this->clock, ttlSeconds: 3600);

        // Advance time past expiration
        $this->clock->advanceSeconds(3601);

        self::assertTrue($token->isExpired());
    }

    #[Test]
    public function tokenNotExpiredJustBeforeTtl(): void
    {
        $token = new Token($this->clock, ttlSeconds: 3600);

        // Advance time to just before expiration
        $this->clock->advanceSeconds(3599);

        self::assertFalse($token->isExpired());
    }

    #[Test]
    public function getSecondsRemainingReturnsCorrectValue(): void
    {
        $token = new Token($this->clock, ttlSeconds: 3600);

        $this->clock->advanceSeconds(1000);

        self::assertSame(2600, $token->getSecondsRemaining());
    }

    #[Test]
    public function getSecondsRemainingReturnsZeroWhenExpired(): void
    {
        $token = new Token($this->clock, ttlSeconds: 3600);

        $this->clock->advanceSeconds(7200);

        self::assertSame(0, $token->getSecondsRemaining());
    }
}
```

### Solution 2: Symfony Clock Component (PHP 8.3+)

For projects using Symfony components, use `symfony/clock`:

```bash
composer require symfony/clock
```

**Using PSR-20 Clock Interface:**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Service;

use Psr\Clock\ClockInterface;

final class CacheService
{
    public function __construct(
        private readonly ClockInterface $clock,
        private readonly int $ttlSeconds = 3600,
    ) {}

    public function isValid(\DateTimeImmutable $cachedAt): bool
    {
        $expiresAt = $cachedAt->modify("+{$this->ttlSeconds} seconds");
        return $this->clock->now() < $expiresAt;
    }
}
```

**Testing with MockClock:**

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Service;

use PHPUnit\Framework\Attributes\Test;
use Symfony\Component\Clock\MockClock;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Service\CacheService;

final class CacheServiceTest extends UnitTestCase
{
    #[Test]
    public function cacheIsValidWithinTtl(): void
    {
        $clock = new MockClock('2026-01-15 10:00:00');
        $service = new CacheService($clock, ttlSeconds: 3600);

        $cachedAt = new \DateTimeImmutable('2026-01-15 09:30:00');

        self::assertTrue($service->isValid($cachedAt));
    }

    #[Test]
    public function cacheIsInvalidAfterTtl(): void
    {
        $clock = new MockClock('2026-01-15 12:00:00');
        $service = new CacheService($clock, ttlSeconds: 3600);

        $cachedAt = new \DateTimeImmutable('2026-01-15 09:30:00');

        self::assertFalse($service->isValid($cachedAt));
    }

    #[Test]
    public function clockCanBeAdvanced(): void
    {
        $clock = new MockClock('2026-01-15 10:00:00');
        $service = new CacheService($clock, ttlSeconds: 3600);

        $cachedAt = $clock->now();

        // Initially valid
        self::assertTrue($service->isValid($cachedAt));

        // Advance past TTL
        $clock->modify('+2 hours');

        // Now invalid
        self::assertFalse($service->isValid($cachedAt));
    }
}
```

### Solution 3: Carbon (For Legacy Code)

If your project uses Carbon for date manipulation:

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Tests\Unit\Service;

use Carbon\Carbon;
use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use Vendor\Extension\Service\ScheduleService;

final class ScheduleServiceTest extends UnitTestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        // Set a fixed "now" for all Carbon instances
        Carbon::setTestNow('2026-01-15 10:00:00');
    }

    protected function tearDown(): void
    {
        // CRITICAL: Always reset Carbon after tests
        Carbon::setTestNow();
        parent::tearDown();
    }

    #[Test]
    public function isBusinessHoursReturnsTrueDuringWorkday(): void
    {
        Carbon::setTestNow('2026-01-15 14:00:00'); // Wednesday 2pm

        $service = new ScheduleService();

        self::assertTrue($service->isBusinessHours());
    }

    #[Test]
    public function isBusinessHoursReturnsFalseOnWeekend(): void
    {
        Carbon::setTestNow('2026-01-18 14:00:00'); // Saturday 2pm

        $service = new ScheduleService();

        self::assertFalse($service->isBusinessHours());
    }
}
```

**Warning**: Carbon's `setTestNow()` uses global state. Always reset in `tearDown()` to prevent test pollution.

### Comparison of Approaches

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Clock Interface (DI)** | No global state, explicit, testable | Requires refactoring | New code, clean architecture |
| **Symfony Clock** | PSR-20 standard, well-tested | Adds dependency | Symfony-based projects |
| **Carbon setTestNow** | Quick, no code changes | Global state, must reset | Legacy code, quick fixes |

### Best Practices

1. **Always use fixed times** - Never rely on `time()` or `new \DateTime()` in tests
2. **Use meaningful dates** - Choose dates that make test intent clear (weekday vs weekend, etc.)
3. **Reset global state** - If using Carbon or other global mocks, always reset in `tearDown()`
4. **Test edge cases**:
   - Exactly at boundary (e.g., exactly when TTL expires)
   - One second before/after boundary
   - Timezone transitions (if applicable)
   - Leap years, daylight saving time

5. **Document time dependencies** - Add comments explaining why specific times are chosen:

```php
#[Test]
public function schedulerRunsAtMidnight(): void
{
    // Use 23:59:59 to verify job doesn't run early
    $this->clock->setTime(new \DateTimeImmutable('2026-01-15 23:59:59'));
    self::assertFalse($this->scheduler->shouldRun());

    // Advance to exactly midnight
    $this->clock->advanceSeconds(1);
    self::assertTrue($this->scheduler->shouldRun());
}
```

## Test Patterns for TYPO3 Extensions

### Coverage Attributes: #[CoversClass] and #[CoversNothing]

Every test class MUST declare which production class it covers using `#[CoversClass]`. This is enforced when `beStrictAboutCoverageMetadata` is enabled in PHPUnit configuration.

```php
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\UsesClass;
use Vendor\Extension\Domain\Model\Translation;
use Vendor\Extension\Domain\Repository\TranslationRepository;

#[CoversClass(TranslationRepository::class)]
#[UsesClass(Translation::class)]
final class TranslationRepositoryTest extends UnitTestCase
{
    // ...
}
```

**`#[CoversNothing]`** is used for tests that do not cover application code -- for example, security-oriented tests that validate PHP/libxml behavior rather than extension logic:

```php
use PHPUnit\Framework\Attributes\CoversNothing;

#[CoversNothing]
final class XxeProtectionTest extends UnitTestCase
{
    #[Test]
    public function libxmlDisablesExternalEntityLoading(): void
    {
        // This tests PHP/libxml behavior, not application code
        $previousValue = libxml_disable_entity_loader(true);
        self::assertTrue($previousValue || true);
    }
}
```

### #[UsesClass] for Domain Model Dependencies

When a test exercises domain models indirectly (e.g., a repository test creates model instances), declare them with `#[UsesClass]` to keep coverage reports accurate:

```php
#[CoversClass(TranslationService::class)]
#[UsesClass(Translation::class)]
#[UsesClass(Language::class)]
final class TranslationServiceTest extends UnitTestCase
{
    // Translation and Language are used by TranslationService but not the
    // primary subject under test — #[UsesClass] prevents coverage gaps
}
```

### Mocking All Repository Dependencies

Always mock repository dependencies with `$this->createMock()`. Repositories interact with the database and cannot function in unit tests:

```php
#[CoversClass(TranslationService::class)]
final class TranslationServiceTest extends UnitTestCase
{
    private TranslationService $subject;

    /** @var TranslationRepository&MockObject */
    private TranslationRepository $translationRepositoryMock;

    /** @var LanguageRepository&MockObject */
    private LanguageRepository $languageRepositoryMock;

    protected function setUp(): void
    {
        parent::setUp();

        /** @var TranslationRepository&MockObject $translationRepositoryMock */
        $translationRepositoryMock = $this->createMock(TranslationRepository::class);

        /** @var LanguageRepository&MockObject $languageRepositoryMock */
        $languageRepositoryMock = $this->createMock(LanguageRepository::class);

        $this->translationRepositoryMock = $translationRepositoryMock;
        $this->languageRepositoryMock = $languageRepositoryMock;

        $this->subject = new TranslationService(
            $this->translationRepositoryMock,
            $this->languageRepositoryMock,
        );
    }
}
```

### Testing Fluent Setters (return $this)

Domain models with fluent setters (`return $this`) need two assertions: verify the value was set AND verify the setter returns the object itself:

```php
#[Test]
public function setValueSetsValueAndReturnsSelf(): void
{
    $result = $this->subject->setValue('test-value');

    // Verify the value was actually set
    self::assertSame('test-value', $this->subject->getValue());

    // Verify fluent interface — setter returns $this
    self::assertSame($this->subject, $result);
}

#[Test]
public function setKeySetsKeyAndReturnsSelf(): void
{
    $result = $this->subject->setKey('my-key');

    self::assertSame('my-key', $this->subject->getKey());
    self::assertSame($this->subject, $result);
}
```

**Why test both:** A setter could accidentally return `new self()` instead of `$this`, or return nothing at all. The `assertSame($this->subject, $result)` check catches both bugs.

### Testing Auto-Created Translations

When an extension auto-creates translation stubs (e.g., for missing locale entries), test that the auto-created flag is set and the placeholder value is correct:

```php
#[Test]
public function autoCreatedTranslationHasCorrectProperties(): void
{
    $translation = Translation::createAutoTranslation(
        key: 'label.greeting',
        locale: 'de',
    );

    // Auto-created flag must be true
    self::assertTrue($translation->isAutoCreated());

    // Value should contain a placeholder indicating it needs translation
    self::assertStringContainsString('[TRANSLATE]', $translation->getValue());

    // Key and locale must be preserved
    self::assertSame('label.greeting', $translation->getKey());
    self::assertSame('de', $translation->getLocale());
}

#[Test]
public function manualTranslationIsNotAutoCreated(): void
{
    $translation = new Translation();
    $translation->setKey('label.greeting');
    $translation->setValue('Hallo');

    self::assertFalse($translation->isAutoCreated());
    self::assertSame('Hallo', $translation->getValue());
}
```

## Resources

- [TYPO3 Unit Testing Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Testing/UnitTests.html)
- [PHPUnit Documentation](https://phpunit.de/documentation.html)
- [PHPUnit 11 Migration Guide](https://phpunit.de/announcements/phpunit-11.html)
- [TYPO3 DataHandler Hooks](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Hooks/DataHandler/Index.html)
- [Symfony Clock Component](https://symfony.com/doc/current/clock.html)
- [PSR-20 Clock Interface](https://www.php-fig.org/psr/psr-20/)
