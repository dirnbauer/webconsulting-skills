---
name: "typo3-seo"
description: "Configures TYPO3 SEO for EXT:seo, metadata, hreflang, XML sitemaps, robots.txt, canonical URLs, structured data, Core Web Vitals, SEO extensions, and monitoring. Use when working on TYPO3 SEO, sitemap setup, meta tags, robots rules, Open Graph, schema.org, canonical URLs, hreflang, or search visibility."
compatibility: "TYPO3 14.x"
metadata:
  version: "2.0.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 SEO Configuration

> Source: https://github.com/dirnbauer/webconsulting-skills

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
        # Recommended social image: 1200×630 px; add og:image:width / og:image:height when known for faster previews
        
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

Add an **`x-default`** `hreflang` (often the primary market language) in site config when you target international SEO — EXT:seo emits tags from `languages` entries.

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
                        excludedDoktypes = 3,4,6,7,199,254
                        additionalWhere = {#no_index} = 0 AND {#canonical_link} = ''
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
                        # Google largely ignores changefreq/priority — keep for other crawlers; focus on accurate lastmod
                        additionalWhere = {#hidden} = 0 AND {#deleted} = 0
                        pid = 123
                        url {
                            pageId = 45
                            fieldToParameterMap {
                                uid = tx_news_pi1[news]
                            }
                            additionalGetParameters {
                                tx_news_pi1.controller = News
                                tx_news_pi1.action = detail
                            }
                            # Match this with a News route enhancer that maps the namespaced tx_news_pi1 arguments.
                            # Example:
                            # routeEnhancers:
                            #   NewsPlugin:
                            #     type: Extbase
                            #     extension: News
                            #     plugin: Pi1
                            #     routes:
                            #       - routePath: '/{news-title}'
                            #         _controller: 'News::detail'
                            #         _arguments:
                            #           news-title: news
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

Without route enhancers, the underlying page type is usually requested via `?type=1533906435`. The exact child sitemap URLs are generated by TYPO3 from the sitemap index. Do not hardcode `?sitemap=...` URLs unless your routing explicitly maps them.

> **TYPO3 v14:** Per Breaking #104422, sitemap GET parameters are namespaced as `tx_seo[sitemap]` and `tx_seo[page]`. The `PageTypeSuffix` enhancer above maps only the sitemap **page type**. Core keeps sitemap index pagination on **query parameters** by default; a **custom** route enhancer for pretty child URLs is **optional**, must define proper **`aspects`**, and must avoid enhancer keys that clash with Core:

```yaml
  # Optional — NOT shipped by Core; tune routePath + aspects + mappers to your real sitemap segments.
  CustomSitemapPagination:
    type: Simple
    routePath: 'sitemap/{sitemap}/{page}'
    aspects:
      sitemap:
        type: StaticRangeMapper
        start: '0'
        end: '99'
      page:
        type: StaticRangeMapper
        start: '0'
        end: '999'
    defaults:
      page: '0'
    _arguments:
      sitemap: 'tx_seo/sitemap'
      page: 'tx_seo/page'
```

See [references/v14-notes.md](references/v14-notes.md) for the same pattern in context.

> This enhancer is **optional and custom** — Core maps `tx_seo/sitemap` but leaves pagination on query parameters by design. Test thoroughly after adding.

> **Pagination & route enhancers:** Core maps `sitemap.xml` to the SEO page type; **sitemap index pagination stays on query parameters** by design (Core does not ship a ready-made pretty-URL enhancer for `tx_seo/page`). Any **custom** enhancer (e.g. `CustomSitemapPagination` above) is **optional** and must define proper **`aspects`** — do not treat examples as Core defaults.

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


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
