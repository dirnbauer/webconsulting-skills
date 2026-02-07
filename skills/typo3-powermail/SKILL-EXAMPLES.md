---
name: typo3-powermail-examples
description: Comprehensive multi-step shop form example with Austrian legal types, conditional fields, GDPR compliance, translations, workspace support, and two implementation approaches (DDEV SQL and DataHandler CLI command).
version: 1.1.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-powermail
  - typo3-ddev
  - typo3-datahandler
  - legal-impressum
triggers:
  - powermail example
  - powermail shop
  - powermail multi-step
  - powermail gesellschaftsform
  - powermail conditions example
  - powermail workspace
  - powermail draft
---

# Powermail Examples: Multi-Step Shop with Conditions

> **Related Skills:**
> - [SKILL.md](./SKILL.md) - Main Powermail guide
> - [SKILL-CONDITIONS.md](./SKILL-CONDITIONS.md) - Conditional fields
> - [typo3-ddev](../typo3-ddev/SKILL.md) - DDEV local development
> - [typo3-datahandler](../typo3-datahandler/SKILL.md) - DataHandler operations
> - [legal-impressum](../legal-impressum/SKILL.md) - Austrian Gesellschaftsformen

---

> **WARNING: LOCAL DEVELOPMENT ONLY**
>
> The SQL statements and CLI commands in this document insert test data directly
> into the database. **NEVER run these on a production site.** Use DDEV or a
> local development environment only. The data contains dummy records that will
> pollute a live database and may break existing forms.

---

## Scenario

A mini-shop order form with 4 steps:

1. **Rechtsform (Legal Type)**: User selects their Austrian Gesellschaftsform
2. **Kontaktdaten (Contact Data)**: Fields change dynamically based on legal type via powermail_cond
3. **Bestellübersicht (Order Overview)**: Summary and GDPR consent
4. **Bestätigung (Confirmation)**: Submit button

### Austrian Legal Types (Gesellschaftsformen)

| Key | German | Required Extra Fields |
|-----|--------|-----------------------|
| `einzelunternehmen` | Einzelunternehmen | Gewerbeberechtigung, WKO-Mitgliedsnr. |
| `eu` | Einzelunternehmen e.U. | Firmenbuchnummer, Firmenbuchgericht |
| `og` | OG (Offene Gesellschaft) | Firmenbuchnummer, Firmenbuchgericht, alle Gesellschafter |
| `kg` | KG (Kommanditgesellschaft) | Firmenbuchnummer, Firmenbuchgericht, Komplementär |
| `gmbh` | GmbH | Firmenbuchnummer, Firmenbuchgericht, Stammkapital, Geschäftsführer |
| `ag` | AG (Aktiengesellschaft) | Firmenbuchnummer, Firmenbuchgericht, Grundkapital, Vorstandsvorsitzender |
| `verein` | Verein | ZVR-Zahl, Vereinssitz, Obmann/Obfrau |
| `gesbr` | GesBR | Alle Gesellschafter (mind. 2) |

### Form Structure Overview

```
Form: "Bestellformular / Order Form"
├── Page 1: "Rechtsform" (Legal Type)
│   └── rechtsform (select) -- all Austrian types
│
├── Page 2: "Kontaktdaten" (Contact Data)
│   ├── firma (input) -- Company name [all types]
│   ├── anrede (select) -- Salutation [all types]
│   ├── vorname (input) -- First name [all types]
│   ├── nachname (input) -- Last name [all types]
│   ├── email (input) -- Email [all types]
│   ├── telefon (input) -- Phone [all types]
│   ├── strasse (input) -- Street [all types]
│   ├── plz (input) -- ZIP [all types]
│   ├── ort (input) -- City [all types]
│   ├── uid_nummer (input) -- UID/VAT number [all types]
│   │
│   ├── firmenbuchnummer (input)   -- [e.U., OG, KG, GmbH, AG]
│   ├── firmenbuchgericht (input)  -- [e.U., OG, KG, GmbH, AG]
│   ├── stammkapital (input)       -- [GmbH only]
│   ├── geschaeftsfuehrer (input)  -- [GmbH only]
│   ├── grundkapital (input)       -- [AG only]
│   ├── vorstandsvorsitzender (input) -- [AG only]
│   ├── gewerbeberechtigung (input) -- [Einzelunternehmen only]
│   ├── wko_mitgliedsnr (input)    -- [Einzelunternehmen only]
│   ├── gesellschafter (textarea)  -- [OG, GesBR]
│   ├── komplementaer (input)      -- [KG only]
│   ├── zvr_zahl (input)           -- [Verein only]
│   ├── vereinssitz (input)        -- [Verein only]
│   └── obmann (input)             -- [Verein only]
│
├── Page 3: "Bestellübersicht" (Order Overview)
│   ├── produkt1_info (html) -- Product 1: image + description
│   ├── produkt1_menge (input) -- Quantity (integer, validation=9)
│   ├── produkt2_info (html) -- Product 2: image + description
│   ├── produkt2_menge (input) -- Quantity (integer)
│   ├── produkt3_info (html) -- Product 3: image + description
│   ├── produkt3_menge (input) -- Quantity (integer)
│   ├── produkt4_info (html) -- Product 4: image + description
│   ├── produkt4_menge (input) -- Quantity (integer)
│   ├── anmerkungen (textarea) -- Notes
│   ├── agb (check) -- Terms & Conditions
│   ├── datenschutz (check) -- GDPR consent
│   └── widerruf (check) -- Right of withdrawal
│
└── Page 4: "Bestätigung" (Confirmation)
    ├── zusammenfassung (text) -- Summary text
    └── absenden (submit) -- Submit button
```

### Product Catalog

Each product is displayed as an HTML field (type `html`) with an Unsplash placeholder image, title, description, and price, followed by a quantity input (type `input`, integer validation).

| # | Marker (info) | Marker (qty) | Title (EN) | Title (DE) | Price |
|---|---------------|--------------|------------|------------|-------|
| 1 | `produkt1_info` | `produkt1_menge` | Website Basic | Website Basis | EUR 990 |
| 2 | `produkt2_info` | `produkt2_menge` | Website Professional | Website Professional | EUR 2.490 |
| 3 | `produkt3_info` | `produkt3_menge` | SEO Package | SEO-Paket | EUR 490/mo |
| 4 | `produkt4_info` | `produkt4_menge` | Maintenance Contract | Wartungsvertrag | EUR 190/mo |

**Product images** use Unsplash Source for dummy photos (do not use in production):

```
https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=250&fit=crop  (Website Basic)
https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=250&fit=crop  (Website Professional)
https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=400&h=250&fit=crop  (SEO Package)
https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400&h=250&fit=crop  (Maintenance)
```

---

## Approach 1: DDEV SQL (Direct Database Queries)

> **WARNING:** Raw SQL bypasses DataHandler. Use only for local testing.
> See [typo3-datahandler SKILL.md](../typo3-datahandler/SKILL.md) Section 1 for why.

> **Populated Database:** These queries work safely alongside existing powermail forms.
> All UID lookups use `SELECT ... WHERE marker = '...' AND page = @pageN_uid` scoped to
> the newly created page UIDs — they never collide with existing forms or fields.
> Steps 2 and 3 run in separate MySQL sessions and re-read UIDs via SELECT subqueries.

### SQL Column Reference

Before diving into the SQL, here's what each column means across the powermail tables:

#### `tx_powermail_domain_model_form` (Form)

| Column | Type | Description |
|--------|------|-------------|
| `pid` | int | **Storage page UID** — the TYPO3 page (sysfolder) where the record is stored |
| `title` | varchar | Form title shown in the backend module |
| `css` | varchar | CSS class added to the `<form>` tag for styling |
| `pages` | int | Number of pages in this form (auto-counted) |
| `sys_language_uid` | int | **Language ID**: `0` = default (English), `1` = first translation (German), etc. |
| `l10n_parent` | int | **Translation parent**: UID of the default-language record this is a translation of. `0` = this IS the default |
| `tstamp` | int | Last modification timestamp (Unix) |
| `crdate` | int | Creation timestamp (Unix) |

#### `tx_powermail_domain_model_page` (Form Page / Step)

| Column | Type | Description |
|--------|------|-------------|
| `pid` | int | Storage page UID |
| `form` | int | **Parent form UID** — which form this page belongs to |
| `title` | varchar | Page/step title shown as tab or step label |
| `css` | varchar | CSS class for this step container |
| `sorting` | int | **Display order** within the form (1 = first step, 2 = second, etc.) |
| `sys_language_uid` | int | Language ID (`0` = default) |
| `l10n_parent` | int | Translation parent UID (`0` = default language record) |

#### `tx_powermail_domain_model_field` (Form Field)

| Column | Type | Description |
|--------|------|-------------|
| `pid` | int | Storage page UID |
| `page` | int | **Parent page UID** — which form page this field belongs to |
| `title` | varchar | Field label shown to the user |
| `type` | varchar | **Field type**: `input`, `textarea`, `select`, `check`, `radio`, `submit`, `html`, `text`, `hidden`, `file`, `captcha`, etc. |
| `marker` | varchar | **Unique marker** — used in Fluid templates as `{marker}`, in email templates, and as CSS class. Must be unique within the form |
| `mandatory` | tinyint | `1` = required field, `0` = optional |
| `settings` | text | **Options for select/radio/check** — one option per line (`\n`-separated). Also used for prefill values |
| `sorting` | int | Display order within the page |
| `validation` | int | **Validation type**: `0` = none, `1` = email, `2` = URL, `3` = phone, `4` = numbers only, `9` = integer (custom), etc. |
| `validation_configuration` | varchar | Extra config for validation (e.g., min/max length) |
| `text` | text | **HTML content** for `type=html` or `type=text` fields — renders raw HTML or static text |
| `sender_name` | tinyint | `1` = use this field's value as the sender name in notification emails |
| `sender_email` | tinyint | `1` = use this field's value as the sender email (reply-to) in notifications |
| `sys_language_uid` | int | Language ID |
| `l10n_parent` | int | Translation parent UID |

#### `tx_powermailcond_domain_model_conditioncontainer` (Condition Container)

| Column | Type | Description |
|--------|------|-------------|
| `pid` | int | Storage page UID |
| `title` | varchar | Container name (for backend reference) |
| `form` | int | **Form UID** this container applies to |
| `conditions` | int | Number of conditions in this container |

#### `tx_powermailcond_domain_model_condition` (Condition)

| Column | Type | Description |
|--------|------|-------------|
| `pid` | int | Storage page UID |
| `conditioncontainer` | int | **Parent container UID** |
| `title` | varchar | Condition name (for backend reference) |
| `target_field` | varchar | **Field UID to show/hide** — the field affected by this condition (stored as string) |
| `actions` | varchar | **Action**: `0` = hide the target field when rules match, `1` = unhide (show) when rules match |
| `conjunction` | varchar | **Logic between rules**: `AND` = all rules must match, `OR` = any rule matches |
| `rules` | int | Number of rules in this condition |

#### `tx_powermailcond_domain_model_rule` (Condition Rule)

| Column | Type | Description |
|--------|------|-------------|
| `pid` | int | Storage page UID |
| `conditions` | int | **Parent condition UID** |
| `title` | varchar | Rule name (for backend reference) |
| `start_field` | int | **Source field UID** — the field whose value is checked (e.g., `rechtsform`) |
| `ops` | int | **Operator**: `0` = is set (not empty), `1` = is not set (empty), `2` = contains, `3` = not contains, `4` = is (exact match), `5` = is not (exact mismatch), `6` = greater than, `7` = less than, `8` = contains value from field, `9` = not contains value from field |
| `cond_string` | varchar | **Comparison value** — the string to compare against (e.g., `'GmbH'`, `'Verein'`) |

