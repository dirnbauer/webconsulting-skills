# Dual Version (v13 + v14) Compatibility Patterns

> **Companion to:** `dual-version-compatibility.md` (v12 + v13).
> **Context:** TYPO3 v14.3 LTS released 2026-04-21. Many Netresearch extensions continue supporting v13 LTS alongside v14 during the v13 → v14 migration window (v13 free-support end ≈ 2027-10-31).

---

## Version constraint strategy

### composer.json

```json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.4 || ^14.3"
    }
}
```

Alternative allowing pre-14.3 sprint releases (not recommended for prod):

```json
"typo3/cms-core": "^13.4 || ^14.0"
```

### ext_emconf.php

```php
'constraints' => [
    'depends' => [
        'typo3' => '13.4.0-14.3.99',
        'php' => '8.2.0-8.5.99',
    ],
],
```

> Note: `ext_emconf.php` itself is deprecated in v14.2 (#108345). Keep it for classic-mode support, but mirror all metadata in `composer.json` — v15 will remove `ext_emconf.php` entirely.

---

## Rector configuration

```php
// rector.php - DUAL v13+v14
$rectorConfig->sets([
    LevelSetList::UP_TO_PHP_82,
    Typo3LevelSetList::UP_TO_TYPO3_13, // NOT UP_TO_TYPO3_14
    Typo3SetList::CODE_QUALITY,
    Typo3SetList::GENERAL,
]);
```

**Reason:** `UP_TO_TYPO3_14` applies the v14 Fluid 5 strict-typing + FAL strict-typing + `HashService` removal rules that would break v13. Use the v14 rule set on a dedicated v14-only branch.

To run just a single v14 rule against the dual codebase:

```bash
vendor/bin/rector process --only=Ssch\\TYPO3Rector\\Rules\\v14\\v0\\MigrateRemovedMailMessageSendRector Classes/
```

---

## API compatibility decision matrix

| Purpose | v13 + v14 (dual-safe) | v14-only (avoid) |
|---|---|---|
| Frontend page information | `$request->getAttribute('frontend.page.information')` | (same — identical API) |
| TypoScriptFrontendController | **avoid entirely** (removed in v14) | — |
| Site | `$request->getAttribute('site')` | — |
| Language | `$request->getAttribute('language')` | — |
| Password hashing | `PasswordHashFactory` + `BackendPasswordHasher` / `FrontendPasswordHasher` | — |
| HMAC / signing | `HashService` from `TYPO3\\CMS\\Extbase\\Security\\Cryptography\\HashService` in v13 **only** — class is **removed in v14** | use `TYPO3\\CMS\\Core\\Crypto\\HashService` in v14 |
| Magic repo finders (`findByX()`) | **avoid** — removed in v14; use `createQuery()` | |
| Fluid view rendering | `Core\\View\\ViewFactoryInterface` (available v13+, preferred); `StandaloneView` only if v13-only | `StandaloneView` removed in v14 |
| TCA search | use explicit search TCA (#106972 pattern); `control.searchFields` still works in v13, removed in v14 | `control.searchFields` |
| Extbase annotations | PHP attributes (`#[Validate]`) | docblock `@Validate` (removed in v14) |
| ext_tables.php | **still supported in v14.3** but deprecated — split now into `Configuration/Backend/Modules.php` + `Routes.php` | |
| Plugin registration via `list_type` | v13 still accepts; v14 removed. Use CType-only plugins (dual-safe in v13.4+) | `list_type` |

---

## HashService replacement (breaking for v14)

v13 usage:

```php
use TYPO3\CMS\Extbase\Security\Cryptography\HashService;

class Foo {
    public function __construct(private readonly HashService $hashService) {}
}
```

v14: `HashService` is gone. Use `Core\Crypto\HashService` if you only need HMAC, or the new symmetric cipher service (#108002) for encryption:

```php
// dual-safe adapter pattern
if (class_exists(\TYPO3\CMS\Core\Crypto\HashService::class)) {
    // v14+: Core HashService
    $hashService = GeneralUtility::makeInstance(\TYPO3\CMS\Core\Crypto\HashService::class);
} else {
    // v13: Extbase HashService
    $hashService = GeneralUtility::makeInstance(\TYPO3\CMS\Extbase\Security\Cryptography\HashService::class);
}
```

Better: inject via constructor with a shim service defined in `Services.yaml` per TYPO3 major.

---

## Fluid 5 dual-mode templates

**v13 (Fluid 4.x)** vs **v14 (Fluid 5)** differences that bite:

1. **Variable names starting with `_`** — forbidden in v14.
   - `{_myVar}` → rename to `{myVar}` or `{my_var}`.
2. **Strict VH argument types** — v14 requires typed args. v13 is forgiving.
   - Dual-safe: add types to all custom ViewHelpers now.
3. **`renderStatic()`** — removed in Fluid 5. Replace with non-static `render()`.
4. **CDATA sections** — preserved in Fluid 5 (v13 stripped them). Only matters if your templates embed `<![CDATA[…]]>`.

**ViewHelper pattern that works in both v13 and v14:**

```php
<?php
declare(strict_types=1);

namespace Vendor\Ext\ViewHelpers;

use TYPO3Fluid\Fluid\Core\ViewHelper\AbstractViewHelper;

final class FooViewHelper extends AbstractViewHelper
{
    public function initializeArguments(): void
    {
        $this->registerArgument('value', 'string', 'The value', true);
    }

    public function render(): string
    {
        return htmlspecialchars((string)$this->arguments['value']);
    }
}
```

---

## TypoLink / TSFE migration

Every v13 extension using `$GLOBALS['TSFE']` must switch before v14:

```php
// DUAL-SAFE (works in v13 and v14)
$pageInfo = $request->getAttribute('frontend.page.information');
$pageId = $pageInfo?->getId() ?? 0;

// v14 dropped $GLOBALS['TSFE'] entirely — NO FALLBACK available in v14
```

If you must support both v13 AND v12 (tri-compat), use the `Typo3Version` check from `dual-version-compatibility.md` §Compatibility Layer Pattern.

---

## Security attributes (v14 excellence bonus)

v14 introduces `#[Authorize]` and `#[RateLimit]` attributes in `TYPO3\CMS\Extbase\Attribute`. These classes **do not exist in v13**. Naively adding `use` + the attribute to a dual-version extension will:

- Not break at `use`-statement parse time (PHP `use` aliases are lazy; they don't autoload).
- Break the first time v13 **reflects** the attributes on the method (e.g., `ReflectionMethod::getAttributes()` with `newInstance()` triggers autoload of the missing class → fatal `Class not found`).

**If v13 never reflects these attributes on your controllers, you can add them without guard** — v13 will simply ignore them at dispatch time because v13's dispatcher doesn't know to read them. Verify for your specific code path.

**Safer: ship a polyfill stub for v13.** In a file conditionally loaded in `ext_localconf.php`:

```php
// Classes/Compat/AttributeStubs.php (loaded only on v13)
if (!class_exists(\TYPO3\CMS\Extbase\Attribute\Authorize::class)) {
    #[\Attribute(\Attribute::TARGET_METHOD | \Attribute::TARGET_CLASS)]
    final class Authorize { public function __construct(bool $requireLogin = true, array $requireGroups = []) {} }
}
if (!class_exists(\TYPO3\CMS\Extbase\Attribute\RateLimit::class)) {
    #[\Attribute(\Attribute::TARGET_METHOD)]
    final class RateLimit { public function __construct(int $limit, string $interval) {} }
}
```

```php
// ext_localconf.php
if ((new \TYPO3\CMS\Core\Information\Typo3Version())->getMajorVersion() < 14) {
    require __DIR__ . '/../Classes/Compat/AttributeStubs.php';
}
```

Then in your controller — works on both versions:

```php
use TYPO3\CMS\Extbase\Attribute\Authorize;
use TYPO3\CMS\Extbase\Attribute\RateLimit;

final class LoginController
{
    #[Authorize(requireLogin: false)]
    #[RateLimit(limit: 5, interval: '1m')]
    public function submitAction(): ResponseInterface { /* ... */ }
}
```

Treat this as **progressive enhancement**: v14 users get real rate-limiting; v13 users get no-op stubs (the attributes are present but v13's dispatcher ignores them). v15 will remove the stub loader when v13 support is dropped.

> **Why not `class_exists()` at runtime?** PHP attributes are declarative syntax attached to methods/classes at parse time. You can't wrap an attribute in a runtime conditional. The only valid alternatives are: (a) ship the stub classes, (b) branch the whole class definition (two controller files selected via service factory), (c) forgo the attribute on v13.

---

## CI matrix

```yaml
matrix:
  include:
    - php: '8.2'
      typo3: '^13.4'
    - php: '8.3'
      typo3: '^13.4'
    - php: '8.4'
      typo3: '^13.4'
    - php: '8.2'
      typo3: '^14.3'
    - php: '8.3'
      typo3: '^14.3'
    - php: '8.4'
      typo3: '^14.3'
    - php: '8.5'
      typo3: '^14.3'
```

PHPUnit major is unified: testing-framework `^9` works with both v13 and v14 cores.

---

## Conformance scoring adjustments

| Criterion | Single v14 | Dual v13+v14 |
|---|---|---|
| Uses v13-only API (e.g. `HashService`, magic finders) | N/A | -10 points |
| Uses v14-only API with guard | N/A | +0 |
| Uses v14-only API without guard | N/A | Critical — blocks v13 install |
| No deprecated API in v14 cycle | +0 | +0 |
| `#[Authorize]` with guard for v13 | N/A | +3 excellence |
| `#[RateLimit]` with guard for v13 | N/A | +2 excellence |
| CI tests v13 AND v14 on PHP 8.2 + 8.3 minimum | Required | Required |
| CI also tests PHP 8.5 on v14 | +1 excellence | +1 excellence |

---

## Documentation example

```markdown
## Compatibility

| TYPO3 | PHP | Status |
|---|---|---|
| 14.3 LTS | 8.2 – 8.5 | Supported (current LTS; gold standard) |
| 13.4 LTS | 8.2 – 8.4 | Supported |
| 12.4 LTS | 8.2 – 8.3 | Use v2.x of this extension |
```

---

## Checklist for v13+v14 dual support

- [ ] `composer.json`: `"typo3/cms-core": "^13.4 || ^14.3"`
- [ ] `composer.json` carries full metadata (don't rely on `ext_emconf.php` only — deprecated)
- [ ] `ext_emconf.php`: constraint `13.4.0-14.3.99`, PHP `8.2.0-8.5.99`
- [ ] No `$GLOBALS['TSFE']` anywhere — use `$request` attributes
- [ ] No `HashService` from Extbase — use adapter or Core HashService
- [ ] No magic Extbase repo finders (`findByX`, `findOneByX`, `countByX`)
- [ ] Fluid VHs strict-typed (`registerArgument` with type, `render(): string`)
- [ ] No leading-underscore variable names in Fluid templates
- [ ] No removed TCA options (`subtype_value_field`, `control.searchFields`, `eval=year`, `is_static`, `pages.url`, `tt_content.list_type`)
- [ ] No removed hooks in EXT:form (migrated to PSR-14 events)
- [ ] Rector set: `UP_TO_TYPO3_13` (NOT `UP_TO_TYPO3_14`)
- [ ] CI matrix exercises both v13 and v14
- [ ] `ext_tables.php` split preview into `Configuration/Backend/*.php` (future-proof for v15)
- [ ] `#[Authorize]` / `#[RateLimit]` on sensitive actions (guarded with `class_exists()`)
