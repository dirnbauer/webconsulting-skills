# Content Element Contract

Use this checklist for every `ContentBlocks/ContentElements/<element>`.

## Required Files

- `config.yaml`
- `templates/frontend.fluid.html` (Content Blocks 2.x default since 2.0.4; plain `frontend.html` is the legacy 1.x name)
- `templates/backend-preview.fluid.html`
- `language/labels.xlf`
- `assets/icon.svg`
- `assets/frontend.css` only when the shared Fluid component layer cannot express the layout, unless the repository has an explicit per-element asset-file invariant; then keep an empty/comment-only marker file and do not include it from the template until rules are actually needed
- `assets/frontend.js` only when interaction or visualization is genuinely element-local; prefer a shared include file for whole families such as charts, carousels, tabs, counters, and dashboards

## Schema And Template Checks

`config.yaml:title` is the editor-facing content element name. Use clear product names
instead of slug-shaped labels: `Text & Media`, `Image Call to Action`, `Logo Cloud Hero`,
`Table of Contents Navigation`.

For each field in `config.yaml`:

- If it is editor-facing, render it in `frontend.fluid.html` or document why it is backend-only.
- If it is `Select`, `Checkbox`, variant, density, or layout related, set a default.
- If it is named `variant` or labeled as `Style`, prove that every value changes output through an existing shared shadcn component feature or a real template branch. Good examples are Button/Badge/Alert variants and TabsList `data-variant="default|line"`. Bad examples are values that only produce unused classes such as `accordion--bordered`, `table--striped`, or `tabs--pills`.
- Remove unsupported style fields instead of adding one-off CSS. A content element should not invent custom visual variants merely because a `variant` field exists.
- If it is `Collection`, render meaningful child fields and handle empty states.
- If it is `Collection`, give it an explicit `table:` key. Without one, Content Blocks derives the table name from the field `identifier` only, which silently shares a single physical table across every content element that uses the same identifier (`posts`, `rows`, `column_items`, `cells`, `items`, `links`...). The shared table accumulates the union of all those blocks' fields, schema migrations get confused (parent UIDs end up as the wrong type, see "Collection Table Naming" below), and a future rename loses or scrambles content. Pick a name like `<contentblock-slug>_<identifier>` (for example `blog_teasers_posts`, `feature_matrix_rows`, `footer_mega_column_items`).
- If it is a repeatable list inside another repeatable item, use a nested `Collection` when the installed Content Blocks version supports it. Do not model editor-managed feature lists as newline-separated textareas just because they are second-level data.
- Do not model repeatable editor content as delimiter protocols. Fields such as `features_list`, `specs_text`, `row_data`, comma-separated `tier_values`, or newline/pipe encoded people/pages are legacy migration inputs, not the target schema.
- If it is `File`, render with TYPO3 file APIs and provide alt/caption/copyright strategy.
- If it stores an editor-managed URL, use `type: Link`; keep the visible label in a separate text field such as `cta_text`, `link_1_label`, or `child_1_label`.
- If it is JSON/data, validate that the template emits a stable `data-*` attribute and the shared JavaScript parses the declared structure.

For each field used in `frontend.fluid.html`:

- It must exist in `config.yaml`, unless it is a TYPO3 system field like `uid`.
- Use `f:render.text(field: ...)` for Content Blocks transformed text fields where appropriate.
- Use `f:format.html` only for configured rich text.
- Format `Date`, `DateTime`, and `Time` fields explicitly with `f:format.date` before passing them to attributes or visual-editor text helpers. Do not render raw `DateTimeImmutable` objects through text ViewHelpers.
- Since Fluid 2.12 (TYPO3 v12+), tag-based ViewHelpers such as `f:link.typolink` accept arbitrary unregistered attributes (for example `aria-label` or `aria="{...}"`) directly; `additionalAttributes` still works but is not required. Pick one style per project and use it consistently.
- Render `Link` fields with `f:link.typolink parameter="{field}"` after checking `{field.url}`. The field resolves to a TYPO3 typolink object with URL, target, class, title, and additional params.
- Do not parse link textareas with `f:split(separator: '|')`. A pipe-delimited string such as `Docs|https://example.com/docs` hides URL semantics from TYPO3, weakens editor UX, and breaks previews/seed conversion.
- Do not parse structural lists with `f:split()` in frontend templates. If a template needs rows, cells, features, people, pages, specs, or tier values, the data should arrive as a Collection or JSON/data field with an explicit parser.
- Use package-qualified resource paths such as `EXT:desiderio/Resources/Public/...` for `f:uri.resource`; a bare relative path can be parsed as an empty package key.
- Guard string-only ViewHelpers such as `f:split` with defaults or conditions when the editor field can be empty, an array, or parsed JSON.
- Avoid undeclared Fluid arguments and unsupported ViewHelper arguments.

