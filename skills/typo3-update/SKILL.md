---
name: typo3-update
description: >-
  TYPO3 v14 development guide: version constraints, core APIs, extension patterns, and
  upgrade workflows. Use when working with update, upgrade, v14, migration, lts,
  TYPO3 core.
compatibility: TYPO3 14.x
metadata:
  version: "2.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 v14 development

> **Strategy:** This collection targets **TYPO3 v14.x only**. Patterns here assume a v14 codebase.
> For migrating from older majors, use `typo3-rector`, `typo3-extension-upgrade`, Fractor, and the official upgrade guide first.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## 1. Version Strategy

### Target: TYPO3 v14.x only

| Version | Role for this collection |
|---------|--------------------------|
| **v14.x** | **Supported target** — examples and constraints assume TYPO3 v14 |
| Older majors | **Not targeted** — complete a core upgrade, then use these patterns |

**Best Practice:** Declare TYPO3 **v14-only** constraints in `composer.json` and `ext_emconf.php` for new work.

### Version Constraints

```php
<?php
// ext_emconf.php — TYPO3 v14
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '2.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '14.0.0-14.99.99',
            'php' => '8.2.0-8.5.99',
        ],
        'conflicts' => [],
        'suggests' => [],
    ],
];
```

```json
// composer.json — TYPO3 v14
{
    "name": "vendor/my-extension",
    "type": "typo3-cms-extension",
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^14.0"
    },
    "extra": {
        "typo3/cms": {
            "extension-key": "my_extension"
        }
    }
}
```

> **Content Blocks:** `friendsoftypo3/content-blocks` may require **`typo3/cms-core` ^14.1** or higher — match the [Packagist constraint](https://packagist.org/packages/friendsoftypo3/content-blocks) before pinning `^14.0` only.

## 2. PHP Requirements

### Minimum PHP Version: 8.2

TYPO3 v14 requires PHP 8.2+. Use modern PHP features:

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Service;

// ✅ Constructor property promotion (PHP 8.0+)
final class MyService
{
    public function __construct(
        private readonly SomeDependency $dependency,
        private readonly AnotherService $anotherService,
    ) {}
}

// ✅ Named arguments (PHP 8.0+)
$result = $this->doSomething(
    name: 'value',
    options: ['key' => 'value'],
);

// ✅ Match expressions (PHP 8.0+)
$type = match ($input) {
    'a' => 'Type A',
    'b' => 'Type B',
    default => 'Unknown',
};

// ✅ Enums (PHP 8.1+)
enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';
}
```

## 3. Controller Patterns (TYPO3 v14)

### Extbase Action Controller

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;
use Vendor\Extension\Domain\Repository\ItemRepository;

final class ItemController extends ActionController
{
    public function __construct(
        private readonly ItemRepository $itemRepository,
    ) {}

    // ✅ Must return ResponseInterface (required in TYPO3 v14)
    public function listAction(): ResponseInterface
    {
        $items = $this->itemRepository->findAll();
        $this->view->assign('items', $items);
        return $this->htmlResponse();
    }

    public function showAction(int $item): ResponseInterface
    {
        $item = $this->itemRepository->findByUid($item);
        $this->view->assign('item', $item);
        return $this->htmlResponse();
    }

    // ✅ JSON response
    public function apiAction(): ResponseInterface
    {
        $data = ['success' => true, 'items' => []];
        return $this->jsonResponse(json_encode($data));
    }

    // ✅ Redirect
    public function createAction(): ResponseInterface
    {
        // Process creation...
        $this->addFlashMessage('Item created');
        return $this->redirect('list');
    }
}
```

### Backend Module Controller

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Backend\Attribute\AsController;
use TYPO3\CMS\Backend\Template\ModuleTemplateFactory;

#[AsController]
final class BackendModuleController
{
    public function __construct(
        private readonly ModuleTemplateFactory $moduleTemplateFactory,
    ) {}

    public function indexAction(ServerRequestInterface $request): ResponseInterface
    {
        $moduleTemplate = $this->moduleTemplateFactory->create($request);
        $moduleTemplate->assign('items', []);
        
        return $moduleTemplate->renderResponse('Backend/Index');
    }
}
```

## 4. View & Templating (TYPO3 v14)

### ViewFactory (Preferred Pattern)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Service;

use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Core\View\ViewFactoryData;
use TYPO3\CMS\Core\View\ViewFactoryInterface;

final class RenderingService
{
    public function __construct(
        private readonly ViewFactoryInterface $viewFactory,
    ) {}

    public function renderEmail(ServerRequestInterface $request, array $data): string
    {
        $viewFactoryData = new ViewFactoryData(
            templateRootPaths: ['EXT:my_extension/Resources/Private/Templates/Email'],
            partialRootPaths: ['EXT:my_extension/Resources/Private/Partials'],
            layoutRootPaths: ['EXT:my_extension/Resources/Private/Layouts'],
            request: $request,
        );
        
        $view = $this->viewFactory->create($viewFactoryData);
        $view->assignMultiple($data);
        
        return $view->render('Notification');
    }
}
```

