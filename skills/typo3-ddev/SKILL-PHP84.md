---
name: typo3-ddev-php84
description: PHP 8.4 configuration for DDEV TYPO3 development. Container setup, Xdebug 3.4, and multi-version testing.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-ddev
  - php-modernization
triggers:
  - ddev php 8.4
  - ddev php84
  - xdebug 3.4
---

# DDEV with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-ddev](./SKILL.md) - Main DDEV guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. PHP 8.4 Configuration

### .ddev/config.yaml

```yaml
name: my-typo3-project
type: typo3
docroot: public
php_version: "8.4"
webserver_type: nginx-fpm
database:
  type: mariadb
  version: "10.11"

# Recommended for PHP 8.4
composer_version: "2"
nodejs_version: "20"
```

### Update Existing Project

```bash
# Update PHP version
ddev config --php-version=8.4

# Restart to apply changes
ddev restart

# Verify PHP version
ddev exec php -v
# PHP 8.4.x (cli) ...
```

---

## 2. Xdebug 3.4 Configuration

PHP 8.4 requires Xdebug 3.4+.

### .ddev/php/xdebug.ini

```ini
[xdebug]
xdebug.mode=debug,develop
xdebug.start_with_request=trigger
xdebug.client_host=host.docker.internal
xdebug.client_port=9003
xdebug.idekey=CURSOR
xdebug.log_level=0

; PHP 8.4 specific: Better property hooks debugging
xdebug.show_local_vars=1
xdebug.var_display_max_depth=5
```

### Enable/Disable Xdebug

```bash
# Enable Xdebug
ddev xdebug on

# Disable for performance
ddev xdebug off

# Check status
ddev xdebug status
```

---

## 3. Multi-Version Testing (PHP 8.2/8.3/8.4)

### Matrix Testing Script

```bash
#!/bin/bash
# .ddev/commands/host/test-php-versions

for version in 8.2 8.3 8.4; do
    echo "=== Testing PHP $version ==="
    ddev config --php-version=$version
    ddev restart
    ddev exec vendor/bin/phpunit
done

# Reset to PHP 8.4
ddev config --php-version=8.4
ddev restart
```

### composer.json for Multi-Version

```json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.0 || ^14.0"
    },
    "config": {
        "platform": {
            "php": "8.2.0"
        }
    }
}
```

---

## 4. PHP 8.4 Extensions

### .ddev/config.yaml

```yaml
# Additional PHP extensions for 8.4
webimage_extra_packages:
  - php8.4-intl
  - php8.4-gd
  - php8.4-zip
  - php8.4-bcmath

# Custom php.ini settings
php_ini_defs:
  error_reporting: E_ALL
  display_errors: "On"
  max_execution_time: 240
  memory_limit: 512M
```

---

## 5. Troubleshooting PHP 8.4

### Extension Compatibility Check

```bash
# Check for deprecated function usage
ddev exec php -d error_reporting=E_ALL vendor/bin/phpstan analyse

# Run Rector to detect issues
ddev exec vendor/bin/rector process --dry-run
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Implicit nullable deprecation | Add `?` to nullable parameters |
| Extension not loading | Check extension PHP 8.4 compatibility |
| Xdebug not working | Update to Xdebug 3.4+ |

---

## References

- [typo3-ddev SKILL.md](./SKILL.md)
- [DDEV Documentation](https://ddev.readthedocs.io/)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
