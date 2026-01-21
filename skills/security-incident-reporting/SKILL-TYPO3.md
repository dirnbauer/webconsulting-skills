---
name: security-incident-reporting-typo3
description: TYPO3-specific incident reporting. Forensic checklist, vulnerability classification, and Security Team communication with PGP templates.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - security-incident-reporting
  - typo3-security
triggers:
  - typo3 incident
  - typo3 security report
  - typo3 hack
  - typo3 vulnerability report
  - typo3 forensics
  - security@typo3.org
---

# TYPO3 Security Incident Reporting

> **Compatibility:** TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [security-incident-reporting](./SKILL.md) - General incident reporting framework
> - [typo3-security](../typo3-security/SKILL.md) - TYPO3 hardening

---

## 1. TYPO3 System Inventory

Before analyzing an incident, document the exact system state.

### System Inventory Template

```markdown
## TYPO3 System Inventory

### Core Information
| Field | Value |
|-------|-------|
| TYPO3 Version | 13.4.2 LTS |
| Release Type | LTS / Sprint / ELTS |
| Installation Method | Composer / Legacy |
| PHP Version | 8.3.12 |
| Database | MySQL 8.0 / MariaDB 10.11 / PostgreSQL 15 |

### PHP Configuration
| Setting | Value |
|---------|-------|
| memory_limit | 512M |
| max_execution_time | 240 |
| disable_functions | exec, shell_exec, system, passthru |
| allow_url_fopen | Off |
| allow_url_include | Off |

### Extensions
| Extension | Version | Source | Status |
|-----------|---------|--------|--------|
| news | 11.4.0 | TER/Packagist | Active |
| solr | 12.0.0 | Packagist | Active |
| custom_ext | 1.2.3 | Private | Active |
| [abandoned_ext] | 2.0.0 | TER | ⚠️ Abandoned |

### Security-Relevant Configuration
| Setting | Value | Expected |
|---------|-------|----------|
| BE/debug | false | false |
| SYS/displayErrors | 0 | 0 |
| SYS/trustedHostsPattern | configured | configured |
| SYS/features/security.* | enabled | enabled |
```

---

## 2. TYPO3 Vulnerability Classification

### Common Vulnerability Types

| Type | Severity | Description | Detection |
|------|----------|-------------|-----------|
| Insecure Deserialization | Critical | RCE via phar://, cookies, or session data | Monitor file operations, unusual processes |
| SQL Injection | Critical | Missing `createNamedParameter()` in QueryBuilder | DB error logs, unusual queries |
| Cross-Site Scripting (XSS) | High | `f:format.raw` on user input in Fluid | Stored payloads in content, reflected in URL |
| Broken Access Control | High | IDOR, missing permission checks | Unauthorized data access in logs |
| Information Disclosure | Medium | Debug output, exposed backups, credentials | Public file access, error messages |
| CSRF | Medium | Missing form tokens | Unauthorized state changes |

### TYPO3-Specific Attack Vectors

```markdown
## Insecure Deserialization
- Location: Cookies, session data, mailer file spool
- Example CVE: TYPO3-CORE-SA-2026-004 (Mailer File Spool)
- Detection: Monitor `unserialize()` calls, phar:// wrappers
- Prevention: Use JSON, validate serialized data sources

## XSS in Fluid Templates
- Location: f:format.raw on user input, custom ViewHelpers
- Detection: Search for `f:format.raw` usage on dynamic content
- Prevention: Default escaping, f:format.htmlspecialchars

## SQL Injection in Extensions
- Location: Custom QueryBuilder usage, direct SQL
- Detection: DB error logs showing SQL syntax errors
- Prevention: Always use createNamedParameter()
```

---

## 3. Forensic Checklist

### Phase 1: Integrity Verification

```bash
# 1. Verify TYPO3 Core Integrity (Composer Installation)
cd /var/www/html
composer install --dry-run 2>&1 | grep -i "warning\|error"

# 2. Check for modified core files
find vendor/typo3/cms-* -type f -name "*.php" -mtime -7

# 3. Verify package checksums
composer audit

# 4. Check for unexpected PHP files in public directories
find public/fileadmin public/typo3temp -name "*.php" -o -name "*.phtml"

# 5. Search for common webshell patterns
grep -r "eval\|base64_decode\|system\|exec\|shell_exec" public/fileadmin/
```

### Phase 2: Log Analysis

```markdown
## Log Sources

### TYPO3 Application Logs
| Log | Location | Content |
|-----|----------|---------|
| sys_log | Database table | Backend actions, errors |
| TYPO3 Logs | var/log/*.log | Application events |
| Deprecation | var/log/typo3_deprecations_*.log | API changes |

### Server Logs
| Log | Location | Content |
|-----|----------|---------|
| Apache Access | /var/log/apache2/access.log | HTTP requests |
| Apache Error | /var/log/apache2/error.log | PHP errors |
| Nginx Access | /var/log/nginx/access.log | HTTP requests |
| PHP-FPM | /var/log/php-fpm/*.log | PHP process errors |

### Analysis Queries

```sql
-- Suspicious backend logins
SELECT * FROM sys_log 
WHERE type = 255 
AND action = 1 
AND tstamp > UNIX_TIMESTAMP(NOW() - INTERVAL 7 DAY)
ORDER BY tstamp DESC;

