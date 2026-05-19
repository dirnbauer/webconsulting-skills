---
name: "typo3-content-blocks"
description: "Guides TYPO3 Content Blocks modeling for Content Elements, Record Types, Page Types, and File Types as the single source of truth. Use when creating, migrating, auditing, or debugging Content Blocks config.yaml files, make:content-block output, content elements, record types, page types, file types, collections, IRRE, labels, previews, or friendsoftypo3/content-blocks behavior."
compatibility: "TYPO3 14.x — `friendsoftypo3/content-blocks` 2.x (verify on [Packagist](https://packagist.org/packages/friendsoftypo3/content-blocks))"
metadata:
  version: "1.5.0"
  related_skills: "typo3-content-blocks-migration, shadcn-ui, typo3-vite"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Content Blocks Development

> Source: https://github.com/dirnbauer/webconsulting-skills

> **Compatibility:** This skill targets **TYPO3 v14.x** with **Content Blocks 2.x**. Always match the [Packagist `friendsoftypo3/content-blocks`](https://packagist.org/packages/friendsoftypo3/content-blocks) constraint to your Core version.
> For **Content Blocks 1.x on TYPO3 v13**, upstream requires **TYPO3 ≥ 13.4** (`typo3/cms-core: ^13.4`) — confirm on Packagist.
> Examples use TYPO3 v14 APIs and CB 2.x; adjust `composer.json` if upstream constraints differ.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

> **Migration Coverage:** Content Blocks migration and cross-skill handoff guidance are documented directly in this skill and its local add-ons.

## 1. The Single Source of Truth Principle

Content Blocks is the **modern approach** to creating custom content types in TYPO3. It eliminates redundancy by providing a **single YAML configuration** that generates:

- TCA (Table Configuration Array)
- Database schema (SQL)
- TypoScript rendering
- Backend forms and previews
- Labels and translations

### Why Content Blocks?

| Traditional Approach | Content Blocks Approach |
|---------------------|------------------------|
| Multiple TCA files | One `config.yaml` |
| Manual SQL definitions | Auto-generated schema |
| Separate TypoScript | Auto-registered rendering |
| Scattered translations | Single `labels.xlf` |
| Complex setup | Simple folder structure |

## 2. Installation

```bash
# Install via Composer (DDEV recommended)
ddev composer require friendsoftypo3/content-blocks

# After installation, clear caches
ddev typo3 cache:flush
```

> **Version constraint:** Content Blocks **1.x** requires TYPO3 **≥ 13.4** (`typo3/cms-core: ^13.4` in the package). TYPO3 **13.1–13.3** do **not** satisfy that Composer constraint.

### Security Configuration (Classic Mode)

For non-composer installations, deny web access to ContentBlocks folder:

```apache
# .htaccess addition
RewriteRule (?:typo3conf/ext|typo3/sysext|typo3/ext)/[^/]+/(?:Configuration|ContentBlocks|Resources/Private|Tests?|Documentation|docs?)/ - [F]
```

## 3. Content Types Overview

Content Blocks supports four content types:

| Type | Folder | Table | Use Case |
|------|--------|-------|----------|
| `ContentElements` | `ContentBlocks/ContentElements/` | `tt_content` | Frontend content (hero, accordion, CTA) |
| `RecordTypes` | `ContentBlocks/RecordTypes/` | Custom/existing | Structured records (news, products, team) |
| `PageTypes` | `ContentBlocks/PageTypes/` | `pages` | Custom page types (blog, landing page) |
| `FileTypes` | `ContentBlocks/FileTypes/` | `sys_file_reference` | Extended file references (photographer, copyright) |

## 4. Folder Structure

```
EXT:my_sitepackage/
└── ContentBlocks/
    ├── ContentElements/
    │   └── my-hero/
    │       ├── assets/
    │       │   └── icon.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       ├── templates/
    │       │   ├── backend-preview.fluid.html
    │       │   ├── frontend.fluid.html
    │       │   └── partials/
    │       └── config.yaml
    ├── RecordTypes/
    │   └── my-record/
    │       ├── assets/
    │       │   └── icon.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       └── config.yaml
    ├── PageTypes/
    │   └── blog-article/
    │       ├── assets/
    │       │   ├── icon.svg
    │       │   ├── icon-hide-in-menu.svg
    │       │   └── icon-root.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       ├── templates/
    │       │   └── backend-preview.fluid.html
    │       └── config.yaml
    └── FileTypes/
        └── image-extended/
            ├── language/
            │   └── labels.xlf
            └── config.yaml
```

## 5. Creating Content Elements

### Kickstart Command (Recommended)

```bash
# Interactive mode
ddev typo3 make:content-block

# One-liner
ddev typo3 make:content-block \
  --content-type="content-element" \
  --vendor="myvendor" \
  --name="hero-banner" \
  --title="Hero Banner" \
  --extension="my_sitepackage"

# After creation, update database
ddev typo3 cache:flush -g system
ddev typo3 extension:setup --extension=my_sitepackage
```

### Predefined Basics (content elements)

List under `basics:` to pull in Core field groups: **`TYPO3/Header`**, **`TYPO3/Appearance`**, **`TYPO3/Links`**, **`TYPO3/Categories`**. See the [Content Blocks basics reference](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/API/Basics/Index.html).

### Minimal Content Element

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/hero-banner/config.yaml
name: myvendor/hero-banner
fields:
  - identifier: header
    useExistingField: true
  - identifier: bodytext
    useExistingField: true
```

### Full Content Element Example

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/hero-banner/config.yaml
name: myvendor/hero-banner
group: default
description: "A full-width hero banner with image and CTA"
prefixFields: true
prefixType: full
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
    label: Subheadline
  - identifier: hero_image
    type: File
    minitems: 1
    maxitems: 1
    allowed: common-image-types
  - identifier: cta_link
    type: Link
    label: Call to Action Link
  - identifier: cta_text
    type: Text
    label: Button Text
```

### Frontend Template

```html
<!-- templates/frontend.fluid.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:cb="http://typo3.org/ns/TYPO3/CMS/ContentBlocks/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:asset.css identifier="hero-banner-css" href="{cb:assetPath()}/frontend.css"/>

<section class="hero-banner">
    <f:if condition="{data.hero_image}">
        <f:for each="{data.hero_image}" as="image">
            <f:image image="{image}" alt="{data.header}" class="hero-image"/>
        </f:for>
    </f:if>
    
    <div class="hero-content">
        <h1>{data.header}</h1>
        <f:if condition="{data.subheadline}">
            <p class="subheadline">{data.subheadline}</p>
        </f:if>
        
        <f:if condition="{data.cta_link}">
            <f:link.typolink parameter="{data.cta_link}" class="btn btn-primary">
                {data.cta_text -> f:or(default: 'Learn more')}
            </f:link.typolink>
        </f:if>
    </div>
</section>
</html>
```

### shadcn/ui Frontend Template Pattern

When a Content Block should follow shadcn/ui styling, keep the Content Block YAML as the content model and move repeated visual structure into shared Fluid components. The `frontend.fluid.html` entrypoint should map `{data}` fields to typed atomic components rather than duplicating bespoke CSS in every block.

```html
<!-- templates/frontend.fluid.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:d="http://typo3.org/ns/Vendor/Sitepackage/Components/ComponentCollection"
      data-namespace-typo3-fluid="true">

<section class="py-12 md:py-16">
    <d:molecule.card class="mx-auto max-w-2xl">
        <d:molecule.cardHeader>
            <d:molecule.cardTitle>{data.header}</d:molecule.cardTitle>
            <f:if condition="{data.subheadline}">
                <d:molecule.cardDescription>{data.subheadline}</d:molecule.cardDescription>
            </f:if>
        </d:molecule.cardHeader>
        <d:molecule.cardContent>
            <f:format.html>{data.bodytext}</f:format.html>
        </d:molecule.cardContent>
    </d:molecule.card>
</section>
</html>
```

Guidelines:
- Preserve existing field identifiers, `fixture.json`, labels, and editor workflows unless the content model itself is changing.
- Use shared Fluid components for shadcn primitives such as Button, Badge, Card, Form controls, Tabs, Accordion, Alert, Table, and Sheet/Dialog shells.
- Put `<f:argument>` type contracts in reusable Fluid components and partials. Avoid adding required arguments to a Content Block entry template unless the render context is fully controlled.
- Use `f:asset.css` / `f:asset.script` only for block-specific assets. Shared shadcn/Tailwind tokens and utility classes belong in the site CSS entrypoint.
- For interactive shadcn patterns, use Alpine or small vanilla controllers with ARIA and `data-state` attributes instead of React/Radix runtime dependencies.
- Create or update styleguide fixtures so every Content Block can be rendered with realistic content in light and dark mode.

### Backend Preview Template

```html
<!-- templates/backend-preview.fluid.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:be="http://typo3.org/ns/TYPO3/CMS/Backend/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="content-block-preview">
    <strong>{data.header}</strong>
    <f:if condition="{data.subheadline}">
        <br/><em>{data.subheadline}</em>
    </f:if>
    <f:if condition="{data.hero_image}">
        <f:for each="{data.hero_image}" as="image">
            <be:thumbnail image="{image}" width="100" height="100"/>
        </f:for>
    </f:if>
</div>
</html>
```


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
