# shadcn Preset Workflow

Use this reference when a TYPO3/Fluid project must follow a shadcn/create preset.

## Rule

shadcn presets are build-time design-system inputs. They generate CSS variables, fonts, radius, icon-library settings, and component class contracts. A TYPO3 site should not fetch a preset dynamically at runtime. Generate or inspect the preset in a scratch app, then commit the resulting tokens and translated Fluid component classes.

For EXT:desiderio, the current default reference preset is `b4hb38Fyj`
(`radix-mira`, olive base, Nunito Sans, Phosphor icons). Keep older committed
presets available as scoped token blocks when the Site Setting still exposes
them. `b6G5977cw` is a supported alternate preset (`radix-lyra`, olive/stone,
JetBrains Mono, Tabler metadata, square radius, default-translucent menu,
subtle menu accent).

## Scratch App

From any safe temp directory:

```bash
npx shadcn@latest init --template vite --preset <preset-id> --name preset-check --yes --no-monorepo --no-reinstall
cd preset-check
npx shadcn@latest add button card badge alert accordion tabs table input label textarea select separator avatar progress skeleton --yes
```

Inspect:

- `components.json`: `style`, `tailwind.baseColor`, `iconLibrary`,
  `menuColor`, and `menuAccent`.
- `src/index.css`: `:root`, `.dark`, `@theme inline`, imported fonts.
- `src/components/ui/*.tsx`: primitive class contracts.

## Porting To TYPO3

- Put preset tokens into committed CSS, usually
  `Resources/Public/Css/shadcn-theme.css`.
- Scope alternate presets with `body[data-shadcn-preset="<preset-id>"]` and
  `.dark body[data-shadcn-preset="<preset-id>"]`.
- Keep Tailwind v4 semantic utilities wired through `Resources/Private/Tailwind/desiderio.css`.
- Translate React `className` to Fluid `class`.
- Preserve `data-slot`, `data-size`, `data-state`, `data-orientation`, `aria-*`, and group variants.
- Prefer Fluid components in `Resources/Private/Components` over repeated class strings in every content element.
- Make sure radius is not accidentally overridden. In Desiderio,
  `desiderio.layout.radius = preset` lets the shadcn preset own `--radius`;
  values such as `none`, `md`, or `full` intentionally override the preset.

## Switching Presets

When the user gives another preset id, such as `b6G5977cw`:

1. Confirm whether the id is already supported in the project.
2. If supported, tell the user to set `desiderio.shadcn.preset` to that id.
3. If supported and the preset has a new source style, set
   `desiderio.shadcn.style` to the matching style value.
4. Set `desiderio.layout.radius` to `preset` when the preset should control
   radius.
5. Keep `desiderio.typography.fontSans` on `preset` when the preset should
   control typography.
6. Flush TYPO3 caches.
7. Check a frontend page in light mode.
8. Check the same frontend page in dark mode.
9. Check the styleguide page if it exists.
10. Check at least one TYPO3 backend layout preview.

When the id is not supported yet:

1. Start from a clean or understood git state.
2. Generate a scratch shadcn project outside the TYPO3 extension.
3. Record `style` from `components.json`.
4. Record `tailwind.baseColor`.
5. Record `iconLibrary`.
6. Record `menuColor`.
7. Record `menuAccent`.
8. Open the generated CSS source.
9. Copy every light `:root` token.
10. Copy every `.dark` token.
11. Copy font imports and font-family choices.
12. Add `body[data-shadcn-preset="<id>"]` to the theme CSS.
13. Add `.dark body[data-shadcn-preset="<id>"]` to the theme CSS.
14. Map font variables to project variables such as `--d-font-sans`,
    `--d-font-heading`, and `--d-font-mono`.
15. Add the id to the TYPO3 Site Settings enum.
16. Add a new style enum value when needed.
17. Do not make the new id the global default unless the user asked for that.
18. Add/update documentation screenshots.
19. Update README and project docs.
20. Update tests that assert supported presets.
21. Run the relevant CSS build if classes or Tailwind sources changed.
22. Run the project tests.
23. Run `git diff --check`.
24. Flush TYPO3 caches.
25. Browser-check frontend light mode.
26. Browser-check frontend dark mode.
27. Browser-check TYPO3 backend previews.
28. Commit the resulting token/settings/docs slice.

## shadcn/create Left-Nav Values

Do not claim every shadcn/create left-nav value is an independent runtime
switch unless the project actually renders a matching Site Setting and CSS/data
attribute. In Desiderio, the preset id is the primary supported switch:

- Style: stored as metadata and used when manually porting component class
  contracts.
- Base Color, Theme, Chart Color, Heading, Font: supported through committed
  preset tokens.
- Radius: supported through preset tokens only when the site radius is
  `preset`; otherwise the site radius intentionally overrides it.
- Icon Library: metadata only. TYPO3 backend icons are committed SVG files.
- Menu and Menu Accent: metadata only unless the project adds explicit Site
  Settings and CSS rules for those values.

Do not claim arbitrary preset switching works unless the preset is committed or there is a documented generator that writes the tokens.
