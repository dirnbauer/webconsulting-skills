---
name: "typo3-powermail"
description: "Guides Powermail 13+ form development for TYPO3, including form setup, finishers, validators, spam protection, ViewHelpers, PSR-14 events, TypoScript, email templates, conditional visibility, and extension points. Use when creating, debugging, or extending powermail forms, mail handling, validation, finishers, powermail_cond behavior, or tx_powermail data."
metadata:
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Powermail Development

> Source: https://github.com/dirnbauer/webconsulting-skills

> **Compatibility:** Powermail **13.x** currently targets **TYPO3 13.4** per Packagist — do **not** assume v14 until the package declares it. Examples use modern TYPO3 APIs where possible; adjust for your Core version.
> All examples use PHP 8.2+.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

> **Supplements:**
> - [SKILL-CONDITIONS.md](SKILL-CONDITIONS.md) - Conditional field/page visibility (powermail_cond)
> - PHP 8.4 patterns for finishers, validators, and conditions are covered directly in this skill
> - [SKILL-EXAMPLES.md](SKILL-EXAMPLES.md) - Multi-step shop form with Austrian legal types, DDEV SQL + DataHandler CLI

## Powermail vs Core EXT:form

These are **different systems**. Do not mix migration advice between them.

| | **Powermail (`in2code/powermail`)** | **TYPO3 Core EXT:form** |
|---|-------------------------------------|-------------------------|
| **Purpose** | Mail forms built in the Powermail backend module; stored in `tx_powermail_*` tables | Declarative forms (often YAML), `form` framework, finishers defined in YAML/PHP |
| **Rendering** | Powermail plugins / ViewHelpers / TypoScript | Fluid templates + Core form runtime |
| **This skill** | Documents Powermail APIs, finishers, validators, events **as shipped by in2code** | Only where **your** code also touches EXT:form (bridges, shared sites, dual form stacks) |

