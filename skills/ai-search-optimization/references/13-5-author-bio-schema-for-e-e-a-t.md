# 13.5 Author Bio Schema for E-E-A-T

Continues `ai-search-optimization` from [full guide](full-guide.md).

### 13.5 Author Bio Schema for E-E-A-T

#### TCA Extension for Author Fields

```php
<?php
// Configuration/TCA/Overrides/pages.php

use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;

$additionalColumns = [
    'tx_sitepackage_author_name' => [
        'label' => 'Author Name',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_sitepackage_author_title' => [
        'label' => 'Author Title/Credentials',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_sitepackage_author_bio' => [
        'label' => 'Author Bio',
        'config' => [
            'type' => 'text',
            'rows' => 5,
        ],
    ],
    'tx_sitepackage_author_linkedin' => [
        'label' => 'Author LinkedIn URL',
        'config' => [
            'type' => 'link',
            'allowedTypes' => ['url'],
        ],
    ],
];

ExtensionManagementUtility::addTCAcolumns('pages', $additionalColumns);
ExtensionManagementUtility::addToAllTCAtypes(
    'pages',
    '--div--;Author,tx_sitepackage_author_name,tx_sitepackage_author_title,tx_sitepackage_author_bio,tx_sitepackage_author_linkedin'
);
```

#### Author Schema PSR-14 Event Listener

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use Brotkrueml\Schema\Event\RenderAdditionalTypesEvent;
use Brotkrueml\Schema\Type\TypeFactory;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener(identifier: 'site-package/add-author-schema')]
final readonly class AddAuthorSchema
{
    public function __construct(
        private TypeFactory $typeFactory,
    ) {}

    public function __invoke(RenderAdditionalTypesEvent $event): void
    {
        $request = $event->getRequest();
        $pageInformation = $request->getAttribute('frontend.page.information');
        $page = $pageInformation->getPageRecord();

        if (empty($page['tx_sitepackage_author_name'])) {
            return;
        }

        $author = $this->typeFactory->create('Person')
            ->setProperty('name', $page['tx_sitepackage_author_name'])
            ->setProperty('jobTitle', $page['tx_sitepackage_author_title'] ?? '')
            ->setProperty('description', $page['tx_sitepackage_author_bio'] ?? '');

        if (!empty($page['tx_sitepackage_author_linkedin'])) {
            $author->setProperty('sameAs', [$page['tx_sitepackage_author_linkedin']]);
        }

        $event->addType($author);
    }
}
```

### 13.6 FAQ Content Element with Schema

#### Content Block Definition (EXT:content_blocks)

```yaml
# ContentBlocks/ContentElements/faq-accordion/config.yaml
name: vendor/faq-accordion
typeName: faq_accordion
title: FAQ Accordion
description: FAQ with structured data for AI search
group: common

fields:
  - identifier: faq_items
    type: Collection
    labelField: question
    fields:
      - identifier: question
        type: Text
        required: true
      - identifier: answer
        type: Textarea
        enableRichtext: true
        required: true
```

#### Fluid Template with Schema

```html
<!-- ContentBlocks/ContentElements/faq-accordion/Resources/Private/Frontend.html -->
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<section class="faq-accordion">
    <schema:type.fAQPage>
        <f:for each="{data.faq_items}" as="item">
            <schema:type.question -as="mainEntity" name="{item.question}">
                <schema:type.answer -as="acceptedAnswer">
                    <schema:property -as="text" value="{item.answer -> f:format.stripTags()}" />
                </schema:type.answer>
            </schema:type.question>
            
            <details class="faq-item">
                <summary class="faq-question">{item.question}</summary>
                <div class="faq-answer">
                    <f:format.html>{item.answer}</f:format.html>
                </div>
            </details>
        </f:for>
    </schema:type.fAQPage>
</section>
```

### 13.7 Breadcrumb Schema

#### Fluid ViewHelper Implementation

```html
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<nav aria-label="Breadcrumb">
    <schema:type.breadcrumbList>
        <f:for each="{breadcrumbs}" as="crumb" iteration="iter">
            <schema:type.listItem -as="itemListElement" position="{iter.cycle}">
                <schema:property -as="name" value="{crumb.title}" />
                <schema:property -as="item" value="{crumb.url}" />
            </schema:type.listItem>
        </f:for>
    </schema:type.breadcrumbList>
    
    <ol class="breadcrumb">
        <f:for each="{breadcrumbs}" as="crumb" iteration="iter">
            <li class="breadcrumb-item{f:if(condition: iter.isLast, then: ' active')}">
                <f:if condition="{iter.isLast}">
                    <f:then>{crumb.title}</f:then>
                    <f:else>
                        <a href="{crumb.url}">{crumb.title}</a>
                    </f:else>
                </f:if>
            </li>
        </f:for>
    </ol>
</nav>
```

### 13.8 Semantic HTML via Fluid Layouts

```html
<!-- Resources/Private/Layouts/Default.html -->
<!DOCTYPE html>
<html lang="{siteLanguage.locale.languageCode}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <f:render section="HeaderAssets" optional="true" />
</head>
<body>
    <header role="banner">
        <f:render partial="Header" />
    </header>
    
    <nav role="navigation" aria-label="Main navigation">
        <f:render partial="Navigation/Main" />
    </nav>
    
    <main role="main">
        <article>
            <header>
                <h1>{page.title}</h1>
                <f:if condition="{page.subtitle}">
                    <p class="lead">{page.subtitle}</p>
                </f:if>
            </header>
            
            <section>
                <f:render section="Content" />
            </section>
        </article>
    </main>
    
    <aside role="complementary">
        <f:render partial="Sidebar" optional="true" />
    </aside>
    
    <footer role="contentinfo">
        <f:render partial="Footer" />
    </footer>
</body>
</html>
```

### 13.9 TYPO3 AI Search Optimization Checklist

#### Extensions & Configuration
- [ ] EXT:seo installed and configured
- [ ] EXT:schema (brotkrueml/schema ^4.2) installed
- [ ] Static TypoScript templates included
- [ ] robots.txt configured via site config with AI bot rules

#### Schema Implementation
- [ ] Organization schema on all pages
- [ ] Article schema on content pages
- [ ] FAQPage schema on FAQ content
- [ ] HowTo schema on tutorial content
- [ ] BreadcrumbList on all pages
- [ ] Author/Person schema with credentials

#### Content Structure
- [ ] Semantic HTML5 elements in Fluid templates
- [ ] Proper heading hierarchy (single H1)
- [ ] Visible publication and update dates
- [ ] Author bios with credentials
- [ ] Alt text on all images via FAL

#### Technical
- [ ] SYS_LASTCHANGED used for content freshness
- [ ] Cache headers configured
- [ ] XML sitemap via EXT:seo
- [ ] Canonical URLs configured
- [ ] hreflang for multi-language sites

### 13.10 Debugging Schema Output

#### Admin Panel Integration

EXT:schema integrates with TYPO3's Admin Panel. Enable it to see generated JSON-LD:

```typoscript
# config/system/settings.php
$GLOBALS['TYPO3_CONF_VARS']['BE']['adminPanel'] = true;
```

#### Validation Tools

After implementing structured data, validate using:

1. **Schema Markup Validator**: https://validator.schema.org/
2. **Google Rich Results Test**: https://search.google.com/test/rich-results
3. **Google Search Console**: Submit and monitor structured data

#### View Generated JSON-LD

```bash
# Fetch page and extract JSON-LD
curl -s https://example.com/page | grep -o '<script type="application/ld+json">.*</script>'
```

---
