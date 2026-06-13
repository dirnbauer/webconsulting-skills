---
id: security-escape-output-and-csp
title: "Escape output, ship a per-extension CSP, and guard actions"
category: security
severity: error
appliesTo: ["**/Classes/**/*.php", "**/Resources/Private/**/*.html", "**/Configuration/ContentSecurityPolicies.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when rendering user-influenced output, registering CSP, or exposing a controller action."
---
# Escape output, ship a per-extension CSP, and guard actions

Escape everything that reaches HTML (Fluid escapes by default — don't bypass it for
untrusted data). Ship a Content Security Policy via `Configuration/ContentSecurityPolicies.php`
returning a `Map` of scope → `MutationCollection`. Protect frontend actions that change
state or need a session with `#[Authorize]` (and validate CSRF tokens where applicable).

**Do:** keep Fluid escaping on; declare a CSP map of mutations; gate sensitive actions with `#[Authorize]`.
**Don't:** echo raw request data, run inline scripts without a CSP nonce, or leave state-changing actions unguarded.

```php
// Configuration/ContentSecurityPolicies.php
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Directive;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Mutation;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\MutationCollection;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\MutationMode;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Scope;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\SourceKeyword;
use TYPO3\CMS\Core\Type\Map;

return Map::fromEntries([
    Scope::frontend(),
    new MutationCollection(
        new Mutation(MutationMode::Extend, Directive::ScriptSrc, SourceKeyword::self),
    ),
]);
```

> Why: `Configuration/ContentSecurityPolicies.php` (scope → `MutationCollection`) is the
> v14 extension-level CSP mechanism (verified against core `cms-backend`/`cms-frontend`);
> per-site overrides use `csp.yaml`. Escaping + CSP + access checks defend against XSS/CSRF.
