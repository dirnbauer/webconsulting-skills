# 7. Email Templates

Continues `typo3-powermail` from [full guide](full-guide.md).

## 7. Email Templates

### Template Paths (TypoScript)

```typoscript
plugin.tx_powermail {
    view {
        templateRootPaths {
            0 = EXT:powermail/Resources/Private/Templates/
            10 = EXT:my_ext/Resources/Private/Templates/Powermail/
        }
        partialRootPaths {
            0 = EXT:powermail/Resources/Private/Partials/
            10 = EXT:my_ext/Resources/Private/Partials/Powermail/
        }
        layoutRootPaths {
            0 = EXT:powermail/Resources/Private/Layouts/
            10 = EXT:my_ext/Resources/Private/Layouts/Powermail/
        }
    }
}
```

### Key Templates

| Template | Purpose |
|----------|---------|
| `Form/Form.html` | Main form rendering |
| `Form/Confirmation.html` | Confirmation page |
| `Form/Create.html` | Thank you page |
| `Mail/ReceiverMail.html` | Admin notification email |
| `Mail/SenderMail.html` | User confirmation email |
| `Mail/OptinMail.html` | Double opt-in email |
| `Form/PowermailAll.html` | All-fields summary |

### Field Partials

Override individual field types by copying partials:

```
Partials/Form/Field/Input.html
Partials/Form/Field/Textarea.html
Partials/Form/Field/Select.html
Partials/Form/Field/Check.html
Partials/Form/Field/Radio.html
Partials/Form/Field/File.html
Partials/Form/Field/Date.html
Partials/Form/Field/Captcha.html
Partials/Form/Field/Hidden.html
Partials/Form/Field/Password.html
Partials/Form/Field/Country.html
Partials/Form/Field/Location.html
Partials/Form/Field/Html.html
Partials/Form/Field/Content.html
Partials/Form/Field/Typoscript.html
Partials/Form/Field/Submit.html
Partials/Form/Field/Reset.html
```

### Available Variables in Mail Templates

```html
<!-- In ReceiverMail.html / SenderMail.html -->
{mail}                          <!-- Mail domain object -->
{mail.senderName}               <!-- Sender name -->
{mail.senderMail}               <!-- Sender email -->
{mail.form.title}               <!-- Form title -->
{mail.answers}                  <!-- All answers (ObjectStorage) -->

<!-- Iterate answers -->
<f:for each="{mail.answers}" as="answer">
    {answer.field.title}: {answer.value}
</f:for>

<!-- PowermailAll marker (all fields formatted) -->
{powermail_all}
```
