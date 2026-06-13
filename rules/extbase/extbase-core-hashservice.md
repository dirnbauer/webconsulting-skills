---
id: extbase-core-hashservice
title: "Use the Core HashService with an extra secret, not the removed Extbase one"
category: extbase
severity: error
appliesTo: ["**/Classes/**/*.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when signing or validating a value with an HMAC."
---
# Use the Core HashService with an extra secret

`TYPO3\CMS\Extbase\Security\Cryptography\HashService` was removed. Inject
`TYPO3\CMS\Core\Crypto\HashService` and pass an `$additionalSecret` to every call —
the secret scopes the HMAC so a token signed for one purpose can't be replayed elsewhere.

**Do:** inject `Core\Crypto\HashService`; call `hmac()` / `appendHmac()` / `validateAndStripHmac()` with a purpose-specific secret.
**Don't:** reference the old Extbase `HashService`, or call without the secret argument.

```php
use TYPO3\CMS\Core\Crypto\HashService;

final class TokenService
{
    public function __construct(private readonly HashService $hashService) {}

    public function sign(string $payload): string
    {
        // secret scopes the signature to this feature
        return $this->hashService->appendHmac($payload, 'webcon_example/token');
    }

    public function verify(string $signed): string
    {
        return $this->hashService->validateAndStripHmac($signed, 'webcon_example/token');
    }
}
```

> Why: `Extbase\...\HashService` was removed (#102763, v13) and is absent in v14;
> `Core\Crypto\HashService::hmac(string $input, string $additionalSecret,
> HashAlgo $algo = HashAlgo::SHA1)` requires the secret argument (verified in vendor).
