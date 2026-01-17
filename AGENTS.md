# Available Agent Skills

Auto-generated index of all available skills in this marketplace.

> **📢 Early Adopter Notice:** We encourage you to use these skills! Expect occasional updates as 
> Anthropic, Cursor, and webconsulting evolve their platforms. Always review AI-generated code.
> See [README](README.md) for details.

> **TYPO3 Compatibility:** All skills support TYPO3 v13.x and v14.x (v14 preferred)
> Code examples are designed to work on both versions simultaneously.

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

## Skills Overview

| Skill | Description | Version | Triggers |
|-------|-------------|---------|----------|
| **TYPO3 Development** | | | |
| `typo3-content-blocks` | Content Elements & Record Types with single source of truth config | 1.0.0 | content-blocks, content-element, record-type, irre |
| `typo3-datahandler` | Expert guidance on DataHandler for transactional database operations | 2.0.0 | database, datahandler, tcemain, records |
| `typo3-ddev` | TYPO3 local development with DDEV, multi-version testing | 2.0.0 | ddev, local, development, docker |
| `typo3-testing` | Unit, functional, E2E, architecture, mutation testing | 1.0.0 | testing, phpunit, playwright, phpat |
| `typo3-conformance` | Extension standards compliance checker | 1.0.0 | conformance, standards, quality |
| `typo3-docs` | Documentation using docs.typo3.org standards | 1.0.0 | documentation, rst, docs |
| `typo3-core-contributions` | TYPO3 Core contribution workflow (Gerrit, Forge) | 1.0.0 | core, contributions, gerrit, forge |
| **Upgrade & Migration** | | | |
| `typo3-rector` | TYPO3 upgrade patterns using Rector for dual-version support | 2.0.0 | rector, upgrade, migration, refactoring |
| `typo3-update` | TYPO3 v13/v14 dual-version development guide | 2.0.0 | update, upgrade, v13, v14 |
| `typo3-extension-upgrade` | Systematic extension upgrades with Rector, Fractor, PHPStan | 1.0.0 | extension, upgrade, fractor |
| **Security & Operations** | | | |
| `typo3-security` | Security hardening checklist and best practices | 2.0.0 | security, hardening, permissions |
| `typo3-seo` | SEO configuration with EXT:seo, sitemaps, meta tags | 2.0.0 | seo, sitemap, meta, robots |
| `ai-search-optimization` | AEO/GEO for AI search visibility with TYPO3, MD/MDX, and llms.txt | 1.0.0 | aeo, geo, ai search, chatgpt, perplexity, llms.txt |
| `security-audit` | Security audit patterns (OWASP, XXE, SQLi, XSS, CVSS) | 1.0.0 | security, audit, owasp, vulnerabilities |
| `enterprise-readiness` | OpenSSF, SLSA, supply chain security, quality gates | 1.0.0 | enterprise, openssf, slsa, security |
| **PHP & Tools** | | | |
| `php-modernization` | PHP 8.x patterns, PHPStan level 10, DTOs, enums | 1.0.0 | php, modernization, phpstan, rector |
| `php-modernization/PHP84` | PHP 8.4 features: property hooks, asymmetric visibility | 1.0.0 | php 8.4, property hooks |
| `cli-tools` | CLI tool management and auto-installation | 1.0.0 | cli, tools, installation |
| `context7` | Library documentation lookup via REST API | 1.0.0 | documentation, api, libraries |
| **Frontend Development** | | | |
| `webconsulting-branding` | webconsulting.at design system, colors, typography, MDX | 1.0.0 | frontend, design, branding, ui |
| `ui-design-patterns` | Practical UI design patterns, accessibility, usability | 1.1.0 | ui, design, accessibility, usability |

## Skill Categories

### TYPO3 Development
- **typo3-content-blocks**: Content Elements & Record Types with single YAML config (no duplicate TCA/SQL)
- **typo3-datahandler**: Safe database operations via DataHandler API with PSR-14 events
- **typo3-ddev**: Local development environment setup with multi-version testing
- **typo3-testing**: Comprehensive testing (unit, functional, E2E, architecture, mutation)
- **typo3-conformance**: Extension quality assessment and standards compliance
- **typo3-docs**: Official documentation standards with RST and TYPO3 directives
- **typo3-core-contributions**: Contributing to TYPO3 Core via Gerrit and Forge

