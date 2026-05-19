# 6. TYPO3 v14 platform snapshot

Continues `typo3-rector` from [full guide](full-guide.md).

## 6. TYPO3 v14 platform snapshot

| Topic | TYPO3 v14 |
|-------|-----------|
| PHP | 8.2 minimum; 8.3/8.4 supported |
| PSR-14 events | Preferred over legacy hooks |
| ViewFactory | Preferred over removed StandaloneView patterns |
| Content Blocks | Current major aligned with v14 (see Packagist) |
| TCA | Static `Configuration/TCA` only — no runtime `$GLOBALS['TCA']` writes |
