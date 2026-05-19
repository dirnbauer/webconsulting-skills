# 10. Anti-Patterns (Flag These in Reviews)

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 10. Anti-Patterns (Flag These in Reviews)

| Anti-Pattern | Fix |
|-------------|-----|
| `<div onclick="...">` | Use `<button>` |
| `outline: none` without replacement | Use `:focus-visible` with custom outline |
| `placeholder` as sole label | Add `<label>` element |
| `tabindex > 0` | Use `tabindex="0"` or natural DOM order |
| `user-scalable=no` in viewport | Remove it |
| `font-size: 12px` (absolute) | Use `rem` units |
| Images without `alt` | Add `alt="..."` or `alt=""` for decorative |
| Color-only error indication | Add icon + text |
| `<a>` without `href` for action | Use `<button>` |
| Missing `lang` on `<html>` | Set via middleware or Fluid layout |
| Auto-playing video with sound | Add `muted` or remove `autoplay` |
| Skipped heading levels | Fix hierarchy |
