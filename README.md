# webconsulting skills - Claude Marketplace

A curated collection of **Agent Skills** for AI-augmented software development. These skills transform Claude into a specialized assistant for web development, video creation, security auditing, and enterprise software engineering.

> **Works with:** Claude Code, Cursor IDE (tested with Cursor 2.2+)

## Skill Categories

| Category | Skills | Description |
|----------|--------|-------------|
| **TYPO3 CMS** | 12 skills | Content Blocks, DataHandler, upgrades, testing, security |
| **Video & Animation** | 1 skill | Remotion video creation in React |
| **Security & Enterprise** | 4 skills | OWASP audits, deepfake detection, OpenSSF Scorecard, supply chain security |
| **Database** | 1 skill | Postgres performance, RLS, indexes, connection pooling (Supabase) |
| **Marketing** | 1 skill | CRO, copywriting, SEO, pricing, psychology (Corey Haines) |
| **PHP & Tools** | 5 skills | PHP 8.x modernization, CLI tools, documentation lookup, web scraping, skill creation |
| **Frontend & Design** | 6 skills | UI patterns, design systems, accessibility, OG images, React/Next.js performance, creative frontend design |
| **Documents & Office** | 1 skill | PDF, DOCX, PPTX, XLSX processing |
| **Legal & Compliance** | 4 skills | Impressum (AT, DE, EU, international) |
| **AI & SEO** | 2 skills | AEO/GEO for AI search visibility, agent readiness assessment |

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

### Option 1: Standalone Installation (Recommended)

```bash
# Clone the repository
git clone git@github.com:dirnbauer/webconsulting-skills.git
cd webconsulting-skills

# Install skills
chmod +x install.sh
./install.sh

# Restart Cursor IDE or Claude Code
```

### Option 2: Clone as Project Subdirectory

```bash
# From your project root
git clone git@github.com:dirnbauer/webconsulting-skills.git webconsulting-skills

# Install skills (auto-detects parent project)
cd webconsulting-skills
./install.sh

# Skills are installed to ~/.claude/skills/ AND your project's .cursor/
```

> The installer auto-detects if it's running from a vendor directory, project subdirectory, or standalone clone, and adjusts paths accordingly.

### Alternative: Composer from GitHub (VCS)

Install this skills package directly from GitHub without Packagist.

**1. Add the repository to your project's `composer.json`:**

```json
{
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/dirnbauer/webconsulting-skills"
        }
    ]
}
```

**2. Require the package:**

```bash
composer require --dev webconsulting/webconsulting-skills:dev-main
```

The Composer plugin will automatically run `install.sh` after installation to deploy skills to `~/.claude/skills/`.

## How to Use Agent Skills

### Skills for Dummies

**What are Agent Skills?** They're Markdown files (`SKILL.md`) containing expert knowledge that Claude reads to become a specialist. After running `./install.sh`, skills are installed to `~/.claude/skills/` and automatically discovered by both Cursor and Claude Code.

