# 8. Creating File Types (Extended Metadata)

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 8. Creating File Types (Extended Metadata)

> New in version 1.2

File Types extend the `sys_file_reference` table with custom fields – perfect for photographer credits, copyright notices, or additional reference-level options.

### Available File Type Names

| typeName | File Types |
|----------|------------|
| `image` | JPEG, PNG, GIF, WebP, SVG |
| `video` | MP4, WebM, OGG |
| `audio` | MP3, WAV, OGG |
| `text` | TXT, PDF, Markdown |
| `application` | ZIP, Office formats |

### Minimal File Type

```yaml
# EXT:my_sitepackage/ContentBlocks/FileTypes/image-extended/config.yaml
name: myvendor/image-extended
typeName: image
fields:
  - identifier: photographer
    type: Text
    label: Photographer
```

### Full File Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/FileTypes/image-extended/config.yaml
name: myvendor/image-extended
typeName: image
prefixFields: false  # Keep original column names
fields:
  - identifier: image_overlay_palette
    type: Palette
    label: 'LLL:EXT:core/Resources/Private/Language/locallang_tca.xlf:sys_file_reference.imageoverlayPalette'
    fields:
      # Reuse existing TYPO3 core fields
      - identifier: alternative
        useExistingField: true
      - identifier: description
        useExistingField: true
      - type: Linebreak
      - identifier: link
        useExistingField: true
      - identifier: title
        useExistingField: true
      - type: Linebreak
      # Custom fields
      - identifier: photographer
        type: Text
        label: Photographer
      - identifier: copyright
        type: Text
        label: Copyright Notice
      - identifier: source_url
        type: Link
        label: Source URL
      - type: Linebreak
      - identifier: crop
        useExistingField: true
```

### File Type Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `typeName` | string | ✓ | One of: `text`, `image`, `audio`, `video`, `application` |
| `prefixFields` | boolean | | Whether to prefix field identifiers with the Content Block name (often `false` for File Types to keep shared field names) |

### Use Cases for File Types

| Use Case | Fields to Add |
|----------|---------------|
| Photography agency | `photographer`, `copyright`, `license_type`, `expiry_date` |
| Video platform | `director`, `duration`, `transcript`, `subtitles` |
| Document management | `document_version`, `author`, `confidentiality` |
| E-commerce | `product_sku`, `variant_color`, `variant_size` |

### Accessing File Type Fields

In Fluid templates, access custom metadata through FAL references:

```html
<f:for each="{data.images}" as="image">
    <figure>
        <f:image image="{image}" alt="{image.alternative}"/>
        <f:if condition="{image.properties.photographer}">
            <figcaption>
                Photo: {image.properties.photographer}
                <f:if condition="{image.properties.copyright}">
                    | © {image.properties.copyright}
                </f:if>
            </figcaption>
        </f:if>
    </figure>
</f:for>
```