## Client-Side Behavior Pattern

Use this pattern for charts, dashboards, carousels, counters, and other browser behavior:

- Register shared JavaScript through TypoScript `page.includeJSFooterlibs`, `f:asset.script`,
  or TYPO3's AssetCollector.
- Keep Fluid templates declarative: semantic markup, shadcn classes, `data-ce`,
  `data-chart-data`, `data-chart-json`, `data-state`, and ARIA attributes.
- Do not render inline `<script>` blocks inside `templates/frontend.fluid.html`.
- Make initializers idempotent by marking enhanced nodes, for example
  `data-chart-rendered="true"`.
- Read colors from CSS variables such as `--chart-1`, `--chart-2`, `--primary`,
  `--muted-foreground`, or `currentColor`; do not put raw color literals in JS.
- If the user asks for Astro include files, use an Astro shadcn scratch app to model the
  component behavior, then ship compiled/shared include assets in TYPO3.

Run this scan after moving scripts:

```bash
rg -n "<script>|JSON\\.parse" ContentBlocks/ContentElements/*/templates/frontend.fluid.html
```

## Link Field Pattern

Use this pattern whenever editors need a link:

```yaml
- identifier: cta_text
  type: Textarea
  rows: 1
  label: Button Text
- identifier: cta_link
  type: Link
  label: Button Link
```

```html
<f:if condition="{data.cta_text} && {data.cta_link.url}">
    <f:link.typolink parameter="{data.cta_link}" class="...">
        {data -> f:render.text(field: 'cta_text')}
    </f:link.typolink>
</f:if>
```

For repeatable link groups, prefer a flat Collection with one row per link when the model allows it. If the element already uses a Collection for groups and Content Blocks cannot nest another Collection inside it, use fixed slots:

```yaml
- identifier: link_1_label
  type: Textarea
  rows: 1
  label: Link 1 Label
- identifier: link_1
  type: Link
  label: Link 1
```

Do:

- Store URL targets in `type: Link` fields so TYPO3 can manage page, file, record, external, target, class, and title data.
- Store visible link copy separately. Visible text is the primary accessible name.
- Add `aria-label` only when a link truly needs one; pass it directly as an attribute (Fluid 2.12+, TYPO3 v12+) or via `additionalAttributes` — both work.
- Use image/File `alternative` fields for image alt text.
- Seed structured links as objects, for example `{"label": "Docs", "link": "https://example.com/docs"}`.

Do not:

- Do not use textarea rows like `Docs|https://example.com/docs`.
- Do not invent `alt` fields for plain links. `alt` belongs to images, not anchors.
- Do not add redundant `aria-label` values that merely repeat the visible link text; the visible text is already the accessible name.
- Do not render raw URL strings as visible content unless the URL itself is the intended label.

## Nested Collection Pattern

Content Blocks can model second-level repeatables with nested Collections. Use this for structures such as pricing plans with repeatable features:

```yaml
- identifier: plans
  type: Collection
  labelField: name
  fields:
    - identifier: name
      type: Textarea
      rows: 1
      label: Plan Name
    - identifier: features
      type: Collection
      table: pricing_plan_features
      labelField: text
      fields:
        - identifier: text
          type: Textarea
          rows: 1
          label: Feature
```

```html
<f:for each="{data.plans}" as="plan">
    <f:for each="{plan.features}" as="feature">
        {feature -> f:render.text(field: 'text')}
    </f:for>
</f:for>
```

Seed fixtures should stay structured:

```json
{
  "plans": [
    {
      "name": "Business",
      "features": ["Unlimited users", "Priority support"]
    }
  ]
}
```

If a project is pinned to a Content Blocks release that cannot nest Collections, use an explicit fallback such as fixed `feature_1`...`feature_6` fields and document that limitation in the element.

## Collection Table Naming

**Every `type: Collection` field must declare an explicit `table:`.** This is non-negotiable. The default behavior of deriving the table name from the field `identifier` is unsafe for three reasons.

**Reserved SQL words.** MySQL 8.0+ reserves `ROWS` (used in window-function `ROWS BETWEEN`); MariaDB matches. Doctrine quotes identifiers at runtime, so the table works in TYPO3, but `mysqldump`, ad-hoc CLI queries, schema-diff tools, IDE introspection, and `mysqlcheck` all stumble on unquoted `rows`. Other risky bare names: `groups`, `order`, `range`, `system`. Prefix every Collection table to sidestep the reserved-word list permanently.

