# 10. Field Prefixing

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 10. Field Prefixing

Content Blocks automatically prefixes field identifiers to avoid collisions.

### Prefixing Types

```yaml
# Full prefix (default): myvendor_myblock_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: full

# Vendor prefix only: myvendor_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: vendor

# Custom vendor prefix: tx_custom_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: vendor
vendorPrefix: tx_custom

# No prefix (use with caution!)
name: myvendor/my-block
prefixFields: false
```

### Disable Prefixing per Field

```yaml
fields:
  - identifier: my_custom_field
    type: Text
    prefixField: false  # This field won't be prefixed
```

### Prefix Collection Fields When Root Fields Are Shared

If a `tt_content` Content Block uses `prefixFields: false`, still enable prefixing on every top-level `Collection` field that could share an identifier with another Content Block, such as `items`, `links`, `plans`, or `members`.

```yaml
name: vendor/accordion
typeName: vendor_accordion
prefixFields: false
fields:
  - identifier: items
    type: Collection
    table: accordion_items
    prefixField: true
    fields:
      - identifier: title
        type: Textarea
      - identifier: content
        type: Textarea
        enableRichtext: true
```

Do not work around reused Collection identifiers by patching `columnsOverrides` or rewriting `foreign_table` per CType. In TYPO3 TCA there is one root column per field identifier; without `prefixField: true`, the last merged Collection configuration can win and point multiple content elements at the wrong child table.

### Reusing Collection Tables to Reduce Schema Noise

Default to one generated child table per Collection. The many-table setup is safer and clearer for generated Content Blocks because each content element owns its schema, labels, migrations, fixtures, and seed logic.

Reuse a Collection table only as an explicit modeling decision, not automatically by shared identifiers like `items`, `links`, `plans`, or `members`.

Use table reuse when all of these are true:

- The child schema is intentionally identical, for example repeated `label` + `link`, `text`, `label` + `value`, or logo rows.
- The shared table name describes a real reusable concept, not just a coincidental field identifier.
- Every parent Collection that points to the table is configured consistently.
- If the same parent record can have multiple fields using the same child table, use `foreign_table` with `shareAcrossFields: true` or another explicit match field so rows cannot leak between fields.
- Import, seed, cleanup, and migration code can resolve the shared table and match fields correctly.

Avoid table reuse when:

- The field schemas differ or may evolve independently.
- The only reason is to reduce a visually large table list.
- Two fields on the same content element would point to the same child table without `shareAcrossFields`.
- Editors need different labels, validation, record labels, or preview assumptions per content element.
- You would need nullable catch-all columns to force unrelated structures into one table.

Expected benefit: fewer tables and less schema noise. Do not expect a major physical database-size reduction unless table overhead is the actual bottleneck in the target database. Reuse tables for small, stable primitives; keep bespoke content structures isolated.
