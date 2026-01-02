# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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

[Unreleased]: https://github.com/dirnbauer/claude-cursor-typo3-skills/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/dirnbauer/claude-cursor-typo3-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/dirnbauer/claude-cursor-typo3-skills/releases/tag/v1.0.0