**How do they work?** 
- **Auto-applied**: Cursor's Agent decides when a skill is relevant based on your query
- **Manual invoke**: Type `/skill-name` in chat (e.g., `/remotion-best-practices`, `/security-audit`)
- **Trigger keywords**: Mentioning keywords like "video", "animation", "security audit", or "content-blocks" activates relevant skills

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
| `typo3-powermail` | powermail, mailform, form extension, tx_powermail | "Create a contact form with custom finisher" or "Configure spam shield" |
| `typo3-workspaces` | workspace, versioning, staging, publishing, draft content | "Set up workspace workflow" or "Debug workspace overlay" |
| `typo3-records-list-types` | records list types, grid view backend, compact view, teaser view | "Set Grid View as default" or "Create custom Timeline view" |
| `ai-search-optimization` | aeo, geo, ai search, chatgpt, llms.txt | "Optimize for ChatGPT and Perplexity citations" |
| `security-audit` | security audit, owasp, vulnerabilities | "Audit my controller for security issues" |
| `enterprise-readiness` | enterprise, openssf, slsa | "Assess my project for enterprise readiness" |
| `php-modernization` | php, phpstan, dto, enum | "Modernize my PHP code to 8.3 patterns" |
| `cli-tools` | cli, tools, command not found | "Install missing CLI tools" |
| `context7` | documentation, api, libraries | "Look up current Symfony documentation" |
| `webconsulting-branding` | branding, design, components | "Apply webconsulting design system" |
| `ui-design-patterns` | ui, design, layout, typography | "Improve the visual hierarchy of my UI" |
| `remotion-best-practices` | remotion, video, react, animation, composition | "Create a video intro with fade-in text animation" |
| `react-best-practices` | react, next.js, performance, optimization, bundle size, waterfalls | "Optimize this React component" or "Eliminate request waterfalls" |
| `deepfake-detection` | deepfake, media forensics, fake detection, synthetic media, prnu | "Verify authenticity of this video" or "Detect AI-generated images" |
| `readiness-report` | /readiness-report, agent readiness, codebase maturity | "Run /readiness-report to evaluate this repository" |
| `postgres-best-practices` | postgres, sql, database, query, index, rls, supabase | "Optimize this slow Postgres query" or "Set up RLS for multi-tenant" |
| `marketing-skills` | marketing, cro, conversion, landing page, pricing | "Optimize this landing page" or "Write homepage copy" |
| `og-image` | og-image, open graph, social preview, twitter card, meta tags | "Generate an OG image" or "Set up Twitter card meta tags" |
| `frontend-design` | frontend, design, creative, beautiful, distinctive, aesthetics | "Create a distinctive landing page" or "Design a dark tech hero section" |
| `web-design-guidelines` | web design, accessibility, a11y, wcag, aria, semantic html | "Review this component for accessibility issues" or "Audit my form for WCAG" |
| `document-processing` | pdf, docx, word, pptx, powerpoint, xlsx, excel | "Extract text from this PDF" or "Create an Excel model with formulas" |
| `firecrawl` | scrape, crawl, search web, research, fetch url | "Search the web for..." or "Scrape this page" |
| `skill-creator` | create skill, new skill, skill creator, package skill, SKILL.md | "Create a new skill for database migrations" or "Package my skill" |
| `android-design` | android, material design, jetpack compose, material you | "Review my Android app for Material Design" |
| `ios-design` | ios, iphone, swiftui, dynamic type, dark mode | "Review my iOS app for HIG compliance" |
| `ipados-design` | ipad, ipados, split view, stage manager, sidebar | "Add keyboard shortcuts to my iPad app" |
| `macos-design` | macos, mac app, appkit, menu bar, toolbar | "Create a Mac app with proper menu bar" |
| `tvos-design` | tvos, apple tv, siri remote, focus navigation | "Design 10-foot UI for Apple TV" |
| `visionos-design` | visionos, vision pro, spatial computing | "Design spatial UI for Vision Pro" |
| `watchos-design` | watchos, apple watch, complications, digital crown | "Create glanceable watchOS interface" |
| `web-platform-design` | wcag, web platform, responsive, accessibility, i18n | "Audit my web app for WCAG 2.2" |
| `ab-testing` | ab test, split test, experiment, hypothesis | "Design A/B test for my homepage" |
| `cro-funnel` | cro funnel, form cro, signup flow, onboarding, paywall | "Optimize my signup flow" |
| `programmatic-seo` | programmatic seo, template pages, directory, location pages | "Build [service] in [city] pages at scale" |
| `launch-strategy` | product launch, product hunt, gtm, beta launch | "Plan my Product Hunt launch" |

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

#### ✨ Creative Frontend Design (frontend-design)

The `frontend-design` skill helps you create **distinctive, memorable interfaces** that avoid generic "AI slop" aesthetics. It covers typography, color, motion, spatial composition, and component design.

**Distinctive Landing Pages:**

```
Create a landing page that looks nothing like a typical SaaS template. Use bold typography, asymmetric layout, and a unique color palette.
```

```
Design a dark-mode landing page with a gradient mesh background, floating elements, and glass morphism cards.
```

```
Build a brutalist-style landing page with raw aesthetics, monospace fonts, and intentional visual tension.
```

**Typography That Stands Out:**

```
Suggest distinctive font pairings for my tech startup. Avoid Inter, Roboto, and other overused fonts.
```

```
Create a typography system with a display font for headlines and a body font that pairs well. Show me the CSS variables.
```

```
Design a heading hierarchy with variable font weights, tight letter-spacing, and optical sizing.
```

**Color Palettes:**

```
Create a cohesive color palette for a fintech app. Use a dominant color for 60%, secondary for 30%, and accent for 10%.
```

```
Design a dark theme color system with proper contrast ratios, surface elevation colors, and accent states.
```

```
Generate a color palette inspired by [brand/concept]. Include semantic colors for success, warning, error states.
```

**Hero Sections:**

```
Create a hero section with a diagonal split layout, bold headline on the left, and product screenshot on the right.
```

```
Design a full-screen hero with animated gradient background, centered headline with letter-by-letter animation.
```

```
Build a hero with parallax scrolling, floating UI elements, and a CTA that pulses subtly.
```

**Component Design:**

```
Create a pricing card with glass morphism effect, gradient border, and hover animation that lifts the card.
```

```
Design a testimonial carousel with asymmetric cards, large quotation marks, and smooth slide transitions.
```

```
Build a feature grid with icons that animate on hover, subtle shadows, and a staggered reveal animation.
```

**Motion & Animation:**

```
Add micro-interactions to my buttons: subtle scale on hover, satisfying click feedback, loading state animation.
```