### Fluid Template Best Practices

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:core="http://typo3.org/ns/TYPO3/CMS/Core/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="Main">
    <div class="content">
        <!-- ✅ Auto-escaped output -->
        <h1>{item.title}</h1>
        
        <!-- ✅ Explicit HTML (use with caution) -->
        <f:format.html>{item.bodytext}</f:format.html>
        
        <!-- ✅ Conditional rendering -->
        <f:if condition="{items}">
            <f:then>
                <f:for each="{items}" as="item">
                    <f:render partial="Item" arguments="{item: item}" />
                </f:for>
            </f:then>
            <f:else>
                <p>No items found.</p>
            </f:else>
        </f:if>
        
        <!-- ✅ Link building -->
        <f:link.action action="show" arguments="{item: item.uid}">
            View Details
        </f:link.action>
    </div>
</f:section>

</html>
```

## 5. Event System (TYPO3 v14)

### PSR-14 Event Listeners

PSR-14 events are the standard in TYPO3 v14. Always prefer events over hooks.

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Frontend\Event\ModifyCacheLifetimeForPageEvent;

#[AsEventListener(identifier: 'vendor-extension/modify-cache-lifetime')]
final class ModifyCacheLifetimeListener
{
    public function __invoke(ModifyCacheLifetimeForPageEvent $event): void
    {
        // Reduce cache lifetime for certain pages
        if ($event->getPageId() === 123) {
            $event->setCacheLifetime(300); // 5 minutes
        }
    }
}
```

### Common Events (TYPO3 v14)

| Event | Purpose |
|-------|---------|
| `ModifyPageLinkConfigurationEvent` | Modify link building |
| `ModifyCacheLifetimeForPageEvent` | Adjust page cache |
| `BeforeStdWrapFunctionsInitializedEvent` | Modify stdWrap |
| *(DataHandler)* | Core ships **no** generic `BeforeRecordOperationEvent` / `AfterRecordOperationEvent`; use **`SC_OPTIONS`** DataHandler hooks or documented `TYPO3\CMS\Core\DataHandling\Event\*` only ([list](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/DataHandling/Index.html)) |

### Services.yaml Registration

```yaml
# Configuration/Services.yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\Extension\:
    resource: '../Classes/*'
    exclude:
      - '../Classes/Domain/Model/*'

  # Event listener (alternative to #[AsEventListener] attribute)
  Vendor\Extension\EventListener\MyListener:
    tags:
      - name: event.listener
        identifier: 'vendor-extension/my-listener'
```

## 6. Backend Module Registration (TYPO3 v14)

### Configuration/Backend/Modules.php

```php
<?php
// Configuration/Backend/Modules.php
return [
    'web_myextension' => [
        'parent' => 'content',
        'position' => ['after' => 'records'],
        'access' => 'user,group',
        'iconIdentifier' => 'myextension-module',
        'path' => '/module/web/myextension',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExtension',
        'controllerActions' => [
            \Vendor\MyExtension\Controller\BackendController::class => [
                'index',
                'list',
                'show',
            ],
        ],
    ],
];
```

### Icon Registration

```php
<?php
// Configuration/Icons.php
return [
    'myextension-module' => [
        'provider' => \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/module.svg',
    ],
];
```

## 7. TCA Configuration (TYPO3 v14)

### Static TCA Only

In v14, runtime TCA modifications are forbidden. Always use static files:

```php
<?php
// Configuration/TCA/tx_myext_domain_model_item.php
return [
    'ctrl' => [
        'title' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item',
        'label' => 'title',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'searchFields' => 'title,description',
        'iconIdentifier' => 'myextension-item',
    ],
    'palettes' => [
        'visibility' => [
            'showitem' => 'hidden',
        ],
        'access' => [
            'showitem' => 'starttime, endtime',
        ],
    ],
    'types' => [
        '1' => [
            'showitem' => '
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
                    title, description,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
                    --palette--;;visibility,
                    --palette--;;access,
            ',
        ],
    ],
    'columns' => [
        'title' => [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item.title',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'description' => [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item.description',
            'config' => [
                'type' => 'text',
                'cols' => 40,
                'rows' => 5,
                'enableRichtext' => true,
            ],
        ],
    ],
];
```

