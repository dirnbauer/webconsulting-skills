---
name: web-platform-design
description: >-
  Comprehensive web platform design and accessibility guidelines. Use when building web
  interfaces, implementing WCAG compliance, responsive layouts, forms, typography,
  performance, animations, or internationalization. Covers HTML, CSS, and JavaScript best
  practices.
license: MIT
metadata:
  version: "1.0.0"
---

# Web Platform Design Guidelines

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Framework-agnostic rules for accessible, performant, responsive web interfaces.

Based on WCAG 2.2, MDN Web Docs, and modern web platform APIs.

---

## 1. Accessibility / WCAG [CRITICAL]

Accessibility is not optional. Every rule in this section maps to WCAG 2.2 success criteria.

### 1.1 Use Semantic HTML Elements

| Element | Purpose |
|---------|---------|
| `<main>` | Primary page content (one per page) |
| `<nav>` | Navigation blocks |
| `<header>` | Introductory content or navigational aids |
| `<footer>` | Footer for nearest sectioning content |
| `<article>` | Self-contained, independently distributable content |
| `<section>` | Thematic grouping with a heading |
| `<aside>` | Tangentially related content (sidebars, callouts) |
| `<figure>` / `<figcaption>` | Illustrations, diagrams, code listings |
| `<details>` / `<summary>` | Expandable/collapsible disclosure widget |
| `<dialog>` | Modal or non-modal dialog boxes |
| `<time>` | Machine-readable dates/times |

**Anti-pattern**: Using `<div>` or `<span>` for interactive elements. Never write `<div onclick>` when `<button>` exists.

### 1.2 ARIA Labels on Interactive Elements

Every interactive element must have an accessible name.

```html
<!-- Using aria-label -->
<button aria-label="Close dialog">
  <svg>...</svg>
</button>

<!-- Using visible text -->
<button>
  Save Changes
</button>
```

### 1.3 Keyboard Navigation

All interactive elements must be reachable and operable via keyboard (SC 2.1.1).

- Use native interactive elements which are keyboard-accessible by default
- Never use `tabindex` values greater than 0
- Trap focus inside modals; return focus on close

### 1.4 Visible Focus Indicators

Never remove focus outlines without providing a visible replacement (SC 2.4.7).

```css
:focus-visible {
  outline: 3px solid var(--focus-color, #4A90D9);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}
```

### 1.5 Skip Navigation Links

Provide a mechanism to skip repeated blocks of content (SC 2.4.1).

```html
<a href="#main" class="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main">...</main>
```

### 1.6 Alt Text for Images

Every `<img>` must have an `alt` attribute (SC 1.1.1).

- **Informative images**: describe the content and function
- **Decorative images**: use `alt=""` so screen readers skip them
- **Functional images** (inside links/buttons): describe the action

### 1.7 Color Contrast

| Content | Minimum Ratio |
|---------|--------------|
| Normal text (<24px) | 4.5:1 |
| Large text (>=24px or >=18.66px bold) | 3:1 |
| UI components and graphical objects | 3:1 |

Do not rely on color alone to convey information (SC 1.4.1).

### 1.8 Form Labels

Every form input must have a programmatically associated label (SC 1.3.1, 3.3.2).

```html
<label for="email">Email address</label>
<input type="email" id="email" />
```

---

## 2. Responsive Design [CRITICAL]

### 2.1 Mobile-First Approach

Write base styles for the smallest viewport. Layer complexity with `min-width` media queries.

```css
/* Base: mobile */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet */
@media (min-width: 48rem) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 64rem) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 2.2 Fluid Layouts with Modern CSS Functions

Use `clamp()`, `min()`, and `max()` for fluid sizing.

```css
h1 {
  font-size: clamp(1.75rem, 1.2rem + 2vw, 3rem);
}

.section {
  padding: clamp(1.5rem, 4vw, 4rem);
}

