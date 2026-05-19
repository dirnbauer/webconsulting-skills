# 7. Performance SEO

Continues `typo3-seo` from [full guide](full-guide.md).

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
