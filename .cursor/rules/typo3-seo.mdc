---
name: typo3-seo
description: >-
  SEO configuration and best practices for TYPO3 v14, including EXT:seo setup,
  sitemaps, meta tags, and structured data. Use when working with seo, sitemap, meta,
  robots, structured data, opengraph.
compatibility: TYPO3 14.x
metadata:
  version: "2.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 SEO Configuration

> **Compatibility:** TYPO3 v14.x
> All SEO configurations in this skill work on TYPO3 v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## 1. Core SEO Extension Setup

### Installation

```bash
ddev composer require typo3/cms-seo
ddev typo3 extension:setup -e seo
ddev typo3 cache:flush
```

### Page Properties SEO Tab

After installation, pages have an "SEO" tab with:
- `seo_title` - Override page title for search engines
- `description` - Meta description
- `og_title`, `og_description`, `og_image` - Open Graph
- `twitter_title`, `twitter_description`, `twitter_image` - Twitter Cards
- `canonical_link` - Canonical URL override
- `no_index`, `no_follow` - Robot directives

## 2. Meta Tags Configuration

### TypoScript Setup (TYPO3 v14)

```typoscript
page {
    meta {
        # Basic meta tags
        viewport = width=device-width, initial-scale=1
        robots = index,follow
        author = webconsulting
        
        # Open Graph (auto-filled by EXT:seo if page properties set)
        og:type = website
        og:site_name = {$site.name}
        og:locale = de_AT
        
        # Twitter Cards
        twitter:card = summary_large_image
        twitter:site = @webconsulting
    }
}
```

### Dynamic Meta Description

```typoscript
page.meta.description = TEXT
page.meta.description {
    # Page description, then slide rootline; add further fallbacks via stdWrap.if / constants (do not use {$...} inside `data` as a getText key)
    data = page:description
    ifEmpty.data = levelfield:-1,description,slide
    htmlSpecialChars = 1
}
```

### Hreflang Tags (Multi-Language)

EXT:seo automatically generates hreflang tags based on site configuration:

```yaml
# config/sites/main/config.yaml
languages:
  - languageId: 0
    locale: de_AT
    hreflang: de-AT
    title: Deutsch
    
  - languageId: 1
    locale: en_GB
    hreflang: en-GB
    title: English
```

## 3. XML Sitemap Configuration

### Basic Sitemap Setup

```yaml
# config/sites/main/config.yaml
base: 'https://example.com/'
routeEnhancers:
  PageTypeSuffix:
    type: PageType
    map:
      sitemap.xml: 1533906435
```

### TypoScript Sitemap Configuration (TYPO3 v14)

```typoscript
plugin.tx_seo {
    config {
        xmlSitemap {
            sitemaps {
                # Pages sitemap (default)
                pages {
                    provider = TYPO3\CMS\Seo\XmlSitemap\PagesXmlSitemapDataProvider
                    config {
                        excludedDoktypes = 3,4,6,7,199,254,255
                        additionalWhere = no_index = 0 AND nav_hide = 0
                    }
                }
                
                # News sitemap (example for EXT:news)
                news {
                    provider = GeorgRinger\News\Seo\NewsXmlSitemapDataProvider
                    config {
                        table = tx_news_domain_model_news
                        sortField = datetime
                        lastModifiedField = tstamp
                        changeFreqField = sitemap_changefreq
                        priorityField = sitemap_priority
                        additionalWhere = {#hidden} = 0 AND {#deleted} = 0
                        pid = 123
                        url {
                            pageId = 45
                            fieldToParameterMap {
                                uid = tx_news_pi1[news]
                            }
                        }
                    }
                }
                
                # Products sitemap (custom extension)
                products {
                    provider = TYPO3\CMS\Seo\XmlSitemap\RecordsXmlSitemapDataProvider
                    config {
                        table = tx_shop_domain_model_product
                        sortField = title
                        lastModifiedField = tstamp
                        pid = 100
                        recursive = 2
                        url {
                            pageId = 50
                            fieldToParameterMap {
                                uid = tx_shop_pi1[product]
                            }
                            additionalGetParameters {
                                tx_shop_pi1.controller = Product
                                tx_shop_pi1.action = show
                            }
                        }
                    }
                }
            }
        }
    }
}
```

### Sitemap Index

Access sitemap at: `https://example.com/sitemap.xml`

Individual sitemaps:
- `https://example.com/sitemap.xml?sitemap=pages`
- `https://example.com/sitemap.xml?sitemap=news`

## 4. Robots.txt Configuration

### Static Robots.txt

```text
# public/robots.txt
User-agent: *
Allow: /

# Disallow TYPO3 backend and system directories
Disallow: /typo3/
Disallow: /typo3conf/
Disallow: /typo3temp/

# Sitemap location
Sitemap: https://example.com/sitemap.xml
```

