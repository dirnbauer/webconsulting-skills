---
name: typo3-rector-content-blocks
description: Rector patterns for Content Blocks migration. Automating TCA to Content Blocks conversion and code updates.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-rector
  - typo3-content-blocks
triggers:
  - rector content blocks
  - migrate tca rector
  - content blocks automation
---

# Rector for Content Blocks Migration

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-rector](./SKILL.md) - Main Rector guide
> - [typo3-content-blocks SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md) - Migration guide

---

## 1. Automated Migration Possibilities

### What Rector Can Help With

| Task | Rector Support |
|------|---------------|
| Update CType references in PHP | ✅ Custom rule possible |
| Update field names in queries | ✅ Custom rule possible |
| Convert TCA to config.yaml | ❌ Manual (use SKILL-MIGRATION) |
| Update Fluid templates | ❌ Manual or Fractor |

---

## 2. Custom Rector Rule: CType Migration

### Rule Definition

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Rector;

use PhpParser\Node;
use PhpParser\Node\Scalar\String_;
use Rector\Rector\AbstractRector;
use Symplify\RuleDocGenerator\ValueObject\RuleDefinition;

final class ContentBlocksCTypeMigrationRector extends AbstractRector
{
    private const CTYPE_MAPPING = [
        'myext_hero' => 'myvendor_hero',
        'myext_accordion' => 'myvendor_accordion',
    ];

    public function getRuleDefinition(): RuleDefinition
    {
        return new RuleDefinition(
            'Migrate classic CTypes to Content Blocks CTypes',
            []
        );
    }

    public function getNodeTypes(): array
    {
        return [String_::class];
    }

    public function refactor(Node $node): ?Node
    {
        if (!$node instanceof String_) {
            return null;
        }

        $oldCType = $node->value;
        if (!isset(self::CTYPE_MAPPING[$oldCType])) {
            return null;
        }

        return new String_(self::CTYPE_MAPPING[$oldCType]);
    }
}
```

### Register in rector.php

```php
<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;
use Vendor\MyExtension\Rector\ContentBlocksCTypeMigrationRector;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
    ])
    ->withRules([
        ContentBlocksCTypeMigrationRector::class,
    ]);
```

---

## 3. Field Name Migration Rule

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Rector;

use PhpParser\Node;
use PhpParser\Node\Scalar\String_;
use Rector\Rector\AbstractRector;

final class ContentBlocksFieldMigrationRector extends AbstractRector
{
    private const FIELD_MAPPING = [
        'tx_myext_subheadline' => 'myvendor_hero_subheadline',
        'tx_myext_image' => 'myvendor_hero_image',
        'tx_myext_cta_link' => 'myvendor_hero_cta_link',
    ];

    public function getNodeTypes(): array
    {
        return [String_::class];
    }

    public function refactor(Node $node): ?Node
    {
        if (!$node instanceof String_) {
            return null;
        }

        $oldField = $node->value;
        if (!isset(self::FIELD_MAPPING[$oldField])) {
            return null;
        }

        return new String_(self::FIELD_MAPPING[$oldField]);
    }
}
```

---

## 4. Running Migration

```bash
# Dry run to preview changes
ddev exec vendor/bin/rector process --dry-run

# Apply changes
ddev exec vendor/bin/rector process

# Verify changes
git diff
```

---

## 5. Combined with Fractor

For non-PHP files (TypoScript, Fluid), use Fractor:

```bash
# Install Fractor
ddev composer require --dev ssch/typo3-fractor

# Run Fractor for TypoScript/Fluid
ddev exec vendor/bin/fractor process
```

---

## References

- [typo3-rector SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md)
- [Rector Custom Rules](https://getrector.com/documentation/custom-rules)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
