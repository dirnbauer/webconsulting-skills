# 9. WCAG 2.2 Quick Reference

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 9. WCAG 2.2 Quick Reference

| Success Criterion | Level | TYPO3 Solution |
|-------------------|-------|----------------|
| 1.1.1 Non-text Content | A | `alt` attribute on `<f:image>`, TCA required field |
| 1.3.1 Info and Relationships | A | Semantic HTML in Fluid, `<fieldset>`/`<legend>` |
| 1.3.5 Identify Input Purpose | AA | `autocomplete` attributes on form fields |
| 1.4.1 Use of Color | A | Icons + text alongside color indicators |
| 1.4.3 Contrast (Minimum) | AA | CSS variables with 4.5:1 ratio |
| 1.4.4 Resize Text | AA | `rem` units, no `user-scalable=no` |
| 1.4.10 Reflow | AA | Fluid/responsive layouts |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components |
| 1.4.12 Text Spacing | AA | `line-height: 1.6`, flexible containers |
| 2.1.1 Keyboard | A | Native elements, keyboard handlers |
| 2.4.1 Bypass Blocks | A | Skip link |
| 2.4.3 Focus Order | A | Logical DOM order |
| 2.4.7 Focus Visible | AA | `:focus-visible` styles |
| 2.4.11 Focus Not Obscured | AA | `scroll-margin-top`, no sticky overlaps |
| 2.5.8 Target Size (Minimum) | AA | **24×24 CSS px** minimum; larger targets improve usability |
| 3.1.1 Language of Page | A | `<html lang>` via middleware |
| 3.1.2 Language of Parts | AA | `lang` attribute on multilingual content |
| 3.3.1 Error Identification | A | `aria-invalid`, `aria-describedby` |
| 3.3.2 Labels or Instructions | A | `<label>` on every input |
| 4.1.2 Name, Role, Value | A | ARIA attributes on custom widgets |
| 4.1.3 Status Messages | AA | `aria-live` regions |
