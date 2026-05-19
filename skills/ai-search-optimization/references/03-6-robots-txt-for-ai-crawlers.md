# 6. Robots.txt for AI Crawlers

Continues `ai-search-optimization` from [full guide](full-guide.md).

## 6. Robots.txt for AI Crawlers

### Allowing AI Bots

To be indexed by AI search engines, explicitly allow their crawlers:

```text
# robots.txt - AI Search Optimization

# Standard search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# OpenAI (ChatGPT)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# Perplexity AI
User-agent: PerplexityBot
Allow: /

# Anthropic (Claude)
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /

# Google AI (Gemini)
User-agent: Google-Extended
Allow: /

# Meta AI
User-agent: FacebookBot
Allow: /

# Common Crawl (used by many AI systems)
User-agent: CCBot
Allow: /

# Microsoft/Bing AI
User-agent: Applebot
Allow: /

# Default rule
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

# Sitemap
Sitemap: https://example.com/sitemap.xml
```

### Blocking AI Training While Allowing AI Search (Optional)

Some organizations want to be **cited in AI search results** but don't want their content **used to train AI models**. Here's how:

**Understanding the difference:**

| Bot | What it does | Block = |
|-----|--------------|---------|
| `GPTBot` | Crawls for **training** OpenAI models | Your content won't train future GPT versions |
| `ChatGPT-User` | **Live browsing** when users search | ChatGPT can't cite you in real-time answers |
| `Google-Extended` | Crawls for **training** Gemini AI | Your content won't train Gemini |
| `PerplexityBot` | **Live search** for Perplexity answers | Perplexity can't cite you |
| `CCBot` | Common Crawl - open **training datasets** | Your content won't be in public AI training data |

**Example: Block training, allow live search citations:**

```text
# BLOCK: AI model training (your content won't train future AI)
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

# ALLOW: Real-time AI search (AI can cite you in answers)
User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /
```

> **Note:** Most businesses focused on AI search visibility should **allow all bots** (Section 6 above).
> Only use this approach if you have specific concerns about AI training on your content.

### AI Bot Reference

| Bot Name | Company | Purpose |
|----------|---------|---------|
| GPTBot | OpenAI | Training data & ChatGPT browsing |
| ChatGPT-User | OpenAI | ChatGPT web browsing |
| PerplexityBot | Perplexity | Real-time search & citations |
| ClaudeBot | Anthropic | Training & retrieval |
| anthropic-ai | Anthropic | Claude AI training |
| Google-Extended | Google | Gemini AI training |
| FacebookBot | Meta | Meta AI training |
| CCBot | Common Crawl | Open dataset for AI training |