### Prerequisites

```bash
# Ensure DDEV is running with powermail + powermail_cond installed
ddev start
ddev composer require in2code/powermail in2code/powermail_cond
ddev typo3 cache:flush

# Verify tables exist
ddev mysql -e "SHOW TABLES LIKE 'tx_powermail%';"
ddev mysql -e "SHOW TABLES LIKE 'tx_powermailcond%';"
```

### Step 1: Create the Form (English, sys_language_uid=0)

```bash
ddev mysql -e "
-- =============================================
-- POWERMAIL SHOP FORM - English (default language)
-- Storage PID = 1 (adjust to your sysfolder UID)
-- sys_language_uid=0 means this is the DEFAULT language record
-- l10n_parent=0 means this is NOT a translation (it's the original)
-- =============================================

-- Create the form record (the top-level container for all pages and fields)
INSERT INTO tx_powermail_domain_model_form
  (pid, title, css, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, 'Order Form', 'order-form', 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
-- pid=1: store on page UID 1 | css='order-form': adds CSS class to <form> tag

-- Capture the auto-generated UID so we can reference it in page records
SET @form_uid = LAST_INSERT_ID();

-- Create 4 form pages (= steps in the multi-step wizard)
-- Each page's 'form' column links it to the parent form
-- 'sorting' determines the step order (1=first, 2=second, etc.)

-- Page 1: User selects their Austrian legal type (Gesellschaftsform)
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, css, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @form_uid, 'Legal Type', 'step-legal-type', 1, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @page1_uid = LAST_INSERT_ID();

-- Page 2: Contact details + conditional fields per legal type
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, css, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @form_uid, 'Contact Data', 'step-contact', 2, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @page2_uid = LAST_INSERT_ID();

-- Page 3: Product catalog (4 products) + notes + GDPR checkboxes
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, css, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @form_uid, 'Order Overview', 'step-overview', 3, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @page3_uid = LAST_INSERT_ID();

-- Page 4: Final confirmation with summary text and submit button
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, css, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @form_uid, 'Confirmation', 'step-confirm', 4, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @page4_uid = LAST_INSERT_ID();

-- Tell the form how many pages it has (used by backend display)
UPDATE tx_powermail_domain_model_form SET pages = 4 WHERE uid = @form_uid;

-- =============================================
-- PAGE 1 FIELDS: Legal Type Selection
-- =============================================
-- Each field's 'page' column links it to its parent page.
-- 'marker' is the unique identifier used in Fluid templates ({rechtsform}),
-- email templates, conditions, and CSS classes.
-- 'type' determines how the field renders (input, select, check, etc.)

-- Dropdown for selecting Austrian Gesellschaftsform (legal entity type)
-- type='select': renders a <select> dropdown
-- mandatory=1: field is required (form won't submit without it)
-- settings: one option per line (\n-separated), first option is the placeholder
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, settings, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page1_uid, 'Legal Type', 'select', 'rechtsform', 1,
   'Please select...\nEinzelunternehmen\nEinzelunternehmen e.U.\nOG (Offene Gesellschaft)\nKG (Kommanditgesellschaft)\nGmbH\nAG (Aktiengesellschaft)\nVerein\nGesBR',
   1, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
-- Save UID for use in conditions (powermail_cond checks this field's value)
SET @f_rechtsform = LAST_INSERT_ID();

-- =============================================
-- PAGE 2 FIELDS: Contact Data (common + conditional)
-- =============================================
-- These fields are split into two groups:
--   1. Common fields: always visible regardless of legal type
--   2. Conditional fields: shown/hidden by powermail_cond based on rechtsform selection

-- COMMON FIELDS (always visible for all legal types)
-- Bulk INSERT creates 10 fields at once. All use type='input' except anrede (select).
-- mandatory=1 means required, mandatory=0 means optional (telefon, uid_nummer).
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page2_uid, 'Company Name',  'input',    'firma',    1, 1,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Salutation',    'select',   'anrede',   1, 2,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'First Name',    'input',    'vorname',  1, 3,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Last Name',     'input',    'nachname', 1, 4,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Email',         'input',    'email',    1, 5,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Phone',         'input',    'telefon',  0, 6,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Street',        'input',    'strasse',  1, 7,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'ZIP',           'input',    'plz',      1, 8,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'City',          'input',    'ort',      1, 9,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'VAT Number',    'input',    'uid_nummer', 0, 10, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Look up UIDs of common fields by marker + page for later use in UPDATEs.
-- This is safe even with a populated database (scoped to our page UID).
SET @f_firma    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firma'      AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_anrede   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'anrede'     AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vorname  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vorname'    AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_email    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'email'      AND sys_language_uid = 0 AND page = @page2_uid);

-- Post-INSERT updates: set dropdown options and email/sender configuration
-- settings: dropdown options for salutation (one per line)
UPDATE tx_powermail_domain_model_field SET settings = 'Mr.\nMs.\nDiverse' WHERE uid = @f_anrede;
-- validation=1: enable email format validation | sender_email=1: use as reply-to in notification emails
UPDATE tx_powermail_domain_model_field SET validation = 1, sender_email = 1 WHERE uid = @f_email;
-- sender_name=1: use this field's value as the "From" name in notification emails
UPDATE tx_powermail_domain_model_field SET sender_name = 1 WHERE uid = @f_vorname;

-- CONDITIONAL FIELDS (shown/hidden dynamically by powermail_cond)
-- These fields are created normally but will be hidden by default via conditions
-- in Step 3. powermail_cond toggles their visibility based on the 'rechtsform' value.
-- sorting starts at 20 to leave a gap after common fields (good practice).
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  -- Commercial register fields (for e.U., OG, KG, GmbH, AG)
  (1, @page2_uid, 'Company Register No.',    'input',    'firmenbuchnummer',      1, 20, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Register Court',          'input',    'firmenbuchgericht',     1, 21, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  -- GmbH-specific fields
  (1, @page2_uid, 'Share Capital',           'input',    'stammkapital',          1, 22, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Managing Director',       'input',    'geschaeftsfuehrer',     1, 23, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  -- AG-specific fields
  (1, @page2_uid, 'Equity Capital',          'input',    'grundkapital',          1, 24, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Chairman of the Board',   'input',    'vorstandsvorsitzender', 1, 25, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  -- Einzelunternehmen-specific fields
  (1, @page2_uid, 'Trade License',           'input',    'gewerbeberechtigung',   1, 26, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'WKO Member No.',          'input',    'wko_mitgliedsnr',       0, 27, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  -- Partnership fields (OG, GesBR)
  (1, @page2_uid, 'Partners (one per line)', 'textarea', 'gesellschafter',        1, 28, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  -- KG-specific field
  (1, @page2_uid, 'General Partner',         'input',    'komplementaer',         1, 29, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  -- Verein-specific fields
  (1, @page2_uid, 'ZVR Number',              'input',    'zvr_zahl',              1, 30, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Association Seat',        'input',    'vereinssitz',           1, 31, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Chairman',                'input',    'obmann',                1, 32, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Look up conditional field UIDs by marker + page (safe with populated DB).
-- These UIDs are needed in Step 3 to create condition rules.
SET @f_fb_nr     = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firmenbuchnummer'      AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_fb_ger    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firmenbuchgericht'     AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_stammkap  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'stammkapital'          AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gf        = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'geschaeftsfuehrer'     AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_grundkap  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'grundkapital'          AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vorstand  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vorstandsvorsitzender' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gewerbe   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'gewerbeberechtigung'   AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_wko       = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'wko_mitgliedsnr'       AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gesell    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'gesellschafter'        AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_kompl     = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'komplementaer'         AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_zvr       = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'zvr_zahl'              AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vsitz     = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vereinssitz'           AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_obmann    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'obmann'                AND sys_language_uid = 0 AND page = @page2_uid);

-- =============================================
-- PAGE 3 FIELDS: Product Catalog + GDPR
-- =============================================
-- Each product has two fields:
--   1. type='html': renders raw HTML (product image, title, description, price)
--      The 'text' column contains the HTML markup. No user input — display only.
--   2. type='input': quantity field with validation=9 (integer only, no decimals)
--      mandatory=0 because the user may not want every product.

-- Product 1: Website Basic (display card + quantity input)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Website Basic', 'html', 'produkt1_info', 1,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=250&fit=crop\" alt=\"Website Basic\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>Website Basic</h3><p>Professional one-page website with responsive design, contact form, and SEO basics. Perfect for freelancers and small businesses.</p><p><strong>EUR 990 (one-time)</strong></p></div>',
   0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
-- type='html': renders the 'text' column as raw HTML in the form (no input, display only)

-- Quantity input: validation=9 means "integer only" — user can only enter whole numbers
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, validation_configuration, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Quantity Website Basic', 'input', 'produkt1_menge', 0, 2, 9, '', 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Product 2: Website Professional (display card + quantity input)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Website Professional', 'html', 'produkt2_info', 3,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=250&fit=crop\" alt=\"Website Professional\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>Website Professional</h3><p>Multi-page website with CMS, blog, image galleries, multi-language support, and advanced SEO. Ideal for growing companies.</p><p><strong>EUR 2.490 (one-time)</strong></p></div>',
   0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, validation_configuration, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Quantity Website Professional', 'input', 'produkt2_menge', 0, 4, 9, '', 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Product 3: SEO Package
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'SEO Package', 'html', 'produkt3_info', 5,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=400&h=250&fit=crop\" alt=\"SEO Package\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>SEO Package</h3><p>Monthly search engine optimization: keyword research, on-page optimization, content strategy, backlink building, and monthly reporting.</p><p><strong>EUR 490/month</strong></p></div>',
   0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, validation_configuration, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Quantity SEO Package', 'input', 'produkt3_menge', 0, 6, 9, '', 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Product 4: Maintenance Contract
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Maintenance Contract', 'html', 'produkt4_info', 7,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400&h=250&fit=crop\" alt=\"Maintenance Contract\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>Maintenance Contract</h3><p>Monthly TYPO3 maintenance: security updates, backups, uptime monitoring, performance optimization, and 2h support included.</p><p><strong>EUR 190/month</strong></p></div>',
   0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, validation_configuration, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Quantity Maintenance Contract', 'input', 'produkt4_menge', 0, 8, 9, '', 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Notes (optional free text) + GDPR consent checkboxes (all mandatory)
-- type='textarea': multi-line text input
-- type='check': renders a single checkbox, mandatory=1 means user MUST check it
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Notes',    'textarea', 'anmerkungen',  0, 9,  0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page3_uid, 'I accept the Terms & Conditions', 'check', 'agb', 1, 10, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page3_uid, 'I consent to data processing according to GDPR Art. 6(1)(a)', 'check', 'datenschutz', 1, 11, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page3_uid, 'I acknowledge the right of withdrawal (14 days)', 'check', 'widerruf', 1, 12, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- =============================================
-- PAGE 4 FIELDS: Confirmation
-- =============================================

-- type='text': renders static text (from 'text' column) — no user input, just information display
-- type='submit': renders the form submit button
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page4_uid, 'Summary', 'text', 'zusammenfassung', 1,
   'Please review your order and click Submit to complete.',
   0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page4_uid, 'Submit Order', 'submit', 'absenden', 2, NULL, 0, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- =============================================
-- OUTPUT: Show created UIDs for verification
-- =============================================
-- Steps 2 and 3 re-read UIDs via SELECT subqueries, so these are just for your reference.
SELECT @form_uid AS form_uid,
       @page1_uid AS page1, @page2_uid AS page2,
       @page3_uid AS page3, @page4_uid AS page4,
       @f_rechtsform AS rechtsform_field_uid,
       @f_fb_nr AS firmenbuchnummer_uid, @f_stammkap AS stammkapital_uid,
       @f_grundkap AS grundkapital_uid, @f_gewerbe AS gewerbeberechtigung_uid;
"
```

