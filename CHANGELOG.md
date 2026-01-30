# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **frontend-design**: Distinctive UI aesthetics from Anthropic
  - Anti-AI-slop patterns for memorable interfaces
  - Creative typography pairings (avoid Inter/Roboto/Arial)
  - Color palettes with dominant + accent approach
  - Motion design for high-impact moments
  - Component examples: dark tech hero, glass morphism cards, pricing cards
  - Quick reference CSS variables system

- **web-design-guidelines**: Interface review for accessibility from Vercel
  - WCAG 2.1 AA compliance checking
  - Semantic HTML validation patterns
  - ARIA patterns for common UI components
  - Keyboard navigation requirements
  - Focus states and color contrast guidelines
  - Quick checklist for pre-launch review

- **document-processing**: PDF, DOCX, PPTX, XLSX processing from Anthropic
  - PDF: pdfplumber text extraction, pypdf merge/split/rotate, reportlab creation, OCR with pytesseract
  - DOCX: pandoc conversion, docx-js creation, OOXML tracked changes workflow
  - PPTX: markitdown extraction, PptxGenJS creation, template workflows
  - XLSX: pandas analysis, openpyxl formulas, financial model standards

- **update.sh**: New update script for easy skill management
  - `--pull` flag to pull git changes before updating
  - `--sync-only` flag to only sync external skills
  - `--force` flag to stash local changes
  - `--dry-run` flag to preview changes
  - Automatic lastSync timestamp in .sync-config.json

### Changed

- **composer.json**: Added composer scripts for skill management
  - `composer skills:install` - Install skills to ~/.claude/skills
  - `composer skills:update` - Sync external skills and reinstall
  - `composer skills:sync` - Only sync external skills
  - `composer skills:list` - List all available skills

- **.sync-config.json**: Added external sources for new skills
  - web-design-guidelines from Vercel
  - Reference entries for Anthropic skills (disabled, using local versions)
  - Reference entries for marketing-skills (disabled, using local version with supplements)

- **AGENTS.md**: Updated with new skills
  - Added frontend-design, web-design-guidelines, document-processing to overview
  - Added example prompts for new skills
  - Added new session profiles (Creative Design, Accessibility Audit, Document Processing)
  - Updated compatibility matrix

- **README.md**: Updated documentation
  - Added new update script documentation
  - Added composer scripts documentation
  - Added sync-config.json documentation
  - Updated skill counts and categories
  - Added Anthropic to external skill sources

- **react-best-practices**: React and Next.js performance optimization from Vercel Engineering
  - 57 rules across 8 priority categories
  - Eliminating waterfalls (async/await patterns, Promise.all, Suspense)
  - Bundle size optimization (barrel imports, dynamic imports, defer third-party)
  - Server-side performance (React.cache, parallel fetching, after() API)
  - Client-side data fetching (SWR, event listeners, passive listeners)
  - Re-render optimization (memo, functional setState, useTransition, refs)
  - Rendering performance (content-visibility, hydration, Activity component)
  - JavaScript performance (batching, caching, Set/Map lookups)
  - Advanced patterns (event handler refs, init once, useLatest)

- **readiness-report**: AI agent readiness assessment from OpenHands
  - 9 technical pillars: Style, Build, Testing, Docs, DevEnv, Debugging, Security, Tasks, Analytics
  - 5 maturity levels (L1 Sandbox to L5 Collaborative)
  - Automated repository analysis scripts
  - Prioritized recommendations for improving agent readiness

- **security-incident-reporting**: Security incident documentation templates
  - NIST/SANS incident report structure
  - DDoS post-mortem templates with timeline documentation
  - CVE correlation and MITRE ATT&CK TTP mapping
  - Blameless root cause analysis (5-Whys)
  - SKILL-TYPO3.md: TYPO3 forensics, Security Team communication, PGP templates

- **firecrawl**: LLM-optimized web scraping and research from Mendable AI
  - Replaces built-in WebFetch/WebSearch with superior accuracy
  - Clean markdown output optimized for LLM context windows
  - JavaScript rendering and common block bypass
  - Web, image, and news search with time/location filters
  - Site mapping and URL discovery
  - Parallel scraping with automatic rate limiting
  - Search AND scrape in single operation

### Changed

- **install.sh**: Improved project root detection with 4-tier priority:
  1. Composer vendor install (`vendor/webconsulting/webconsulting-skills`)
  2. Subdirectory of project (`project/webconsulting-skills/`)
  3. Current working directory (if has `composer.json`)
  4. Script directory (fallback)

- **README.md**: Updated installation instructions
  - Split Quick Start into "Standalone" and "Clone as Subdirectory" options
  - Added pre-pull steps (git stash) to Updating Skills section
  - Added note about symlink recreation behavior

### Added

- **marketing-skills**: Marketing skills collection from Corey Haines
  - CRO: Page conversion rate optimization framework
  - Copywriting: Headlines, CTAs, page structure, copy formulas
  - SEO: Technical and on-page SEO audit checklist
  - Psychology: 70+ mental models for marketing and persuasion
  - Pricing: Pricing strategy, tiers, value metrics, freemium vs trial

