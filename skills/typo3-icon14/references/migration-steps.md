# TYPO3 Icon Migration Checklist

Use this checklist when updating existing extension icons.

## 1. Inventory

- [ ] Read the current SVG files
- [ ] Read `Configuration/Icons.php`
- [ ] Read `Configuration/Backend/Modules.php`
- [ ] Read relevant TCA and TCA override files

## 2. Classify

- [ ] Assign every icon to one type: module, extension, plugin, record, or action
- [ ] Confirm the render context and expected viewBox
- [ ] Keep existing identifiers unless there is a good reason to rename them

## 3. Capture meaning

- [ ] Infer the semantic meaning from module names, record names, plugin names, and old SVGs
- [ ] If the meaning is not obvious, ask the user what the icon should communicate
- [ ] For icon families, note which icon is the parent and which are sub-variants

## 4. Load references

- [ ] Load the matching live Core icon family from TYPO3.Icons
- [ ] Check the official Icon API docs for registration details
- [ ] If available, validate the look in `EXT:styleguide`

## 5. Redraw

- [ ] Remove solid legacy backgrounds
- [ ] Replace hardcoded white/black/gray with `currentColor`
- [ ] Use `var(--icon-color-accent, #ff8700)` for accent geometry
- [ ] Confirm no `#fff`, `#000`, `#333`, `white`, or `black` fills remain
- [ ] Simplify shapes until they are readable at the real render size
- [ ] Keep module icons and 16x16 icons visually appropriate for their type

## 6. Register and wire up

- [ ] Register the icon in `Configuration/Icons.php`
- [ ] Update `iconIdentifier` in `Configuration/Backend/Modules.php` if needed
- [ ] Update `pluginIcon`, `typeicon_classes`, and related references
- [ ] Remove legacy registration from `ext_localconf.php`

## 7. Verify

- [ ] Confirm the SVG file path matches the registered source
- [ ] Confirm the icon has the intended viewBox
- [ ] Confirm the icon is readable in its real backend context
- [ ] Switch the backend color scheme and confirm the icon works in **both**
      light and dark mode (top-right user dropdown or User Settings)
- [ ] Clear TYPO3 caches and browser local storage if stale icons still appear