### Step 2: German Translation (sys_language_uid=1)

```bash
ddev mysql -e "
-- =============================================
-- GERMAN TRANSLATION (sys_language_uid=1)
-- =============================================
-- TYPO3 translations work by creating a COPY of the default-language record
-- with sys_language_uid=1 (German) and l10n_parent pointing to the English UID.
-- This tells TYPO3: 'this German record is a translation of that English record.'
-- The translated record inherits structure — only labels/text need translating.

-- First, look up the English UIDs from Step 1.
-- We use SELECT subqueries because the @variables from Step 1 are lost
-- (each `ddev mysql -e` runs in its own session).
SET @form_uid    = (SELECT uid FROM tx_powermail_domain_model_form WHERE title = 'Order Form' AND sys_language_uid = 0 ORDER BY uid DESC LIMIT 1);
SET @page1_uid   = (SELECT uid FROM tx_powermail_domain_model_page WHERE form = @form_uid AND sorting = 1 AND sys_language_uid = 0);
SET @page2_uid   = (SELECT uid FROM tx_powermail_domain_model_page WHERE form = @form_uid AND sorting = 2 AND sys_language_uid = 0);
SET @page3_uid   = (SELECT uid FROM tx_powermail_domain_model_page WHERE form = @form_uid AND sorting = 3 AND sys_language_uid = 0);
SET @page4_uid   = (SELECT uid FROM tx_powermail_domain_model_page WHERE form = @form_uid AND sorting = 4 AND sys_language_uid = 0);

-- Create German form record:
-- sys_language_uid=1: this is a German translation
-- l10n_parent=@form_uid: points to the English original
INSERT INTO tx_powermail_domain_model_form
  (pid, title, css, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, 'Bestellformular', 'order-form', 1, @form_uid, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Create German page translations (one per step)
-- Each page's l10n_parent points to its English counterpart
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, css, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @form_uid, 'Rechtsform',         'step-legal-type', 1, 1, @page1_uid, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @form_uid, 'Kontaktdaten',       'step-contact',    2, 1, @page2_uid, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @form_uid, 'Bestellübersicht',   'step-overview',   3, 1, @page3_uid, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @form_uid, 'Bestätigung',        'step-confirm',    4, 1, @page4_uid, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Field translations (German)
-- For each English field, we create a German copy with:
--   sys_language_uid=1 (German) and l10n_parent=<English field UID>
-- First we look up each English field UID by its unique marker.
-- PAGE 1 FIELDS (German)
-- Look up the English rechtsform field UID by marker + language + page
SET @f_rechtsform = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'rechtsform' AND sys_language_uid = 0 AND page = @page1_uid);

-- German translation of the rechtsform dropdown
-- l10n_parent=@f_rechtsform: links this German record to its English parent
-- settings: translated dropdown options (German labels, same structure)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, settings, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page1_uid, 'Rechtsform', 'select', 'rechtsform', 1,
   'Bitte wählen...\nEinzelunternehmen\nEinzelunternehmen e.U.\nOG (Offene Gesellschaft)\nKG (Kommanditgesellschaft)\nGmbH\nAG (Aktiengesellschaft)\nVerein\nGesBR',
   1, 1, @f_rechtsform, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- PAGE 2 COMMON FIELDS (German labels)
-- Look up all English field UIDs by their unique marker
SET @f_firma    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firma' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_anrede   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'anrede' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vorname  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vorname' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_nachname = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'nachname' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_email    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'email' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_telefon  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'telefon' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_strasse  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'strasse' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_plz      = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'plz' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_ort      = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'ort' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_uid_nr   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'uid_nummer' AND sys_language_uid = 0 AND page = @page2_uid);

INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page2_uid, 'Firmenname',       'input',  'firma',    1,  1, 1, @f_firma,    UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Anrede',           'select', 'anrede',   1,  2, 1, @f_anrede,   UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Vorname',          'input',  'vorname',  1,  3, 1, @f_vorname,  UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Nachname',         'input',  'nachname', 1,  4, 1, @f_nachname, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'E-Mail-Adresse',   'input',  'email',    1,  5, 1, @f_email,    UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Telefon',          'input',  'telefon',  0,  6, 1, @f_telefon,  UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Straße',           'input',  'strasse',  1,  7, 1, @f_strasse,  UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'PLZ',              'input',  'plz',      1,  8, 1, @f_plz,      UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Ort',              'input',  'ort',      1,  9, 1, @f_ort,      UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'UID-Nummer',       'input',  'uid_nummer', 0, 10, 1, @f_uid_nr, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Update the German salutation dropdown options (Herr/Frau/Divers instead of Mr./Ms./Diverse)
-- We find the German record by its l10n_parent pointing to the English anrede field
UPDATE tx_powermail_domain_model_field SET settings = 'Herr\nFrau\nDivers' WHERE sys_language_uid = 1 AND l10n_parent = @f_anrede;

-- PAGE 2 CONDITIONAL FIELDS (German labels)
-- Same pattern: look up English UIDs, then create German copies with l10n_parent
SET @f_fb_nr    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firmenbuchnummer' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_fb_ger   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firmenbuchgericht' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_stammkap = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'stammkapital' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gf       = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'geschaeftsfuehrer' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_grundkap = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'grundkapital' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vorstand = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vorstandsvorsitzender' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gewerbe  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'gewerbeberechtigung' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_wko      = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'wko_mitgliedsnr' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gesell   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'gesellschafter' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_kompl    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'komplementaer' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_zvr      = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'zvr_zahl' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vsitz    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vereinssitz' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_obmann   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'obmann' AND sys_language_uid = 0 AND page = @page2_uid);

INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page2_uid, 'Firmenbuchnummer',       'input',    'firmenbuchnummer',      1, 20, 1, @f_fb_nr,    UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Firmenbuchgericht',      'input',    'firmenbuchgericht',     1, 21, 1, @f_fb_ger,   UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Stammkapital',           'input',    'stammkapital',          1, 22, 1, @f_stammkap, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Geschäftsführer',        'input',    'geschaeftsfuehrer',     1, 23, 1, @f_gf,       UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Grundkapital',           'input',    'grundkapital',          1, 24, 1, @f_grundkap, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Vorstandsvorsitzender',  'input',    'vorstandsvorsitzender', 1, 25, 1, @f_vorstand, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Gewerbeberechtigung',    'input',    'gewerbeberechtigung',   1, 26, 1, @f_gewerbe,  UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'WKO-Mitgliedsnummer',    'input',    'wko_mitgliedsnr',       0, 27, 1, @f_wko,      UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Gesellschafter (einer pro Zeile)', 'textarea', 'gesellschafter', 1, 28, 1, @f_gesell, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Komplementär',           'input',    'komplementaer',         1, 29, 1, @f_kompl,    UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'ZVR-Zahl',               'input',    'zvr_zahl',              1, 30, 1, @f_zvr,      UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Vereinssitz',             'input',    'vereinssitz',           1, 31, 1, @f_vsitz,    UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page2_uid, 'Obmann/Obfrau',          'input',    'obmann',                1, 32, 1, @f_obmann,   UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- PAGE 3 FIELDS (German) — product HTML, quantities, notes, GDPR checkboxes
-- Look up English field UIDs for the product info/quantity fields + GDPR fields
SET @f_p1_info  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt1_info' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p1_qty   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt1_menge' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p2_info  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt2_info' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p2_qty   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt2_menge' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p3_info  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt3_info' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p3_qty   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt3_menge' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p4_info  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt4_info' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_p4_qty   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'produkt4_menge' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_anmerk   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'anmerkungen' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_agb      = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'agb' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_dsgvo    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'datenschutz' AND sys_language_uid = 0 AND page = @page3_uid);
SET @f_wider    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'widerruf' AND sys_language_uid = 0 AND page = @page3_uid);

-- Product 1: German HTML card (translated title, description, price label)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Website Basis', 'html', 'produkt1_info', 1,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=250&fit=crop\" alt=\"Website Basis\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>Website Basis</h3><p>Professionelle One-Page-Website mit responsivem Design, Kontaktformular und SEO-Grundlagen. Perfekt für Freelancer und Kleinunternehmen.</p><p><strong>EUR 990 (einmalig)</strong></p></div>',
   1, @f_p1_info, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
-- Product 1: German quantity label
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Anzahl Website Basis', 'input', 'produkt1_menge', 0, 2, 9, 1, @f_p1_qty, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Product 2: German HTML card
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Website Professional', 'html', 'produkt2_info', 3,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=250&fit=crop\" alt=\"Website Professional\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>Website Professional</h3><p>Mehrseiten-Website mit CMS, Blog, Bildergalerien, Mehrsprachigkeit und erweitertem SEO. Ideal für wachsende Unternehmen.</p><p><strong>EUR 2.490 (einmalig)</strong></p></div>',
   1, @f_p2_info, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Anzahl Website Professional', 'input', 'produkt2_menge', 0, 4, 9, 1, @f_p2_qty, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Product 3: German HTML card (SEO-Paket)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'SEO-Paket', 'html', 'produkt3_info', 5,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=400&h=250&fit=crop\" alt=\"SEO-Paket\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>SEO-Paket</h3><p>Monatliche Suchmaschinenoptimierung: Keyword-Recherche, OnPage-Optimierung, Content-Strategie, Linkaufbau und monatliches Reporting.</p><p><strong>EUR 490/Monat</strong></p></div>',
   1, @f_p3_info, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Anzahl SEO-Paket', 'input', 'produkt3_menge', 0, 6, 9, 1, @f_p3_qty, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Product 4: German HTML card (Wartungsvertrag)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Wartungsvertrag', 'html', 'produkt4_info', 7,
   '<div class=\"powermail-product\"><img src=\"https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400&h=250&fit=crop\" alt=\"Wartungsvertrag\" style=\"width:100%%;max-width:400px;border-radius:8px;\"><h3>Wartungsvertrag</h3><p>Monatliche TYPO3-Wartung: Sicherheitsupdates, Backups, Uptime-Monitoring, Performance-Optimierung und 2h Support inklusive.</p><p><strong>EUR 190/Monat</strong></p></div>',
   1, @f_p4_info, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, validation, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Anzahl Wartungsvertrag', 'input', 'produkt4_menge', 0, 8, 9, 1, @f_p4_qty, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Notes + GDPR checkboxes (German labels)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sorting, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page3_uid, 'Anmerkungen',  'textarea', 'anmerkungen', 0, 9,  1, @f_anmerk, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page3_uid, 'Ich akzeptiere die AGB',      'check', 'agb',         1, 10, 1, @f_agb,  UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page3_uid, 'Ich stimme der Datenverarbeitung gemäß DSGVO Art. 6 Abs. 1 lit. a zu', 'check', 'datenschutz', 1, 11, 1, @f_dsgvo, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page3_uid, 'Ich nehme das Widerrufsrecht (14 Tage) zur Kenntnis', 'check', 'widerruf', 1, 12, 1, @f_wider, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- PAGE 4 FIELDS (German) — summary text and submit button
SET @f_summary = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'zusammenfassung' AND sys_language_uid = 0 AND page = @page4_uid);
SET @f_submit  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'absenden' AND sys_language_uid = 0 AND page = @page4_uid);

INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, sorting, text, sys_language_uid, l10n_parent, tstamp, crdate)
VALUES
  (1, @page4_uid, 'Zusammenfassung', 'text', 'zusammenfassung', 1,
   'Bitte überprüfen Sie Ihre Bestellung und klicken Sie auf Absenden.',
   1, @f_summary, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @page4_uid, 'Bestellung absenden', 'submit', 'absenden', 2, NULL, 1, @f_submit, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

SELECT 'German translation complete' AS status;
"
```

