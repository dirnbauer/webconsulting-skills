---
id: site-config-typed-settings
title: "Define environment settings via typed Site Settings, not untyped constants"
category: site-config
severity: warning
appliesTo: ["**/Configuration/Sets/**/settings.definitions.yaml", "**/Configuration/Sets/**/settings.yaml", "**/Configuration/Sets/**/config.yaml"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when introducing a configurable, environment-specific value for an extension."
---
# Define environment settings via typed Site Settings, not untyped constants

Ship configurable values as a **Site Set** with a typed `settings.definitions.yaml`
(name, default, `type`, `category`) and read them from the site's settings, rather than
as untyped TypoScript constants. Typed definitions give validation, a backend editor, and
per-site overrides via `settings.yaml`.

**Do:** declare each setting in `Configuration/Sets/<Set>/settings.definitions.yaml` with an explicit `type`.
**Don't:** introduce environment values only as TypoScript constants with no type or category.

```yaml
# Configuration/Sets/Main/config.yaml
name: webcon/example
label: 'Webcon Example'

# Configuration/Sets/Main/settings.definitions.yaml
categories:
  webconExample:
    label: 'Webcon Example'
settings:
  webconExample.api.baseUrl:
    label: 'API base URL'
    type: string
    default: 'https://api.example.org'
    category: webconExample
  webconExample.api.timeout:
    type: int
    default: 30
    category: webconExample
```

Values can be overridden per site in `config/sites/<site>/settings.yaml` and read via
`Site::getSettings()->get('webconExample.api.baseUrl')`.

> Why: Site Sets + `settings.definitions.yaml` provide typed, categorized, editable
> settings (#103437); available types include string, int, bool, number, color, page,
> url, stringlist, text (verified in `Core/Classes/Settings/Type/`).
