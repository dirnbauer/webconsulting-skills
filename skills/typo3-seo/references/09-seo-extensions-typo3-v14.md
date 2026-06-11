# 9. SEO Extensions (TYPO3 v14)

Continues `typo3-seo` from [full guide](full-guide.md).

## 9. SEO Extensions (TYPO3 v14)

### Recommended Extensions

| Extension | Purpose | TYPO3 v14 Support |
|-----------|---------|-----------------|
| `typo3/cms-seo` | Core SEO functionality | ✓ |
| `yoast-seo-for-typo3/yoast_seo` | Content analysis | ✓ — 12.1.0 (2026-05-08) declares `typo3/cms-core ^12.4.25 \|\| ^13.4 \|\| ^14.3` |
| `brotkrueml/schema` | Advanced structured data | ✓ (verify `require.typo3/cms-core` on Packagist) |
| `b13/seo_basics` | Legacy package (last targets old TYPO3) — **do not** treat as TYPO3 v14 default; prefer `typo3/cms-seo` |

> **Yoast SEO for TYPO3:** Since version 12.1.0 (2026-05-08), `yoast_seo` supports TYPO3 v14 (`typo3/cms-core ^12.4.25 || ^13.4 || ^14.3`). Require at least `^12.1` on v14 projects and verify the installed version's constraints on Packagist as usual.

### Schema Extension

```bash
ddev composer require brotkrueml/schema
ddev typo3 extension:setup -e schema
```

Pick a `brotkrueml/schema` version that explicitly supports your TYPO3 core release.

Features:
- Type-safe schema.org implementation
- WebPage, Organization, Article types
- Event and Product schemas
