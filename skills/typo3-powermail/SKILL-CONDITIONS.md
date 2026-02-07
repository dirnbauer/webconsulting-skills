---
name: typo3-powermail-conditions
description: Conditional field and page visibility for TYPO3 Powermail forms using powermail_cond. AJAX-based dynamic show/hide of fields and fieldsets based on user input with 10 comparison operators.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - powermail_cond
  - powermail condition
  - conditional fields
  - show hide fields
  - form conditions
  - in2code/powermail_cond
---

# Powermail Conditions (powermail_cond)

> **Compatibility:** TYPO3 v13.x with Powermail 13.x and powermail_cond 13.x
> **Requires:** `in2code/powermail: ^13.0`

## 1. Overview

`powermail_cond` adds dynamic conditional visibility to powermail forms. Fields or entire pages (fieldsets) can be shown/hidden based on user input, evaluated via AJAX in real-time.

### Installation

```bash
composer require in2code/powermail_cond
```

Include the static TypoScript template from `powermail_cond`.

### Architecture

```
ConditionContainer (tx_powermailcond_domain_model_conditioncontainer)
 └── Condition (tx_powermailcond_domain_model_condition)
      └── Rule (tx_powermailcond_domain_model_rule)
```

- **ConditionContainer**: Links to one powermail Form (1:1)
- **Condition**: Defines a target (field or page) and action (hide/unhide), contains rules with AND/OR conjunction
- **Rule**: Single comparison against a field value

## 2. Operators

| # | Operator | Description |
|---|----------|-------------|
| 0 | `is set` | Field has any value |
| 1 | `is not set` | Field is empty |
| 2 | `contains value` | Field value contains string |
| 3 | `contains value not` | Field value does not contain string |
| 4 | `is` | Field value equals string exactly |
| 5 | `is not` | Field value does not equal string |
| 6 | `is greater than` | Numeric comparison (numbers only) |
| 7 | `is less than` | Numeric comparison (numbers only) |
| 8 | `contains value from field` | Field value matches another field's value |
| 9 | `contains not value from field` | Field value differs from another field's value |

Operators 0-7 compare against a static string (`cond_string`).
Operators 8-9 compare against another form field (`equal_field`).

## 3. Backend Configuration

### Step 1: Create Condition Container

1. Go to a sysfolder (or the page with the form)
2. Create new record: **Condition Container**
3. Set **Title** and select the **Form**
4. Add **Conditions**

### Step 2: Configure Conditions

Each condition defines:

| Field | Description |
|-------|-------------|
| **Title** | Descriptive name |
| **Target Field** | Which field or page to affect |
| **Action** | `hide` (0) or `unhide` (1) |
| **Conjunction** | `OR` (any rule matches) or `AND` (all rules must match) |
| **Rules** | One or more comparison rules |

### Step 3: Configure Rules

Each rule defines:

| Field | Description |
|-------|-------------|
| **Title** | Descriptive name |
| **Start Field** | The field whose value is checked |
| **Operator** | One of the 10 operators above |
| **Condition String** | Static comparison value (operators 2-7) |
| **Equal Field** | Other field for comparison (operators 8-9) |

### Targeting Pages (Fieldsets)

To show/hide an entire page (fieldset), set the target field to the page. Pages appear in the target dropdown with a `fieldset:` prefix. When a page is hidden, all its fields are excluded from validation.

## 4. AJAX Endpoint

Conditions are evaluated server-side via TypeNum `3132`.

### TypoScript Setup (auto-included)

```typoscript
# TypeNum for AJAX condition evaluation
powermailCondition = PAGE
powermailCondition {
    typeNum = 3132
    config {
        disableAllHeaderCode = 1
        no_cache = 1
        additionalHeaders.10.header = Content-type: application/json
    }
    10 = USER
    10 {
        userFunc = TYPO3\CMS\Extbase\Core\Bootstrap->run
        extensionName = PowermailCond
        vendorName = In2code
        controller = Condition
        pluginName = Pi1
    }
}
```

### Route Enhancer for Clean URLs

```yaml
routeEnhancers:
  PageTypeSuffix:
    type: PageType
    default: /
    index: ''
    suffix: /
    map:
      condition.json: 3132
```

### JSON Response Format

