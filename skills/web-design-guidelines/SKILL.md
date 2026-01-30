---
name: web-design-guidelines
description: Review web interfaces for compliance with modern design guidelines. Check accessibility, usability, semantic HTML, ARIA, keyboard navigation, and responsive design. Use when reviewing frontend code, auditing interfaces, or ensuring WCAG compliance.
version: 1.0.0
license: MIT
triggers:
  - web design
  - interface review
  - accessibility audit
  - a11y
  - wcag
  - aria
  - semantic html
  - keyboard navigation
  - usability review
  - design review
---

# Web Design Guidelines

> **Source:** This skill is adapted from **[Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)** 
> web-design-guidelines skill for Claude Code and AI agents.

Review web interfaces for compliance with modern design guidelines. Check for accessibility, 
usability, semantic HTML, ARIA patterns, keyboard navigation, and responsive design.

---

## How to Use

When reviewing frontend code:

1. Read the specified files
2. Apply all rules from this guide
3. Output findings in terse `file:line` format

---

## Rule Categories by Priority

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Accessibility | CRITICAL |
| 2 | Semantic HTML | HIGH |
| 3 | Keyboard Navigation | HIGH |
| 4 | ARIA Patterns | MEDIUM-HIGH |
| 5 | Responsive Design | MEDIUM |
| 6 | Performance | MEDIUM |
| 7 | Best Practices | LOW |

---

## 1. Accessibility (CRITICAL)

### Color Contrast

| Requirement | Minimum Ratio | WCAG Level |
|-------------|---------------|------------|
| Normal text (< 18px) | 4.5:1 | AA |
| Large text (≥ 18px bold or ≥ 24px) | 3:1 | AA |
| UI components & graphics | 3:1 | AA |
| Enhanced contrast | 7:1 | AAA |

```css
/* ❌ BAD: Insufficient contrast */
.text-light {
  color: #999999;
  background: #ffffff;
  /* Ratio: ~2.8:1 - FAILS */
}

/* ✅ GOOD: Sufficient contrast */
.text-accessible {
  color: #595959;
  background: #ffffff;
  /* Ratio: ~7:1 - PASSES */
}
```

### Focus States

Every interactive element MUST have a visible focus indicator.

```css
/* ❌ BAD: No focus indicator */
button:focus {
  outline: none;
}

/* ✅ GOOD: Clear focus ring */
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* ✅ GOOD: Custom focus style */
a:focus-visible {
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.4);
  border-radius: 4px;
}
```

### Alt Text for Images

```html
<!-- ❌ BAD: Missing alt -->
<img src="hero.jpg" />

<!-- ❌ BAD: Useless alt -->
<img src="hero.jpg" alt="image" />

<!-- ✅ GOOD: Descriptive alt -->
<img src="hero.jpg" alt="Team collaborating around a whiteboard" />

<!-- ✅ GOOD: Decorative image -->
<img src="decoration.svg" alt="" role="presentation" />
```

### Icon-Only Buttons

```html
<!-- ❌ BAD: No accessible label -->
<button>
  <svg><!-- close icon --></svg>
</button>

<!-- ✅ GOOD: Using aria-label -->
<button aria-label="Close dialog">
  <svg aria-hidden="true"><!-- close icon --></svg>
</button>

<!-- ✅ GOOD: Using visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- close icon --></svg>
  <span class="sr-only">Close dialog</span>
</button>
```

### Form Labels

```html
<!-- ❌ BAD: Input without label -->
<input type="email" placeholder="Email" />

<!-- ✅ GOOD: Explicit label -->
<label for="email">Email address</label>
<input type="email" id="email" />

<!-- ✅ GOOD: Label wrapping input -->
<label>
  Email address
  <input type="email" />
</label>
```

### Color Independence

Never use color alone to convey information.

```html
<!-- ❌ BAD: Color only -->
<span style="color: red;">Error</span>

<!-- ✅ GOOD: Color + icon -->
<span style="color: red;">
  <svg aria-hidden="true"><!-- error icon --></svg>
  Error: Invalid email format
</span>

<!-- ✅ GOOD: Color + pattern -->
<div class="error-box" style="border-left: 4px solid red;">
  Error: Invalid email format
</div>
```

---

## 2. Semantic HTML (HIGH)

### Document Structure

