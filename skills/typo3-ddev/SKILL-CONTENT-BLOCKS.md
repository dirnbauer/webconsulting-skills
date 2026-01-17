---
name: typo3-ddev-content-blocks
description: Local Content Blocks development with DDEV. Setup, testing, and debugging Content Blocks extensions.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-ddev
  - typo3-content-blocks
triggers:
  - ddev content blocks
  - content blocks local development
  - content blocks setup
---

# Content Blocks Development with DDEV

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-ddev](./SKILL.md) - Main DDEV guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. Initial Setup

### Install Content Blocks Extension

```bash
# Start DDEV
ddev start

# Install Content Blocks
ddev composer require friendsoftypo3/content-blocks

# Activate extension
ddev typo3 extension:setup
```

### Project Structure

```
my-typo3-project/
├── .ddev/
│   └── config.yaml
├── packages/
│   └── my_extension/
│       └── ContentBlocks/
│           ├── ContentElements/
│           │   └── hero/
│           │       ├── config.yaml
│           │       └── templates/
│           └── RecordTypes/
│               └── team-member/
│                   └── config.yaml
├── public/
└── composer.json
```

---

## 2. Development Workflow

### Create Content Block

```bash
# Create Content Element
ddev typo3 make:content-block myvendor/hero --type=content-element

# Create Record Type
ddev typo3 make:content-block myvendor/team-member --type=record-type
```

### Cache Management

```bash
# Flush all caches after config.yaml changes
ddev typo3 cache:flush

# Rebuild Content Blocks cache specifically
ddev typo3 cache:flush -g system
```

### Database Schema Updates

```bash
# After adding new fields
ddev typo3 extension:setup

# Or via Install Tool
ddev launch /typo3/install.php
```

---

## 3. Debugging Content Blocks

### Enable Debug Mode

```php
// config/system/settings.php
return [
    'BE' => [
        'debug' => true,
    ],
    'FE' => [
        'debug' => true,
    ],
    'SYS' => [
        'devIPmask' => '*',
        'displayErrors' => 1,
        'exceptionalErrors' => E_ALL,
    ],
];
```

### View Generated TCA

```bash
# Dump TCA for Content Block element
ddev typo3 configuration:show TCA.tt_content.types.myvendor_hero
```

### Check Database Columns

```bash
# List columns for tt_content
ddev mysql -e "DESCRIBE tt_content" | grep myvendor

# For Record Types
ddev mysql -e "DESCRIBE tx_myvendor_team_member"
```

---

## 4. Testing Content Blocks

### Functional Test Setup

```bash
# Install testing framework
ddev composer require --dev typo3/testing-framework

# Run Content Blocks tests
ddev exec vendor/bin/phpunit -c Build/phpunit-functional.xml
```

### Test Fixtures

```xml
<!-- Tests/Functional/Fixtures/pages.xml -->
<dataset>
    <pages>
        <uid>1</uid>
        <pid>0</pid>
        <title>Test Page</title>
    </pages>
    <tt_content>
        <uid>1</uid>
        <pid>1</pid>
        <CType>myvendor_hero</CType>
        <header>Test Hero</header>
        <myvendor_hero_subheadline>Test Subheadline</myvendor_hero_subheadline>
    </tt_content>
</dataset>
```

---

## 5. DDEV Commands for Content Blocks

### Custom DDEV Command

```bash
# .ddev/commands/web/cb-flush
#!/bin/bash
## Description: Flush caches and rebuild Content Blocks
## Usage: cb-flush
## Example: ddev cb-flush

vendor/bin/typo3 cache:flush
vendor/bin/typo3 extension:setup
echo "Content Blocks cache rebuilt!"
```

```bash
chmod +x .ddev/commands/web/cb-flush
ddev cb-flush
```

---

## 6. Common Issues

| Issue | Solution |
|-------|----------|
| Content Block not appearing | Run `ddev typo3 cache:flush` |
| Database columns missing | Run `ddev typo3 extension:setup` |
| CType not registered | Check config.yaml syntax |
| Template not found | Verify `templates/frontend.html` path |

---

## References

- [typo3-ddev SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [Content Blocks Documentation](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
