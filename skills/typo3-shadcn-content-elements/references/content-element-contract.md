# Content Element Contract

Use this checklist for every `ContentBlocks/ContentElements/<element>`.

## Required Files

- `config.yaml`
- `templates/frontend.html`
- `templates/backend-preview.fluid.html`
- `language/labels.xlf`
- `assets/icon.svg`
- `assets/frontend.css` only when the shared Fluid component layer cannot express the layout
- `assets/frontend.js` only when interaction or visualization requires it

## Schema And Template Checks

`config.yaml:title` is the editor-facing content element name. Use clear product names
instead of slug-shaped labels: `Text & Media`, `Image Call to Action`, `Logo Cloud Hero`,
`Table of Contents Navigation`.

For each field in `config.yaml`:

- If it is editor-facing, render it in `frontend.html` or document why it is backend-only.
- If it is `Select`, `Checkbox`, variant, density, or layout related, set a default.
- If it is `Collection`, render meaningful child fields and handle empty states.
- If it is `File`, render with TYPO3 file APIs and provide alt/caption/copyright strategy.
- If it stores an editor-managed URL, use `type: Link`; keep the visible label in a separate text field such as `cta_text`, `link_1_label`, or `child_1_label`.
- If it is JSON/data, validate that the template and JavaScript parse the declared structure.

For each field used in `frontend.html`:

- It must exist in `config.yaml`, unless it is a TYPO3 system field like `uid`.
- Use `f:render.text(field: ...)` for Content Blocks transformed text fields where appropriate.
- Use `f:format.html` only for configured rich text.
- Format `Date`, `DateTime`, and `Time` fields explicitly with `f:format.date` before passing them to attributes or visual-editor text helpers. Do not render raw `DateTimeImmutable` objects through text ViewHelpers.
- Put unsupported `f:link.typolink` attributes such as `aria-label` into `additionalAttributes`; the ViewHelper does not accept them as direct arguments.
- Render `Link` fields with `f:link.typolink parameter="{field}"` after checking `{field.url}`. The field resolves to a TYPO3 typolink object with URL, target, class, title, and additional params.
- Do not parse link textareas with `f:split(separator: '|')`. A pipe-delimited string such as `Docs|https://example.com/docs` hides URL semantics from TYPO3, weakens editor UX, and breaks previews/seed conversion.
- Use package-qualified resource paths such as `EXT:desiderio/Resources/Public/...` for `f:uri.resource`; a bare relative path can be parsed as an empty package key.
- Guard string-only ViewHelpers such as `f:split` with defaults or conditions when the editor field can be empty, an array, or parsed JSON.
- Avoid undeclared Fluid arguments and unsupported ViewHelper arguments.

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
- Use `additionalAttributes` when a link truly needs an `aria-label`.
- Use image/File `alternative` fields for image alt text.
- Seed structured links as objects, for example `{"label": "Docs", "link": "https://example.com/docs"}`.

Do not:

- Do not use textarea rows like `Docs|https://example.com/docs`.
- Do not invent `alt` fields for plain links. `alt` belongs to images, not anchors.
- Do not pass `aria-label` directly to `f:link.typolink`; TYPO3 rejects undeclared ViewHelper arguments.
- Do not render raw URL strings as visible content unless the URL itself is the intended label.

## Labels

- Keep global generic labels in `Resources/Private/Language/labels.xlf`.
- Add element-specific labels in the element `language/labels.xlf` when the global label is too vague.
- Collection item labels should describe editor intent, not implementation names.

## Seed Data

Seed scripts must fill:

- all top-level fields,
- all repeatable Collection fields,
- image/file fields with usable demo images,
- alt text and copyright/source text when fields exist,
- valid links and CTA labels,
- link fields as TYPO3 links, with labels in separate fields and no `Label|URL` syntax,
- date and time fields as values that TYPO3 stores and Fluid formats predictably,
- valid chart/data JSON matching the template parser.

## Styling

- Use shared Fluid atoms/molecules first.
- Use shadcn semantic utilities and tokens.
- Use bespoke CSS only for layout geometry, media aspect ratios, chart drawing, or unusual responsive behavior.
- Avoid hardcoded color palettes when a token exists.
- Do not add raw hex, RGB(A), HSL(A), or OKLCH values to live content-element templates/assets.
- Keep raw shadcn preset values in the theme token file; consume them through `var(--*)` tokens or Tailwind/shadcn utilities.
- Verify both light mode (`:root`) and dark mode (`.dark`) behavior when adding surfaces, borders, overlays, shadows, or chart colors.
