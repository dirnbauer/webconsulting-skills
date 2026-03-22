---
name: typo3-extension-upgrade
description: >-
  Systematic TYPO3 extension upgrades to newer LTS versions. Covers Extension Scanner,
  Rector, Fractor, PHPStan, and testing. Use when working with extension, upgrade,
  fractor, rector, migration.
compatibility: TYPO3 14.x
metadata:
  version: "1.1.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Extension Upgrade Skill

Systematic framework for upgrading TYPO3 extensions **to TYPO3 v14** (and verifying them on v14).

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

> **Scope**: Extension code upgrades only. NOT for TYPO3 project/core upgrades.

## Upgrade Toolkit

| Tool | Purpose | Files |
|------|---------|-------|
| Extension Scanner | Diagnose **PHP** deprecations / removals in scanned classes | TYPO3 Backend (does **not** analyze Fluid, TypoScript, FlexForm, or YAML — use Fractor + manual review there) |
| Rector | Automated PHP migrations | `.php` |
| Fractor | Non-PHP migrations (see `typo3-fractor` skill) | FlexForms, TypoScript, YAML, Fluid |
| PHPStan | Static analysis | `.php` |

## Planning Phase (Required)

Before ANY code changes for major upgrades:

1. **List all files with hardcoded versions** (composer.json, CI, Docker, Rector)
2. **Document scope** - how many places need changes?
3. **Present plan to user** for approval
4. **Track progress** with todo list

### Pre-Upgrade Checklist

- [ ] Extension key and current TYPO3 version documented
- [ ] Target TYPO3 **v14.x** confirmed
- [ ] Current PHP version and target PHP version noted
- [ ] All deprecation warnings from logs collected
- [ ] Extension Scanner report reviewed
- [ ] Dependencies checked for target version compatibility

## Upgrade Workflow

### 1. Prepare Environment

```bash
# Create backup/snapshot
ddev snapshot --name=before-upgrade

# Verify git is clean
git status

# Create feature branch
git checkout -b feature/typo3-14-upgrade
```

