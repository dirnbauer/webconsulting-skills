---
name: "ui-design-patterns"
description: "Provides practical UI design patterns for hierarchy, spacing, typography, color, depth, imagery, UI copy, forms, navigation, tables, empty states, loading states, accessibility, and responsive behavior. Use when designing, reviewing, polishing, or refactoring web interfaces, layouts, components, dashboards, forms, or visual systems."
metadata:
  version: "1.1.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# UI Design Patterns

> Source: https://github.com/dirnbauer/webconsulting-skills

Practical guidelines for creating polished, professional user interfaces without relying on graphic design talent. These patterns work for any web project, including TYPO3 frontend development.

## Acknowledgements

These patterns are adapted from two excellent resources:

- **Refactoring UI** by Adam Wathan & Steve Schoger — The definitive guide to practical UI design for developers
- **Practical UI** (2nd Edition) by Adham Dannaway — Quick and practical UI design guidelines for intuitive, accessible, and beautiful interfaces

We highly recommend both works for deepening your UI design knowledge.

---

## 0. Core Principles (from Practical UI)

Before diving into specific patterns, internalize these foundational principles:

### Minimize Usability Risks

Base design decisions on risk assessment—the risk that someone could have difficulty using an interface:

- Light grey text may look sleek but risks readability issues
- Icons without labels risk confusion about meaning
- Colored heading text risks being mistaken for links

**Always consider:** people with poor eyesight, low computer literacy, reduced dexterity, and cognitive differences.

### Have a Logical Reason for Every Design Detail

Every UI element should have a rationale. "That looks nice" is not constructive feedback. Be able to articulate *why* each design decision was made.

| Element | Logical Reason |
|---------|----------------|
| Left-aligned text | Creates neat edge, improves readability |
| Descriptive headings | Scannable, works with screen readers |
| Blue underlined links | Indicates interactivity, accessible for color blind |
| Grouped spacing | Related items closer together reduce cognitive load |

### Minimize Interaction Cost

Interaction cost = physical + mental effort to complete a task. Reduce it by:

