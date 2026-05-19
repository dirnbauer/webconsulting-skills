# 5. Custom Validators

Continues `typo3-powermail` from [full guide](full-guide.md).

## 5. Custom Validators

### Creating a Custom Validator (PSR-14 Event)

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\CustomValidatorEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/custom-validator')]
final class CustomValidatorListener
{
    public function __invoke(CustomValidatorEvent $event): void
    {
        $mail = $event->getMail();
        $validator = $event->getCustomValidator();

        foreach ($mail->getAnswers() as $answer) {
            $field = $answer->getField();
            if ($field === null || $field->getMarker() !== 'company_vat') {
                continue;
            }
            if (!$this->isValidVat((string)$answer->getValue())) {
                $validator->setErrorAndMessage($field, 'Invalid VAT number');
            }
        }
    }

    private function isValidVat(string $vat): bool
    {
        return (bool)preg_match('/^[A-Z]{2}\d{8,12}$/', $vat);
    }
}
```

### Built-in Validators

| Validator | Purpose |
|-----------|---------|
| `InputValidator` | Email, URL, phone, number, letters, min/max length, regex |
| `UploadValidator` | File size, extension whitelist |
| `PasswordValidator` | Password match and strength |
| `CaptchaValidator` | Built-in CAPTCHA |
| *(Spam shield)* | Spam checking is distributed across multiple `Domain\Validator\SpamShield\AbstractMethod` subclasses (`HoneyPodMethod`, `LinkMethod`, …), orchestrated by `SpamShieldValidator` |
| `UniqueValidator` | Unique field values |
| `ForeignValidator` | Validate against foreign table |
| `CustomValidator` | TypoScript-based custom rules |

### Spam Shield Methods

| Method | Weight | Description |
|--------|--------|-------------|
| `HoneyPodMethod` | 5 | Hidden honeypot field |
| `LinkMethod` | 3 | Excessive links detection |
| `NameMethod` | 3 | Suspicious name patterns |
| `SessionMethod` | 5 | Session/cookie check (shipping TypoScript: **`_enable = 0`** — opt-in because it sets a cookie) |
| `UniqueMethod` | 2 | Duplicate submission check |
| `ValueBlacklistMethod` | 7 | Blacklisted content |
| `IpBlacklistMethod` | 7 | Blacklisted IP addresses |
| `RateLimitMethod` | 100 | Request rate limiting |
