---
name: typo3-conformance-content-blocks
description: Content Blocks extension structure conformance. Directory layout, naming conventions, and best practices.
version: 1.0.0
typo3_compatibility: "14.x"
related_skills:
  - typo3-conformance
  - typo3-content-blocks
triggers:
  - content blocks conformance
  - content blocks structure
  - content blocks standards
---

# Content Blocks Conformance

> **Compatibility:** TYPO3 v14.x
> 
> **Related Skills:**
> - [typo3-conformance](./SKILL.md) - Main conformance guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. Directory Structure Standards

### Recommended Layout

```
packages/my_extension/
├── ContentBlocks/
│   ├── ContentElements/
│   │   ├── hero/
│   │   │   ├── config.yaml
│   │   │   ├── labels.xlf
│   │   │   └── templates/
│   │   │       ├── frontend.fluid.html
│   │   │       └── backend-preview.fluid.html
│   │   └── accordion/
│   │       └── ...
│   └── RecordTypes/
│       └── team-member/
│           ├── config.yaml
│           └── labels.xlf
├── Classes/
├── Configuration/
├── Resources/
├── composer.json
└── ext_emconf.php
```

---

## 2. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Vendor | lowercase | `myvendor` |
| Element name | kebab-case | `hero-banner` |
| Folder name | kebab-case | `ContentElements/hero-banner/` |
| config.yaml name | `vendor/element` | `myvendor/hero-banner` |

---

## 3. config.yaml Standards

### Required Fields

```yaml
name: myvendor/hero  # Required: vendor/name format
fields:              # Required: at least one field
  - identifier: header
    useExistingField: true
```

### Recommended Fields

```yaml
name: myvendor/hero
description: Hero banner with image and CTA  # Recommended
group: content                                 # Recommended
basics:                                        # Recommended
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  # ...
```

---

## 4. Template Standards

### frontend.fluid.html Requirements

```html
<!-- Must be valid Fluid template -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:cb="http://typo3.org/ns/TYPO3/CMS/ContentBlocks/ViewHelpers"
      data-namespace-typo3-fluid="true">

<!-- Access data via {data.fieldname} -->
<section class="hero">
    <h1>{data.header}</h1>
    <p>{data.subheadline}</p>
</section>
</html>
```

---

## 5. Conformance Checklist

### Structure
- [ ] `ContentBlocks/` folder in extension root
- [ ] Proper subfolder structure (`ContentElements/`, `RecordTypes/`)
- [ ] kebab-case folder names

### config.yaml
- [ ] Valid `name` in vendor/element format
- [ ] All identifiers are camelCase or snake_case
- [ ] `useExistingField: true` for standard fields (header, bodytext)
- [ ] Proper field types used

### Templates
- [ ] `frontend.fluid.html` exists and is valid Fluid
- [ ] `backend-preview.fluid.html` for complex elements
- [ ] No hardcoded strings (use labels.xlf)

### Translations
- [ ] `labels.xlf` for all custom labels
- [ ] Proper XLIFF structure

---

## 6. Quality Tools

### Check Config Syntax

```bash
# Validate YAML syntax
ddev exec php -r "yaml_parse_file('ContentBlocks/ContentElements/hero/config.yaml');"

# Flush cache and check for errors
ddev typo3 cache:flush
```

---

## References

- [typo3-conformance SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [Content Blocks Documentation](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
