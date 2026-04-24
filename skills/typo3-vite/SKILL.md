---
name: typo3-vite
description: "Vite build setup for TYPO3 v13+ with vite-asset-collector, Tailwind v4/shadcn CSS, SCSS architecture, Bootstrap 5 theming, SVG optimization, code splitting, and CSP compliance. Use when configuring Vite for TYPO3 projects, setting up Tailwind or SCSS, adding shadcn/ui tokens to TYPO3, creating entrypoints per content element, optimizing SVGs, configuring PostCSS, loading local fonts, or customizing Bootstrap variables. Also triggers for: asset hashing, Gzip/Brotli compression, Tailwind @theme inline, global CSS entrypoints, shadcn preset CSS, selective Bootstrap imports."
---

# TYPO3 Vite Skill

Vite 7 build configuration for TYPO3 v13+ sitepackage development with `praetorius/vite-asset-collector`.

## Key Concepts

### Entrypoint-per-CE Pattern

Each content element gets its own Vite entrypoint (`*.entry.ts`) that imports its SCSS and TypeScript. This enables automatic code splitting -- only the CSS/JS needed for visible content elements is loaded.

### Selective Bootstrap Imports

Never import Bootstrap as a whole. Import only the components you use (`bootstrap/scss/grid`, `bootstrap/scss/buttons`, etc.) to minimize CSS bundle size.

### Tailwind v4 + shadcn Mode

For shadcn/ui TYPO3 projects, create a global CSS entrypoint that imports Tailwind v4 and maps shadcn tokens:

```css
@import "tailwindcss";
@import "shadcn/tailwind.css";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-border: var(--border);
  --color-ring: var(--ring);
  --radius-lg: var(--radius);
}
```

Keep `:root` and `.dark` preset tokens in committed CSS, not runtime-generated markup. Include TYPO3 Fluid, Content Blocks, and component template paths in Tailwind content scanning so shadcn utility classes used in `.fluid.html` files are emitted.

Use `f:asset.css`, `vite:asset`, or the project asset collector consistently with the existing sitepackage. Avoid inline scripts/styles so CSP nonces from `vite-asset-collector` can do their job.

### SVG Optimization

Custom `SvgCopyOptimizePlugin` processes SVGs from `Resources/Private/Svg/` through SVGO and writes optimized files to `Resources/Public/Svg/`. Supports dev-mode file watching.

### CSP Compliance

Assets loaded via `<vite:asset>` ViewHelper automatically get nonce attributes for Content Security Policy compliance. No inline `<script>` or `<style>` tags needed.

## Technology Stack

| Layer | Technology |
|---|---|
| Build | Vite 7+ with `praetorius/vite-asset-collector` |
| CSS | Tailwind v4/shadcn tokens or Bootstrap 5.3+ (selective imports, custom theming) |
| PostCSS | autoprefixer + cssnano (production) |
| SCSS | Modern Compiler API (`api: 'modern-compiler'`) |
| SVG | Custom SVGO plugin (`SvgCopyOptimizePlugin`) |
| Compression | Gzip + Brotli (production) |
| Package Manager | npm, pnpm, or yarn |

## References

- `references/vite-configuration.md` -- Complete vite.config.ts, entrypoints, SVG plugin, CSP
- `references/scss-architecture.md` -- SCSS folder structure, import chain, naming conventions, CSS units
- `references/bootstrap-theming.md` -- Bootstrap variable customization per project
- For TYPO3 shadcn adaptation, also read `../shadcn-ui/references/typo3-fluid-adapter.md`

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-vite-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
