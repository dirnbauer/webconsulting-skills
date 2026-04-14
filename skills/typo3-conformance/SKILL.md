---
name: typo3-conformance
description: >-
  Use when assessing TYPO3 extension quality, conformance checking, standards
  compliance, modernization to v12/v13/v14, TER readiness, or best practices
  review. Also triggers on: extension audit, quality score, full assessment,
  fix all findings, conformance audit, Bootstrap 5 migration, CSP compliance,
  ViewHelper security, XLIFF hygiene, PHP 8.4/8.5 compat.
metadata:
  version: "2.10.0"
  repository: "https://github.com/netresearch/typo3-conformance-skill"
  author: "Netresearch DTT GmbH"
---

# TYPO3 Extension Conformance Checker

Evaluate TYPO3 extensions against TYPO3 coding standards, architecture patterns, and best practices.

## When to Use

- Assessing extension quality or TER readiness
- Generating scored conformance reports
- Planning modernization to v12/v13/v14

## Delegation

Testing -> `typo3-testing` | Docs -> `typo3-docs` | OpenSSF -> `enterprise-readiness`

## Workflow

### Step 0: Context

Read ext_emconf.php + composer.json to determine TYPO3/PHP version, extension type, scope.

### Steps 1-10: Checks

1. **Metadata** -- Extension key, TYPO3 version, type
2. **Structure** -- composer.json, ext_emconf.php, Classes/, Configuration/, Resources/
3. **Coding** -- strict_types, PSR-12, PHP 8.4 explicit nullable, PHP 8.5 float-to-int
4. **Prohibited** -- No `$GLOBALS`, no `GeneralUtility::makeInstance()` for services
5. **Architecture** -- Constructor DI, Services.yaml, PSR-14 events
6. **Backend** -- ES6 modules, Modal API, CSRF, CSP (v13+)
7. **Testing** -- PHPUnit, Playwright E2E, coverage >70%
8. **Practices** -- DDEV, runTests.sh, CI/CD, quality tools
9. **TER** -- Publish workflow, upload comment format
10. **Audit** -- PHPStan baseline, TCA searchFields/default_sortby, XLIFF completeness, cache has()+get() anti-pattern, Extbase query property names, multi-version adapters

### Step 11: Verify

Re-run after fixes. Document score delta (e.g., "58 -> 82").

## Quick Grep Recipes

```bash
# Missing strict_types
grep -rL 'strict_types' Classes/ --include='*.php'
# Prohibited $GLOBALS
grep -rn '\$GLOBALS' Classes/ --include='*.php'
# makeInstance for services
grep -rn 'GeneralUtility::makeInstance' Classes/ --include='*.php'
# PHP 8.4 implicit nullable (deprecated)
grep -rPn '\(\s*[A-Za-z\\]+\s+\$\w+\s*=\s*null' Classes/ --include='*.php' | grep -v '?'
# Cache has()+get() anti-pattern
grep -rn '->has(' Classes/ --include='*.php'
# ext_emconf must NOT have strict_types
grep -l 'strict_types' ext_emconf.php
# PHP 8.5 implicit float-to-int (deprecated)
grep -rn '(int)\s*\$' Classes/ --include='*.php'
# Bootstrap 4 data attributes in Fluid
grep -rn 'data-toggle\|data-dismiss\|data-ride' Resources/ --include='*.html'
```

## Scoring

**Base (0-100):** Architecture(20) + Guidelines(20) + PHP(20) + Testing(20) + Practices(20). Excellence bonus up to 22. Critical issues block regardless.

| Range | Level | Action |
|-------|-------|--------|
| 90+ | Excellent | Production/TER ready |
| 80-89 | Good | Minor fixes |
| 70-79 | Acceptable | Fix before release |
| 50-69 | Needs Work | Significant effort |
| <50 | Critical | Block deployment |

## References

- `references/extension-architecture.md` -- Structure, required files
- `references/coding-guidelines.md` -- PSR-12, naming, PHPStan
- `references/php-architecture.md` -- DI, events, middleware
- `references/testing-standards.md` -- PHPUnit/Playwright
- `references/composer-validation.md` -- composer.json rules
- `references/ext-emconf-validation.md` -- TER fields
- `references/version-requirements.md` -- TYPO3/PHP compat
- `references/dual-version-compatibility.md` -- v12+v13
- `references/multi-version-dependency-compatibility.md` -- Adapter pattern
- `references/v13-deprecations.md` -- Migration paths
- `references/backend-module-v13.md` -- ES6, Modal, a11y
- `references/ter-publishing.md` -- TER workflow
- `references/report-template.md` -- Report format
- `references/excellence-indicators.md` -- Bonus scoring
- `references/best-practices.md` -- Organizational patterns

Asset templates in `assets/Build/`: PHPStan, PHP-CS-Fixer, Rector, ESLint, Stylelint, TypoScript lint.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-conformance-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
