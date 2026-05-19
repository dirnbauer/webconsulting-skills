# Common Pitfalls & Hard-Won Lessons

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## Common Pitfalls & Hard-Won Lessons

These rules come from real debugging sessions. Violating them causes errors that are difficult to trace.

### 1. Multilevel Collections Need Explicit Tables

Current Content Blocks supports a Collection inside another Collection. Use it intentionally for structures like pricing plans with feature rows, table rows with cells, or navigation groups with links.

```yaml
# GOOD - each level has its own table and label field
fields:
  - identifier: rows
    type: Collection
    table: data_table_rows
    prefixField: true
    labelField: row_label
    fields:
      - identifier: row_label
        type: Textarea
      - identifier: cells
        type: Collection
        table: data_table_cells
        labelField: value
        fields:
          - identifier: value
            type: Textarea
```

Avoid anonymous or ambiguous multilevel structures. If a nested set is reused across multiple parent fields or parent tables, extract it to a Record Type and reference it with `foreign_table`, plus `shareAcrossTables` / `shareAcrossFields` where needed.

### 2. Dashes in typeName Values

When Content Blocks auto-generates `typeName` from the `name` field, it **strips all dashes**. If you set `typeName` explicitly, it must follow the same convention — no dashes.

```yaml
# WRONG — dash in typeName causes CType mismatch
name: myvendor/my-block
typeName: myvendor_my-block

# CORRECT — no dashes, matches auto-generation
name: myvendor/my-block
typeName: myvendor_myblock
```

The auto-generation logic (`UniqueIdentifierCreator::removeDashes`) converts `myvendor/my-block` to `myvendor_myblock`. If your explicit `typeName` uses dashes, it won't match existing database records created by auto-generation.

### 3. Reserved Field Identifier: `description`

The identifier `description` is a **top-level config.yaml key** (the content block's description shown in the backend). Using it as a field identifier creates a type conflict — the config key is a string, but a Textarea field resolves to a different type.

```yaml
# WRONG — conflicts with the config.yaml root key
description: My content block description
fields:
  - identifier: description      # <-- conflicts with root "description"
    type: Textarea

# CORRECT — use a distinct identifier
description: My content block description
fields:
  - identifier: description_text  # <-- no conflict
    type: Textarea
```

### 4. Template Field References Must Match config.yaml Identifiers

Every `{data.fieldname}` in `frontend.html` must exactly match an `identifier` in `config.yaml`. There is no runtime error — the field simply renders empty, making this a silent bug.

```yaml
# config.yaml defines:
- identifier: features_list
  type: Textarea
```

```html
<!-- WRONG — silent failure, renders empty -->
{data.features -> f:split(separator: '\n')}

<!-- CORRECT — matches the identifier -->
{data.features_list -> f:split(separator: '\n')}
```

When renaming field identifiers (e.g., to resolve conflicts), always search templates for the old name.

### 5. Collection Identifier Naming — Avoid Table Name Collisions

Never name a Collection field with an identifier that matches an existing TYPO3 database table (e.g., `pages`, `tt_content`, `sys_file`). Content Blocks generates table names from Collection identifiers, and a collision with a core table causes unpredictable errors.

For `tt_content` Content Blocks with `prefixFields: false`, do not reuse an unprefixed top-level Collection identifier across multiple content elements. Either give each Collection a unique identifier or set `prefixField: true` on that Collection so Content Blocks generates a separate TCA column for each content element.

```yaml
# DANGEROUS — "pages" collides with TYPO3 core table
- identifier: pages
  type: Collection

# SAFE — use a descriptive, unique identifier
- identifier: page_items
  type: Collection
```

---