1. **Keep related actions close** (Fitts's Law—closer/larger targets are faster to click)
2. **Reduce distractions** (avoid attention-grabbing elements that pull focus)
3. **Use progressive disclosure** (reveal complexity only when needed)

### Minimize Cognitive Load

Cognitive load is the mental effort required to use an interface. Reduce it by:

- Breaking information into smaller, digestible chunks
- Using familiar patterns people already understand
- Removing unnecessary elements and decisions
- Grouping related items visually

### Design System First

Create a system of reusable guidelines before designing:

- Color palette with usage rules
- Typography scale
- Spacing system
- Component patterns
- Interaction states

This ensures consistency and speeds up decision-making.

### Accessibility is Non-Negotiable

Meet **WCAG 2.1 Level AA** at minimum:

| Requirement | Minimum Ratio |
|-------------|---------------|
| Small text (≤18px) | 4.5:1 contrast |
| Large text (>18px bold or >24px) | 3:1 contrast |
| UI elements (borders, icons) | 3:1 contrast |

**Never rely on color alone**—always pair with icons, patterns, or text for color blind users.

### Use Common Design Patterns

Per Jakob's Law, stick with patterns people already know:

- Conventional form fields (not custom/unfamiliar styles)
- Standard navigation patterns
- Expected icon meanings
- Familiar button behaviors

Save creativity for your product's unique value proposition, not basic UI conventions.

### The 80/20 Rule

Roughly 80% of users use 20% of features. Prioritize the common paths:

- Optimize for frequent tasks, not edge cases
- Focus design effort where it has the largest impact
- Don't over-engineer rarely-used features

---

## 1. Starting from Scratch

### Start with a Feature, Not a Layout

Don't begin by designing the shell (navigation, sidebar, footer). Start with actual functionality.

**Wrong approach:**
- "Should it have a top nav or sidebar?"
- "Where should the logo go?"

**Right approach:**
- Design the core feature first (search form, product card, user profile)
- The navigation will reveal itself as you design features

### Detail Comes Later

In early stages, ignore typefaces, shadows, and icons. Use thick markers or low-fidelity wireframes to explore layouts quickly.

### Hold the Color

Design in grayscale first. This forces you to use spacing, contrast, and size to create hierarchy. Color comes later as enhancement.

### Work in Cycles

1. Design a simple version of the next feature
2. Build it
3. Iterate on the working design
4. Move to the next feature

### Be a Pessimist

Design the smallest useful version first. Don't design features you can't build yet—ship what works.

---

## 2. Hierarchy is Everything

### Not All Elements Are Equal

Visual hierarchy makes interfaces feel "designed". When everything competes for attention, nothing stands out.

**The key:** Deliberately de-emphasize secondary and tertiary information while highlighting what matters most.

### Size Isn't Everything

Don't rely solely on font size for hierarchy. Use:

| Technique | Effect |
|-----------|--------|
| **Font weight** | 600-700 for emphasis, 400-500 for normal |
| **Color contrast** | Dark for primary, grey for secondary, light grey for tertiary |
| **Spacing** | More space around important elements |

**Color guidelines for text:**
- Primary content: Dark color (e.g., `slate-900`)
- Secondary content: Medium grey (e.g., `slate-600`)
- Tertiary content: Light grey (e.g., `slate-400`)

### Don't Use Grey Text on Colored Backgrounds

Grey text on colored backgrounds looks washed out. Instead, pick a color with the same hue as the background, adjusting saturation and lightness.

```css
/* Bad: Grey on blue background */
background: hsl(220, 80%, 50%);
color: #888888; /* Looks dull */

/* Good: Tinted text matching background hue */
background: hsl(220, 80%, 50%);
color: hsl(220, 60%, 85%); /* Harmonious and readable */
```

### Emphasize by De-emphasizing

If a primary element doesn't stand out, don't make it louder—make competing elements quieter.

```css
/* Instead of making active nav item bolder... */
/* ...make inactive items softer */
.nav-item { color: var(--slate-400); }
.nav-item.active { color: var(--slate-900); }
```

### Labels Are a Last Resort

Context often eliminates the need for labels:

| Instead of | Use |
|------------|-----|
| "Email: john@example.com" | john@example.com (format is obvious) |
| "In stock: 12" | "12 left in stock" |
| "Bedrooms: 3" | "3 bedrooms" |

When labels are necessary, de-emphasize them—the data is what matters.

### Balance Weight and Contrast

Heavy elements (icons, bold text) can be de-emphasized with softer colors. Light elements (thin borders) can be emphasized with increased weight.

```css
/* Icon feels too heavy? Reduce contrast */
.icon { color: var(--slate-400); } /* Instead of slate-900 */

/* Border too subtle? Increase width */
border: 2px solid hsl(210, 23%, 95%); /* Instead of 1px darker */
```

### Button Hierarchy

Design buttons based on hierarchy, not just semantics:

| Type | Style | Use for |
|------|-------|---------|
| **Primary** | Solid, high contrast | Main action on page |
| **Secondary** | Outline or lower contrast | Less important actions |
| **Tertiary** | Link style | Seldom-used actions |

**Destructive actions** aren't automatically red and bold. If "Delete" isn't the primary action, style it as secondary or tertiary, then use bold red styling in the confirmation modal.

---

## 3. Layout and Spacing

### Start with Too Much White Space

Begin with excessive space, then remove until satisfied. This ensures elements breathe properly.

### Establish a Spacing System

Use a constrained scale with meaningful jumps (~25% between values):

```
4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px
```

**Base on 16px** (default browser font size, divides nicely).

### You Don't Have to Fill the Screen

If content only needs 600px, don't stretch it to 1200px. Extra space around edges never hurts.

### Shrink the Canvas

Designing for mobile first often reveals better solutions. Start with ~400px width, then expand.

### Grids Are Overrated

Not all elements should be fluid. Sidebars, icons, and avatars often work better with fixed sizes while main content flexes.

```css
/* Better than percentage-based sidebar */
.sidebar { width: 280px; flex-shrink: 0; }
.main { flex: 1; min-width: 0; }
```

### Relative Sizing Doesn't Scale

Headlines shouldn't stay proportional to body text across screen sizes. Large elements should shrink faster than small ones on mobile.

```css
/* Desktop: 45px headline, 18px body (2.5x ratio) */
/* Mobile: 24px headline, 14px body (1.7x ratio) */
```

### Avoid Ambiguous Spacing

When elements are grouped without visible separators, the spacing between groups must be greater than spacing within groups.

```css
/* Form labels should be closer to their inputs than to previous inputs */
.form-group { margin-bottom: 24px; }
.form-label { margin-bottom: 8px; }
```

---


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
