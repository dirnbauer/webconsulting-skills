# 9. Troubleshooting

Continues `typo3-fractor` from [full guide](full-guide.md).

## 9. Troubleshooting

### Fractor Fails to Parse TypoScript

```bash
# Check for syntax errors in TypoScript first
# Fractor uses helmich/typo3-typoscript-parser which requires valid TypoScript

# Skip problematic files
vendor/bin/fractor process --dry-run
# Then add them to withSkip() in fractor.php
```

### FlexForm Changes Not Applied

```bash
# Ensure XML files are in the configured paths
# Check ALLOWED_FILE_EXTENSIONS includes 'xml'
# Verify the FlexForm has the expected structure (<T3DataStructure>)
```

### Formatting Changes Unexpected

```bash
# Configure code style explicitly in fractor.php
# Use 'auto' indent detection to preserve existing formatting
# Review withOptions() settings
```

### Running Fractor in CI

```yaml
# .github/workflows/fractor.yml
- name: Check Fractor
  run: vendor/bin/fractor process --dry-run
  # Fails if any rules would apply = outdated code
```
