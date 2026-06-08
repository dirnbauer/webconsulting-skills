# Backend Module Render Verification

> Fluid templates escape every static gate — render the actual module before calling it done.

## Why this matters

`cgl`, `phpstan` (even level 10), and unit tests do **not** parse Fluid. A backend
module can have green CI across the board and still throw an HTTP 500 the moment a
human opens it, because the only thing that exercises the template is an actual
render. "All checks pass" is **not** evidence that a backend module renders.

Two real failure modes that no static gate catches:

| Trap | Symptom | Cause |
|------|---------|-------|
| Wrong ViewHelper namespace | **Whole module 500s** (parse-time, before any output) | e.g. `<be:infobox>` instead of `<f:be.infobox>` — an unregistered namespace prefix is a template **parse** error, not a runtime one, so it takes down the entire view |
| Unbounded chart/canvas | Page balloons (a `<canvas>` grew to 6543px tall) | Chart.js (or similar) with `maintainAspectRatio: false` inside a container that has no fixed height — the canvas keeps growing every reflow |

## Verify the render — two complementary layers

### 1. StandaloneView (functional, no browser)

For ViewHelper-level correctness, render the template through `StandaloneView` in a
functional test (see `functional-testing.md`). This catches namespace registration,
argument, and output errors **without** a browser and runs in CI.

Limitation: it does **not** reproduce the `ModuleTemplate` / backend doc-header
context, asset inclusion (CSS/JS), or browser layout — so it cannot catch the
canvas-height trap or a CSS/JS load-order problem.

### 2. Live render (browser)

For anything with layout, charts, JS modules, or `ModuleTemplate` chrome, open the
module in a running backend (a live render is a browser/manual step, **not** an
automated test — run schema/CLI against the same binaries CI uses, not through DDEV):

```bash
# 1. Apply the schema (v14: extension:setup — NOT database:updateschema, which was removed)
vendor/bin/typo3 extension:setup
# (or: php vendor/bin/typo3 extension:setup)

# 2. Open the module in a running backend (the typo3-ddev skill covers spinning one
#    up locally + the URL scheme), then check:
#    - HTTP 200, not 500 (a 500 here is almost always a Fluid parse error)
#    - no console errors / no "Chart.js not available" (classic-script vs ES-module load order)
#    - canvases/charts have a sane bounded height
```

Take the verification screenshot at **≥1440px** viewport (narrow viewports hide
sidebar/column overflow). The screenshot doubles as documentation evidence.

## Checklist before declaring a backend module "done"

- [ ] Module opens with **HTTP 200** in a real backend (not just green CI)
- [ ] Every ViewHelper namespace used in the template is registered (`<f:…>`, or a declared custom namespace) — a typo'd prefix is a whole-template 500
- [ ] Charts/canvases sit in a **fixed-height** wrapper; no unbounded growth
- [ ] Browser console is clean (no asset load-order / missing-global errors)
- [ ] (Optional but cheap) a `StandaloneView` functional test renders each custom template/partial
