# 13. Common Recipes

Continues `typo3-powermail` from [full guide](full-guide.md).

## 13. Common Recipes

### Route Enhancer for SEO-Friendly URLs

```yaml
routeEnhancers:
  PowermailOptIn:
    type: Plugin
    routePath: '/optin/{mail}/{hash}'
    namespace: 'tx_powermail_pi1'
    requirements:
      mail: '\d+'
      hash: '[a-zA-Z0-9]+'
```

### Conditional Receiver Based on Form Field

Use `ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent` (see Section 6).

### Custom Spam Shield Method

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\SpamShield;

use In2code\Powermail\Domain\Validator\SpamShield\AbstractMethod;

final class ApiCheckMethod extends AbstractMethod
{
    public function spamCheck(): bool
    {
        $mail = $this->mail;
        // Return true if spam detected
        return $this->callExternalApi($mail);
    }
}
```

Register in TypoScript:

```typoscript
plugin.tx_powermail.settings.setup.spamshield.methods {
    100 {
        class = Vendor\MyExt\SpamShield\ApiCheckMethod
        _enable = 1
        configuration {
            apiUrl = https://spam-api.example.com
        }
    }
}
```

### Extend Form with TypoScript-Generated Fields

```typoscript
plugin.tx_powermail.settings.setup.manipulateVariablesInPowermailAllMarker {
    timestamp = TEXT
    # Avoid `strftime` (removed in PHP 8.4); use TEXT `date:` data instead
    timestamp.data = date:Y-m-d H:i:s
}
```
