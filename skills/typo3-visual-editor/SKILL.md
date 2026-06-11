---
name: "typo3-visual-editor"
description: "Installs, configures, removes, and migrates TYPO3 sitepackages for FriendsOfTYPO3 Visual Editor, including inline editing, f:render.text, f:render.contentArea, f:mark.contentArea, record transformation, PAGEVIEW content areas, colPos migration, and template readiness. Use when the user mentions Visual Editor, inline editing, frontend editing, content areas, Fluid template migration, or visual editing readiness in TYPO3 13/14."
metadata:
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Visual Editor

> Source: https://github.com/dirnbauer/webconsulting-skills

Use this skill to make a TYPO3 project ready for `friendsoftypo3/visual-editor`, especially when upgrading Fluid templates so editors can edit fields and content areas in context.

The critical work is not only installing the extension. The Visual Editor needs frontend output that is traceable back to records, fields, and content areas. Migrate page columns to `f:render.contentArea` where possible and migrate editable text fields to `f:render.text`.

## What it does

The Visual Editor adds an in-backend frontend editing mode for TYPO3 content. Editors can work close to the rendered page, with inline text editing, drag-and-drop repositioning, adding/removing content elements, real-time preview behavior, workspace support, optional autosaving, container support, and Context Panel integration.

For custom sitepackages, the extension depends on Fluid hooks:

- `f:render.text` marks TCA-backed text fields as editable and renders them according to field configuration.
- `f:render.contentArea` renders TYPO3 v14.2+ page content areas and lets extensions modify content-area output.
- `f:mark.contentArea` is the Visual Editor fallback for TYPO3 v13 or legacy renderers that cannot yet use `f:render.contentArea`.

## When to use

Use this skill when the user asks for:

- installing or removing `friendsoftypo3/visual-editor`
- making a sitepackage compatible with visual editing
- replacing `f:cObject typoscriptObjectPath="lib.dynamicContent"` column rendering
- updating Fluid templates for fields shown in the backend
- using `f:render.text`, `f:render.contentArea`, or `f:mark.contentArea`
- diagnosing why inline editing, drag-and-drop, add, delete, or content-area highlighting does not work
- upgrading TYPO3 v13/v14 templates toward v14.2+ PAGEVIEW rendering

## Version strategy

Prefer TYPO3 v14.2+ and Core ViewHelpers:

```html
<f:render.contentArea contentArea="{content.main}" />
<h1>{record -> f:render.text(field: 'header')}</h1>
```

Use `f:mark.contentArea` only when the project cannot use the v14.2+ content-area pipeline yet, for example TYPO3 v13 compatibility or legacy content rendering with VHS/Flux/container loops.

Always verify the package constraints before changing `composer.json`; current upstream (1.7.1) requires PHP 8.2+ and supports TYPO3 13.4.22+ or 14.3+ (`typo3/cms-core ^13.4.22 || ^14.3.0`; only early 1.0.x releases supported 14.2).

## How to install

Composer installation:

```bash
ddev composer require friendsoftypo3/visual-editor
ddev typo3 cache:flush
```

Without DDEV:

```bash
composer require friendsoftypo3/visual-editor
vendor/bin/typo3 cache:flush
```

Non-Composer installation:

1. Install the extension through the TYPO3 Extension Manager.
2. Activate `visual_editor`.
3. Flush TYPO3 caches.
4. Run database updates if the Install Tool requests them.

Optional helpers:

- Install `andersundsehr/visual-editor-fluid-styled-content-addon` (extension key: `visual_editor_fluid_styled_content_addon`) if the project relies heavily on `fluid_styled_content` templates and wants automatic text-editing integration there.
- Consider `wapplersystems/multisite-belogin` for multi-domain projects where backend users need to be logged in across several frontend domains.

## How to configure

1. Confirm backend users can access the Visual Editor module and page tree.
2. Make frontend rendering use templates that expose editable records and fields.
3. Add `record-transformation` where templates currently receive raw arrays but need Record objects.
4. Render page columns through `f:render.contentArea` on TYPO3 v14.2+.
5. Wrap unavoidable legacy column renderers with `f:mark.contentArea`.
6. Ensure rich-text styles used by CKEditor are also available in frontend CSS, because Visual Editor uses the rendered frontend context.
7. Test in the backend Visual Editor module with a real editor user, not only an admin account.

### Record transformation

If a content element template has raw `{data}` but no `{record}` object, add the data processor before using `f:render.text`:

```typoscript
lib.contentElement.dataProcessing.1768551979 = record-transformation
```

Then render TCA-backed text fields from the Record object:

```html
<h1>{record -> f:render.text(field: 'header')}</h1>
```

Use the database/TCA field name in `field`, not an Extbase property alias.

## Template migration workflow

### 1. Inventory editable fields

