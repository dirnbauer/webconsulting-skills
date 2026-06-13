---
id: di-private-autoconfigured-services
title: "Keep services private, autowired and autoconfigured"
category: di
severity: warning
appliesTo: ["**/Configuration/Services.yaml", "**/Configuration/Services.php"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when authoring or editing an extension's Services.yaml."
---
# Keep services private, autowired and autoconfigured

Declare the standard `_defaults` block (`autowire`, `autoconfigure`, `public: false`)
and register your `Classes/` namespace by resource. Only mark a service `public: true`
or tag it explicitly when the framework fetches it from the container by class name
(e.g. command controllers, some event listeners that aren't autoconfigured).

**Do:** rely on `_defaults` + a `resource` glob; keep everything private and autowired.
**Don't:** make services public "just in case", or hand-tag what autoconfiguration already handles.

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Webcon\WebconExample\:
    resource: '../Classes/*'

  # Make public only when something is pulled from the container by name:
  Webcon\WebconExample\Command\ImportCommand:
    public: true
```

> Why: matches core extensions' `Configuration/Services.yaml` `_defaults` convention;
> private autowired services are the v14 default and keep the container lean.
