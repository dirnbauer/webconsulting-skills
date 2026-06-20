# TYPO3 v14 Web Components Examples And How-Tos

Use these examples as patterns, not as a package to copy blindly. Replace `Vendor`, `my_extension`, route names, and labels with the project conventions.

## Table Of Contents

- Inventory existing components
- Create a no-build Lit component
- Register the import map
- Load the component from PHP or Fluid
- Add backend data with an AJAX route
- Use Web Components in backend modules
- Modernize Form Editor custom elements
- Reuse existing components
- Frontend Web Components decision

## Inventory Existing Components

Search project and Core sources before writing a custom component:

```bash
rg -n "@customElement\\(|customElements\\.define\\(" Build typo3/sysext vendor/typo3 packages Resources 2>/dev/null
rg -n "JavaScriptModules.php|loadJavaScriptModule|f:asset.module|@typo3/" Configuration Resources Classes
```

In a TYPO3 source checkout, the interesting Core source path is usually `Build/Sources/TypeScript`. In a Composer project, shipped JavaScript may be compiled under `vendor/typo3/cms-*/Resources/Public/JavaScript`, so decorators may no longer be visible.

## Create A No-Build Lit Component

Use this pattern when the extension does not have a TypeScript build. Avoid decorators and class fields so the file can be loaded directly as an ES module.

`EXT:my_extension/Resources/Public/JavaScript/backend/status-card.js`

```js
import {LitElement, html, nothing} from 'lit';

export class VendorStatusCard extends LitElement {
  static properties = {
    headline: {type: String},
    count: {type: Number},
    endpoint: {type: String},
    _busy: {state: true},
    _error: {state: true},
  };

  constructor() {
    super();
    this.headline = '';
    this.count = 0;
    this.endpoint = '';
    this._busy = false;
    this._error = '';
  }

  createRenderRoot() {
    return this;
  }

  render() {
    return html`
      <section class="card">
        <div class="card-body d-flex align-items-center justify-content-between gap-3">
          <div>
            <h2 class="h5 mb-1">${this.headline}</h2>
            <p class="mb-0 text-muted">${this.count} records</p>
          </div>
          <button
            class="btn btn-default"
            type="button"
            ?disabled=${this._busy || !this.endpoint}
            @click=${this.refresh}
          >
            ${this._busy ? 'Loading...' : 'Refresh'}
          </button>
        </div>
        ${this._error ? html`<p class="card-footer text-danger mb-0">${this._error}</p>` : nothing}
      </section>
    `;
  }

  async refresh() {
    if (!this.endpoint) {
      return;
    }
    this._busy = true;
    this._error = '';

    try {
      const response = await fetch(this.endpoint, {credentials: 'same-origin'});
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const payload = await response.json();
      this.count = Number(payload.count || 0);
    } catch (error) {
      this._error = error instanceof Error ? error.message : 'Request failed';
    } finally {
      this._busy = false;
    }
  }
}

if (!customElements.get('vendor-status-card')) {
  customElements.define('vendor-status-card', VendorStatusCard);
}
```

Why `createRenderRoot() { return this; }`: TYPO3 backend CSS and Bootstrap classes are already present in the backend document. Rendering into light DOM lets those styles apply. Keep Shadow DOM when scoped component styles and slots matter more than reusing backend CSS.

## Register The Import Map

`EXT:my_extension/Configuration/JavaScriptModules.php`

```php
<?php

declare(strict_types=1);

return [
    'dependencies' => ['core', 'backend'],
    'imports' => [
        '@vendor/my-extension/' => 'EXT:my_extension/Resources/Public/JavaScript/',
    ],
];
```

Rules:

- Use a trailing slash for recursive import-map prefixes.
- Use import-map identifiers from inside modules, for example `@vendor/my-extension/backend/status-card.js`.
- Avoid relative imports such as `./status-card.js` in TYPO3-loaded backend modules. They are brittle with TYPO3's module resolution and cache behavior.
- Add the `backend.form` tag when the module can be needed later inside dynamically loaded backend form elements.

## Load The Component From PHP Or Fluid

In a backend controller:

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Controller;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Backend\Attribute\AsController;
use TYPO3\CMS\Backend\Routing\UriBuilder;
use TYPO3\CMS\Backend\Template\ModuleTemplateFactory;
use TYPO3\CMS\Core\Page\PageRenderer;

#[AsController]
final readonly class ReportModuleController
{
    public function __construct(
        private ModuleTemplateFactory $moduleTemplateFactory,
        private PageRenderer $pageRenderer,
        private UriBuilder $uriBuilder,
    ) {}

    public function handleRequest(ServerRequestInterface $request): ResponseInterface
    {
        $this->pageRenderer->loadJavaScriptModule('@vendor/my-extension/backend/status-card.js');

        $view = $this->moduleTemplateFactory->create($request);
        $view->assignMultiple([
            'statusEndpoint' => (string)$this->uriBuilder->buildUriFromRoute('vendor_myextension_status'),
            'recordCount' => 0,
        ]);

        return $view->renderResponse('Backend/Report');
    }
}
```

In Fluid:

```html
<f:asset.module identifier="@vendor/my-extension/backend/status-card.js" />