### Dynamic Robots.txt via TypoScript

```typoscript
# Generate robots.txt dynamically
robotstxt = PAGE
robotstxt {
    typeNum = 9999
    config {
        disableAllHeaderCode = 1
        additionalHeaders.10.header = Content-Type: text/plain; charset=utf-8
    }
    
    10 = TEXT
    10.value (
User-agent: *
Allow: /
Disallow: /typo3/
Disallow: /typo3conf/
Disallow: /typo3temp/

Sitemap: https://example.com/sitemap.xml
    )
    # For a dynamic base URL, derive it from site `base` (YAML), a TypoScript constant, or
    # a small data processor — `TEXT.value` does not interpolate `{getEnv:...}` getText.
}
```

Route enhancement:

```yaml
# config/sites/main/config.yaml
routeEnhancers:
  PageTypeSuffix:
    type: PageType
    map:
      robots.txt: 9999
```

## 5. Canonical URLs

### Automatic Canonicals

EXT:seo generates canonical tags automatically. Configure in site:

```yaml
# config/sites/main/config.yaml
base: 'https://example.com/'
baseVariants:
  - base: 'https://staging.example.com/'
    condition: 'applicationContext == "Development"'
```

### Manual Canonical Override

In page properties SEO tab, set "Canonical URL" field.

Via TypoScript:

```typoscript
page.headerData.100 = TEXT
page.headerData.100 {
    value = <link rel="canonical" href="https://example.com/specific-page" />
}
```

## 6. Structured Data (JSON-LD)

### Organization Schema

```typoscript
page.headerData.200 = TEXT
page.headerData.200.value (
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "webconsulting",
    "url": "https://webconsulting.at",
    "logo": "https://webconsulting.at/logo.png",
    "sameAs": [
        "https://www.linkedin.com/company/webconsulting",
        "https://github.com/webconsulting"
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+43-1-234567",
        "contactType": "customer service"
    }
}
</script>
)
```

### Breadcrumb Schema (Dynamic)

```typoscript
lib.breadcrumbSchema = COA
lib.breadcrumbSchema {
    10 = TEXT
    10.value = <script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    
    20 = HMENU
    20 {
        special = rootline
        special.range = 0|-1
        1 = TMENU
        1 {
            NO = 1
            NO {
                doNotLinkIt = 1
                stdWrap.cObject = COA
                stdWrap.cObject {
                    10 = TEXT
                    10.value = {"@type":"ListItem","position":
                    20 = TEXT
                    20.data = register:count_HMENU_MENUOBJ
                    30 = TEXT
                    30.value = ,"name":"
                    40 = TEXT
                    40.field = nav_title // title
                    # Inside JSON-LD, avoid htmlSpecialChars (produces &quot; in <script> — invalid JSON). Sanitize in PHP/Fluid or ensure plain-text titles.
                    40.htmlSpecialChars = 0
                    50 = TEXT
                    50.value = ","item":"
                    60 = TEXT
                    60.typolink.parameter.field = uid
                    60.typolink.returnLast = url
                    60.typolink.forceAbsoluteUrl = 1
                    70 = TEXT
                    70.value = "},
                }
            }
        }
    }
    
    30 = TEXT
    30.value = ]}</script>
    30.replacement {
        10.search = ,]}
        10.replace = ]}
    }
}

page.headerData.300 < lib.breadcrumbSchema
```

### Advanced Structured Data with EXT:schema

```bash
# Install schema extension for advanced structured data
ddev composer require brotkrueml/schema
```

```php
<?php
// In a PSR-14 event listener
use Brotkrueml\Schema\Type\TypeFactory;
use Brotkrueml\Schema\Manager\SchemaManager;

#[AsEventListener]
final class AddSchemaListener
{
    public function __construct(
        private readonly TypeFactory $typeFactory,
        private readonly SchemaManager $schemaManager,
    ) {}

    public function __invoke(SomeEvent $event): void
    {
        $organization = $this->typeFactory->create('Organization')
            ->setProperty('name', 'My Company')
            ->setProperty('url', 'https://example.com');
        
        $this->schemaManager->addType($organization);
    }
}
```

## 7. Performance SEO

### Core Web Vitals Optimization

```typoscript
# Preload critical resources
page.headerData.50 = TEXT
page.headerData.50.value (
<link rel="preload" href="/typo3conf/ext/site_package/Resources/Public/Fonts/raleway.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
)

# Lazy load images (built-in TYPO3 v14)
lib.contentElement {
    settings {
        media {
            lazyLoading = lazy
        }
    }
}
```

### Image Optimization (TYPO3 v14)

