# 8. Upgrade Workflow Integration

Continues `typo3-fractor` from [full guide](full-guide.md).

## 8. Upgrade Workflow Integration

### Recommended Order

```
1. git checkout -b feature/typo3-upgrade
2. Run Rector (PHP migrations)        → vendor/bin/rector process
3. Run Fractor (non-PHP migrations)   → vendor/bin/fractor process
4. Run PHP-CS-Fixer (code style)      → vendor/bin/php-cs-fixer fix
5. Run PHPStan (static analysis)      → vendor/bin/phpstan analyse
6. Run Tests                          → vendor/bin/phpunit
7. Manual testing in target version
```

### Combined fractor.php for Extension Development

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;
use a9f\FractorTypoScript\Configuration\TypoScriptProcessorOption;
use Helmich\TypoScriptParser\Parser\Printer\PrettyPrinterConfiguration;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/Configuration/',
        __DIR__ . '/Resources/',
    ])
    ->withSkip([
        __DIR__ . '/Resources/Public/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ])
    ->withOptions([
        TypoScriptProcessorOption::INDENT_SIZE => 4,
        TypoScriptProcessorOption::INDENT_CHARACTER => PrettyPrinterConfiguration::INDENTATION_STYLE_SPACES,
    ]);
```
