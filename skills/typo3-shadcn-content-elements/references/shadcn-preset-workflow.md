# shadcn Preset Workflow

Use this reference when a TYPO3/Fluid project must follow a shadcn/create preset.

## Rule

shadcn presets are build-time design-system inputs. They generate CSS variables, fonts, radius, icon-library settings, and component class contracts. A TYPO3 site should not fetch a preset dynamically at runtime. Generate or inspect the preset in a scratch app, then commit the resulting tokens and translated Fluid component classes.

For EXT:desiderio, the current default reference preset is `b4hb38Fyj`
(`radix-mira`, olive base, Nunito Sans, Phosphor icons). Keep older committed presets
available as scoped token blocks when the Site Setting still exposes them.

## Scratch App

From any safe temp directory:

```bash
npx shadcn@latest init --template vite --preset <preset-id> --name preset-check --yes --no-monorepo --no-reinstall
cd preset-check
npx shadcn@latest add button card badge alert accordion tabs table input label textarea select separator avatar progress skeleton --yes
```

Inspect:

- `components.json`: `style`, `baseColor`, `iconLibrary`, menu flags.
- `src/index.css`: `:root`, `.dark`, `@theme inline`, imported fonts.
- `src/components/ui/*.tsx`: primitive class contracts.

## Porting To TYPO3

- Put preset tokens into committed CSS, usually `Resources/Public/Css/shadcn-theme.css`.
- Scope alternate presets with `body[data-shadcn-preset="<preset-id>"]` and `.dark body[data-shadcn-preset="<preset-id>"]`.
- Keep Tailwind v4 semantic utilities wired through `Resources/Private/Tailwind/desiderio.css`.
- Translate React `className` to Fluid `class`.
- Preserve `data-slot`, `data-size`, `data-state`, `data-orientation`, `aria-*`, and group variants.
- Prefer Fluid components in `Resources/Private/Components` over repeated class strings in every content element.

## Switching Presets

When the user gives another preset id, such as `b6G5977cw`:

1. Generate the scratch app.
2. Extract tokens and primitive class differences.
3. Add/update a scoped preset block.
4. Rebuild CSS.
5. Verify a representative styleguide page and at least one backend preview.

Do not claim arbitrary preset switching works unless the preset is committed or there is a documented generator that writes the tokens.