```php
// config/system/additional.php
$GLOBALS['TYPO3_CONF_VARS']['GFX']['processor_allowUpscaling'] = false;

// WebP is automatically generated in TYPO3 v14 when supported
```

> **Responsive images:** configure image processing via your site package, `fluid_styled_content`, and FAL — there is no stable Core TypoScript path `tt_content.image.settings.responsive_image_rendering`; avoid copy-pasting fabricated keys.

## 8. SEO Checklist

### Page Level

- [ ] Unique `<title>` with primary keyword (50-60 chars)
- [ ] Meta description with call-to-action (150-160 chars)
- [ ] Single H1 per page containing primary keyword
- [ ] Structured heading hierarchy (H1 > H2 > H3)
- [ ] Alt text on all images
- [ ] Internal links with descriptive anchor text
- [ ] External links with `rel="noopener"` on `target="_blank"`

### Technical

- [ ] XML sitemap submitted to Search Console
- [ ] robots.txt properly configured
- [ ] Canonical tags present
- [ ] hreflang tags for multi-language
- [ ] HTTPS enforced
- [ ] Mobile-friendly (responsive)
- [ ] Page speed < 3 seconds
- [ ] Core Web Vitals passing

### Content

- [ ] Unique content per page
- [ ] Keywords naturally integrated
- [ ] Fresh, regularly updated content
- [ ] Structured data where applicable

## 9. SEO Extensions (TYPO3 v14)

### Recommended Extensions

| Extension | Purpose | TYPO3 v14 Support |
|-----------|---------|-----------------|
| `typo3/cms-seo` | Core SEO functionality | ✓ |
| `yoast-seo-for-typo3/yoast_seo` | Content analysis (historical) | **Not for v14** — Packagist releases target up to **TYPO3 10.x** only; do **not** list as v14-compatible |
| `brotkrueml/schema` | Advanced structured data | ✓ (verify `require.typo3/cms-core` on Packagist) |
| `b13/seo_basics` | Legacy package (last targets old TYPO3) — **do not** treat as TYPO3 v14 default; prefer `typo3/cms-seo` |

> **Yoast SEO for TYPO3:** If you need readability scoring on v14, use Core/`cms-seo` features, `brotkrueml/schema`, or another extension that **explicitly** declares `typo3/cms-core: ^14` on Packagist — do not rely on `yoast_seo` without confirming constraints.

### Schema Extension

```bash
ddev composer require brotkrueml/schema
ddev typo3 extension:setup -e schema
```

Features:
- Type-safe schema.org implementation
- WebPage, Organization, Article types
- Event and Product schemas

## 10. Monitoring & Analytics

### Google Search Console Integration

1. Verify domain ownership
2. Submit sitemap: `https://example.com/sitemap.xml`
3. Monitor crawl errors
4. Check Core Web Vitals

### Analytics Setup (GDPR Compliant)

```typoscript
# Conditional Google Analytics (with consent)
[{$plugin.tx_cookie.googleAnalyticsConsent} == 1]
page.headerData.1000 = TEXT
page.headerData.1000.value (
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXX', { 'anonymize_ip': true });
</script>
)
[END]
```

## v14-Only Changes

> The following SEO changes apply **exclusively to TYPO3 v14**.

### Sitemap GET Parameters Namespaced **[v14 only]**

Sitemap GET parameters use the **`tx_seo[...]`** namespace (see [Breaking: #104422](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-104422-SeoParameterNamespace.html)). Update route enhancers and templates that still expect flat `sitemap` / `page` arguments.

### Fluid Page Meta & Title ViewHelpers **[v14 only]**

New ViewHelpers for setting page meta tags and titles directly from Fluid templates:

```html
<!-- Set page title from Fluid -->
<f:page.title>{article.title} - My Site</f:page.title>

<!-- Set meta tags from Fluid -->
<f:page.meta name="description" content="{article.teaser}" />
<f:page.meta property="og:title" content="{article.title}" />
```

These complement (and can replace) PHP-based `PageTitleProvider` and `MetaTagManager` approaches.

### RecordTitleProvider **[v14 only]**

`RecordTitleProvider` (PageTitle API) ties the browser title to rendered records where configured. Useful for Extbase detail views — confirm the exact registration flags in Core docs for your minor version.

### Regex-Based Slug Replacements **[v14 only]**

Slugs now support **regex-based replacements** (#106072) for advanced URL transformation rules beyond simple character substitution.

### headerData / footerData ViewHelpers **[v14 only]**

Use `<f:page.headerData>` / `<f:page.footerData>` (Fluid / TYPO3 core ViewHelpers) to inject raw head markup such as JSON-LD — confirm availability in your Fluid / core combination.

---

## Credits & Attribution

Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.