```
Create a page transition effect with content that slides up and fades in as you scroll.
```

```
Design a navigation menu that morphs smoothly between mobile hamburger and desktop horizontal layout.
```

**Background Effects:**

```
Create a gradient mesh background using CSS that subtly animates and shifts colors.
```

```
Add a noise texture overlay to my dark sections for visual depth without looking dated.
```

```
Build an animated blob background that responds to mouse movement.
```

**Anti-AI-Slop Audit:**

```
Review my landing page for generic AI patterns. Check for: overused fonts, stock gradients, predictable layouts, bland copy.
```

```
Make this hero section more distinctive. It currently looks like every other SaaS landing page.
```

```
Audit my design for "AI slop" indicators and suggest specific improvements for each issue.
```

---

#### ♿ Web Accessibility Audit (web-design-guidelines)

The `web-design-guidelines` skill provides **WCAG 2.1 AA compliance checking**, semantic HTML validation, and accessibility best practices.

**Color & Contrast:**

```
Check all text colors in my CSS for WCAG 2.1 AA contrast compliance (4.5:1 for normal text, 3:1 for large text).
```

```
My brand color is #3B82F6. What's the minimum darkness needed for text on white background to pass WCAG AA?
```

```
Review my color palette for colorblind accessibility. Suggest alternatives for red/green combinations.
```

**Focus States:**

```
Audit my interactive elements for visible focus indicators. Show me how to add proper focus-visible styles.
```

```
My designer wants to remove focus outlines. Create accessible alternatives that still look good.
```

```
Add a skip link to my page header that becomes visible on focus.
```

**Form Accessibility:**

```
Review my form for accessibility issues: labels, error messages, required field indicators, and field grouping.
```

```
Make this form accessible: add proper labels, aria-describedby for help text, and live error announcements.
```

```
Create an accessible date picker pattern with keyboard navigation and screen reader support.
```

**Semantic HTML:**

```
Audit my page structure for semantic HTML issues. Check heading hierarchy, landmarks, and proper element usage.
```

```
Convert this div-soup navigation to proper semantic HTML with nav, ul, li, and a elements.
```

```
Review my table markup. Add proper headers, scope attributes, and caption for accessibility.
```

**ARIA Patterns:**

```
Implement an accessible modal dialog with proper focus trapping, escape key handling, and aria attributes.
```

```
Create accessible tabs with proper ARIA roles, keyboard navigation (arrow keys), and focus management.
```

```
Build an accessible accordion using details/summary with enhanced keyboard support and animations.
```

```
Add ARIA live regions to my notification system so screen readers announce new messages.
```

**Keyboard Navigation:**

```
Audit my page for keyboard accessibility. Check tab order, focus traps, and interactive element reachability.
```

```
My dropdown menu isn't keyboard accessible. Fix the tab order and add arrow key navigation.
```

```
Create a keyboard-navigable image gallery with arrow keys, escape to close, and focus restoration.
```

**Screen Reader Testing:**

```
What will a screen reader announce for this component? Check all interactive elements and dynamic content.
```

```
Add proper alt text to my images. Some are decorative, some are informational, some are functional.
```

```
Review my icon buttons. They need accessible names since they have no visible text.
```

**Responsive & Touch:**

```
Audit my touch targets for mobile accessibility. Minimum 44x44px with adequate spacing.
```

```
Check my responsive design for accessibility issues at different breakpoints and zoom levels.
```

```
Add prefers-reduced-motion support to my animations for users with vestibular disorders.
```

**Quick Accessibility Checklist:**

```
Run a full accessibility audit on my homepage. Check: color contrast, focus states, semantic HTML, ARIA, keyboard nav, and alt text.
```

```
Prepare my site for WCAG 2.1 AA compliance. Create a checklist of issues and fixes.
```

```
Review this component against WCAG success criteria and list all failures with fixes.
```

---

#### 📄 Document Processing (document-processing)

The `document-processing` skill handles **PDF, DOCX, PPTX, and XLSX** files — extraction, creation, editing, and analysis.

**PDF Text Extraction:**

```
Extract all text from this PDF while preserving structure (headings, paragraphs, lists).
```

```
Extract the table on page 3 of this PDF into a structured format I can use in code.
```

```
Extract text from this scanned PDF using OCR. The quality is poor, so maximize accuracy.
```

**PDF Creation:**

```
Create a PDF invoice with company header, line items table, and footer with payment terms.
```

```
Generate a PDF report from this data with charts, tables, and formatted sections.
```

```
Create a certificate PDF with a decorative border, centered text, and signature line.
```

**PDF Manipulation:**

```
Merge these 5 PDF files into one, maintaining bookmarks and page numbers.
```

```
Split this 100-page PDF into separate files, one per chapter (chapters start at pages 1, 23, 45, 67, 89).
```

```
Extract pages 10-25 from this PDF as a new file.
```

