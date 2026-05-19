# 3. PHP: Accessibility Middleware & Helpers

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 3. PHP: Accessibility Middleware & Helpers

### 3.1 Language Attribute Middleware (PSR-15)

Ensures `<html lang="...">` is always correct based on site language config.

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;
use TYPO3\CMS\Core\Site\Entity\SiteLanguage;

final class AccessibilityLangMiddleware implements MiddlewareInterface
{
    public function process(ServerRequestInterface $request, RequestHandlerInterface $handler): ResponseInterface
    {
        $response = $handler->handle($request);

        $siteLanguage = $request->getAttribute('language');
        if (!$siteLanguage instanceof SiteLanguage) {
            return $response;
        }

        $contentType = $response->getHeaderLine('Content-Type');
        if (!str_contains($contentType, 'text/html')) {
            return $response;
        }

        $locale = $siteLanguage->getLocale();
        $langCode = $locale->getLanguageCode();
        $body = (string)$response->getBody();

        $body = preg_replace(
            '/<html([^>]*)lang="[^"]*"/',
            '<html$1lang="' . htmlspecialchars($langCode) . '"',
            $body,
            1
        );

        $newBody = new \TYPO3\CMS\Core\Http\Stream('php://temp', 'rw');
        $newBody->write($body);

        return $response->withBody($newBody);
    }
}
```

Register via `Configuration/RequestMiddlewares.php` (TYPO3 v14; same registration file exists on supported older majors if you maintain multi-version code):

```php
<?php
// Configuration/RequestMiddlewares.php
return [
    'frontend' => [
        'vendor/site-package/accessibility-lang' => [
            'target' => \Vendor\SitePackage\Middleware\AccessibilityLangMiddleware::class,
            'after' => ['typo3/cms-frontend/content-length-headers'],
        ],
    ],
];
```

### 3.2 Image Alt Text Validation (DataHandler hook)

Warn editors when images lack alt text. Use a **`processDatamapClass`** hook on `sys_file_metadata` saves — not workspace publish events (`AfterRecordPublishedEvent` lives under **Workspaces** and fires on publish workflows).

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\Hooks;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Messaging\FlashMessage;
use TYPO3\CMS\Core\Messaging\FlashMessageService;
use TYPO3\CMS\Core\Type\ContextualFeedbackSeverity;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ImageAltTextValidationHook
{
    public function processDatamap_afterDatabaseOperations(
        string $status,
        string $table,
        string|int $id,
        array $fieldArray,
        DataHandler $dataHandler,
    ): void {
        if ($table !== 'sys_file_metadata') {
            return;
        }

        if (empty($fieldArray['alternative'] ?? '')) {
            $message = GeneralUtility::makeInstance(
                FlashMessage::class,
                'Image is missing alt text. Please add descriptive alt text for accessibility (WCAG 1.1.1).',
                'Accessibility Warning',
                ContextualFeedbackSeverity::WARNING,
                true,
            );

            GeneralUtility::makeInstance(FlashMessageService::class)
                ->getMessageQueueByIdentifier()
                ->addMessage($message);
        }
    }
}
```

Register in `ext_localconf.php`:

```php
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
    = \Vendor\SitePackage\Hooks\ImageAltTextValidationHook::class;
```

### 3.3 Accessible Fluid ViewHelper: SrOnly

Renders screen-reader-only text:

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\ViewHelpers;

use TYPO3Fluid\Fluid\Core\ViewHelper\AbstractTagBasedViewHelper;

final class SrOnlyViewHelper extends AbstractTagBasedViewHelper
{
    protected $tagName = 'span';

    // Fluid 5.x / TYPO3 v14: `registerUniversalTagAttributes()` and `registerTagAttribute()` were
    // removed from AbstractTagBasedViewHelper. Register explicit arguments via `registerArgument()`
    // in `initializeArguments()`; unregistered attributes pass through via handleAdditionalArguments().

    public function render(): string
    {
        $this->tag->addAttribute('class', 'sr-only');
        $this->tag->setContent($this->renderChildren());
        return $this->tag->render();
    }
}
```

```css
/* CSS for sr-only */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

Usage in Fluid:

```html
{namespace sp = Vendor\SitePackage\ViewHelpers}
<button aria-label="{f:translate(key: 'button.close')}">
    <svg aria-hidden="true"><!-- icon --></svg>
    <sp:srOnly><f:translate key="button.close" /></sp:srOnly>
</button>
```
