# 9. AJAX Form Submission

Continues `typo3-powermail` from [full guide](full-guide.md).

## 9. AJAX Form Submission

```typoscript
plugin.tx_powermail.settings.setup.misc.ajaxSubmit = 1
```

When enabled, form submission is handled via AJAX without page reload. The response replaces the form container with the thank-you content.
