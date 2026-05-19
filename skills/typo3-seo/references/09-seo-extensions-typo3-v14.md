# 9. SEO Extensions (TYPO3 v14)

Continues `typo3-seo` from [full guide](full-guide.md).

## 9. SEO Extensions (TYPO3 v14)

### Recommended Extensions

| Extension | Purpose | TYPO3 v14 Support |
|-----------|---------|-----------------|
| `typo3/cms-seo` | Core SEO functionality | ✓ |
| `yoast-seo-for-typo3/yoast_seo` | Content analysis (historical) | **Verify Packagist** — current 11.x lines target up to **TYPO3 13.4** in published constraints; **no `^14` until declared** |
| `brotkrueml/schema` | Advanced structured data | ✓ (verify `require.typo3/cms-core` on Packagist) |
| `b13/seo_basics` | Legacy package (last targets old TYPO3) — **do not** treat as TYPO3 v14 default; prefer `typo3/cms-seo` |

> **Yoast SEO for TYPO3:** If you need readability scoring on v14, use Core/`cms-seo` features, `brotkrueml/schema`, or another extension that **explicitly** declares `typo3/cms-core: ^14` on Packagist — do not rely on `yoast_seo` without confirming constraints.

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
