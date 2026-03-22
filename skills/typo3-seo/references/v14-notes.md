# TYPO3 SEO Appendix

## v14-Only Changes

> The following SEO changes apply **exclusively to TYPO3 v14**.

### Sitemap GET Parameters Namespaced **[v14 only]**

Sitemap GET parameters use the **`tx_seo[...]`** namespace (see [Breaking: #104422](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-104422-SeoParameterNamespace.html)). Update route enhancers and templates that still expect flat `sitemap` / `page` arguments.

Configure route enhancers for clean sitemap URLs:

```yaml
# config/sites/<site>/config.yaml
routeEnhancers:
  Sitemap:
    type: PageType
    map:
      sitemap.xml: 1533906435
  SitemapPagination:
    type: Simple
    routePath: '{sitemap}'
    _arguments:
      sitemap: 'tx_seo/sitemap'
      page: 'tx_seo/page'
```

### Fluid Page Meta & Title ViewHelpers **[v14 only]**

New ViewHelpers for setting page meta tags and titles directly from Fluid templates:

```html
<!-- Set page title from Fluid -->
<f:page.title>{article.title} - My Site</f:page.title>

<!-- Set meta tags from Fluid -->
<f:page.meta property="description">{article.teaser}</f:page.meta>
<f:page.meta property="og:title">{article.title}</f:page.meta>
```

These complement (and can replace) PHP-based `PageTitleProvider` and `MetaTagManager` approaches.

### RecordTitleProvider **[v14 only]**

`RecordTitleProvider` (PageTitle API) ties the browser title to rendered records where configured. Useful for Extbase detail views — confirm the exact registration flags in Core docs for your minor version.

### Regex-Based Slug Replacements **[v14 only]**

Slugs now support **regex-based replacements** (#106072) for advanced URL transformation rules beyond simple character substitution.

### headerData / footerData ViewHelpers **[v14 only]**

Use `<f:page.headerData>` / `<f:page.footerData>` (Fluid / TYPO3 core ViewHelpers) to inject raw head markup such as JSON-LD — confirm availability in your Fluid / core combination.
