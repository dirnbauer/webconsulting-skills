# Vite Configuration

## Overview

Vite is the standard build tool, integrated with TYPO3 via `praetorius/vite-asset-collector`. The configuration handles:

- TypeScript compilation
- SCSS processing with PostCSS (autoprefixer + cssnano)
- Per-content-element code splitting via entrypoints
- SVG optimization via custom plugin
- Image optimization
- Gzip + Brotli compression (production)
- HMR for development

## vite.config.ts

```typescript
import { defineConfig } from 'vite';
import { resolve } from 'node:path';
import autoprefixer from 'autoprefixer';
import cssnano from 'cssnano';
import { compression } from 'vite-plugin-compression2';
import { ViteImageOptimizer } from 'vite-plugin-image-optimizer';
import autoOrigin from 'vite-plugin-auto-origin';
import { SvgCopyOptimizePlugin } from './vite.helpers';

const isProduction = process.env.NODE_ENV === 'production';

export default defineConfig({
    publicDir: false,
    build: {
        manifest: true,
        rollupOptions: {
            input: {
                'main': resolve(__dirname, 'Resources/Private/Entrypoints/main.entry.ts'),
                'accordion': resolve(__dirname, 'Resources/Private/Entrypoints/accordion.entry.ts'),
                // ... one entry per content element / page feature
                'rte': resolve(__dirname, 'Resources/Private/Scss/rte.scss'),
            },
            output: {
                entryFileNames: 'js/[name]-[hash].js',
                chunkFileNames: 'js/[name]-[hash].js',
                assetFileNames: (assetInfo) => {
                    if (assetInfo.name?.endsWith('.css')) return 'css/[name]-[hash][extname]';
                    if (assetInfo.name?.match(/\.(woff2?|ttf|eot)$/)) return 'fonts/[name]-[hash][extname]';
                    if (assetInfo.name?.match(/\.(png|jpe?g|gif|svg|webp|avif)$/)) return 'images/[name]-[hash][extname]';
                    return 'assets/[name]-[hash][extname]';
                },
                manualChunks: (id) => {
                    if (id.includes('node_modules')) {
                        return id.split('node_modules/').pop()?.split('/')[0];
                    }
                },
            },
        },
        outDir: resolve(__dirname, 'Resources/Public/Build'),
        emptyOutDir: true,
        cssCodeSplit: true,
        assetsInlineLimit: 100, // Prevents SVG inlining (needed for SvgIconProvider)
        minify: isProduction ? 'terser' : false,
    },
    css: {
        postcss: {
            plugins: [
                autoprefixer(),
                ...(isProduction ? [cssnano()] : []),
            ],
        },
        preprocessorOptions: {
            scss: {
                api: 'modern-compiler',
                additionalData: `$mode: "${isProduction ? 'production' : 'development'}";`,
            },
        },
    },
    plugins: [
        autoOrigin(),
        SvgCopyOptimizePlugin(),
        ...(isProduction ? [
            ViteImageOptimizer({
                png: { quality: 80 },
                jpeg: { quality: 80 },
                webp: { quality: 80 },
            }),
            compression({ algorithm: 'gzip' }),
            compression({ algorithm: 'brotliCompress' }),
        ] : []),
    ],
    server: {
        host: '0.0.0.0',
        port: 5173,
        strictPort: true,
        origin: 'http://localhost:5173',
    },
});
```

## Entrypoints

Each content element or page feature gets its own entrypoint in `Resources/Private/Entrypoints/`:

```
main.entry.ts          # Main entrypoint (always loaded)
accordion.entry.ts     # Only loaded on pages with accordions
slider.entry.ts        # Only loaded on pages with sliders
lightbox.entry.ts      # Only loaded on pages with lightboxes
solr.entry.ts          # Only loaded on search pages
```

### Entrypoint Pattern

```typescript
// main.entry.ts
import '../Scss/main.scss';
import { Collapse, Dropdown } from 'bootstrap';
import { initStickyHeader } from '../TypeScript/Plugins/stickyheader';
import { initNavHelper } from '../TypeScript/Plugins/navhelper';

document.addEventListener('DOMContentLoaded', () => {
    initStickyHeader();
    initNavHelper();
});
```

```typescript
// accordion.entry.ts
import '../Scss/ContentElements/_accordion.scss';
import { initAccordionStacked } from '../TypeScript/Plugins/accordion-stacked';

document.addEventListener('DOMContentLoaded', () => {
    const accordions = document.querySelectorAll('.ce-accordion');
    if (accordions.length > 0) {
        initAccordionStacked();
    }
});
```

### Fluid Integration

Include entrypoints in content element templates:

```html
<vite:asset entry="EXT:my_sitepackage/Resources/Private/Entrypoints/accordion.entry.ts" />
```

The `main.entry.ts` is included in the page layout (loaded on every page).

## SVG Optimization Plugin

The custom `SvgCopyOptimizePlugin` processes SVGs from `Resources/Private/Svg/` to `Resources/Public/Svg/`:

- Reads SVGs from `Resources/Private/Svg/`
- Optimizes with SVGO (using `svgo.config.js` if present)
- Slugifies filenames (lowercase, hyphens)
- Writes optimized files to `Resources/Public/Svg/`
- Watches for changes in dev mode (add/change/delete)
- Tracks processed files to avoid redundant work
- Logs optimization stats (original size vs optimized)

The plugin source lives in `vite.helpers.ts` and is imported in `vite.config.ts`.

### svgo.config.js

```javascript
export default {
    plugins: [
        {
            name: 'preset-default',
            params: {
                overrides: {
                    removeViewBox: false,
                    cleanupIds: false,
                },
            },
        },
        'removeDimensions',
    ],
};
```

## HMR (Hot Module Replacement)

For local development:

1. Run the Vite dev server (e.g. `npm run hmr`) on port 5173
2. The `vite-asset-collector` extension detects the dev server and serves assets from it
3. CSS changes are injected without page reload
4. TypeScript changes trigger a page reload

## CSP Compliance

The `vite-asset-collector` supports nonce-based asset inclusion for Content Security Policy:

- Assets loaded via `<vite:asset>` automatically get the correct nonce
- No inline `<script>` or `<style>` tags needed
- Configure CSP headers in TYPO3's Content-Security-Policy API or web server config
- The `autoOrigin` plugin ensures HMR works with CSP in development

## package.json Scripts

Configure build and lint scripts in your project's `package.json` as needed.
