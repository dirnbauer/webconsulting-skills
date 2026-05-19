# 9. Field Types Reference

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 9. Field Types Reference

### Simple Fields

| Type | Description | Example |
|------|-------------|---------|
| `Text` | Single line text | `type: Text` |
| `Textarea` | Multi-line text | `type: Textarea` |
| `Email` | Email address | `type: Email` |
| `Link` | Link/URL | `type: Link` |
| `Number` | Integer/Float | `type: Number` (+ `format: integer` or `format: decimal` as needed; legacy YAML sometimes used a non-existent `Integer` type — use `Number`) |
| `DateTime` | Date and/or time | `type: DateTime` |
| `Color` | Color picker | `type: Color` |
| `Checkbox` | Boolean checkbox | `type: Checkbox` |
| `Radio` | Radio buttons | `type: Radio` |
| `Slug` | URL slug | `type: Slug` |
| `Password` | Password field | `type: Password` |
| `Basic` | Shared “basic” field helper | `type: Basic` |
| `Country` | Country selection (aligns with TCA `country` where supported) | `type: Country` |
| `Pass` | Virtual field, not visible in the backend; used for storing data handled by extension logic | `type: Pass` |
| `SelectNumber` | Select with numeric values | `type: SelectNumber` |
| `Uuid` | UUID string | `type: Uuid` |

### Relational Fields

| Type | Description | Example |
|------|-------------|---------|
| `File` | File references (FAL) | `type: File` |
| `Relation` | Record relations | `type: Relation` |
| `Select` | Dropdown selection | `type: Select` |
| `Category` | System categories | `type: Category` |
| `Collection` | Inline records (IRRE) | `type: Collection` |
| `Folder` | Folder reference | `type: Folder` |
| `Language` | Language selector | `type: Language` |

### Structural Fields

| Type | Description | Example |
|------|-------------|---------|
| `Tab` | Tab separator | `type: Tab` |
| `Palette` | Group fields | `type: Palette` |
| `Linebreak` | Line break in palette | `type: Linebreak` |
| `FlexForm` | FlexForm container | `type: FlexForm` |
| `Json` | JSON field | `type: Json` |

### Common Field Options

```yaml
fields:
  - identifier: my_field
    type: Text
    label: My Field Label           # Static label (or use labels.xlf)
    description: Help text          # Field description
    required: true                  # Make field required
    default: "Default value"        # Default value
    placeholder: "Enter text..."    # Placeholder text
    prefixField: false              # Disable prefixing for this field
    useExistingField: true          # Reuse existing TCA field
    displayCond: 'FIELD:other:=:1'  # Conditional display
    onChange: reload                # Reload form on change
```

### File Field Example

> **TCA-only options:** Keys like `appearance` / `behaviour` belong in generated TCA, not always in Content Blocks YAML. If the schema rejects them, add a **TCA override** for that field after generation (see Content Blocks docs on extending TCA).

```yaml
fields:
  - identifier: gallery_images
    type: File
    allowed: common-image-types
    minitems: 1
    maxitems: 10
```

### Select Field Example

```yaml
fields:
  - identifier: layout
    type: Select
    renderType: selectSingle
    default: default
    items:
      - label: Default Layout
        value: default
      - label: Wide Layout
        value: wide
      - label: Compact Layout
        value: compact
```

### Collection Field Example (Inline IRRE)

Collections can contain normal child fields and, on current Content Blocks, another Collection field for multilevel IRRE structures. Keep each level explicit with its own `table`, `labelField`, and item limits.

```yaml
fields:
  - identifier: accordion_items
    type: Collection
    prefixField: true
    labelField: title
    minitems: 1
    maxitems: 20
    appearance:
      collapseAll: true
      levelLinksPosition: both
    fields:
      - identifier: title
        type: Text
        required: true
      - identifier: content
        type: Textarea
        enableRichtext: true
      - identifier: is_open
        type: Checkbox
        label: Initially Open
```

### Multilevel Collection Example

Use a multilevel Collection when editors need repeatable groups where each group has its own repeatable children. This Desiderio pattern models pricing plans, and each plan owns a nested list of features:

```yaml
name: desiderio/pricing
typeName: desiderio_pricing
prefixFields: false
fields:
  - identifier: plans
    type: Collection
    table: pricing_plans
    prefixField: true
    label: Pricing Plans
    labelField: name
    minItems: 1
    maxItems: 4
    fields:
      - identifier: name
        type: Textarea
        rows: 1
        required: true
      - identifier: price
        type: Textarea
        rows: 1
        required: true
      - identifier: features
        type: Collection
        table: pricing_plan_features
        label: Features
        labelField: text
        minItems: 1
        maxItems: 8
        fields:
          - identifier: text
            type: Textarea
            rows: 1
```

Guidelines for multilevel Collections:

- Use `prefixField: true` on the top-level Collection when the root Content Block has `prefixFields: false` or when identifiers like `items`, `plans`, or `rows` are reused across `tt_content` types.
- Give every Collection level a stable `table` name. In the example, `plans` writes to `pricing_plans`, and nested `features` writes to `pricing_plan_features`.
- Keep nested levels shallow unless the editor workflow really needs them. Two levels is usually understandable; deeper structures become hard to seed, translate, preview, and migrate.
- In import/seed code, recurse through nested `Collection` definitions and write child rows using the current parent row uid, not the original `tt_content` uid.
- If you use `foreign_table`, do not also define local `fields` for that Collection; define the reusable structure as a Record Type and reference it instead.
