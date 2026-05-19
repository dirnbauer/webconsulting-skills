# 12. Extension Best Practices

Continues `typo3-powermail` from [full guide](full-guide.md).

## 12. Extension Best Practices

### Register Services (Services.yaml)

```yaml
services:
  Vendor\MyExt\EventListener\CrmSyncListener:
    tags:
      - name: event.listener
        identifier: 'vendor-myext/crm-sync'
```

Or use the `#[AsEventListener]` attribute (preferred on TYPO3 v14).

### Access Mail Answers Efficiently

```php
// By field marker (most common)
$answers = $mail->getAnswersByFieldMarker();
$email = $answers['email']?->getValue();

// By field UID
$answers = $mail->getAnswersByFieldUid();

// Filter by value type
$uploads = $mail->getAnswersByValueType(Answer::VALUE_TYPE_UPLOAD);
```

### Custom Data on Mail Object

```php
// Add custom data (available in all finishers/events)
$mail->addAdditionalData('crm_id', $crmResponse['id']);

// Retrieve in another finisher/event
$crmId = $mail->getAdditionalData()['crm_id'] ?? null;
```

### Rate Limiting

Powermail uses Symfony RateLimiter. Configure in `ext_conf_template.txt` or extension settings.

### Garbage Collection

Powermail auto-registers garbage collection for mails and answers (default: 30 days). Configure via Scheduler task `TableGarbageCollectionTask`.
