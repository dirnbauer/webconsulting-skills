---
name: "typo3-vite"
description: "Vite build setup for TYPO3 v13+ with vite-asset-collector, SCSS architecture, Bootstrap 5 theming, SVG optimization, code splitting, and CSP compliance. Use when configuring Vite for TYPO3 projects, setting up SCSS with Bootstrap, creating entrypoints per content element, optimizing SVGs, configuring PostCSS (autoprefixer, cssnano), loading local fonts via font-face, setting up CSS units (rem/em), or customizing Bootstrap variables. Also triggers for: asset hashing, Gzip/Brotli compression, SCSS import chain, global-basics.scss, selective Bootstrap imports."
---

# TYPO3 Vite Skill

Vite 7 build configuration for TYPO3 v13+ sitepackage development with `praetorius/vite-asset-collector`.

## Key Concepts

### Entrypoint-per-CE Pattern

Each content element gets its own Vite entrypoint (`*.entry.ts`) that imports its SCSS and TypeScript. This enables automatic code splitting -- only the CSS/JS needed for visible content elements is loaded.

### Selective Bootstrap Imports

Never import Bootstrap as a whole. Import only the components you use (`bootstrap/scss/grid`, `bootstrap/scss/buttons`, etc.) to minimize CSS bundle size.

### SVG Optimization

Custom `SvgCopyOptimizePlugin` processes SVGs from `Resources/Private/Svg/` through SVGO and writes optimized files to `Resources/Public/Svg/`. Supports dev-mode file watching.

### CSP Compliance

Assets loaded via `<vite:asset>` ViewHelper automatically get nonce attributes for Content Security Policy compliance. No inline `<script>` or `<style>` tags needed.

## Technology Stack

| Layer | Technology |
|---|---|
| Build | Vite 7+ with `praetorius/vite-asset-collector` |
| CSS | Bootstrap 5.3+ (selective imports, custom theming) |
| PostCSS | autoprefixer + cssnano (production) |
| SCSS | Modern Compiler API (`api: 'modern-compiler'`) |
| SVG | Custom SVGO plugin (`SvgCopyOptimizePlugin`) |
| Compression | Gzip + Brotli (production) |
| Package Manager | npm, pnpm, or yarn |

## References

- `references/vite-configuration.md` -- Complete vite.config.ts, entrypoints, SVG plugin, CSP
- `references/scss-architecture.md` -- SCSS folder structure, import chain, naming conventions, CSS units
- `references/bootstrap-theming.md` -- Bootstrap variable customization per project

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-vite-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
