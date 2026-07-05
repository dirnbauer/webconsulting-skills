# Manual review workflow

1. Open the target page.
2. Open the extension side panel and connect the page.
3. Run **page helper scan**.
4. Review the scan summary:
   - missing alt attributes are not automatically a fail, but need review;
   - empty alt may be correct for decorative images;
   - generic links need human judgment from context;
   - small targets may be allowed if spacing/inline/UA exceptions apply.
5. Use highlights for structural checks:
   - Headings: check H1 and logical order.
   - Landmarks: check header/nav/main/footer/search regions.
   - Images: check alt text quality, not just presence.
   - Forms: check labels, instructions, errors and autocomplete.
   - Links: check link purpose and icon-only accessible names.
   - Focusable: check unexpected tab stops and missing names.
   - Small targets: review WCAG 2.5.8 exceptions.
6. Start focus recorder and tab through the page:
   - record focus order problems under 2.4.3;
   - invisible focus under 2.4.7;
   - focus hidden by sticky content under 2.4.11;
   - keyboard traps under 2.1.2.
7. Mark each relevant checkpoint.
8. Export session JSON.
9. Export open-issues YAML.
10. Merge confirmed issues into `.a11y/open-issues.yml`.
11. Run the skill's report and statement generator.

## Recommended page samples

At minimum, review:

- homepage,
- standard content page,
- news/listing page,
- detail page,
- search page,
- contact/form page,
- login/authentication page if present,
- pages with accordions/tabs/modals/sliders/maps/video/PDF downloads,
- each language variant,
- mobile viewport.