.container {
  width: min(90%, 72rem);
  margin-inline: auto;
}
```

### 2.3 Container Queries

Size components based on their container, not the viewport.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

### 2.4 Touch Targets

Minimum 44x44 CSS pixels for touch targets (WCAG SC 2.5.8). Provide at least 24px spacing between adjacent targets.

```css
button, a, input, select, textarea {
  min-height: 44px;
  min-width: 44px;
}
```

### 2.5 Viewport Meta Tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

Never use `maximum-scale=1` or `user-scalable=no` -- these break pinch-to-zoom accessibility.

### 2.6 No Horizontal Scrolling

Content must reflow at 320px width without horizontal scrolling (SC 1.4.10).

```css
img, video, iframe, svg {
  max-width: 100%;
  height: auto;
}

.prose {
  overflow-wrap: break-word;
}
```

---

## 3. Forms [HIGH]

### 3.1 Autocomplete Attributes

Use `autocomplete` for common fields to enable browser autofill (SC 1.3.5).

```html
<input type="text" name="name" autocomplete="name" />
<input type="email" name="email" autocomplete="email" />
<input type="tel" name="phone" autocomplete="tel" />
```

### 3.2 Correct Input Types

| Type | Use For |
|------|---------|
| `email` | Email addresses |
| `tel` | Phone numbers |
| `url` | URLs |
| `number` | Numeric values with spinners |
| `search` | Search fields |
| `date` / `time` / `datetime-local` | Temporal values |
| `password` | Passwords |
| `text` with `inputmode="numeric"` | PINs, zip codes |

### 3.3 Inline Validation

Validate on `blur` (not on every keystroke). Show success and error states.

```html
<div class="field" data-state="error">
  <label for="username">Username</label>
  <input type="text" id="username" aria-describedby="username-error" aria-invalid="true" />
  <span id="username-error" class="error">Username must be at least 3 characters</span>
</div>
```

### 3.4 Required Field Indication

```html
<label for="name">
  Full name <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input type="text" id="name" required />
```

---

## 4. Typography [HIGH]

### 4.1 Font Stacks

```css
/* System font stack */
body {
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Monospace stack */
code, pre, kbd {
  font-family: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
}
```

### 4.2 Relative Units

Use `rem` for font sizes and spacing. Use `em` for component-relative sizing.

```css
html {
  font-size: 100%; /* = 16px default, respects user preference */
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
small { font-size: 0.875rem; }
```

### 4.3 Line Height and Spacing

Body text line height of at least 1.5 (SC 1.4.12).

```css
body {
  line-height: 1.6;
}

h1, h2, h3 {
  line-height: 1.2;
}
```

### 4.4 Maximum Line Length

Limit line length to approximately 75 characters for readability.

```css
.prose {
  max-width: 75ch;
}
```

### 4.5 Heading Hierarchy

Use `h1` through `h6` in order. Never skip levels. One `h1` per page.

---

## 5. Performance [HIGH]

### 5.1 Lazy Load Below-Fold Images

```html
<img src="below-fold.jpg" alt="Description" loading="lazy" />

<!-- Above fold: eager load -->
<img src="hero.jpg" alt="Description" loading="eager" />
```

### 5.2 Explicit Image Dimensions

Always specify `width` and `height` to prevent layout shift.

```html
<img src="image.jpg" alt="Description" width="800" height="600" />
```

### 5.3 Resource Hints

```html
<!-- Preconnect to third-party origins -->
<link rel="preconnect" href="https://fonts.googleapis.com" />

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin />
```

### 5.4 Avoid Layout Thrashing

Batch DOM reads and writes. Never interleave them.

```js
// Good: batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px';
});
```

---

## 6. Animation and Motion [MEDIUM]

### 6.1 Respect prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 6.2 Compositor-Friendly Animations

Animate only `transform` and `opacity` for smooth 60fps animation.

```css
/* Good: compositor-only properties */
.slide-in {
  transition: transform 200ms ease-out, opacity 200ms ease-out;
}

