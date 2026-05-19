# v14-Only Accessibility Changes

Continues `typo3-accessibility` from [full guide](full-guide.md).

## v14-Only Accessibility Changes

> The following accessibility-related changes apply **exclusively to TYPO3 v14**.

### Accessible Combobox Pattern **[v14 only]**

TYPO3 v14 introduces a new **accessible combobox pattern** (Forge [#106637](https://forge.typo3.org/issues/106637); do not confuse with unrelated Gerrit change IDs) in the backend. When building custom backend UI widgets, use this pattern instead of custom autocomplete/dropdown implementations.

### Native `<dialog>` Element **[v14 only]**

Backend modals migrated from **Bootstrap Modal to native `<dialog>` element** (Forge [#107443](https://forge.typo3.org/issues/107443)). The native dialog provides better accessibility out of the box:
- Built-in focus trapping
- Proper `aria-modal` semantics
- `Escape` key handling
- Inert background
- No JavaScript framework dependency

Update custom backend JavaScript that listens to **Bootstrap modal events** such as `show.bs.modal` / `hidden.bs.modal` — TYPO3 v14 uses events like `typo3-modal-show`, `typo3-modal-shown`, `typo3-modal-hide`, and `typo3-modal-hidden`. Also replace Bootstrap modal triggers such as `data-bs-toggle="modal"` with TYPO3's `t3js-modal-trigger` class where appropriate.

### Fluid 5.x Accessibility Impact **[v14 only]**

Fluid 5.x is stricter about ViewHelper arguments in some setups. Prefer correct types for numeric and boolean attributes (`tabindex`, `aria-expanded`, etc.) and validate templates after upgrades.

---
