# 6. PSR-14 Events

Continues `typo3-powermail` from [full guide](full-guide.md).

## 6. PSR-14 Events

### Form Lifecycle Events

```php
// Before form is rendered
FormControllerFormActionEvent

// Before confirmation page
FormControllerConfirmationActionEvent

// After mail is saved to database
FormControllerCreateActionAfterMailDbSavedEvent

// After submit view is built
FormControllerCreateActionAfterSubmitViewEvent

// Before final view is rendered
FormControllerCreateActionBeforeRenderViewEvent

// Controller initialization
FormControllerInitializeObjectEvent
```

### Mail Events

```php
// Modify receiver email addresses
ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent

// Modify receiver name
ReceiverMailReceiverPropertiesServiceGetReceiverNameEvent

// Modify sender email (receiver mail)
ReceiverMailSenderPropertiesGetSenderEmailEvent

// Modify sender name (receiver mail)
ReceiverMailSenderPropertiesGetSenderNameEvent

// Modify sender email (confirmation mail)
SenderMailPropertiesGetSenderEmailEvent

// Modify sender name (confirmation mail)
SenderMailPropertiesGetSenderNameEvent

// Modify email body before sending
SendMailServiceCreateEmailBodyEvent

// Before email is sent (last chance to modify)
SendMailServicePrepareAndSendEvent
```

### Other Events

```php
// Control if mail should be saved to DB
CheckIfMailIsAllowedToSaveEvent

// Custom validation logic
CustomValidatorEvent

// Prefill field values
PrefillFieldViewHelperEvent
PrefillMultiFieldViewHelperEvent

// File upload processing
UploadServicePreflightEvent
UploadServiceGetFilesEvent
GetNewPathAndFilenameEvent

// Before password is hashed
MailFactoryBeforePasswordIsHashedEvent

// Modify mail variables/markers
MailRepositoryGetVariablesWithMarkersFromMailEvent

// Validation data attributes
ValidationDataAttributeViewHelperEvent

// Double opt-in confirmation
FormControllerOptinConfirmActionAfterPersistEvent
FormControllerOptinConfirmActionBeforeRenderViewEvent

// Disclaimer/unsubscribe
FormControllerDisclaimerActionBeforeRenderViewEvent
```

### Example: Modify Receiver Email (from form answers)

`ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent` only exposes `getEmailArray()` / `setEmailArray()` and `getService()` — the service does **not** publish the `Mail` model, so you cannot read field markers from that event alone. For routing based on answers, listen when the mail is available, e.g. **`SendMailServicePrepareAndSendEvent`**:

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\SendMailServicePrepareAndSendEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/dynamic-receiver')]
final class DynamicReceiverListener
{
    public function __invoke(SendMailServicePrepareAndSendEvent $event): void
    {
        $mail = $event->getSendMailService()->getMail();
        $answers = $mail->getAnswersByFieldMarker();
        $department = $answers['department'] ?? null;
        if ($department === null) {
            return;
        }

        $value = (string)$department->getValue();
        $emailConfig = $event->getEmail();
        // Adjust the receiver list inside $emailConfig for your Powermail / Symfony Mailer setup, then:
        // $event->setEmail($emailConfig);
    }
}
```

To tweak the raw address list earlier in the pipeline, use **`ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent`** with `getEmailArray()` / `setEmailArray()` when you do not need access to individual answers.

### Example: Prevent DB Save

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\CheckIfMailIsAllowedToSaveEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/skip-db-save')]
final class SkipDbSaveListener
{
    public function __invoke(CheckIfMailIsAllowedToSaveEvent $event): void
    {
        // Skip DB save for specific forms
        $form = $event->getMail()->getForm();
        if ($form !== null && $form->getTitle() === 'Contact (no storage)') {
            $event->setSavingOfMailAllowed(false);
        }
    }
}
```
