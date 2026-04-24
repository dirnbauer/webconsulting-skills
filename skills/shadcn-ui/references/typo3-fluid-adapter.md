# shadcn/ui for TYPO3 Fluid and Content Blocks

Use this reference when a TYPO3 project wants the shadcn/ui look, tokens, and interaction model without using React components in production.

## Core Rule

Treat shadcn/ui as a design source and code reference, not as a runtime dependency. Inspect the official registry output, then translate these parts into TYPO3:

- semantic Tailwind class strings
- CSS variable tokens and dark-mode overrides
- slot structure (`data-slot`, header/content/footer anatomy)
- ARIA attributes and keyboard expectations
- `data-state` conventions for open/closed/active states

Do not copy React hooks, JSX-only control flow, Radix imports, or client-only assumptions into Fluid templates.

## Preset Pipeline

1. Store the selected preset id in Site Settings, for example `desiderio.shadcn.preset`.
2. Generate CSS variables from `shadcn/create` or `shadcn apply --preset`.
3. Commit the generated tokens in a global CSS entrypoint, including `:root`, `.dark`, `@theme inline`, chart tokens, sidebar tokens, radius, shadows, and fonts.
4. Add a stable page attribute such as `data-shadcn-preset="{siteSetting}"` so QA can verify the active preset.
5. Keep light and dark mode token sets together. A preset update is incomplete if only light mode changes.

For an existing shadcn project, prefer:

```bash
npx shadcn@latest apply --preset <id> --only theme
```

For a non-React TYPO3 project, use a temporary scratch app to run `apply`, then port the generated token changes into the TYPO3 CSS file.

## Fluid Component Mapping

Map upstream shadcn components to typed Fluid components:

| shadcn source | Fluid target | Notes |
| --- | --- | --- |
| `button` | `Atom/Button` | variants, sizes, disabled/focus states |
| `badge` | `Atom/Badge` | secondary/destructive/outline variants |
| `card` | `Molecule/Card*` | `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter` |
| `input`, `textarea`, `label` | `Atom/Form/*` | keep focus-visible/ring/input tokens |
| `accordion` | `Molecule/Accordion*` | Alpine or vanilla JS sets `aria-expanded` and `data-state` |
| `tabs` | `Molecule/Tabs*` | Alpine or vanilla JS sets active trigger/content |
| `dialog`, `sheet`, `popover` | `Organism/Overlay*` | preserve focus management and escape/overlay behavior |
| `table` | `Molecule/Table*` | semantic table tags, shadcn border/text classes |
| `chart` | `Organism/Chart*` | chart colors use `var(--chart-*)`; avoid React chart wrappers unless the project already uses React |

Declare Fluid component arguments with `<f:argument>`, pass child content through `<f:slot />`, and expose only meaningful variants instead of arbitrary raw HTML options.

## Content Blocks Pattern

Content Blocks remain the data contract. When restyling, keep `config.yaml` field identifiers and `fixture.json` stable unless the content model is intentionally changing.

Use `templates/frontend.fluid.html` for the content element entrypoint and shared Fluid components for repeated shadcn primitives:

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:d="http://typo3.org/ns/Vendor/Sitepackage/Components/ComponentCollection"
      data-namespace-typo3-fluid="true">

<section class="py-12 md:py-16">
    <d:molecule.card class="mx-auto max-w-xl">
        <d:molecule.cardHeader>
            <d:molecule.cardTitle>{data.header}</d:molecule.cardTitle>
            <d:molecule.cardDescription>{data.subheadline}</d:molecule.cardDescription>
        </d:molecule.cardHeader>
        <d:molecule.cardContent>
            <f:format.html>{data.bodytext}</f:format.html>
        </d:molecule.cardContent>
    </d:molecule.card>
</section>
</html>
```

Use per-block CSS only for genuinely unique layout or media behavior. Shared surfaces, buttons, forms, cards, tabs, and tables should come from the global shadcn/Tailwind layer or Fluid components.

## Page Templates and Columns

For TYPO3 v14 PAGEVIEW templates, render page-layout columns through content areas:

```html
<main class="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <f:render.contentArea contentArea="{content.main}" />
</main>
```

For multi-column layouts, use backend layout identifiers such as `main`, `sidebar`, or `footer`, and let content elements receive their area context. Use column restrictions in backend layouts to keep inappropriate content types out of narrow regions.

## Alpine and Interactions

Use Alpine or small vanilla controllers when shadcn behavior depends on client state:

- accordion: `aria-expanded`, `hidden`, `data-state`
- tabs: `role="tablist"`, `aria-selected`, panel visibility
- dialog/sheet: focus trap, escape key, overlay click, body scroll locking
- dropdown/popover: trigger relation, escape key, click outside

Keep interaction hooks as `data-*` attributes where possible so templates stay framework-agnostic.

## Verification

Add tests or static checks for:

- required shadcn tokens in global CSS (`--background`, `--foreground`, `--card`, `--primary`, `--border`, `--ring`, `--chart-*`, `.dark`)
- `@theme inline` mappings for Tailwind v4
- body/html attributes for active preset and color scheme
- Fluid components containing expected canonical class recipes
- Content Blocks preserving their field identifiers while using shared components/classes
- styleguide or overview page fixtures covering every content element

For visual QA, render a page containing all content elements in both light and dark modes, compare screenshots, and check that cards, buttons, forms, tabs, accordions, and chart colors use shadcn tokens instead of bespoke one-off colors.

## Upgrade Strategy

Keep upstream and local concerns separate:

1. Commit the current local state.
2. Run `shadcn info --json` if the project has `components.json`.
3. Use `shadcn apply --preset <id> --only theme` or a scratch app for preset changes.
4. Use `shadcn view <component>` or `shadcn add --dry-run --diff` to inspect upstream component changes.
5. Port token and class changes to Fluid components.
6. Run static tests, Fluid rendering tests, and visual checks.
7. Commit the TYPO3 adaptation separately from upstream scratch output.
