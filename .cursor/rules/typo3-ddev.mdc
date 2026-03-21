---
name: typo3-ddev
description: >-
  Best practices for TYPO3 local development with DDEV, including configuration, database
  management, multi-version testing, and common workflows for TYPO3 v14. Use when working
  with ddev, local, development, docker, environment, multi-version.
compatibility: TYPO3 14.x
metadata:
  version: "2.1.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 DDEV Local Development

> **Compatibility:** TYPO3 v14.x
> All configurations in this skill support TYPO3 v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## Container Priority

**Always check for existing containers first:**

1. Check `.ddev/` exists → use `ddev exec`
2. Check `docker-compose.yml` exists → use `docker compose exec`
3. Only use system tools if no container environment

> **Critical**: Use the project's configured PHP version, not system PHP.

## 1. Project Initialization

### New TYPO3 Project (v14 - Preferred)

```bash
# Create project directory
mkdir my-typo3-project && cd my-typo3-project

# Initialize DDEV with TYPO3 preset
ddev config --project-type=typo3 --docroot=public --php-version=8.3

# Start the environment
ddev start

# Install TYPO3 v14 (preferred)
ddev composer create "typo3/cms-base-distribution:^14"

# Run TYPO3 setup
ddev typo3 setup
```

### Existing TYPO3 Project

```bash
# Clone repository
git clone git@github.com:org/project.git
cd project

# Configure DDEV (if not already)
ddev config --project-type=typo3 --docroot=public --php-version=8.3

# Start and install dependencies
ddev start
ddev composer install

# Import database (see Database Operations)
```

## 2. Recommended Configuration

### `.ddev/config.yaml` (TYPO3 v14)

```yaml
name: my-typo3-project
type: typo3
docroot: public
php_version: "8.3"    # 8.2 minimum for TYPO3 v14; 8.3/8.4 common locally
webserver_type: nginx-fpm
database: mariadb:10.11    # 10.11+ or 11.x recommended for TYPO3 v14

# Fixed port for external tools (MySQL MCP, etc.)
host_db_port: "33060"
host_webserver_port: "8080"
host_https_port: "8443"

# Enable Mailpit for email testing (replaced Mailhog in newer DDEV)
# mailpit_http_port defaults to 8025; omit unless you need a non-default port

# PHP settings
web_environment:
  - TYPO3_CONTEXT=Development
  - PHP_IDE_CONFIG=serverName=my-typo3-project.ddev.site

# Additional services
hooks:
  post-start:
    - exec: composer install --no-interaction
```

### `.ddev/config.local.yaml` (Personal Overrides)

```yaml
# Personal machine-specific overrides (gitignored)
host_db_port: "33061"  # If 33060 conflicts
```

### PHP version matrix (TYPO3 v14)

| TYPO3 Version | Minimum PHP | Recommended PHP | MariaDB |
|---------------|-------------|-----------------|---------|
| v14.x         | 8.2         | 8.3 / 8.4       | 10.11+  |

## 3. Database Operations

### Import Database

```bash
# From SQL file
ddev import-db --file=dump.sql

# From gzipped file
ddev import-db --file=dump.sql.gz

# From remote (via SSH)
ssh user@server "mysqldump -u root dbname | gzip" | gunzip | ddev import-db
```

### Export Database

```bash
# Standard export
ddev export-db --file=/tmp/backup.sql.gz

# Without gzip
ddev export-db --gzip=false --file=/tmp/backup.sql
```

If you prefer relative paths, note that DDEV resolves them from the project root. Absolute paths are the documented convention.

### Database Snapshots

```bash
# Create snapshot before risky operation
ddev snapshot --name=before-upgrade

# List snapshots
ddev snapshot --list

# Restore snapshot
ddev snapshot restore before-upgrade

# Remove old snapshots (interactive cleanup; there is no `snapshot delete` subcommand)
ddev snapshot --cleanup
```

### Direct MySQL Access

```bash
# MySQL CLI
ddev mysql

# Execute query
ddev mysql -e "SELECT uid, title FROM pages WHERE hidden = 0"

# Connect from external tool (e.g., TablePlus, DBeaver)
# Host: 127.0.0.1
# Port: 33060 (or your configured host_db_port)
# User: db
# Password: db
# Database: db
```

## 4. TYPO3 CLI Commands

### Console Commands

