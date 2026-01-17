---
name: typo3-update-content-blocks
description: Content Blocks as an upgrade path for TYPO3 extensions. Modernizing classic TCA during version updates.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-update
  - typo3-content-blocks
triggers:
  - upgrade to content blocks
  - modernize extension
  - content blocks upgrade path
---

# Content Blocks as Upgrade Path

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-update](./SKILL.md) - Main update guide
> - [typo3-content-blocks SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md) - Migration guide

---

## 1. When to Adopt Content Blocks During Upgrade

### Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Upgrading v12 → v14 with simple content elements | ✅ Convert to Content Blocks |
| Upgrading with complex Extbase extensions | ⚠️ Keep Extbase, optionally use CB for TCA |
| New features during upgrade | ✅ Build with Content Blocks |
| Time-critical upgrade | ❌ Upgrade first, convert later |

---

## 2. Upgrade + Content Blocks Strategy

### Phase 1: TYPO3 Version Upgrade

```bash
# Focus on core upgrade first
ddev composer require typo3/cms-core:^14.0
ddev typo3 extension:setup
ddev typo3 upgrade:run
```

### Phase 2: Install Content Blocks

```bash
# Add Content Blocks extension
ddev composer require friendsoftypo3/content-blocks
ddev typo3 extension:setup
```

### Phase 3: Gradual Migration

Migrate content elements one at a time:

1. Create Content Block version
2. Run data migration script
3. Test thoroughly
4. Remove old TCA files

---

## 3. Side-by-Side Operation

During migration, both classic and Content Blocks elements can coexist:

```yaml
# New Content Block element
# ContentBlocks/ContentElements/hero-v2/config.yaml
name: myvendor/hero-v2
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
```

```php
// Classic element still works
// Configuration/TCA/Overrides/tt_content.php
$GLOBALS['TCA']['tt_content']['types']['myext_hero'] = [
    // ... existing config
];
```

---

## 4. Data Migration During Upgrade

### Combined Upgrade + Migration Command

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use TYPO3\CMS\Core\Database\ConnectionPool;

final class MigrateDuringUpgradeCommand extends Command
{
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $connection = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getConnectionForTable('tt_content');

        // Migrate CType
        $connection->update(
            'tt_content',
            ['CType' => 'myvendor_hero'],
            ['CType' => 'myext_hero']
        );

        // Copy field data if column names changed
        $connection->executeStatement('
            UPDATE tt_content 
            SET myvendor_hero_subheadline = tx_myext_subheadline 
            WHERE CType = "myvendor_hero"
        ');

        return Command::SUCCESS;
    }
}
```

---

## 5. Upgrade Checklist with Content Blocks

```markdown
## Pre-Upgrade
- [ ] Identify content elements suitable for Content Blocks
- [ ] Document field mappings
- [ ] Backup database

## TYPO3 Upgrade
- [ ] Update TYPO3 core
- [ ] Fix deprecations
- [ ] Run upgrade wizards

## Content Blocks Migration
- [ ] Install friendsoftypo3/content-blocks
- [ ] Create config.yaml for each element
- [ ] Create templates
- [ ] Run data migration
- [ ] Remove old TCA files

## Verification
- [ ] Test all migrated elements
- [ ] Check frontend rendering
- [ ] Verify backend forms
```

---

## References

- [typo3-update SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL-MIGRATION](../typo3-content-blocks/SKILL-MIGRATION.md)
- [TYPO3 Upgrade Guide](https://docs.typo3.org/m/typo3/guide-installation/main/en-us/Upgrade/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
