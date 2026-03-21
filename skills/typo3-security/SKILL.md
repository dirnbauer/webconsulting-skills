---
name: typo3-security
description: >-
  Security hardening checklist and best practices for TYPO3 v14 installations,
  covering configuration, file permissions, and common vulnerabilities. Use when working
  with security, hardening, permissions, authentication, vulnerabilities.
compatibility: TYPO3 14.x
metadata:
  version: "2.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Security Hardening

> **Compatibility:** TYPO3 v14.x
> All security configurations in this skill work on TYPO3 v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## 1. Critical Configuration Settings

### `config/system/settings.php` (TYPO3 v14)

```php
<?php
return [
    'BE' => [
        // Disable debug in production
        'debug' => false,
        
        // Session security
        'lockIP' => 4,                    // Lock backend session to full IP
        'lockIPv6' => 8,                  // Lock to IPv6 prefix
        'sessionTimeout' => 3600,         // 1 hour session timeout
        'lockSSL' => true,                // Force HTTPS for backend
        
        // Password policy (TYPO3 v14)
        'passwordHashing' => [
            'className' => \TYPO3\CMS\Core\Crypto\PasswordHashing\Argon2idPasswordHash::class,
            'options' => [],
        ],
    ],
    
    'FE' => [
        'debug' => false,
        'lockIP' => 0,                    // Usually 0 for frontend (mobile users)
        'sessionTimeout' => 86400,
        // `FE.lockSSL` was removed in v12 — enforce HTTPS with the web server / reverse proxy
        'passwordHashing' => [
            'className' => \TYPO3\CMS\Core\Crypto\PasswordHashing\Argon2idPasswordHash::class,
            'options' => [],
        ],
    ],
    
    'SYS' => [
        // NEVER display errors in production
        'displayErrors' => 0,
        'devIPmask' => '',                // No dev IPs in production
        'errorHandlerErrors' => E_ALL & ~E_NOTICE & ~E_DEPRECATED,
        'exceptionalErrors' => E_ALL & ~E_NOTICE & ~E_WARNING & ~E_DEPRECATED,
        
        // Encryption key (generate unique per installation)
        'encryptionKey' => 'generate-unique-key-per-installation',
        
        // Trusted hosts pattern (CRITICAL)
        'trustedHostsPattern' => 'example\\.com|www\\.example\\.com',
        
        // File handling security
        'textfile_ext' => 'txt,html,htm,css,js,tmpl,ts,typoscript,xml,svg',
        'mediafile_ext' => 'gif,jpg,jpeg,png,webp,svg,pdf,mp3,mp4,webm',
        
        // Security feature toggles — names and availability differ by minor release; confirm in Core docs for your exact version
        'features' => [
            'security.backend.enforceReferrer' => true,
        ],
    ],
    
    'LOG' => [
        'writerConfiguration' => [
            \Psr\Log\LogLevel::WARNING => [
                \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
                    'logFile' => 'var/log/typo3-warning.log',
                ],
            ],
            \Psr\Log\LogLevel::ERROR => [
                \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
                    'logFile' => 'var/log/typo3-error.log',
                ],
                \TYPO3\CMS\Core\Log\Writer\SyslogWriter::class => [],
            ],
        ],
    ],
];
```

## 2. Trusted Hosts Pattern

**CRITICAL**: Always configure `trustedHostsPattern` to prevent host header injection.

```php
// ❌ DANGEROUS - Allows any host
'trustedHostsPattern' => '.*',

// ✅ SECURE - Explicit host list
'trustedHostsPattern' => 'example\\.com|www\\.example\\.com',

// ✅ SECURE - Regex for subdomains
'trustedHostsPattern' => '(.*\\.)?example\\.com',

// Development with DDEV
'trustedHostsPattern' => '(.*\\.)?example\\.com|.*\\.ddev\\.site',
```

## 3. File System Security

### Directory Permissions

```bash
# Set correct ownership (adjust www-data to your web user)
chown -R www-data:www-data /var/www/html

# Directories: 2775 (group sticky)
find /var/www/html -type d -exec chmod 2775 {} \;

# Files: 664
find /var/www/html -type f -exec chmod 664 {} \;

# Configuration files: more restrictive
chmod 660 config/system/settings.php
chmod 660 config/system/additional.php

# var directory (writable)
chmod -R 2775 var/

# public/fileadmin (writable for uploads)
chmod -R 2775 public/fileadmin/
chmod -R 2775 public/typo3temp/
```

### Critical Files to Protect

Never expose these in `public/`:

```
❌ var/log/
❌ config/
❌ .env
❌ composer.json
❌ composer.lock
❌ .git/
❌ vendor/ (should be outside public)
```

### .htaccess Security (Apache)

```apache
# public/.htaccess additions

# Block access to hidden files
<FilesMatch "^\.">
    Require all denied
</FilesMatch>

# Block access to sensitive file types
<FilesMatch "\.(sql|sqlite|bak|backup|log|sh)$">
    Require all denied
</FilesMatch>

# Block PHP execution in upload directories
<Directory "fileadmin">
    <FilesMatch "\.php$">
        Require all denied
    </FilesMatch>
</Directory>

# Security headers
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>
```

