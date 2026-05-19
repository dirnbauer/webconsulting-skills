# 7. Creating Page Types (Custom doktypes)

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 7. Creating Page Types (Custom doktypes)

Page Types extend the `pages` table with custom page types – ideal for blog articles, landing pages, news pages, or other page variants with special properties.

### When to Use Page Types

| Use Case | Example |
|----------|---------|
| Structured page properties | Blog with author, teaser image, publish date |
| Plugin integration | News lists, event calendars reading page properties |
| Different page behavior | Landing pages without navigation |
| SEO-specific fields | Custom meta fields per page type |

### Minimal Page Type

```yaml
# EXT:my_sitepackage/ContentBlocks/PageTypes/blog-article/config.yaml
name: myvendor/blog-article
typeName: 1705234567
fields:
  - identifier: author_name
    type: Text
```

### Full Page Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/PageTypes/blog-article/config.yaml
name: myvendor/blog-article
typeName: 1705234567   # Unix timestamp (unique identifier)
group: default         # Options: default, link, special
fields:
  - identifier: author_name
    type: Text
    label: Author
    required: true
  - identifier: teaser_text
    type: Textarea
    label: Teaser
  - identifier: hero_image
    type: File
    allowed: common-image-types
    maxitems: 1
  - identifier: publish_date
    type: DateTime
    label: Publish Date
  - identifier: reading_time
    type: Number
    label: Reading Time (minutes)
```

### Page Type Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `typeName` | integer | ✓ | Unique doktype number (use Unix timestamp) |
| `group` | string | | Group in selector: `default`, `link`, `special` |
| `allowedRecordTypes` | array | | Record types allowed on this doktype (default includes pages, `sys_category`, `sys_file_reference`, `sys_file_collection`; `*` wildcard possible — see official Page Types API) |

**Reserved typeName values:** 199, 254 (cannot be used)

### Icons for Page States

Page Types support state-specific icons. Add these to your assets folder:

```
ContentBlocks/PageTypes/blog-article/
├── assets/
│   ├── icon.svg              # Default icon
│   ├── icon-hide-in-menu.svg # Hidden in menu state
│   └── icon-root.svg         # Site root state
└── config.yaml
```

### Backend Preview

Create a `backend-preview.fluid.html` to preview custom page properties:

```html
<!-- templates/backend-preview.fluid.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:be="http://typo3.org/ns/TYPO3/CMS/Backend/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="card card-size-medium">
    <div class="card-body">
        <be:link.editRecord uid="{data.uid}" table="{data.mainType}" fields="author_name">
            <strong>Author:</strong> {data.author_name}
        </be:link.editRecord>
        <f:if condition="{data.publish_date}">
            <br/><small>Published: <f:format.date format="d.m.Y">{data.publish_date}</f:format.date></small>
        </f:if>
    </div>
</div>
</html>
```

### Frontend Integration

Page Types have **no automatic frontend rendering**. Add the ContentBlocksDataProcessor to your TypoScript:

```typoscript
# Configuration/TypoScript/setup.typoscript
page = PAGE
page {
    10 = FLUIDTEMPLATE
    10 {
        templateName = Default
        templateRootPaths.10 = EXT:my_sitepackage/Resources/Private/Templates/
        
        dataProcessing {
            # Process Content Blocks page data
            1 = content-blocks
        }
    }
}
```

Then access fields in your Fluid template:

```html
<!-- Resources/Private/Templates/Default.html -->
<f:if condition="{data.author_name}">
    <p class="author">By {data.author_name}</p>
</f:if>

<f:if condition="{data.hero_image}">
    <f:for each="{data.hero_image}" as="image">
        <f:image image="{image}" class="hero-image"/>
    </f:for>
</f:if>
```

### PAGEVIEW Content Areas and Columns **[v14.2+ only]**

For TYPO3 v14.2+ PAGEVIEW templates, prefer rendering backend layout columns through Core content areas instead of manually querying `tt_content`. This keeps Content Blocks, Fluid Styled Content, workspace overlays, language handling, and per-column context intact.

```html
<main class="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <f:render.contentArea contentArea="{content.main}" />
</main>

<aside class="space-y-4">
    <f:render.contentArea contentArea="{content.sidebar}" />
</aside>
```

Use backend layout identifiers (`main`, `sidebar`, `footer`, etc.) as the page-template contract. Apply TYPO3 v14 content restrictions per column so wide hero/feature elements stay out of narrow sidebars, and pass the content area context to element templates when their rendering needs to change by column.

### Remove from Page Tree Drag Area

To hide your page type from the "Create new page" drag area:

```typoscript
# Configuration/user.tsconfig
options {
    pageTree {
        doktypesToShowInNewPageDragArea := removeFromList(1705234567)
    }
}
```
