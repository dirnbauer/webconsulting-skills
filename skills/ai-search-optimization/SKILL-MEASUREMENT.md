---
name: ai-search-optimization-measurement
description: >-
  Measuring AEO/GEO success: KPIs, benchmarks, monitoring tools,
  manual audit protocols, and GA4/Matomo tracking for AI search visibility.
  Use when working with measure aeo, track ai citations, ai visibility audit,
  geo kpis, ai referral traffic.
metadata:
  version: "1.0.0"
  related_skills:
    - ai-search-optimization
    - marketing-skills
---

# Measuring AEO/GEO Success

> **Scope:** KPI frameworks, benchmark data, monitoring tools, analytics setup, and audit protocols
> for tracking AI search visibility across ChatGPT, Perplexity, Google AI Overviews, and other platforms.

## 1. KPI Framework

### Three-Tier KPI Model

Organize AEO/GEO metrics into three tiers of increasing business impact:

#### Tier 1: Visibility Metrics (Leading Indicators)

Track these first to understand your baseline AI search presence.

| KPI | What It Measures | How to Track | Target |
|-----|-----------------|--------------|--------|
| **AI Citation Rate** | % of tracked queries where your content is cited in AI answers | Monitoring tools + manual audit | 8-20% (varies by industry) |
| **Share of Voice** | Your brand's citation frequency relative to competitors | Semrush, SE Ranking | >30% = market leader |
| **Citation Position** | Where your citation appears in the AI answer (1st source, 2nd, etc.) | Manual audit, Otterly.ai | Top-3 position |
| **Query Coverage** | % of target queries where you have any AI visibility | Monthly audit | 60%+ of strategic queries |
| **Platform Coverage** | How many AI platforms cite you (ChatGPT, Perplexity, Google AI, etc.) | Cross-platform testing | Present on 3+ platforms |

#### Tier 2: Competitive Metrics (Context Indicators)

Compare your AI visibility to the competitive landscape.

| KPI | What It Measures | How to Track | Target |
|-----|-----------------|--------------|--------|
| **Competitive Gap** | Queries where competitors are cited but you aren't | Competitor monitoring | Reduce 10% quarterly |
| **Brand Mention Rate** | Unprompted mentions in AI responses (without brand query) | Brand24, manual testing | Upward monthly trend |
| **Sentiment Score** | Positive/negative/neutral context of AI mentions | Brand24, manual classification | >80% positive |
| **Source Authority** | How often you're cited as a primary vs. secondary source | Manual audit | Primary source >50% |

#### Tier 3: Business Impact (Lagging Indicators)

Connect AI visibility to measurable business outcomes.

| KPI | What It Measures | How to Track | Target |
|-----|-----------------|--------------|--------|
| **AI Referral Traffic** | Sessions originating from AI search platforms | GA4/Matomo (see setup below) | Month-over-month growth |
| **AI-Influenced Conversions** | Conversions within AI referral sessions | GA4 conversion tracking | Compare to organic baseline |
| **Brand Search Lift** | Increase in brand name searches correlated with AI visibility | Google Search Console | Positive correlation |
| **Revenue Attribution** | Revenue traceable to AI-referred visitors | GA4 + CRM integration | Growing % of total |

## 2. Benchmark Data by Industry

Industry benchmarks for AI Citation Rate (approximate, based on 2025-2026 data):

| Industry | AI Citation Rate | Share of Voice (Leader) | AI Referral % of Traffic |
|----------|-----------------|-------------------------|--------------------------|
| **B2B SaaS** | 8-12% | 25-35% | 2-5% |
| **Media / Publishing** | 15-20% | 20-30% | 5-10% |
| **E-commerce** | 5-8% | 15-25% | 1-3% |
| **Local Services** | 3-5% | 30-50% (local monopoly) | 1-2% |
| **Healthcare / Finance** | 10-15% (YMYL) | 20-30% | 2-4% |
| **Technology / Developer Tools** | 12-18% | 25-40% | 5-8% |

