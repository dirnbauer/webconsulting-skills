---
id: di-no-objectmanager
title: "Inject collaborators via constructor DI, never ObjectManager"
category: di
severity: error
appliesTo: ["**/Classes/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when a class needs another service, repository, or framework component."
---
# Inject collaborators via constructor DI, never ObjectManager

Obtain services through constructor injection. The Extbase `ObjectManager` was
removed in v12; `GeneralUtility::makeInstance()` is only for runtime/value objects
that the container cannot inject (e.g. an instance built from a runtime class name).

**Do:** declare dependencies as constructor parameters; let the symfony container wire them.
**Don't:** call `ObjectManager->get()`, `$this->objectManager`, or reach for `makeInstance()` for injectable services.

```php
final class NewsletterService
{
    public function __construct(
        private readonly NewsletterRepository $newsletterRepository,
        private readonly LoggerInterface $logger,
    ) {}
}

// runtime object only (class name known at runtime, not a service): OK
$instance = GeneralUtility::makeInstance($runtimeClassName);
```

> Why: the Extbase `ObjectManager` was deprecated in v11 (#94619) and removed in v12
> (#96107); constructor DI is the supported wiring. `GeneralUtility::makeInstance()`
> remains for non-injectable/runtime objects only.