### Upgrade & Migration
- **typo3-rector**: Automated code refactoring with Rector for dual-version support
- **typo3-update**: Version migration and compatibility strategies for v13/v14
- **typo3-extension-upgrade**: Systematic extension upgrades with Rector, Fractor, PHPStan

### Security & Operations
- **typo3-security**: Production hardening checklist for v13/v14
- **typo3-seo**: Search engine optimization with EXT:seo
- **ai-search-optimization**: AEO/GEO for AI search (schema.org, robots.txt, llms.txt, TYPO3, MD/MDX)
- **security-audit**: Deep security audits aligned with OWASP Top 10
- **enterprise-readiness**: OpenSSF Scorecard, SLSA, supply chain security

### PHP & Tools
- **php-modernization**: PHP 8.x features, type safety, PHPStan level 10
  - `SKILL-PHP84.md`: PHP 8.4 property hooks, asymmetric visibility, new array functions
- **cli-tools**: CLI tool management, auto-installation on "command not found"
- **context7**: Library documentation lookup via Context7 REST API

## Supplement Skills (PHP 8.4 & Content Blocks)

Each TYPO3-related skill now includes optional supplement files:

### PHP 8.4 Supplements (`SKILL-PHP84.md`)

Cover PHP 8.4 specific patterns for each skill domain:
- Property hooks for validation
- Asymmetric visibility for encapsulation
- New array functions (`array_find`, `array_any`, `array_all`)
- `#[\Deprecated]` attribute usage
- Migration patterns from PHP 8.2/8.3

**Skills with PHP 8.4 supplements:**
`php-modernization`, `typo3-datahandler`, `typo3-ddev`, `typo3-testing`, `typo3-rector`, 
`typo3-update`, `typo3-extension-upgrade`, `typo3-conformance`, `typo3-security`, 
`typo3-seo`, `typo3-docs`, `typo3-core-contributions`

### Content Blocks Supplements (`SKILL-CONTENT-BLOCKS.md`)

Cover Content Blocks integration for each skill domain:
- Using Content Blocks with the skill's topic
- Migration from classic TCA/SQL
- Best practices and patterns

**Skills with Content Blocks supplements:**
`typo3-datahandler`, `typo3-ddev`, `typo3-testing`, `typo3-rector`, `typo3-update`, 
`typo3-extension-upgrade`, `typo3-conformance`, `typo3-security`, `typo3-seo`, 
`typo3-docs`, `typo3-core-contributions`

### Frontend Development
- **webconsulting-branding**: Design tokens, colors, typography, MDX components
- **ui-design-patterns**: Visual hierarchy, spacing, color, typography, accessibility

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

**🔒 Security (typo3-security, security-audit)**
- "Security audit for XSS, CSRF, SQL injection"
- "Production hardening checklist"
- "OWASP Top 10 compliance review"
- "PSR-15 middleware for security headers"

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

## Session Profiles

For optimal performance, limit active skills per session:

### Frontend Session
Active: `webconsulting-branding`, `ui-design-patterns`  
Use case: UI development, styling, component creation, visual design

### Backend Session
Active: `typo3-content-blocks`, `typo3-datahandler`, `typo3-ddev`, `typo3-update`, `typo3-testing`  
Use case: Extension development, Content Blocks, database operations, v13/v14 compatible code

### Ops Session
Active: `typo3-security`, `security-audit`, `enterprise-readiness`, `typo3-ddev`  
Use case: Server configuration, deployment, hardening, security audits

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
| enterprise-readiness | ✓ | ✓ | ✓ | ✓ | ✓ |
| php-modernization | ✓ | ✓ | ✓ | ✓ | ✓ |
| cli-tools | ✓ | ✓ | ✓ | ✓ | ✓ |
| context7 | ✓ | ✓ | ✓ | ✓ | ✓ |
| webconsulting-branding | ✓ | ✓ | ✓ | ✓ | ✓ |
| ui-design-patterns | ✓ | ✓ | ✓ | ✓ | ✓ |

## Adding New Skills

1. Create directory: `skills/my-new-skill/`
2. Add `SKILL.md` with YAML frontmatter
3. Include `typo3_compatibility: "13.0 - 14.x"` in frontmatter
4. Run `./install.sh` to deploy
5. This index updates automatically via GitHub Actions

---
*Generated by webconsulting Claude Marketplace*