**Cross-element collisions.** Several content elements naturally pick the same identifier (`posts`, `rows`, `column_items`, `cells`, `items`, `links`, `features`, `tabs`). Without `table:`, Content Blocks merges them into one shared physical table whose schema is the union of every consuming element's fields. This causes:

- Bloated tables with link/file/select columns that only one of the sharing elements actually uses.
- Schema-migration deadlocks when one of the elements is renamed or removed: TYPO3 wants to drop columns that another element still needs.
- Type drift on `foreign_table_parent_uid`: because every old Content Blocks version generated different defaults for the parent reference, a shared `column_items` table can keep an old `varchar(255) DEFAULT '' NOT NULL` definition while TYPO3 wants `int unsigned DEFAULT 0 NOT NULL`. The migration then fails with `Truncated incorrect INTEGER value: ''` because existing rows hold empty strings.
- Editor data loss on rename: splitting one shared table back into per-element tables requires a parent-aware data migration, and orphaned rows are common.

**TYPO3 convention.** Extension-owned tables should be prefixed so dump files, schema diffs, and other extensions can attribute ownership. Bare names like `posts` collide with every other extension that ships a blog.

### Don't

- Do not declare `type: Collection` without `table:`. The bare-identifier fallback is a footgun, not a feature.
- Do not use reserved SQL keywords as table names: `rows`, `groups`, `range`, `order`, `system`, `values`, `user`, `cross`, `dense_rank`, `window`. Doctrine quotes at runtime, but `mysqldump`, `mysqlcheck`, schema-diff tooling, and IDE introspection break.
- Do not use generic single-word table names (`posts`, `items`, `cells`, `tabs`, `members`, `slides`, `stats`, `links`, `features`, `tiers`, `partners`, `clients`, `reviews`, `routes`, `metrics`, `specs`, `jobs`, `awards`, `events`, `mentions`, `counters`...). They collide with other extensions on the same TYPO3 instance and across the Content Blocks ecosystem.
- Do not silently rename a Collection's `table:` after editor content exists. Renaming triggers a drop-and-create in TYPO3's schema migration unless you do a parent-aware data move first.
- Do not paper over a `Truncated incorrect INTEGER value: ''` error by lowering MySQL's `sql_mode`. Fix the data (`UPDATE ... SET foreign_table_parent_uid = 0 WHERE foreign_table_parent_uid = ''`) and the column type properly.
- Do not assume "the table works because TYPO3 boots fine" means safe — the failure surface is dump/restore, schema migration, and renames, not steady-state runtime.

### Do

- Always set `table:` on every `type: Collection` field, top-level and nested.
- Name tables `<contentblock-slug-as-snake_case>_<collection-identifier>`. Examples: `blog_teasers_posts`, `feature_matrix_rows`, `footer_mega_column_items`, `pricing_plan_features`, `data_table_cells`, `team_department_members`.
- For nested Collections, prefix with the parent collection so the relationship is readable (`pricing_plan_features` inside a `plans` Collection that has a `features` child Collection).
- When porting or auditing an extension, fix every Collection in one pass — partial fixes leave broken schema transitions.
- Run the audit grep below before declaring a Collection sweep complete.
- Match an existing extension's prefix style if one already dominates (`<ext>_<slug>_<identifier>` for stricter projects, plain `<slug>_<identifier>` for desiderio-style).

### Naming Pattern

Use `<contentblock-slug-as-snake_case>_<collection-identifier>`:

```yaml
# ContentBlocks/ContentElements/blog-teasers/config.yaml
- identifier: posts
  type: Collection
  table: blog_teasers_posts

# ContentBlocks/ContentElements/table-content/config.yaml
- identifier: column_items
  type: Collection
  table: table_content_column_items
- identifier: rows
  type: Collection
  table: table_content_rows

# ContentBlocks/ContentElements/feature-matrix/config.yaml
- identifier: rows
  type: Collection
  table: feature_matrix_rows

# ContentBlocks/ContentElements/footer-mega/config.yaml
- identifier: column_items
  type: Collection
  table: footer_mega_column_items
```

For nested Collections, follow the same pattern with the parent collection in the name (`pricing_plan_features`, `data_table_cells`).

### Audit Command

```bash
# Find Collection fields that lack an explicit table: key.
rg -nP '^\s*type: Collection\s*$' --no-heading -A1 ContentBlocks/ContentElements \
  | rg -B1 -v 'table:'

# List bare table names that collide with MySQL/MariaDB reserved words.
rg -n '^\s+table:\s+(rows|groups|range|order|system|values|user|cross|dense_rank)\s*$' \
  ContentBlocks/ContentElements
```

