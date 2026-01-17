---
name: typo3-extension-upgrade-content-blocks
description: Converting extensions to Content Blocks during upgrade. Step-by-step migration from classic TCA.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-extension-upgrade
  - typo3-content-blocks
triggers:
  - extension content blocks
  - convert extension to content blocks
---

# Extension Upgrade with Content Blocks

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-extension-upgrade](./SKILL.md) - Main extension upgrade guide
> - [typo3-content-blocks SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md) - Migration guide

---

## 1. Assessment: Should You Convert?

### Good Candidates for Content Blocks

- Simple content elements (hero, card, teaser)
- Record types without complex business logic
- Elements with straightforward field structures

### Keep as Classic

- Complex Extbase extensions with controllers
- Elements with custom DataProcessors
- Heavy backend module integration

---

## 2. Upgrade + Convert Workflow

```
┌─────────────────────────────────────────┐
│  1. Upgrade TYPO3 version first         │
├─────────────────────────────────────────┤
│  2. Stabilize extension on new version  │
├─────────────────────────────────────────┤
│  3. Install Content Blocks extension    │
├─────────────────────────────────────────┤
│  4. Convert elements one at a time      │
├─────────────────────────────────────────┤
│  5. Run data migration                  │
├─────────────────────────────────────────┤
│  6. Remove old TCA/SQL                  │
└─────────────────────────────────────────┘
```

---

## 3. Quick Conversion Example

### Before (Classic)

```
packages/my_ext/
├── Configuration/
│   ├── TCA/
│   │   └── Overrides/
│   │       └── tt_content.php
│   └── TypoScript/
│       └── setup.typoscript
├── Resources/
│   └── Private/
│       └── Templates/
│           └── Hero.html
└── ext_tables.sql
```

### After (Content Blocks)

```
packages/my_ext/
└── ContentBlocks/
    └── ContentElements/
        └── hero/
            ├── config.yaml
            └── templates/
                └── frontend.html
```

---

## 4. Migration Script Template

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use TYPO3\CMS\Core\Database\ConnectionPool;

#[AsCommand(name: 'myext:migrate-to-content-blocks')]
final class MigrateCommand extends Command
{
    private const MIGRATIONS = [
        ['old_ctype' => 'myext_hero', 'new_ctype' => 'myvendor_hero'],
        ['old_ctype' => 'myext_card', 'new_ctype' => 'myvendor_card'],
    ];

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $connection = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getConnectionForTable('tt_content');

        foreach (self::MIGRATIONS as $migration) {
            $count = $connection->update(
                'tt_content',
                ['CType' => $migration['new_ctype']],
                ['CType' => $migration['old_ctype']]
            );
            $output->writeln("Migrated {$count} records: {$migration['old_ctype']} → {$migration['new_ctype']}");
        }

        return Command::SUCCESS;
    }
}
```

---

## 5. Files to Remove After Migration

| File | Reason |
|------|--------|
| `Configuration/TCA/Overrides/tt_content.php` | Replaced by config.yaml |
| `ext_tables.sql` (migrated columns) | Auto-generated |
| `Resources/Private/Templates/ContentElements/` | Moved to ContentBlocks |
| `Configuration/TypoScript/` (rendering) | Auto-registered |

---

## References

- [typo3-extension-upgrade SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