### Nginx Security

```nginx
# Block hidden files
location ~ /\. {
    deny all;
}

# Block sensitive directories
location ~ ^/(config|var|vendor)/ {
    deny all;
}

# Block PHP in upload directories
location ~ ^/fileadmin/.*\.php$ {
    deny all;
}

# Security headers
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

## 4. Install Tool Security

### Disable Install Tool

```bash
# Remove enable file after installation
rm public/typo3conf/ENABLE_INSTALL_TOOL
```

### Secure Install Tool Password

Generate strong password and store securely:

```bash
# Generate random password
openssl rand -base64 32
```

Set the hashed password via the Install Tool or an environment-specific `config/system/additional.php`; never commit a placeholder or empty string.

### IP Restriction for Install Tool

```php
// config/system/additional.php
$GLOBALS['TYPO3_CONF_VARS']['BE']['installToolPassword'] = '$argon2id$...'; // hashed
```

## 5. Backend User Security

### Strong Password Policy (TYPO3 v14)

```php
<?php
// ext_localconf.php of site extension
$GLOBALS['TYPO3_CONF_VARS']['BE']['passwordPolicy'] = 'default';
$GLOBALS['TYPO3_CONF_VARS']['BE']['passwordPolicies']['default'] = [
    'validators' => [
        \TYPO3\CMS\Core\PasswordPolicy\Validator\CorePasswordValidator::class => [
            'options' => [
                'minimumLength' => 12,
                'upperCaseCharacterRequired' => true,
                'lowerCaseCharacterRequired' => true,
                'digitCharacterRequired' => true,
                'specialCharacterRequired' => true,
            ],
        ],
        \TYPO3\CMS\Core\PasswordPolicy\Validator\NotCurrentPasswordValidator::class => [],
    ],
];
```

### Multi-Factor Authentication (TYPO3 v14)

MFA is built into TYPO3 v14. Users can configure in:
**User Settings > Account Security**

Supported providers:
- TOTP (Time-based One-Time Password)
- Recovery Codes

Configure MFA enforcement in **`config/system/settings.php`** via [`$GLOBALS['TYPO3_CONF_VARS']['BE']['requireMfa']`](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Configuration/Typo3ConfVars/BE.html#typo3confvars-be-requiremfa) (`0`–`3` per Core docs), or per user/group with **user TSconfig** [`auth.mfa.required`](https://docs.typo3.org/m/typo3/reference-typoscript/main/en-us/UserTsconfig/Auth.html):

```typoscript
# User or group TSconfig — require MFA for those accounts (overrides global when set)
auth.mfa.required = 1
```

See [Multi-factor authentication](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Authentication/MultiFactorAuthentication/Index.html).

### Backend Access Logging

```php
// Log all backend logins
$GLOBALS['TYPO3_CONF_VARS']['LOG']['TYPO3']['CMS']['Backend']['Authentication']['writerConfiguration'] = [
    \Psr\Log\LogLevel::INFO => [
        \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
            'logFile' => 'var/log/backend-auth.log',
        ],
    ],
];
```

## 6. Content Security Policy (CSP)

### Built-in CSP (TYPO3 v14)

TYPO3 v14 has built-in CSP support. Enable it:

Enable CSP through `config/system/settings.php` / Install Tool using the **feature flags documented for your TYPO3 minor** (toggle names have changed across releases — check Core docs rather than copying stale keys).

### CSP Configuration via Events (TYPO3 v14)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Directive;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Event\PolicyMutatedEvent;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\UriValue;

#[AsEventListener(identifier: 'vendor-extension/csp-modification')]
final class ContentSecurityPolicyListener
{
    public function __invoke(PolicyMutatedEvent $event): void
    {
        if (!$event->scope->type->isFrontend()) {
            return;
        }

        $policy = $event->getCurrentPolicy()
            ->extend(Directive::ScriptSrc, new UriValue('https://cdn.example.com'))
            ->extend(Directive::StyleSrc, new UriValue('https://fonts.googleapis.com'));

        $event->setCurrentPolicy($policy);
    }
}
```

### TypoScript CSP Headers (Alternative)

```typoscript
config.additionalHeaders {
    10.header = Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; frame-ancestors 'self';
}
```

## 7. SQL Injection Prevention

### ALWAYS Use QueryBuilder

```php
<?php
declare(strict_types=1);

// ❌ VULNERABLE - Never do this
$result = $connection->executeQuery(
    "SELECT * FROM pages WHERE uid = " . $_GET['id']
);

// ✅ SECURE - Use QueryBuilder with prepared statements
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('pages');
$result = $queryBuilder
    ->select('*')
    ->from('pages')
    ->where(
        $queryBuilder->expr()->eq(
            'uid',
            $queryBuilder->createNamedParameter($id, \TYPO3\CMS\Core\Database\Connection::PARAM_INT)
        )
    )
    ->executeQuery();
```