```
Rotate all landscape pages in this PDF to portrait orientation.
```

```
Add a watermark "CONFIDENTIAL" to every page of this PDF.
```

```
Password-protect this PDF with encryption.
```

**Word Document Processing:**

```
Extract all text from this DOCX file as plain markdown, preserving headings and lists.
```

```
Convert this Word document to clean markdown for use in my documentation site.
```

```
Create a Word document from this markdown content with proper heading styles.
```

```
Create a DOCX file with my report content, including a table of contents and page numbers.
```

**Word Document Editing:**

```
Find and replace all instances of "Company A" with "Company B" in this Word document.
```

```
Extract all tracked changes from this Word document and list them with authors and dates.
```

```
Accept all tracked changes in this document and save a clean version.
```

```
Add a comment to this Word document at the paragraph starting with "In conclusion..."
```

**PowerPoint Processing:**

```
Extract all text from this PowerPoint presentation, organized by slide.
```

```
Create a summary of this PPTX: slide titles, key bullet points, and speaker notes.
```

```
Convert this PowerPoint to a markdown outline for use in documentation.
```

**PowerPoint Creation:**

```
Create a PowerPoint presentation from this markdown outline. Use a clean, professional style.
```

```
Generate slides for my quarterly report: title slide, 4 content slides with charts, and summary slide.
```

```
Create a pitch deck with these sections: Problem, Solution, Market, Traction, Team, Ask.
```

**PowerPoint Editing:**

```
Replace all images in this PowerPoint with updated versions from this folder.
```

```
Update the footer on all slides to show "Q4 2026" instead of "Q3 2026".
```

```
Extract slide 5 as a high-resolution PNG image for use in marketing.
```

**Excel Data Analysis:**

```
Analyze this Excel file and summarize: row count, column names, data types, and any obvious issues.
```

```
Calculate summary statistics for the 'Revenue' column: sum, average, min, max, and standard deviation.
```

```
Find all duplicate rows in this Excel file based on the 'Email' column.
```

```
Create a pivot table summary: sales by region and product category.
```

**Excel Creation:**

```
Create an Excel file from this JSON data with proper column headers and formatting.
```

```
Generate an Excel report with these sheets: Summary, Details, Charts. Add formulas, not hardcoded values.
```

```
Create a budget spreadsheet with categories, monthly columns, and SUM formulas for totals.
```

**Excel Formulas & Formatting:**

```
Add formulas to this Excel file: column D should be C * B, and row 20 should sum each column.
```

```
Format this Excel file: header row bold with background color, currency format for money columns, alternating row colors.
```

```
Create a financial model with proper Excel standards: blue for inputs, black for formulas, green for outputs.
```

```
Add conditional formatting: highlight cells red if value is negative, green if above target.
```

**Excel Advanced:**

```
Create a dropdown list in column A that only allows values from the 'Categories' sheet.
```

```
Add data validation to the 'Date' column to only accept dates in 2026.
```

```
Create a chart from this data and embed it in the 'Dashboard' sheet.
```

```
Protect this worksheet but allow users to edit cells in the 'Input' range.
```

**Cross-Format Workflows:**

```
Convert this PDF report to an editable Word document, preserving formatting as much as possible.
```

```
Extract the tables from this PDF and save them as an Excel file.
```

```
Create a PowerPoint from the key findings in this Excel analysis.
```

