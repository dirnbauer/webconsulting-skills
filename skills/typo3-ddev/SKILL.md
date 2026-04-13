---
name: typo3-ddev
description: "Use when setting up DDEV for TYPO3 extension development, testing across multiple TYPO3 versions (11.5/12.4/13.4/14.0), configuring local dev environments, or multi-version testing. Also triggers on: ddev start, ddev config, local development, docker environment, PHP version management."
---

# TYPO3 DDEV Setup Skill

DDEV automation for TYPO3 extension development with multi-version testing.

## Container Priority

1. `.ddev/` exists -> `ddev exec`
2. `docker-compose.yml` exists -> `docker compose exec`
3. System tools only if no container

> Always use the project's configured PHP, not system PHP.

## Quick Start

```bash
scripts/validate-prerequisites.sh    # Check Docker, DDEV prerequisites
ddev start
ddev install-all                     # All versions (11/12/13/14)
ddev install-v13                     # Single version
```

## Database Selection (Tiered)

- **SQLite**: Simple extensions, no ext_tables.sql, development only
- **MariaDB 10.11** (default): Extensions with ext_tables.sql or raw SQL
- **PostgreSQL 16**: GIS/spatial data
- **MySQL 8.0**: Corporate/Oracle parity

See `references/advanced-options.md`.

## PHP Management

Set `php_version: "8.3"` in config.yaml. Upgrade beyond DDEV's bundled version via `.ddev/web-build/Dockerfile` using `apt-get dist-upgrade`. Install extensions with `apt-get` (pecl unavailable). Custom settings: `.ddev/php/custom.ini`.

See `references/0003-php-version-management.md`.

## TYPO3 Version Differences

| | TYPO3 12 | TYPO3 13+ |
|---|---|---|
| Setup | `install:setup --use-existing-database` | `setup` |
| Password flag | `--admin-user-password` | `--admin-user-password` |
| Extension activation | Automatic (Composer) | `extension:setup` |

See `references/typo3-12-cli-changes.md`.

## Access URLs & Credentials

| Environment | URL |
|---|---|
| TYPO3 v13 Backend | `https://v13.{sitename}.ddev.site/typo3/` |
| Docs | `https://docs.{sitename}.ddev.site/` |

**Credentials**: admin / Joh316!!

## Post-Setup Verification

`ddev status`, `ddev exec -d /var/www/html/v13 vendor/bin/typo3 extension:list --active`, `ddev describe`. See `references/post-setup-verification.md`.

## Optional Services & Commands

- **Valkey 8** (default, wire-compatible with Redis) or Redis 7: `references/0001-valkey-default-with-redis-alternative.md`
- **Ofelia** scheduler (`ghcr.io/netresearch/ofelia`): TYPO3 scheduler automation
- `ddev generate-makefile` / `ddev generate-index` / `ddev docs` (renders `Documentation-GENERATED-temp/`)
- `ddev xdebug on` / Cache: `ddev exec -d /var/www/html/v13 vendor/bin/typo3 cache:flush`

## Extension Naming

Hyphens for display/composer (`nr-llm`), underscores for internal TYPO3 key (`nr_llm`). Source: composer.json `name`.

## Troubleshooting

| Issue | Solution |
|---|---|
| Port 80/443 conflict | Set `router_http_port: "8080"` / `router_https_port: "8443"` in config.yaml |
| Database exists | `ddev mysql -e "DROP DATABASE v13; CREATE DATABASE v13;"` |
| Extension not found | `ddev exec -d /var/www/html/v13 vendor/bin/typo3 cache:flush` |
| Windows: health check hangs | Add `/phpstatus` endpoint with `php-fpm.sock` to Apache config |
| Windows: CRLF errors | Convert to LF preserving UTF-8 encoding (for emoji support) |
| PCOV/pecl fails | Use `apt-get install php${PHP_VERSION}-pcov` instead |
| PHP settings ignored | Place in `.ddev/php/custom.ini`, not `/usr/local/etc/php/conf.d/` |
| Full cleanup | `ddev delete --omit-snapshot --yes` then remove Docker volumes |

## References

| Topic | File |
|---|---|
| Prerequisites | `references/prerequisites-validation.md` |
| Quick start | `references/quickstart.md` |
| Advanced options | `references/advanced-options.md` |
| Post-setup | `references/post-setup-verification.md` |
| Branding/landing page | `references/index-page-generation.md` (Netresearch: #2F99A4, Raleway) |
| Windows | `references/windows-fixes.md`, `references/windows-optimizations.md` |
| Docs rendering | `references/documentation-rendering.md` |
| PHP versions | `references/0003-php-version-management.md` |
| Troubleshooting | `references/troubleshooting.md` |

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-ddev-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
