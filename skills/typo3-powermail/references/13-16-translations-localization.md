# 16. Translations (Localization)

Continues `typo3-powermail` from [full guide](full-guide.md).

## 16. Translations (Localization)

Powermail supports full TYPO3 localization. Form structure (form, pages, fields) can be translated so editors see localized labels, settings, and options. Submitted mails inherit the frontend language.

### How Translation Works

| Level | What gets translated | Key columns |
|-------|---------------------|-------------|
| Form | Title | `sys_language_uid`, `l10n_parent` |
| Page | Title (step heading) | `sys_language_uid`, `l10n_parent` |
| Field | Title, settings, placeholder, mandatory_text, description | `sys_language_uid`, `l10n_parent` |
| Mail | Automatically stored with `sys_language_uid` from frontend | `sys_language_uid` |
| Answer | Stored with language of submission | `sys_language_uid` |

### Translation Rules

- `sys_language_uid = 0` is the **default language** (e.g., English)
- `sys_language_uid = 1` (or higher) is a translation (e.g., German)
- `l10n_parent` points to the default language record UID
- The `marker` field is **not translated** -- markers stay identical across languages
- Field `type` is **not translated** -- structure is shared
- Field `settings` (select/radio options) **is translated** -- option labels change per language

### Example: Create Form in English, Translate to German

#### Default Language (English, sys_language_uid=0)

```sql
-- Form
INSERT INTO tx_powermail_domain_model_form (pid, title, sys_language_uid, l10n_parent)
VALUES (1, 'Contact Form', 0, 0);
-- Assume UID = 10

-- Page
INSERT INTO tx_powermail_domain_model_page (pid, form, title, sorting, sys_language_uid, l10n_parent)
VALUES (1, 10, 'Your Details', 1, 0, 0);
-- Assume UID = 20

-- Fields
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sender_name, sorting, sys_language_uid, l10n_parent)
VALUES
  (1, 20, 'First Name', 'input', 'firstname', 1, 1, 1, 0, 0),   -- UID 30
  (1, 20, 'Last Name', 'input', 'lastname', 1, 0, 2, 0, 0),     -- UID 31
  (1, 20, 'Email', 'input', 'email', 1, 0, 3, 0, 0),            -- UID 32
  (1, 20, 'Message', 'textarea', 'message', 0, 0, 4, 0, 0),     -- UID 33
  (1, 20, 'Subject', 'select', 'subject', 1, 0, 5, 0, 0),       -- UID 34
  (1, 20, 'Send', 'submit', 'submit', 0, 0, 6, 0, 0);           -- UID 35

-- Select options for subject (English)
UPDATE tx_powermail_domain_model_field
SET settings = 'General Inquiry\nSupport Request\nPartnership\nOther'
WHERE uid = 34;

-- Mark email field as sender_email
UPDATE tx_powermail_domain_model_field SET sender_email = 1 WHERE uid = 32;
```

#### German Translation (sys_language_uid=1)

```sql
-- Form translation (l10n_parent = 10, the English form)
INSERT INTO tx_powermail_domain_model_form (pid, title, sys_language_uid, l10n_parent)
VALUES (1, 'Kontaktformular', 1, 10);

-- Page translation (l10n_parent = 20)
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, sorting, sys_language_uid, l10n_parent)
VALUES (1, 10, 'Ihre Daten', 1, 1, 20);

-- Field translations (l10n_parent points to English field UID)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sender_name, sorting, sys_language_uid, l10n_parent)
VALUES
  (1, 20, 'Vorname', 'input', 'firstname', 1, 1, 1, 1, 30),
  (1, 20, 'Nachname', 'input', 'lastname', 1, 0, 2, 1, 31),
  (1, 20, 'E-Mail-Adresse', 'input', 'email', 1, 0, 3, 1, 32),
  (1, 20, 'Nachricht', 'textarea', 'message', 0, 0, 4, 1, 33),
  (1, 20, 'Betreff', 'select', 'subject', 1, 0, 5, 1, 34),
  (1, 20, 'Absenden', 'submit', 'submit', 0, 0, 6, 1, 35);

-- German select options for subject
UPDATE tx_powermail_domain_model_field
SET settings = 'Allgemeine Anfrage\nSupportanfrage\nPartnerschaft\nSonstiges'
WHERE sys_language_uid = 1 AND l10n_parent = 34;

-- Mark email field as sender_email (must be set on translation too)
UPDATE tx_powermail_domain_model_field
SET sender_email = 1
WHERE sys_language_uid = 1 AND l10n_parent = 32;
```

### Translation via DataHandler

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->start([], []);

// Localize form (UID 10) to German (sys_language_uid=1)
$cmdMap = [
    'tx_powermail_domain_model_form' => [
        10 => [
            'localize' => 1, // target language UID
        ],
    ],
];
$dataHandler->start([], $cmdMap);
$dataHandler->process_cmdmap();

// DataHandler auto-creates translations of all IRRE children (pages + fields)
// Then update the translated titles:
$translatedFormUid = $dataHandler->copyMappingArray_merged['tx_powermail_domain_model_form'][10] ?? null;
if ($translatedFormUid) {
    $data = [
        'tx_powermail_domain_model_form' => [
            $translatedFormUid => [
                'title' => 'Kontaktformular',
            ],
        ],
    ];
    $dataHandler->start($data, []);
    $dataHandler->process_datamap();
}
```

### Important Translation Notes

- **Markers are language-independent.** The marker `email` stays `email` in all languages.
- **IRRE localization:** When you localize a form via DataHandler (`localize` command), TYPO3 automatically creates translations for all child pages and fields.
- **Select options:** The `settings` field (select/radio/check options) **must** be translated separately -- option values should match (for condition evaluation) but labels can differ.
- **Submitted mails:** Mails store `sys_language_uid` from the frontend context. Answers reference the default-language field UID regardless of submission language.
- **Backend module:** The mail list shows mails from all languages. Filter by language if needed.