### Step 3: Condition Container (powermail_cond)

```bash
ddev mysql -e "
-- =============================================
-- CONDITIONS: Show/hide fields per legal type
-- =============================================
-- powermail_cond uses 3 tables:
--   1. conditioncontainer: groups all conditions for one form
--   2. condition: defines WHAT to do (hide/show a target field) and HOW rules combine (AND/OR)
--   3. rule: defines WHEN to trigger (checks a source field's value with an operator)
--
-- Operator reference (ops column):
--   0 = is set (field has any value)
--   1 = is not set (field is empty)
--   2 = contains (value includes the string)
--   3 = not contains (value does NOT include the string)
--   4 = is (exact match)
--   5 = is not (exact mismatch)
--   6 = greater than
--   7 = less than
--
-- Action reference (actions column):
--   0 = hide the target field when ALL/ANY rules match
--   1 = unhide (show) the target field when ALL/ANY rules match

-- Look up form and page UIDs from Step 1
SET @form_uid = (SELECT uid FROM tx_powermail_domain_model_form WHERE title = 'Order Form' AND sys_language_uid = 0 ORDER BY uid DESC LIMIT 1);
SET @page2_uid = (SELECT uid FROM tx_powermail_domain_model_page WHERE form = @form_uid AND sorting = 2 AND sys_language_uid = 0);

-- Look up all field UIDs needed for conditions (English defaults only)
-- The rechtsform field is the SOURCE (start_field) — its value is checked
-- All other fields are TARGETS (target_field) — they get shown/hidden
SET @page1_uid   = (SELECT uid FROM tx_powermail_domain_model_page WHERE form = @form_uid AND sorting = 1 AND sys_language_uid = 0);
SET @f_rechtsform = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'rechtsform' AND sys_language_uid = 0 AND page = @page1_uid);
SET @f_fb_nr     = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firmenbuchnummer' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_fb_ger    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'firmenbuchgericht' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_stammkap  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'stammkapital' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gf        = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'geschaeftsfuehrer' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_grundkap  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'grundkapital' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vorstand  = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vorstandsvorsitzender' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gewerbe   = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'gewerbeberechtigung' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_wko       = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'wko_mitgliedsnr' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_gesell    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'gesellschafter' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_kompl     = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'komplementaer' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_zvr       = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'zvr_zahl' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_vsitz     = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'vereinssitz' AND sys_language_uid = 0 AND page = @page2_uid);
SET @f_obmann    = (SELECT uid FROM tx_powermail_domain_model_field WHERE marker = 'obmann' AND sys_language_uid = 0 AND page = @page2_uid);

-- Create the condition container — one per form, groups all conditions
-- 'form' links it to our order form, 'conditions' will be updated with the count
INSERT INTO tx_powermailcond_domain_model_conditioncontainer
  (pid, title, form, conditions, tstamp, crdate)
VALUES
  (1, 'Rechtsform Conditions', @form_uid, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @container_uid = LAST_INSERT_ID();

-- -----------------------------------------------
-- CONDITION 1: Hide Firmenbuchnummer when NOT needed
-- -----------------------------------------------
-- Strategy: actions='0' (hide) when rechtsform IS one of the types that don't need it.
-- conjunction='AND' with ops=4 (is exact match) per rule.
-- Effect: field is hidden when rechtsform = Einzelunternehmen OR Verein OR GesBR OR placeholder.
-- It remains VISIBLE for: e.U., OG, KG, GmbH, AG.

-- Create the condition: target_field = the field UID to hide/show
-- CAST(@f_fb_nr AS CHAR) because target_field is stored as varchar, not int
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Firmenbuchnummer',  CAST(@f_fb_nr AS CHAR),  '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_fb_nr = LAST_INSERT_ID();

-- Create rules: each rule checks if rechtsform (start_field) matches a value
-- ops=4 means "is" (exact match), cond_string = the value to compare against
-- When ANY of these rules matches, the field gets hidden (action=0)
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_fb_nr, 'is Einzelunternehmen', @f_rechtsform, 4, 'Einzelunternehmen', UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_fb_nr, 'is Verein',            @f_rechtsform, 4, 'Verein',            UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_fb_nr, 'is GesBR',             @f_rechtsform, 4, 'GesBR',             UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_fb_nr, 'is empty',             @f_rechtsform, 4, 'Please select...',  UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
-- Update rule count on the condition (must match the number of rules inserted)
UPDATE tx_powermailcond_domain_model_condition SET rules = 4 WHERE uid = @cond_fb_nr;

-- -----------------------------------------------
-- CONDITION 2: Firmenbuchgericht — same hide-logic as Firmenbuchnummer
-- Hidden for: Einzelunternehmen, Verein, GesBR, placeholder
-- Visible for: e.U., OG, KG, GmbH, AG
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Firmenbuchgericht', CAST(@f_fb_ger AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_fb_ger = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_fb_ger, 'is Einzelunternehmen', @f_rechtsform, 4, 'Einzelunternehmen', UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_fb_ger, 'is Verein',            @f_rechtsform, 4, 'Verein',            UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_fb_ger, 'is GesBR',             @f_rechtsform, 4, 'GesBR',             UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_fb_ger, 'is empty',             @f_rechtsform, 4, 'Please select...',  UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 4 WHERE uid = @cond_fb_ger;

-- -----------------------------------------------
-- CONDITIONS 3+4: Stammkapital + Geschäftsführer — GmbH only
-- ops=5 means "is not" — hide when rechtsform is NOT 'GmbH'
-- Single rule per condition: hidden for ALL types except GmbH
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Stammkapital', CAST(@f_stammkap AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_stammkap = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_stammkap, 'is not GmbH', @f_rechtsform, 5, 'GmbH', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_stammkap;

INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Geschäftsführer', CAST(@f_gf AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_gf = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_gf, 'is not GmbH', @f_rechtsform, 5, 'GmbH', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_gf;

-- -----------------------------------------------
-- CONDITIONS 5+6: Grundkapital + Vorstandsvorsitzender — AG only
-- ops=5 "is not": hide when rechtsform is NOT 'AG (Aktiengesellschaft)'
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Grundkapital', CAST(@f_grundkap AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_grundkap = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_grundkap, 'is not AG', @f_rechtsform, 5, 'AG (Aktiengesellschaft)', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_grundkap;

INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Vorstandsvorsitzender', CAST(@f_vorstand AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_vorstand = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_vorstand, 'is not AG', @f_rechtsform, 5, 'AG (Aktiengesellschaft)', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_vorstand;

-- -----------------------------------------------
-- CONDITIONS 7+8: Gewerbeberechtigung + WKO — Einzelunternehmen only
-- ops=5 "is not": hide when rechtsform is NOT 'Einzelunternehmen'
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Gewerbeberechtigung', CAST(@f_gewerbe AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_gewerbe = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_gewerbe, 'is not Einzelunternehmen', @f_rechtsform, 5, 'Einzelunternehmen', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_gewerbe;

INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show WKO Mitgliedsnr', CAST(@f_wko AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_wko = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_wko, 'is not Einzelunternehmen', @f_rechtsform, 5, 'Einzelunternehmen', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_wko;

-- -----------------------------------------------
-- CONDITION 9: Gesellschafter — OG and GesBR only
-- Uses conjunction='AND' with TWO rules:
--   Rule 1: ops=3 "not contains 'OG'" — true when rechtsform doesn't have 'OG'
--   Rule 2: ops=5 "is not 'GesBR'" — true when rechtsform isn't GesBR
-- Both must be true to hide → field only shows for OG or GesBR
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Gesellschafter', CAST(@f_gesell AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_gesell = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_gesell, 'not contains OG',   @f_rechtsform, 3, 'OG',    UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_gesell, 'is not GesBR',      @f_rechtsform, 5, 'GesBR', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 2 WHERE uid = @cond_gesell;

-- -----------------------------------------------
-- CONDITION 10: Komplementär — KG only
-- ops=3 "not contains 'KG'": hide when rechtsform doesn't contain 'KG'
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show Komplementär', CAST(@f_kompl AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_kompl = LAST_INSERT_ID();
INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_kompl, 'not contains KG', @f_rechtsform, 3, 'KG', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid = @cond_kompl;

-- -----------------------------------------------
-- CONDITIONS 11+12+13: ZVR-Zahl + Vereinssitz + Obmann — Verein only
-- Three conditions with identical logic: ops=5 "is not 'Verein'"
-- Bulk INSERT creates all 3 conditions at once
-- -----------------------------------------------
INSERT INTO tx_powermailcond_domain_model_condition
  (pid, conditioncontainer, title, target_field, actions, conjunction, rules, tstamp, crdate)
VALUES
  (1, @container_uid, 'Show ZVR-Zahl',     CAST(@f_zvr AS CHAR),    '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @container_uid, 'Show Vereinssitz',   CAST(@f_vsitz AS CHAR),  '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @container_uid, 'Show Obmann',        CAST(@f_obmann AS CHAR), '0', 'AND', 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @cond_obmann = LAST_INSERT_ID();
SET @cond_vsitz  = @cond_obmann - 1;
SET @cond_zvr    = @cond_obmann - 2;

INSERT INTO tx_powermailcond_domain_model_rule (pid, conditions, title, start_field, ops, cond_string, tstamp, crdate) VALUES
  (1, @cond_zvr,    'is not Verein', @f_rechtsform, 5, 'Verein', UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_vsitz,  'is not Verein', @f_rechtsform, 5, 'Verein', UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @cond_obmann, 'is not Verein', @f_rechtsform, 5, 'Verein', UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
UPDATE tx_powermailcond_domain_model_condition SET rules = 1 WHERE uid IN (@cond_zvr, @cond_vsitz, @cond_obmann);

-- Update the container's condition count (must match actual number of conditions)
-- This count is used by the backend module to display the container correctly
UPDATE tx_powermailcond_domain_model_conditioncontainer
SET conditions = (SELECT COUNT(*) FROM tx_powermailcond_domain_model_condition WHERE conditioncontainer = @container_uid)
WHERE uid = @container_uid;

-- Verify: output container UID and total conditions count
SELECT @container_uid AS container_uid,
       (SELECT COUNT(*) FROM tx_powermailcond_domain_model_condition WHERE conditioncontainer = @container_uid) AS total_conditions;
"
```

### Step 4: Verify

```bash
# Check form structure
ddev mysql -e "
SELECT f.uid, f.title, f.sys_language_uid,
       (SELECT COUNT(*) FROM tx_powermail_domain_model_page WHERE form = f.uid AND sys_language_uid = f.sys_language_uid) AS pages,
       (SELECT COUNT(*) FROM tx_powermail_domain_model_field fi
        JOIN tx_powermail_domain_model_page p ON fi.page = p.uid
        WHERE p.form = f.uid AND fi.sys_language_uid = f.sys_language_uid) AS fields
FROM tx_powermail_domain_model_form f
WHERE f.deleted = 0
ORDER BY f.l10n_parent, f.sys_language_uid;
"

# Check conditions
ddev mysql -e "
SELECT cc.title AS container,
       c.title AS condition_name, c.target_field, c.actions, c.conjunction,
       r.title AS rule_name, r.ops, r.cond_string
FROM tx_powermailcond_domain_model_conditioncontainer cc
JOIN tx_powermailcond_domain_model_condition c ON c.conditioncontainer = cc.uid
JOIN tx_powermailcond_domain_model_rule r ON r.conditions = c.uid
WHERE cc.deleted = 0
ORDER BY cc.uid, c.uid, r.uid;
"

# Flush caches
ddev typo3 cache:flush
```

