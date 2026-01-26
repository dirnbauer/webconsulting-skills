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
| **PHP & Tools** | | | |
| `php-modernization` | PHP 8.x patterns, PHPStan level 10, DTOs, enums | 1.0.0 | php, modernization, phpstan, rector |
| `php-modernization/PHP84` | PHP 8.4 features: property hooks, asymmetric visibility | 1.0.0 | php 8.4, property hooks |
| `cli-tools` | CLI tool management and auto-installation | 1.0.0 | cli, tools, installation |
| `context7` | Library documentation lookup via REST API | 1.0.0 | documentation, api, libraries |
| **Frontend & Design** | | | |
| `webconsulting-branding` | webconsulting.at design system, colors, typography, MDX | 1.0.0 | frontend, design, branding, ui |
| `ui-design-patterns` | Practical UI design patterns, accessibility, usability | 1.1.0 | ui, design, accessibility, usability |
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

### PHP & Tools
- **php-modernization**: PHP 8.x features, type safety, PHPStan level 10
  - `SKILL-PHP84.md`: PHP 8.4 property hooks, asymmetric visibility, new array functions
- **cli-tools**: CLI tool management, auto-installation on "command not found"
- **context7**: Library documentation lookup via Context7 REST API

### Frontend & Design
- **webconsulting-branding**: Design tokens, colors, typography, MDX components
- **ui-design-patterns**: Visual hierarchy, spacing, color, typography, accessibility

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

## Session Profiles

For optimal performance, limit active skills per session:

### Frontend Session
Active: `webconsulting-branding`, `ui-design-patterns`  
Use case: UI development, styling, component creation, visual design

### Backend Session
Active: `typo3-content-blocks`, `typo3-datahandler`, `typo3-ddev`, `typo3-update`, `typo3-testing`  
Use case: Extension development, Content Blocks, database operations, v13/v14 compatible code

### Ops Session
Active: `typo3-security`, `security-audit`, `security-incident-reporting`, `enterprise-readiness`, `typo3-ddev`  
Use case: Server configuration, deployment, hardening, security audits, incident response

### Upgrade Session
Active: `typo3-rector`, `typo3-update`, `typo3-extension-upgrade`, `php-modernization`  
Use case: TYPO3 version migrations, PHP upgrades, dual-version compatibility

### PHP 8.4 Migration Session
Active: `php-modernization/SKILL-PHP84`, `typo3-rector/SKILL-PHP84`, `typo3-update/SKILL-PHP84`  
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

## Adding New Skills

1. Create directory: `skills/my-new-skill/`
2. Add `SKILL.md` with YAML frontmatter
3. Include `typo3_compatibility: "13.0 - 14.x"` in frontmatter
4. Run `./install.sh` to deploy
5. This index updates automatically via GitHub Actions

---
*Generated by webconsulting Claude Marketplace*
