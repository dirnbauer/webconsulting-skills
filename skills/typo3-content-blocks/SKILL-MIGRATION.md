---
name: typo3-content-blocks-migration
description: Bidirectional migration between classic TYPO3 TCA/SQL extensions and Content Blocks. Includes step-by-step guides, field mappings, data migration scripts, and checklists for both directions.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-content-blocks
triggers:
  - migrate to content blocks
  - convert tca
  - modernize extension
  - tca to yaml
  - classic to content blocks
  - revert content blocks
  - content blocks to tca
  - yaml to tca
  - remove content blocks
  - classic extension
  - tca migration
  - content blocks migration
---

# Content Blocks Migration Guide

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skill:** [typo3-content-blocks](./SKILL.md) - Main Content Blocks development guide

This skill covers bidirectional migration between classic TYPO3 extensions (TCA/SQL/TypoScript) and the modern Content Blocks approach.

---

## 1. Migrating Classic Extensions to Content Blocks

This section guides you through converting traditional TYPO3 extensions (with separate TCA, SQL, TypoScript) to the modern Content Blocks approach.

### When to Migrate

| Scenario | Recommendation |
|----------|----------------|
| New content elements | ✅ Use Content Blocks from the start |
| Simple records (products, team, events) | ✅ Migrate to Content Blocks |
| Complex Extbase extensions with controllers | ⚠️ Keep Extbase, optionally use Content Blocks for TCA |
| Heavy business logic in domain models | ⚠️ Keep Extbase models, consider Content Blocks for forms only |
| Extensions with many plugins | ❌ Keep traditional approach |

### Migration Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  1. ANALYZE                                                       │
│     └─ Identify TCA, SQL, TypoScript, Templates                  │
├─────────────────────────────────────────────────────────────────┤
│  2. MAP                                                           │
│     └─ Create field mapping from TCA columns to Content Blocks   │
├─────────────────────────────────────────────────────────────────┤
│  3. CREATE                                                        │
│     └─ Build config.yaml with mapped fields                      │
├─────────────────────────────────────────────────────────────────┤
│  4. MIGRATE DATA                                                  │
│     └─ Rename columns if needed, update CTypes                   │
├─────────────────────────────────────────────────────────────────┤
│  5. CLEANUP                                                       │
│     └─ Remove old TCA, SQL, TypoScript files                     │
└─────────────────────────────────────────────────────────────────┘
```

### TCA to Content Blocks Field Mapping

| TCA Type | TCA renderType | Content Blocks Type | Notes |
|----------|----------------|---------------------|-------|
| `input` | - | `Text` | Basic text input |
| `input` | `inputDateTime` | `DateTime` | Date/time picker |
| `input` | `inputLink` | `Link` | Link browser |
| `input` | `colorPicker` | `Color` | Color picker |
| `input` | `slug` | `Slug` | URL slug |
| `text` | - | `Textarea` | Multi-line text |
| `text` | (richtext) | `Textarea` + `enableRichtext: true` | RTE |
| `check` | - | `Checkbox` | Boolean checkbox |
| `radio` | - | `Radio` | Radio buttons |
| `select` | `selectSingle` | `Select` | Single selection |
| `select` | `selectMultipleSideBySide` | `Select` + `multiple: true` | Multiple selection |
| `select` | `selectCheckBox` | `Select` + `renderType: selectCheckBox` | Checkbox group |
| `group` | - | `Relation` or `File` | Depends on internal_type |
| `file` | - | `File` | FAL references |
| `inline` | - | `Collection` | IRRE relations |
| `category` | - | `Category` | System categories |
| `flex` | - | `FlexForm` | FlexForm container |
| `json` | - | `Json` | JSON data |

### Migration Example 1: Content Element (tt_content)

**BEFORE (Classic):**

```php
// Configuration/TCA/Overrides/tt_content.php
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addPlugin(
    ['LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:ce.hero', 'myext_hero'],
    'CType',
    'my_ext'
);

$GLOBALS['TCA']['tt_content']['types']['myext_hero'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            tx_myext_subheadline,
            tx_myext_image,
            tx_myext_link,
        --div--;LLL:EXT:frontend/Resources/Private/Language/locallang_ttc.xlf:tabs.appearance,
            --palette--;;frames,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
    ',
];

