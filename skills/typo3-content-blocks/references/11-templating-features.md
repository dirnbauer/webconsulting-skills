# 11. Templating Features

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 11. Templating Features

### Accessing Data in Fluid

```html
<!-- Basic field access -->
{data.header}
{data.my_field}

<!-- Record metadata -->
{data.uid}
{data.pid}
{data.languageId}
{data.mainType}      <!-- Table name: tt_content -->
{data.recordType}    <!-- CType: myvendor_heroblock -->
{data.fullType}      <!-- tt_content.myvendor_heroblock -->

<!-- Raw database values -->
{data.rawRecord.some_field}

<!-- System properties -->
{data.systemProperties.createdAt}
{data.systemProperties.lastUpdatedAt}
{data.systemProperties.sorting}
{data.systemProperties.disabled}

<!-- Language info -->
{data.languageInfo.translationParent}
{data.languageInfo.translationSource}

<!-- Relations are auto-resolved! -->
<f:for each="{data.gallery_images}" as="image">
    <f:image image="{image}" width="400"/>
</f:for>

<!-- Nested collections -->
<f:for each="{data.accordion_items}" as="item">
    <h3>{item.title}</h3>
    <f:format.html>{item.content}</f:format.html>
</f:for>
```

### Asset ViewHelpers

```html
<!-- Include CSS from assets folder -->
<f:asset.css identifier="my-block-css" href="{cb:assetPath()}/frontend.css"/>

<!-- Include JS from assets folder -->
<f:asset.script identifier="my-block-js" src="{cb:assetPath()}/frontend.js"/>

<!-- Cross-block asset reference -->
<f:asset.css identifier="shared-css" href="{cb:assetPath(name: 'vendor/other-block')}/shared.css"/>
```

### Translation ViewHelper

```html
<!-- Access labels.xlf translations -->
<f:translate key="{cb:languagePath()}:my_label"/>

<!-- Cross-block translation -->
<f:translate key="{cb:languagePath(name: 'vendor/other-block')}:shared_label"/>
```