```
Batch process all PDFs in this folder: extract text and save as individual markdown files.
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

#### 🎬 Video Creation with Remotion

**Basic Video Composition:**
```
Create a Remotion composition with a 1920x1080 video at 30fps, 5 seconds duration. Add a centered title that fades in.
```

**Animated Text Intro:**
```
Build a YouTube-style intro: logo zooms in with spring animation, title types in letter-by-letter, then both fade out.
```

**Audio Visualization:**
```
Create an audio visualizer that reacts to music. Use waveform data to animate bars that pulse with the beat.
```

**TikTok-Style Captions:**
```
Add TikTok-style word-by-word captions to my video. Highlight the current word, use a bold font, and add a subtle shadow.
```

**Scene Transitions:**
```
Create a video with 3 scenes using slide and fade transitions. Each scene has different background colors and centered text.
```

**3D Product Showcase:**
```
Build a 3D product rotation video using React Three Fiber. The product rotates 360° with smooth easing over 4 seconds.
```

**Data Visualization Video:**
```
Create an animated bar chart that grows from zero. Each bar animates in sequence with a spring effect. Add value labels.
```

**Video with Dynamic Duration:**
```
Create a Remotion composition where the duration is calculated based on the audio file length using calculateMetadata.
```

**GIF Integration:**
```
Embed an animated GIF into my Remotion video, synchronized with the timeline. Loop it 3 times during a 6-second segment.
```

**Lottie Animation:**
```
Add a Lottie animation to my video intro. Synchronize the Lottie playback with Remotion's frame timing.
```

**Custom Fonts:**
```
Load a custom Google Font (Inter) and a local font file (.woff2) for my video. Apply different weights to title and subtitle.
```

**Video Trimming:**
```
Embed an external video file, trim the first 2 seconds, and play it at 1.5x speed. Add a fade-out at the end.
```

**Thumbnail Generation:**
```
Create a Still composition for video thumbnails. Include the video title, a background image, and a play button overlay.
```

**Sequenced Animations:**
```
Create a sequence of 5 elements that animate in one after another with 0.5s delays. Use useCurrentFrame and interpolate.
```

**Spring Physics:**
```
Animate a bouncing ball using spring physics. Configure tension, friction, and mass for a realistic bounce effect.
```

---

#### 🖼️ OG Images & Social Sharing

**Generate OG Image:**
```
Create an OG image page for my Next.js app that matches my existing design system. Use my brand colors and fonts.
```

**Social Meta Tags:**
```
Configure all necessary Open Graph and Twitter card meta tags for my website. Include og:image at 1200x630.
```

**Screenshot OG Page:**
```
Navigate to my /og-image page, resize to 1200x630, and take a screenshot for use as og:image.
```

**Cache Busting:**
```
I've updated my OG image. How do I refresh the cache on Facebook, Twitter, and LinkedIn?
```

**Design Templates:**
```
Show me the different OG image design templates available: cosmic, editorial, brutalist, ethereal.
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

#### 🐘 Postgres & Supabase

**Optimize Slow Query:**
```
Optimize this slow Postgres query. Use EXPLAIN ANALYZE to identify bottlenecks and suggest proper indexes.
```

**Row Level Security Setup:**
```
Set up Row Level Security for my multi-tenant orders table. Users should only see their own orders. Use auth.uid() with proper caching.
```

**Connection Pooling:**
```
Configure PgBouncer connection pooling for my Supabase project. Recommend pool size based on 4GB RAM.
```

**Find Missing Indexes:**
```
Find all foreign key columns in my database that are missing indexes. Generate CREATE INDEX statements.
```

**Cursor Pagination:**
```
Convert my OFFSET-based pagination to cursor-based pagination for the products table. Handle multi-column sorting.
```

**Batch Operations:**
```
Optimize my bulk insert loop. Convert individual INSERTs to batched statements or COPY for better performance.
```

**RLS Performance:**
```
Review my RLS policies for performance issues. Wrap function calls in SELECT for caching and add proper indexes.
```

**JSONB Indexing:**
```
My JSONB queries on the products.attributes column are slow. Add the right index type (GIN vs expression index).
```

---

#### 📈 Marketing & Growth

**Landing Page CRO:**
```
Optimize this landing page for conversions. Analyze the value proposition, headline, CTAs, and social proof placement.
```

**Homepage Copywriting:**
```
Write homepage copy for my SaaS product that helps teams manage projects. Focus on clarity over cleverness.
```

**Headline Formulas:**
```
Generate 5 headline variations for my product using proven formulas. Product: email marketing tool for e-commerce.
```

**CTA Optimization:**
```
Improve these CTA buttons. Current: "Submit", "Learn More", "Sign Up". Make them value-focused.
```

**Pricing Strategy:**
```
Review my pricing page. I have 3 tiers at $29, $79, $199. Should the middle tier be recommended? How do I handle enterprise?
```

**Freemium vs Trial:**
```
Should I use freemium or free trial for my collaboration tool? What are the pros and cons of each?
```

**SEO Audit:**
```
Audit my site for SEO issues. Check technical SEO, on-page optimization, and content quality.
```

**Pricing Psychology:**
```
What psychological principles can I apply to my pricing page to increase conversions?
```

**Page Structure:**
```
Help me structure my landing page. What sections should I include and in what order?
```

**Objection Handling:**
```
What objections might visitors have on my pricing page and how should I address them?
```

**A/B Test Ideas:**
```
Suggest A/B test ideas for my homepage hero section. What should I test first?
```

**Social Proof Strategy:**
```
How should I incorporate social proof on my landing page? Where should logos, testimonials, and stats go?
```

---

#### ⚛️ React & Next.js Performance (Vercel Best Practices)

The `react-best-practices` skill contains **57 rules across 8 priority categories** from Vercel Engineering. It automatically detects performance anti-patterns and suggests fixes prioritized by impact.

**Why it's cool:** Instead of guessing what to optimize, you get Vercel's battle-tested rules applied automatically. The skill catches issues like request waterfalls, bundle bloat, and re-render storms that kill Core Web Vitals.

**Critical: Eliminate Waterfalls (Priority 1)**

```
I have this data fetching code that feels slow:

const user = await fetchUser(id);
const posts = await fetchPosts(userId);
const comments = await fetchComments(postId);

Why is it slow and how do I fix it?
```

