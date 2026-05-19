# 10. Double Opt-In

Continues `typo3-powermail` from [full guide](full-guide.md).

## 10. Double Opt-In

```typoscript
plugin.tx_powermail.settings.setup.main.optin = 1

plugin.tx_powermail.settings.setup.optin {
    subject = Please confirm your submission
    senderName = My Website
    senderEmail = noreply@example.com
}
```

Flow:
1. User submits form
2. Mail is saved with `hidden=1`
3. Opt-in email sent with confirmation link (HMAC-secured)
4. User clicks link -> `optinConfirmAction` unhides the mail
5. Receiver email sent after confirmation
