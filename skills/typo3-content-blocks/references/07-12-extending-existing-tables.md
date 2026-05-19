# 12. Extending Existing Tables

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 12. Extending Existing Tables

Add custom types to existing tables (like `tx_news`):

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/custom-news/config.yaml
name: myvendor/custom-news
table: tx_news_domain_model_news
typeName: custom_news
fields:
  - identifier: title
    useExistingField: true
  - identifier: custom_field
    type: Text
```
