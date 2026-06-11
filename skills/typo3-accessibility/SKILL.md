---
name: "typo3-accessibility"
description: "Audits and implements TYPO3 accessibility patterns for WCAG 2.2 AA, including Fluid templates, PHP helpers, JavaScript widgets, forms, focus states, ARIA, and go-live checks. Use when building or reviewing TYPO3 templates, content elements, extensions, or frontend code for accessibility, keyboard support, screen readers, WCAG, ARIA, or a11y readiness."
compatibility: "TYPO3 14.x"
metadata:
  version: "1.0.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Accessibility (WCAG 2.2 AA)

> Source: https://github.com/dirnbauer/webconsulting-skills

> **Compatibility:** TYPO3 **v14.x only**. Older cores are out of scope for this collection.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, Fluid ViewHelpers, and core
> features before adding custom markup. Verify methods exist in TYPO3 v14.

> **PHP & JS over TypoScript:** This skill provides PHP middleware, Fluid partials, and
> vanilla JavaScript solutions. TypoScript examples are avoided; use PHP-based approaches.

## 1. Accessibility Checklist (Go-Live Gate)

Run through this checklist before every deployment. Mark items as you fix them.

### Semantic Structure
- [ ] Every page has exactly one `<h1>`
- [ ] Heading hierarchy is sequential (`h1` > `h2` > `h3`, no skips)
- [ ] Landmark elements used: `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`
- [ ] Skip-to-content link is the first focusable element
- [ ] `<html lang="...">` matches page language
- [ ] Language changes within content use `lang` attribute on containing element

### Images & Media
- [ ] All `<img>` have `alt` attribute (empty `alt=""` for decorative)
- [ ] All `<img>` have explicit `width` and `height` (prevents CLS)
- [ ] Complex images (charts, infographics) have long description
- [ ] Videos have captions/subtitles
- [ ] Audio content has transcript
- [ ] No auto-playing media with sound

### Color & Contrast
- [ ] Text contrast >= 4.5:1 (normal) / 3:1 (large text >= 24px / 18.66px bold)
- [ ] UI components and graphical objects >= 3:1 contrast
- [ ] Information not conveyed by color alone (add icon, text, or pattern)
- [ ] Dark mode (if implemented) maintains contrast ratios

### Keyboard & Focus
- [ ] All interactive elements reachable via Tab
- [ ] Focus order matches visual order
- [ ] Visible focus indicator on all interactive elements (`:focus-visible`)
- [ ] No focus traps (except modals — which must trap correctly)
- [ ] Escape closes modals/overlays and returns focus to trigger
- [ ] Custom widgets have correct keyboard handlers

### Forms
- [ ] Every input has a programmatic `<label>` (explicit `for`/`id` or wrapping)
- [ ] Placeholder is not used as sole label
- [ ] Required fields indicated visually and with `required` attribute
- [ ] Error messages linked to inputs via `aria-describedby` + `aria-invalid`
- [ ] Form groups use `<fieldset>` + `<legend>`
- [ ] Correct `type` and `autocomplete` attributes on inputs

### ARIA & Dynamic Content
- [ ] Icon-only buttons have `aria-label`
- [ ] Decorative icons have `aria-hidden="true"`
- [ ] Dynamic updates use `aria-live="polite"` or `role="status"`
- [ ] Error alerts use `role="alert"`
- [ ] Active navigation links have `aria-current="page"`
- [ ] Expandable elements use `aria-expanded`

### Motion & Interaction
- [ ] `prefers-reduced-motion` respected (CSS and JS)
- [ ] No content flashes more than 3 times per second
- [ ] Touch targets meet **WCAG 2.2 AA 2.5.8** (minimum **24×24 CSS pixels**); use **44×44** as a stricter comfort target where feasible
- [ ] `user-scalable=no` is NOT set in viewport meta

### TYPO3-Specific
- [ ] Backend: alt text fields are filled for all images in File List
- [ ] Backend: content elements have descriptive headers (or `header_layout = 100` for hidden)
- [ ] Backend: page properties have proper `<title>` and `description`
- [ ] Fluid templates use `<f:link.page>` / `<f:link.typolink>` (not `<a>` with manual hrefs)
- [ ] Content Block / Content Element templates follow accessible patterns below

## 2. Fluid Template Patterns

### 2.1 Page Layout with Landmarks

```html
<!-- EXT:site_package/Resources/Private/Layouts/Default.html -->
<!-- Layout files must NOT contain <f:layout> — that tag belongs in Templates to select a layout. -->
<f:render section="Main" />
```

```html
<!-- EXT:site_package/Resources/Private/Templates/Default.html -->
<f:layout name="Default" />
<f:section name="Main">

<a href="#main-content" class="skip-link">
    <f:translate key="LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:skip_to_content" />
</a>

<header>
    <!-- Main nav landmark lives in the partial (e.g. MainMenu.html) to avoid nested <nav>. -->
    <f:cObject typoscriptObjectPath="lib.mainNavigation" />
</header>

<main id="main-content">
    <f:render section="Content" />
</main>

<footer>
    <nav aria-label="{f:translate(key: 'LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:nav.footer')}">
        <f:cObject typoscriptObjectPath="lib.footerNavigation" />
    </nav>
</footer>

</f:section>
```

