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
- If it is JSON/data, validate that the template and JavaScript parse the declared structure.

For each field used in `frontend.html`:

- It must exist in `config.yaml`, unless it is a TYPO3 system field like `uid`.
- Use `f:render.text(field: ...)` for Content Blocks transformed text fields where appropriate.
- Use `f:format.html` only for configured rich text.
- Format `Date`, `DateTime`, and `Time` fields explicitly with `f:format.date` before passing them to attributes or visual-editor text helpers. Do not render raw `DateTimeImmutable` objects through text ViewHelpers.
- Put unsupported `f:link.typolink` attributes such as `aria-label` into `additionalAttributes`; the ViewHelper does not accept them as direct arguments.
- Use package-qualified resource paths such as `EXT:desiderio/Resources/Public/...` for `f:uri.resource`; a bare relative path can be parsed as an empty package key.
- Guard string-only ViewHelpers such as `f:split` with defaults or conditions when the editor field can be empty, an array, or parsed JSON.
- Avoid undeclared Fluid arguments and unsupported ViewHelper arguments.

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
- date and time fields as values that TYPO3 stores and Fluid formats predictably,
- valid chart/data JSON matching the template parser.

## Styling

- Use shared Fluid atoms/molecules first.
- Use shadcn semantic utilities and tokens.
- Use bespoke CSS only for layout geometry, media aspect ratios, chart drawing, or unusual responsive behavior.
- Avoid hardcoded color palettes when a token exists.
