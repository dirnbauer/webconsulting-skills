# Scripts Guide

Detailed usage for documentation extraction and analysis scripts.

## Documentation Extraction

To extract documentation data from all sources:

```bash
scripts/extract-all.sh /path/to/extension
```

To extract from specific sources:

```bash
# Extract PHP API documentation
scripts/extract-php.sh /path/to/extension

# Extract extension configuration (ext_emconf.php, ext_localconf.php)
scripts/extract-extension-config.sh /path/to/extension

# Extract Composer metadata
scripts/extract-composer.sh /path/to/extension

# Extract build configurations (CI, testing)
scripts/extract-build-configs.sh /path/to/extension

# Extract project files (README, CHANGELOG)
scripts/extract-project-files.sh /path/to/extension

# Extract repository metadata (GitHub/GitLab)
scripts/extract-repo-metadata.sh /path/to/extension
```

## Documentation Analysis

To analyze documentation coverage and identify gaps:

```bash
scripts/analyze-docs.sh /path/to/extension
```

## AI Context Setup

To add AGENTS.md template to Documentation/ folder:

```bash
scripts/add-agents-md.sh /path/to/extension
```