$tempColumns = [
    'tx_myext_subheadline' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:subheadline',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_myext_image' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:image',
        'config' => [
            'type' => 'file',
            'maxitems' => 1,
            'allowed' => 'common-image-types',
        ],
    ],
    'tx_myext_link' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:link',
        'config' => [
            'type' => 'link',
        ],
    ],
];
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTCAcolumns('tt_content', $tempColumns);
```

```sql
-- ext_tables.sql
CREATE TABLE tt_content (
    tx_myext_subheadline varchar(255) DEFAULT '' NOT NULL,
    tx_myext_image int(11) DEFAULT 0 NOT NULL,
    tx_myext_link varchar(1024) DEFAULT '' NOT NULL
);
```

```typoscript
# Configuration/TypoScript/setup.typoscript
tt_content.myext_hero = FLUIDTEMPLATE
tt_content.myext_hero {
    templateName = Hero
    templateRootPaths.10 = EXT:my_ext/Resources/Private/Templates/
}
```

**AFTER (Content Blocks):**

```yaml
# ContentBlocks/ContentElements/hero/config.yaml
name: myvendor/hero
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
  - identifier: image
    type: File
    maxitems: 1
    allowed: common-image-types
  - identifier: link
    type: Link
```

```html
<!-- ContentBlocks/ContentElements/hero/templates/frontend.html -->
<section class="hero">
    <f:if condition="{data.image}">
        <f:for each="{data.image}" as="img">
            <f:image image="{img}" class="hero-bg"/>
        </f:for>
    </f:if>
    <h1>{data.header}</h1>
    <f:if condition="{data.subheadline}">
        <p>{data.subheadline}</p>
    </f:if>
    <f:if condition="{data.link}">
        <f:link.typolink parameter="{data.link}" class="btn">Learn More</f:link.typolink>
    </f:if>
