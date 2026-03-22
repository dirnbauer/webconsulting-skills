# TYPO3 Security Checklists

## Rate Limiting (TYPO3 v14)

TYPO3 v14 includes built-in rate limiting:

```php
// config/system/additional.php
// Rate limiting: check current Core / feature documentation — do not assume a stable `security.backend.rateLimiter` toggle name

// Configure rate limits
$GLOBALS['TYPO3_CONF_VARS']['BE']['loginRateLimit'] = 5;  // max attempts per default interval (see `loginRateLimitInterval`, often ~15 minutes — not “per minute”)
```

## Security Audit Checklist

### Before Go-Live

- [ ] `displayErrors` = 0
- [ ] `debug` = false (BE and FE)
- [ ] `trustedHostsPattern` configured
- [ ] Install Tool disabled
- [ ] HTTPS enforced at the edge (web server / proxy); `FE.lockSSL` no longer exists
- [ ] Strong backend passwords (12+ chars)
- [ ] MFA enabled for admins
- [ ] File permissions correct
- [ ] Sensitive directories protected
- [ ] Error logs to files, not screen
- [ ] Encryption key unique
- [ ] CSP enabled
- [ ] Rate limiting enabled

### Regular Maintenance

- [ ] Update TYPO3 core monthly
- [ ] Update extensions monthly
- [ ] Review security bulletins (https://typo3.org/security)
- [ ] Audit backend user accounts
- [ ] Review access logs
- [ ] Test backup restoration

### Monitoring

- [ ] Set up uptime monitoring
- [ ] Configure error alerting
- [ ] Monitor authentication failures
- [ ] Track file integrity (optional)

## Security Resources

- **TYPO3 Security**: https://typo3.org/security (advisories, team contact, coordinated releases)
- **Security Guide**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/Index.html
- **v14 changelog index**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html

## Remaining v14 Security Changes

> The following security changes apply **exclusively to TYPO3 v14**.

### Stronger HMAC Algorithm **[v14 only]**

TYPO3 v14 uses a **stronger cryptographic algorithm for HMAC** (#106307). Existing HMAC tokens (e.g., in URLs, form tokens) generated with the old algorithm will be invalid after upgrade. Plan for token regeneration.

### Built-in CipherService **[v14 only]**

New `CipherService` (#108002) provides **symmetric encryption/decryption** out of the box. Use it instead of custom encryption implementations:

```php
use TYPO3\CMS\Core\Crypto\Cipher\CipherService;

$cipherService = GeneralUtility::makeInstance(CipherService::class);
$keyFactory = GeneralUtility::makeInstance(\TYPO3\CMS\Core\Crypto\Cipher\KeyFactory::class);
$key = $keyFactory->deriveSharedKeyFromEncryptionKey('my-context');
$cipherValue = $cipherService->encrypt('sensitive data', $key);
$decrypted = $cipherService->decrypt($cipherValue, $key);
```