> **Note:** These benchmarks are derived from early AEO/GEO studies ([Seenos.ai](https://seenos.ai/geo-analytics/kpis-geo-success), [Averi.ai](https://www.averi.ai/how-to/how-to-track-ai-citations-and-measure-geo-success-the-2026-metrics-guide)) and will evolve as the field matures. Use them as directional guidance, not absolute targets.

## 3. Monitoring Tools Comparison

### Commercial Tools

| Tool | Pricing | Platforms Monitored | Key Features | Best For |
|------|---------|---------------------|--------------|----------|
| **[Semrush AI Visibility](https://www.semrush.com/blog/ai-visibility-audit-with-semrush-one/)** | Free (limited) + paid plans | ChatGPT, Gemini, Perplexity | Full AI visibility audit, competitor analysis, daily tracking, mention tracking | Enterprise teams with existing Semrush subscription |
| **[Brand24](https://brand24.com/ai-visibility/)** | From $79/mo | ChatGPT, Perplexity, Claude, Gemini | Multi-platform brand monitoring, sentiment analysis, competitor tracking | Brand reputation monitoring across AI platforms |
| **[Otterly.ai](https://otterly.ai)** | Free tier + paid | ChatGPT, Perplexity, Google AI | Prompt-level tracking, citation source analysis, weekly reports | Agencies tracking multiple client brands |
| **[SE Ranking](https://seranking.com/ai-visibility-tracker.html)** | From $52/mo | Google AI Overviews, ChatGPT, Gemini | Share of voice analysis, position tracking, content gaps | SEO teams wanting AI + traditional metrics |
| **[Gauge](https://www.withgauge.com/resources/top-ai-visibility-tools-by-aeo-improvement-score)** | Free tier | Multiple AI platforms | AEO improvement scoring, before/after comparison | Quick initial assessments |
| **[Keyword.com](https://keyword.com)** | From $69/mo | Google AI Overviews, ChatGPT, Perplexity | Rank tracking with AI visibility, optimization suggestions | Teams already doing keyword tracking |

### Decision Matrix

```
Need enterprise-grade auditing?          → Semrush AI Visibility
Need multi-platform brand monitoring?     → Brand24
Need prompt-level tracking on a budget?   → Otterly.ai (free tier)
Need AI + traditional SEO in one tool?    → SE Ranking
Need quick AEO score?                     → Gauge (free)
Already tracking keywords?               → Keyword.com (add-on)
```

## 4. GA4 Setup for AI Referral Traffic

Track visits originating from AI search platforms in Google Analytics 4.

### Step 1: Identify AI Referral Sources

AI search platforms generate traffic from these referral domains:

| Platform | Referral Domains |
|----------|-----------------|
| **Google AI Overviews** | Appears as organic Google traffic (difficult to separate) |
| **ChatGPT** | `chatgpt.com`, `chat.openai.com` |
| **Perplexity** | `perplexity.ai` |
| **Microsoft Copilot** | `copilot.microsoft.com`, `bing.com` (AI referrals mixed) |
| **Claude** | `claude.ai` |
| **Gemini** | `gemini.google.com` |

### Step 2: Create Custom Channel Group in GA4

1. Navigate to **Admin → Data display → Channel groups**
2. Create a new channel group or modify the default
3. Add a channel called **"AI Search"** with these rules:

```
Source matches regex: chatgpt\.com|chat\.openai\.com|perplexity\.ai|copilot\.microsoft\.com|claude\.ai|gemini\.google\.com
```

### Step 3: Create Exploration Report

1. Go to **Explore → Blank**
2. Add dimensions: **Session source/medium**, **Landing page**
3. Add metrics: **Sessions**, **Conversions**, **Engagement rate**, **Average engagement time**
4. Filter: Source matches regex pattern from Step 2
5. Save as "AI Search Traffic Report"

### Step 4: Set Up Custom Alerts

1. Navigate to **Admin → Custom definitions → Custom alerts**
2. Create alert: "AI Referral Traffic Spike"
3. Condition: Sessions from AI sources increase >50% week-over-week

### GA4 Limitations

- **Google AI Overviews traffic** is extremely difficult to separate from regular Google organic traffic. Google does not provide a distinct referrer for AI Overview clicks.
- **Copilot clicks from Bing** may blend with regular Bing organic traffic.
- Consider using UTM parameters on content specifically promoted in AI-answer contexts.

## 5. TYPO3 Integration: Matomo & GA4

### Matomo Setup for AI Referral Tracking

```php
<?php
// EXT:site_package/Classes/EventListener/AddAiSearchTrackingCode.php

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Page\Event\BeforePageIsResolvedEvent;
use TYPO3\CMS\Core\Page\AssetCollector;

#[AsEventListener(identifier: 'site-package/add-ai-search-tracking')]
final readonly class AddAiSearchTrackingCode
{
    public function __construct(
        private AssetCollector $assetCollector,
    ) {}

    public function __invoke(BeforePageIsResolvedEvent $event): void
    {
        $this->assetCollector->addInlineJavaScript(
            'ai-referral-tracking',
            $this->getTrackingScript(),
            ['defer' => 'defer'],
        );
    }

    private function getTrackingScript(): string
    {
        return <<<'JS'
(function() {
    var aiSources = [
        'chatgpt.com', 'chat.openai.com',
        'perplexity.ai',
        'copilot.microsoft.com',
        'claude.ai',
        'gemini.google.com'
    ];
    var referrer = document.referrer;
    if (!referrer) return;

    var isAiReferral = aiSources.some(function(source) {
        return referrer.indexOf(source) !== -1;
    });

    if (isAiReferral && typeof _paq !== 'undefined') {
        _paq.push(['setCustomDimension', 1, 'AI Search']);
        _paq.push(['trackEvent', 'AI Search', 'Referral', referrer]);
    }
})();
JS;
    }
}
```

### Matomo Custom Dimension Setup

1. In Matomo: **Settings → Custom Dimensions → Visit scope**
2. Create dimension: **"Traffic Source Type"** (Index 1)
3. Use the PSR-14 event listener above to set dimension value to "AI Search" for AI referrals
4. Create a segment: Custom Dimension 1 equals "AI Search"
5. Apply segment to standard reports (pages, conversions, engagement)

### GA4 with TYPO3 via Google Tag Manager

```typoscript
# Include GTM container
page.headerData.999 = TEXT
page.headerData.999.value (
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
)
```

Then configure a **Custom JavaScript Variable** in GTM to detect AI referrers and push to the data layer.

## 6. Manual Audit Protocol

Run this protocol monthly to track AI visibility trends.

### Audit Template

```markdown
# AI Visibility Audit — [Month Year]

## Configuration
- **Brand:** [Your brand/product name]
- **Date:** [Audit date]
- **Auditor:** [Name]
- **Competitors tracked:** [Competitor 1, Competitor 2, Competitor 3]

## Query Set (5 types × 5 queries = 25 queries)

### Type 1: Brand Queries
1. "What is [Your Brand]?"
2. "[Your Brand] reviews"
3. "Is [Your Brand] good for [use case]?"
4. "[Your Brand] pricing"
5. "[Your Brand] alternatives"

### Type 2: Category Queries
1. "Best [your category] in [year]"
2. "Top [your category] for [target audience]"
3. "[your category] comparison"
4. "Which [your category] should I choose?"
5. "[your category] recommendations"

### Type 3: Problem/Solution Queries
1. "How to [task your product solves]"
2. "Best way to [problem you solve]"
3. "[Pain point] solutions for [audience]"
4. "How do I improve [outcome you deliver]?"
5. "Tools for [workflow you support]"

### Type 4: Comparison Queries
1. "[Your Brand] vs [Competitor 1]"
2. "[Your Brand] vs [Competitor 2]"
3. "[Competitor 1] vs [Competitor 2]" (check if you're mentioned)
4. "[Your category]: [Product A] or [Product B]?"
5. "Switch from [Competitor] to [alternative]"

### Type 5: Expert/Authority Queries
1. "[Your expertise area] best practices [year]"
2. "[Industry topic] guide"
3. "[Technical topic] explained"
4. "Latest [industry] trends"
5. "[Your niche] tips for beginners"

## Platforms to Test

| Platform | URL | Method |
|----------|-----|--------|
| ChatGPT | chat.openai.com | New conversation, GPT-4 |
| Perplexity | perplexity.ai | Default search mode |
| Google AI | google.com | Check for AI Overviews |
| Microsoft Copilot | copilot.microsoft.com | Default mode |
| Claude | claude.ai | New conversation |

## Recording Template (per query)

| Field | Value |
|-------|-------|
| Query | |
| Platform | |
| Cited? | Yes / No |
| Citation position | 1st / 2nd / 3rd / Not cited |
| Context | Positive / Neutral / Negative |
| Competitors mentioned | |
| Information accurate? | Yes / Partially / No |
| Source URL cited | |
| Notes / Improvements | |

## Summary Scorecard

| Metric | This Month | Last Month | Trend |
|--------|-----------|------------|-------|
| Total citations | /125 | /125 | ↑↓→ |
| Citation rate | % | % | |
| ChatGPT citations | /25 | /25 | |
| Perplexity citations | /25 | /25 | |
| Google AI citations | /25 | /25 | |
| Copilot citations | /25 | /25 | |
| Claude citations | /25 | /25 | |
| Top-3 positions | /125 | /125 | |
| Positive sentiment | % | % | |
| Competitors outranked | /[total] | /[total] | |
```

### Audit Tips

- **Use incognito/private mode** to avoid personalization bias
- **Log out of all accounts** before testing
- **Test at different times** (AI responses can vary)
- **Screenshot results** for documentation
- **Track the exact query** used (AI systems are sensitive to phrasing)
- **Note response date/time** — AI answers change frequently

## 7. Review Cadence Checklists

### Monthly Review

- [ ] Run manual audit protocol (25 queries × 5 platforms)
- [ ] Review AI referral traffic in GA4/Matomo
- [ ] Compare citation rate to previous month
- [ ] Identify new competitor citations
- [ ] Update content for queries where you lost visibility
- [ ] Check for schema validation errors
- [ ] Verify AI crawler access in server logs

### Quarterly Review

- [ ] Analyze citation rate trends over 3 months
- [ ] Compare Share of Voice against competitors
- [ ] Review AI referral conversion rates vs. organic
- [ ] Update query set based on new business priorities
- [ ] Refresh outdated content flagged in audits
- [ ] Test new AI platforms that emerged
- [ ] Review and update robots.txt for new AI bots
- [ ] Update schema markup for new page types

### Annual Review

- [ ] Comprehensive AI visibility strategy review
- [ ] Benchmark against industry standards
- [ ] ROI analysis: AI visibility investment vs. business outcomes
- [ ] Tool evaluation: assess current monitoring stack
- [ ] Update KPI targets for next year
- [ ] Review competitive landscape shifts
- [ ] Plan content calendar aligned with AI search trends

---

## Resources

- [Seenos.ai: GEO KPIs for 2026](https://seenos.ai/geo-analytics/kpis-geo-success)
- [Averi.ai: How to Track AI Citations and Measure GEO Success](https://www.averi.ai/how-to/how-to-track-ai-citations-and-measure-geo-success-the-2026-metrics-guide)
- [Gauge: Top AI Visibility Tools by AEO Improvement Score](https://www.withgauge.com/resources/top-ai-visibility-tools-by-aeo-improvement-score)
- [Semrush: AI Visibility Audit with Semrush One](https://www.semrush.com/blog/ai-visibility-audit-with-semrush-one/)
- [Brand24: AI Visibility Monitoring](https://brand24.com/ai-visibility/)
- [Glenn Gabe / GSQI: Is AEO/GEO different than SEO?](https://www.gsqi.com/marketing-blog/straight-from-the-ai-source-is-aeo-geo-different-than-seo/)

---

Created by webconsulting.at for the Claude Cursor Skills collection.
