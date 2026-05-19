# 10. Version Constraints for Extensions

Continues `typo3-datahandler` from [full guide](full-guide.md).

## 10. Version Constraints for Extensions

When creating extensions that use DataHandler, ensure proper version constraints:

```php
<?php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '1.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '14.0.0-14.99.99',
            'php' => '8.2.0-8.4.99',
        ],
    ],
];
```
