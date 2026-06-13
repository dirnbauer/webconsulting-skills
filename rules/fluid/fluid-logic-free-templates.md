---
id: fluid-logic-free-templates
title: "Keep Fluid templates logic-free and output escaped"
category: fluid
severity: warning
appliesTo: ["**/Resources/Private/**/*.html"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when building a Fluid template, layout, or partial."
---
# Keep Fluid templates logic-free and output escaped

Templates present data; they do not compute it. Move business logic, data shaping, and
any procedural work into controllers or dedicated ViewHelpers. Never embed raw PHP, and
never disable Fluid's automatic HTML escaping unless the value is verified trusted markup.

**Do:** prepare values in the controller; use ViewHelpers for presentation; let Fluid escape by default.
**Don't:** put `{... -> f:format.raw()}` on user input, call PHP inside templates, or pile conditionals into the view.

```html
<!-- Controller assigns a ready-to-render value; template just outputs it (auto-escaped) -->
<f:for each="{articles}" as="article">
    <h2>{article.title}</h2>
    <p>{article.teaser}</p>
</f:for>

<!-- Trusted, sanitized rich text only — never on raw request input -->
<div>{article.bodytext -> f:format.html()}</div>
```

> Why: logic-free templates keep escaping intact and presentation testable; `f:format.raw`
> on untrusted data is an XSS vector. Fluid escapes output by default — keep it that way.