---

## Approach 2: DataHandler CLI Command

> **Recommended approach.** Uses DataHandler for proper reference index, cache clearing,
> and event dispatching. See [typo3-datahandler SKILL.md](../typo3-datahandler/SKILL.md).

> **Populated Database:** This command works safely alongside existing powermail forms.
> DataHandler uses `NEW_xxx` placeholder IDs that are resolved to real UIDs internally —
> no UID arithmetic, no collision with existing records. The `localize` command is scoped
> to the newly created form UID. Conditions reference fields via the `$fieldUids` map
> built from `substNEWwithIDs`, which is always accurate.

### CLI Command Class

Create this in your site package or a custom extension.

**File:** `Classes/Command/CreateShopFormCommand.php`

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

#[AsCommand(
    name: 'shop:create-form',
    description: 'Create multi-step shop form with conditions (LOCAL DEV ONLY)',
)]
final class CreateShopFormCommand extends Command
{
    private const STORAGE_PID = 1;

    protected function configure(): void
    {
        $this->addOption(
            'with-german',
            'g',
            InputOption::VALUE_NONE,
            'Also create German translation (sys_language_uid=1)'
        );
        $this->addOption(
            'with-conditions',
            'c',
            InputOption::VALUE_NONE,
            'Create powermail_cond conditions for legal type fields'
        );
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        $io->warning([
            'LOCAL DEVELOPMENT ONLY!',
            'Never run this command on a production site.',
            'It creates test data that will pollute your database.',
        ]);

        // ---------------------------------------------------------
        // 1. Create Form + Pages + Fields (English)
        // ---------------------------------------------------------
        // DataHandler uses a $data array (datamap) where:
        //   Key 1: table name (e.g., 'tx_powermail_domain_model_form')
        //   Key 2: record identifier — 'NEW_xxx' for new records, numeric UID for updates
        //   Value: array of column => value pairs
        //
        // DataHandler advantages over raw SQL:
        //   - Maintains reference index (sys_refindex) for relation integrity
        //   - Dispatches PSR-14 events (other extensions can react)
        //   - Handles cache clearing automatically
        //   - Respects TCA configuration and validation
        //   - Proper workspace/versioning support
        $io->section('Creating form structure (English)...');

        // Create DataHandler instance and bypass access checks (CLI has no BE user)
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->bypassAccessCheckForRecords = true;

        $data = [];

        // --- FORM ---
        // 'pages' uses comma-separated NEW_xxx IDs — DataHandler resolves these
        // to real UIDs after insert and creates the IRRE (inline relational record
        // editing) parent-child relationship automatically.
        $data['tx_powermail_domain_model_form']['NEW_form'] = [
            'pid' => self::STORAGE_PID,   // Storage page UID (sysfolder)
            'title' => 'Order Form',       // Form title (backend label)
            'css' => 'order-form',         // CSS class on <form> tag
            'pages' => 'NEW_page1,NEW_page2,NEW_page3,NEW_page4', // IRRE: child pages
        ];

        // --- PAGES (form steps) ---
        // Each page's 'fields' key lists its child field NEW_xxx IDs (IRRE relation).
        // DataHandler creates the page→field parent-child links automatically.

        // Page 1: Legal type selection (1 field: rechtsform dropdown)
        $data['tx_powermail_domain_model_page']['NEW_page1'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Legal Type',
            'css' => 'step-legal-type',
            'sorting' => 1,                            // Step order
            'fields' => 'NEW_f_rechtsform',             // IRRE: 1 child field
        ];

        // Page 2: Contact data (10 common + 13 conditional = 23 fields)
        $data['tx_powermail_domain_model_page']['NEW_page2'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Contact Data',
            'css' => 'step-contact',
            'sorting' => 2,
            'fields' => implode(',', [                  // IRRE: all 23 child fields
                'NEW_f_firma', 'NEW_f_anrede', 'NEW_f_vorname', 'NEW_f_nachname',
                'NEW_f_email', 'NEW_f_telefon', 'NEW_f_strasse', 'NEW_f_plz',
                'NEW_f_ort', 'NEW_f_uid_nummer',
                // Conditional fields (shown/hidden by powermail_cond):
                'NEW_f_firmenbuchnummer', 'NEW_f_firmenbuchgericht',
                'NEW_f_stammkapital', 'NEW_f_geschaeftsfuehrer',
                'NEW_f_grundkapital', 'NEW_f_vorstandsvorsitzender',
                'NEW_f_gewerbeberechtigung', 'NEW_f_wko_mitgliedsnr',
                'NEW_f_gesellschafter', 'NEW_f_komplementaer',
                'NEW_f_zvr_zahl', 'NEW_f_vereinssitz', 'NEW_f_obmann',
            ]),
        ];

        // Page 3: Product catalog (4 products × 2 fields each + notes + 3 GDPR checkboxes)
        $data['tx_powermail_domain_model_page']['NEW_page3'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Order Overview',
            'css' => 'step-overview',
            'sorting' => 3,
            'fields' => implode(',', [
                'NEW_f_produkt1_info', 'NEW_f_produkt1_menge',
                'NEW_f_produkt2_info', 'NEW_f_produkt2_menge',
                'NEW_f_produkt3_info', 'NEW_f_produkt3_menge',
                'NEW_f_produkt4_info', 'NEW_f_produkt4_menge',
                'NEW_f_anmerkungen', 'NEW_f_agb', 'NEW_f_datenschutz', 'NEW_f_widerruf',
            ]),
        ];

        // Page 4: Confirmation (summary text + submit button)
        $data['tx_powermail_domain_model_page']['NEW_page4'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Confirmation',
            'css' => 'step-confirm',
            'sorting' => 4,
            'fields' => 'NEW_f_zusammenfassung,NEW_f_absenden', // IRRE: 2 child fields
        ];

        // ----- Page 1 Fields -----
        // Rechtsform dropdown: the source field for ALL conditions.
        // type='select': renders <select>, settings: one option per \n line.
        // marker='rechtsform': unique identifier for Fluid, conditions, CSS.
        $data['tx_powermail_domain_model_field']['NEW_f_rechtsform'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Legal Type',           // Label shown to user
            'type' => 'select',                // Field type: dropdown
            'marker' => 'rechtsform',          // Unique marker for templates/conditions
            'mandatory' => 1,                  // Required field
            'sorting' => 1,                    // Display order within page
            'settings' => "Please select...\nEinzelunternehmen\nEinzelunternehmen e.U.\nOG (Offene Gesellschaft)\nKG (Kommanditgesellschaft)\nGmbH\nAG (Aktiengesellschaft)\nVerein\nGesBR",
            // settings: dropdown options, \n-separated, first = placeholder
        ];

        // ----- Page 2 Fields: Common (always visible) -----
        // Using an array + loop to avoid repetitive code.
        // Format: marker => [title, type, mandatory, sorting, [extra columns]]
        $commonFields = [
            //  marker     => [title,           type,     mandatory, sorting, [extra config]]
            'firma'      => ['Company Name',  'input',  1, 1, ['sender_name' => 0]],
            'anrede'     => ['Salutation',    'select', 1, 2, ['settings' => "Mr.\nMs.\nDiverse"]], // settings: dropdown options
            'vorname'    => ['First Name',    'input',  1, 3, ['sender_name' => 1]],  // sender_name=1: used as "From" name in emails
            'nachname'   => ['Last Name',     'input',  1, 4, []],
            'email'      => ['Email',         'input',  1, 5, ['validation' => 1, 'sender_email' => 1]], // validation=1: email format, sender_email=1: reply-to
            'telefon'    => ['Phone',         'input',  0, 6, []],   // mandatory=0: optional
            'strasse'    => ['Street',        'input',  1, 7, []],
            'plz'        => ['ZIP',           'input',  1, 8, []],
            'ort'        => ['City',          'input',  1, 9, []],
            'uid_nummer' => ['VAT Number',    'input',  0, 10, []],  // optional
        ];

        // Loop creates DataHandler entries with NEW_f_<marker> as identifier.
        // The array_merge adds extra columns (validation, sender_email, etc.) when present.
        foreach ($commonFields as $marker => [$title, $type, $mandatory, $sorting, $extra]) {
            $data['tx_powermail_domain_model_field']['NEW_f_' . $marker] = array_merge([
                'pid' => self::STORAGE_PID,
                'title' => $title,
                'type' => $type,
                'marker' => $marker,
                'mandatory' => $mandatory,
                'sorting' => $sorting,
            ], $extra);
        }

        // ----- Page 2 Fields: Conditional (shown/hidden by powermail_cond) -----
        // These fields are created as normal fields; conditions (Step 3) control visibility.
        // Format: marker => [title, type, mandatory, sorting]
        $conditionalFields = [
            // Commercial register (e.U., OG, KG, GmbH, AG)
            'firmenbuchnummer'      => ['Company Register No.',    'input',    1, 20],
            'firmenbuchgericht'     => ['Register Court',          'input',    1, 21],
            'stammkapital'          => ['Share Capital',           'input',    1, 22],
            'geschaeftsfuehrer'     => ['Managing Director',       'input',    1, 23],
            'grundkapital'          => ['Equity Capital',          'input',    1, 24],
            'vorstandsvorsitzender' => ['Chairman of the Board',   'input',    1, 25],
            'gewerbeberechtigung'   => ['Trade License',           'input',    1, 26],
            'wko_mitgliedsnr'       => ['WKO Member No.',          'input',    0, 27],
            'gesellschafter'        => ['Partners (one per line)', 'textarea', 1, 28],
            'komplementaer'         => ['General Partner',         'input',    1, 29],
            'zvr_zahl'              => ['ZVR Number',              'input',    1, 30],
            'vereinssitz'           => ['Association Seat',        'input',    1, 31],
            'obmann'                => ['Chairman',                'input',    1, 32],
        ];

        foreach ($conditionalFields as $marker => [$title, $type, $mandatory, $sorting]) {
            $data['tx_powermail_domain_model_field']['NEW_f_' . $marker] = [
                'pid' => self::STORAGE_PID,
                'title' => $title,
                'type' => $type,
                'marker' => $marker,
                'mandatory' => $mandatory,
                'sorting' => $sorting,
            ];
        }

        // ----- Page 3 Fields: Product Catalog -----
        // Each product has 2 fields:
        //   type='html': display-only card with image, title, description, price (from 'text' column)
        //   type='input' with validation=9: integer-only quantity input

        // Product definitions: [marker_info, marker_qty, title_en, html_content]
        $products = [
            [
                'produkt1_info', 'produkt1_menge', 'Website Basic', 'Quantity Website Basic',
                '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=250&fit=crop" alt="Website Basic" style="width:100%;max-width:400px;border-radius:8px;"><h3>Website Basic</h3><p>Professional one-page website with responsive design, contact form, and SEO basics. Perfect for freelancers and small businesses.</p><p><strong>EUR 990 (one-time)</strong></p></div>',
            ],
            [
                'produkt2_info', 'produkt2_menge', 'Website Professional', 'Quantity Website Professional',
                '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=250&fit=crop" alt="Website Professional" style="width:100%;max-width:400px;border-radius:8px;"><h3>Website Professional</h3><p>Multi-page website with CMS, blog, image galleries, multi-language support, and advanced SEO. Ideal for growing companies.</p><p><strong>EUR 2.490 (one-time)</strong></p></div>',
            ],
            [
                'produkt3_info', 'produkt3_menge', 'SEO Package', 'Quantity SEO Package',
                '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=400&h=250&fit=crop" alt="SEO Package" style="width:100%;max-width:400px;border-radius:8px;"><h3>SEO Package</h3><p>Monthly search engine optimization: keyword research, on-page optimization, content strategy, backlink building, and monthly reporting.</p><p><strong>EUR 490/month</strong></p></div>',
            ],
            [
                'produkt4_info', 'produkt4_menge', 'Maintenance Contract', 'Quantity Maintenance Contract',
                '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400&h=250&fit=crop" alt="Maintenance Contract" style="width:100%;max-width:400px;border-radius:8px;"><h3>Maintenance Contract</h3><p>Monthly TYPO3 maintenance: security updates, backups, uptime monitoring, performance optimization, and 2h support included.</p><p><strong>EUR 190/month</strong></p></div>',
            ],
        ];

        $sortIdx = 1;
        foreach ($products as [$infoMarker, $qtyMarker, $infoTitle, $qtyTitle, $htmlContent]) {
            // HTML display card (type='html' renders raw HTML, no user input)
            $data['tx_powermail_domain_model_field']['NEW_f_' . $infoMarker] = [
                'pid' => self::STORAGE_PID,
                'title' => $infoTitle,         // Backend label
                'type' => 'html',              // Display-only HTML content
                'marker' => $infoMarker,
                'sorting' => $sortIdx++,
                'text' => $htmlContent,         // Raw HTML rendered in form
            ];
            // Quantity input (validation=9 = integer only)
            $data['tx_powermail_domain_model_field']['NEW_f_' . $qtyMarker] = [
                'pid' => self::STORAGE_PID,
                'title' => $qtyTitle,
                'type' => 'input',
                'marker' => $qtyMarker,
                'mandatory' => 0,              // Optional: user may not want this product
                'sorting' => $sortIdx++,
                'validation' => 9,             // 9 = integer validation (whole numbers only)
            ];
        }

        // Notes (optional textarea) + GDPR consent checkboxes (all mandatory)
        $data['tx_powermail_domain_model_field']['NEW_f_anmerkungen'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Notes',
            'type' => 'textarea',              // Multi-line text input
            'marker' => 'anmerkungen',
            'sorting' => $sortIdx++,
        ];
        $data['tx_powermail_domain_model_field']['NEW_f_agb'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'I accept the Terms & Conditions',
            'type' => 'check',                 // Single checkbox
            'marker' => 'agb',
            'mandatory' => 1,                  // Must be checked to submit
            'sorting' => $sortIdx++,
        ];
        $data['tx_powermail_domain_model_field']['NEW_f_datenschutz'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'I consent to data processing according to GDPR Art. 6(1)(a)',
            'type' => 'check',
            'marker' => 'datenschutz',
            'mandatory' => 1,
            'sorting' => $sortIdx++,
        ];
        $data['tx_powermail_domain_model_field']['NEW_f_widerruf'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'I acknowledge the right of withdrawal (14 days)',
            'type' => 'check',
            'marker' => 'widerruf',
            'mandatory' => 1,
            'sorting' => $sortIdx++,
        ];

        // ----- Page 4 Fields: Confirmation -----
        $data['tx_powermail_domain_model_field']['NEW_f_zusammenfassung'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Summary',
            'type' => 'text',              // type='text': renders static text (no input)
            'marker' => 'zusammenfassung',
            'sorting' => 1,
            'text' => 'Please review your order and click Submit to complete.', // Display text
        ];
        $data['tx_powermail_domain_model_field']['NEW_f_absenden'] = [
            'pid' => self::STORAGE_PID,
            'title' => 'Submit Order',
            'type' => 'submit',            // type='submit': renders the form submit button
            'marker' => 'absenden',
            'sorting' => 2,
        ];

        // Execute DataHandler: process all records in a single transaction.
        // start($data, $cmdMap): $data = datamap (create/update), $cmdMap = commands (copy/move/delete)
        // process_datamap(): executes all create/update operations from $data
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        // Check for errors (e.g., TCA validation failures, missing required fields)
        if ($dataHandler->errorLog !== []) {
            $io->error('DataHandler errors:');
            foreach ($dataHandler->errorLog as $error) {
                $io->writeln('  - ' . $error);
            }
            return Command::FAILURE;
        }

        // substNEWwithIDs maps NEW_xxx identifiers to real auto-incremented UIDs.
        // e.g., 'NEW_form' => 10, 'NEW_f_rechtsform' => 42, etc.
        $formUid = (int)$dataHandler->substNEWwithIDs['NEW_form'];
        $io->success('Form created with UID ' . $formUid);

        // Build a marker → UID map for all fields (needed for conditions in Step 3)
        $fieldUids = [];
        foreach ($dataHandler->substNEWwithIDs as $newId => $realUid) {
            if (str_starts_with($newId, 'NEW_f_')) {
                $marker = substr($newId, 6); // strip 'NEW_f_' prefix → marker name
                $fieldUids[$marker] = (int)$realUid;
            }
        }

        // Display the marker→UID mapping table for verification
        $io->table(
            ['Marker', 'UID'],
            array_map(fn($m, $u) => [$m, $u], array_keys($fieldUids), array_values($fieldUids))
        );

        // ---------------------------------------------------------
        // 2. German Translation (sys_language_uid=1)
        // ---------------------------------------------------------
        // DataHandler's 'localize' command copies a record and all its IRRE children
        // to a new language. It automatically:
        //   - Creates translated form, pages, and field records
        //   - Sets sys_language_uid=1 (German) and l10n_parent to the English UID
        //   - Copies all field values from the English original
        // After localizing, we update the German labels/settings with correct translations.
        if ($input->getOption('with-german')) {
            $io->section('Creating German translation...');

            // cmdMap uses 'localize' command: {table: {uid: {localize: target_language_uid}}}
            // 'localize' => 1 means: create a translation for language UID 1 (German)
            $cmdMap = [
                'tx_powermail_domain_model_form' => [
                    $formUid => ['localize' => 1], // Localizes form + all child pages + all child fields
                ],
            ];

            // Use a fresh DataHandler instance for the command map
            $dataHandler2 = GeneralUtility::makeInstance(DataHandler::class);
            $dataHandler2->bypassAccessCheckForRecords = true;
            $dataHandler2->start([], $cmdMap);  // Empty datamap, only cmdMap
            $dataHandler2->process_cmdmap();     // Execute localize command

            if ($dataHandler2->errorLog !== []) {
                $io->error('Localization errors:');
                foreach ($dataHandler2->errorLog as $error) {
                    $io->writeln('  - ' . $error);
                }
                return Command::FAILURE;
            }

            // After localize, all German records have English labels. Now update them.
            // copyMappingArray_merged maps original UIDs to translated UIDs:
            //   {table: {original_uid: translated_uid}}
            // This lets us find the German record for each English original.

            // Find the translated form UID from the mapping
            $translatedFormUid = $dataHandler2->copyMappingArray_merged['tx_powermail_domain_model_form'][$formUid] ?? null;

            if ($translatedFormUid) {
                // Build a datamap to UPDATE the German records with translated labels
                $germanData = [
                    'tx_powermail_domain_model_form' => [
                        $translatedFormUid => ['title' => 'Bestellformular'], // German form title
                    ],
                ];

                // German page titles (matched by sorting order)
                $pageLabels = [
                    1 => 'Rechtsform',
                    2 => 'Kontaktdaten',
                    3 => 'Bestellübersicht',
                    4 => 'Bestätigung',
                ];

                foreach ($dataHandler2->copyMappingArray_merged['tx_powermail_domain_model_page'] ?? [] as $origUid => $transUid) {
                    // Determine which page by looking up sorting
                    foreach ($pageLabels as $sorting => $label) {
                        $germanData['tx_powermail_domain_model_page'][$transUid] = [
                            'title' => $label,
                        ];
                    }
                }

                // German labels for all fields, keyed by marker.
                // Each entry contains the columns to UPDATE on the translated record.
                // 'title': translated field label | 'settings': translated dropdown options
                // 'text': translated HTML/display content
                $fieldGermanLabels = [
                    // Page 1: Rechtsform dropdown
                    'rechtsform'          => ['title' => 'Rechtsform', 'settings' => "Bitte wählen...\nEinzelunternehmen\nEinzelunternehmen e.U.\nOG (Offene Gesellschaft)\nKG (Kommanditgesellschaft)\nGmbH\nAG (Aktiengesellschaft)\nVerein\nGesBR"],
                    // Page 2: Common contact fields
                    'firma'               => ['title' => 'Firmenname'],
                    'anrede'              => ['title' => 'Anrede', 'settings' => "Herr\nFrau\nDivers"],
                    'vorname'             => ['title' => 'Vorname'],
                    'nachname'            => ['title' => 'Nachname'],
                    'email'               => ['title' => 'E-Mail-Adresse'],
                    'telefon'             => ['title' => 'Telefon'],
                    'strasse'             => ['title' => 'Straße'],
                    'plz'                 => ['title' => 'PLZ'],
                    'ort'                 => ['title' => 'Ort'],
                    'uid_nummer'          => ['title' => 'UID-Nummer'],
                    // Page 2: Conditional fields
                    'firmenbuchnummer'    => ['title' => 'Firmenbuchnummer'],
                    'firmenbuchgericht'   => ['title' => 'Firmenbuchgericht'],
                    'stammkapital'        => ['title' => 'Stammkapital'],
                    'geschaeftsfuehrer'   => ['title' => 'Geschäftsführer'],
                    'grundkapital'        => ['title' => 'Grundkapital'],
                    'vorstandsvorsitzender' => ['title' => 'Vorstandsvorsitzender'],
                    'gewerbeberechtigung' => ['title' => 'Gewerbeberechtigung'],
                    'wko_mitgliedsnr'     => ['title' => 'WKO-Mitgliedsnummer'],
                    'gesellschafter'      => ['title' => 'Gesellschafter (einer pro Zeile)'],
                    'komplementaer'       => ['title' => 'Komplementär'],
                    'zvr_zahl'            => ['title' => 'ZVR-Zahl'],
                    'vereinssitz'         => ['title' => 'Vereinssitz'],
                    'obmann'              => ['title' => 'Obmann/Obfrau'],
                    // Page 3: Product cards (HTML content translated) + quantities
                    'produkt1_info'       => ['title' => 'Website Basis', 'text' => '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=250&fit=crop" alt="Website Basis" style="width:100%;max-width:400px;border-radius:8px;"><h3>Website Basis</h3><p>Professionelle One-Page-Website mit responsivem Design, Kontaktformular und SEO-Grundlagen. Perfekt für Freelancer und Kleinunternehmen.</p><p><strong>EUR 990 (einmalig)</strong></p></div>'],
                    'produkt1_menge'      => ['title' => 'Anzahl Website Basis'],
                    'produkt2_info'       => ['title' => 'Website Professional', 'text' => '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=250&fit=crop" alt="Website Professional" style="width:100%;max-width:400px;border-radius:8px;"><h3>Website Professional</h3><p>Mehrseiten-Website mit CMS, Blog, Bildergalerien, Mehrsprachigkeit und erweitertem SEO. Ideal für wachsende Unternehmen.</p><p><strong>EUR 2.490 (einmalig)</strong></p></div>'],
                    'produkt2_menge'      => ['title' => 'Anzahl Website Professional'],
                    'produkt3_info'       => ['title' => 'SEO-Paket', 'text' => '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=400&h=250&fit=crop" alt="SEO-Paket" style="width:100%;max-width:400px;border-radius:8px;"><h3>SEO-Paket</h3><p>Monatliche Suchmaschinenoptimierung: Keyword-Recherche, OnPage-Optimierung, Content-Strategie, Linkaufbau und monatliches Reporting.</p><p><strong>EUR 490/Monat</strong></p></div>'],
                    'produkt3_menge'      => ['title' => 'Anzahl SEO-Paket'],
                    'produkt4_info'       => ['title' => 'Wartungsvertrag', 'text' => '<div class="powermail-product"><img src="https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=400&h=250&fit=crop" alt="Wartungsvertrag" style="width:100%;max-width:400px;border-radius:8px;"><h3>Wartungsvertrag</h3><p>Monatliche TYPO3-Wartung: Sicherheitsupdates, Backups, Uptime-Monitoring, Performance-Optimierung und 2h Support inklusive.</p><p><strong>EUR 190/Monat</strong></p></div>'],
                    'produkt4_menge'      => ['title' => 'Anzahl Wartungsvertrag'],
                    // Page 3: Notes + GDPR
                    'anmerkungen'         => ['title' => 'Anmerkungen'],
                    'agb'                 => ['title' => 'Ich akzeptiere die AGB'],
                    'datenschutz'         => ['title' => 'Ich stimme der Datenverarbeitung gemäß DSGVO Art. 6 Abs. 1 lit. a zu'],
                    'widerruf'            => ['title' => 'Ich nehme das Widerrufsrecht (14 Tage) zur Kenntnis'],
                    // Page 4: Summary + submit
                    'zusammenfassung'     => ['title' => 'Zusammenfassung', 'text' => 'Bitte überprüfen Sie Ihre Bestellung und klicken Sie auf Absenden.'],
                    'absenden'            => ['title' => 'Bestellung absenden'],
                ];

                // Map each translated field to its German labels:
                // copyMappingArray_merged[table][original_uid] = translated_uid
                // We look up the marker for each original UID, then apply the German label
                foreach ($dataHandler2->copyMappingArray_merged['tx_powermail_domain_model_field'] ?? [] as $origUid => $transUid) {
                    foreach ($fieldUids as $marker => $uid) {
                        if ($uid === $origUid && isset($fieldGermanLabels[$marker])) {
                            // Update the translated record with German title/settings/text
                            $germanData['tx_powermail_domain_model_field'][$transUid] = $fieldGermanLabels[$marker];
                            break;
                        }
                    }
                }

                // Execute the label updates via a third DataHandler instance
                $dataHandler3 = GeneralUtility::makeInstance(DataHandler::class);
                $dataHandler3->bypassAccessCheckForRecords = true;
                $dataHandler3->start($germanData, []);  // Datamap only (updates)
                $dataHandler3->process_datamap();

                $io->success('German translation created.');
            }
        }

        // ---------------------------------------------------------
        // 3. Conditions (powermail_cond)
        // ---------------------------------------------------------
        // Creates condition rules that dynamically show/hide fields based on
        // the rechtsform (legal type) dropdown value.
        //
        // powermail_cond structure:
        //   Container → has many Conditions → each has many Rules
        //   Container: groups all conditions for one form
        //   Condition: defines the TARGET field to show/hide + action + conjunction
        //   Rule: checks the SOURCE field value with an operator
        //
        // Operator codes (ops):
        //   0=is set, 1=is not set, 2=contains, 3=not contains,
        //   4=is (exact), 5=is not (exact), 6=greater, 7=less
        //
        // Action codes: 0=hide target when rules match, 1=show target when rules match
        if ($input->getOption('with-conditions')) {
            $io->section('Creating conditions...');

            $condData = [];

            // Condition container: one per form, links all conditions to the form
            $condData['tx_powermailcond_domain_model_conditioncontainer']['NEW_container'] = [
                'pid' => self::STORAGE_PID,
                'title' => 'Rechtsform Conditions',
                'form' => $formUid,                  // Link to our form
            ];

            // Condition definitions array:
            // Format: [target_marker, action, conjunction, rules[]]
            //   target_marker: field to show/hide (resolved to UID via $fieldUids)
            //   action: '0'=hide when rules match, '1'=show when rules match
            //   conjunction: 'AND'=all rules must match, 'OR'=any rule matches
            //   rules: [[source_marker, operator, compare_value], ...]
            $conditions = [
                // Firmenbuchnummer: HIDE when rechtsform is one of the types that don't need it
                // ops=4 "is": exact match → hide when value equals Einzelunternehmen/Verein/GesBR/placeholder
                // Result: field visible only for e.U., OG, KG, GmbH, AG
                ['firmenbuchnummer', '0', 'OR', [
                    ['rechtsform', 4, 'Einzelunternehmen'],    // ops=4: is exact match
                    ['rechtsform', 4, 'Verein'],
                    ['rechtsform', 4, 'GesBR'],
                    ['rechtsform', 4, 'Please select...'],     // Placeholder = no selection
                ]],
                // Firmenbuchgericht: same visibility logic as Firmenbuchnummer
                ['firmenbuchgericht', '0', 'OR', [
                    ['rechtsform', 4, 'Einzelunternehmen'],
                    ['rechtsform', 4, 'Verein'],
                    ['rechtsform', 4, 'GesBR'],
                    ['rechtsform', 4, 'Please select...'],
                ]],
                // Stammkapital: HIDE when NOT GmbH → visible only for GmbH
                // ops=5 "is not": hide when rechtsform doesn't equal 'GmbH'
                ['stammkapital', '0', 'AND', [
                    ['rechtsform', 5, 'GmbH'],                 // ops=5: is not
                ]],
                // Geschäftsführer: same as Stammkapital (GmbH only)
                ['geschaeftsfuehrer', '0', 'AND', [
                    ['rechtsform', 5, 'GmbH'],
                ]],
                // Grundkapital: HIDE when NOT AG → visible only for AG
                ['grundkapital', '0', 'AND', [
                    ['rechtsform', 5, 'AG (Aktiengesellschaft)'],
                ]],
                // Vorstandsvorsitzender: same as Grundkapital (AG only)
                ['vorstandsvorsitzender', '0', 'AND', [
                    ['rechtsform', 5, 'AG (Aktiengesellschaft)'],
                ]],
                // Gewerbeberechtigung: HIDE when NOT Einzelunternehmen
                ['gewerbeberechtigung', '0', 'AND', [
                    ['rechtsform', 5, 'Einzelunternehmen'],
                ]],
                // WKO Mitgliedsnr: same as Gewerbeberechtigung (Einzelunternehmen only)
                ['wko_mitgliedsnr', '0', 'AND', [
                    ['rechtsform', 5, 'Einzelunternehmen'],
                ]],
                // Gesellschafter: HIDE when rechtsform NOT contains 'OG' AND is not 'GesBR'
                // conjunction='AND': both rules must match to hide
                // ops=3 "not contains" + ops=5 "is not" → visible for OG or GesBR
                ['gesellschafter', '0', 'AND', [
                    ['rechtsform', 3, 'OG'],                   // ops=3: not contains
                    ['rechtsform', 5, 'GesBR'],                // ops=5: is not
                ]],
                // Komplementär: HIDE when NOT contains 'KG' → visible only for KG
                ['komplementaer', '0', 'AND', [
                    ['rechtsform', 3, 'KG'],                   // ops=3: not contains
                ]],
                // ZVR-Zahl: HIDE when NOT Verein → visible only for Verein
                ['zvr_zahl', '0', 'AND', [
                    ['rechtsform', 5, 'Verein'],
                ]],
                // Vereinssitz: same as ZVR-Zahl (Verein only)
                ['vereinssitz', '0', 'AND', [
                    ['rechtsform', 5, 'Verein'],
                ]],
                // Obmann: same as ZVR-Zahl (Verein only)
                ['obmann', '0', 'AND', [
                    ['rechtsform', 5, 'Verein'],
                ]],
            ];

            // Build DataHandler datamap entries for all conditions and rules
            $condIdx = 0;
            foreach ($conditions as [$targetMarker, $action, $conjunction, $rules]) {
                $condKey = 'NEW_cond_' . $condIdx;

                // Resolve target marker to real UID (from $fieldUids map built in Step 1)
                $targetFieldUid = $fieldUids[$targetMarker]
                    ?? throw new \RuntimeException('Unknown field marker: ' . $targetMarker);

                // Create rule records for this condition
                $ruleKeys = [];
                foreach ($rules as $ruleIdx => [$startMarker, $operator, $condString]) {
                    $ruleKey = $condKey . '_rule_' . $ruleIdx;
                    $ruleKeys[] = $ruleKey;
                    $condData['tx_powermailcond_domain_model_rule'][$ruleKey] = [
                        'pid' => self::STORAGE_PID,
                        'title' => 'Rule ' . ($ruleIdx + 1),
                        'start_field' => $fieldUids[$startMarker]  // Source field UID to check
                            ?? throw new \RuntimeException('Unknown start field: ' . $startMarker),
                        'ops' => $operator,           // Operator code (4=is, 5=is not, 3=not contains, etc.)
                        'cond_string' => $condString, // Value to compare against
                    ];
                }

                // Create the condition record linking rules to the target field
                $condData['tx_powermailcond_domain_model_condition'][$condKey] = [
                    'pid' => self::STORAGE_PID,
                    'conditioncontainer' => 'NEW_container',        // IRRE: parent container
                    'title' => 'Cond: ' . $targetMarker,
                    'target_field' => (string)$targetFieldUid,      // Field UID to show/hide (varchar!)
                    'actions' => $action,                           // '0'=hide, '1'=show
                    'conjunction' => $conjunction,                  // 'AND' or 'OR'
                    'rules' => implode(',', $ruleKeys),             // IRRE: comma-separated rule NEW_xxx IDs
                ];

                $condIdx++;
            }

            // Execute all condition + rule inserts in a single DataHandler call
            $dataHandler4 = GeneralUtility::makeInstance(DataHandler::class);
            $dataHandler4->bypassAccessCheckForRecords = true;
            $dataHandler4->start($condData, []);
            $dataHandler4->process_datamap();

            if ($dataHandler4->errorLog !== []) {
                $io->error('Condition errors:');
                foreach ($dataHandler4->errorLog as $error) {
                    $io->writeln('  - ' . $error);
                }
                return Command::FAILURE;
            }

            $containerUid = (int)$dataHandler4->substNEWwithIDs['NEW_container'];
            $io->success('Conditions created. Container UID: ' . $containerUid);
            $io->writeln('  Total conditions: ' . count($conditions));
        }

        // ---------------------------------------------------------
        // Done
        // ---------------------------------------------------------
        $io->newLine();
        $io->success('All done! Flush caches: ddev typo3 cache:flush');

        return Command::SUCCESS;
    }
}
```

### Register the Command

**File:** `Configuration/Services.yaml`

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\SitePackage\:
    resource: '../Classes/*'

  Vendor\SitePackage\Command\CreateShopFormCommand:
    tags:
      - name: console.command
        command: 'shop:create-form'
        description: 'Create multi-step shop form with conditions'
```

