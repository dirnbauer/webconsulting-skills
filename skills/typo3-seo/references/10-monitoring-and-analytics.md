# 10. Monitoring & Analytics

Continues `typo3-seo` from [full guide](full-guide.md).

## 10. Monitoring & Analytics

### Google Search Console Integration

1. Verify domain ownership
2. Submit sitemap: `https://example.com/sitemap.xml`
3. Monitor crawl errors
4. Check Core Web Vitals

### Analytics Setup (GDPR Compliant)

```typoscript
# Conditional Google Analytics
# Wrap this block in your consent extension's real condition / signal.
page.headerData.1000 = TEXT
page.headerData.1000.value (
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXX');
</script>
)
```