/* Bad: triggers layout/paint */
.slide-in-bad {
  transition: left 200ms, width 200ms;
}
```

### 6.3 No Flashing Content

Never flash content more than 3 times per second (SC 2.3.1).

---

## 7. Dark Mode and Theming [MEDIUM]

### 7.1 System Preference Detection

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f0f17;
    --text: #e4e4ef;
    --surface: #1c1c2e;
    --border: #2e2e44;
  }
}
```

### 7.2 CSS Custom Properties for Theming

```css
:root {
  color-scheme: light dark;
  --color-bg: #ffffff;
  --color-text-primary: #1a1a2e;
  --color-primary: #2563eb;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0f0f17;
    --color-text-primary: #e4e4ef;
    --color-primary: #60a5fa;
  }
}
```

### 7.3 Color-Scheme Meta Tag

```html
<meta name="color-scheme" content="light dark" />
```

---

## 8. Internationalization [MEDIUM]

### 8.1 dir and lang Attributes

```html
<html lang="en">

<!-- User-generated content -->
<p dir="auto">User-submitted text here</p>
```

### 8.2 Intl APIs for Formatting

```js
// Dates
new Intl.DateTimeFormat('en-US', { dateStyle: 'long' }).format(date);

// Numbers
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(1234.56);

// Relative time
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day');
```

### 8.3 CSS Logical Properties

Use logical properties instead of physical ones to support both LTR and RTL layouts.

```css
/* Logical (works in LTR and RTL) */
.sidebar {
  margin-inline-start: 1rem;
  padding-inline-end: 2rem;
  border-inline-start: 1px solid var(--color-border);
}

.stack > * + * {
  margin-block-start: 1rem;
}
```

| Physical | Logical |
|----------|---------|
| `left` / `right` | `inline-start` / `inline-end` |
| `top` / `bottom` | `block-start` / `block-end` |
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |

---

## Evaluation Checklist

### Accessibility
- [ ] All images have appropriate `alt` text
- [ ] Color contrast meets 4.5:1 (text) and 3:1 (UI components)
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible
- [ ] Skip navigation link is present
- [ ] Form inputs have associated labels
- [ ] Error messages are linked to their inputs
- [ ] Page has proper heading hierarchy

### Responsive
- [ ] No horizontal scrolling at 320px width
- [ ] Touch targets are at least 44x44px
- [ ] Viewport meta tag is present
- [ ] Layout works on mobile, tablet, and desktop

### Forms
- [ ] All inputs have visible labels
- [ ] Autocomplete attributes are set for common fields
- [ ] Correct input types trigger correct mobile keyboards
- [ ] Error messages are clear and specific

### Performance
- [ ] Below-fold images use `loading="lazy"`
- [ ] Images have explicit `width` and `height`
- [ ] Critical fonts are preloaded

### Motion and Theming
- [ ] `prefers-reduced-motion` is respected
- [ ] Animations use only `transform` and `opacity`
- [ ] Dark mode maintains contrast ratios
- [ ] `color-scheme` meta tag is present

### Internationalization
- [ ] `lang` attribute on `<html>`
- [ ] CSS logical properties used
- [ ] Dates/numbers formatted with Intl APIs

---

## Common Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| `<div onclick>` | Use `<button>` |
| `outline: none` without replacement | Use `:focus-visible` with custom outline |
| `placeholder` as label | Add a `<label>` element |
| `tabindex="5"` | Use `tabindex="0"` or natural order |
| `user-scalable=no` | Remove it |
| `font-size: 12px` | Use `font-size: 0.75rem` |
| Animating `width`/`height`/`top`/`left` | Animate `transform` and `opacity` |
| Color alone for status | Add icon, text, or pattern |
| `margin-left` / `padding-right` | Use `margin-inline-start` / `padding-inline-end` |
| `<img>` without dimensions | Add `width` and `height` attributes |
| Hover-only disclosure | Add `:focus-within` and click handler |

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