### Run the Command

```bash
# Create English form only
ddev typo3 shop:create-form

# Create with German translation
ddev typo3 shop:create-form --with-german

# Create with German translation AND conditions
ddev typo3 shop:create-form --with-german --with-conditions

# Full setup with cache flush
ddev typo3 shop:create-form -g -c && ddev typo3 cache:flush
```

### Output Example

```
 ! [WARNING] LOCAL DEVELOPMENT ONLY!
 !           Never run this command on a production site.
 !           It creates test data that will pollute your database.

 Creating form structure (English)...

 [OK] Form created with UID 10

 ---------- -----
  Marker     UID
 ---------- -----
  rechtsform  42
  firma       43
  email       47
  ...
 ---------- -----

 Creating German translation...

 [OK] German translation created.

 Creating conditions...

 [OK] Conditions created. Container UID: 1
   Total conditions: 13

 [OK] All done! Flush caches: ddev typo3 cache:flush
```

---

## Workspace Support

> **What are TYPO3 Workspaces?** Workspaces let editors draft, review, and stage changes
> before publishing to the live site. Records created or modified in a workspace are stored
> as "versioned" copies. They only become live when an editor publishes (swaps) them.

> **Workspace UID:** Most TYPO3 installations that use workspaces have at least one custom
> workspace with UID `1` (the first workspace created in the backend module). Adjust
> `@ws_id` / `WORKSPACE_ID` below to match your setup. Check your workspaces via:
> `ddev mysql -e "SELECT uid, title FROM sys_workspace WHERE deleted=0;"`