```html
<!-- ❌ BAD: Div soup -->
<div class="header">
  <div class="nav">...</div>
</div>
<div class="main">...</div>
<div class="footer">...</div>

<!-- ✅ GOOD: Semantic elements -->
<header>
  <nav>...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

### Heading Hierarchy

```html
<!-- ❌ BAD: Skipped heading levels -->
<h1>Page Title</h1>
<h3>Section Title</h3>  <!-- Skipped h2! -->

<!-- ✅ GOOD: Sequential headings -->
<h1>Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>
```

### Lists

```html
<!-- ❌ BAD: Fake list -->
<div>
  <span>• Item 1</span>
  <span>• Item 2</span>
</div>

<!-- ✅ GOOD: Real list -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

### Buttons vs Links

```html
<!-- ❌ BAD: Link as button -->
<a href="#" onclick="submitForm()">Submit</a>

<!-- ❌ BAD: Div as button -->
<div onclick="handleClick()">Click me</div>

<!-- ✅ GOOD: Button for actions -->
<button type="submit">Submit</button>

<!-- ✅ GOOD: Link for navigation -->
<a href="/about">About us</a>
```

### Tables

```html
<!-- ❌ BAD: Missing table semantics -->
<table>
  <tr>
    <td>Name</td>
    <td>Email</td>
  </tr>
  <tr>
    <td>John</td>
    <td>john@example.com</td>
  </tr>
</table>

<!-- ✅ GOOD: Proper table structure -->
<table>
  <caption>User list</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John</td>
      <td>john@example.com</td>
    </tr>
  </tbody>
</table>
```

---

## 3. Keyboard Navigation (HIGH)

### Tab Order

Tab order should match visual order.

```html
<!-- ❌ BAD: Positive tabindex breaks order -->
<input tabindex="2" />
<input tabindex="1" />
<input tabindex="3" />

<!-- ✅ GOOD: Natural order or 0 -->
<input />
<input />
<input />
```

### Skip Links

```html
<!-- ✅ GOOD: Skip to main content -->
<a href="#main" class="skip-link">Skip to main content</a>

<nav>...</nav>

<main id="main">...</main>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
  z-index: 999;
}

.skip-link:focus {
  left: 10px;
  top: 10px;
  padding: 8px 16px;
  background: #000;
  color: #fff;
}
```

### Focus Trap for Modals

```javascript
// ✅ GOOD: Trap focus in modal
function trapFocus(modal) {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      } else if (!e.shiftKey && document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}
```

---

## 4. ARIA Patterns (MEDIUM-HIGH)

### ARIA Landmarks

```html
<!-- ✅ GOOD: Landmark regions -->
<header role="banner">...</header>
<nav role="navigation" aria-label="Main">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

### Live Regions

```html
<!-- ✅ GOOD: Announce status updates -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Content updates are announced to screen readers -->
</div>

<!-- ✅ GOOD: Urgent announcements -->
<div role="alert" aria-live="assertive">
  Error: Form submission failed
</div>
```

### Expandable Content

```html
<!-- ✅ GOOD: Disclosure pattern -->
<button 
  aria-expanded="false" 
  aria-controls="content-1"
>
  Toggle content
</button>
<div id="content-1" hidden>
  Hidden content here
</div>
```

### Tabs

```html
<!-- ✅ GOOD: Tab pattern -->
<div role="tablist" aria-label="Settings tabs">
  <button 
    role="tab" 
    aria-selected="true" 
    aria-controls="panel-1" 
    id="tab-1"
  >
    General
  </button>
  <button 
    role="tab" 
    aria-selected="false" 
    aria-controls="panel-2" 
    id="tab-2"
  >
    Security
  </button>
</div>

<div 
  role="tabpanel" 
  id="panel-1" 
  aria-labelledby="tab-1"
>
  General settings content
</div>

<div 
  role="tabpanel" 
  id="panel-2" 
  aria-labelledby="tab-2" 
  hidden
>
  Security settings content
</div>
```

### Modal Dialog

```html
<!-- ✅ GOOD: Dialog pattern -->
<div 
  role="dialog" 
  aria-modal="true" 
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to proceed?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>
```

---

## 5. Responsive Design (MEDIUM)

### Viewport Meta

```html
<!-- ✅ REQUIRED -->
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

### Responsive Typography

