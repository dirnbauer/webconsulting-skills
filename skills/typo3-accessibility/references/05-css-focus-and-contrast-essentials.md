# 5. CSS: Focus & Contrast Essentials

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 5. CSS: Focus & Contrast Essentials

```css
/* EXT:site_package/Resources/Public/Css/accessibility.css */

/* Visible focus indicator */
:focus-visible {
    outline: 3px solid var(--focus-color, #2563eb);
    outline-offset: 2px;
}

:focus:not(:focus-visible) {
    outline: none;
}

/* Touch targets: WCAG 2.2 AA 2.5.8 minimum = 24×24 CSS px (baseline below). */
button, a, input, select, textarea, [role="button"] {
    min-height: 24px;
    min-width: 24px;
}

/* Optional comfort target — intentionally stricter than AA; common for mobile tap areas */
.touch-target-comfort {
    min-height: 44px;
    min-width: 44px;
}

/* Good default; test with user-overridden spacing per WCAG 1.4.12 */
body {
    line-height: 1.6;
}

p + p {
    margin-top: 1em;
}

/* Max line length for readability */
.ce-bodytext, .frame-default .content {
    max-width: 75ch;
}

/* Scroll margin for anchored headings */
[id] {
    scroll-margin-top: 5rem;
}

/* Hover + focus parity */
a:hover, a:focus-visible,
button:hover, button:focus-visible {
    text-decoration: underline;
}
```