Search Fluid templates for direct field output and manual text formatting:

```bash
rg -n "\{(record|data)\.[a-zA-Z0-9_]+\}|format\.html|format\.nl2br" Resources/Private
```

For each TCA-backed input, textarea, or richtext field shown in frontend output, prefer `f:render.text`.

Before:

```html
<h1>{record.header}</h1>
<f:format.html>{record.bodytext}</f:format.html>
<f:format.nl2br>{record.teaser}</f:format.nl2br>
```

After:

```html
<h1>{record -> f:render.text(field: 'header')}</h1>
<div class="prose">{record -> f:render.text(field: 'bodytext')}</div>
<p>{record -> f:render.text(field: 'teaser')}</p>
```

For conditional rendering, render once into a variable so the condition and output use the same processed value:

```html
<f:variable name="header" value="{record -> f:render.text(field: 'header', optional: true)}" />
<f:if condition="{header}">
    <h1>{header}</h1>
</f:if>
```

### 2. Migrate content areas

Find legacy content rendering:

```bash
rg -n "lib\.dynamicContent|f:cObject|v:content\.render|flux:content\.render|children_" Resources/Private Configuration
```

On TYPO3 v14.2+, replace dynamic `colPos` rendering with `f:render.contentArea`.

Before:

```html
<f:cObject typoscriptObjectPath="lib.dynamicContent" data="{colPos: '3'}"/>
```

After:

```html
<f:render.contentArea contentArea="{content.main}" />
```

The replacement is not a mechanical `3` to `main` conversion. `{content.main}` exists when the page uses `PAGEVIEW`, the `page-content` data processor, and a backend layout column whose identifier is `main`. Map every old `colPos` to the matching backend layout identifier:

| Legacy value | Backend layout contract | Fluid output |
|--------------|-------------------------|--------------|
| `colPos = 0` | identifier `main` | `{content.main}` |
| `colPos = 1` | identifier `sidebar` | `{content.sidebar}` |
| `colPos = 3` | identifier `main`, `stage`, or project-specific name | `{content.<identifier>}` |

Set up PAGEVIEW and page-content processing when missing:

```typoscript
page = PAGE
page {
  10 = PAGEVIEW
  10 {
    paths.10 = EXT:my_sitepackage/Resources/Private/Templates/
    dataProcessing.10 = page-content
  }
}
```

Keep backend layout identifiers stable because they become the template contract.

### 3. Use fallback wrappers for legacy rendering

If the project cannot use `f:render.contentArea`, preserve the existing renderer and wrap it:

```html
<f:mark.contentArea colPos="3">
    <f:cObject typoscriptObjectPath="lib.dynamicContent" data="{colPos: '3'}"/>
</f:mark.contentArea>
```

For EXT:container child columns:

```html
<f:mark.contentArea colPos="201" txContainerParent="{record.uid}">
    <f:for each="{children_201}" as="element">
        {element.renderedContent -> f:format.raw()}
    </f:for>
</f:mark.contentArea>
```

For EXT:vhs:

```html
<f:mark.contentArea colPos="0">
    <v:content.render column="0"/>
</f:mark.contentArea>
```

For EXT:flux:

```html
<f:mark.contentArea colPos="{data.uid}00">
    <flux:content.render area="column0"/>
</f:mark.contentArea>
```

Treat `f:mark.contentArea` as a compatibility step. Plan to remove it when the project moves fully to TYPO3 v14.2+ Core content areas.

## Backend fields

For every field that is editable in the backend and rendered in the frontend:

- Use `f:render.text` for TCA `input` and `text` fields, including rich text.
- Use the exact database field name, for example `header`, `subheader`, `bodytext`, or `tx_sitepackage_teaser`.
- Use `optional: true` only for shared partials where the field may legitimately be absent.
- Do not use `f:render.text` for computed values, virtual getters, FAL objects, links, booleans, selects, dates, or already-rendered HTML snippets.
- Keep non-text fields on the appropriate ViewHelper, for example `f:image`, `f:link.typolink`, or project-specific rendering.

Content Blocks templates follow the same rule once a Record object is available. If the frontend template only exposes `{data}`, either add record transformation or keep direct rendering for values that are not supported by `f:render.text`.

## Problems to check

Inline text is not editable:

- The template still outputs `{record.header}` or `{data.header}` directly.
- The template receives an array instead of a Record object.
- The field is not a supported TCA text field.
- The backend user cannot edit that field.

Content area is not highlighted or drag-and-drop does not work:

- The page template still renders content through `f:cObject`, VHS, Flux, or a custom query without `f:render.contentArea` or `f:mark.contentArea`.
- The backend layout column does not have the identifier used by `{content.<identifier>}`.
- `page-content` data processing is missing.
- A container child column is missing `txContainerParent`.

Rich text looks different while editing:

