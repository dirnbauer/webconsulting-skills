---
name: typo3-docs
description: >-
  Create and maintain TYPO3 extension documentation following official docs.typo3.org
  standards. RST syntax, TYPO3 directives, rendering, and deployment. Use when working
  with documentation, rst, docs, readme, typo3 documentation.
compatibility: TYPO3 14.x
metadata:
  version: "1.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Documentation Skill

Create and maintain TYPO3 extension documentation following official docs.typo3.org standards.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

> **Supplements:** [SKILL-PHP84.md](SKILL-PHP84.md) (PHP version badges, PHP 8.4 in RST) · [SKILL-CONTENT-BLOCKS.md](SKILL-CONTENT-BLOCKS.md) (Content Blocks fields with `.. confval::` and `:name:`)

## When to Use

- Creating documentation from scratch (no `Documentation/` exists)
- Editing `Documentation/**/*.rst` files
- Using TYPO3 directives: `confval`, `versionadded`, `card-grid`, `tabs`
- Creating/adding screenshots
- Rendering and testing documentation locally
- Deploying to docs.typo3.org

## Documentation Structure

```
Documentation/
├── Index.rst                 # Main entry point
├── guides.xml                # Configuration file
├── Introduction/
│   └── Index.rst
├── Installation/
│   └── Index.rst
├── Configuration/
│   └── Index.rst
├── Usage/
│   └── Index.rst
├── Developer/
│   └── Index.rst
└── Images/
    └── screenshot.png
```

## Creating Documentation from Scratch

When no `Documentation/` directory exists, use the init command:

```bash
docker run --rm --pull always -v $(pwd):/project -w /project -it \
  ghcr.io/typo3-documentation/render-guides:latest init
```

**Interactive prompts:**
1. **Format**: Choose `rst` (ReStructuredText) for full TYPO3 theme features
2. **Site Set**: Enter name/path if extension defines a Site set

## guides.xml Configuration

