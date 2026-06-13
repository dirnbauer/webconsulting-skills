---
id: extbase-attributes-not-annotations
title: "Use Extbase PHP attributes, not the removed Annotation namespace"
category: extbase
severity: error
appliesTo: ["**/Classes/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when adding validation, ORM, or access metadata to Extbase models and controllers."
---
# Use Extbase PHP attributes, not the removed Annotation namespace

Extbase metadata lives under `TYPO3\CMS\Extbase\Attribute\*` as native PHP 8 attributes.
The `TYPO3\CMS\Extbase\Annotation\*` namespace (and Doctrine-style `@TYPO3\...` docblocks)
is gone. v14 also adds method attributes `#[Authorize]` and `#[RateLimit]`.

**Do:** use `#[Validate]`, `#[IgnoreValidation]`, `#[ORM\Lazy]`, `#[Authorize]`, `#[RateLimit]`.
**Don't:** use `@TYPO3\CMS\Extbase\Annotation\Validate(...)` docblocks or the `Annotation\` namespace.

Pass `#[Validate]` arguments explicitly (`#[Validate('EmailAddress')]`); the array
config form (`#[Validate(['validator' => ...])]`) is deprecated for removal in v15.

```php
use TYPO3\CMS\Extbase\Attribute\Authorize;
use TYPO3\CMS\Extbase\Attribute\RateLimit;
use TYPO3\CMS\Extbase\Attribute\Validate;
use TYPO3\CMS\Extbase\Attribute\ORM\Lazy;

final class Subscriber extends AbstractEntity
{
    #[Lazy]
    protected ?ObjectStorage $tags = null;
}

final class SubscriptionController extends ActionController
{
    #[Authorize(requireLogin: true)]
    #[RateLimit(limit: 5, interval: '15 minutes')]
    public function subscribeAction(#[Validate('EmailAddress')] string $email): ResponseInterface
    {
        // ...
    }
}
```

> Why: the `Annotation\*` namespace is removed; attributes live in
> `TYPO3\CMS\Extbase\Attribute\*`. `Authorize(callback|requireLogin|requireGroups)` and
> `RateLimit(limit, interval, policy, message)` are v14 method attributes (verified in vendor).