```bash
# List all commands
ddev typo3 list

# Clear all caches
ddev typo3 cache:flush

# Clear specific cache
ddev typo3 cache:flush --group=pages

# Database schema: use Backend → Admin Tools → Maintenance → Analyze Database Structure,
# or run extension setup (applies pending schema for extensions). The `database:updateschema`
# command exists only when `helhum/typo3-console` is installed.

# Reference index
ddev typo3 referenceindex:update

# Scheduled tasks
ddev typo3 scheduler:run

# Run upgrade wizards (after version update)
ddev typo3 upgrade:list
ddev typo3 upgrade:run
```

### Extension Management

```bash
# System extension (Composer metapackage, ships with TYPO3 distribution)
ddev composer require typo3/cms-seo

# Install extension from Packagist
ddev composer require vendor/extension-name

# Setup extensions (generate PackageStates.php)
ddev typo3 extension:setup

# Run setup / migrations for one extension (`extension:setup` is the usual Composer-mode workflow;
# `extension:activate` exists in Core but is often disabled in Composer installations — see Core docs)
ddev typo3 extension:setup -e my_extension

# Remove a Composer-managed extension: `ddev composer remove vendor/package` then clear caches
```

## 5. Composer Operations

```bash
# Install dependencies
ddev composer install

# Update all dependencies
ddev composer update

# Update single package
ddev composer update typo3/cms-core --with-dependencies

# Require new package (match constraints to TYPO3 v14 + your PHP version)
ddev composer require "vendor/package:^1.0"

# Remove package
ddev composer remove vendor/package

# Clear Composer cache
ddev composer clear-cache
```

### Dual-Version Development

For extensions supporting TYPO3 v14:

```bash
# Set version constraint in extension's composer.json
ddev composer require "typo3/cms-core:^14.0" --no-update
```

## 6. File Operations

### SSH into Container

```bash
# Web container (as www-data)
ddev ssh

# Web container (as root)
ddev ssh -s web -u root

# Database container
ddev ssh -s db
```

### File Sync

```bash
# Copy file into container
ddev exec cp /path/in/container /other/path

# Copy from host to container
docker cp localfile.txt ddev-myproject-web:/var/www/html/

# Download file from container
ddev exec cat /var/www/html/somefile > localfile
```

## 7. Debugging with Xdebug

### Enable/Disable

```bash
# Enable Xdebug
ddev xdebug on

# Disable Xdebug (faster performance)
ddev xdebug off

# Check status
ddev xdebug status
```

### IDE Configuration (PhpStorm/Cursor)

1. Set breakpoint in PHP file
2. Start listening for connections (PhpStorm: "Start Listening")
3. Enable Xdebug: `ddev xdebug on`
4. Trigger request in browser
5. Debugger should connect

### Xdebug Environment

Avoid setting `XDEBUG_MODE`, `XDEBUG_CONFIG`, or hardcoded `client_host` values in `.ddev/config.yaml` for normal projects. DDEV manages these automatically via `ddev xdebug on`, `ddev xdebug off`, and `ddev xdebug toggle`, including the correct host value per platform.

## 8. Multi-Site Configuration

### Additional Hostnames

```yaml
# .ddev/config.yaml
additional_hostnames:
  - site1
  - site2
additional_fqdns:
  - site1.myproject.ddev.site
  - site2.myproject.ddev.site
```

### Site Configuration

```bash
# Create site configuration
mkdir -p config/sites/site1
```

```yaml
# config/sites/site1/config.yaml
base: 'https://site1.myproject.ddev.site/'
rootPageId: 1
languages:
  - title: English
    languageId: 0
    locale: en_US.UTF-8
```

## 9. Services and Add-ons

### Common Add-ons

```bash
# Redis (for caching)
ddev add-on get ddev/ddev-redis

# Elasticsearch
ddev add-on get ddev/ddev-elasticsearch

# Solr
ddev add-on get ddev/ddev-solr
```

### Custom Services

```yaml
# .ddev/docker-compose.redis.yaml
# Attach the service to the DDEV project network so the `web` container can reach hostname `redis`.
services:
  redis:
    image: redis:7-alpine
    container_name: ddev-${DDEV_SITENAME}-redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    labels:
      com.ddev.site-name: ${DDEV_SITENAME}
      com.ddev.approot: $DDEV_APPROOT
    networks: [default]

volumes:
  redis-data:

networks:
  default:
    name: ddev-${DDEV_SITENAME}_default
    external: true
```

