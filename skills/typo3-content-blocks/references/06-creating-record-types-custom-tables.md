# 6. Creating Record Types (Custom Tables)

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 6. Creating Record Types (Custom Tables)

Record Types create **custom database tables** for structured data like teams, products, events, etc.

### Extbase-Compatible Table Naming

**IMPORTANT:** For Extbase compatibility, use the `tx_extensionkey_domain_model_*` naming convention:

```yaml
# ✅ CORRECT - Extbase compatible table name
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fields:
  - identifier: name
    type: Text
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
```

```yaml
# ❌ WRONG - Short table names don't work with Extbase
name: myvendor/team-member
table: team_member  # Won't work with Extbase!
```

### Minimal Record Type

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fields:
  - identifier: name
    type: Text
```

### Full Record Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fallbackLabelFields:
  - email
languageAware: true
workspaceAware: true
sortable: true
softDelete: true
trackCreationDate: true
trackUpdateDate: true
internalDescription: true
restriction:
  disabled: true
  startTime: true
  endTime: true
  userGroup: true  # fe_group visibility fields when applicable
security:
  ignorePageTypeRestriction: true  # Allow on normal pages
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: phone
    type: Text
  - identifier: bio
    type: Textarea
    enableRichtext: true
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
  - identifier: social_links
    type: Collection
    labelField: platform
    fields:
      - identifier: platform
        type: Select
        renderType: selectSingle
        items:
          - label: LinkedIn
            value: linkedin
          - label: Twitter/X
            value: twitter
          - label: GitHub
            value: github
      - identifier: url
        type: Link
```

### Record Type options (reference)

Content Blocks exposes many **optional** root keys on record types — always confirm names against the current [Record Types YAML reference](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/YamlReference/ContentTypes/RecordTypes/Index.html). Commonly used flags include:

| Option | Role |
|--------|------|
| `editLocking` | Editor locking behaviour |
| `sortField` / `sortable` | Manual sorting (`sorting` column) |
| `rootLevelType` | Allow records at PID 0 |
| `readOnly` | Read-only in FormEngine |
| `adminOnly` | Visible to admins only |
| `hideAtCopy` / `appendLabelAtCopy` | Copy behaviour |
| `group` | Backend selector grouping |

### Multi-Type Records (Single Table Inheritance)

Create multiple types for one table:

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/person-employee/config.yaml
name: myvendor/person-employee
table: tx_mysitepackage_domain_model_person
typeField: person_type
typeName: employee
priority: 0  # Integer ordering; higher values load first (higher priority)
labelField: name
languageAware: false
workspaceAware: false
fields:
  - identifier: name
    type: Text
  - identifier: department
    type: Text
```

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/person-contractor/config.yaml
name: myvendor/person-contractor
table: tx_mysitepackage_domain_model_person
typeName: contractor
fields:
  - identifier: name
    type: Text
  - identifier: company
    type: Text
  - identifier: contract_end
    type: DateTime
```

### Record Types as Collection Children

Define a record that can be used in IRRE collections:

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/slide/config.yaml
name: myvendor/slide
table: tx_mysitepackage_domain_model_slide
labelField: title
fields:
  - identifier: title
    type: Text
  - identifier: image
    type: File
    maxitems: 1
  - identifier: link
    type: Link
```

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    foreign_table: tx_mysitepackage_domain_model_slide
    shareAcrossTables: true
    shareAcrossFields: true
    minitems: 1
```
