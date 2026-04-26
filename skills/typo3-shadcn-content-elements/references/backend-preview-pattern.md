# Backend Preview Pattern

Content Blocks custom Content Elements should provide their own backend preview. TYPO3's default preview renderer is optimized for Core fields such as `header`, `subheader`, and `bodytext`, so custom schemas can produce broken or empty layout module previews.

## Required Shape

Create:

`ContentBlocks/ContentElements/<element>/templates/backend-preview.fluid.html`

Use:

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:cb="http://typo3.org/ns/TYPO3/CMS/ContentBlocks/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Preview"/>

<f:section name="Header">
    <cb:link.editRecord uid="{data.uid}" table="{data.mainType}">Element title</cb:link.editRecord>
</f:section>

<f:section name="Content">
    <f:asset.css identifier="d-preview-shared" href="EXT:desiderio/Resources/Public/Css/content-preview.css"/>
    <div class="d-preview-card">
        <!-- concise editor-facing summary -->
    </div>
</f:section>

</html>
```

## What To Show

Show the highest-signal content:

- headline/title,
- eyebrow/category/status,
- short description/body excerpt,
- CTA text/link,
- repeatable item count plus first few labels,
- image thumbnails,
- chart/data summaries,
- table dimensions,
- formatted date and time values instead of raw objects,
- warnings when required data is empty.

## Visual Style

Match TYPO3 backend expectations:

- compact bordered card,
- internal padding,
- readable in dark and light backend schemes,
- small thumbnails with rounded borders,
- bullet lists for repeatables,
- no heavy frontend hero layout.

## Avoid

- Copying the full frontend template into the backend preview.
- Calling fields that do not exist on that element, including `data.header` on headerless blocks.
- Relying on `header` for elements that do not declare it.
- Loading frontend-only JavaScript just to show a preview.
