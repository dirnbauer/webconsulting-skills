---
name: typo3-security-content-blocks
description: Security considerations for Content Blocks. Input validation, XSS prevention, and secure templating.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-security
  - typo3-content-blocks
triggers:
  - content blocks security
  - secure content blocks
---

# Content Blocks Security

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-security](./SKILL.md) - Main security guide
> - [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Content Blocks development

---

## 1. XSS Prevention in Templates

### Fluid Auto-Escaping

Content Blocks templates use Fluid, which auto-escapes by default:

```html
<!-- ✅ Safe: Auto-escaped -->
<h1>{data.header}</h1>
<p>{data.description}</p>

<!-- ⚠️ Dangerous: Raw output (only for trusted content) -->
<f:format.raw>{data.bodytext}</f:format.raw>
```

### When to Use Raw Output

```html
<!-- Only use f:format.raw for RTE content processed by TYPO3 -->
<f:if condition="{data.bodytext}">
    <div class="content">
        <f:format.html>{data.bodytext}</f:format.html>
    </div>
</f:if>
```

---

## 2. Link Security

### Safe Link Handling

```html
<!-- ✅ Safe: Use typolink ViewHelper -->
<f:link.typolink parameter="{data.link}" class="btn">
    {data.link_text}
</f:link.typolink>

<!-- ❌ Dangerous: Never use raw href -->
<a href="{data.link}">Link</a>
```

### External Link Validation

```yaml
# config.yaml - Restrict link types
fields:
  - identifier: external_link
    type: Link
    allowedTypes:
      - url
      - email
    # Prevent file:// and javascript: protocols
```

---

## 3. File Upload Security

### Restrict Allowed File Types

```yaml
# config.yaml
fields:
  - identifier: document
    type: File
    allowed: pdf,doc,docx
    disallowed: php,html,js,exe
    maxitems: 1
    
  - identifier: image
    type: File
    allowed: common-image-types
    maxitems: 5
```

### Validate in Template

```html
<f:for each="{data.document}" as="file">
    <f:if condition="{file.extension} == 'pdf'">
        <a href="{file.publicUrl}" download>
            {file.name}
        </a>
    </f:if>
</f:for>
```

---

## 4. Input Validation via TCA

Content Blocks inherits TYPO3 TCA validation:

```yaml
# config.yaml
fields:
  - identifier: email
    type: Email  # Built-in email validation

  - identifier: quantity
    type: Number
    range:
      lower: 1
      upper: 100

  - identifier: slug
    type: Slug
    generatorOptions:
      fields:
        - header
```

---

## 5. Backend Access Control

### Restrict Content Block Types

```yaml
# config.yaml
fields:
  - identifier: admin_only_field
    type: Text
    displayCond: 'USER:Vendor\MyExt\Condition->isAdmin'
```

### Type Access by User Group

```php
// Configuration/TCA/Overrides/tt_content.php
$GLOBALS['TCA']['tt_content']['types']['myvendor_sensitive']['access'] = 'admin';
```

---

## 6. Security Checklist

### Template Security
- [ ] No raw output for user input
- [ ] Use `f:format.html` only for RTE content
- [ ] Use typolink ViewHelpers for links
- [ ] Escape dynamic attributes

### Field Configuration
- [ ] Restrict file upload extensions
- [ ] Set appropriate maxitems limits
- [ ] Use proper field types (Email, Link)
- [ ] Add validation constraints

### Access Control
- [ ] Restrict sensitive fields by user group
- [ ] Limit backend access where needed

---

## References

- [typo3-security SKILL.md](./SKILL.md)
- [typo3-content-blocks SKILL.md](../typo3-content-blocks/SKILL.md)
- [Fluid Security](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/Index.html)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