### Auto-Created Columns from ctrl

Since **TYPO3 v13.3+**, column definitions for fields referenced in `ctrl` are **auto-created** by the Core. You no longer need explicit `'columns'` entries for:

- `enablecolumns` fields: `hidden`/`disabled`, `starttime`, `endtime`, `fe_group`
- Language fields: `sys_language_uid`, `l10n_parent`, `l10n_diffsource`
- `editlock`, `description` (if set as `descriptionColumn`)

**Convention fields don't need `ext_tables.sql`** -- all fields referenced by `ctrl` properties (`deleted`, `hidden`, `starttime`, `endtime`, `fe_group`, `sorting`, `tstamp`, `crdate`, `sys_language_uid`, `l10n_parent`, `l10n_diffsource`) are added to the database automatically. Defining them in `ext_tables.sql` may cause problems.

**Fields that never need `columns` definitions:**
- `deleted` -- handled by DataHandler, not shown in forms
- `tstamp`, `crdate`, `t3_origuid` -- managed by DataHandler, never displayed
- `sorting` -- managed by DataHandler, should NOT be in `columns`

**Still required:**
- The `ctrl` properties themselves (`tstamp`, `crdate`, `delete`, `enablecolumns`, etc.)
- References in `showitem` / palettes (auto-created columns must still be added to types manually)
- Use dedicated palettes: `visibility` for `hidden`, `access` for `starttime, endtime`
- Your own custom column definitions

**Override auto-created columns** in `Configuration/TCA/Overrides/` if needed:

```php
<?php
// Configuration/TCA/Overrides/pages.php
// New pages are disabled by default
$GLOBALS['TCA']['pages']['columns']['disabled']['config']['default'] = 1;
```

> **Important:** Auto-creation only works for `ctrl` properties in base `Configuration/TCA/` files, NOT in `Configuration/TCA/Overrides/`.
>
> See: [Common fields](https://docs.typo3.org/permalink/t3tca:fields-for-datahandler) | [Auto-created columns](https://docs.typo3.org/m/typo3/reference-tca/main/en-us/Ctrl/AutoCreatedColumns.html)

### TCA Overrides

```php
<?php
// Configuration/TCA/Overrides/tt_content.php
defined('TYPO3') or die();

\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTcaSelectItem(
    'tt_content',
    'CType',
    [
        'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:ctype.title',
        'value' => 'myextension_element',
        'icon' => 'content-text',
        'group' => 'default',
    ]
);

$GLOBALS['TCA']['tt_content']['types']['myextension_element'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            bodytext,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
    ',
];
```

## 8. Database Operations (TYPO3 v14)

### QueryBuilder

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Repository;

use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Database\Query\QueryBuilder;

final class CustomRepository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    public function findByStatus(string $status): array
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return $queryBuilder
            ->select('*')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'status',
                    $queryBuilder->createNamedParameter($status)
                )
            )
            ->orderBy('title', 'ASC')
            ->executeQuery()
            ->fetchAllAssociative();
    }

    public function countByPid(int $pid): int
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return (int)$queryBuilder
            ->count('uid')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'pid',
                    $queryBuilder->createNamedParameter($pid, Connection::PARAM_INT)
                )
            )
            ->executeQuery()
            ->fetchOne();
    }
}
```

### Extbase Repository

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Domain\Repository;

use TYPO3\CMS\Extbase\Persistence\QueryInterface;
use TYPO3\CMS\Extbase\Persistence\Repository;

final class ItemRepository extends Repository
{
    protected $defaultOrderings = [
        'sorting' => QueryInterface::ORDER_ASCENDING,
    ];

    public function findPublished(): array
    {
        $query = $this->createQuery();
        $query->matching(
            $query->logicalAnd(
                $query->equals('hidden', false),
                $query->lessThanOrEqual('starttime', time()),
                $query->logicalOr(
                    $query->equals('endtime', 0),
                    $query->greaterThan('endtime', time())
                )
            )
        );
        
        return $query->execute()->toArray();
    }
}
```

## 9. CLI Commands (TYPO3 v14)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\Core\Bootstrap;