-- Failed login attempts
SELECT * FROM sys_log 
WHERE type = 255 
AND action = 3 
AND tstamp > UNIX_TIMESTAMP(NOW() - INTERVAL 24 HOUR)
ORDER BY tstamp DESC;

-- Recent backend user changes
SELECT * FROM be_users 
WHERE tstamp > UNIX_TIMESTAMP(NOW() - INTERVAL 7 DAY)
OR crdate > UNIX_TIMESTAMP(NOW() - INTERVAL 7 DAY);
```
```

### Phase 3: File System Analysis

```bash
# Recently modified PHP files
find /var/www/html -name "*.php" -mtime -7 -ls

# Files with suspicious permissions
find /var/www/html -type f -perm /u+x -name "*.php"

# Hidden files and directories
find /var/www/html -name ".*" -type f

# Large files in upload directories (potential dumps)
find public/fileadmin -size +10M -type f

# Check cron jobs
crontab -l
cat /etc/cron.d/*
ls -la /var/spool/cron/
```

### Phase 4: Database Analysis

```sql
-- Check for new admin users
SELECT uid, username, admin, disable, crdate, tstamp 
FROM be_users 
WHERE admin = 1;

-- Check for suspicious content (webshells in bodytext)
SELECT uid, pid, header, bodytext 
FROM tt_content 
WHERE bodytext LIKE '%<?php%' 
   OR bodytext LIKE '%eval(%' 
   OR bodytext LIKE '%base64_decode%';

-- Check fe_users for mass creation
SELECT DATE(FROM_UNIXTIME(crdate)) as date, COUNT(*) as count 
FROM fe_users 
GROUP BY DATE(FROM_UNIXTIME(crdate)) 
ORDER BY date DESC 
LIMIT 30;

-- Verify file references
SELECT * FROM sys_file 
WHERE name LIKE '%.php%' 
   OR name LIKE '%.phtml%';
```

---

## 4. TYPO3 Security Team Communication

### Policy of Least Disclosure

> **CRITICAL**: Never discuss vulnerabilities publicly before the official advisory is released.
> - No posts in Slack, StackOverflow, or forums
> - Use PGP-encrypted email only
> - Respect the embargo period

### PGP Key Information

| Field | Value |
|-------|-------|
| **Key ID** | C05FBE60 |
| **Fingerprint** | B41C C3EF 373E 0F5C 7018 7FE9 3BEF BD27 C05F BE60 |
| **Download** | https://typo3.org/security |
| **Keyserver** | keys.openpgp.org |

### Import PGP Key

```bash
# From keyserver
gpg --keyserver keys.openpgp.org --recv-keys C05FBE60

# Verify fingerprint
gpg --fingerprint C05FBE60
# Should show: B41C C3EF 373E 0F5C 7018 7FE9 3BEF BD27 C05F BE60
```

---

## 5. Vulnerability Report Template

### E-Mail Template for security@typo3.org

```
Subject: Suspected Vulnerability in [EXTENSION_NAME] - [VULNERABILITY_TYPE]
To: security@typo3.org
Encryption: PGP (Key ID: C05FBE60)

-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

Dear TYPO3 Security Team,

I am writing to report a suspected security vulnerability in [COMPONENT].
In accordance with your coordinated disclosure policy, I am sharing this
information confidentially.

## 1. VULNERABILITY METADATA

| Field | Value |
|-------|-------|
| Project | [TYPO3 Core / Extension Name] |
| Affected Versions | [e.g., 11.5.0 - 11.5.24, 12.0.0 - 12.4.8] |
| Tested Version | [e.g., 12.4.8] |
| Vulnerability Type | [e.g., SQL Injection, XSS, Deserialization] |
| Severity Estimation | [e.g., High (CVSS 7.5)] |

## 2. DESCRIPTION

[Detailed description of the vulnerability. How does it work?
What is the root cause?]

Example: "The 'search' parameter in the Pi1 Controller is passed
directly to the QueryBuilder without sanitization or using
createNamedParameter(), allowing SQL injection."

## 3. PROOF OF CONCEPT (PoC)

Step-by-step instructions to reproduce:

1. Install Extension X via Composer
2. Create a page with the plugin
3. Send the following HTTP request:

```
GET /index.php?id=1&tx_ext_pi1[search]=' OR 1=1-- HTTP/1.1
Host: example.com
```

4. Observed Result: [Database error / data leakage]
5. Expected Result: [Input should be sanitized]

## 4. IMPACT

[What can an attacker achieve?]

Example: "An unauthenticated attacker can read the entire 'fe_users'
table, including password hashes and personal data, leading to
data breach and potential account takeover."

## 5. PROPOSED FIX (Optional)

[If you have a patch, describe it or attach a diff]

```php
// Before (vulnerable)
$query->where('title LIKE "' . $searchTerm . '"');

