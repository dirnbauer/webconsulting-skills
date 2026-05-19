# 7. Testing & Tools

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 7. Testing & Tools

### Automated Testing

| Tool | Use |
|------|-----|
| `axe-core` / `axe DevTools` | Browser extension for automated WCAG checks |
| `pa11y` | CLI accessibility testing for CI/CD |
| `Lighthouse` | Chrome DevTools audit (Accessibility score) |
| `WAVE` | Browser extension for visual feedback |

### Manual Testing Checklist

1. **Keyboard only**: Navigate entire page using Tab, Shift+Tab, Enter, Escape, Arrow keys
2. **Screen reader**: Test with VoiceOver (macOS), NVDA/JAWS (Windows)
3. **Zoom**: Verify layout at 200% and 400% zoom
4. **Color**: Use browser dev tools to simulate color blindness
5. **Reduced motion**: Enable `prefers-reduced-motion: reduce` in OS settings

### Pa11y CI Integration

```bash
# Run against local DDEV instance
npx pa11y https://mysite.ddev.site --standard WCAG2AA --reporter cli
```

```json
// .pa11yci.json
{
    "defaults": {
        "standard": "WCAG2AA",
        "timeout": 30000,
        "wait": 2000
    },
    "urls": [
        "https://mysite.ddev.site/",
        "https://mysite.ddev.site/contact",
        "https://mysite.ddev.site/news"
    ]
}
```
