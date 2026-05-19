# 16. Troubleshooting

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 16. Troubleshooting

### Content Block Not Appearing

```bash
# Clear all caches
ddev typo3 cache:flush

# Rebuild class loading
ddev composer dump-autoload

# Check extension setup
ddev typo3 extension:setup --extension=my_sitepackage
```

### Database Errors

```bash
# Update database schema (Core)
ddev typo3 extension:setup --extension=my_sitepackage
# With typo3-console only: ddev typo3 database:updateschema

# Or use Compare Tool
# Admin Tools > Maintenance > Analyze Database Structure
```

### Field Not Saving

- Check field identifier is unique (use prefixing)
- Verify field type is correct
- Check for typos in config.yaml
- Ensure labels.xlf has matching keys