```json
{
    "todo": {
        "42": {
            "1": {
                "email": {
                    "#action": "hide",
                    "matching_condition": { "5": "5" }
                },
                "#action": "un_hide"
            }
        }
    },
    "loops": 3,
    "loopLimit": 100
}
```

Structure: `todo[formUid][pageUid][fieldMarker]` or `todo[formUid][pageUid]` for page-level actions.

## 5. Reducing Flickering (Server-Side Prerendering)

By default, conditions are loaded via AJAX after page load, causing visible flickering. Prerender conditions server-side to avoid this.

### ViewHelper for Prerendering

Add to your copy of `EXT:powermail/Resources/Private/Templates/Form/Form.html`:

```html
{namespace pc=In2code\PowermailCond\ViewHelpers}

<!-- Prerender conditions as inline JSON -->
<script type="application/json" id="form-{form.uid}-actions">
    {pc:conditions(form:form) -> f:format.raw()}
</script>

<!-- Hide fieldsets until conditions are applied -->
<style type="text/css">
    .powermail_fieldset {
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.5s, visibility 0.5s;
    }
</style>
```

The JavaScript detects the prerendered JSON and skips the initial AJAX call.

## 6. File Upload Optimization

File upload fields send all selected files with every AJAX condition request. If you don't need conditions based on file uploads, exclude them:

```html
<f:form
    action="{action}"
    name="field"
    enctype="multipart/form-data"
    additionalAttributes="{vh:validation.enableJavascriptValidationAndAjax(
        form:form,
        additionalAttributes:{
            data-powermail-cond-excluded-fields: '.powermail_file'
        }
    )}"
>
```

## 7. Validator Integration (XCLASS)

powermail_cond XCLASSes powermail's `InputValidator` with `ConditionAwareValidator` to skip validation on hidden fields.

```php
// Registered in ext_localconf.php
$GLOBALS['TYPO3_CONF_VARS']['SYS']['Objects'][
    \In2code\Powermail\Domain\Validator\InputValidator::class
] = [
    'className' => \In2code\PowermailCond\Domain\Validator\ConditionAwareValidator::class,
];
```

Hidden field state is stored in the frontend user session under key `tx_powermail_cond`. The validator checks this session data before validating each field.

## 8. Extension Configuration

### Loop Count Safety

The condition container iterates until no changes occur. A safety limit prevents infinite loops.

| Setting | Default | Description |
|---------|---------|-------------|
| `conditionLoopCount` | 100 | Maximum iteration loops per evaluation |

Configure via Extension Manager or `ext_conf_template.txt`.

## 9. JavaScript Behavior

The frontend JavaScript (`PowermailCondition.min.js`) is auto-included via TypoScript:

```typoscript
page.includeJSFooter.powermailCond = EXT:powermail_cond/Resources/Public/JavaScript/PowermailCondition.min.js
page.includeJSFooter.powermailCond.defer = 1
```

### Behavior

- Listens to `change` events on all form fields (input, textarea, select)
- Sends form data to the condition endpoint via `fetch()`
- Applies hide/show actions via CSS classes (`powermail-cond-hidden`)
- Manages `required` attribute (removes on hidden fields, restores on show)
- Handles multi-step forms (`powermail_morestep`)
- Supports `pageshow` event (back/forward cache)

### CSS for Hidden Fields

```css
/* Applied by JavaScript */
.powermail-cond-hidden {
    display: none !important;
}
```

## 10. Known Limitations

- **Multi-step forms**: Cannot use powermail multi-step forms with powermail_cond
- **One container per form**: Each form can have exactly one condition container
- **XCLASS approach**: Only one extension can XCLASS `InputValidator` -- conflicts possible with other extensions modifying the same class
- **jQuery not required**: Since powermail_cond 10.0.0, vanilla JS is used (no jQuery dependency)

## 11. Common Patterns

### Show Field Based on Select Value

**Scenario**: Show "Other" text input when user selects "Other" in a dropdown.

1. Create Condition Container for the form
2. Add Condition:
   - Target: `other_details` field
   - Action: **hide** (hidden by default)
3. Add Rule:
   - Start field: `category` (the select field)
   - Operator: **is** (4)
   - Condition string: `Other`

The "other_details" field is hidden by default and only shown when "Other" is selected.

### Hide Page Based on Checkbox