### How Workspaces Affect Powermail Records

When TYPO3 workspaces are enabled (EXT:workspaces installed), the powermail tables gain
additional versioning columns managed automatically by TYPO3 Core:

| Column | Type | Description |
|--------|------|-------------|
| `t3ver_wsid` | int | **Workspace ID**: `0` = live, `>0` = draft in that workspace |
| `t3ver_oid` | int | **Original UID**: for modified records, points to the live version |
| `t3ver_state` | smallint | **Version state**: `0` = default, `1` = new (only in workspace), `-1` = move placeholder |
| `t3ver_stage` | int | **Review stage**: `0` = editing, `1` = ready to review, `10` = ready to publish, `-1` = rejected |

**Key rules:**
- `t3ver_wsid = 0`: record is **live** (visible to frontend visitors)
- `t3ver_wsid > 0`: record is a **draft** in that workspace (only visible in workspace preview)
- New records created in a workspace get `t3ver_state = 1` (new placeholder)
- Modified records: the original stays live, a copy with changes lives in the workspace

### SQL Approach: Creating Form in a Workspace

To create the shop form as a **workspace draft** (not immediately live), add the workspace
columns to all INSERT statements. Use `@ws_id = 1` for the default workspace.

```bash
ddev mysql -e "
-- =============================================
-- WORKSPACE DRAFT: Create form in workspace 1
-- =============================================
-- All records get t3ver_wsid=@ws_id so they exist only in the workspace.
-- t3ver_state=1 marks them as 'new in workspace' (not yet published).
-- t3ver_stage=0 means 'editing' (not yet staged for review).
-- Records will NOT appear on the live site until published.

SET @ws_id = 1;  -- Workspace UID (adjust to your workspace)

-- Create form in workspace (not live)
INSERT INTO tx_powermail_domain_model_form
  (pid, title, css, sys_language_uid, l10n_parent,
   t3ver_wsid, t3ver_state, t3ver_stage,
   tstamp, crdate)
VALUES
  (1, 'Order Form', 'order-form', 0, 0,
   @ws_id, 1, 0,  -- wsid=workspace, state=1 (new), stage=0 (editing)
   UNIX_TIMESTAMP(), UNIX_TIMESTAMP());
SET @form_uid = LAST_INSERT_ID();

-- Create pages in workspace
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, css, sorting, sys_language_uid, l10n_parent,
   t3ver_wsid, t3ver_state, t3ver_stage,
   tstamp, crdate)
VALUES
  (1, @form_uid, 'Legal Type',      'step-legal-type', 1, 0, 0, @ws_id, 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @form_uid, 'Contact Data',    'step-contact',    2, 0, 0, @ws_id, 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @form_uid, 'Order Overview',  'step-overview',   3, 0, 0, @ws_id, 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()),
  (1, @form_uid, 'Confirmation',    'step-confirm',    4, 0, 0, @ws_id, 1, 0, UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- For fields, add the same 3 columns to every INSERT:
--   t3ver_wsid = @ws_id
--   t3ver_state = 1
--   t3ver_stage = 0
-- (Same pattern as above — add these 3 columns to all field INSERTs from Step 1)

-- Example: Page 1 field in workspace
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, settings, sorting,
   sys_language_uid, l10n_parent,
   t3ver_wsid, t3ver_state, t3ver_stage,
   tstamp, crdate)
VALUES
  (1, (SELECT uid FROM tx_powermail_domain_model_page
       WHERE form = @form_uid AND sorting = 1 AND t3ver_wsid = @ws_id LIMIT 1),
   'Legal Type', 'select', 'rechtsform', 1,
   'Please select...\nEinzelunternehmen\nEinzelunternehmen e.U.\nOG (Offene Gesellschaft)\nKG (Kommanditgesellschaft)\nGmbH\nAG (Aktiengesellschaft)\nVerein\nGesBR',
   1, 0, 0,
   @ws_id, 1, 0,
   UNIX_TIMESTAMP(), UNIX_TIMESTAMP());

-- Continue with all other fields using the same pattern...
-- NOTE: When looking up page UIDs for fields, add AND t3ver_wsid = @ws_id
-- to ensure you reference the workspace version, not a live record.

SELECT @form_uid AS workspace_form_uid, @ws_id AS workspace_id;
"
```

