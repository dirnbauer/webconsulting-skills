# 17. Version constraints

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 17. Version constraints

Use **TYPO3 v14.1+** with **Content Blocks 2.x** (`friendsoftypo3/content-blocks` currently requires `typo3/cms-core: ^14.1` — confirm on [Packagist](https://packagist.org/packages/friendsoftypo3/content-blocks)).

```php
// ext_emconf.php — TYPO3 v14.1+ + Content Blocks 2.x
'depends' => [
    'typo3' => '14.1.0-14.99.99',
    'content_blocks' => '2.0.0-2.99.99',
],
```

---
