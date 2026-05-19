# 18. Package Management for v14 Compatibility

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 18. Package Management for v14 Compatibility

If extensions don't support TYPO3 v14 yet, fork and update:

```bash
# Add private fork as VCS repository in composer.json
# Then update extension for v14 using typo3-rector and typo3-update skills
```

Required private forks for webconsulting stack:
- `webprofil/wp-t3monitoring-client` (^13 → ^14)
- `webprofil/deployer` (^13 → ^14)
- `webprofil/crawler` (^1.0 → compatible with v14)
- `webprofil/make` (^1.1 → compatible with v14)

---
