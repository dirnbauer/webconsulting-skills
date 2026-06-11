# Quick Reference: System Recommendations

Continues `ui-design-patterns` from [full guide](full-guide.md).

## Quick Reference: System Recommendations

### Spacing Scale

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
--space-12: 48px;
--space-16: 64px;
--space-24: 96px;
--space-32: 128px;
```

### Type Scale

```css
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
--text-4xl: 36px;
--text-5xl: 48px;
--text-6xl: 60px;
```

### Shadow Scale

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
--shadow-xl: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-2xl: 0 20px 25px rgba(0, 0, 0, 0.15), 0 10px 10px rgba(0, 0, 0, 0.04);
```

### Border Radius Scale

```css
--radius-sm: 2px;
--radius-md: 4px;
--radius-lg: 8px;
--radius-xl: 12px;
--radius-2xl: 16px;
--radius-full: 9999px;
```

### Interaction States

Every interactive element needs clear state feedback:

```css
/* Button states example */
.button {
  background: var(--primary-500);
  transition: all 0.15s ease;
}
.button:hover {
  background: var(--primary-600);
}
.button:active {
  background: var(--primary-700);
  transform: translateY(1px);
}
.button:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### WCAG 2.1 AA Checklist

| Requirement | Target |
|-------------|--------|
| Text contrast (small) | 4.5:1 minimum |
| Text contrast (large) | 3:1 minimum |
| UI component contrast | 3:1 minimum |
| Focus indicators | Visible (SC 2.4.7) |
| Touch targets | 24×24px minimum (WCAG 2.2 SC 2.5.8); 44×44px is AAA/best practice |
| Color independence | Never color alone |
| Text resize | Works at 200% zoom |

---

*For deeper learning, study the source materials: [Refactoring UI](https://www.refactoringui.com/) and [Practical UI](https://www.practical-ui.com/)*


Source: https://github.com/dirnbauer/webconsulting-skills
