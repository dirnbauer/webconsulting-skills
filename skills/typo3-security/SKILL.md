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
        
        // Session security (example hardening values — tune for proxies/load balancers)
        'lockIP' => 4,                    // Example: bind backend sessions to the full IPv4 address
        'lockIPv6' => 8,                  // Lock to IPv6 prefix
        'sessionTimeout' => 3600,         // 1 hour session timeout
        'lockSSL' => true,                // Example: require HTTPS for backend requests
        
        // Password policy (TYPO3 v14)
        'passwordHashing' => [
            'className' => \TYPO3\CMS\Core\Crypto\PasswordHashing\Argon2idPasswordHash::class,
            'options' => [],
        ],
    ],
    
    'FE' => [
        'debug' => false,
        'lockIP' => 0,                    // Common for frontend sessions; mobile users / proxies often change IPs
        'sessionTimeout' => 86400,
        // `FE.lockSSL` was removed in v12 — enforce HTTPS at the **web server / proxy** and send **HSTS** (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) for production hosts
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
        
        // Trusted hosts pattern (CRITICAL) — Core wraps the pattern in `/^...$/`; omit `^` and `$`. Avoid `.*example\\.com` (without `\\.` before `example` — matches `evil-example.com`). Note: `.*\\.example\\.com` requires a subdomain and won't match bare `example.com`.
        'trustedHostsPattern' => '(www\\.)?example\\.com',
        
        // File handling security
        'textfile_ext' => 'txt,html,htm,css,js,tmpl,ts,typoscript,xml,svg',
        'mediafile_ext' => 'gif,jpg,jpeg,png,webp,svg,pdf,mp3,mp4,webm',
        
        // Security feature toggles — names and availability differ by minor release; confirm in Core docs for your exact version
        'features' => [
            'security.backend.enforceReferrer' => true,
            // Frontend CSP toggles (names stable from v12+; confirm in reference for your minor)
            'security.frontend.enforceContentSecurityPolicy' => false,
            'security.frontend.reportContentSecurityPolicy' => false,
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

// ✅ SECURE - Explicit host list (Core adds `/^...$/` around the pattern)
'trustedHostsPattern' => '(?:example\\.com|www\\.example\\.com)',

// ✅ SECURE - Regex for subdomains (tie to your registrable domain)
'trustedHostsPattern' => '(.*\\.)?example\\.com',

// Development with DDEV
'trustedHostsPattern' => '(?:(?:.*\\.)?example\\.com|.*\\.ddev\\.site)',
```

## 3. File System Security

### `fileDenyPattern` (upload / public file access)

Keep Core’s deny list strict — extend only when you understand the risk:

```php
// Example: tighten executable uploads (adjust to your policy)
$GLOBALS['TYPO3_CONF_VARS']['BE']['fileDenyPattern'] = '\\.(php[0-9]?|phtml|phar|sh|bash|cgi|pl|py|asp|aspx|jsp)(\\..*)?$';
```

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
# Composer-based TYPO3 v14: file is in var/transient/
rm var/transient/ENABLE_INSTALL_TOOL
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
$GLOBALS['TYPO3_CONF_VARS']['BE']['passwordPolicy'] = 'default'; // policy *name* only
$GLOBALS['TYPO3_CONF_VARS']['SYS']['passwordPolicies']['default'] = [
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

Configure MFA enforcement in **`config/system/settings.php`** via [`$GLOBALS['TYPO3_CONF_VARS']['BE']['requireMfa']`](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Configuration/Typo3ConfVars/BE.html#typo3confvars-be-requiremfa): `0` disabled, `1` all users, `2` non-admins, `3` admins only, **`4` system maintainers only** — confirm exact semantics in Core docs for your minor), or per user/group with **user TSconfig** [`auth.mfa.required`](https://docs.typo3.org/m/typo3/reference-typoscript/main/en-us/UserTsconfig/Auth.html):

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

Enable CSP through `config/system/settings.php` / Install Tool. Frontend toggles (names may evolve — verify in Core for your minor) commonly include:
`$GLOBALS['TYPO3_CONF_VARS']['SYS']['features']['security.frontend.enforceContentSecurityPolicy']` and `security.frontend.reportContentSecurityPolicy`. **Backend CSP is enforced by default since v13** — there is no equivalent FE-style toggle for BE.

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

## Appendix

For TYPO3 v14-specific hardening notes and related-skill links, see [references/v14-notes.md](references/v14-notes.md). For go-live checklists, rate limiting, and remaining v14 security notes, see [references/checklists.md](references/checklists.md).

---

## Credits & Attribution


Source: https://github.com/dirnbauer/webconsulting-skills
Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.