#[AsCommand(
    name: 'myext:process',
    description: 'Process items in the extension',
)]
final class ProcessCommand extends Command
{
    protected function configure(): void
    {
        $this
            ->addArgument('type', InputArgument::REQUIRED, 'The type to process')
            ->addOption('force', 'f', InputOption::VALUE_NONE, 'Force processing');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        
        // Initialize backend for DataHandler operations
        Bootstrap::initializeBackendAuthentication();
        
        $type = $input->getArgument('type');
        $force = $input->getOption('force');
        
        $io->title('Processing: ' . $type);
        
        // Your logic here...
        
        $io->success('Processing completed successfully');
        
        return Command::SUCCESS;
    }
}
```

### Command Registration

With **`autoconfigure: true`** in `Services.yaml` defaults, **`#[AsCommand]` is enough** — you do **not** need the `console.command` tag unless autoconfigure is disabled for that service.

```yaml
# Optional — only when not using #[AsCommand] + autoconfigure
services:
  Vendor\Extension\Command\ProcessCommand:
    tags:
      - name: console.command
```

## 10. Testing

### PHPUnit Setup

```xml
<!-- phpunit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/UnitTestsBootstrap.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>Tests/Unit</directory>
        </testsuite>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

### CI matrix (TYPO3 v14)

```yaml
# .github/workflows/ci.yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        typo3: ['^14.0']
        php: ['8.2', '8.3', '8.4']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: intl, pdo_mysql
      
      - name: Install dependencies
        run: |
          composer require typo3/cms-core:${{ matrix.typo3 }} --no-update
          composer install --prefer-dist --no-progress
      
      - name: Run tests
        run: vendor/bin/phpunit
```

## 11. Upgrade Process

### From older majors to v14

```bash
# 1. Create backup
ddev snapshot --name=before-upgrade

# 2. Update composer constraints
ddev composer require "typo3/cms-core:^14.0" --no-update
ddev composer update "typo3/*" --with-all-dependencies

# 3. Run upgrade wizards
ddev typo3 upgrade:list
ddev typo3 upgrade:run

# 4. Clear caches
ddev typo3 cache:flush

# 5. Register extensions and align database schema
ddev typo3 extension:setup
# Schema compare/apply (CLI entry point depends on your project: `typo3`, `vendor/bin/typo3`, typo3-console, etc.)
# `database:updateschema` is from **helhum/typo3-console**, not plain Core — omit if you only have `vendor/bin/typo3`.
ddev typo3 database:updateschema

