# 14. Database Structure

Continues `typo3-powermail` from [full guide](full-guide.md).

## 14. Database Structure

> **Conditions tables:** See [SKILL-CONDITIONS.md](../SKILL-CONDITIONS.md) Section 12 for `tx_powermailcond_*` tables.

### TYPO3 Standard Columns

All powermail tables include these TYPO3-managed columns (not listed per table below):

| Column | Type | Purpose |
|--------|------|---------|
| `uid` | int AUTO_INCREMENT | Primary key |
| `pid` | int | Storage page UID |
| `tstamp` | int | Last modification timestamp |
| `crdate` | int | Creation timestamp |
| `deleted` | tinyint | Soft-delete flag |
| `hidden` | tinyint | Visibility flag |
| `sys_language_uid` | int | Language UID (0 = default, -1 = all) |
| `l10n_parent` | int | UID of the default language record |
| `l10n_diffsource` | mediumblob | Diff source for translation |
| `starttime` | int | Publish start (Unix timestamp) |
| `endtime` | int | Publish end (Unix timestamp) |

### tx_powermail_domain_model_form

| Column | Type | Description |
|--------|------|-------------|
| `title` | varchar(255) | Form title |
| `note` | tinyint | Backend note renderer (internal) |
| `css` | varchar(255) | CSS class for form wrapper |
| `pages` | varchar(255) | IRRE children count or element browser list |
| `autocomplete_token` | varchar(3) | Autocomplete on/off/empty |
| `is_dummy_record` | tinyint | Test record flag |

**Indexes:** `language (l10n_parent, sys_language_uid)`

### tx_powermail_domain_model_page

| Column | Type | Description |
|--------|------|-------------|
| `form` | int | Parent form UID |
| `title` | varchar(255) | Page/step title |
| `css` | varchar(255) | CSS class for fieldset |
| `fields` | int | IRRE children count |
| `sorting` | int | Sort order within form |

**Indexes:** `parent_form (form)`, `language (l10n_parent, sys_language_uid)`

### tx_powermail_domain_model_field

| Column | Type | Description |
|--------|------|-------------|
| `page` | int | Parent page UID |
| `title` | varchar(255) | Field label |
| `type` | varchar(255) | Field type key (input, select, check, ...) |
| `settings` | text | Options for select/radio/check (one per line) |
| `path` | varchar(255) | File path reference |
| `content_element` | int | CE reference for type=content |
| `text` | text | Static text for type=text |
| `prefill_value` | text | Default/prefill value |
| `placeholder` | text | Placeholder text |
| `placeholder_repeat` | text | Placeholder for repeat field (password) |
| `create_from_typoscript` | text | TypoScript for type=typoscript |
| `validation` | int | Validation type (0=none, 1=email, ...) |
| `validation_configuration` | varchar(255) | Regex or config for validation |
| `css` | varchar(255) | CSS class for field wrapper |
| `description` | varchar(255) | Help text / description |
| `multiselect` | tinyint | Allow multi-select |
| `datepicker_settings` | varchar(255) | Datepicker format |
| `feuser_value` | varchar(255) | Prefill from fe_user property |
| `sender_email` | tinyint | This field is the sender email |
| `sender_name` | tinyint | This field is the sender name |
| `mandatory` | tinyint | Required field |
| `own_marker_select` | tinyint | Custom marker enabled |
| `marker` | varchar(255) | Field marker (variable name) |
| `mandatory_text` | varchar(255) | Custom mandatory error text |
| `autocomplete_token` | varchar(20) | Autocomplete attribute |
| `autocomplete_section` | varchar(100) | Autocomplete section |
| `autocomplete_type` | varchar(8) | Autocomplete type |
| `autocomplete_purpose` | varchar(8) | Autocomplete purpose |
| `sorting` | int | Sort order within page |

**Indexes:** `parent_page (page)`, `language (l10n_parent, sys_language_uid)`

### tx_powermail_domain_model_mail

| Column | Type | Description |
|--------|------|-------------|
| `sender_name` | varchar(255) | Submitter name |
| `sender_mail` | varchar(255) | Submitter email |
| `subject` | varchar(255) | Mail subject |
| `receiver_mail` | varchar(1024) | Receiver email(s) |
| `body` | text | Mail body (RTE) |
| `feuser` | int | Frontend user UID (if logged in) |
| `sender_ip` | tinytext | Submitter IP address |
| `user_agent` | text | Browser user agent |
| `time` | int | Submission timestamp |
| `form` | int | Source form UID |
| `answers` | int | IRRE children count |
| `spam_factor` | varchar(255) | Spam score |
| `marketing_referer_domain` | text | HTTP referer domain |
| `marketing_referer` | text | Full HTTP referer |
| `marketing_country` | text | Visitor country |
| `marketing_mobile_device` | tinyint | Mobile device flag |
| `marketing_frontend_language` | int | Frontend language UID |
| `marketing_browser_language` | text | Browser Accept-Language |
| `marketing_page_funnel` | text | Pages visited before submit |

**Indexes:** `form (form)`, `feuser (feuser)`

### tx_powermail_domain_model_answer

| Column | Type | Description |
|--------|------|-------------|
| `mail` | int | Parent mail UID |
| `value` | text | Answer value (JSON for arrays) |
| `value_type` | int | 0=text, 1=array, 2=date, 3=upload, 4=password |
| `field` | int | Source field UID |

**Indexes:** `mail (mail)`, `deleted (deleted)`, `hidden (hidden)`, `language (l10n_parent, sys_language_uid)`

### ER Diagram (Relations)

```
tx_powermail_domain_model_form
  │ 1
  ├──── * tx_powermail_domain_model_page (IRRE via form)
  │       │ 1
  │       └──── * tx_powermail_domain_model_field (IRRE via page)
  │                    │
  │                    │ referenced by
  │                    ▼
  │             tx_powermail_domain_model_answer.field
  │
  └──── * tx_powermail_domain_model_mail (via form)
           │ 1
           └──── * tx_powermail_domain_model_answer (IRRE via mail)
```