### Extbase Repository Safety

```php
<?php
declare(strict_types=1);

// Extbase automatically escapes parameters
$query = $this->createQuery();
$query->matching(
    $query->equals('uid', $id)  // Safe - auto-escaped
);
```

## 8. XSS Prevention

### Fluid Templates

```html
<!-- ✅ SAFE - Auto-escaped -->
{variable}

<!-- ❌ DANGEROUS - Raw output -->
{variable -> f:format.raw()}

<!-- ✅ SAFE - Explicit escaping -->
{variable -> f:format.htmlspecialchars()}

<!-- For HTML content, use with caution -->
<f:format.html>{bodytext}</f:format.html>
```

### Backend Forms

TCA automatically handles escaping. For custom fields:

```php
'config' => [
    'type' => 'input',
    'max' => 255,
    // Input is automatically escaped
],
```

## 9. CSRF Protection

### Backend Requests (TYPO3 v14)

TYPO3 backend automatically includes CSRF tokens. For custom AJAX:

```php
<?php
declare(strict_types=1);

use TYPO3\CMS\Core\FormProtection\FormProtectionFactory;

final class MyController
{
    public function __construct(
        private readonly FormProtectionFactory $formProtectionFactory,
    ) {}

    public function generateToken(): string
    {
        $formProtection = $this->formProtectionFactory->createFromRequest($this->request);
        return $formProtection->generateToken('myFormIdentifier');
    }

    public function validateToken(string $token): bool
    {
        $formProtection = $this->formProtectionFactory->createFromRequest($this->request);
        return $formProtection->validateToken($token, 'myFormIdentifier');
    }
}
```

### Frontend Forms (Extbase)

```html
<!-- Extbase forms: use <f:form> so the framework injects CSRF / form protection as configured -->
<f:form action="submit" controller="Contact" method="post">
    <!-- `__trustedProperties` is for Extbase property-mapping allow-lists, not a substitute for CSRF -->
    <f:form.hidden name="__trustedProperties" value="{trustedProperties}" />
</f:form>
```

## 10. Rate Limiting (TYPO3 v14)

TYPO3 v14 includes built-in rate limiting:

```php
// config/system/additional.php
// Rate limiting: check current Core / feature documentation — do not assume a stable `security.backend.rateLimiter` toggle name

// Configure rate limits
$GLOBALS['TYPO3_CONF_VARS']['BE']['loginRateLimit'] = 5;  // attempts per minute
```

## 11. Security Audit Checklist

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

## 12. Security Resources

- **TYPO3 Security**: https://typo3.org/security (advisories, team contact, coordinated releases)
- **Security Guide**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/Index.html
- **v14 changelog index**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html

## v14-Only Security Changes

> The following security changes apply **exclusively to TYPO3 v14**.

### Stronger HMAC Algorithm **[v14 only]**

TYPO3 v14 uses a **stronger cryptographic algorithm for HMAC** (#106307). Existing HMAC tokens (e.g., in URLs, form tokens) generated with the old algorithm will be invalid after upgrade. Plan for token regeneration.

### Built-in CipherService **[v14 only]**

New `CipherService` (#108002) provides **symmetric encryption/decryption** out of the box. Use it instead of custom encryption implementations:

```php
use TYPO3\CMS\Core\Crypto\Cipher\CipherService;
use TYPO3\CMS\Core\Crypto\Cipher\SharedKey;

$cipherService = GeneralUtility::makeInstance(CipherService::class);
// SharedKey must be 32 bytes; use a secrets manager in real projects — this is illustrative only.
$key = new SharedKey(hash('sha256', $GLOBALS['TYPO3_CONF_VARS']['SYS']['encryptionKey'], true));
$cipherValue = $cipherService->encrypt('sensitive data', $key);
$decrypted = $cipherService->decrypt($cipherValue, $key);
```

### MFA Failed Verification Notifications **[v14 only]**

Backend users are now **notified on failed MFA verification attempts** (#105783). This provides early warning of potential brute-force attacks against MFA-protected accounts.

### Install Tool Password via CLI **[v14 only]**

New CLI command `install:password:set` (#104058) allows setting the Install Tool password without web access. Useful for automated deployments:

```bash
vendor/bin/typo3 install:password:set
```

### Redis-Based Install Tool Sessions **[v14 only]**

Install Tool sessions can now be stored in **Redis** (#101059) instead of the filesystem. This enables Install Tool access in multi-server / shared-nothing deployments without shared filesystems.

### Modal Migration **[v14 only]**

Backend modals migrated from **Bootstrap Modal to native `<dialog>`** element (#107443). Custom backend JavaScript using Bootstrap Modal API must be updated.

---

## Related Skills

- [security-incident-reporting/TYPO3](../security-incident-reporting/SKILL-TYPO3.md) - TYPO3 forensics, vulnerability classification, Security Team communication with PGP templates
- [security-audit](../security-audit/SKILL.md) - General security audit patterns, OWASP, CVSS scoring

---

## Credits & Attribution

Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.
