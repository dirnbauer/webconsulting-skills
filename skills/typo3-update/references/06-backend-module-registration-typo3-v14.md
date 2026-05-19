# 6. Backend Module Registration (TYPO3 v14)

Continues `typo3-update` from [full guide](full-guide.md).

## 6. Backend Module Registration (TYPO3 v14)

### Configuration/Backend/Modules.php

```php
<?php
// Configuration/Backend/Modules.php
return [
    'web_myextension' => [
        'parent' => 'content',
        'position' => ['after' => 'records'],
        'access' => 'user,group',
        'iconIdentifier' => 'myextension-module',
        'path' => '/module/content/myextension',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExtension',
        'controllerActions' => [
            \Vendor\MyExtension\Controller\BackendController::class => [
                'index',
                'list',
                'show',
            ],
        ],
    ],
];
```

### Icon Registration

```php
<?php
// Configuration/Icons.php
return [
    'myextension-module' => [
        'provider' => \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/module.svg',
    ],
];
```