```
Add Suspense boundaries to my Next.js page so the header shows immediately while data loads.
```

```
My API route awaits a database call early but only uses it in one branch. How do I defer the await?
```

**Critical: Bundle Size (Priority 2)**

```
My Next.js bundle is 2MB. Analyze my imports and find barrel file imports that pull in entire libraries.
```

```
I'm importing a heavy charting library. Show me how to use next/dynamic with a loading skeleton.
```

```
Move my analytics initialization to after hydration so it doesn't block the main bundle.
```

```
I have a feature flag that controls a heavy component. Only load the component when the flag is true.
```

**High: Server-Side Performance (Priority 3)**

```
I'm calling getUser() in multiple server components. Show me how to use React.cache() to deduplicate.
```

```
Restructure this server component to start fetches in the parent and await in children (parallel fetching).
```

```
I need to log analytics after responding. Use next/after() to make it non-blocking.
```

```
My server component passes a huge object to a client component. How do I minimize serialization?
```

**Medium-High: Client-Side Data Fetching (Priority 4)**

```
Convert my useEffect + useState data fetching to SWR for automatic deduplication and caching.
```

```
I'm adding scroll event listeners in multiple components. Show me how to deduplicate them.
```

```
Make my scroll listeners passive to improve scrolling performance.
```

**Medium: Re-render Optimization (Priority 5)**

```
This component re-renders every time state changes, but it only uses state in a callback. Fix it.
```

```
Extract my expensive list rendering into a memoized component.
```

```
My callback changes on every render because it references count. Use functional setState.
```

```
I'm computing derived state in useEffect. Show me how to derive it during render instead.
```

```
My search input lags because filtering is slow. Use startTransition for the non-urgent filter update.
```

```
I'm storing mouse position in state but I only use it in event handlers. Use a ref instead.
```

**Medium: Rendering Performance (Priority 6)**

```
I have a long list with 1000 items. Add content-visibility: auto for performance.
```

```
This static JSX is defined inside the component. Hoist it outside to avoid recreating.
```

```
I'm animating an SVG directly. Wrap it in a div and animate the wrapper instead.
```

```
I get hydration mismatch warnings for user-specific data. How do I handle client-only values?
```

**Low-Medium: JavaScript Performance (Priority 7)**

```
I'm setting multiple CSS properties in a loop. Batch them using cssText or a class.
```

```
I'm doing array.includes() in a loop. Build a Set for O(1) lookups.
```

```
I'm accessing object.nested.value repeatedly in a loop. Cache it in a variable.
```

```
I have filter().map().filter(). Combine into a single loop.
```

```
This function sorts an array just to find the max. Use a loop instead.
```

**Advanced Patterns (Priority 8)**

```
My event handler function changes every render. Store it in a ref for stable reference.
```

```
I need to initialize an SDK once per app load, not per render. Show me the init-once pattern.
```

---

#### 🔬 Media Forensics & Deepfake Detection

**Verify Media Authenticity:**
```
Verify authenticity of this video before publication. Check for temporal inconsistencies, face swap artifacts, and synthetic speech patterns.
```

**Detect AI-Generated Images:**
```
Is this image AI-generated? Check for diffusion model artifacts, GAN fingerprints, and semantic inconsistencies.
```

**PRNU Analysis:**
```
Analyze PRNU/PCE sensor fingerprints to match this image to its claimed camera source.
```

**Content Provenance:**
```
Verify C2PA/CAI content provenance and check the cryptographic chain of custody for this media file.
```

**Forensic Report:**
```
Create a forensic report with authenticity grade (1-6) and confidence intervals for this video.
```

---

#### 📊 Agent Readiness Assessment

**Run Readiness Report:**
```
Run /readiness-report to evaluate this repository for AI-assisted development readiness.
```

**Identify Gaps:**
```
What gaps are preventing effective autonomous development in this codebase?
```

