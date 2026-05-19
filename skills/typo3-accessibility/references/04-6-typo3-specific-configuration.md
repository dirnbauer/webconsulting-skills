# 6. TYPO3-Specific Configuration

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 6. TYPO3-Specific Configuration

### 6.1 TCA: Require Alt Text on Images

Make the alt text field required in file metadata:

```php
<?php
// Configuration/TCA/Overrides/sys_file_metadata.php

$GLOBALS['TCA']['sys_file_metadata']['columns']['alternative']['config']['required'] = true;

// On v14 prefer `required` (above). Avoid legacy `eval` = required patterns.
```

### 6.2 TCA: Header Layout Options

Provide proper heading levels and a "hidden" option for content elements:

```php
<?php
// Configuration/TCA/Overrides/tt_content.php

$GLOBALS['TCA']['tt_content']['columns']['header_layout']['config']['items'] = [
    ['label' => 'H1', 'value' => '1'],
    ['label' => 'H2', 'value' => '2'],
    ['label' => 'H3', 'value' => '3'],
    ['label' => 'H4', 'value' => '4'],
    ['label' => 'H5', 'value' => '5'],
    ['label' => 'Hidden', 'value' => '100'],
];
$GLOBALS['TCA']['tt_content']['columns']['header_layout']['config']['default'] = '2';
```

**Legacy TCA `items` shape (pre–label/value arrays):** numeric keys `[0]` = label, `[1]` = value — **avoid on v14-only projects**; kept here only for reading older extensions:

```php
// Legacy style (do not use for new v14-only TCA)
$GLOBALS['TCA']['tt_content']['columns']['header_layout']['config']['items'] = [
    ['H1', '1'],
    ['H2', '2'],
    ['H3', '3'],
    ['H4', '4'],
    ['H5', '5'],
    ['Hidden', '100'],
];
```

### 6.3 Form Framework: Accessible Forms (EXT:form)

```yaml
# EXT:site_package/Configuration/Form/Overrides/AccessibleForm.yaml
TYPO3:
  CMS:
    Form:
      prototypes:
        standard:
          formElementsDefinition:
            Text:
              properties:
                fluidAdditionalAttributes:
                  autocomplete: 'on'
            Email:
              properties:
                fluidAdditionalAttributes:
                  autocomplete: 'email'
                  inputmode: 'email'
            Telephone:
              properties:
                fluidAdditionalAttributes:
                  autocomplete: 'tel'
                  inputmode: 'tel'
```

### 6.4 Content Security Policy: Allow Inline Focus Styles

If CSP is enabled, ensure focus styles via external CSS (not inline):

```php
<?php
// No inline styles needed — use the external accessibility.css
// If you must add inline styles, extend CSP via PSR-14:

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Event\PolicyMutatedEvent;

#[AsEventListener(identifier: 'vendor/site-package/csp-accessibility')]
final class CspAccessibilityListener
{
    public function __invoke(PolicyMutatedEvent $event): void
    {
        if ($event->scope->type->isFrontend()) {
            // Prefer external CSS over extending CSP for inline styles
        }
    }
}
```
