# 5. Content Freshness Strategy

Continues `ai-search-optimization` from [full guide](full-guide.md).

## 5. Content Freshness Strategy

### Update Frequency by Platform

| Platform | Freshness Preference | Recommended Update Cycle |
|----------|---------------------|--------------------------|
| Perplexity AI | Very high | Every 2-3 days for trending topics |
| ChatGPT Search | High | Weekly updates |
| Google AI Overviews | Moderate | Monthly refresh |
| Bing Copilot | Moderate | Monthly refresh |

### Content Refresh Protocol

```markdown
## Content Freshness Checklist

### Weekly Tasks
- [ ] Update statistics with latest data
- [ ] Refresh screenshots and examples
- [ ] Add new developments or news
- [ ] Update "Last modified" timestamp

### Monthly Tasks
- [ ] Review and update all factual claims
- [ ] Add new sections for emerging topics
- [ ] Update broken links
- [ ] Refresh expert quotes

### Quarterly Tasks
- [ ] Comprehensive content audit
- [ ] Competitive analysis
- [ ] Restructure based on query trends
- [ ] Update all schema markup
```

### Visible Timestamps

```html
<article>
    <header>
        <h1>Article Title</h1>
        <div class="article-meta">
            <time datetime="2025-01-15" itemprop="datePublished">
                Published: January 15, 2025
            </time>
            <time datetime="2025-01-15" itemprop="dateModified">
                Last Updated: January 15, 2025
            </time>
        </div>
    </header>
    <!-- Content -->
</article>
```