> **Important:** When querying workspace records in subsequent steps (German translation,
> conditions), add `AND t3ver_wsid = @ws_id` to all SELECT lookups:
> ```sql
> SET @form_uid = (SELECT uid FROM tx_powermail_domain_model_form
>   WHERE title = 'Order Form' AND sys_language_uid = 0
>   AND t3ver_wsid = @ws_id ORDER BY uid DESC LIMIT 1);
> ```

### SQL: Publishing Workspace Records

After review, publish (swap) workspace records to make them live:

```bash
# Stage all records for review (t3ver_stage = 1)
ddev mysql -e "
SET @ws_id = 1;
SET @form_uid = (SELECT uid FROM tx_powermail_domain_model_form
  WHERE title = 'Order Form' AND t3ver_wsid = @ws_id
  ORDER BY uid DESC LIMIT 1);

-- Stage form for review
UPDATE tx_powermail_domain_model_form
  SET t3ver_stage = 1  -- 1 = ready for review
  WHERE uid = @form_uid;

-- Stage all related pages
UPDATE tx_powermail_domain_model_page
  SET t3ver_stage = 1
  WHERE form = @form_uid AND t3ver_wsid = @ws_id;

-- Stage all related fields
UPDATE tx_powermail_domain_model_field
  SET t3ver_stage = 1
  WHERE page IN (
    SELECT uid FROM tx_powermail_domain_model_page
    WHERE form = @form_uid AND t3ver_wsid = @ws_id
  ) AND t3ver_wsid = @ws_id;

SELECT 'Records staged for review' AS status;
"

# Actually publish: use the TYPO3 CLI (recommended over raw SQL!)
# This properly handles all workspace swapping, cache clearing, and index updates.
ddev typo3 workspace:publish 1
```

> **Best practice:** Always use `ddev typo3 workspace:publish <workspace_id>` or the
> backend Workspaces module to publish. Raw SQL `UPDATE ... SET t3ver_wsid=0` will
> break reference index and skip workspace events.

### DataHandler CLI: Workspace-Aware Form Creation

The DataHandler approach is **strongly recommended** for workspaces because it handles
all versioning columns, reference index, and workspace events automatically.

The only change needed: set the backend user's workspace before executing DataHandler.

Add a `--workspace` option to the CLI command:

```php
// In configure():
$this->addOption(
    'workspace',
    'w',
    InputOption::VALUE_REQUIRED,
    'Create records in this workspace ID (default: 0 = live)',
    '0'
);

// In execute(), BEFORE creating the DataHandler:
$workspaceId = (int)$input->getOption('workspace');

if ($workspaceId > 0) {
    $io->note('Creating records in workspace ' . $workspaceId);

    // Verify workspace exists
    $wsRecord = GeneralUtility::makeInstance(\TYPO3\CMS\Core\Database\ConnectionPool::class)
        ->getConnectionForTable('sys_workspace')
        ->select(['uid', 'title'], 'sys_workspace', ['uid' => $workspaceId, 'deleted' => 0])
        ->fetchAssociative();

    if (!$wsRecord) {
        $io->error('Workspace ' . $workspaceId . ' not found.');
        return Command::FAILURE;
    }

    $io->writeln('  Workspace: ' . $wsRecord['title']);

    // Set the backend user's workspace — DataHandler reads this automatically.
    // All records created by DataHandler will get t3ver_wsid = $workspaceId.
    $GLOBALS['BE_USER']->setWorkspace($workspaceId);
}

// The rest of the code stays EXACTLY the same!
// DataHandler automatically:
//   - Sets t3ver_wsid on all new records
//   - Sets t3ver_state = 1 (new in workspace)
//   - Handles IRRE children in workspace context
//   - Manages reference index for workspace versions

$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->bypassAccessCheckForRecords = true;
// ... all existing $data array code unchanged ...
```

### Running the Command with Workspaces

```bash
# Create form in live workspace (default, same as before)
ddev typo3 shop:create-form -g -c

# Create form as draft in workspace 1
ddev typo3 shop:create-form -g -c --workspace=1

# Create form in workspace 1, then publish
ddev typo3 shop:create-form -g -c -w 1
ddev typo3 workspace:publish 1 && ddev typo3 cache:flush

# Check which workspace a form lives in
ddev mysql -e "
SELECT uid, title, t3ver_wsid, t3ver_state, t3ver_stage
FROM tx_powermail_domain_model_form
WHERE deleted = 0
ORDER BY uid DESC LIMIT 5;
"
```

### Workspace Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Form invisible in frontend | Records still in workspace (`t3ver_wsid > 0`) | Publish via backend module or `workspace:publish` CLI |
| Conditions not working in preview | Condition container not in same workspace | Ensure conditions have same `t3ver_wsid` as form |
| Duplicate fields after publish | Localization created both live + workspace copies | Use DataHandler `localize` instead of raw SQL |
| Form shows in workspace preview but fields missing | Field `page` column points to wrong page version | Use DataHandler — it resolves IRRE relations correctly |
| `t3ver_stage` stuck at 0 | Records never staged for review | Stage via backend module or update `t3ver_stage = 1` |

---

## Condition Logic Summary

| Legal Type | FB-Nr | FB-Gericht | Stammkapital | GF | Grundkapital | Vorstand | Gewerbe | WKO | Gesellschafter | Komplementär | ZVR | V-Sitz | Obmann |
|------------|:-----:|:----------:|:------------:|:--:|:------------:|:--------:|:-------:|:---:|:--------------:|:------------:|:---:|:------:|:------:|
| Einzelunternehmen | | | | | | | x | x | | | | | |
| e.U. | x | x | | | | | | | | | | | |
| OG | x | x | | | | | | | x | | | | |
| KG | x | x | | | | | | | | x | | | |
| GmbH | x | x | x | x | | | | | | | | | |
| AG | x | x | | | x | x | | | | | | | |
| Verein | | | | | | | | | | | x | x | x |
| GesBR | | | | | | | | | x | | | | |

`x` = field is visible for this legal type
