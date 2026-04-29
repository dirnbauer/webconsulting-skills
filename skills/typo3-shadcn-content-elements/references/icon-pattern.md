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
- Make every content element icon visually distinguishable from every other icon in the same wizard group. A title-only or metadata-only difference does not count.
- For large catalogs, normalize SVGs by removing `<title>` and compare geometry hashes. Duplicate bodies should fail the pass.
- Add a visible per-element signature mark or secondary motif when many elements share a family shape, but do not rely on the mark alone when a stronger metaphor exists.

## Starter Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round">
  <style>.accent{stroke:var(--icon-color-accent,currentColor);fill:none}.accent-fill{stroke:none;fill:var(--icon-color-accent,currentColor)}</style>
  <!-- semantic shape -->
</svg>
```

For batches of dozens or hundreds of icons, generate the SVGs deterministically from the content element slug, title, group, and schema.

When a user asks for GPT Image / Image GPT / `gpt-image-*` icon generation:

1. Check whether `OPENAI_API_KEY` or the project's image-generation integration is available.
2. Verify the current model name in official OpenAI docs. Do not assume a requested model such as `gpt-image-2` exists; use the latest available GPT Image model when configured.
3. Use the image model to produce 2-4 metaphor directions per difficult icon family, for example "pricing annual/monthly toggle", "navbar sticky", or "hero startup".
4. Redraw the chosen direction as SVG paths by hand or deterministic code. Do not commit PNG/WebP output, bitmap traces, base64 images, or unreviewed generated SVG.
5. Sanitize the final SVG: no scripts, no external references, no embedded raster data, no hardcoded colors, no IDs that collide across icons.

## Semantic Families

- hero/header: distinguish startup, search, video, testimonial, product, pricing, logo-cloud, countdown, form, fullscreen, gradient, and minimal variants.
- content/text: distinguish article, story, text-media, resource library, case study, highlight, divider, and carousel variants.
- card/grid: distinguish card, overlay, interactive, category, product, library, bento, and matrix variants.
- data/chart: distinguish bar, line, area, pie, donut, radar, heatmap, table, dashboard, KPI, counter, and leaderboard variants.
- navigation/footer: distinguish menu, tabs, table of contents, breadcrumb, pagination, mobile, sidebar, sticky, transparent, mega menu, app links, newsletter, social, contact, and legal footer variants.
- commerce/pricing: distinguish two/three/four tier, toggle, annual/monthly, usage meter, calculator, comparison, enterprise, FAQ, bundle, and order summary variants.
- people/team/testimonial: distinguish member, grid, department, org chart, founder quote, culture, history, values, career, testimonial video, review carousel, rating, awards, certifications, logos, and trust badges.
- legal/compliance: distinguish shield, lock, accessibility figure, document, warning, GDPR/privacy, imprint, terms, and disclaimer variants.

## Duplicate Audit

Use this pattern after regenerating icons:

```bash
php -r '
$groups = [];
foreach (glob("ContentBlocks/ContentElements/*/assets/icon.svg") as $file) {
    $svg = file_get_contents($file);
    $svg = preg_replace("#<title>.*?</title>\s*#s", "", $svg);
    $groups[sha1($svg)][] = $file;
}
$dupes = array_filter($groups, fn($files) => count($files) > 1);
echo "unique bodies: " . count($groups) . " / " . count(glob("ContentBlocks/ContentElements/*/assets/icon.svg")) . PHP_EOL;
echo "duplicate groups: " . count($dupes) . PHP_EOL;
'
```

If duplicate bodies remain, add a more specific metaphor first. Use a small signature mark only as the last bit of differentiation.

## Verification

- Open several icons at 16px and 32px.
- Check dark and light backend schemes.
- Confirm the metaphor matches the content element title.
- Confirm no solid background rectangle is present.
- Confirm no two icons share identical geometry after removing `<title>`.
