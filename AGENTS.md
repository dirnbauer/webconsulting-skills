# Available Agent Skills

A curated collection of Agent Skills for AI-augmented software development. Skills cover web development, video creation, security auditing, legal compliance, and enterprise software engineering.

> **📢 Early Adopter Notice:** We encourage you to use these skills! Expect occasional updates as 
> Anthropic, Cursor, and webconsulting evolve their platforms. Always review AI-generated code.
> See [README](README.md) for details.

> **TYPO3 Skills:** All TYPO3 skills support v13.x and v14.x (v14 preferred). Code examples work on both versions simultaneously.

> **PHP 8.4 & Content Blocks:** Most TYPO3 skills include supplement files:
> - `SKILL-PHP84.md` - PHP 8.4 specific patterns and migration
> - `SKILL-CONTENT-BLOCKS.md` - Content Blocks integration and migration

---

## Acknowledgements

We are deeply grateful to **[Netresearch DTT GmbH](https://www.netresearch.de/)** for their
outstanding contributions to the TYPO3 community. Their excellent methodology and best practices
have been invaluable in shaping these guidelines.

The majority of skills in this repository are derived from Netresearch's open-source skill
repositories. We recommend checking their original repositories for the latest updates:
https://github.com/netresearch

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection

---

We also thank **[Supabase](https://supabase.com/)** for their excellent Postgres best practices
and AI agent skills. The `postgres-best-practices` skill is adapted from their open-source
repository: https://github.com/supabase/agent-skills

**Copyright (c) Supabase** - Postgres performance optimization guidelines  
See: [Postgres Best Practices for AI Agents](https://supabase.com/blog/postgres-best-practices-for-ai-agents)

---

We also thank **[Corey Haines](https://coreyhaines.com/)** for his excellent marketing skills
collection. The `marketing-skills` skill is adapted from his open-source repository:
https://github.com/coreyhaines31/marketingskills

**Copyright (c) Corey Haines** - Marketing frameworks and best practices  
See: [Conversion Factory](https://conversionfactory.co/) | [Swipe Files](https://swipefiles.com/)

---

We also thank **[Stevy Smith](https://github.com/stevysmith)** for the excellent OG Image skill.
The `og-image` skill is adapted from their open-source repository:
https://github.com/stevysmith/og-image-skill

**Copyright (c) Stevy Smith** - OG Image generation and social meta tag configuration

---

We also thank **[Vercel Engineering](https://vercel.com)** for their excellent React and Next.js 
performance optimization guidelines. The `react-best-practices` and `web-design-guidelines` skills 
are adapted from their open-source repository:
https://github.com/vercel-labs/agent-skills

**Copyright (c) Vercel, Inc.** - React and Next.js performance optimization (MIT License)

---

We also thank **[Firecrawl](https://firecrawl.dev/)** by Mendable AI for their excellent web
scraping and research tools. The `firecrawl` skill provides LLM-optimized content extraction.

**Copyright (c) Mendable AI** - Web scraping and content extraction  
See: [Firecrawl](https://firecrawl.dev/) | [GitHub](https://github.com/mendableai/firecrawl)

---

We also thank **[Anthropic](https://anthropic.com)** for their excellent document processing, 
frontend design, and skill creator skills. The `document-processing`, `frontend-design`, and 
`skill-creator` skills are adapted from their open-source repository:
https://github.com/anthropics/skills

**Copyright (c) Anthropic** - Document processing, frontend design, and skill creation (Apache-2.0 / MIT License)

---

We also thank **[ehmo](https://github.com/ehmo)** for the excellent platform design skills collection.
The platform design skills (Android, iOS, iPadOS, macOS, tvOS, visionOS, watchOS, Web) are adapted 
from their open-source repository:
https://github.com/ehmo/platform-design-skills

**Copyright (c) platform-design-skills** - Apple HIG and Material Design guidelines (MIT License)

---

We also thank **[AITYTech](https://github.com/aitytech)** for their excellent AgentKits Marketing 
skills collection. The `cro-funnel`, `programmatic-seo`, `launch-strategy`, and `ab-testing` skills 
are adapted from their open-source repository:
https://github.com/aitytech/agentkits-marketing

**Copyright (c) AITYTech** - Enterprise-grade AI marketing automation (MIT License)  
See: [AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)

---

## Skills Overview

| Skill | Description | Version | Triggers |
|-------|-------------|---------|----------|
| **Video & Animation** | | | |
| `remotion-best-practices` | Video creation in React with Remotion | 1.0.0 | remotion, video, react, animation, composition |
| **Security & Enterprise** | | | |
| `security-audit` | Security audit patterns (OWASP, XXE, SQLi, XSS, CVSS) | 1.0.0 | security, audit, owasp, vulnerabilities |
| `security-incident-reporting` | NIST/SANS incident reports, DDoS post-mortem, CVE correlation | 1.0.0 | incident report, post-mortem, ddos, forensics |
| `security-incident-reporting/TYPO3` | TYPO3 forensics, Security Team communication, PGP templates | 1.0.0 | typo3 incident, typo3 hack, security team |
| `deepfake-detection` | Multimodal media authentication, PRNU/IGH/DQ forensics, GAN detection | 1.0.0 | deepfake, media forensics, fake detection, synthetic media |
| `enterprise-readiness` | OpenSSF, SLSA, supply chain security, quality gates | 1.0.0 | enterprise, openssf, slsa, security |
| `readiness-report` | AI agent readiness assessment (9 pillars, 5 maturity levels) | 1.0.0 | /readiness-report, agent readiness, codebase maturity |
| `ai-search-optimization` | AEO/GEO for AI search visibility with TYPO3, MD/MDX, and llms.txt | 1.0.0 | aeo, geo, ai search, chatgpt, perplexity, llms.txt |
| **Database** | | | |
| `postgres-best-practices` | Postgres performance, RLS, indexes, connection pooling (Supabase) | 1.0.0 | postgres, sql, database, query, index, rls |
| `postgres-best-practices/SUPABASE` | Supabase auth.uid(), RLS patterns, Edge Functions, MCP | 1.0.0 | supabase, auth.uid, edge-functions, supabase-mcp |
| **Marketing** | | | |
| `marketing-skills` | CRO, copywriting, SEO, pricing, psychology (Corey Haines) | 1.0.0 | marketing, cro, conversion, landing page, funnel |
| `marketing-skills/CRO` | Page conversion rate optimization framework | 1.0.0 | cro, optimize page, page not converting |
| `marketing-skills/COPYWRITING` | Headlines, CTAs, page structure, copy formulas | 1.0.0 | copywriting, headline, rewrite, cta |
| `marketing-skills/SEO` | Technical SEO, on-page SEO, content quality audit | 1.0.0 | seo audit, not ranking, technical seo |
| `marketing-skills/PSYCHOLOGY` | 70+ mental models for marketing and persuasion | 1.0.0 | psychology, mental model, persuasion, bias |
| `marketing-skills/PRICING` | Pricing tiers, value metrics, freemium vs trial | 1.0.0 | pricing, tiers, freemium, monetization |
| **CRO & Growth (AgentKits)** | | | |
| `cro-funnel` | Full-funnel CRO: form, signup, onboarding, popup, paywall | 1.0.0 | cro funnel, form cro, signup flow, onboarding, paywall |
| `programmatic-seo` | SEO pages at scale with templates and data | 1.0.0 | programmatic seo, template pages, directory, location pages |
| `launch-strategy` | Product launches, Product Hunt, go-to-market | 1.0.0 | product launch, product hunt, gtm, beta launch |
| `ab-testing` | A/B test design, sample size, statistical significance | 1.0.0 | ab test, split test, experiment, hypothesis |
| **PHP & Tools** | | | |
| `php-modernization` | PHP 8.x patterns, PHPStan level 10, DTOs, enums | 1.0.0 | php, modernization, phpstan, rector |
| `php-modernization/PHP84` | PHP 8.4 features: property hooks, asymmetric visibility | 1.0.0 | php 8.4, property hooks |
| `cli-tools` | CLI tool management and auto-installation | 1.0.0 | cli, tools, installation |
| `context7` | Library documentation lookup via REST API | 1.0.0 | documentation, api, libraries |
| `firecrawl` | LLM-optimized web scraping, search, and research | 1.0.0 | scrape, crawl, search web, research, fetch url |
| `skill-creator` | Guide for creating and packaging effective Agent Skills (Anthropic) | 1.0.0 | create skill, new skill, skill creator, package skill, SKILL.md |
| **Frontend & Design** | | | |
| `webconsulting-branding` | webconsulting.at design system, colors, typography, MDX | 1.0.0 | frontend, design, branding, ui |
| `ui-design-patterns` | Practical UI design patterns, accessibility, usability | 1.1.0 | ui, design, accessibility, usability |
| `frontend-design` | Distinctive UI aesthetics, anti-AI-slop patterns, creative interfaces | 1.0.0 | frontend, design, creative, beautiful, distinctive, aesthetics |
| `web-design-guidelines` | Interface review, accessibility audit, WCAG, ARIA, semantic HTML | 1.0.0 | web design, accessibility, a11y, wcag, aria, semantic html |
| `og-image` | Social preview images (Open Graph), meta tags, Twitter cards | 1.0.0 | og-image, open graph, social preview, twitter card, meta tags |
| `react-best-practices` | React/Next.js performance optimization from Vercel (57 rules) | 1.0.0 | react, next.js, performance, optimization, bundle, waterfalls |
| **Platform Design** | | | |
| `android-design` | Material Design 3, Jetpack Compose, dynamic color, navigation | 1.0.0 | android, material design, jetpack compose, material you |
| `ios-design` | Apple HIG for iPhone, SwiftUI, Dynamic Type, Dark Mode | 1.0.0 | ios, iphone, swiftui, uikit, dynamic type |
| `ipados-design` | Apple HIG for iPad, multitasking, keyboard, pointer support | 1.0.0 | ipad, ipados, split view, stage manager, sidebar |
| `macos-design` | Apple HIG for Mac, menu bar, toolbars, keyboard shortcuts | 1.0.0 | macos, mac app, appkit, menu bar, toolbar |
| `tvos-design` | Apple HIG for Apple TV, focus navigation, 10-foot UI | 1.0.0 | tvos, apple tv, siri remote, focus navigation |
| `visionos-design` | Apple HIG for Vision Pro, spatial UI, eye/hand input | 1.0.0 | visionos, vision pro, spatial computing, realitykit |
| `watchos-design` | Apple HIG for Apple Watch, complications, glanceable UI | 1.0.0 | watchos, apple watch, complications, digital crown |
| `web-platform-design` | WCAG 2.2, responsive design, forms, typography, i18n | 1.0.0 | wcag, web platform, responsive, accessibility, i18n |
| **Documents & Office** | | | |
| `document-processing` | PDF, DOCX, PPTX, XLSX creation, editing, and analysis | 1.0.0 | pdf, docx, word, pptx, powerpoint, xlsx, excel, document |
| **Legal & Compliance** | | | |
| `legal-impressum` | Austrian Impressum for all Gesellschaftsformen (ECG, MedienG) | 1.0.0 | impressum, legal notice, austria, offenlegung |
| `legal-impressum/GERMANY` | German Impressum (DDG, MStV) for all Rechtsformen | 1.0.0 | impressum, germany, DDG |
| `legal-impressum/EU` | EU eCommerce Directive compliance | 1.0.0 | impressum, eu, ecommerce directive |
| `legal-impressum/WORLD` | International requirements (UK, CH, US) | 1.0.0 | impressum, international, uk, switzerland |
| **TYPO3 CMS** | | | |
| `typo3-content-blocks` | Content Elements & Record Types with single source of truth config | 1.0.0 | content-blocks, content-element, record-type, irre |
| `typo3-datahandler` | Expert guidance on DataHandler for transactional database operations | 2.0.0 | database, datahandler, tcemain, records |
| `typo3-ddev` | TYPO3 local development with DDEV, multi-version testing | 2.0.0 | ddev, local, development, docker |
| `typo3-testing` | Unit, functional, E2E, architecture, mutation testing | 1.0.0 | testing, phpunit, playwright, phpat |
| `typo3-conformance` | Extension standards compliance checker | 1.0.0 | conformance, standards, quality |
| `typo3-docs` | Documentation using docs.typo3.org standards | 1.0.0 | documentation, rst, docs |
| `typo3-core-contributions` | TYPO3 Core contribution workflow (Gerrit, Forge) | 1.0.0 | core, contributions, gerrit, forge |
| `typo3-rector` | TYPO3 upgrade patterns using Rector for dual-version support | 2.0.0 | rector, upgrade, migration, refactoring |
| `typo3-update` | TYPO3 v13/v14 dual-version development guide | 2.0.0 | update, upgrade, v13, v14 |
| `typo3-extension-upgrade` | Systematic extension upgrades with Rector, Fractor, PHPStan | 1.0.0 | extension, upgrade, fractor |
| `typo3-security` | Security hardening checklist and best practices | 2.0.0 | security, hardening, permissions |
| `typo3-seo` | SEO configuration with EXT:seo, sitemaps, meta tags | 2.0.0 | seo, sitemap, meta, robots |
| `typo3-powermail` | Powermail 13+ forms, finishers, validators, events, spam shield | 1.0.0 | powermail, mailform, form extension, tx_powermail |
| `typo3-powermail/CONDITIONS` | Conditional field/page visibility with powermail_cond 13+ | 1.0.0 | powermail_cond, conditional fields, show hide fields |
| `typo3-powermail/PHP84` | PHP 8.4 patterns for Powermail finishers, validators, conditions | 1.0.0 | powermail php 8.4, powermail property hooks |
| `typo3-records-list-types` | Grid, Compact, Teaser, custom view modes for TYPO3 v14 Records module | 1.0.0 | records list types, grid view backend, compact view, teaser view, custom view type, backend record cards |
| `typo3-records-list-types/CUSTOM-VIEWS` | Custom view types with TSconfig + Fluid (zero PHP) | 1.0.0 | custom view type, records list template, kanban view, timeline view |

## Skill Categories

### Video & Animation
- **remotion-best-practices**: Video creation in React with Remotion, animations, transitions, audio

### Security & Enterprise
- **security-audit**: Deep security audits aligned with OWASP Top 10
- **security-incident-reporting**: Post-incident documentation drawing from NIST/SANS, DDoS post-mortem, CVE correlation
  - `SKILL-TYPO3.md`: TYPO3 forensics, Security Team communication, PGP-encrypted vulnerability reports
- **deepfake-detection**: Multimodal media authentication, synthetic media forensics (PRNU, IGH, DQ, GAN fingerprints)
- **enterprise-readiness**: OpenSSF Scorecard, SLSA, supply chain security
- **readiness-report**: AI agent readiness assessment across 9 technical pillars and 5 maturity levels
- **ai-search-optimization**: AEO/GEO for AI search (schema.org, robots.txt, llms.txt, TYPO3, MD/MDX)

### Database
- **postgres-best-practices**: Postgres performance optimization from Supabase
  - Query performance, indexes, connection pooling
  - Row Level Security (RLS) patterns
  - Schema design, data types, partitioning
  - Concurrency, locking, queue processing
  - `SKILL-SUPABASE.md`: auth.uid(), Edge Functions, MCP server, Realtime

### Marketing
- **marketing-skills**: Marketing skills from Corey Haines
  - `SKILL-CRO.md`: Page conversion rate optimization
  - `SKILL-COPYWRITING.md`: Headlines, CTAs, page structure
  - `SKILL-SEO.md`: Technical and on-page SEO audit
  - `SKILL-PSYCHOLOGY.md`: 70+ mental models for marketing
  - `SKILL-PRICING.md`: Pricing strategy, tiers, value metrics

### CRO & Growth (AgentKits Marketing)
- **cro-funnel**: Full-funnel Conversion Rate Optimization from AgentKits
  - Form CRO: Lead capture, contact forms, demo requests
  - Signup Flow CRO: Registration, account creation, trial activation
  - Onboarding CRO: Post-signup activation, time-to-value, aha moment
  - Popup CRO: Modals, exit intent, slide-ins, email capture
  - Paywall CRO: In-app paywalls, upgrade screens, freemium conversion
- **programmatic-seo**: Build SEO pages at scale with templates and data
  - 12 playbooks: Templates, Curation, Comparisons, Locations, Personas, Integrations, Glossary
  - URL structure best practices (subfolders > subdomains)
  - Unique value per page, avoid thin content penalties
- **launch-strategy**: Product launches and go-to-market strategies
  - ORB Framework: Owned, Rented, Borrowed channels
  - Five-phase launch: Internal → Alpha → Beta → Early Access → Full
  - Product Hunt launch strategy and checklist
  - Post-launch product marketing
- **ab-testing**: A/B test design and experimentation
  - Hypothesis framework and documentation
  - Sample size calculation and duration planning
  - Metrics selection: primary, secondary, guardrail
  - Statistical analysis and result interpretation

### PHP & Tools
- **php-modernization**: PHP 8.x features, type safety, PHPStan level 10
  - `SKILL-PHP84.md`: PHP 8.4 property hooks, asymmetric visibility, new array functions
- **cli-tools**: CLI tool management, auto-installation on "command not found"
- **context7**: Library documentation lookup via Context7 REST API
- **firecrawl**: LLM-optimized web scraping, search, and research
  - Clean markdown output optimized for LLM context windows
  - JavaScript rendering, parallel scraping, time/location filters
- **skill-creator**: Guide for creating effective Agent Skills (from Anthropic)
  - `scripts/init_skill.py`: Initialize new skill from template
  - `scripts/package_skill.py`: Package and validate skill for distribution
  - `references/workflows.md`: Sequential and conditional workflow patterns
  - `references/output-patterns.md`: Template and example output patterns

### Frontend & Design
- **webconsulting-branding**: Design tokens, colors, typography, MDX components
- **ui-design-patterns**: Visual hierarchy, spacing, color, typography, accessibility
- **frontend-design**: Distinctive UI aesthetics that avoid generic "AI slop"
  - Bold aesthetic directions: brutalist, maximalist, luxury, editorial
  - Creative typography pairings (avoid Inter/Roboto/Arial)
  - Color palettes with dominant + accent approach
  - Motion design for high-impact moments
  - Anti-patterns checklist
- **web-design-guidelines**: Interface review for accessibility and usability
  - WCAG 2.1 AA compliance checking
  - Semantic HTML validation
  - ARIA patterns and keyboard navigation
  - Responsive design and touch targets
  - Focus states and color contrast
- **og-image**: Social media preview images (Open Graph) and meta tag configuration
  - Creates `/og-image` route matching project design system
  - Screenshots at 1200x630 dimensions
  - Configures og:image, twitter:card, theme-color meta tags
  - Supports Next.js, Vite, Astro, Remix, plain HTML
- **react-best-practices**: React and Next.js performance optimization from Vercel
  - 57 rules across 8 categories, prioritized by impact
  - Eliminating waterfalls (async/await, Promise.all, Suspense)
  - Bundle size optimization (barrel imports, dynamic imports)
  - Server-side performance (React.cache, parallel fetching)
  - Re-render optimization (memo, useTransition, refs)

### Platform Design
- **android-design**: Material Design 3 and Android platform guidelines
  - Dynamic color (Material You) with static fallback
  - Navigation Bar, Navigation Rail, Navigation Drawer
  - Window size classes, edge-to-edge display
  - Accessibility: 48dp touch targets, TalkBack support
- **ios-design**: Apple Human Interface Guidelines for iPhone
  - 44pt touch targets, safe areas, thumb zone placement
  - Tab bar navigation, NavigationStack, large titles
  - Dynamic Type, semantic system colors, Dark Mode
  - VoiceOver, Bold Text, Reduce Motion support
- **ipados-design**: Apple Human Interface Guidelines for iPad
  - Adaptive layouts, Split View, Slide Over, Stage Manager
  - Sidebar navigation, keyboard shortcuts (Cmd+key)
  - Pointer/trackpad support, hover effects, right-click menus
  - Drag and drop between apps, Apple Pencil support
- **macos-design**: Apple Human Interface Guidelines for Mac
  - Complete menu bar with keyboard shortcuts
  - Resizable windows, fullscreen, multiple windows
  - Toolbars, sidebars, source list style
  - Full keyboard navigation, vibrancy, Dark Mode
- **tvos-design**: Apple Human Interface Guidelines for Apple TV
  - Focus-based navigation with parallax effects
  - 10-foot UI: 29pt minimum text, high contrast
  - Siri Remote: swipe, click, Menu, Play/Pause
  - Top Shelf content, media playback controls
- **visionos-design**: Apple Human Interface Guidelines for Vision Pro
  - Spatial layout: content at 1-2m, never behind user
  - Look-and-pinch interaction, 60pt minimum targets
  - Windows with glass material, volumes, immersive spaces
  - Progressive immersion, world-anchored UI
- **watchos-design**: Apple Human Interface Guidelines for Apple Watch
  - Glanceable design: 2-second comprehension
  - Digital Crown scrolling with haptic detents
  - Complications: multiple families, fresh data
  - Always On display, workout features
- **web-platform-design**: Comprehensive web platform design guidelines
  - WCAG 2.2 accessibility, semantic HTML, ARIA patterns
  - Responsive design, container queries, touch targets
  - Forms, typography, performance optimization
  - Dark mode, animations, internationalization (RTL)

### Documents & Office
- **document-processing**: PDF, DOCX, PPTX, XLSX creation, editing, and analysis
  - PDF: text extraction, merge/split, OCR, watermarks, forms
  - DOCX: pandoc conversion, docx-js creation, tracked changes
  - PPTX: markitdown extraction, PptxGenJS creation, thumbnails
  - XLSX: pandas analysis, openpyxl formulas, financial models

### Legal & Compliance
- **legal-impressum**: Austrian Impressum for all company types (Gesellschaftsformen)
  - `SKILL-GERMANY.md`: German DDG/MStV requirements
  - `SKILL-EU.md`: EU eCommerce Directive compliance
  - `SKILL-WORLD.md`: International (UK, Switzerland, USA)

### TYPO3 CMS
- **typo3-content-blocks**: Content Elements & Record Types with single YAML config (no duplicate TCA/SQL)
- **typo3-datahandler**: Safe database operations via DataHandler API with PSR-14 events
- **typo3-ddev**: Local development environment setup with multi-version testing
- **typo3-testing**: Comprehensive testing (unit, functional, E2E, architecture, mutation)
- **typo3-conformance**: Extension quality assessment and standards compliance
- **typo3-docs**: Official documentation standards with RST and TYPO3 directives
- **typo3-core-contributions**: Contributing to TYPO3 Core via Gerrit and Forge
- **typo3-rector**: Automated code refactoring with Rector for dual-version support
- **typo3-update**: Version migration and compatibility strategies for v13/v14
- **typo3-extension-upgrade**: Systematic extension upgrades with Rector, Fractor, PHPStan
- **typo3-security**: Production hardening checklist for v13/v14
- **typo3-seo**: Search engine optimization with EXT:seo
- **typo3-powermail**: Powermail 13+ form extension (finishers, validators, events, spam shield, emails)
  - `SKILL-CONDITIONS.md`: Conditional field/page visibility with powermail_cond
  - `SKILL-PHP84.md`: PHP 8.4 patterns for finishers, validators, conditions (property hooks, asymmetric visibility)
  - `SKILL-EXAMPLES.md`: Multi-step shop form with Austrian legal types, conditions, translations, DDEV SQL + DataHandler CLI
- **typo3-records-list-types**: Grid, Compact, Teaser, and custom view modes for TYPO3 v14 Records module
  - `SKILL-CUSTOM-VIEWS.md`: Custom view types (zero PHP), template variables, real-world examples, PSR-14 registration

## TYPO3 Skill Supplements

TYPO3 skills include optional supplement files for PHP 8.4 and Content Blocks:

### PHP 8.4 Supplements (`SKILL-PHP84.md`)

Cover PHP 8.4 specific patterns: property hooks, asymmetric visibility, new array functions, `#[\Deprecated]` attribute.

### Content Blocks Supplements (`SKILL-CONTENT-BLOCKS.md`)

Cover Content Blocks integration: using Content Blocks with the skill's domain, migration from classic TCA/SQL.

## Usage

Skills are automatically loaded by Claude when relevant keywords are detected in your query. You can also explicitly request a skill:

> "Using the typo3-datahandler skill, help me create a content element programmatically."

### Quick Examples by Category

**🏗️ Project Setup (typo3-ddev)**
- "Set up TYPO3 v14 with DDEV, Redis, and Xdebug"
- "Configure multi-site with shared codebase"
- "Import production database and sanitize sensitive data"
- "Docker production setup with nginx and PHP-FPM"

**📦 Content Blocks (typo3-content-blocks)**
- "Create a hero banner Content Element with CTA button"
- "Create a team members Record Type with Extbase naming"
- "Build an accordion with Collection items"
- "FAQ with categories using Record Type relations"
- "Image slider with IRRE and max 10 slides"
- "Migrate my classic TCA/SQL extension to Content Blocks"
- "Convert this TCA config to Content Blocks YAML"
- "Keep existing column names during migration"
- "Revert Content Block to classic TCA/SQL format"
- "Generate TCA PHP from Content Blocks config.yaml"
- "Remove Content Blocks dependency safely"

**🔧 Extension Development (typo3-datahandler, typo3-update)**
- "CRUD operations with DataHandler and transactions"
- "Extbase controller with list/show actions for v13+v14"
- "PSR-14 event listener with AsEventListener attribute"
- "Custom repository with QueryBuilder methods"
- "Scheduler task with progress reporting"
- "Backend module with list view and bulk actions"
- "REST API with authentication and rate limiting"
- "CLI command with progress bar and dry-run mode"

**🗂️ TCA & FlexForm (typo3-datahandler)**
- "TCA select field with icons and default value"
- "TCA inline (IRRE) with sorting and appearance"
- "FlexForm with tabs and database record selection"
- "Custom route enhancers for SEO-friendly URLs"

**📁 Files & Media (typo3-datahandler)**
- "Process uploaded images: resize, convert to WebP"
- "Extract and store EXIF metadata from images"
- "Custom image processor with watermark"

**🌐 Localization (typo3-update)**
- "Multi-language setup with fallback types"
- "XLIFF translations with pluralization"
- "Sync translations from Phrase/Lokalise"

**📧 Forms & Email (typo3-datahandler)**
- "EXT:form custom finisher for CRM integration"
- "Custom validator for email domain whitelist"
- "Styled HTML email template with Fluid"

**⚡ Performance (typo3-ddev, typo3-security)**
- "Redis caching with cache groups and tags"
- "Cache invalidation strategy with tags"
- "Database query optimization and indexing"

**🔐 Auth & Permissions (typo3-security)**
- "Frontend user registration with email verification"
- "Backend user groups with granular permissions"
- "SAML SSO integration with Azure AD"

**🔄 Upgrades (typo3-rector, typo3-extension-upgrade)**
- "Upgrade extension from v12 to v13/v14 with Rector"
- "Fix all deprecations for TYPO3 v14"
- "Fractor for TypoScript and Fluid migrations"
- "Site migration from v10 to v14 with URL preservation"

**🧪 Testing (typo3-testing)**
- "Unit tests with mocked repositories"
- "Functional tests with database fixtures"
- "E2E tests with Playwright for contact form"
- "GitHub Actions CI for PHP 8.2/8.3 + TYPO3 v13/v14"

**🔒 Security Hardening (typo3-security, security-audit)**
- "Security audit for XSS, CSRF, SQL injection"
- "Production hardening checklist"
- "OWASP Top 10 compliance review"
- "PSR-15 middleware for security headers"
- "CVSS scoring for discovered vulnerabilities"

**📊 Agent Readiness (readiness-report)**
- "Run /readiness-report to evaluate this repository"
- "Assess codebase maturity for AI-assisted development"
- "Identify gaps preventing effective autonomous development"
- "Check which maturity level (L1-L5) this repo achieves"
- "Generate prioritized recommendations for agent readiness"
- "Evaluate the 9 technical pillars: Style, Build, Testing, Docs, DevEnv, Debugging, Security, Tasks, Analytics"

**🚨 Incident Response (security-incident-reporting)**
- "Create NIST/SANS-style incident report for executive summary"
- "Document DDoS attack with timeline, peak bandwidth, and attack vectors"
- "Build post-mortem report with blameless root cause analysis (5-Whys)"
- "Generate IoC list with MITRE ATT&CK TTPs for threat intelligence"
- "Correlate UDP amplification attack with CVE-2023-29552 (SLP)"
- "Calculate incident severity using NCISS and DRS scoring"
- "Create chronological timeline with detection, containment, recovery phases"
- "Assess financial impact: lost revenue, scrubbing costs, response hours"
- "Multi-vector DDoS analysis: volumetric + application layer"
- "Executive summary for C-level stakeholders (max 200 words)"

**🔬 TYPO3 Forensics (security-incident-reporting/TYPO3)**
- "Verify TYPO3 Core integrity after suspected compromise"
- "Analyze sys_log for suspicious backend logins and failed attempts"
- "Search fileadmin for PHP webshells and malicious uploads"
- "Check tt_content bodytext for injected scripts or spam"
- "Audit be_users for unauthorized admin accounts"
- "Create PGP-encrypted vulnerability report for security@typo3.org"
- "Document TYPO3 system inventory: version, PHP, extensions"
- "Classify vulnerability: Deserialization, XSS, SQLi, IDOR"
- "Generate forensic checklist: logs, filesystem, database analysis"
- "Responsible disclosure: follow embargo rules until advisory release"

**📈 SEO (typo3-seo)**
- "XML sitemap with custom entries"
- "OpenGraph/Twitter cards with fallbacks"
- "Hreflang for multi-language sites"
- "Structured data for articles (JSON-LD)"

**📬 Powermail Forms (typo3-powermail)**
- "Create a simple contact form with name, email, subject, message"
- "Build a multi-step order form with product selection and GDPR checkboxes"
- "Create a registration form with company details and VAT number"
- "Build a job application form with file upload and cover letter"
- "Create an event registration form with date picker and attendee count"
- "Build a feedback/survey form with radio buttons and rating scale"
- "Create a newsletter signup form with double opt-in"
- "Build a support ticket form that routes to departments via select"
- "Create a booking request form with date range and room type"
- "Build a callback request form with preferred time slot selection"
- "Create a custom finisher that sends form data to a CRM API"
- "Custom finisher that creates fe_users from registration form"
- "Write a finisher that posts form data to Slack/Teams webhook"
- "SaveToAnyTable: write form answers to a custom database table"
- "Create a SendParametersFinisher to forward data to external service"
- "Custom validator for Austrian VAT number (ATU format)"
- "Custom validator for IBAN fields"
- "Custom validator for Austrian ZIP codes (4 digits)"
- "Validate that at least one checkbox in a group is selected"
- "PSR-14 event: route receiver email based on department select field"
- "PSR-14 event: modify sender name from multiple form fields"
- "PSR-14 event: prevent DB save for specific forms"
- "PSR-14 event: add custom data to mail object for use in finishers"
- "PSR-14 event: modify email body before sending"
- "Configure spam shield with honeypot, rate limiting, and blacklists"
- "Custom spam shield method with external API (Akismet, reCAPTCHA)"
- "Configure double opt-in for newsletter signups with custom email template"
- "AJAX form submission without page reload"
- "Override receiver and sender email templates with custom Fluid partials"
- "Prefill form fields from logged-in frontend user data"
- "Prefill form fields from GET/POST parameters"
- "Add form to page via TypoScript without backend plugin"
- "Configure route enhancer for SEO-friendly opt-in URLs"
- "Export submitted mails to CSV/Excel via backend module"
- "Create a multi-language form (English + German) with translated labels"
- "Translate select/radio options for multi-language forms"
- "Create form structure via DataHandler CLI command"
- "Insert form with all fields via DDEV SQL for local testing"
- "Show the database structure of all powermail tables"

**📬 Powermail Conditions (typo3-powermail/CONDITIONS)**
- "Show/hide fields based on select dropdown value"
- "Hide an entire page/fieldset unless a checkbox is checked"
- "Show extra fields when user selects 'Other' in a dropdown"
- "Field-to-field comparison: warn when email fields don't match"
- "Build conditional form for Austrian legal types (Gesellschaftsformen)"
- "Show Firmenbuchnummer only for GmbH, AG, OG, KG, e.U."
- "Show Stammkapital and Geschäftsführer only for GmbH"
- "Show ZVR-Zahl and Obmann only for Verein"
- "Create condition container with multiple rules and AND/OR conjunction"
- "Reduce flickering with server-side prerendered conditions ViewHelper"
- "Configure route enhancer for condition AJAX endpoint (TypeNum 3132)"
- "Exclude file upload fields from condition AJAX payload"
- "Create conditions via DDEV SQL for local testing"
- "Create conditions via DataHandler CLI command"
- "Show the database structure of all powermail_cond tables"
- "Numeric comparison: show discount field when quantity > 10"
- "Multi-step shop form with conditional fields per legal type (full example)"
- "Create powermail form as workspace draft (not live)"
- "Set up DataHandler CLI with --workspace option for draft forms"
- "Publish workspace form via CLI: workspace:publish"
- "Ensure conditions are in the same workspace as the form"
- "Check which workspace a powermail form lives in (t3ver_wsid)"

**📋 Records List Types (typo3-records-list-types)**
- "Set Grid View as default for the Records module"
- "Configure per-table fields for News cards (title, teaser, image)"
- "Switch between Grid, Compact, and Teaser views in the backend"
- "Create a custom Timeline view type with TSconfig and Fluid template"
- "Add an Address Book view using CompactView with fixed columns"
- "Restrict view modes to specific pages via TSconfig conditions"
- "Register a custom view type via PSR-14 RegisterViewModesEvent"
- "Configure pagination: items per page, per-type override"
- "Create a Photo Gallery view (GridView, 48 items, no description)"
- "Add a Product Catalog view with custom template and large thumbnails"
- "Reuse built-in TeaserView for event calendar page"
- "Set up drag-and-drop reordering in Grid View"
- "Add custom CSS for dark mode support using TYPO3 CSS variables"
- "Add custom JavaScript module to a view type"
- "Configure grid column count for media folder pages"
- "Force Grid View for a specific backend user group"
- "Show workspace state indicators (new, modified, moved, deleted)"
- "Disable extension for specific page trees"
- "Create a custom view with no pagination (itemsPerPage = 0)"
- "Install the companion records-list-examples extension"

**🤖 AI Search (ai-search-optimization)**
- "Optimize content for ChatGPT and Perplexity citations"
- "Schema markup for Google AI Overviews (FAQPage, Article, HowTo)"
- "Configure robots.txt for AI crawlers (GPTBot, PerplexityBot, ClaudeBot)"
- "E-E-A-T signals and author bios for AI trust"
- "Implement llms.txt for LLM site discovery"
- "TYPO3 EXT:schema for structured data"
- "TYPO3 EXT:ai_llms_txt for llms.txt generation"
- "MDX JSON-LD components for Next.js/Astro"
- "Raw MDX view with .md suffix or ?raw=true"
- "FAQ Content Block with FAQPage schema"
- "Content freshness with visible timestamps"
- "Monitor brand mentions in AI search platforms"
- "Audit website for AI search visibility"

**🔍 Deepfake Detection & Media Forensics (deepfake-detection)**
- "What are deepfakes and how do they work technically?"
- "Verify authenticity of this video before publication"
- "Is this image AI-generated? Check for diffusion model or GAN artifacts"
- "Analyze PRNU/PCE sensor fingerprints to match claimed camera source"
- "Generate DQ probability map to detect image splicing and compositing"
- "Detect face-swap deepfakes via temporal consistency and blink analysis"
- "Check this audio for voice cloning artifacts and synthetic speech patterns"
- "Verify C2PA/CAI content provenance and cryptographic chain of custody"
- "Analyze shadow physics and reflection consistency for semantic forensics"
- "Build automated media authentication pipeline with ffmpeg and exiftool"
- "Create forensic report with authenticity grade (1-6) and confidence intervals"
- "What tools do I need for deepfake detection? Install ffmpeg, exiftool, c2patool"
- "Explain the Liar's Dividend and 4D disinformation tactics"
- "How do I defend against CEO voice clone fraud attacks?"

**📚 Documentation (typo3-docs)**
- "RST documentation following docs.typo3.org"
- "API documentation with code examples"
- "Configuration reference with confval directive"

**🏢 Quality (enterprise-readiness, php-modernization)**
- "PHPStan level 9 configuration"
- "Enterprise readiness assessment"
- "Quality gates for CI/CD"
- "Custom logging with Sentry integration"

**🚀 Deployment (typo3-ddev)**
- "Deployer config with staging and production"
- "GitHub Actions automated deployment"
- "Docker production with health checks"

**🛠️ Common Fixes (typo3-datahandler)**
- "Fix broken relations and orphaned records"
- "Bulk content update with DataHandler"
- "Debug extension conflicts in TCA/hooks"
- "Database optimization and missing indexes"

**🐘 Postgres & Supabase (postgres-best-practices)**
- "Optimize this slow Postgres query"
- "Add proper indexes for WHERE and JOIN columns"
- "Review my schema for performance issues"
- "Set up Row Level Security for multi-tenant app"
- "Configure connection pooling with PgBouncer"
- "Find missing indexes on foreign keys"
- "Use cursor-based pagination instead of OFFSET"
- "Batch INSERT statements for bulk data"
- "UPSERT pattern for insert-or-update"
- "Use SKIP LOCKED for job queue processing"
- "Partition large time-series table"
- "Enable pg_stat_statements for query analysis"
- "Choose right index type: B-tree vs GIN vs BRIN"
- "Optimize RLS policies for performance"
- "Fix N+1 queries with batch loading"

**🖼️ OG Images & Social Sharing (og-image)**
- "Generate an OG image for my Next.js app"
- "Create social preview image matching my design system"
- "Set up Twitter card meta tags"
- "Configure Open Graph meta tags for LinkedIn sharing"
- "Screenshot my /og-image page at 1200x630"
- "Add og:image, og:title, og:description meta tags"
- "Create OG image with cosmic/ethereal/brutalist/editorial style"
- "Audit my site's social sharing meta tags"
- "Set up metadataBase for absolute OG image URLs"
- "Cache bust my OG image on Facebook/Twitter/LinkedIn"

**📈 Marketing & Growth (marketing-skills)**
- "Optimize this landing page for conversions"
- "Review my pricing page CRO"
- "Write homepage copy for my SaaS product"
- "Create headlines for this feature page"
- "Improve this CTA copy"
- "Audit my site for SEO issues"
- "Why isn't my page ranking?"
- "Review my pricing tiers and packaging"
- "Should I use freemium or free trial?"
- "Apply psychology to increase conversions"
- "What mental models apply to this marketing challenge?"
- "Help me structure this landing page"
- "Write copy for my demo request page"
- "Optimize my signup flow"
- "Create an A/B test plan for my pricing page"
- "Add social proof and trust signals"
- "Handle objections on my sales page"
- "Write a value proposition for my product"

**🎯 CRO Funnel Optimization (cro-funnel)**
- "Optimize my lead capture form (reduce fields)"
- "Review my contact form for CRO issues"
- "Audit my demo request form for friction"
- "Improve my signup flow conversion rate"
- "Add social auth to reduce signup friction"
- "Design multi-step registration flow"
- "Create onboarding checklist for new users"
- "Define and optimize for the aha moment"
- "Design empty states that drive first action"
- "Create re-engagement flow for stalled users"
- "Design email capture popup with exit intent"
- "Create scroll-triggered newsletter popup"
- "Build announcement banner for new feature"
- "Design paywall screen for freemium upgrade"
- "Create trial expiration modal"
- "Optimize feature gate for paid conversion"
- "Full-funnel CRO audit from page to payment"

**📊 Programmatic SEO (programmatic-seo)**
- "Build [service] in [city] pages at scale"
- "Create comparison pages ([X] vs [Y])"
- "Design directory pages for my category"
- "Build integration pages for partner tools"
- "Create persona pages ([product] for [audience])"
- "Design template gallery for SEO"
- "Build glossary pages for industry terms"
- "Plan programmatic SEO strategy for my SaaS"
- "Avoid thin content penalties at scale"
- "Design URL structure for programmatic pages"
- "Create hub and spoke internal linking"
- "Choose between the 12 pSEO playbooks"

**🚀 Product Launch (launch-strategy)**
- "Plan my Product Hunt launch strategy"
- "Create pre-launch waitlist campaign"
- "Design 5-phase launch from alpha to GA"
- "Build ORB channel strategy (owned/rented/borrowed)"
- "Create Product Hunt listing and assets"
- "Plan post-launch momentum strategy"
- "Design feature announcement campaign"
- "Create beta program with early access"
- "Build launch checklist for new product"
- "Plan ongoing launch for feature releases"

**🧪 A/B Testing (ab-testing)**
- "Design A/B test for my homepage hero"
- "Create hypothesis for pricing page test"
- "Calculate sample size for my experiment"
- "How long should I run this A/B test?"
- "Choose primary and guardrail metrics"
- "Analyze A/B test results"
- "Document test learnings and next steps"
- "Plan multivariate test for checkout flow"
- "Avoid common A/B testing mistakes"
- "Set up experiment tracking"

**⚛️ React & Next.js Performance (react-best-practices)**
- "Review this React component for performance issues"
- "Optimize this Next.js page"
- "Eliminate request waterfalls in my data fetching"
- "Use Promise.all for parallel fetches"
- "Add Suspense boundaries for streaming"
- "Reduce bundle size with dynamic imports"
- "Avoid barrel file imports"
- "Use React.cache() for request deduplication"
- "Optimize re-renders with memo and useTransition"
- "Defer third-party scripts after hydration"
- "Use SWR for client-side data fetching"
- "Parallelize server component fetches"

**🛠️ Skill Creation (skill-creator)**
- "Create a new skill for database migrations"
- "Initialize a skill template for my custom workflow"
- "Package my skill for distribution"
- "Validate my SKILL.md frontmatter"
- "Help me structure a skill with references and scripts"
- "What's the best pattern for organizing a multi-domain skill?"

**🔥 Web Research & Scraping (firecrawl)**
- "Search the web for Next.js 15 new features and summarize"
- "Scrape the Stripe API documentation for webhooks"
- "Research competitor pricing pages and compare features"
- "Fetch the latest React documentation on Server Components"
- "Map all URLs on docs.example.com and find API pages"
- "Get the Tailwind CSS v4 migration guide"
- "Search for tech news from today about AI agents"
- "Scrape this JavaScript-heavy SPA page (wait for render)"
- "Find GitHub repositories for headless CMS"
- "Search for reviews of these 5 products in parallel"
- "Extract all code examples from this documentation page"
- "Find the latest security vulnerabilities disclosed this week"

**🎨 Frontend Design & Creative UI (frontend-design)**
- "Create a distinctive landing page that doesn't look AI-generated"
- "Design a dark tech hero section with gradient mesh backgrounds"
- "Build a pricing card with glass morphism effects"
- "Create an editorial-style testimonial section"
- "Design a brutalist navigation menu"
- "Build a retro-futuristic dashboard interface"
- "Create animated cards with staggered reveal on scroll"
- "Design a luxury product page with serif typography"
- "Build a SaaS hero with neon accents and glow effects"
- "Create a minimalist portfolio with bold typography"
- "Design feature cards with creative hover states"
- "Build a dark mode interface with proper contrast"
- "Suggest distinctive font pairings, avoid Inter/Roboto"
- "Create a color palette with dominant, secondary, and accent colors"
- "Add micro-interactions to my buttons (hover, click, loading)"
- "Build a page transition with slide-up fade-in animations"
- "Create a gradient mesh background with subtle animation"
- "Add noise texture overlay for visual depth"
- "Design a navigation that morphs between mobile and desktop"
- "Audit my design for 'AI slop' patterns and fix them"
- "Create CSS variables for a complete design system"
- "Build a hero with parallax scrolling and floating elements"
- "Design an asymmetric layout with intentional visual tension"
- "Create a diagonal split layout for my hero section"

**✅ Accessibility & Interface Review (web-design-guidelines)**
- "Review this component for accessibility issues"
- "Audit my form for WCAG 2.1 AA compliance"
- "Check color contrast ratios in my design"
- "Add proper ARIA labels to my navigation"
- "Fix keyboard navigation in my modal"
- "Add focus indicators to all interactive elements"
- "Review semantic HTML structure"
- "Check touch target sizes for mobile"
- "Add skip links for keyboard users"
- "Audit my site for screen reader compatibility"
- "Fix heading hierarchy issues"
- "Add alt text to all images"
- "Create an accessible modal with focus trapping and escape key"
- "Build accessible tabs with ARIA roles and arrow key navigation"
- "Add ARIA live regions for dynamic notifications"
- "Check my color palette for colorblind accessibility"
- "Create accessible date picker with keyboard support"
- "Implement prefers-reduced-motion for my animations"
- "Convert this div-soup navigation to semantic HTML"
- "Add scope attributes and captions to my data tables"
- "Create keyboard-navigable image gallery"
- "What will a screen reader announce for this component?"
- "Run a full WCAG 2.1 AA audit with issue list and fixes"
- "Add focus-visible styles that look good without outlines"

**📱 Platform Design (android-design, ios-design, ipados-design, macos-design, tvos-design, visionos-design, watchos-design, web-platform-design)**
- "Review my Android app for Material Design 3 compliance"
- "Implement dynamic color theming in Jetpack Compose"
- "Create a Navigation Bar with 4 destinations"
- "Review my iOS app for Human Interface Guidelines"
- "Implement Dark Mode with semantic system colors"
- "Add Dynamic Type support to my SwiftUI app"
- "Create a tab bar with 5 sections using SF Symbols"
- "Adapt my iPhone app layout for iPad Split View"
- "Add keyboard shortcuts to my iPad app"
- "Implement sidebar navigation for iPad"
- "Support trackpad hover effects and right-click menus"
- "Create a Mac app with proper menu bar and shortcuts"
- "Implement toolbar and sidebar for my macOS app"
- "Review my tvOS app for focus navigation issues"
- "Design a 10-foot UI with proper text sizes for Apple TV"
- "Create Top Shelf content with deep links"
- "Design a visionOS window with glass material"
- "Implement look-and-pinch interaction for Vision Pro"
- "Create glanceable watchOS interface for Apple Watch"
- "Add complications to my watchOS app"
- "Audit my web app for WCAG 2.2 compliance"
- "Make my forms accessible with proper labels and error states"
- "Add RTL support with CSS logical properties"

**📄 Document Processing (document-processing)**
- "Extract text from this PDF while preserving structure"
- "Merge these 5 PDFs into one with bookmarks"
- "Split this 100-page PDF into chapters"
- "OCR this scanned PDF with poor quality"
- "Add 'CONFIDENTIAL' watermark to all pages"
- "Create a PDF invoice with header, line items, and footer"
- "Rotate all landscape pages to portrait"
- "Password-protect this PDF with encryption"
- "Extract pages 10-25 as a new PDF"
- "Convert this Word document to clean markdown"
- "Create a DOCX with table of contents and page numbers"
- "Find and replace text across this Word document"
- "Extract all tracked changes with authors and dates"
- "Accept all tracked changes and save clean version"
- "Extract all text from this PowerPoint by slide"
- "Create a pitch deck: Problem, Solution, Market, Traction, Team, Ask"
- "Replace all images in this PowerPoint with new versions"
- "Export slide 5 as high-resolution PNG"
- "Analyze this Excel: row count, columns, data types, issues"
- "Calculate summary statistics for the Revenue column"
- "Find duplicate rows based on Email column"
- "Create an Excel budget with SUM formulas for totals"
- "Add formulas: column D = C * B, row 20 sums each column"
- "Format Excel: bold headers, currency format, alternating rows"
- "Create financial model: blue inputs, black formulas, green outputs"
- "Add conditional formatting: red if negative, green if above target"
- "Create dropdown list from values in another sheet"
- "Convert PDF tables to Excel file"
- "Batch process all PDFs: extract text to markdown files"

## Session Profiles

For optimal performance, limit active skills per session:

### Frontend Session
Active: `webconsulting-branding`, `ui-design-patterns`, `frontend-design`, `og-image`, `react-best-practices`  
Use case: UI development, styling, component creation, visual design, social sharing, React/Next.js optimization

### Creative Design Session
Active: `frontend-design`, `ui-design-patterns`, `webconsulting-branding`, `og-image`  
Use case: Distinctive UI design, creative interfaces, anti-AI-slop aesthetics, memorable user experiences

### Accessibility Audit Session
Active: `web-design-guidelines`, `ui-design-patterns`, `react-best-practices`  
Use case: WCAG compliance, accessibility audits, semantic HTML, ARIA patterns, keyboard navigation

### Document Processing Session
Active: `document-processing`, `enterprise-readiness`  
Use case: PDF manipulation, Word document creation, PowerPoint presentations, Excel analysis

### Backend Session
Active: `typo3-content-blocks`, `typo3-datahandler`, `typo3-powermail`, `typo3-records-list-types`, `typo3-ddev`, `typo3-update`, `typo3-testing`  
Use case: Extension development, Content Blocks, database operations, forms, backend views, v13/v14 compatible code

### Ops Session
Active: `typo3-security`, `security-audit`, `security-incident-reporting`, `enterprise-readiness`, `typo3-ddev`  
Use case: Server configuration, deployment, hardening, security audits, incident response

### Upgrade Session
Active: `typo3-rector`, `typo3-update`, `typo3-extension-upgrade`, `php-modernization`  
Use case: TYPO3 version migrations, PHP upgrades, dual-version compatibility

### PHP 8.4 Migration Session
Active: `php-modernization/SKILL-PHP84`, `typo3-rector/SKILL-PHP84`, `typo3-update/SKILL-PHP84`, `typo3-powermail/SKILL-PHP84`  
Use case: Migrating to PHP 8.4, using new language features, fixing deprecations

### Content Blocks Migration Session
Active: `typo3-content-blocks`, `typo3-datahandler/SKILL-CONTENT-BLOCKS`, `typo3-extension-upgrade/SKILL-CONTENT-BLOCKS`  
Use case: Converting classic TCA/SQL extensions to Content Blocks

### Documentation Session
Active: `typo3-docs`, `typo3-conformance`  
Use case: Extension documentation, quality assessment, standards compliance

### Core Contribution Session
Active: `typo3-core-contributions`, `typo3-testing`, `typo3-conformance`  
Use case: Contributing patches to TYPO3 Core via Gerrit

### Marketing & SEO Session
Active: `typo3-seo`, `ai-search-optimization`, `webconsulting-branding`  
Use case: SEO optimization, AI search visibility, content marketing, structured data

### Media Forensics Session
Active: `deepfake-detection`, `security-audit`, `security-incident-reporting`  
Use case: Media authentication, deepfake detection, disinformation defense, content provenance verification

### Database Session
Active: `postgres-best-practices`, `typo3-datahandler`, `security-audit`  
Use case: Database optimization, Postgres queries, RLS policies, connection pooling, schema design

### Marketing Session
Active: `marketing-skills`, `ai-search-optimization`, `ui-design-patterns`  
Use case: Landing page optimization, copywriting, pricing strategy, SEO audits, conversion optimization

### CRO & Growth Session
Active: `cro-funnel`, `ab-testing`, `marketing-skills`, `programmatic-seo`  
Use case: Full-funnel conversion optimization, A/B testing, signup flows, onboarding, paywall optimization

### Product Launch Session
Active: `launch-strategy`, `marketing-skills`, `og-image`, `programmatic-seo`  
Use case: Product launches, Product Hunt campaigns, go-to-market strategy, feature announcements

### React & Next.js Session
Active: `react-best-practices`, `ui-design-patterns`, `og-image`  
Use case: React/Next.js performance optimization, bundle size reduction, data fetching patterns, server components

### Research & Documentation Session
Active: `firecrawl`, `context7`, `ai-search-optimization`  
Use case: Web research, API documentation lookup, competitor analysis, content extraction, documentation crawling

### Android Development Session
Active: `android-design`, `ui-design-patterns`, `react-best-practices`  
Use case: Material Design 3, Jetpack Compose, dynamic color, Android navigation, accessibility

### Apple Platform Session
Active: `ios-design`, `ipados-design`, `macos-design`, `watchos-design`, `tvos-design`, `visionos-design`  
Use case: SwiftUI/UIKit development, Human Interface Guidelines, Apple platform-specific patterns

### Cross-Platform Design Session
Active: `android-design`, `ios-design`, `web-platform-design`, `ui-design-patterns`  
Use case: Designing for multiple platforms, ensuring platform-appropriate patterns, accessibility across platforms

## Version Compatibility Matrix

| Skill | TYPO3 v13 | TYPO3 v14 | PHP 8.2 | PHP 8.3 | PHP 8.4 |
|-------|-----------|-----------|---------|---------|---------|
| typo3-content-blocks | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-datahandler | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-ddev | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-testing | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-conformance | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-docs | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-core-contributions | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-rector | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-update | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-extension-upgrade | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-security | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-seo | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-powermail | ✓ | ✓ | ✓ | ✓ | ✓ |
| typo3-records-list-types | | ✓ | | ✓ | ✓ |
| ai-search-optimization | ✓ | ✓ | ✓ | ✓ | ✓ |
| security-audit | ✓ | ✓ | ✓ | ✓ | ✓ |
| security-incident-reporting | ✓ | ✓ | ✓ | ✓ | ✓ |
| deepfake-detection | ✓ | ✓ | ✓ | ✓ | ✓ |
| enterprise-readiness | ✓ | ✓ | ✓ | ✓ | ✓ |
| readiness-report | ✓ | ✓ | ✓ | ✓ | ✓ |
| php-modernization | ✓ | ✓ | ✓ | ✓ | ✓ |
| cli-tools | ✓ | ✓ | ✓ | ✓ | ✓ |
| context7 | ✓ | ✓ | ✓ | ✓ | ✓ |
| webconsulting-branding | ✓ | ✓ | ✓ | ✓ | ✓ |
| ui-design-patterns | ✓ | ✓ | ✓ | ✓ | ✓ |
| postgres-best-practices | ✓ | ✓ | ✓ | ✓ | ✓ |
| marketing-skills | ✓ | ✓ | ✓ | ✓ | ✓ |
| og-image | ✓ | ✓ | ✓ | ✓ | ✓ |
| react-best-practices | ✓ | ✓ | ✓ | ✓ | ✓ |
| frontend-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| web-design-guidelines | ✓ | ✓ | ✓ | ✓ | ✓ |
| document-processing | ✓ | ✓ | ✓ | ✓ | ✓ |
| firecrawl | ✓ | ✓ | ✓ | ✓ | ✓ |
| skill-creator | ✓ | ✓ | ✓ | ✓ | ✓ |
| android-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| ios-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| ipados-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| macos-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| tvos-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| visionos-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| watchos-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| web-platform-design | ✓ | ✓ | ✓ | ✓ | ✓ |
| cro-funnel | ✓ | ✓ | ✓ | ✓ | ✓ |
| programmatic-seo | ✓ | ✓ | ✓ | ✓ | ✓ |
| launch-strategy | ✓ | ✓ | ✓ | ✓ | ✓ |
| ab-testing | ✓ | ✓ | ✓ | ✓ | ✓ |

## Adding New Skills

1. Create directory: `skills/my-new-skill/`
2. Add `SKILL.md` with YAML frontmatter
3. Include `typo3_compatibility: "13.0 - 14.x"` in frontmatter
4. Run `./install.sh` to deploy
5. This index updates automatically via GitHub Actions

---
*Generated by webconsulting Claude Marketplace*
