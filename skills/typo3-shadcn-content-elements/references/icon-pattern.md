# TYPO3 Content Element Icon Pattern

Use this reference when creating or refreshing `assets/icon.svg` for Content Blocks.

## SVG Rules

- Use `viewBox="0 0 16 16"`.
- Keep a transparent background.
- Primary geometry uses `currentColor`.
- Accent geometry uses `var(--icon-color-accent,currentColor)`.
- Include a short `<title>` matching the content element, for example `Pricing Calculator icon`.
- Avoid hardcoded black, white, gray, or theme-specific fills.
- Keep detail low; icons must work at 16px in the new content element wizard and page module.

## Starter Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round">
  <style>.accent{stroke:var(--icon-color-accent,currentColor);fill:none}.accent-fill{stroke:none;fill:var(--icon-color-accent,currentColor)}</style>
  <!-- semantic shape -->
</svg>
```

For batches of dozens or hundreds of icons, generate the SVGs deterministically from the content element slug, title, group, and schema. It is fine to use image models for metaphor exploration, but do not commit raster output or uneditable traced images as TYPO3 backend icons.

## Semantic Families

- hero/header: large block, image/sun/title line.
- content/text: lines, split layout, document shapes.
- card/grid: bordered cards, tiles, lists.
- data/chart: bars, line, pie, radar, table.
- navigation/footer: menu, links, columns, social nodes.
- commerce/pricing: tag, currency, tier cards, calculator.
- people/team/testimonial: avatar, quote, group.
- legal/compliance: shield, document, check, scales.

## Verification

- Open several icons at 16px and 32px.
- Check dark and light backend schemes.
- Confirm the metaphor matches the content element title.
- Confirm no solid background rectangle is present.