```css
/* ✅ GOOD: Fluid typography */
html {
  font-size: clamp(14px, 1vw + 12px, 18px);
}

h1 {
  font-size: clamp(2rem, 4vw + 1rem, 4rem);
}
```

### Touch Targets

```css
/* ✅ GOOD: Minimum 44x44px touch targets */
button, 
a, 
input[type="checkbox"], 
input[type="radio"] {
  min-height: 44px;
  min-width: 44px;
}

/* For inline links, add padding */
nav a {
  padding: 12px 16px;
  display: inline-block;
}
```

### Horizontal Scroll Prevention

```css
/* ✅ GOOD: Prevent horizontal overflow */
html, body {
  overflow-x: hidden;
}

img, video, iframe {
  max-width: 100%;
  height: auto;
}

/* Handle long words */
p, li, td {
  word-break: break-word;
  overflow-wrap: break-word;
}
```

### Responsive Images

```html
<!-- ✅ GOOD: Responsive image -->
<img 
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="Description"
  loading="lazy"
/>
```

---

## 6. Performance (MEDIUM)

### Reduce Motion

```css
/* ✅ GOOD: Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Content Layout Shift

```css
/* ✅ GOOD: Reserve space for async content */
.image-container {
  aspect-ratio: 16 / 9;
  background-color: #f0f0f0;
}

/* Skeleton placeholder */
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Lazy Loading

```html
<!-- ✅ GOOD: Lazy load below-fold images -->
<img src="below-fold.jpg" alt="Description" loading="lazy" />

<!-- ✅ GOOD: Eager load critical images -->
<img src="hero.jpg" alt="Description" loading="eager" fetchpriority="high" />
```

---

## 7. Best Practices (LOW)

### Dark Mode Support

```css
/* ✅ GOOD: Automatic dark mode */
:root {
  --bg-primary: #ffffff;
  --text-primary: #1a1a1a;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1a1a1a;
    --text-primary: #ffffff;
  }
}
```

### Print Styles

```css
@media print {
  /* Hide non-essential elements */
  nav, footer, .no-print {
    display: none;
  }
  
  /* Ensure readability */
  body {
    font-size: 12pt;
    color: #000;
    background: #fff;
  }
  
  /* Show link URLs */
  a[href]::after {
    content: " (" attr(href) ")";
  }
}
```

### Error Messages

```html
<!-- ✅ GOOD: Accessible error message -->
<label for="email">Email</label>
<input 
  type="email" 
  id="email" 
  aria-invalid="true"
  aria-describedby="email-error"
/>
<div id="email-error" role="alert">
  Please enter a valid email address
</div>
```

### Loading States

```html
<!-- ✅ GOOD: Accessible loading -->
<button aria-busy="true" disabled>
  <span class="spinner" aria-hidden="true"></span>
  Loading...
</button>

<!-- Or with live region -->
<div role="status" aria-live="polite">
  Loading content...
</div>
```

---

## Quick Checklist

### Before Launch

- [ ] All images have alt text (or alt="" for decorative)
- [ ] All form inputs have labels
- [ ] Focus indicators visible on all interactive elements
- [ ] Tab order matches visual order
- [ ] Skip link present
- [ ] Heading hierarchy is sequential (h1 → h2 → h3)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Touch targets minimum 44x44px
- [ ] No horizontal scroll on mobile
- [ ] `prefers-reduced-motion` respected
- [ ] Icons have accessible labels
- [ ] Errors announced to screen readers
- [ ] Modals trap focus
- [ ] Viewport meta tag present

### Testing Tools

| Tool | Purpose |
|------|---------|
| axe DevTools | Automated accessibility testing |
| WAVE | Visual accessibility checker |
| Lighthouse | Performance & accessibility |
| NVDA/VoiceOver | Screen reader testing |
| Keyboard only | Tab through entire interface |

---

## Output Format

When reviewing files, output findings as:

```
file.tsx:42 - Missing alt text on image
file.tsx:67 - Button has no accessible label
file.tsx:89 - Insufficient color contrast (2.1:1, needs 4.5:1)
file.css:23 - Focus outline removed without replacement
```

---

## Credits & Attribution

This skill is adapted from **[Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)**.

Original repository: https://github.com/vercel-labs/agent-skills

**Copyright (c) Vercel, Inc.** - MIT License  
Adapted by webconsulting.at for this skill collection
