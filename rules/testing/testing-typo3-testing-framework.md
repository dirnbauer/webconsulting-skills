---
id: testing-typo3-testing-framework
title: "Extend the TYPO3 testing-framework base classes and test the CI matrix"
category: testing
severity: warning
appliesTo: ["**/Tests/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when writing or organizing unit/functional tests for a TYPO3 extension."
---
# Extend the TYPO3 testing-framework base classes and test the CI matrix

Unit tests extend `TYPO3\TestingFramework\Core\Unit\UnitTestCase`; functional tests
extend `TYPO3\TestingFramework\Core\Functional\FunctionalTestCase`. Many v14 core classes
are `final`, so test against their public behavior or the interfaces they implement rather
than mocking the concrete class. Run the suite across the LTS lines you support (12 / 13 / 14.3).

**Do:** subclass the framework base classes; mock interfaces/abstractions; matrix CI over supported LTS + PHP versions.
**Don't:** roll your own PHPUnit bootstrap, or try to `createMock()` a `final` class.

```php
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class NewsletterServiceTest extends FunctionalTestCase
{
    protected array $testExtensionsToLoad = ['webcon_example'];

    public function test_subscribes_a_new_address(): void
    {
        $service = $this->get(NewsletterService::class);
        self::assertTrue($service->subscribe('user@example.org'));
    }
}
```

> Why: `UnitTestCase` / `FunctionalTestCase` live under `TYPO3\TestingFramework\Core\*`
> (verified in vendor); typo3/testing-framework targets PHPUnit
> `^11.2.5 || ^12.1.2 || ^13.0.2`. Final core classes can't be mocked — test behavior/interfaces.