### 2.2 Skip Link CSS

```css
.skip-link {
    position: absolute;
    top: -100%;
    left: 0;
    z-index: 10000;
    padding: 0.75rem 1.5rem;
    background: var(--color-primary, #2563eb);
    color: var(--color-on-primary, #fff);
    font-weight: 600;
    text-decoration: none;
}
.skip-link:focus {
    top: 0;
}
```

### 2.3 Accessible Image Rendering

```html
<!-- Partial: Resources/Private/Partials/Media/Image.html -->
<f:if condition="{image}">
    <figure>
        <f:image
            image="{image}"
            alt="{image.alternative}"
            title="{image.title}"
            width="{dimensions.width}"
            height="{dimensions.height}"
            loading="{f:if(condition: lazyLoad, then: 'lazy', else: 'eager')}"
            additionalAttributes="{decoding: 'async'}"
        />
        <f:if condition="{image.description}">
            <figcaption>{image.description}</figcaption>
        </f:if>
    </figure>
</f:if>
```

For decorative images (no informational value):

```html
<f:image image="{image}" alt="" />
```

### 2.4 Accessible Content Element Wrapper

```html
<!-- Partial: Resources/Private/Partials/ContentElement/Header.html -->
<f:if condition="{data.header} && {data.header_layout} != '100'">
    <f:switch expression="{data.header_layout}">
        <f:case value="1"><h1>{data.header}</h1></f:case>
        <f:case value="2"><h2>{data.header}</h2></f:case>
        <f:case value="3"><h3>{data.header}</h3></f:case>
        <f:case value="4"><h4>{data.header}</h4></f:case>
        <f:case value="5"><h5>{data.header}</h5></f:case>
        <f:defaultCase><h2>{data.header}</h2></f:defaultCase>
    </f:switch>
</f:if>
```

### 2.5 Accessible Navigation Partial

```html
<!-- Partial: Resources/Private/Partials/Navigation/MainMenu.html -->
<nav aria-label="{f:translate(key: 'LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:nav.main')}">
    <!-- role="list" restores list semantics in Safari/VoiceOver when list-style:none strips native list role -->
    <ul role="list">
        <f:for each="{menu}" as="item">
            <li>
                <f:if condition="{item.active}">
                    <f:then>
                        <a href="{item.link}" aria-current="page">{item.title}</a>
                    </f:then>
                    <f:else>
                        <a href="{item.link}">{item.title}</a>
                    </f:else>
                </f:if>

                <f:if condition="{item.children}">
                    <ul>
                        <f:for each="{item.children}" as="child">
                            <li>
                                <a href="{child.link}"
                                   {f:if(condition: child.active, then: 'aria-current="page"')}>
                                    {child.title}
                                </a>
                            </li>
                        </f:for>
                    </ul>
                </f:if>
            </li>
        </f:for>
    </ul>
</nav>
```

### 2.6 Accessible Accordion (Content Blocks / Custom CE)

```html
<div class="accordion" data-accordion>
    <f:for each="{items}" as="item" iteration="iter">
        <div class="accordion__item">
            <!-- Use role="heading" + aria-level so level matches page outline (pass headingLevel 2–6 from CE). -->
            <div role="heading" aria-level="{f:if(condition: headingLevel, then: headingLevel, else: '3')}">
                <button
                    type="button"
                    class="accordion__trigger"
                    aria-expanded="false"
                    aria-controls="accordion-panel-{data.uid}-{iter.index}"
                    id="accordion-header-{data.uid}-{iter.index}"
                    data-accordion-trigger
                >
                    {item.header}
                </button>
            </div>
            <div
                id="accordion-panel-{data.uid}-{iter.index}"
                role="region"
                aria-labelledby="accordion-header-{data.uid}-{iter.index}"
                class="accordion__panel"
                hidden
            >
                <f:format.html>{item.bodytext}</f:format.html>
            </div>
        </div>
    </f:for>
</div>
```

### 2.7 Accessible Tab Component

```html
<div class="tabs" data-tabs>
    <div role="tablist" aria-label="{f:translate(key: 'tabs.label')}">
        <f:for each="{items}" as="item" iteration="iter">
            <button
                type="button"
                role="tab"
                id="tab-{data.uid}-{iter.index}"
                aria-controls="tabpanel-{data.uid}-{iter.index}"
                aria-selected="{f:if(condition: iter.isFirst, then: 'true', else: 'false')}"
                tabindex="{f:if(condition: iter.isFirst, then: '0', else: '-1')}"
            >
                {item.header}
            </button>
        </f:for>
    </div>

    <f:for each="{items}" as="item" iteration="iter">
        <div
            role="tabpanel"
            id="tabpanel-{data.uid}-{iter.index}"
            aria-labelledby="tab-{data.uid}-{iter.index}"
            tabindex="0"
            {f:if(condition: iter.isFirst, then: '', else: 'hidden')}
        >
            <f:format.html>{item.bodytext}</f:format.html>
        </div>
    </f:for>
</div>
```


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