<vendor-status-card
    headline="{f:translate(key: 'module.status.headline')}"
    count="{recordCount}"
    endpoint="{statusEndpoint}">
</vendor-status-card>
```

Prefer `f:asset.module` in reusable partials so the module is loaded only when the markup appears. Prefer `PageRenderer->loadJavaScriptModule()` when every action in a backend controller needs the module.

## Add Backend Data With An AJAX Route

For authenticated backend data, use a backend AJAX route. Do not put privileged data into HTML attributes.

`EXT:my_extension/Configuration/Backend/AjaxRoutes.php`

```php
<?php

declare(strict_types=1);

use Vendor\MyExtension\Controller\StatusController;

return [
    'vendor_myextension_status' => [
        'path' => '/vendor/my-extension/status',
        'target' => StatusController::class . '::statusAction',
        'inheritAccessFromModule' => 'web_MyExtensionReport',
    ],
];
```

`EXT:my_extension/Classes/Controller/StatusController.php`

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Controller;

use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;

final readonly class StatusController
{
    public function __construct(
        private ResponseFactoryInterface $responseFactory,
    ) {}

    public function statusAction(ServerRequestInterface $request): ResponseInterface
    {
        $response = $this->responseFactory->createResponse()
            ->withHeader('Content-Type', 'application/json; charset=utf-8');
        $response->getBody()->write(json_encode(['count' => 42], JSON_THROW_ON_ERROR));

        return $response;
    }
}
```

In a Lit component, prefer the TYPO3 AJAX helper for backend routes:

```js
import AjaxRequest from '@typo3/core/ajax/ajax-request.js';

async function loadStatus(endpoint) {
  const response = await new AjaxRequest(endpoint).get();
  return await response.resolve();
}
```

Flush caches after changing backend route definitions.

## Use Web Components In Backend Modules

Backend modules are registered in `Configuration/Backend/Modules.php`. Most custom modules should still use the standard TYPO3 module shell, `ModuleTemplateFactory`, DocHeader buttons, and Fluid. Put Web Components inside the module content where interaction is needed.

Use module configuration component options only deliberately:

```php
<?php

declare(strict_types=1);

return [
    'web_MyExtensionReport' => [
        'parent' => 'web',
        'path' => '/module/my-extension/report',
        'access' => 'user',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'iconIdentifier' => 'my-extension-module',
        'navigationComponent' => '@typo3/backend/tree/page-tree-element',
        'routes' => [
            '_default' => [
                'target' => \Vendor\MyExtension\Controller\ReportModuleController::class . '::handleRequest',
            ],
        ],
    ],
];
```

TYPO3 v14 removed the old `@typo3/backend/page-tree/page-tree-element` navigation component name. Use `@typo3/backend/tree/page-tree-element`.

## Modernize Form Editor Custom Elements

For TYPO3 v14.2+, custom Form Framework elements usually do not need custom stage JavaScript. If no `formEditorPartials` entry is configured, the Form Editor uses the built-in `<typo3-form-form-element-stage-item>` Web Component.

Use this default when the custom element can be represented by label, icon, required state, validators, select options, allowed MIME types, toolbar, and hidden state.

Only keep a custom Form Editor JavaScript module when the stage needs specialized interaction or visualization:

```yaml
prototypes:
  standard:
    formEditor:
      dynamicJavaScriptModules:
        additionalViewModelModules:
          10: '@vendor/my-extension/backend/form-editor/view-model.js'
```

The module should export `bootstrap(formEditorApp)` and communicate through the Form Editor publish/subscribe bus. Avoid direct cross-module calls.

## Reuse Existing Components

Good reusable examples:

- TYPO3 backend UI primitives from Core, after checking current source: modal, alert, spinner, progress bar, breadcrumb, pagination, combobox, tree, wizard, copy-to-clipboard, QR code helpers, and code editor elements.
- Form Framework v14.2 Web Components: generic stage items for custom form elements and the modern Form Editor tree.
- Extension-owned components such as Yoast SEO for TYPO3 preview and analysis elements when that extension is installed and its public component contract fits the task.

Do not assume every Core custom element is public API. Confirm the source file, imports, events, properties, and changelog before reusing a component directly.

## Frontend Web Components Decision

If the user asks for frontend usage:

```text
Backend Web Components in frontend: no.
Own Web Components in frontend: possible, but use only when the component will be reused or needs a real component lifecycle.
Lit in frontend: possible, but bundle through the frontend build pipeline and treat it as a frontend dependency.
```

Use `typo3-vite` for frontend bundling. Do not reference backend modules like `@typo3/backend/*`, backend globals, or backend CSS in frontend code.
