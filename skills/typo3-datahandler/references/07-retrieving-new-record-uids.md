# 7. Retrieving New Record UIDs

Continues `typo3-datahandler` from [full guide](full-guide.md).

## 7. Retrieving New Record UIDs

After processing, get the real UIDs for NEW records:

```php
<?php
declare(strict_types=1);

$dataHandler->process_datamap();

// Get the real UID for 'NEW_1'
$newContentUid = $dataHandler->substNEWwithIDs['NEW_1'] ?? null;

if ($newContentUid === null) {
    throw new \RuntimeException('Failed to create content element');
}
```
