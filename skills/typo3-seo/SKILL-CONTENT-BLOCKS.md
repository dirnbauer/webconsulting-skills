---
name: typo3-seo-content-blocks
description: SEO optimization for Content Blocks elements. Structured data, meta tags, and semantic HTML.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-seo
  - typo3-content-blocks
triggers:
  - seo content blocks
  - content blocks structured data
  - content blocks schema
---

# SEO with Content Blocks

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-seo](./SKILL.md) - Main SEO guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. Semantic HTML in Templates

### Proper Heading Hierarchy

```html
<!-- ContentBlocks/ContentElements/hero/templates/frontend.html -->
<header class="hero" role="banner">
    <h1>{data.header}</h1>
    <f:if condition="{data.subheadline}">
        <p class="lead">{data.subheadline}</p>
    </f:if>
</header>
```

### Article Content Block

```html
<!-- ContentBlocks/ContentElements/article/templates/frontend.html -->
<article itemscope itemtype="https://schema.org/Article">
    <header>
        <h2 itemprop="headline">{data.header}</h2>
        <time itemprop="datePublished" datetime="{data.publish_date -> f:format.date(format: 'c')}">
            {data.publish_date -> f:format.date(format: 'd.m.Y')}
        </time>
    </header>
    <div itemprop="articleBody">
        <f:format.html>{data.bodytext}</f:format.html>
    </div>
</article>
```

---

## 2. JSON-LD Structured Data

### FAQ Content Block with Schema

```yaml
# ContentBlocks/ContentElements/faq/config.yaml
name: myvendor/faq
fields:
  - identifier: items
    type: Collection
    labelField: question
    fields:
      - identifier: question
        type: Text
        required: true
      - identifier: answer
        type: Textarea
        enableRichtext: true
```

```html
<!-- templates/frontend.html -->
<div class="faq">
    <f:for each="{data.items}" as="item">
        <details>
            <summary>{item.question}</summary>
            <div><f:format.html>{item.answer}</f:format.html></div>
        </details>
    </f:for>
</div>

<!-- FAQPage Schema -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        <f:for each="{data.items}" as="item" iteration="iter">
        {
            "@type": "Question",
            "name": "{item.question -> f:format.htmlspecialchars()}",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "{item.answer -> f:format.stripTags() -> f:format.htmlspecialchars()}"
            }
        }<f:if condition="!{iter.isLast}">,</f:if>
        </f:for>
    ]
}
</script>
```

---

## 3. Image SEO

### Optimized Image Field

```yaml
# config.yaml
fields:
  - identifier: image
    type: File
    allowed: common-image-types
    maxitems: 1
```

```html
<!-- Template with proper alt text -->
<f:for each="{data.image}" as="img">
    <f:image 
        image="{img}" 
        alt="{img.alternative -> f:or(default: data.header)}"
        title="{img.title}"
        loading="lazy"
        width="800"
    />
</f:for>
```

---

## 4. Meta Tag Fields

### SEO-Enhanced Content Block

```yaml
# config.yaml
name: myvendor/page-hero
fields:
  - identifier: header
    useExistingField: true
  - identifier: seo_title
    type: Text
    max: 60
    description: Override page title (max 60 chars)
  - identifier: seo_description
    type: Textarea
    max: 160
    description: Meta description (max 160 chars)
```

---

## 5. Breadcrumb Schema

```html
<!-- ContentBlocks/ContentElements/breadcrumb/templates/frontend.html -->
<nav aria-label="Breadcrumb">
    <ol itemscope itemtype="https://schema.org/BreadcrumbList">
        <f:for each="{data.items}" as="item" iteration="iter">
            <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                <a itemprop="item" href="{item.link}">
                    <span itemprop="name">{item.title}</span>
                </a>
                <meta itemprop="position" content="{iter.cycle}" />
            </li>
        </f:for>
    </ol>
</nav>
```

---

## References

- [typo3-seo SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [Schema.org](https://schema.org/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