**Maturity Level:**
```
Check which maturity level (L1-L5) this repo achieves across the 9 technical pillars.
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

## What's Included

### Agent Skills

| Skill | Purpose | Origin |
|-------|---------|--------|
| **TYPO3 Development** | | |
| `typo3-content-blocks` | Content Elements & Record Types with single source of truth | webconsulting |
| `typo3-datahandler` | Transactional database operations via DataHandler | webconsulting |
| `typo3-ddev` | Local DDEV development environment | webconsulting |
| `typo3-testing` | Unit, functional, E2E, architecture testing | webconsulting |
| `typo3-conformance` | Extension standards compliance checker | webconsulting |
| `typo3-docs` | Documentation using docs.typo3.org standards | webconsulting |
| `typo3-core-contributions` | TYPO3 Core contribution workflow (Gerrit, Forge) | webconsulting |
| **Upgrade & Migration** | | |
| `typo3-rector` | TYPO3 upgrade patterns with Rector | webconsulting |
| `typo3-update` | TYPO3 v13/v14 migration guide (prefers v14) | webconsulting |
| `typo3-extension-upgrade` | Systematic extension upgrades (Rector, Fractor) | webconsulting |
| **Security & Operations** | | |
| `typo3-security` | Security hardening checklist | webconsulting |
| `typo3-seo` | SEO configuration with EXT:seo | webconsulting |
| `typo3-powermail` | Powermail 13+ forms, finishers, validators, events | webconsulting |
| `typo3-records-list-types` | Grid, Compact, Teaser view modes for Records module | webconsulting |
| `typo3-workspaces` | Workspaces versioning, staging, publishing workflows | webconsulting |
| `ai-search-optimization` | AEO/GEO for AI search (schema, llms.txt, TYPO3, MDX) | webconsulting |
| `security-audit` | Security audit patterns (OWASP, XXE, SQLi, XSS) | webconsulting |
| `security-incident-reporting` | NIST/SANS incident reports, DDoS post-mortem, CVE correlation | webconsulting |
| `deepfake-detection` | Multimodal media authentication, synthetic media forensics | webconsulting |
| `readiness-report` | AI agent readiness assessment (9 pillars, 5 maturity levels) | OpenHands |
| `enterprise-readiness` | OpenSSF, SLSA, supply chain security | webconsulting |
| **PHP & Tools** | | |
| `php-modernization` | PHP 8.x patterns, PHPStan, DTOs, enums | webconsulting |
| `cli-tools` | CLI tool management and auto-installation | webconsulting |
| `context7` | Library documentation lookup via REST API | webconsulting |
| `firecrawl` | Firecrawl CLI for web scraping, search, and research | Firecrawl |
| `skill-creator` | Guide for creating and packaging Agent Skills | Anthropic |
| **Database** | | |
| `postgres-best-practices` | Postgres performance, RLS, indexes, pooling | Supabase |
| **Marketing** | | |
| `marketing-skills` | CRO, copywriting, SEO, pricing, psychology | Corey Haines |
| **Frontend & Design** | | |
| `webconsulting-branding` | Design tokens, MDX components, brand guidelines | webconsulting |
| `ui-design-patterns` | Practical UI design patterns, accessibility | webconsulting |
| `frontend-design` | Distinctive UI aesthetics, anti-AI-slop patterns | Anthropic |
| `web-design-guidelines` | Interface review, WCAG, ARIA, accessibility | Vercel |
| `og-image` | Social preview images (Open Graph), meta tags, Twitter cards | Stevy Smith |
| `react-best-practices` | React/Next.js performance optimization (57 rules) | Vercel |
| **Documents & Office** | | |
| `document-processing` | PDF, DOCX, PPTX, XLSX creation, editing, analysis | Anthropic |
| **Video & Animation** | | |
| `remotion-best-practices` | Video creation in React with Remotion | remotion-dev |
| **Legal & Compliance** | | |
| `legal-impressum` | Austrian Impressum (all Gesellschaftsformen) | webconsulting |
| `legal-impressum/GERMANY` | German Impressum (DDG, MStV) | webconsulting |
| `legal-impressum/EU` | EU eCommerce Directive compliance | webconsulting |
| `legal-impressum/WORLD` | International (UK, CH, US) | webconsulting |
| **Platform Design** | | |
| `android-design` | Material Design 3, Jetpack Compose, dynamic color | ehmo |
| `ios-design` | Apple HIG for iPhone, SwiftUI, Dynamic Type | ehmo |
| `ipados-design` | Apple HIG for iPad, multitasking, pointer support | ehmo |
| `macos-design` | Apple HIG for Mac, menu bar, toolbars, shortcuts | ehmo |
| `tvos-design` | Apple HIG for Apple TV, focus navigation, 10-foot UI | ehmo |
| `visionos-design` | Apple HIG for Vision Pro, spatial UI, eye/hand input | ehmo |
| `watchos-design` | Apple HIG for Apple Watch, complications, glanceable UI | ehmo |
| `web-platform-design` | WCAG 2.2, responsive design, forms, typography, i18n | ehmo |
| **CRO & Growth** | | |
| `cro-funnel` | Full-funnel CRO: form, signup, onboarding, popup, paywall | AITYTech |
| `programmatic-seo` | SEO pages at scale with templates and data | AITYTech |
| `launch-strategy` | Product launches, Product Hunt, go-to-market | AITYTech |
| `ab-testing` | A/B test design, sample size, statistical significance | AITYTech |

### Skill Supplements

Most TYPO3 skills include additional supplement files:

| Supplement | Purpose |
|------------|---------|
| `SKILL-PHP84.md` | PHP 8.4 specific patterns: property hooks, asymmetric visibility, new array functions |
| `SKILL-CONTENT-BLOCKS.md` | Content Blocks integration: using Content Blocks with the skill's domain |

**Skills with supplements:**
- `php-modernization/SKILL-PHP84.md` - Comprehensive PHP 8.4 features reference
- `typo3-datahandler/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - DataHandler with PHP 8.4 and Content Blocks
- `typo3-ddev/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - DDEV PHP 8.4 config and CB development
- `typo3-testing/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Testing with PHP 8.4 and Content Blocks
- `typo3-rector/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Rector rules for PHP 8.4 and CB migration
- `typo3-update/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Upgrade strategies with PHP 8.4 and CB
- `typo3-extension-upgrade/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Extension upgrades
- `typo3-conformance/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Standards with PHP 8.4 and CB
- `typo3-security/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Security patterns
- `typo3-seo/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - SEO with structured data
- `typo3-docs/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Documenting PHP 8.4 and CB
- `typo3-core-contributions/SKILL-PHP84.md`, `SKILL-CONTENT-BLOCKS.md` - Core contributions

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
│  │ TYPO3 CMS           │  │ Project   │  │ DDEV (local)  │  │
│  │ Video & Animation   │  │ Instruc-  │  │ Hetzner       │  │
│  │ Security & Ops      │  │ tions     │  │ MySQL         │  │
│  │ PHP & Tools         │  │           │  │ GitHub        │  │
│  │ Frontend & Design   │  │           │  │ Context7      │  │
│  │ Legal & Compliance  │  │           │  │               │  │
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

**Quick Update (recommended):**

```bash
# Update everything in one command
./update.sh --pull