# 6. Test thoroughly
```

## 12. Resources

- **v14 Documentation**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/
- **v14 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html
- **TYPO3 Rector**: https://github.com/sabbelasichon/typo3-rector

## 13. v14-Only Changes (Manual — Not Handled by Rector)

> The following changes apply **exclusively to TYPO3 v14** and require **manual migration**.
> They are NOT fully covered by `ssch/typo3-rector` (check your installed version; the TYPO3 14 rule set counts **tens** of rules and changes between releases).
> For automated migrations, run `Typo3LevelSetList::UP_TO_TYPO3_14` first, then address these manually.

### Fluid 5.0 Template Changes **[v14 only]**

Rector handles PHP-side ViewHelper declarations (`UseStrictTypesInFluidViewHelpersRector`), but Fluid **template** changes require manual review:

- ViewHelper arguments in `.html` templates must match strict types (e.g., `tabindex` must be int, not string).
- Fluid variable names with **underscore prefix** (`_myVar`) are disallowed — rename in all templates.
- CDATA sections in Fluid templates are **no longer removed** automatically.
- Use `{variable as type}` casting for ambiguous ViewHelper arguments.

### TypoScriptFrontendController Removed **[v14 only]**

Not covered by Rector — context-dependent migration requiring manual analysis:

- `$GLOBALS['TSFE']` and `TypoScriptFrontendController` are fully removed.
- Each usage needs different request attribute replacements:
  ```php
  // ❌ Removed in v14
  $tsfe = $GLOBALS['TSFE'];
  
  // ✅ TYPO3 v14 pattern
  $pageInformation = $request->getAttribute('frontend.page.information');
  $language = $request->getAttribute('language');
  $typoscript = $request->getAttribute('frontend.typoscript');
  ```

### Backend Module Renaming **[v14 only]**

Not a PHP migration — requires manual update to `Configuration/Backend/Modules.php`:

| Old Parent | New Parent |
|------------|------------|
| `web` | `content` |
| `file` | `media` |
| `tools` | `admin` **or** `system` (Core split tools into multiple parents — map each module to its new parent in `Configuration/Backend/Modules.php`) |

### Runtime TCA Modifications Forbidden **[v14 only]**

`$GLOBALS['TCA']` is **read-only after boot** in TYPO3 v14 — stricter than older majors. Static TCA under `Configuration/TCA/` has been the supported approach **since v12**; extensions still mutating TCA from `ext_tables.php`, middleware, or event listeners must be refactored (architectural change, not a one-line replace).

### Plugin Subtypes Removed **[v14 only]**

- **`switchableControllerActions`:** removed in **TYPO3 v10** (#88496) — not a v14-only topic, but legacy FlexForm/plugins may still reference it until you split plugins.
- **`list_type` subtypes / plugin list types:** further tightened in **v14** (#105538) — each variant needs its own `configurePlugin()` / registration and TypoScript/FlexForm split.

### EXT:form Hooks → PSR-14 Events **[v14 only]**

Hook-to-event migration requires manual rewrite of hook implementations:
- All EXT:form hooks removed (incl. **`afterInitializeCurrentPage`**, Breaking #107566): `beforeRendering`, `afterSubmit`, `initializeFormElement`, `beforeFormSave`, `beforeFormDelete`, `beforeFormDuplicate`, `beforeFormCreate`, `afterBuildingFinished`, `beforeRemoveFromParentRenderable`, `afterInitializeCurrentPage`.
- Replace with corresponding PSR-14 events (e.g., `BeforeFormIsSavedEvent`, `BeforeRenderableIsRenderedEvent`).

### Frontend Asset Pipeline **[v14 only]**

Rector removes PHP configuration (`RemoveConcatenateAndCompressHandlerRector`), but the **infrastructure replacement** is manual:
- CSS/JS concatenation and compression removed from TYPO3 Core entirely.
- Must configure web server compression (nginx gzip, Apache mod_deflate) or use build tools (Vite, webpack).
- TypoScript `config.concatenateCss`, `config.compressCss`, `config.concatenateJs`, `config.compressJs` must be removed (handled by Fractor, not Rector).

### New TCA Features **[v14 only]**

New features to adopt (not migrations):
- **New TCA type `country`** (#99911) for country selection fields.
- **New `itemsProcessors`** option (#107889) for dynamic item generation.
- **Type-specific `title` (and `previewRenderer`) in TCA `types`** — [Feature #108027](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108027-Type-SpecificCtrlPropertiesInTCATypes.html) (not “arbitrary ctrl copies” per type — see changelog).
- **Type-specific TCA defaults** (#107281).

### New Fluid ViewHelpers **[v14 only]**

- `<f:page.meta>` — set page meta tags from Fluid templates.
- `<f:page.title>` — set page title from Fluid templates.
- `<f:page.headerData>` / `<f:page.footerData>` — inject raw HTML into head/footer ([Feature #107056](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.4/Feature-107056-FluidViewHelpersForHeaderAndFooterData.html)).

### Localization System **[v14 only]**

Rector handles parser class replacement (`ReplaceLocalizationParsersWithLoaders`) and label syntax (`MigrateLabelReferenceToDomainSyntaxRector`), but these features are new:
- **XLIFF 2.x** translation files supported alongside XLIFF 1.2.
- **Translation domain mapping** (#93334) for flexible XLIFF file resolution.

### New DataHandler Features **[v14 only]**

- **`discard` command** (#107519) — discard workspace changes programmatically.
- **ISO8601 date handling improved** — qualified and unqualified ISO8601 dates supported.

### v14.1 Features **[v14.1+ only]**

Verify each item in the [official v14.1 changelog](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html) for your minor (entries change over time). Examples that have appeared in v14.1 discussions include **default theme “Camino”**, **per-column content restrictions**, **Fluid Components** tuning, and **PHP 8.5** support — confirm before documenting them for a specific project.

### v14.2 Features **[v14.2+ only]**

- **Backend search by frontend URL** — find pages by their frontend URL in page tree and live search.
- **Workspace selector moved to sidebar** with color and description.
- **Extbase identity map language-aware** — identity map now considers language when resolving objects.
- **XLIFF `xml:space` attribute** — whitespace handling respects the attribute.
- **QR Code for frontend preview** — downloadable QR codes (PNG/SVG) for frontend URLs.

### New v14 Deprecations (removed in v15) — Not Yet Handled by Rector

**v14.0 (examples):**

- `ExtensionManagementUtility::addPiFlexFormValue()` — use direct FlexForm TCA.

**v14.2+ (verify changelog IDs):**

- `ExtensionManagementUtility::addFieldsToUserSettings` (#108843) — use TCA for user settings.
- `PageRenderer->addInlineLanguageDomain()` (#108963).
- `FormEngine "additionalHiddenFields"` key (#109102).

---

## Credits & Attribution

Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.