- CKEditor `contentsCss` styles are not loaded in the actual frontend CSS.
- Custom `lib.parseFunc_RTE` behavior is not represented in frontend styles.

Multi-domain editing fails:

- Backend login exists only on one domain.
- Configure domain login behavior or use a multisite backend-login helper.

Workspace behavior differs:

- Test with a workspace user and confirm overlays, permissions, language overlays, and publish flow before rollout.

## Do

- Prefer TYPO3 v14.2+ `f:render.contentArea` over custom `lib.dynamicContent` rendering.
- Convert text/richtext output to `f:render.text` field by field.
- Keep backend layout column identifiers explicit and stable.
- Verify templates with real content, translations, workspaces, and restricted editor permissions.
- Keep frontend CSS as the source of truth for visual editing styles.
- Leave Core ViewHelpers in place after removing the extension on TYPO3 v14; they are useful beyond Visual Editor.

## Don't

- Do not assume `colPos: 3` always maps to `{content.main}`; inspect the backend layout.
- Do not wrap everything in `f:mark.contentArea` on TYPO3 v14.2+ if `f:render.contentArea` is available.
- Do not use `f:render.text` for non-TCA or computed values.
- Do not pass Extbase property names when the database field name differs.
- Do not remove escaping or replace text rendering with `f:format.raw` to make editing work.
- Do not judge readiness from admin-only testing.

## How to remove

Composer removal:

```bash
ddev composer remove friendsoftypo3/visual-editor
ddev typo3 cache:flush
```

Without DDEV:

```bash
composer remove friendsoftypo3/visual-editor
vendor/bin/typo3 cache:flush
```

Non-Composer removal:

1. Disable and uninstall `visual_editor` in the Extension Manager.
2. Flush caches.
3. Remove Visual Editor-specific configuration.
4. Remove `f:mark.contentArea` wrappers if the ViewHelper came from the extension and the project no longer has it installed.

On TYPO3 v14.2+, keep `f:render.contentArea` and `f:render.text` unless there is a project reason to revert them. They are Core ViewHelpers and remain valid without the extension.

## FAQ

### Is installing the extension enough?

Only for themes/templates that already expose editable fields and content areas in the expected way. Custom sitepackages usually need Fluid template updates.

### What replaces `lib.dynamicContent`?

On TYPO3 v14.2+, use `f:render.contentArea` with a `ContentArea` object from the `page-content` processor:

```html
<f:render.contentArea contentArea="{content.main}" />
```

The old `colPos` number maps through the backend layout column identifier, not through the Fluid ViewHelper itself.

### What if the project still supports TYPO3 v13?

Use `f:mark.contentArea` around the existing renderer for content areas and use the Visual Editor-provided compatibility where available. Keep a migration note to replace those wrappers with `f:render.contentArea` after moving to TYPO3 v14.2+.

### Should all `{record.field}` output become `f:render.text`?

No. Convert TCA-backed text fields that editors should edit inline. Keep images, links, dates, relations, booleans, computed values, and custom view models on appropriate rendering paths.

### Can I use `f:render.text` with Extbase models?

Yes, if the model maps to TCA-backed fields and includes the needed record type information. The `field` argument still uses the database/TCA field name.

### Why does `optional: true` matter?

Shared partials may render several content types. If a field is missing for one record type, `optional: true` lets the partial continue instead of throwing a missing-field exception.

### Does Visual Editor replace backend forms?

No. It improves contextual editing, but complex fields, media replacement, permissions, validation, localization, workspaces, and advanced forms still rely on TYPO3 backend behavior and the Context Panel.

## Validation checklist

- `composer show friendsoftypo3/visual-editor` reports a version compatible with the TYPO3 Core version.
- `rg "f:cObject|lib.dynamicContent|v:content.render|flux:content.render|children_" Resources/Private` has either been migrated or deliberately wrapped.
- Page templates use `PAGEVIEW` and `page-content` where `f:render.contentArea` is used.
- Text fields shown in frontend output use `f:render.text` where inline editing is expected.
- Editors can add, edit, move, and delete content in the Visual Editor module.
- Rich text visually matches frontend output.
- Workspaces, languages, and multi-domain pages have been tested where the project uses them.

## Sources

Source: https://github.com/dirnbauer/webconsulting-skills
- FriendsOfTYPO3 `visual_editor`: https://github.com/FriendsOfTYPO3/visual_editor
- TYPO3 Fluid `f:render.contentArea` ViewHelper: https://docs.typo3.org/other/typo3/view-helper-reference/main/en-us/Global/Render/ContentArea.html
- TYPO3 Fluid `f:render.text` ViewHelper: https://docs.typo3.org/other/typo3/view-helper-reference/main/en-us/Global/Render/Text.html
- b13 overview: https://b13.com/blog/visual-editing-in-typo3-when-content-management-happens-in-context
