---
id: content-blocks-yaml-and-labels
title: "Build content elements as Content Blocks, not hand-rolled TCA/TypoScript"
category: content-blocks
severity: warning
appliesTo: ["**/ContentBlocks/**/config.yaml", "**/ContentBlocks/**/language/labels.xlf", "**/ContentBlocks/**/templates/*.fluid.html"]
typo3: ">=14.3"
php: ">=8.2"
trigger: "Use when creating a new content element or record type for editors."
---
# Build content elements as Content Blocks, not hand-rolled TCA/TypoScript

Define editor-facing content elements with `friendsoftypo3/content-blocks`: a
`config.yaml` (vendor-prefixed `name`, declared `fields`), a `language/labels.xlf`, and a
`templates/frontend.fluid.html` template. Content Blocks generates the TCA, TypoScript and
palettes for you — don't hand-register the element through raw TCA/TypoScript.

**Do:** create `ContentBlocks/ContentElements/<name>/` with `config.yaml` + `language/labels.xlf` + `templates/frontend.fluid.html`.
**Don't:** wire a new CType via `addPlugin`/TypoScript `tt_content` setup and manual TCA columns.

```yaml
# ContentBlocks/ContentElements/teaser/config.yaml
name: webcon/teaser            # vendor/identifier — never wc/*
fields:
  - identifier: headline
    type: Text
    required: true
  - identifier: bodytext
    useExistingField: true
```

```xml
<!-- ContentBlocks/ContentElements/teaser/language/labels.xlf -->
<trans-unit id="title"><source>Teaser</source></trans-unit>
<trans-unit id="headline.label"><source>Headline</source></trans-unit>
```

> Why: Content Blocks 2.x (requires cms-core `^14.3`, verified in vendor) is the
> declarative way to ship content types; `config.yaml` uses a `vendor/name` identifier
> and `language/labels.xlf` with `trans-unit` ids (verified against shipped examples).