> **PHP version requirement:** Rector and Fractor load your project's autoloader, which means
> TYPO3 v14 packages are parsed by PHP. You **must** run these tools with PHP 8.2+ (matching
> TYPO3 v14's minimum). If your local PHP is older, use DDEV (`ddev exec vendor/bin/rector ...`)
> or a Docker container. **Do not skip Rector/Fractor and do manual replacements instead** --
> the tools catch patterns that are easy to miss manually (namespace renames, FlexForm
> structure changes, TypoScript condition syntax).

### 2. Install Upgrade Tools

Add the upgrade tools as dev dependencies **before** updating version constraints:

```bash
composer require --dev ssch/typo3-rector a9f/typo3-fractor
```

This ensures the tools can analyze your code against the target version's rules.

### 3. Update Version Constraints

```json
// composer.json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^14.0"
    }
}
```

```php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'constraints' => [
        'depends' => [
            'typo3' => '14.0.0-14.99.99',
            'php' => '8.2.0-8.5.99',
        ],
    ],
];
```

### 4. Run Rector

Rector handles PHP code migrations automatically.

#### Configuration

```php
<?php
// rector.php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
        __DIR__ . '/Configuration',
        __DIR__ . '/Tests',
    ])
    ->withSkip([
        __DIR__ . '/Resources',
    ])
    ->withSets([
        // PHP version upgrades
        LevelSetList::UP_TO_PHP_82,
        
        // TYPO3 upgrades (v14 target — adjust if you intentionally stop at v13)
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ])
    ->withImportNames();
```

#### Run Rector

```bash
# Dry run first
vendor/bin/rector process --dry-run

# Review changes, then apply
vendor/bin/rector process

# Review git diff
git diff
```

### 5. Run Fractor

Fractor handles non-PHP file migrations (FlexForms, TypoScript, Fluid, YAML, Htaccess). See the `typo3-fractor` skill for detailed configuration, all available rules, code style options, and custom rule creation.

#### Configuration

```php
<?php
// fractor.php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/Configuration/',
        __DIR__ . '/Resources/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

#### Run Fractor

```bash
# Dry run first
vendor/bin/fractor process --dry-run

# Review changes, then apply
vendor/bin/fractor process
```

### 6. Fix Code Style

```bash
# Run PHP-CS-Fixer
vendor/bin/php-cs-fixer fix

# Verify no issues remain
vendor/bin/php-cs-fixer fix --dry-run
```

### 7. Run PHPStan

```bash
# Analyze codebase
vendor/bin/phpstan analyse

# Fix any reported issues
# Then re-run until clean
```

### 8. Run Tests

```bash
# Unit tests
vendor/bin/phpunit -c Tests/UnitTests.xml

# Functional tests
vendor/bin/phpunit -c Tests/FunctionalTests.xml

# Fix failing tests
```

### 9. Manual Testing

```bash
# Test in target TYPO3 version
ddev composer require "typo3/cms-core:^14.0" --no-update
ddev composer update
ddev typo3 cache:flush

# Test all extension functionality:
# - Backend modules
# - Frontend plugins
# - CLI commands
# - Scheduler tasks
```

## Common Migration Patterns

### ViewFactory (Replaces StandaloneView)

```php
// ❌ OLD (legacy Fluid standalone rendering; prefer Core ViewFactory on TYPO3 v14)
use TYPO3\CMS\Fluid\View\StandaloneView;

$view = GeneralUtility::makeInstance(StandaloneView::class);
$view->setTemplatePathAndFilename('...');

// ✅ NEW (TYPO3 v14)
use TYPO3\CMS\Core\View\ViewFactoryInterface;
use TYPO3\CMS\Core\View\ViewFactoryData;

public function __construct(
    private readonly ViewFactoryInterface $viewFactory,
) {}

public function render(ServerRequestInterface $request): string
{
    $viewFactoryData = new ViewFactoryData(
        templateRootPaths: ['EXT:my_ext/Resources/Private/Templates'],
        request: $request,
    );
    $view = $this->viewFactory->create($viewFactoryData);
    $view->assign('data', $data);
    return $view->render('MyTemplate');
}
```

### Controller ResponseInterface

```php
// ❌ OLD (v11 and earlier)
public function listAction(): void
{
    $this->view->assign('items', $items);
}

// ✅ Required since TYPO3 v12 (still mandatory in v14)
public function listAction(): ResponseInterface
{
    $this->view->assign('items', $items);
    return $this->htmlResponse();
}
```

### PSR-14 Events (Replace Hooks)

```php
// ❌ OLD (hooks deprecated)
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['...']['hook'][] = MyHook::class;

// ✅ NEW (PSR-14 events)
// Configuration/Services.yaml
services:
  Vendor\MyExt\EventListener\MyListener:
    tags:
      - name: event.listener
        identifier: 'myext/my-listener'

// Or use PHP attribute
#[AsEventListener(identifier: 'myext/my-listener')]
final class MyListener
{
    public function __invoke(SomeEvent $event): void
    {
        // Handle event
    }
}
```

### Static TCA (No Runtime Modifications)

```php
// ❌ OLD (runtime TCA mutation — enforcement switched to static TCA in TYPO3 v12; still seen in very old extensions)
// ext_tables.php
$GLOBALS['TCA']['tt_content']['columns']['myfield'] = [...];

// ✅ NEW (static TCA files only)
// Configuration/TCA/Overrides/tt_content.php
$GLOBALS['TCA']['tt_content']['columns']['myfield'] = [...];
```

### Backend Module Registration

```php
// ❌ OLD (ext_tables.php registration — migrate to Modules.php when modernizing)
ExtensionUtility::registerModule(...);

// ✅ NEW (Configuration/Backend/Modules.php)
return [
    'web_mymodule' => [
        'parent' => 'content',
        'access' => 'user,group',
        'iconIdentifier' => 'myext-module',
        'labels' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExt',
        'controllerActions' => [
            MyController::class => ['index', 'list'],
        ],
    ],
];
```

## API Changes Reference

### Typical cleanup when modernizing toward v14

| Removed/Changed | Replacement |
|-----------------|-------------|
| `StandaloneView` (legacy) | `ViewFactoryInterface` |
| `ObjectManager` / `GeneralUtility::makeInstance` for services | Constructor injection |
| `TSFE->fe_user->user` | Request attribute |
| Various hooks | PSR-14 events |
| Runtime TCA mutation in `ext_tables.php` | Static TCA under `Configuration/TCA/` (required since **v12**; still common in extensions that predate that layout) |
| Legacy `ExtensionUtility::registerModule()` in `ext_tables.php` | `Configuration/Backend/Modules.php` (same — not new in v14, but a frequent upgrade gap) |

> **Historical note:** `$GLOBALS['TYPO3_DB']` was removed long before v14 (use `Connection`/QueryBuilder). If you still see references while upgrading very old code, treat them as a separate legacy cleanup, not a v14-only item.

## Troubleshooting

### Rector Fails

```bash
# Clear Rector cache
rm -rf .rector_cache/

# Run with verbose output
vendor/bin/rector process --dry-run -vvv

# Skip problematic rules
# Add to rector.php:
->withSkip([
    \Ssch\TYPO3Rector\SomeRule::class,
])
```

### PHPStan Errors

```bash
# Generate baseline for existing issues
vendor/bin/phpstan analyse --generate-baseline

# Add to phpstan.neon:
includes:
    - phpstan-baseline.neon
```

### Extension Not Found

```bash
# Regenerate autoload
ddev composer dump-autoload

# Clear all caches
ddev typo3 cache:flush
rm -rf var/cache/*

# Re-setup extension
ddev typo3 extension:setup
```

### Database Issues

```bash
# After installing/updating an extension (registers tables, TCA, etc.)
ddev typo3 extension:setup

# Check for schema differences (CLI binary name may be `typo3`, `vendor/bin/typo3`, or typo3-console’s `typo3` — use your project’s documented wrapper)
ddev typo3 database:updateschema --verbose

# Apply safe schema changes
ddev typo3 database:updateschema "*.add,*.change"
```

## Success Criteria

Before considering upgrade complete:

- [ ] `rector --dry-run` shows no changes
- [ ] `fractor --dry-run` shows no changes
- [ ] `phpstan analyse` passes
- [ ] `php-cs-fixer --dry-run` passes
- [ ] All unit tests pass
- [ ] All functional tests pass
- [ ] Manual testing on TYPO3 v14 complete
- [ ] No deprecation warnings in logs
- [ ] Extension works in TYPO3 v14

## Resources

- **TYPO3 v14 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html
- **TYPO3 Rector**: https://github.com/sabbelasichon/typo3-rector
- **Fractor**: https://github.com/andreaswolf/fractor (package: `a9f/typo3-fractor`)

## v14-Only Upgrade Targets

> The following items are **common v14 migration topics**. Always confirm against the [TYPO3 v14 changelog](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html) for your exact minor, because details evolve between releases.

### Notable v14 breaking changes

| Change | Migration |
|--------|-----------|
| `$GLOBALS['TSFE']` / `TypoScriptFrontendController` removed | Use request attributes (`frontend.page.information`, `language`) |
| Extbase annotations removed | Use `#[Validate]`, `#[IgnoreValidation]` PHP attributes |
| `MailMessage->send()` removed | Inject `TYPO3\CMS\Core\Mail\MailerInterface` (TYPO3 Core mail transport interface) and send `FluidEmail` / `Email` instances so TYPO3 transport config applies |
| `FlexFormService` merged into `FlexFormTools` | Use `FlexFormTools` (BC alias exists until v15) |
| DataHandler `userid`/`admin`/`storeLogMessages` removed | Use `$GLOBALS['BE_USER']` / context APIs as documented in the changelog entry |
| Frontend asset concat/compress removed | Delegate to web server or build tools |
| Plugin subtypes removed | Register separate plugins via `configurePlugin()` |
| TCA `ctrl.searchFields` removed | Use per-column `'searchable' => true` |
| Backend module menu identifiers | Parent ids were reorganized in v14 (for example `content`, `media`, **`admin`**). Compare with Core `Configuration/Backend/Modules.php` — do not assume a 1:1 string rename from older examples. |
| Fluid 5.0 strict types | Fix ViewHelper argument types; remove underscore-prefixed variables |

### Changelog-first for upcoming minors

For deprecations and removals in **v14.1, v14.2, …**, read the corresponding `Breaking-*` / `Deprecation-*` entries in the official changelog rather than relying on static tables in this skill.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-extension-upgrade-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
