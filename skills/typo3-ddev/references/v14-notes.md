# TYPO3 DDEV v14 Notes

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

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-ddev-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
