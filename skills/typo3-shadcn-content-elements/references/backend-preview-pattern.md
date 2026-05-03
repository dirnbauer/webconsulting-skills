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

<f:section name="Header"></f:section>

<f:section name="Content">
    <f:asset.css identifier="desiderio-content-preview" href="EXT:desiderio/Resources/Public/Css/content-preview.css"/>
    <div class="d-ce-preview" data-slot="card">
        <div class="d-ce-preview__meta">
            <span class="d-ce-preview__type" data-slot="badge">Element title</span>
            <f:if condition="{settings._content_block_name}"><span class="d-ce-preview__ctype">{settings._content_block_name}</span></f:if>
            <span class="d-ce-preview__ctype"><f:translate key="LLL:EXT:desiderio/Resources/Private/Language/labels.xlf:preview.uid"/>: {data.uid}</span>
            <span class="d-ce-preview__ctype"><f:translate key="LLL:EXT:desiderio/Resources/Private/Language/labels.xlf:preview.page"/>: {data.pid}</span>
        </div>
        <f:if condition="{data.header}">
            <h3 class="d-ce-preview__title">{data.header}</h3>
        </f:if>
        <!-- concise editor-facing summary fields -->
    </div>
</f:section>

</html>
```

## Header Section Stays Empty

Leave `<f:section name="Header"></f:section>` empty. The page-module preview chrome already renders the language flag, content-type icon, and edit link above the card; emitting another headline above the formatted card duplicates the title (the formatted card already shows `{data.header}` inside `d-ce-preview__title`).

The empty section is intentional and required: removing the section entirely throws `InvalidSectionException`, which TYPO3 catches and falls back to the standard renderer — re-introducing the duplicated header. An empty body returns `""` after `trim()`, which suppresses the slot cleanly without triggering the fallback.

## Meta Pills (UID + Page)

The first row inside the card uses `d-ce-preview__meta` to host small pills that help editors orient inside the page tree without opening the record:

- `d-ce-preview__type` — uppercase info badge with the editor-facing element title (for example `Founder Quote`).
- `d-ce-preview__ctype` — monospace pill for the Content Block name (`{settings._content_block_name}`), the record `uid`, and the record `pid`.

The UID and page pills must use XLIFF labels via `<f:translate key="LLL:EXT:desiderio/Resources/Private/Language/labels.xlf:preview.uid"/>` and `:preview.page`. The keys live in the global desiderio `Resources/Private/Language/labels.xlf` file (and every translated companion `de.labels.xlf`, `es.labels.xlf`, `fr.labels.xlf`, `it.labels.xlf`, `hu.labels.xlf`). Do not hardcode `UID` / `Page` strings into the template.

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
