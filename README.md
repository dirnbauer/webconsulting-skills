# webconsulting Claude Marketplace

AI-augmented development environment for enterprise TYPO3 projects. This repository provides **Agent Skills** that transform Claude into a specialized TYPO3 Solutions Architect.

> **Works with:** Claude Code, Cursor IDE (tested with Cursor 2.2+)

---

> ## 📢 Early Adopter Notice
>
> **We encourage you to use these skills!** They're designed to boost your TYPO3 productivity significantly.
> However, please keep these points in mind:
>
> - **Evolving Technology** — Anthropic, Cursor, and webconsulting are actively improving their platforms. Expect updates and occasional breaking changes.
> - **Review AI Output** — Always review AI-generated code before committing. These skills enhance productivity, but human judgment remains essential.
> - **Stay Updated** — Run `git pull && ./install.sh` regularly to get the latest improvements and compatibility fixes.
>
> Questions or feedback? We'd love to hear from you!

---

> **Attribution:** The majority of skills in this repository are derived from the excellent work by
> **[Netresearch DTT GmbH](https://github.com/netresearch)**. We recommend using their original
> repositories for the latest updates. A few additional skills are specific to webconsulting.at.

---

## 🚀 Unified Agent Skills (Cursor + Claude Code)

Both **Cursor** and **Claude Code** now share the same skills location: `~/.claude/skills/`

### What's New

| Feature | Description |
|---------|-------------|
| **Unified Location** | Skills install to `~/.claude/skills/` (works for Cursor & Claude Code) |
| **Auto-Discovery** | Both IDEs automatically find and load skills |
| **Invoke with `/`** | Type `/` in Agent chat to see all available skills |
| **Cross-Platform** | Same skills work in Cursor, Claude Code, and Claude CLI |

### Directory Structure After Install

```
~/.claude/skills/          ← Primary (shared by Cursor & Claude Code)
  ├── typo3-content-blocks/
  ├── typo3-datahandler/
  └── ...

.cursor/
  ├── skills/              ← Project-level (version-controlled)
  └── rules/               ← Legacy .mdc files (backwards compat)
```

### Using Skills

**In Cursor:**
1. **Auto-applied**: Cursor decides when skills are relevant
2. **Manual invoke**: Type `/typo3-content-blocks` in Agent chat
3. **View all**: Go to `Cursor Settings → Rules` to see discovered skills

**In Claude Code:**
1. Skills are automatically loaded from `~/.claude/skills/`
2. Reference skills in your prompts or let Claude auto-detect

> **Note:** Legacy `.mdc` rules are still generated in `.cursor/rules/` for backwards compatibility.

---

## Quick Start

```bash
# Clone the repository
git clone git@github.com:dirnbauer/claude-cursor-typo3-skills.git
cd claude-cursor-typo3-skills

# Install skills
chmod +x install.sh
./install.sh

# Restart Cursor IDE
```

### Alternative: Composer Agent Skill Plugin

For automatic skill loading in PHP projects, use Netresearch's Composer plugin:

```bash
composer require --dev netresearch/composer-agent-skill-plugin
```

This plugin automatically discovers and loads agent skills from your Composer dependencies.
See: https://github.com/netresearch/composer-agent-skill-plugin

### Alternative: Composer from GitHub (VCS)

Install this skills package directly from GitHub without Packagist.

**1. Add the repository to your project's `composer.json`:**

```json
{
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/dirnbauer/claude-cursor-typo3-skills"
        }
    ]
}
```

**2. Require the package:**

```bash
composer require --dev webconsulting/claude-typo3-skills:dev-main
```

The Composer plugin will automatically run `install.sh` after installation to deploy skills to `~/.claude/skills/`.

## How to Use Agent Skills

### Skills for Dummies

**What are Agent Skills?** They're Markdown files (`SKILL.md`) containing expert knowledge that Claude reads to become a specialist. After running `./install.sh`, skills are installed to `~/.claude/skills/` and automatically discovered by both Cursor and Claude Code.

**How do they work?** 
- **Auto-applied**: Cursor's Agent decides when a skill is relevant based on your query
- **Manual invoke**: Type `/skill-name` in chat (e.g., `/typo3-content-blocks`)
- **Trigger keywords**: Mentioning keywords like "content-blocks" or "datahandler" activates relevant skills

**Where do skills live?**
- Source files: `skills/*/SKILL.md` (this repo)
- User-level: `~/.claude/skills/` (primary, shared by Cursor & Claude Code)
- Project-level: `.cursor/skills/` (version-controlled)
- Legacy rules: `.cursor/rules/*.mdc` (backwards compatibility)

### Skill Reference

| Skill | Trigger Keywords | Example Prompt |
|-------|------------------|----------------|
| `typo3-content-blocks` | content-blocks, content-element, record-type, migrate tca | "Create a Content Block for a hero banner" or "Migrate my TCA to Content Blocks" |
| `typo3-datahandler` | database, datahandler, records, tcemain | "Create a tt_content record using DataHandler" |
| `typo3-ddev` | ddev, local, docker, environment | "Set up DDEV for TYPO3 v14" |
| `typo3-testing` | testing, phpunit, e2e, coverage | "Write unit tests for my repository" |
| `typo3-conformance` | conformance, standards, quality | "Check if my extension meets TYPO3 standards" |
| `typo3-docs` | documentation, rst, docs | "Create RST documentation for my extension" |
| `typo3-core-contributions` | core, gerrit, forge, patch | "Submit a patch to TYPO3 Core" |
| `typo3-rector` | rector, refactoring, deprecation | "Use Rector to fix deprecations" |
| `typo3-update` | update, upgrade, v13, v14, migration | "Make my code compatible with v13 and v14" |
| `typo3-extension-upgrade` | extension upgrade, fractor | "Upgrade my extension to TYPO3 v14" |
| `typo3-security` | security, hardening, permissions | "Harden my TYPO3 installation" |
| `typo3-seo` | seo, sitemap, meta, opengraph | "Configure SEO with sitemaps and meta tags" |
| `ai-search-optimization` | aeo, geo, ai search, chatgpt, llms.txt | "Optimize for ChatGPT and Perplexity citations" |
| `security-audit` | security audit, owasp, vulnerabilities | "Audit my controller for security issues" |
| `enterprise-readiness` | enterprise, openssf, slsa | "Assess my project for enterprise readiness" |
| `php-modernization` | php, phpstan, dto, enum | "Modernize my PHP code to 8.3 patterns" |
| `cli-tools` | cli, tools, command not found | "Install missing CLI tools" |
| `context7` | documentation, api, libraries | "Look up current Symfony documentation" |
| `webconsulting-branding` | branding, design, components | "Apply webconsulting design system" |
| `ui-design-patterns` | ui, design, layout, typography | "Improve the visual hierarchy of my UI" |

### Example Prompts (Copy & Paste)

#### 🏗️ Project Setup & Environment

**New TYPO3 Project:**
```
Set up a new TYPO3 v14 project with DDEV, Redis caching, and Mailpit for email testing
```

**Multi-Site Configuration:**
```
Configure a multi-site setup with 3 domains sharing the same TYPO3 installation, each with German and English languages
```

**Database Operations:**
```
Export the database from production, sanitize sensitive data, and import it into my local DDEV environment
```

**Xdebug Setup:**
```
Configure Xdebug in DDEV for step debugging with Cursor/PhpStorm, including the correct IDE key settings
```

---

#### 📦 Content Blocks (Single Source of Truth)

**Hero Banner Content Element:**
```
Create a Content Block for a hero banner with: headline, subheadline, background image, CTA button link, and overlay color selection
```

**Team Members Record Type:**
```
Create a Content Block Record Type for team members with: name, position, email, phone, bio (richtext), photo, and social media links (Collection). Use Extbase-compatible table naming.
```

**Accordion Content Element:**
```
Create a Content Block for an accordion with unlimited items. Each item has a title, richtext content, and "initially open" checkbox. Include frontend.html and backend-preview.html templates.
```

**FAQ with Categories:**
```
Create a Record Type for FAQs with question, answer, and category relation. Then create a Content Element that displays FAQs filtered by selected categories.
```

**Image Slider with IRRE:**
```
Create a slider Content Block using a Collection field. Each slide has: image (required), title, description, and link. Limit to 10 slides max.
```

---

#### 🔄 Content Blocks Migration (Classic → Modern)

**Migrate Content Element:**
```
Migrate my classic content element from TCA/SQL to Content Blocks. Here's my current TCA in Configuration/TCA/Overrides/tt_content.php: [paste TCA]
```

**Migrate Record Table:**
```
Convert my classic tx_myext_domain_model_product table (with TCA and ext_tables.sql) to a Content Blocks Record Type. Keep the same table name for data compatibility.
```

**Analyze TCA for Migration:**
```
Analyze this TCA configuration and show me the equivalent Content Blocks config.yaml with all field mappings: [paste TCA]
```

**Migrate IRRE Relations:**
```
My extension has inline (IRRE) child records. Show me how to migrate the parent-child relationship to Content Blocks Collection fields.
```

**Keep Column Names:**
```
Migrate my content element to Content Blocks but keep the existing database column names (tx_myext_*) to avoid data migration. Use prefixField: false.
```

**Data Migration Script:**
```
Create a CLI command that migrates existing content from CType 'myext_hero' to the new Content Blocks CType 'myvendor_hero', including column mapping.
```

**Full Extension Migration:**
```
I have a classic TYPO3 extension with 3 content elements and 2 record types. Create a complete migration plan to Content Blocks, including which files to delete afterward.
```

---

#### ⏪ Content Blocks Revert (Modern → Classic)

**Revert Content Element:**
```
Revert my Content Block hero element back to classic TCA/SQL format. Here's my config.yaml: [paste config.yaml]. Generate the complete TCA, SQL, and TypoScript files.
```

**Revert Record Type:**
```
Convert my Content Blocks Record Type back to a classic TCA configuration. Generate the full TCA file with ctrl section, columns, and types. Table: tx_myext_domain_model_product
```

**Generate TCA from YAML:**
```
Analyze this Content Blocks config.yaml and generate the equivalent classic TCA PHP configuration with all field mappings: [paste config.yaml]
```

**Revert IRRE Collection:**
```
My Content Block uses a Collection field with inline child records. Show me how to revert this to classic TCA inline configuration with a separate child table.
```

**Revert Data Migration:**
```
Create a CLI command that reverts content from Content Blocks CType 'myvendor_hero' back to classic CType 'myext_hero', including copying data between columns.
```

**Update Fluid Templates for Classic:**
```
Update my Content Blocks Fluid template to work with classic TCA. Replace {data.fieldname} with {data.tx_myext_fieldname} and add proper DataProcessors for file relations.
```

**Full Extension Revert:**
```
I need to completely remove Content Blocks from my extension with 2 content elements and 1 record type. Create all necessary TCA, SQL, TypoScript files and a data migration script.
```

**Remove Content Blocks Dependency:**
```
After reverting to classic TCA, how do I safely remove the friendsoftypo3/content-blocks dependency and clean up orphaned database columns?
```

**Compare Approaches:**
```
Show me a side-by-side comparison of the same content element in Content Blocks vs classic TCA format, highlighting the pros and cons of each approach.
```

---

#### 🔧 Extension Development

**DataHandler CRUD:**
```
I need to create, update, and delete records in tx_myext_domain_model_product programmatically using DataHandler. Show me the proper pattern with transaction handling and error checking.
```

**Repository with Custom Query:**
```
Create a repository for my Product model with methods: findByCategory(), findInPriceRange(), and findFeatured(). Use proper typing and QueryBuilder.
```

**Extbase Controller:**
```
Create an Extbase controller with list, show, and filter actions for my Event model. Include proper request handling for v13/v14.
```

**PSR-14 Event Listener:**
```
Create a PSR-14 event listener that modifies page titles before rendering. Register it in Services.yaml with the AsEventListener attribute.
```

**Scheduler Task:**
```
Create a Scheduler task that imports products from an external API daily. Include progress reporting and proper error handling.
```

**Backend Module:**
```
Create a backend module for managing newsletter subscriptions with list view, export to CSV, and bulk delete functionality.
```

**Middleware:**
```
Create a PSR-15 middleware that adds security headers (CSP, X-Frame-Options, etc.) to all frontend responses.
```

---

#### 🔄 Upgrades & Migration

**Extension Upgrade v12 → v14:**
```
Upgrade my extension from TYPO3 v12 to support both v13 and v14. Use Rector for automated refactoring and show me what needs manual attention.
```

**Fix Deprecations:**
```
Scan my extension for deprecated code and fix all deprecations for TYPO3 v14. Use typo3-rector rules.
```

**Dual-Version Compatibility:**
```
My extension needs to work on both TYPO3 v13 and v14. Show me how to write version-compatible code for the breaking changes.
```

**Fractor for Non-PHP Files:**
```
Use Fractor to update my TypoScript, Fluid templates, and YAML files for TYPO3 v14 compatibility.
```

---

#### 🧪 Testing

**Unit Tests:**
```
Write unit tests for my ProductService class. Mock the repository and test the calculateDiscount() method with various inputs.
```

**Functional Tests:**
```
Set up functional tests for my ProductRepository. Include database fixtures and test findByCategory() with actual database queries.
```

**E2E Tests with Playwright:**
```
Write Playwright E2E tests for my contact form: test form submission, validation errors, and success message.
```

**GitHub Actions CI:**
```
Create a GitHub Actions workflow that runs PHPUnit tests, PHPStan analysis, and PHP-CS-Fixer on PHP 8.2 and 8.3 with TYPO3 v13 and v14.
```

---

#### 🔒 Security & Hardening

**Security Audit:**
```
Perform a security audit on my AuthController and UserService. Check for XSS, CSRF, SQL injection, and insecure session handling.
```

**Production Hardening:**
```
Create a security hardening checklist for my TYPO3 installation before going live. Include file permissions, configuration, and server settings.
```

**OWASP Compliance:**
```
Review my extension against OWASP Top 10 vulnerabilities and suggest fixes for any issues found.
```

---

#### 📈 SEO & Performance

**Full SEO Setup:**
```
Configure complete SEO for my TYPO3 site: XML sitemap with custom entries, OpenGraph/Twitter cards, canonical URLs, robots.txt, and structured data for articles.
```

**Meta Tags Configuration:**
```
Set up proper meta tag configuration with fallbacks: use page-specific tags if set, otherwise fall back to site-wide defaults.
```

**Hreflang for Multi-Language:**
```
Configure hreflang tags for my multi-language site with German, English, and French. Handle default language and x-default correctly.
```

---

#### 🤖 AI Search Optimization (AEO/GEO)

**Schema Markup for AI Search (TYPO3):**
```
Add FAQPage, Article, and Organization schema to my TYPO3 site using EXT:schema. Make content more likely to be cited by ChatGPT and Perplexity.
```

**Robots.txt for AI Crawlers:**
```
Configure robots.txt to allow AI search bots (GPTBot, PerplexityBot, ClaudeBot) while blocking AI training crawlers (Google-Extended, CCBot). Use TYPO3 site config static routes.
```

**llms.txt for TYPO3:**
```
Implement llms.txt for my TYPO3 site using web-vision/ai-llms-txt extension. Configure which pages to include and how to structure the index.
```

**llms.txt for Next.js/Astro:**
```
Create a dynamic llms.txt endpoint for my Next.js documentation site. Generate the index from content collections and include llms-full.txt with complete docs.
```

**FAQ Content Element with Schema:**
```
Create a TYPO3 Content Block for FAQ accordion that automatically generates FAQPage schema. Each item has question, answer, and initially-open checkbox.
```

**Article Schema with Author (TYPO3):**
```
Add Article schema with author information to my TYPO3 pages using a PSR-14 event listener. Include author name, credentials, LinkedIn, and dates.
```

**MDX JSON-LD Component:**
```
Create a reusable Next.js MDX component that generates Article schema from frontmatter (title, description, date, author). Include proper TypeScript types.
```

**FAQ Schema Component (MDX):**
```
Create a React FAQ component for MDX that renders an accessible accordion AND generates FAQPage schema. Use details/summary for no-JS support.
```

**E-E-A-T Author Bios:**
```
Add author bio fields to my TYPO3 pages (name, credentials, LinkedIn, bio) via TCA extension. Generate Person schema automatically for each page.
```

**Content Freshness Signals:**
```
Configure visible last-modified dates on my TYPO3 pages using SYS_LASTCHANGED. Add HTTP headers and structured data for content freshness.
```

**AI Search Visibility Audit:**
```
Audit my website for AI search visibility: check schema markup quality, E-E-A-T signals, content structure, robots.txt configuration, and llms.txt presence.
```

**Monitor AI Citations:**
```
What tools can I use to monitor how often my brand is mentioned in ChatGPT, Perplexity, and Google AI Overviews? Set up tracking.
```

**Raw MDX View Endpoint:**
```
Add a .md URL suffix to my Next.js docs that shows raw MDX source instead of rendered content. Similar to how Vercel docs works.
```

**Optimize for Perplexity:**
```
Perplexity prefers fresh content. How do I optimize my content update frequency and visible timestamps to maximize Perplexity citations?
```

**Google AI Overviews Optimization:**
```
What specific schema types and content structures increase the chance of appearing in Google AI Overviews? Implement for my TYPO3 site.
```

---

#### 📚 Documentation

**Extension Documentation:**
```
Create RST documentation for my extension following docs.typo3.org standards. Include: introduction, installation, configuration, and usage sections.
```

**API Documentation:**
```
Document my public API methods using proper RST format with code examples and configuration references.
```

---

#### 🏢 Enterprise & Quality

**PHPStan Level 9:**
```
Configure PHPStan at level 9 for my extension. Fix all errors and add proper type hints to pass the analysis.
```

**Enterprise Readiness:**
```
Assess my extension for enterprise readiness: OpenSSF best practices, supply chain security, and quality gates for CI/CD.
```

**Code Quality Gates:**
```
Set up quality gates for my project: PHPStan level 8+, test coverage >80%, no critical security issues, and proper documentation.
```

---

#### 🎨 Frontend & UI

**Fluid Component:**
```
Create a reusable Fluid partial for a card component with image, title, description, link, and optional badge. Make it work with Content Blocks data.
```

**Accessible Form:**
```
Review my contact form for accessibility issues. Ensure proper labels, error messages, focus management, and ARIA attributes.
```

**Design System Integration:**
```
Apply the webconsulting design system to my TYPO3 templates: colors, typography, spacing, and component styles.
```

---

#### 🗂️ TCA & FlexForm

**TCA Select with Items:**
```
Create a TCA select field for tt_content with 5 layout options. Include icons, default value, and proper labeling.
```

**TCA Group Field:**
```
Add a TCA group field to my model for selecting multiple pages. Include proper MM relation and maxitems configuration.
```

**TCA Inline (IRRE):**
```
Configure TCA inline relations for a parent-child relationship between Event and Ticket models. Include sorting, expand/collapse, and appearance options.
```

**FlexForm Configuration:**
```
Create a FlexForm for my plugin with tabs: General (items per page, sort order), Display (template selection, show images), and Filter (category selection).
```

**FlexForm with Database Records:**
```
Add a FlexForm field that allows selecting multiple news categories from the database. Use itemsProcFunc or foreign_table.
```

---

#### 🔗 Routing & Site Configuration

**Custom Route Enhancers:**
```
Create a route enhancer for my events plugin that generates URLs like /events/2024/01/my-event-title instead of ?tx_events[event]=123
```

**Localized Routes:**
```
Configure site routing for a multi-language site with German (de), English (en), and French (fr). Include language fallbacks and proper base paths.
```

**Static Routes:**
```
Add static routes for /sitemap.xml, /robots.txt, and a custom /api/* route that bypasses TYPO3's page handling.
```

---

#### 📁 File Handling (FAL)

**File Upload Processing:**
```
Create a service that processes uploaded images: resize to max 2000px, convert to WebP, and store in a specific folder with proper FAL references.
```

**File Metadata Extraction:**
```
Extract and store EXIF data from uploaded images: camera model, date taken, GPS coordinates. Update the sys_file_metadata table.
```

**Custom File Processor:**
```
Create a custom image processor that adds a watermark to images on-the-fly when requested with a specific processing instruction.
```

---

#### 🌐 Localization & Translation

**Multi-Language Content:**
```
Set up proper translation handling for my custom model. Include language overlay configuration, fallback types, and translation workflow.
```

**XLIFF Translations:**
```
Create XLIFF translation files for German, English, and French. Include pluralization rules and context descriptions for translators.
```

**Translation Sync:**
```
Create a command that synchronizes translations from a translation management system (like Phrase or Lokalise) into TYPO3 XLIFF files.
```

---

#### 📧 Forms & Email

**EXT:form Custom Finisher:**
```
Create a custom form finisher that sends data to a CRM API after form submission. Include error handling and logging.
```

**EXT:form Custom Validator:**
```
Create a custom form validator that checks if an email address is from an allowed domain list and not a disposable email provider.
```

**Email Template with Fluid:**
```
Create a styled HTML email template using Fluid that works across email clients. Include inline CSS, responsive design, and plain text fallback.
```

---

#### ⚡ Caching & Performance

**Custom Cache Configuration:**
```
Configure Redis caching for my extension with proper cache groups, lifetime settings, and cache tags for targeted invalidation.
```

**Cache Tags Strategy:**
```
Implement a caching strategy for my news listing that uses cache tags to invalidate only affected pages when a news item is updated.
```

**Performance Optimization:**
```
Analyze and optimize my TYPO3 site's performance: database queries, cache configuration, asset loading, and image optimization.
```

---

#### 🔐 Authentication & Permissions

**Frontend User Registration:**
```
Create a frontend user registration flow with email verification, password requirements, and custom fields. Handle fe_users and fe_groups.
```

**Backend User Permissions:**
```
Configure granular backend user permissions: restrict access to specific page trees, content types, and file mounts. Set up user groups properly.
```

**SSO Integration:**
```
Integrate SAML-based SSO for backend users using Azure AD or Okta. Include proper user provisioning and group mapping.
```

---

#### 🔌 API Development

**REST API Endpoint:**
```
Create a REST API endpoint for my Product model with GET (list/detail), POST (create), PUT (update), and DELETE operations. Include authentication.
```

**API Rate Limiting:**
```
Implement rate limiting for my API endpoints: 100 requests per minute per API key, with proper headers and error responses.
```

**Headless TYPO3:**
```
Configure TYPO3 for headless operation with JSON output. Set up content elements as JSON, configure CORS, and handle routing for a React/Vue frontend.
```

---

#### 🛠️ CLI Commands

**Custom CLI Command:**
```
Create a Symfony Console command for my extension that imports products from a CSV file. Include progress bar, dry-run mode, and validation.
```

**Scheduled Command:**
```
Create a CLI command that runs nightly to clean up expired records, send reminder emails, and generate reports. Include proper logging.
```

---

#### 📊 Logging & Debugging

**Custom Logger:**
```
Set up custom logging for my extension: separate log files, different log levels for dev/prod, and structured logging with context data.
```

**Debug Middleware:**
```
Create a debugging middleware that logs all requests with timing, memory usage, and database query counts in development mode.
```

**Error Handling:**
```
Implement proper error handling for my API: custom exceptions, error codes, meaningful messages, and integration with Sentry or similar.
```

---

#### 🎯 Common Tasks & Fixes

**Fix Broken Relations:**
```
My database has orphaned records and broken relations. Create a command that finds and optionally fixes these issues safely.
```

**Bulk Content Update:**
```
I need to update all tt_content records of a certain type: change a field value, update relations, and clear cache. Use DataHandler properly.
```

**Site Migration:**
```
Migrate content from an old TYPO3 v10 installation to v14. Map old content types to new ones, handle file references, and preserve URLs.
```

**Extension Conflicts:**
```
Debug conflicts between two extensions that both modify the same TCA or hook into the same events. Find the issue and suggest resolution.
```

**Database Optimization:**
```
Analyze my database for performance issues: missing indexes, large tables, unused fields. Suggest optimizations and create migration scripts.
```

---

#### 🚀 Deployment & DevOps

**Deployer Configuration:**
```
Create a Deployer configuration for deploying TYPO3 to staging and production servers. Include database sync, shared files, and rollback capability.
```

**GitHub Actions Deployment:**
```
Set up GitHub Actions for automated deployment: run tests on PR, deploy to staging on merge to develop, deploy to production on release tag.
```

**Docker Production Setup:**
```
Create a production-ready Docker setup for TYPO3: nginx, PHP-FPM, Redis, with proper health checks, logging, and security hardening.
```

### Discovery Commands

```bash
# List all installed skills (user-level)
ls ~/.claude/skills/

# List project-level skills
ls .cursor/skills/

# View a specific skill's content
cat ~/.claude/skills/typo3-ddev/SKILL.md

# Search for a keyword across all skills
grep -r "DataHandler" ~/.claude/skills/

# Re-install after pulling updates
./install.sh
```

### Pro Tips

1. **Use `/` to invoke skills** - Type `/typo3-content-blocks` in Agent chat
2. **Use trigger keywords naturally** - Just mention "ddev" or "datahandler" in your prompt
3. **Be explicit for complex tasks** - Start with "Using the security-audit skill..."
4. **Combine skills** - "Using typo3-rector and typo3-testing, upgrade my extension and add tests"
5. **Check the skill source** - Read `~/.claude/skills/*/SKILL.md` for full documentation
6. **View in settings** - Go to `Cursor Settings → Rules` to see all discovered skills

> **Note:** We bundled [Netresearch's excellent skills](https://github.com/netresearch) for quick installation.
> For deep methodology and the latest updates, check their original repositories.

## What's Included

### Agent Skills

| Skill | Purpose | Origin |
|-------|---------|--------|
| **TYPO3 Development** | | |
| `typo3-content-blocks` | Content Elements & Record Types with single source of truth | webconsulting |
| `typo3-datahandler` | Transactional database operations via DataHandler | Netresearch |
| `typo3-ddev` | Local DDEV development environment | Netresearch |
| `typo3-testing` | Unit, functional, E2E, architecture testing | Netresearch |
| `typo3-conformance` | Extension standards compliance checker | Netresearch |
| `typo3-docs` | Documentation using docs.typo3.org standards | Netresearch |
| `typo3-core-contributions` | TYPO3 Core contribution workflow (Gerrit, Forge) | Netresearch |
| **Upgrade & Migration** | | |
| `typo3-rector` | TYPO3 upgrade patterns with Rector | Netresearch |
| `typo3-update` | TYPO3 v13/v14 migration guide (prefers v14) | Netresearch |
| `typo3-extension-upgrade` | Systematic extension upgrades (Rector, Fractor) | Netresearch |
| **Security & Operations** | | |
| `typo3-security` | Security hardening checklist | Netresearch |
| `typo3-seo` | SEO configuration with EXT:seo | Netresearch |
| `ai-search-optimization` | AEO/GEO for AI search (schema, llms.txt, TYPO3, MDX) | webconsulting |
| `security-audit` | Security audit patterns (OWASP, XXE, SQLi, XSS) | Netresearch |
| `enterprise-readiness` | OpenSSF, SLSA, supply chain security | Netresearch |
| **PHP & Tools** | | |
| `php-modernization` | PHP 8.x patterns, PHPStan, DTOs, enums | Netresearch |
| `cli-tools` | CLI tool management and auto-installation | Netresearch |
| `context7` | Library documentation lookup via REST API | Netresearch |
| **WebConsulting Specific** | | |
| `webconsulting-branding` | Design tokens, MDX components, brand guidelines | webconsulting |
| `ui-design-patterns` | Practical UI design patterns, accessibility | webconsulting |

### Cursor Integration

- **Master Architect Rule**: Defines Claude as Senior TYPO3 Solutions Architect
- **MCP Configuration**: Placeholder for DDEV, Hetzner, and MySQL servers

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Cursor IDE / Claude Code                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌───────────┐  ┌───────────────┐  │
│  │   Agent Skills      │  │  AGENTS   │  │  MCP Servers  │  │
│  │  ~/.claude/skills/  │  │    .md    │  │               │  │
│  ├─────────────────────┤  ├───────────┤  ├───────────────┤  │
│  │ TYPO3 Development   │  │ Project   │  │ DDEV (local)  │  │
│  │ Upgrade & Migration │  │ Instruc-  │  │ Hetzner       │  │
│  │ Security & Ops      │  │ tions     │  │ MySQL         │  │
│  │ PHP & Tools         │  │           │  │ GitHub        │  │
│  │ WebConsulting       │  │           │  │ Firecrawl     │  │
│  └─────────────────────┘  └───────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘

Skills are auto-discovered from:
  ~/.claude/skills/    (user-level, unified for Cursor & Claude Code)
  .cursor/skills/      (project-level)
```

## Configuration

### MCP Servers

Edit `.cursor/mcp.json` to add your MCP server configurations:

```json
{
  "mcpServers": {
    "ddev": {
      "command": "npx",
      "args": ["-y", "@codingsasi/ddev-mcp"]
    },
    "hetzner": {
      "command": "npx",
      "args": ["-y", "mcp-hetzner"],
      "env": {
        "HCLOUD_TOKEN": "${HCLOUD_TOKEN}"
      }
    }
  }
}
```

### Updating Skills

```bash
# Pull latest changes
git pull origin main

# Re-run installation
./install.sh
```

## Technology Stack

- **PHP 8.2+** with strict types
- **TYPO3 v13/v14** (preferring v14)
- **DDEV** for local development
- **Hetzner Cloud** for hosting
- **Fluid/Twig** templating
- **TailwindCSS** for styling

## Excluded Technologies

This marketplace explicitly excludes:
- Go
- Jira
- Non-PHP backends

## Netresearch Skill Repositories

The following Netresearch repositories are the source for most skills:

- https://github.com/netresearch/typo3-ddev-skill
- https://github.com/netresearch/typo3-testing-skill
- https://github.com/netresearch/typo3-conformance-skill
- https://github.com/netresearch/typo3-docs-skill
- https://github.com/netresearch/typo3-core-contributions-skill
- https://github.com/netresearch/typo3-extension-upgrade-skill
- https://github.com/netresearch/security-audit-skill
- https://github.com/netresearch/enterprise-readiness-skill
- https://github.com/netresearch/php-modernization-skill
- https://github.com/netresearch/cli-tools-skill
- https://github.com/netresearch/context7-skill

## Contributing

1. Create a skill in `skills/your-skill-name/SKILL.md`
2. Follow the SKILL.md format (see existing skills)
3. Run `./install.sh` to test
4. Submit a pull request

## License

MIT License - webconsulting.at

## Acknowledgements

We are deeply grateful to **[Netresearch DTT GmbH](https://www.netresearch.de/)** for their
outstanding contributions to the TYPO3 community. Their excellent methodology and best practices
have been invaluable in shaping these guidelines.

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices
Adapted by webconsulting.at for this skill collection
