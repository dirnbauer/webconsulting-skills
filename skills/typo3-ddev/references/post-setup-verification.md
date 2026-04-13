# Post-Setup Verification

After `ddev start` and installation, verify TYPO3 is fully functional:

```bash
# 1. Check DDEV status
ddev status                          # All services should be "running"

# 2. Verify backend is accessible
curl -sI https://v13.{sitename}.ddev.site/typo3/ | head -1
# Expected: HTTP/2 200 or HTTP/2 302 (redirect to login)

# 3. Verify extension is activated
ddev exec -d /var/www/html/v13 vendor/bin/typo3 extension:list --active | grep {extension_key}

# 4. Verify database is populated
ddev mysql -e "SHOW DATABASES;" | grep v13
ddev mysql v13 -e "SELECT COUNT(*) FROM be_users;"
# Expected: At least 1 backend user
```

**Quick health check (all-in-one):**
```bash
ddev describe                        # Shows URLs, ports, database info
ddev exec -d /var/www/html/v13 vendor/bin/typo3 backend:lock:status
# Expected: "Backend is not locked"
```

## Generated Files

Copy templates from `assets/templates/` to project's `.ddev/`:

```
.ddev/
├── config.yaml
├── docker-compose.web.yaml
├── apache/
│   ├── apache-site.conf     (main site - gitignored by ddev!)
│   ├── v12.conf             (committable - copy for TYPO3 v12)
│   ├── v13.conf             (committable - copy for TYPO3 v13)
│   └── docs.conf            (committable - for docs subdomain)
├── index.html.netresearch.template  (for netresearch/* packages)
├── index.html.typo3.template        (for all other packages)
└── commands/web/install-v{11,12,13,14}
```

**IMPORTANT:** `apache-site.conf` is gitignored by ddev's default `.gitignore`.
For multi-version setups, copy the separate `v{11,12,13,14}.conf` files which CAN be committed.
