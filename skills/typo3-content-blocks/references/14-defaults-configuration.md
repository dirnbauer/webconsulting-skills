# 14. Defaults Configuration

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 14. Defaults Configuration

Create a `content-blocks.yaml` in project root for default settings:

```yaml
# content-blocks.yaml
vendor: myvendor
extension: my_sitepackage
content-type: content-element
skeleton-path: content-blocks-skeleton

config:
  content-element:
    basics:
      - TYPO3/Header
      - TYPO3/Appearance
      - TYPO3/Links
      - TYPO3/Categories
    group: default
    prefixFields: true
    prefixType: full
  
  record-type:
    prefixFields: true
    prefixType: vendor
    vendorPrefix: tx_mysitepackage
```