Official reference: [guides.xml (How to document)](https://docs.typo3.org/permalink/h2document:guides-xml). The `docker … init` command generates a file from the [render-guides template](https://github.com/TYPO3-Documentation/render-guides/blob/main/packages/typo3-guides-cli/resources/templates/guides.xml.twig); prefer that output over copying fragments by hand.

Minimal RST manual (matches TYPO3 theme expectations — adjust `interlink-shortcode` to your Composer package name):

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<guides
    xmlns="https://www.phpdoc.org/guides"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="https://www.phpdoc.org/guides vendor/phpdocumentor/guides-cli/resources/schema/guides.xsd"
    input-format="rst"
>
    <project title="My Extension" copyright="The contributors"/>
    <extension
        class="\T3Docs\Typo3DocsTheme\DependencyInjection\Typo3DocsThemeExtension"
        interlink-shortcode="vendor/my-extension"
        typo3-core-preferred="stable"
    />
    <inventory id="t3coreapi" url="https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/"/>
</guides>
```

### GitHub “edit on” and project links

TYPO3 sets these as **attributes on `<extension …/>`**, not as a generic `<settings>` block. Example:

```xml
    <extension
        class="\T3Docs\Typo3DocsTheme\DependencyInjection\Typo3DocsThemeExtension"
        edit-on-github="myorg/my-extension"
        edit-on-github-branch="main"
        interlink-shortcode="vendor/my-extension"
        project-home="https://github.com/vendor/my-extension"
        project-repository="https://github.com/vendor/my-extension"
        typo3-core-preferred="stable"
    />
```

Some image tags ship a `configure` helper for `guides.xml` — confirm with `docker run --rm ghcr.io/typo3-documentation/render-guides:latest -h` before documenting it for users. Then run `lint-guides-xml` (below) to validate against the XSD.

## RST Syntax Reference

### Headings

```rst
==========
Page Title
==========

Section
=======

Subsection
----------

Subsubsection
~~~~~~~~~~~~~
```

### Code Blocks

```rst
..  code-block:: php
    :caption: Classes/Service/MyService.php

    <?php
    declare(strict_types=1);

    namespace Vendor\MyExtension\Service;

    final class MyService
    {
        // ...
    }
```

### Inline Code and Text Roles

```rst
Use :php:`MyClass` for PHP references.
The file :file:`ext_localconf.php` is loaded automatically.
Click :guilabel:`Save` to apply changes.
Press :kbd:`Ctrl+S` to save.
```

### Links and References

```rst
See :ref:`my-reference-label` for more information.

External link: `TYPO3 Documentation <https://docs.typo3.org/>`__

..  _my-reference-label:

Section with Reference
======================

This section can be referenced from anywhere.
```

## TYPO3 Directives

### confval (Configuration Values)

If the **display title** of a `.. confval::` is not unique in your manual, you **must** set **`:name:`** to a unique slug (TYPO3 merges duplicate titles poorly in indexes). See [Configuration values (confval)](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/Reference/ReStructuredText/Code/Confval.html) and the Content Blocks supplement for multi-field examples.

```rst
..  confval:: encryptionMethod
    :name: ext-myext-encryptionMethod
    :type: string
    :default: 'aes-256-gcm'
    :required: false

    The encryption method to use for API keys.

    Available options:

    -   ``aes-256-gcm`` (recommended)
    -   ``aes-256-cbc``
```

### versionadded / versionchanged / deprecated

```rst
..  versionadded:: 2.0.0
    This feature was added in version 2.0.0.

..  versionchanged:: 2.1.0
    The default value was changed from ``false`` to ``true``.

..  deprecated:: 3.0.0
    Use :php:`newMethod()` instead.
```

### Admonitions

```rst
..  note::
    Background information users should know.

..  tip::
    Helpful suggestion for better results.

..  warning::
    Potential issue or data loss risk.

..  important::
    Critical information that must not be missed.
```

### Tabs

```rst
..  tabs::

    ..  group-tab:: Composer

        Install via Composer:

        ..  code-block:: bash

            composer require vendor/my-extension

    ..  group-tab:: TER

        Download from the TYPO3 Extension Repository.
```

### Card Grid

```rst
..  card-grid::
    :columns: 2
    :card-height: 100

    ..  card:: Installation

        Learn how to install the extension.

        :ref:`Read more <installation>`

    ..  card:: Configuration

        Configure the extension for your needs.

        :ref:`Read more <configuration>`
```

### Accordion

```rst
..  accordion::

    ..  accordion-item:: How do I install this extension?

        See the :ref:`installation` chapter.

    ..  accordion-item:: What PHP version is required?

        PHP 8.2 or higher is required.
```

## Editor Configuration

Create `Documentation/.editorconfig`:

```editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 80
```

## Rendering Documentation

### Local Rendering

```bash
# Render documentation (extension root = /project; official HOWTO uses --config=Documentation)
docker run --rm --pull always -v $(pwd):/project -w /project -it \
  ghcr.io/typo3-documentation/render-guides:latest --config=Documentation

# Output is in Documentation-GENERATED-temp/
```

### With live preview

Current **`render-guides`** images expose **`render` / `run`**, **`migrate`**, **`init`**, **`lint-guides-xml`**, **`configure`**, **`create-redirects-from-git`**, etc. — confirm with **`-h`** for your tag. **Live preview** is provided by **`--watch`** on the render command (default port is often **1337**); there is **no separate `serve` subcommand** in current entrypoints.

```bash
docker run --rm --pull always -v $(pwd):/project -w /project -p 1337:1337 -it \
  ghcr.io/typo3-documentation/render-guides:latest \
  --config=Documentation --watch
```

> CLI flags and defaults change between image tags — always check **`-h`**. Use **`--watch`** on `render` for live preview; do not assume a `serve` command exists.

### Validation

```bash
# Fail the build on warnings/errors — flag name varies by image; confirm with `-h` before relying on `--fail-on-log`
docker run --rm --pull always -v $(pwd):/project -w /project -it \
  ghcr.io/typo3-documentation/render-guides:latest --config=Documentation --no-progress --fail-on-log

# Validate guides.xml — `lint-guides-xml` must be the first CLI argument (do not prefix with `--config=…` on the same argv slot)
docker run --rm --pull always -v $(pwd):/project -w /project -it \
  ghcr.io/typo3-documentation/render-guides:latest lint-guides-xml
```

## Screenshots

### Requirements
- PNG format (official TYPO3 screenshot guidelines focus on **dimensions**, not DPI — e.g. full-page shots around **1400×1050 px**; confirm current docs)
- Appropriate size (not too large)
- Always include `:alt:` text

### Adding Screenshots

```rst
..  figure:: /Images/BackendModule.png
    :alt: Backend module screenshot
    :class: with-shadow

    The backend module provides an overview of all items.
```

### Screenshot Directory

```
Documentation/
└── Images/
    ├── BackendModule.png
    ├── Configuration.png
    └── Frontend.png
```

## Writing Guidelines

### General Rules
- Use **American English** spelling (color, behavior, optimize)
- Use **sentence case** for headings (not Title Case)
- Maximum line length: **80 characters**
- Use **4 spaces** for indentation (no tabs)
- Add blank line before and after code blocks
- Use present tense

### CamelCase for Files
- `Index.rst` (not `index.rst`)
- `Configuration/` (not `configuration/`)
- `BackendModule.png` (not `backend-module.png`)

### Example: Good Documentation

```rst
============
Installation
============

This chapter explains how to install the extension.

Requirements
============

-   TYPO3 v14.x
-   PHP 8.2 or higher

Installation via Composer
=========================

Run the following command:

..  code-block:: bash

    composer require vendor/my-extension

After installation, activate the extension:

..  code-block:: bash

    vendor/bin/typo3 extension:setup -e my_extension

> Extension CLI flags change between Core versions — run `vendor/bin/typo3 extension:setup --help` (typically **`-e` / `--extension`**).
```

## Deployment to docs.typo3.org

### Prerequisites
1. Extension registered on extensions.typo3.org
2. Documentation in `Documentation/` directory
3. Valid `guides.xml` configuration

### Webhook Setup

1. Go to https://intercept.typo3.com/
2. Login with TYPO3.org account
3. Register your repository
4. Add webhook to GitHub/GitLab

### Trigger Rendering

Documentation is automatically rendered when:
- Webhook receives push event
- Manual trigger via Intercept

## Complete Index.rst Example

> **`Includes.rst.txt`:** When your project root contains this file, the TYPO3 documentation rendering toolchain **merges** it automatically for many manuals — you often **do not** need a manual `.. include::` in every `Index.rst`. If your template or older tutorial shows `.. include:: /Includes.rst.txt`, only keep it when that file actually exists in **your** tree; otherwise remove the directive.

```rst
.. _start:

==============
My Extension
==============

:Extension key:
    my_extension

:Package name:
    vendor/my-extension

:Version:
    |release|

:Language:
    en

:Author:
    Your Name

:License:
    This document is published under the
    `Creative Commons BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__
    license.

:Rendered:
    |today|

----

This extension provides functionality for managing items.

----

**Table of Contents**

..  toctree::
    :maxdepth: 2
    :titlesonly:

    Introduction/Index
    Installation/Index
    Configuration/Index
    Usage/Index
    Developer/Index

..  toctree::
    :hidden:

    Sitemap
```

## Appendix

For resource links, v14-specific documentation notes, and attribution details, see [references/v14-and-resources.md](references/v14-and-resources.md).

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-docs-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
