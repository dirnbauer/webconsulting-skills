# 8. Key ViewHelpers

Continues `typo3-powermail` from [full guide](full-guide.md).

## 8. Key ViewHelpers

### Validation

```html
<!-- Enable JS validation and/or AJAX submit -->
<vh:validation.enableJavascriptValidationAndAjax
    form="{form}"
    additionalAttributes="{...}" />

<!-- Validation data attributes on fields -->
<vh:validation.validationDataAttribute field="{field}" />

<!-- Error CSS class -->
<vh:validation.errorClass field="{field}" class="error" />

<!-- Upload attributes (accept, multiple) -->
<vh:validation.uploadAttributes field="{field}" />
```

### Form Fields

```html
<!-- Country selector -->
<vh:form.countries
    settings="{settings}"
    field="{field}"
    mail="{mail}" />

<!-- Advanced select with optgroups -->
<vh:form.advancedSelect
    field="{field}"
    mail="{mail}" />

<!-- Multi-upload -->
<vh:form.multiUpload field="{field}" />
```

### Prefill

```html
<!-- Prefill single-value field -->
<vh:misc.prefillField field="{field}" mail="{mail}" />

<!-- Prefill multi-value field (select, check, radio) -->
<vh:misc.prefillMultiField field="{field}" mail="{mail}" cycle="{cycle}" />
```

### Conditions

```html
<!-- Check if field is not empty -->
<vh:condition.isNotEmpty val="{value}">
    <f:then>Has value</f:then>
</vh:condition.isNotEmpty>

<!-- Check if array -->
<vh:condition.isArray val="{value}">
    <f:then>Is array</f:then>
</vh:condition.isArray>

<!-- Check file exists -->
<vh:condition.fileExists file="{path}">
    <f:then>File available</f:then>
</vh:condition.fileExists>
```

### Backend

```html
<!-- Edit link in backend module -->
<vh:be.editLink table="tx_powermail_domain_model_mail" uid="{mail.uid}">
    Edit
</vh:be.editLink>
```
