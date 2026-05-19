# 4. Custom Finishers

Continues `typo3-powermail` from [full guide](full-guide.md).

## 4. Custom Finishers

Finishers run after successful form submission, sorted by TypoScript key.

### Registration

```typoscript
plugin.tx_powermail.settings.setup.finishers {
    # Lower number = runs first
    0.class = In2code\Powermail\Finisher\RateLimitFinisher
    10.class = In2code\Powermail\Finisher\SaveToAnyTableFinisher
    20.class = In2code\Powermail\Finisher\SendParametersFinisher
    finally.class = In2code\Powermail\Finisher\RedirectFinisher

    # Custom finisher
    50.class = Vendor\MyExt\Finisher\CrmFinisher
    50.config {
        apiUrl = https://crm.example.com/api
        apiKey = secret123
    }
}
```

### Creating a Custom Finisher

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Finisher;

use In2code\Powermail\Finisher\AbstractFinisher;
use In2code\Powermail\Domain\Model\Mail;

final class CrmFinisher extends AbstractFinisher
{
    /**
     * Method name MUST end with "Finisher"
     * Can have initialize*Finisher() called before
     */
    public function myCustomFinisher(): void
    {
        /** @var Mail $mail */
        $mail = $this->getMail();
        $settings = $this->getSettings();
        $configuration = $this->getConfiguration(); // TS config.*

        // Access form answers
        foreach ($mail->getAnswers() as $answer) {
            $fieldMarker = $answer->getField()->getMarker();
            $value = $answer->getValue();
            // Process...
        }

        // Access by marker
        $answers = $mail->getAnswersByFieldMarker();
        $email = $answers['email'] ?? null;

        // Check if form was actually submitted (not just displayed)
        if (!$this->isFormSubmitted()) {
            return;
        }
    }
}
```

### Built-in Finishers

| Class | Key | Purpose |
|-------|-----|---------|
| `RateLimitFinisher` | 0 | Consumes rate limiter tokens |
| `SaveToAnyTableFinisher` | 10 | Save answers to custom DB tables |
| `SendParametersFinisher` | 20 | POST form data to external URL |
| `RedirectFinisher` | `finally` | Runs last — special TypoScript key, not a numeric sort key |

### SaveToAnyTable Configuration

```typoscript
plugin.tx_powermail.settings.setup.dbEntry {
    1 {
        _enable = TEXT
        _enable.value = 1
        _table = fe_users
        _ifUnique.email = update  # update|skip|none
        username.value = {email}
        email.value = {email}
        first_name.value = {firstname}
        last_name.value = {lastname}
        pid.value = 123
    }
}
```
