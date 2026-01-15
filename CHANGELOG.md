# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

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

[Unreleased]: https://github.com/dirnbauer/claude-cursor-typo3-skills/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/dirnbauer/claude-cursor-typo3-skills/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/dirnbauer/claude-cursor-typo3-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/dirnbauer/claude-cursor-typo3-skills/releases/tag/v1.0.0