# Or step by step:
git pull origin main
./update.sh
```

**Using Composer:**

```bash
# Update skills via composer
composer skills:update

# Sync external skills only (no reinstall)
composer skills:sync

# List all available skills
composer skills:list

# Full reinstall
composer skills:install
```

**Update Script Options:**

```bash
./update.sh              # Sync external skills and reinstall
./update.sh --pull       # Pull git changes first, then update
./update.sh --sync-only  # Only sync external skills, don't reinstall
./update.sh --force      # Stash local changes if needed
./update.sh --dry-run    # Show what would be done without making changes
./update.sh --help       # Show all options
```

### GitHub Push -> skills.sh Publish (Checklist)

Use this simple flow to keep publication deterministic:

```bash
# 1) Push skill changes
git push origin main

# 2) Refresh imported skills if needed
./update.sh --sync-only

# 3) Regenerate local mirrors
./install.sh

# 4) Commit generated files and push
git add -A && git commit -m "chore: refresh generated skill mirrors" && git push
```

Then run the GitHub workflow `skills-sh-publish-check.yml` (manual dispatch) and verify your skill on skills.sh by searching for repository + skill name.

**Syncing External Skills:**

The `.sync-config.json` file defines external skill sources that are automatically synchronized:

```json
{
  "skills": [
    {
      "name": "react-best-practices",
      "source": "https://github.com/vercel-labs/agent-skills.git",
      "branch": "main",
      "path": "skills/react-best-practices",
      "enabled": true
    }
  ]
}
```

To enable/disable external skill syncing, edit `.sync-config.json` and set `enabled: true/false`.

> **Note:** The installer removes and recreates symlinks on each run, so running `./install.sh` or `./update.sh` after pulling always ensures your skills are up to date.

## Technology Stack

Skills in this collection cover:

- **PHP 8.2+** with strict types (PHP 8.4 supplements available)
- **TYPO3 v13/v14** for CMS projects
- **React/Remotion** for video creation
- **DDEV** for local development
- **Next.js/Astro** for frontend (AI Search Optimization)
- **TailwindCSS** for styling

## External Skill Repositories

The following repositories are the source for skills in this collection:

### Supabase (Postgres)
- https://github.com/supabase/agent-skills

### Corey Haines (Marketing)
- https://github.com/coreyhaines31/marketingskills

### Stevy Smith (OG Images)
- https://github.com/stevysmith/og-image-skill

### Vercel (React & Next.js)
- https://github.com/vercel-labs/agent-skills

### OpenHands (AI Readiness)
- https://github.com/OpenHands/skills

### Anthropic (Document Processing, Frontend Design & Skill Creator)
- https://github.com/anthropics/skills

## Contributing

1. Create a skill in `skills/your-skill-name/SKILL.md`
2. Follow the SKILL.md format (see existing skills)
3. Run `./install.sh` to test
4. Submit a pull request

## License

MIT License - webconsulting.at

## Acknowledgements

Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.

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
performance optimization guidelines. The `react-best-practices` skill is adapted from their
open-source repository: https://github.com/vercel-labs/agent-skills

**Copyright (c) Vercel, Inc.** - React and Next.js performance optimization (MIT License)
Adapted by webconsulting.at for this skill collection