- **postgres-best-practices**: Postgres performance optimization skill from Supabase
  - Query performance: indexes, composite indexes, covering indexes, partial indexes
  - Connection management: pooling, limits, idle timeouts
  - Security & RLS: Row Level Security patterns, auth.uid() optimization, least privilege
  - Schema design: data types, FK indexes, partitioning, primary key strategies
  - Concurrency & locking: short transactions, deadlock prevention, SKIP LOCKED
  - Data access patterns: batch inserts, N+1 elimination, cursor pagination, UPSERT
  - Monitoring: pg_stat_statements, EXPLAIN ANALYZE, autovacuum tuning
  - Advanced features: JSONB indexes, full-text search with tsvector
  - SKILL-SUPABASE.md supplement: auth.uid(), Edge Functions, MCP server, Realtime

- **deepfake-detection**: Multimodal media authentication and synthetic media forensics
  - PRNU/PCE sensor fingerprint analysis
  - IGH classification for GAN detection
  - DQ probability maps for splicing detection
  - Semantic forensics (shadows, reflections, physics)
  - C2PA/CAI content provenance verification
  - Voice clone detection patterns
  - LLM-augmented sensemaking for post-empirical media

- **ai-search-optimization**: New skill for AI search visibility (AEO/GEO)
  - Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) strategies
  - Schema.org markup (FAQPage, Article, HowTo, Organization) with sourced statistics
  - E-E-A-T signals for AI trust and domain authority
  - robots.txt configuration for AI crawlers (GPTBot, PerplexityBot, ClaudeBot)
  - Content freshness strategies by platform (Perplexity, ChatGPT, Google AI)
  - AI search visibility monitoring tools reference
  - TYPO3 implementation with EXT:schema and EXT:ai_llms_txt (v13/v14)
  - Markdown/MDX implementation (Next.js, Astro) with JSON-LD components
  - llms.txt specification and implementation guide
  - Raw MDX view with URL parameters (.md suffix, ?raw=true)

## [3.0.0] - 2026-01-04

### Added

- **11 new skills from Netresearch** - Major expansion of skill library
  - `context7`: Library documentation lookup via Context7 REST API
  - `cli-tools`: CLI tool management and auto-installation
  - `security-audit`: Security audit patterns (OWASP, XXE, SQLi, XSS, CVSS)
  - `typo3-conformance`: Extension standards compliance checker
  - `enterprise-readiness`: OpenSSF, SLSA, supply chain security
  - `typo3-testing`: Unit, functional, E2E, architecture, mutation testing
  - `typo3-extension-upgrade`: Systematic extension upgrades (Rector, Fractor)
  - `typo3-docs`: Documentation using docs.typo3.org standards
  - `php-modernization`: PHP 8.x patterns, PHPStan level 10, DTOs, enums
  - `typo3-core-contributions`: TYPO3 Core contribution workflow (Gerrit, Forge)

### Changed

- **README.md**: Added Netresearch attribution section, composer-agent-skill-plugin documentation, and links to original Netresearch repositories
- **AGENTS.md**: Reorganized with new skill categories, updated session profiles, expanded compatibility matrix
- **typo3-ddev**: Added multi-version testing section for extension development, container priority guidance

### Attribution

This release incorporates skills derived from [Netresearch DTT GmbH](https://github.com/netresearch). 
We recommend using their original repositories for the latest updates.

## [2.0.0] - 2026-01-02

### Changed

- **typo3-datahandler**: Command examples now use correct `move`/`copy` syntax. Clarified transaction guidance — DataHandler already wraps its own writes, outer transactions only needed when bundling adjacent operations on the same connection. See [`skills/typo3-datahandler/SKILL.md`](skills/typo3-datahandler/SKILL.md)

- **typo3-ddev**: Snapshot deletion now uses `ddev snapshot delete`. Added warning that "nuclear option" drops the database volume to prevent accidental data loss. See [`skills/typo3-ddev/SKILL.md`](skills/typo3-ddev/SKILL.md)

- **typo3-seo**: Robots.txt sitemap example now uses `{getEnv:TYPO3_SITE_URL}sitemap.xml` for accurate URLs matching site base instead of request host. See [`skills/typo3-seo/SKILL.md`](skills/typo3-seo/SKILL.md)

- **typo3-security**: Install Tool password guidance no longer shows empty placeholder. Now instructs setting hashed password per environment to prevent unsafe defaults. See [`skills/typo3-security/SKILL.md`](skills/typo3-security/SKILL.md)

## [1.0.0] - 2026-01-01

### Added

- Initial release with 7 agent skills
- `webconsulting-branding`: Design tokens, MDX components, brand guidelines
- `typo3-datahandler`: Transactional database operations via DataHandler
- `typo3-ddev`: Local DDEV development environment
- `typo3-seo`: SEO configuration with EXT:seo
- `typo3-security`: Security hardening checklist
- `typo3-rector`: TYPO3 upgrade patterns with Rector
- `typo3-update`: TYPO3 v13/v14 migration guide
- Cursor IDE integration with master architect rule
- Installation script (`install.sh`)

[Unreleased]: https://github.com/dirnbauer/webconsulting-skills/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/dirnbauer/webconsulting-skills/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/dirnbauer/webconsulting-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/dirnbauer/webconsulting-skills/releases/tag/v1.0.0

