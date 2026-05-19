# 13. Workflow with DDEV

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 13. Workflow with DDEV

### Standard Development Workflow

```bash
# 1. Create new Content Block
ddev typo3 make:content-block

# 2. Clear system caches
ddev typo3 cache:flush -g system

# 3. Update database schema
ddev typo3 extension:setup --extension=my_sitepackage

# Alternative: Use Database Analyzer in TYPO3 Backend
# Admin Tools > Maintenance > Analyze Database Structure
```

### Using webprofil/make Extension

If `webprofil/make` is installed:

```bash
# Create Content Block with webprofil/make
ddev make:content_blocks

# Clear caches and update database (prefer Core CLI)
ddev typo3 cache:flush
ddev typo3 extension:setup --extension=my_sitepackage
# `database:updateschema` exists only with helhum/typo3-console — do not assume it in plain Core projects
```

### Integration with Extbase

After creating Record Types with proper table names, generate Extbase models:

```bash
# If typo3:make:model is available
ddev typo3 make:model --extension=my_sitepackage

# Generate repository
ddev typo3 make:repository --extension=my_sitepackage
```