Sections labeled **EXT:form** under [v14-Only Changes](#v14-only-changes) describe **Core** form-framework removals (hooks → PSR-14, storage adapters). They apply to custom code that hooks into **EXT:form**, not to ordinary Powermail-only projects—unless you explicitly integrate both.

## 1. Architecture Overview

### Domain Model Hierarchy

```
Form (tx_powermail_domain_model_form)
 └── Page (tx_powermail_domain_model_page)
      └── Field (tx_powermail_domain_model_field)

Mail (tx_powermail_domain_model_mail)
 └── Answer (tx_powermail_domain_model_answer)
      └── references Field
```

### Plugin Registration

- **Pi1** (cached/uncached): `form`, `create`, `confirmation`, `optinConfirm`, `disclaimer`
- **Pi5** (uncached): `marketing` (AJAX tracking)

### Composer

```bash
composer require in2code/powermail
```

Typical requirements (always confirm the **current** release on [Packagist](https://packagist.org/packages/in2code/powermail)): PHP **^8.2**, **`typo3/cms-core: ^13.4`** (latest stable line at time of writing), plus ext-json, ext-gd, ext-fileinfo, ext-curl. **Do not assume TYPO3 v14** until the package constraint is updated upstream.

## 2. Field Types

| Type | Key | Value Type | Notes |
|------|-----|------------|-------|
| Text | `input` | TEXT (0) | Standard input |
| Textarea | `textarea` | TEXT (0) | Multi-line |
| Select | `select` | TEXT/ARRAY (0/1) | Multiselect possible |
| Checkbox | `check` | ARRAY (1) | Multiple values |
| Radio | `radio` | TEXT (0) | Single selection |
| Submit | `submit` | — | Form submit button |
| Captcha | `captcha` | TEXT (0) | Built-in CAPTCHA |
| Reset | `reset` | — | Form reset button |
| Static text | `text` | — | Display only |
| Content element | `content` | — | CE reference |
| HTML | `html` | TEXT (0) | Raw HTML |
| Password | `password` | PASSWORD (4) | Hashed storage |
| File upload | `file` | UPLOAD (3) | File attachments |
| Hidden | `hidden` | TEXT (0) | Hidden input |
| Date | `date` | DATE (2) | Datepicker |
| Country | `country` | TEXT (0) | Country selector |
| Location | `location` | TEXT (0) | Geolocation |
| TypoScript | `typoscript` | TEXT (0) | TS-generated content |

### Answer Value Types

```php
Answer::VALUE_TYPE_TEXT     = 0;  // String values
Answer::VALUE_TYPE_ARRAY    = 1;  // JSON-encoded arrays (checkboxes, multiselect)
Answer::VALUE_TYPE_DATE     = 2;  // Timestamps
Answer::VALUE_TYPE_UPLOAD   = 3;  // File references
Answer::VALUE_TYPE_PASSWORD = 4;  // Hashed passwords
```

## 3. TypoScript Configuration

### Essential Settings

```typoscript
plugin.tx_powermail {
    settings {
        setup {
            # Form settings
            main {
                pid = {$plugin.tx_powermail.settings.main.pid}
                form = {$plugin.tx_powermail.settings.main.form}
                confirmation = 0
                optin = 0
                morestep = 0
            }

            # Receiver mail
            receiver {
                enable = 1
                subject = Mail from {firstname} {lastname}
                body = A new mail from your website
                senderNameField = firstname
                senderEmailField = email
                # Override receiver: receiver.overwrite.email = admin@example.com
                # Attach uploads: receiver.attachment = 1
                # Add CC: receiver.overwrite.cc = copy@example.com
            }

            # Sender confirmation mail
            sender {
                enable = 1
                subject = Thank you for your message
                body = We received your submission
                senderName = Website
                senderEmail = noreply@example.com
            }

            # Double Opt-In
            optin {
                subject = Please confirm your submission
                senderName = Website
                senderEmail = noreply@example.com
            }

            # Thank you page
            thx {
                redirect = # Page UID for redirect after submit
            }

            # Spam protection — numeric `methods` keys (matches EXT:powermail `12_Spamshield.typoscript`)
            spamshield {
                _enable = 1
                factor = 75
                methods {
                    1 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\HoneyPodMethod
                        indication = 5
                        configuration { }
                    }
                    2 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\LinkMethod
                        indication = 3
                        configuration {
                            linkLimit = 2
                        }
                    }
                    3 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\NameMethod
                        indication = 3
                        configuration { }
                    }
                    # SessionMethod sets a cookie when enabled — shipping TypoScript uses _enable = 0
                    4 {
                        _enable = 0
                        class = In2code\Powermail\Domain\Validator\SpamShield\SessionMethod
                        indication = 5
                        configuration { }
                    }
                    5 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\UniqueMethod
                        indication = 2
                        configuration { }
                    }
                    6 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\ValueBlacklistMethod
                        indication = 7
                        configuration {
                            values = TEXT
                            values.value = viagra,sex,porn
                        }
                    }
                    7 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\IpBlacklistMethod
                        indication = 7
                        configuration {
                            values = TEXT
                            values.value = 203.0.113.1
                        }
                    }
                    8 {
                        _enable = 1
                        class = In2code\Powermail\Domain\Validator\SpamShield\RateLimitMethod
                        indication = 100
                        configuration {
                            interval = 5 minutes
                            limit = 10
                            restrictions {
                                10 = __ipAddress
                                20 = __formIdentifier
                            }
                        }
                    }
                }
            }

            # Validation
            misc {
                htmlForLabels = 1
                showOnlyFilledValues = 1
                ajaxSubmit = 0
                file {
                    folder = uploads/tx_powermail/
                    size = 25000000
                    extension = jpg,jpeg,gif,png,tif,txt,doc,docx,xls,xlsx,ppt,pptx,pdf,zip,csv,svg
                }
            }
        }
    }
}
```

### Prefill Fields via TypoScript

```typoscript
plugin.tx_powermail.settings.setup.prefill {
    # By field marker
    email = TEXT
    email.data = TSFE:fe_user|user|email

    firstname = TEXT
    firstname.data = TSFE:fe_user|user|first_name

    # Prefill from GET/POST
    subject = TEXT
    subject.data = GP:subject
}
```

### Marketing Information

```typoscript
plugin.tx_powermail.settings.setup.marketing {
    enable = 1
    # Tracked: refererDomain, referer, country, mobileDevice, frontendLanguage, browserLanguage, pageFunnel
}
```


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
