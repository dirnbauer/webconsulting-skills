---
name: "typo3-docs"
description: "Use when creating, editing, or reviewing TYPO3 extension documentation (Documentation/*.rst, guides.xml, README.md, XLF translations), rendering docs with Docker, using TYPO3 RST directives, adding screenshots, deploying to docs.typo3.org, improve docs, fix documentation, or XLIFF 2-space indentation (TYPO3 v14+)."
---

# TYPO3 Documentation Skill

Create and maintain TYPO3 extension documentation following official docs.typo3.org standards.

## Core Workflow

1. **Run extraction first** to identify documentation gaps:
   ```bash
   scripts/extract-all.sh /path/to/extension
   scripts/analyze-docs.sh /path/to/extension
   ```
2. Consult the appropriate reference file for the task
3. Use TYPO3-specific directives, not plain text
4. Validate: `scripts/validate_docs.sh /path/to/extension`
5. Render: `scripts/render_docs.sh /path/to/extension`

> **Critical**: When the user asks to "show docs", render and display HTML output, not raw RST.

## Element Selection Guide

| Content Type | Directive |
|--------------|-----------|
| Complete code | `literalinclude` (preferred over `code-block`) |
| Short snippets | `code-block` with `:caption:` |
| Config options | `confval` with `:name:`, `:type:`, `:default:` |
| PHP API | `php:method::` -- use `:returntype:` for nullable/union types |
| Notices | `note`, `tip`, `warning`, `important` |
| Feature grids | `card-grid` with `stretched-link` in footer |
| Alternatives | `tabs` (synchronized) |
| Screenshots | `figure` with `:zoom: lightbox` `:class: with-border with-shadow` |

## Critical Rules

- **UTF-8**, **4-space** indent, **80 char** line length, **LF** endings
- **CamelCase** file/directory names, **sentence case** headings
- **Permalink anchors** (`.. _label:`) before **every** section heading
- **Index.rst** required in every subdirectory
- **PNG** screenshots with `:alt:` and `:zoom: lightbox`
- **.editorconfig** required in `Documentation/`
- **Screenshots MANDATORY** for backend modules, config screens, UI workflows
- **Max 250 lines per RST page** -- split with `toctree` if exceeded
- **No `mailto:` links** -- use GitHub Issues/Discussions URLs
- **PHP domain**: never use `?Type` or `Type|null` in `php:method::` signatures; use `:returntype:` instead

## Code Example Validation

Cross-reference code examples against extension source:
grep method names in `Classes/`, compare CLI arguments against `configure()`,
verify API signatures match. See `references/extraction-patterns.md`.

## Pre-Commit Checklist

1. `.editorconfig` in `Documentation/`, `Index.rst` in every directory
2. 4-space indent, no tabs, max 80 chars
3. Code blocks have `:caption:`, inline code uses proper roles
4. Screenshots exist with `:alt:` and `:zoom: lightbox`
5. `scripts/validate_docs.sh` passes, render has no warnings
6. README and Documentation/ are synchronized

## References

- `references/file-structure.md` -- directory layout, naming conventions
- `references/guides-xml.md` -- build configuration, interlink settings
- `references/coding-guidelines.md` -- .editorconfig, indentation rules
- `references/rst-syntax.md` -- headings, lists, tables, formatting
- `references/text-roles-inline-code.md` -- `:php:`, `:file:`, `:guilabel:`, `:ref:`
- `references/code-structure-elements.md` -- code blocks, confval, PHP domain
- `references/typo3-directives.md` -- confval, versionadded, deprecated
- `references/content-directives.md` -- accordion, tabs, card-grid
- `references/screenshots.md` -- image requirements, figure directives
- `references/rendering.md` -- Docker commands, live preview
- `references/intercept-deployment.md` -- webhook, build triggers
- `references/asset-templates-guide.md` -- templates, screenshot workflow

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-docs-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
