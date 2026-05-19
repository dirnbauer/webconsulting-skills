# Verification Commands

Continues `typo3-translations` from [full guide](full-guide.md).

## Verification Commands

```bash
# XML well-formedness
find Resources ContentBlocks -name '*.xlf' -print0 2>/dev/null | xargs -0 -n1 xmllint --noout

# XLIFF versions
rg -n '<xliff version=' Resources ContentBlocks -S

# Translation consumers
rg -n 'LLL:|f:translate|translate\\(|sL\\(' Classes Configuration ContentBlocks Resources -S

# TYPO3 14 translation domains, when EXT:lowlevel is installed
php bin/typo3 language:domain:list
```

If `xmllint` is unavailable, use the project PHP runtime with `DOMDocument` to
parse changed files.
