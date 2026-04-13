# TYPO3 CI Configuration Patterns

## 1. ext_emconf.php and strict_types

- `ext_emconf.php` must NOT contain `declare(strict_types=1)` — TER cannot parse it
- PHP-CS-Fixer rule `declare_strict_types => true` must exclude ext_emconf.php
- Pattern: `->notPath('ext_emconf.php')` in Finder config
- The shared `typo3-ci-workflows` config already handles this

## 2. Shared PHP-CS-Fixer config factory

Use the shared factory from `netresearch/typo3-ci-workflows` in `Build/.php-cs-fixer.php`:

```php
<?php
declare(strict_types=1);

// Build/.php-cs-fixer.php
$createConfig = require __DIR__ . '/../.Build/vendor/netresearch/typo3-ci-workflows/config/php-cs-fixer/config.php';

return $createConfig(<<<'EOF'
    Copyright header here
EOF, __DIR__ . '/..');
```

- Requires `"netresearch/typo3-ci-workflows": "^1.0"` in `require-dev`
- Benefits: centralized rules, ext_emconf.php exclusion, consistent formatting
- **TYPO3 12 compatibility**: `typo3-ci-workflows` may pull in dependencies for TYPO3 13, causing conflicts. For TYPO3 12 extensions, you may need to inline the config or ensure you use compatible dependency versions, such as `saschaegerer/phpstan-typo3: ^2.0`.

## 3. labeler.yml for TYPO3 extensions

Standard labeler config for PR auto-labeling:

```yaml
documentation:
  - changed-files:
      - any-glob-to-any-file: ['Documentation/**', '*.md']
configuration:
  - changed-files:
      - any-glob-to-any-file: ['Configuration/**', 'ext_emconf.php', 'composer.json']
tests:
  - changed-files:
      - any-glob-to-any-file: ['Tests/**', 'phpunit*.xml']
ci:
  - changed-files:
      - any-glob-to-any-file: ['.github/**']
```

## 4. Composer allow-plugins for CI dependencies

When using `typo3-ci-workflows`, fractor, or infection, add their installers to `allow-plugins`:

```json
{
    "config": {
        "allow-plugins": {
            "a9f/fractor-extension-installer": true,
            "infection/extension-installer": true,
            "captainhook/hook-installer": true
        }
    }
}
```