// After (fixed)
$query->where(
    $queryBuilder->expr()->like(
        'title',
        $queryBuilder->createNamedParameter('%' . $searchTerm . '%')
    )
);
```

## 6. REPORTER DETAILS

| Field | Value |
|-------|-------|
| Name | [Your Name] |
| Organization | [Your Company] |
| Email | [your.email@example.com] |
| PGP Key ID | [Your Key ID] |
| Credit Preference | [Named / Anonymous] |

I will adhere to the embargo until an official advisory is released.

Best regards,
[Your Name]

-----BEGIN PGP SIGNATURE-----
[Your PGP Signature]
-----END PGP SIGNATURE-----
```

---

## 6. Disclosure Process

### Timeline After Reporting

| Phase | Timeframe | Action |
|-------|-----------|--------|
| Acknowledgment | 48 hours | Security Team confirms receipt |
| Evaluation | 1-2 weeks | Team verifies and assesses severity |
| Coordination | Variable | Extension author contacted if needed |
| Fix Development | Variable | Patch developed and tested |
| Advisory Release | Coordinated | TYPO3-CORE-SA-YYYY-NNN published |
| Credits | With Advisory | Reporter acknowledged (if desired) |

### Embargo Rules

- **DO NOT** discuss the vulnerability publicly
- **DO NOT** share PoC code outside the report
- **DO NOT** exploit the vulnerability beyond PoC
- **DO** respond to Security Team questions promptly
- **DO** test patches if requested

### Core vs. Extension Responsibility

| Issue Type | Responsible Party | Report To |
|------------|-------------------|-----------|
| TYPO3 Core | TYPO3 Security Team | security@typo3.org |
| Official Extension (TER) | TYPO3 Security Team | security@typo3.org |
| Third-Party Extension | Extension Author | Author's security contact |
| Custom Extension | Your Organization | Internal security team |

---

## 7. TYPO3 Security Advisory Format

### Understanding Advisory IDs

```
TYPO3-CORE-SA-2026-004
       │    │   │   │
       │    │   │   └── Sequential number
       │    │   └────── Year
       │    └────────── Security Advisory
       └─────────────── Affected component (CORE / EXT)
```

### Advisory Sections

| Section | Content |
|---------|---------|
| Component | Affected TYPO3 component or extension |
| Affected Versions | Version range with vulnerability |
| Severity | Critical / High / Medium / Low |
| Suggested CVSS | CVSS v3.1 vector and score |
| Problem Description | Technical explanation |
| Solution | Update instructions |
| Credits | Reporters and contributors |

---

## 8. Incident Response Checklist (TYPO3)

### Immediate Actions (0-4 hours)

- [ ] Isolate affected TYPO3 instance
- [ ] Preserve logs (access, error, sys_log)
- [ ] Create database backup for forensics
- [ ] Document system state (inventory template)
- [ ] Check for known CVEs in installed versions

### Investigation (4-24 hours)

- [ ] Run integrity verification (Phase 1)
- [ ] Analyze logs for indicators (Phase 2)
- [ ] Check filesystem for modifications (Phase 3)
- [ ] Analyze database for anomalies (Phase 4)
- [ ] Identify attack vector and timeline

### Remediation (24-72 hours)

- [ ] Update TYPO3 Core to latest version
- [ ] Update all extensions
- [ ] Remove abandoned extensions
- [ ] Reset all backend user passwords
- [ ] Review and rotate API keys
- [ ] Verify file permissions
- [ ] Clear all caches

### Post-Incident

- [ ] Complete incident report ([SKILL.md](./SKILL.md) template)
- [ ] Report vulnerability to TYPO3 Security Team if new
- [ ] Schedule post-mortem meeting
- [ ] Implement lessons learned
- [ ] Update security monitoring

---

## 9. Resources

### TYPO3 Security

- **Security Team**: https://typo3.org/community/teams/security
- **Security Bulletins**: https://typo3.org/security/advisory
- **Security Guide**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/
- **Report Issues**: security@typo3.org (PGP encrypted)

### Version Support

| Version | Support Status | Security Updates |
|---------|----------------|------------------|
| 13.4 LTS | Active | Until Oct 2026 |
| 12.4 LTS | Active | Until Apr 2026 |
| 11.5 ELTS | Extended | Paid support only |
| < 11.5 | End of Life | No updates |

---

## Credits & Attribution

This skill is based on the "Handbuch für Advanced Security Incident Reporting" methodology
and TYPO3 Security Team guidelines.

Developed by webconsulting.at for the Claude skill collection.
