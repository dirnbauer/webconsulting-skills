# Available Agent Skills

Auto-generated index of all available skills in this marketplace.

> **TYPO3 Compatibility:** All skills support TYPO3 v13.x and v14.x (v14 preferred)
> Code examples are designed to work on both versions simultaneously.

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
| `security-audit` | Security audit patterns (OWASP, XXE, SQLi, XSS, CVSS) | 1.0.0 | security, audit, owasp, vulnerabilities |
| `enterprise-readiness` | OpenSSF, SLSA, supply chain security, quality gates | 1.0.0 | enterprise, openssf, slsa, security |
| **PHP & Tools** | | | |
| `php-modernization` | PHP 8.x patterns, PHPStan level 10, DTOs, enums | 1.0.0 | php, modernization, phpstan, rector |
| `cli-tools` | CLI tool management and auto-installation | 1.0.0 | cli, tools, installation |
| `context7` | Library documentation lookup via REST API | 1.0.0 | documentation, api, libraries |
| **Frontend Development** | | | |
| `webconsulting-branding` | webconsulting.at design system, colors, typography, MDX | 1.0.0 | frontend, design, branding, ui |
| `ui-design-patterns` | Practical UI design patterns, accessibility, usability | 1.1.0 | ui, design, accessibility, usability |

## Skill Categories

### TYPO3 Development
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
- **security-audit**: Deep security audits aligned with OWASP Top 10
- **enterprise-readiness**: OpenSSF Scorecard, SLSA, supply chain security

### PHP & Tools
- **php-modernization**: PHP 8.x features, type safety, PHPStan level 10
- **cli-tools**: CLI tool management, auto-installation on "command not found"
- **context7**: Library documentation lookup via Context7 REST API

### Frontend Development
- **webconsulting-branding**: Design tokens, colors, typography, MDX components
- **ui-design-patterns**: Visual hierarchy, spacing, color, typography, accessibility

## Usage

Skills are automatically loaded by Claude when relevant keywords are detected in your query. You can also explicitly request a skill:

> "Using the typo3-datahandler skill, help me create a content element programmatically."

## Session Profiles

For optimal performance, limit active skills per session:

### Frontend Session
Active: `webconsulting-branding`, `ui-design-patterns`  
Use case: UI development, styling, component creation, visual design

### Backend Session
Active: `typo3-datahandler`, `typo3-ddev`, `typo3-update`, `typo3-testing`  
Use case: Extension development, database operations, v13/v14 compatible code

### Ops Session
Active: `typo3-security`, `security-audit`, `enterprise-readiness`, `typo3-ddev`  
Use case: Server configuration, deployment, hardening, security audits

### Upgrade Session
Active: `typo3-rector`, `typo3-update`, `typo3-extension-upgrade`, `php-modernization`  
Use case: TYPO3 version migrations, PHP upgrades, dual-version compatibility

### Documentation Session
Active: `typo3-docs`, `typo3-conformance`  
Use case: Extension documentation, quality assessment, standards compliance

### Core Contribution Session
Active: `typo3-core-contributions`, `typo3-testing`, `typo3-conformance`  
Use case: Contributing patches to TYPO3 Core via Gerrit

## Version Compatibility Matrix

| Skill | TYPO3 v13 | TYPO3 v14 | PHP 8.2 | PHP 8.3 | PHP 8.4 |
|-------|-----------|-----------|---------|---------|---------|
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