### Migration From An Existing Shared Table

If `column_items`, `rows`, `posts`, or similar already exist in production:

1. Add `table:` to every Content Block that points at the shared name.
2. Inspect the shared table's `foreign_table_parent_uid` and `pid` to map each row to its owning content element (usually by joining against `tt_content.CType` on the parent UID).
3. Move rows into the new per-element tables before running TYPO3's schema migration; otherwise the schema migration drops the shared table and editor content is lost.
4. If `foreign_table_parent_uid` is `varchar(255)` with empty-string rows, run `UPDATE <table> SET foreign_table_parent_uid = 0 WHERE foreign_table_parent_uid = ''` before the ALTER, or strict-mode MySQL will refuse the type change with `Truncated incorrect INTEGER value: ''`.

## Legacy Workaround Cleanup

When auditing an existing set of content elements, replace these workaround shapes with explicit schema:

- `features_list` textareas -> `features` Collection with one row per feature.
- `specs_text` textareas -> `specs` Collection with one row per spec.
- `row_data` pipe strings -> row Collection with nested `cells` Collection.
- comma-delimited `tier_values` -> nested `tier_values` Collection.
- newline/pipe encoded `members`, `people`, or `pages` -> nested Collections with named child fields.
- `Label|URL` values -> TYPO3 `Link` fields plus separate label fields.

Frontend templates should render the structured fields directly. Seed scripts may keep old aliases only as one-way compatibility converters, and those converters must normalize legacy values into current fields before inserting records. Do not keep legacy examples in tests, fixture files, docs, or generated templates.

## Desiderio Fixture Source

For EXT:desiderio, demo content belongs beside the element:

```text
ContentBlocks/ContentElements/<element>/fixture.json
```

Do not create or restore a monolithic `shadcn2fluid_*` fixture map. Those keys belong to the predecessor package and should not drive current Content Blocks seeding. The seed script should load fixtures by the current `desiderio_*` CType and then complete any missing fields from the element schema.

Allowed `shadcn2fluid` references are limited to package conflict metadata, historical migration/spec notes, and tests or documentation that explicitly prevent runtime reuse. Runtime loaders, seed fixtures, Content Blocks, Fluid templates, and generated examples must use current `desiderio_*` names and per-element fixtures.

## Labels

- Use the `typo3-translations` skill for XLIFF version selection, English/German
  localization, ICU MessageFormat strings, target state handling, `LLL:`
  references, and XML validation.
- Keep global generic labels in `Resources/Private/Language/labels.xlf`.
- Add element-specific labels in the element `language/labels.xlf` when the global label is too vague.
- Collection item labels should describe editor intent, not implementation names.
- Content element titles should be unique editor-facing names. Descriptions should explain the element's purpose and important editor controls; avoid repeated boilerplate such as "A shadcn/ui styled TYPO3 content element...".
- Custom wizard group names must be registered through TCA with localized `LLL:` labels. Keep machine group ids stable, but make visible names descriptive, for example `Hero & Landing Intros` instead of `hero`.

## Seed Data

Seed scripts must fill:

- all top-level fields,
- all repeatable Collection fields,
- nested Collection fields, seeded as nested arrays and inserted after parent rows,
- image/file fields with usable demo images,
- alt text and copyright/source text when fields exist,
- valid links and CTA labels,
- link fields as TYPO3 links, with labels in separate fields and no `Label|URL` syntax,
- date and time fields as values that TYPO3 stores and Fluid formats predictably,
- valid chart/data JSON matching the template parser.
- Select values that still exist in the current `config.yaml`; seed commands should normalize or drop legacy style values before inserting rows.

After seeding, run targeted checks for known regressions:

```bash
rg -n "f:split\\(|\\|https?://|one per line|features_list|row_data|specs_text|shadcn2fluid" \
  ContentBlocks Classes Resources README.md Tests -S
```

Review any matches manually. Compatibility aliases inside seed conversion code can be acceptable; active templates, fixtures, schema, and examples should be clean.

## Styling

- Use shared Fluid atoms/molecules first.
- Use shadcn semantic utilities and tokens.
- Use bespoke CSS only for layout geometry, media aspect ratios, chart drawing, or unusual responsive behavior.
- Avoid hardcoded color palettes when a token exists.
- Do not add raw hex, RGB(A), HSL(A), or OKLCH values to live content-element templates/assets.
- Keep raw shadcn preset values in the theme token file; consume them through `var(--*)` tokens or Tailwind/shadcn utilities.
- Verify both light mode (`:root`) and dark mode (`.dark`) behavior when adding surfaces, borders, overlays, shadows, or chart colors.
