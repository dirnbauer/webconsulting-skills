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

# OpenAI - model training
User-agent: GPTBot
Allow: /

# OpenAI - ChatGPT Search index (controls visibility in ChatGPT Search)
User-agent: OAI-SearchBot
Allow: /

# Perplexity AI - search index
User-agent: PerplexityBot
Allow: /

# Anthropic (Claude) - model training
User-agent: ClaudeBot
Allow: /

# Anthropic (Claude) - search indexing
User-agent: Claude-SearchBot
Allow: /

# Google AI (Gemini training/grounding)
User-agent: Google-Extended
Allow: /

# Meta AI training
User-agent: Meta-ExternalAgent
Allow: /

# Common Crawl (used by many AI systems)
User-agent: CCBot
Allow: /

# Apple (Siri, Spotlight, Apple Intelligence)
User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
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
| `GPTBot` | Crawls for **training** OpenAI models (training only) | Your content won't train future GPT versions |
| `OAI-SearchBot` | Indexes content for **ChatGPT Search** | You won't appear or be cited in ChatGPT Search results |
| `ChatGPT-User` | **User-initiated** page fetches (not bound by robots.txt) | No reliable effect - it fetches on direct user request |
| `Google-Extended` | Crawls for **training/grounding** Gemini AI | Your content won't train Gemini (Search inclusion and ranking are unaffected) |
| `PerplexityBot` | Builds Perplexity's **search index** (not used for model training) | You're removed from Perplexity's search index - but `Perplexity-User` can still fetch pages on user request |
| `CCBot` | Common Crawl - open **training datasets** | Your content won't be in public AI training data |

**Example: Block training, allow AI search citations:**

```text
# BLOCK: AI model training (your content won't train future AI)
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: CCBot
Disallow: /

# ALLOW: AI search indexing (AI can cite you in answers)
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-SearchBot
Allow: /
```

> User-initiated fetchers (`ChatGPT-User`, `Claude-User`, `Perplexity-User`, `Meta-ExternalFetcher`)
> visit pages only when a user asks and are generally **not bound by robots.txt** -
> robots.txt rules for them are informational at best.

> **Note:** Most businesses focused on AI search visibility should **allow all bots** (Section 6 above).
> Only use this approach if you have specific concerns about AI training on your content.

### AI Bot Reference

| Bot Name | Company | Purpose |
|----------|---------|---------|
| GPTBot | OpenAI | AI model training (training only) |
| OAI-SearchBot | OpenAI | ChatGPT Search indexing & citations |
| ChatGPT-User | OpenAI | User-initiated fetches (not bound by robots.txt) |
| PerplexityBot | Perplexity | Search index (not used for model training) |
| Perplexity-User | Perplexity | User-requested fetches (generally ignores robots.txt) |
| ClaudeBot | Anthropic | AI model training |
| Claude-SearchBot | Anthropic | Search indexing |
| Claude-User | Anthropic | User-initiated fetches |
| anthropic-ai / Claude-Web | Anthropic | Deprecated legacy tokens (superseded by the three above) |
| Google-Extended | Google | Gemini training/grounding (does not affect Search inclusion or ranking) |
| Meta-ExternalAgent | Meta | AI training |
| Meta-ExternalFetcher | Meta | User-requested link fetches |
| Applebot / Applebot-Extended | Apple | Siri, Spotlight & Apple Intelligence |
| CCBot | Common Crawl | Open dataset for AI training |
