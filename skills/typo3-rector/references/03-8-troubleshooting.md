# 8. Troubleshooting

Continues `typo3-rector` from [full guide](full-guide.md).

## 8. Troubleshooting

### Rector Fails

```bash
# Clear Rector cache
rm -rf .rector_cache/

# Run with verbose output
ddev exec vendor/bin/rector process --dry-run -vvv
```

### Extension Incompatibility

Check for updates:

```bash
ddev composer outdated
ddev composer show -l
```

Search for TYPO3 v14-compatible alternatives on:
- https://extensions.typo3.org
- https://packagist.org

### Database Issues

```bash
# Core CLI: extension setup / schema alignment
ddev typo3 extension:setup --extension=my_extension

# `database:updateschema` is provided by helhum/typo3-console, not plain Core — only if installed:
#   ddev typo3 list | rg database
# ddev typo3 database:updateschema --verbose
```