</section>
```

**That's it!** No TCA files, no SQL, no TypoScript for rendering.

### Migration Example 2: Custom Record Table

**BEFORE (Classic):**

```php
// Configuration/TCA/tx_myext_domain_model_product.php
return [
    'ctrl' => [
        'title' => 'Product',
        'label' => 'name',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'sortby' => 'sorting',
        'languageField' => 'sys_language_uid',
        'transOrigPointerField' => 'l10n_parent',
        'transOrigDiffSourceField' => 'l10n_diffsource',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'iconfile' => 'EXT:my_ext/Resources/Public/Icons/product.svg',
    ],
    'columns' => [
        'hidden' => [
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.hidden',
            'config' => ['type' => 'check'],
        ],
        'name' => [
            'label' => 'Name',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'description' => [
            'label' => 'Description',
            'config' => [
                'type' => 'text',
                'enableRichtext' => true,
            ],
        ],
        'price' => [
            'label' => 'Price',
            'config' => [
                'type' => 'number',
                'format' => 'decimal',
            ],
        ],
        // ... more columns
    ],
    'types' => [
        '1' => ['showitem' => 'hidden, name, price, description'],
    ],
];
```

```sql
-- ext_tables.sql
CREATE TABLE tx_myext_domain_model_product (
    name varchar(255) DEFAULT '' NOT NULL,
    description text,
    price double(11,2) DEFAULT 0.00 NOT NULL
);
```

**AFTER (Content Blocks):**

```yaml
# ContentBlocks/RecordTypes/product/config.yaml
name: myvendor/product
table: tx_myext_domain_model_product
labelField: name
languageAware: true
sortable: true
softDelete: true
trackCreationDate: true
trackUpdateDate: true
restriction:
  disabled: true
  startTime: true
  endTime: true
security:
  ignorePageTypeRestriction: true
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: price
    type: Number
    format: decimal
  - identifier: description
    type: Textarea
    enableRichtext: true
```

**That's it!** No TCA file, no SQL file.

### Migration Example 3: IRRE Child Records

**BEFORE (Classic with IRRE):**

```php
// Parent TCA with inline field
'slides' => [
    'label' => 'Slides',
    'config' => [
        'type' => 'inline',
        'foreign_table' => 'tx_myext_domain_model_slide',
        'foreign_field' => 'parentid',
        'foreign_table_field' => 'parenttable',
        'maxitems' => 10,
        'appearance' => [
            'collapseAll' => true,
            'levelLinksPosition' => 'both',
            'useSortable' => true,
        ],
    ],
],

// Separate TCA file for tx_myext_domain_model_slide
// Separate SQL for tx_myext_domain_model_slide
```

**AFTER (Content Blocks with inline Collection):**

```yaml
# ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    labelField: title
    maxitems: 10
    appearance:
      collapseAll: true
      levelLinksPosition: both
    fields:
      - identifier: title
        type: Text
      - identifier: image
        type: File
        maxitems: 1
        allowed: common-image-types
      - identifier: link
        type: Link
```

**Or with separate Record Type as child:**

```yaml
# ContentBlocks/RecordTypes/slide/config.yaml
name: myvendor/slide
table: tx_myext_domain_model_slide
labelField: title
fields:
  - identifier: title
    type: Text
  - identifier: image
    type: File
    maxitems: 1
  - identifier: link
    type: Link

# ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    foreign_table: tx_myext_domain_model_slide
    shareAcrossTables: true
    shareAcrossFields: true
```

### Data Migration Script

When migrating existing content, you may need to rename columns and update CType values:

```php
<?php
// Classes/Command/MigrateToContentBlocksCommand.php
namespace MyVendor\MyExt\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

class MigrateToContentBlocksCommand extends Command
{
    protected function configure(): void
    {
        $this->setDescription('Migrate classic content elements to Content Blocks');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $connection = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getConnectionForTable('tt_content');
        
        // Step 1: Update CType from old to new
        $oldCType = 'myext_hero';
        $newCType = 'myvendor_hero';  // Content Blocks generates: vendor_name
        
        $updated = $connection->update(
            'tt_content',
            ['CType' => $newCType],
            ['CType' => $oldCType]
        );
        $output->writeln("Updated $updated records from $oldCType to $newCType");
        
        return Command::SUCCESS;
    }
}
```

### Database Column Renaming

If Content Blocks generates different column names, use the Install Tool:

1. Create the Content Block (new columns will be detected)
2. Go to Admin Tools → Maintenance → Analyze Database Structure
3. Add new columns (Content Blocks generated)
4. Run migration script to copy data:

```sql
-- Copy data from old columns to new columns
UPDATE tt_content 
SET myvendor_hero_subheadline = tx_myext_subheadline
WHERE CType = 'myvendor_hero' AND tx_myext_subheadline != '';

-- After verification, drop old columns via Install Tool
```

### Keeping Same Column Names (Recommended)

To avoid data migration, configure Content Blocks to use the same column names:

```yaml
name: myvendor/hero
prefixFields: false  # No automatic prefixing
fields:
  - identifier: tx_myext_subheadline  # Use exact old column name
    type: Text
  - identifier: tx_myext_image
    type: File
  - identifier: tx_myext_link
    type: Link
```

Or use `prefixField: false` per field:

```yaml
name: myvendor/hero
prefixFields: true  # Enable prefixing by default
fields:
  - identifier: tx_myext_subheadline
    type: Text
    prefixField: false  # Keep original column name
```

### Migration Checklist

```markdown
## Pre-Migration
- [ ] List all content elements and record types to migrate
- [ ] Document existing TCA column names
- [ ] Backup database
- [ ] Install friendsoftypo3/content-blocks

## For Each Content Type
- [ ] Create config.yaml with field mappings
- [ ] Create frontend.html template
- [ ] Create backend-preview.html (optional)
- [ ] Create labels.xlf translations
- [ ] Run cache:flush and extension:setup

## Data Migration
- [ ] Update CType values in database
- [ ] Rename columns if needed (or use prefixField: false)
- [ ] Verify data displays correctly

## Cleanup
- [ ] Remove old TCA files
- [ ] Remove ext_tables.sql (or remove migrated columns)
- [ ] Remove old TypoScript rendering config
- [ ] Remove old Fluid templates
- [ ] Update documentation
```

### Files to Delete After Migration

| Classic File | Why Remove |
|--------------|------------|
| `Configuration/TCA/*.php` | Replaced by config.yaml |
| `Configuration/TCA/Overrides/tt_content.php` | Replaced by config.yaml |
| `ext_tables.sql` | Auto-generated by Content Blocks |
| `Configuration/TypoScript/setup.typoscript` (rendering part) | Auto-registered |
| `Resources/Private/Templates/ContentElements/*.html` | Moved to ContentBlocks folder |

---

## 2. Reverting Content Blocks to Classic Extension Format

This section guides you through converting Content Blocks back to traditional TYPO3 extension format with separate TCA, SQL, and TypoScript files.

### When to Revert

| Scenario | Recommendation |
|----------|----------------|
| Content Blocks has breaking changes | ✅ Revert to classic for stability |
| Need TCA features not supported by Content Blocks | ✅ Revert for full TCA control |
| Team prefers traditional TYPO3 structure | ✅ Revert for familiarity |
| Complex Extbase domain models needed | ✅ Revert for full Extbase integration |
| Performance-critical applications | ⚠️ Consider revert (measure first) |
| Simple content elements working fine | ❌ Keep Content Blocks |

### Revert Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  1. ANALYZE                                                       │
│     └─ Document all config.yaml files and field mappings        │
├─────────────────────────────────────────────────────────────────┤
│  2. GENERATE                                                      │
│     └─ Create TCA, SQL, TypoScript from config.yaml             │
├─────────────────────────────────────────────────────────────────┤
│  3. MOVE TEMPLATES                                                │
│     └─ Move Fluid templates to traditional locations             │
├─────────────────────────────────────────────────────────────────┤
│  4. MIGRATE DATA                                                  │
│     └─ Update CTypes, rename columns if needed                   │
├─────────────────────────────────────────────────────────────────┤
│  5. REMOVE DEPENDENCY                                             │
│     └─ Uninstall Content Blocks, delete ContentBlocks folder    │
└─────────────────────────────────────────────────────────────────┘
```

### Content Blocks to TCA Field Mapping (Reverse)

| Content Blocks Type | TCA type | TCA renderType | Additional Config |
|---------------------|----------|----------------|-------------------|
| `Text` | `input` | - | `max => 255` |
| `Textarea` | `text` | - | `rows => 5` |
| `Textarea` + `enableRichtext` | `text` | - | `enableRichtext => true` |
| `Email` | `email` | - | - |
| `Link` | `link` | - | - |
| `Number` | `number` | - | `format => 'integer'` or `'decimal'` |
| `DateTime` | `datetime` | - | `format => 'date'` or `'datetime'` |
| `Color` | `color` | - | - |
| `Checkbox` | `check` | - | - |
| `Radio` | `radio` | - | `items => [...]` |
| `Slug` | `slug` | - | `generatorOptions => [...]` |
| `Password` | `password` | - | - |
| `Select` | `select` | `selectSingle` | `items => [...]` |
| `Select` + `multiple` | `select` | `selectMultipleSideBySide` | - |
| `File` | `file` | - | `allowed => '...'` |
| `Relation` | `group` or `select` | - | `foreign_table => '...'` |
| `Category` | `category` | - | - |
| `Collection` (inline) | `inline` | - | `foreign_table => '...'` |
| `Collection` (with fields) | `inline` | - | `foreign_table => auto-generated` |
| `FlexForm` | `flex` | - | `ds => [...]` |
| `Json` | `json` | - | - |
| `Tab` | - | - | `--div--;Label` in showitem |
| `Palette` | - | - | `--palette--;;name` in showitem |

### YAML Options to TCA Config Mapping

| Content Blocks YAML | TCA Config Key | Example |
|---------------------|----------------|---------|
| `required: true` | `required => true` | - |
| `default: "value"` | `default => 'value'` | - |
| `placeholder: "text"` | `placeholder => 'text'` | - |
| `minitems: 1` | `minitems => 1` | - |
| `maxitems: 10` | `maxitems => 10` | - |
| `allowed: common-image-types` | `allowed => 'common-image-types'` | - |
| `displayCond: 'FIELD:x:=:1'` | `displayCond => 'FIELD:x:=:1'` | - |
| `onChange: reload` | `onChange => 'reload'` | - |
| `labelField: name` | `ctrl['label'] => 'name'` | Record Types |
| `languageAware: true` | `ctrl['languageField']` etc. | Record Types |
| `sortable: true` | `ctrl['sortby'] => 'sorting'` | Record Types |
| `softDelete: true` | `ctrl['delete'] => 'deleted'` | Record Types |

### Revert Example: Content Element

**BEFORE (Content Blocks):**

```yaml
# ContentBlocks/ContentElements/hero/config.yaml
name: myvendor/hero
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
  - identifier: hero_image
    type: File
    maxitems: 1
    allowed: common-image-types
  - identifier: cta_link
    type: Link
  - identifier: cta_text
    type: Text
```

**AFTER (Classic):**

**Step 1: Create TCA Override**

```php
<?php
// Configuration/TCA/Overrides/tt_content.php

use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;

defined('TYPO3') or die();

// Register the content element
ExtensionManagementUtility::addPlugin(
    [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:ce.hero.title',
        'value' => 'myext_hero',
        'icon' => 'EXT:my_ext/Resources/Public/Icons/ContentElements/hero.svg',
        'group' => 'default',
    ],
    'CType',
    'my_ext'
);

// Define columns
$tempColumns = [
    'tx_myext_subheadline' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.subheadline',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_myext_hero_image' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.hero_image',
        'config' => [
            'type' => 'file',
            'maxitems' => 1,
            'allowed' => 'common-image-types',
        ],
    ],
    'tx_myext_cta_link' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.cta_link',
        'config' => [
            'type' => 'link',
        ],
    ],
    'tx_myext_cta_text' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.cta_text',
        'config' => [
            'type' => 'input',
            'size' => 30,
            'max' => 100,
        ],
    ],
];

ExtensionManagementUtility::addTCAcolumns('tt_content', $tempColumns);

// Define showitem
$GLOBALS['TCA']['tt_content']['types']['myext_hero'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            tx_myext_subheadline,
            tx_myext_hero_image,
            tx_myext_cta_link,
            tx_myext_cta_text,
        --div--;LLL:EXT:frontend/Resources/Private/Language/locallang_ttc.xlf:tabs.appearance,
            --palette--;;frames,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
    ',
];
```

**Step 2: Create SQL Schema**

```sql
-- ext_tables.sql
CREATE TABLE tt_content (
    tx_myext_subheadline varchar(255) DEFAULT '' NOT NULL,
    tx_myext_hero_image int(11) unsigned DEFAULT 0 NOT NULL,
    tx_myext_cta_link varchar(1024) DEFAULT '' NOT NULL,
    tx_myext_cta_text varchar(100) DEFAULT '' NOT NULL
);
```

**Step 3: Create TypoScript Rendering**

```typoscript
# Configuration/TypoScript/setup.typoscript
tt_content.myext_hero = FLUIDTEMPLATE
tt_content.myext_hero {
    templateName = Hero
    templateRootPaths {
        10 = EXT:my_ext/Resources/Private/Templates/ContentElements/
    }
    dataProcessing {
        10 = TYPO3\CMS\Frontend\DataProcessing\FilesProcessor
        10 {
            references.fieldName = tx_myext_hero_image
            as = heroImages
        }
    }
}
```

**Step 4: Update Fluid Template**

```html
<!-- Resources/Private/Templates/ContentElements/Hero.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default"/>
<f:section name="Main">
    <section class="hero-banner">
        <f:if condition="{heroImages}">
            <f:for each="{heroImages}" as="image">
                <f:image image="{image}" alt="{data.header}" class="hero-image"/>
            </f:for>
        </f:if>
        
        <div class="hero-content">
            <h1>{data.header}</h1>
            <f:if condition="{data.tx_myext_subheadline}">
                <p class="subheadline">{data.tx_myext_subheadline}</p>
            </f:if>
            
            <f:if condition="{data.tx_myext_cta_link}">
                <f:link.typolink parameter="{data.tx_myext_cta_link}" class="btn btn-primary">
                    {data.tx_myext_cta_text -> f:or(default: 'Learn more')}
                </f:link.typolink>
            </f:if>
        </div>
    </section>
</f:section>
</html>
```

### Data Migration Script (Revert Direction)

```php
<?php
// Classes/Command/RevertFromContentBlocksCommand.php
namespace MyVendor\MyExt\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

#[AsCommand(
    name: 'myext:revert-content-blocks',
    description: 'Revert Content Blocks elements to classic TCA format'
)]
class RevertFromContentBlocksCommand extends Command
{
    private const CTYPE_MAPPING = [
        'myvendor_hero' => 'myext_hero',
        'myvendor_accordion' => 'myext_accordion',
    ];

    private const COLUMN_MAPPING = [
        'myvendor_hero_subheadline' => 'tx_myext_subheadline',
        'myvendor_hero_hero_image' => 'tx_myext_hero_image',
    ];

    protected function configure(): void
    {
        $this
            ->addOption('dry-run', null, InputOption::VALUE_NONE, 'Show what would be changed')
            ->addOption('copy-data', null, InputOption::VALUE_NONE, 'Copy column data');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        $dryRun = $input->getOption('dry-run');
        $copyData = $input->getOption('copy-data');

        $connection = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getConnectionForTable('tt_content');

        $io->title('Reverting Content Blocks to Classic Format');

        // Update CTypes
        foreach (self::CTYPE_MAPPING as $oldCType => $newCType) {
            $count = $connection->count('*', 'tt_content', ['CType' => $oldCType]);
            $io->writeln("  $oldCType → $newCType: $count records");
            
            if (!$dryRun && $count > 0) {
                $connection->update('tt_content', ['CType' => $newCType], ['CType' => $oldCType]);
            }
        }

        // Copy column data if requested
        if ($copyData && !$dryRun) {
            foreach (self::COLUMN_MAPPING as $oldColumn => $newColumn) {
                try {
                    $connection->executeStatement(
                        "UPDATE tt_content SET $newColumn = $oldColumn WHERE $oldColumn IS NOT NULL AND $oldColumn != ''"
                    );
                } catch (\Exception $e) {
                    $io->warning("Column copy failed: " . $e->getMessage());
                }
            }
        }

        $io->success($dryRun ? 'Dry run completed' : 'Migration completed');
        return Command::SUCCESS;
    }
}
```

### Template Variable Changes

When reverting, update Fluid template variable names:

| Content Blocks | Classic |
|----------------|---------|
| `{data.fieldname}` | `{data.tx_myext_fieldname}` |
| `{data.my_image}` → auto-resolved | Use DataProcessor + `{processedImages}` |
| `{data.collection_items}` → auto-resolved | Use DatabaseQueryProcessor + `{items}` |
| `{cb:assetPath()}` | Static path: `EXT:my_ext/Resources/Public/...` |
| `{cb:languagePath()}` | `LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:` |

### Complete Revert Checklist

```markdown
## Pre-Revert
- [ ] Document all Content Blocks config.yaml files
- [ ] Map field identifiers to TCA column names
- [ ] Backup database
- [ ] Create branch for revert work

## For Each Content Type
- [ ] Create TCA PHP file(s)
- [ ] Add columns to ext_tables.sql
- [ ] Create TypoScript rendering
- [ ] Move/update Fluid templates (update variable names!)
- [ ] Move translations to locallang.xlf
- [ ] Move icons to Resources/Public/Icons/

## Data Migration
- [ ] Update CType values in database
- [ ] Copy data from Content Blocks columns to classic columns
- [ ] Test data displays correctly
- [ ] Verify file relations work

## Cleanup
- [ ] Remove ContentBlocks folder
- [ ] Remove friendsoftypo3/content-blocks from composer.json
- [ ] Run: composer update
- [ ] Remove old columns via Install Tool (after verification)
- [ ] Clear all caches

## Testing
- [ ] All content elements render correctly
- [ ] All record types editable in backend
- [ ] File relations display correctly
- [ ] Translations work
- [ ] No PHP errors in log
```

### Removing Content Blocks Dependency

```bash
# After successful revert and testing
ddev composer remove friendsoftypo3/content-blocks

# Clear caches
ddev typo3 cache:flush

# Update database (remove orphaned columns)
# Go to Admin Tools → Maintenance → Analyze Database Structure
# Select "Remove" for the old Content Blocks columns
```

---

## References

- [Content Blocks Documentation](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/)
- [TCA Reference](https://docs.typo3.org/m/typo3/reference-tca/main/en-us/)
- [Main Content Blocks Skill](./SKILL.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection, adapted from the official Content Blocks documentation.