**Scenario**: Hide an entire page/fieldset unless a checkbox is checked.

1. Add Condition:
   - Target: Page (fieldset) containing the additional fields
   - Action: **hide**
2. Add Rule:
   - Start field: `accept_terms` (checkbox)
   - Operator: **is not set** (1)

### Field-to-Field Comparison

**Scenario**: Show a warning field when two email fields don't match.

1. Add Condition:
   - Target: `email_mismatch_warning` field
   - Action: **unhide** (show when rule matches)
2. Add Rule:
   - Start field: `email`
   - Operator: **contains not value from field** (9)
   - Equal field: `email_repeat`

## 12. Database Structure

> **Note:** powermail_cond uses `l18n_parent` (not `l10n_parent`) for its translation pointer.
> Powermail core uses `l10n_parent`. Be careful with the naming difference.

### TYPO3 Standard Columns

All powermail_cond tables include these TYPO3-managed columns (not listed per table below):

| Column | Type | Purpose |
|--------|------|---------|
| `uid` | int AUTO_INCREMENT | Primary key |
| `pid` | int | Storage page UID |
| `tstamp` | int | Last modification timestamp |
| `crdate` | int | Creation timestamp |
| `deleted` | tinyint | Soft-delete flag |
| `hidden` | tinyint | Visibility flag |
| `sys_language_uid` | int | Language UID (0 = default) |
| `l18n_parent` | int | UID of the default language record |
| `l18n_diffsource` | mediumblob | Diff source for translation |
| `starttime` | int | Publish start |
| `endtime` | int | Publish end |

### tx_powermailcond_domain_model_conditioncontainer

| Column | Type | Description |
|--------|------|-------------|
| `title` | tinytext | Container title |
| `form` | int | Related powermail form UID (1:1) |
| `conditions` | int | IRRE children count |
| `note` | tinyint | Backend warning flag (>30 fields) |

**Relations:** `form` -> `tx_powermail_domain_model_form.uid`

### tx_powermailcond_domain_model_condition

| Column | Type | Description |
|--------|------|-------------|
| `conditioncontainer` | int | Parent container UID |
| `title` | tinytext | Condition title |
| `target_field` | tinytext | Target: field UID or `fieldset:PAGE_UID` |
| `actions` | tinytext | `0` = hide, `1` = unhide |
| `conjunction` | tinytext | `OR` or `AND` |
| `rules` | int | IRRE children count |

**Indexes:** `conditioncontainer`, `target_field(20)`
**Hidden table:** Yes (`hideTable => 1`) -- only editable inline inside container

### tx_powermailcond_domain_model_rule

| Column | Type | Description |
|--------|------|-------------|
| `conditions` | int | Parent condition UID |
| `title` | tinytext | Rule title |
| `start_field` | int | Source field UID (the field whose value is checked) |
| `ops` | int | Operator (0-9, see Section 2) |
| `cond_string` | text | Comparison value (operators 2-7) |
| `equal_field` | int | Comparison field UID (operators 8-9) |

**Indexes:** `conditions`, `start_field`, `equal_field`
**Hidden table:** Yes (`hideTable => 1`) -- only editable inline inside condition

### ER Diagram (Condition Relations)

```
tx_powermail_domain_model_form
  │ 1
  └──── 1 tx_powermailcond_domain_model_conditioncontainer (via form)
           │ 1
           └──── * tx_powermailcond_domain_model_condition (IRRE via conditioncontainer)
                    │ 1
                    └──── * tx_powermailcond_domain_model_rule (IRRE via conditions)
                              │
                              ├── start_field -> tx_powermail_domain_model_field.uid
                              └── equal_field -> tx_powermail_domain_model_field.uid (ops 8-9)
```

### target_field Format

The `target_field` column uses two formats:

| Format | Example | Meaning |
|--------|---------|---------|
| `{fieldUid}` | `42` | Target is a single field (UID 42) |
| `fieldset:{pageUid}` | `fieldset:5` | Target is an entire page/fieldset (page UID 5) |

## 13. Full Example: Multi-Step Shop with Conditions

> For a comprehensive example with Austrian legal types (Gesellschaftsformen),
> conditional fields per legal type, and two implementation approaches
> (DDEV SQL + DataHandler CLI command), see [SKILL-EXAMPLES.md](SKILL-EXAMPLES.md).