### Redis Caching Configuration (TYPO3 v14)

```php
<?php
// config/system/additional.php
$GLOBALS['TYPO3_CONF_VARS']['SYS']['caching']['cacheConfigurations']['hash']['backend'] 
    = \TYPO3\CMS\Core\Cache\Backend\RedisBackend::class;
$GLOBALS['TYPO3_CONF_VARS']['SYS']['caching']['cacheConfigurations']['hash']['options'] = [
    'hostname' => 'redis',
    'port' => 6379,
    'database' => 0,
];
```

## 10. Troubleshooting

### Common Issues

```bash
# Restart everything
ddev restart

# Full reset (keeps database)
ddev stop && ddev start

# Nuclear option (removes containers **and database volume**)
ddev delete -O && ddev start

# View logs
ddev logs

# View specific service logs
ddev logs -s web
ddev logs -s db
```

### Port Conflicts

```bash
# Check what's using a port
lsof -i :80
```

`router_http_port` and `router_https_port` may be set **globally** in `~/.ddev/global_config.yaml` **or per project** in `.ddev/config.yaml` (DDEV documents both scopes). Global values affect all projects unless overridden locally.

### Permission Issues

```bash
# Fix file permissions
ddev exec chmod -R g+w var/
ddev exec chmod -R g+w public/fileadmin/
ddev exec chmod -R g+w public/typo3temp/
```

## 11. Environment Variables

### TYPO3 Context

```bash
# Development (default in DDEV)
TYPO3_CONTEXT=Development

# Production testing
TYPO3_CONTEXT=Production

# Sub-contexts
TYPO3_CONTEXT=Development/Docker
```

### Custom Variables

```yaml
# .ddev/config.yaml
web_environment:
  - MY_API_KEY=secret123
  - FEATURE_FLAG=enabled
```

Access in TYPO3:

```php
<?php
$apiKey = getenv('MY_API_KEY');
// or
$apiKey = $_ENV['MY_API_KEY'];
```

## 12. Best Practices

### Performance

1. **Disable Xdebug** when not debugging (`ddev xdebug off`)
2. **Use snapshots** instead of full imports for quick state changes
3. **Mount with Mutagen** on macOS for better file sync performance
4. **Use PHP 8.3 or 8.4** for best performance on TYPO3 v14

### Team Workflow

1. **Commit** `.ddev/config.yaml` to repository
2. **Gitignore** `.ddev/config.local.yaml` for personal overrides
3. **Document** additional setup steps in `README.md`
4. **Share** database snapshots for consistent development data

### Security

1. **Never expose** DDEV ports publicly
2. **Don't use** DDEV in production
3. **Rotate** any sensitive data in development databases

## 13. Extension development against TYPO3 v14

Use **one TYPO3 v14 instance** per DDEV project. For CI, matrix-test **PHP 8.2 / 8.3 / 8.4** against the same Core constraint (`typo3/cms-core:^14.0`) instead of running multiple Core versions locally.

```bash
# From project root (Composer-mode site with your extension)
ddev exec vendor/bin/phpunit
ddev typo3 cache:flush
```

**Admin user:** Created during `typo3 setup` or the install wizard; use the password you set.

## v14-Only DDEV Changes

> The following DDEV-related changes are relevant when setting up **TYPO3 v14 environments**.

### PHP 8.5 Compatibility **[v14.1+ only]**

TYPO3 v14.1 adds **PHP 8.5 compatibility**. When PHP 8.5 is released, update your DDEV config:
```yaml
# .ddev/config.yaml
php_version: "8.5"
```

### Camino Default Theme **[v14.1+ only]**

TYPO3 v14.1 ships with the **Camino** default frontend theme. For quick-start setups:
```bash
ddev composer require typo3/theme-camino
ddev typo3 extension:setup -e theme_camino
```

### composer.json Required in Classic Mode **[v14 only]**

In v14, extensions **must** have a `composer.json` file even in classic (non-Composer) mode. Ensure all local extensions include a valid `composer.json`.

### Frontend Asset Pipeline **[v14 only]**

Frontend CSS/JS concatenation and compression are removed from TYPO3 Core. Configure your DDEV web server or add a build step:
```yaml
# .ddev/nginx-site.conf or custom config
# Enable gzip compression at the web server level
```

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-ddev-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
