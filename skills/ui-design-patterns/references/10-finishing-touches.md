# 10. Finishing Touches

Continues `ui-design-patterns` from [full guide](full-guide.md).

## 10. Finishing Touches

### Supercharge the Defaults

| Default | Upgrade |
|---------|---------|
| Bullet points | Custom icons (checkmarks, locks, stars) |
| Quote marks | Large, colored quote symbols |
| Links | Bold, custom underline overlapping text |
| Checkboxes | Brand-colored custom controls |

### Add Color with Accent Borders

A 4px colored border adds polish without design skills:

```css
/* Top of cards */
.card { border-top: 4px solid var(--primary-500); }

/* Side of alerts */
.alert { border-left: 4px solid var(--warning-500); }

/* Under headlines */
.headline::after { 
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: var(--primary-500);
  margin-top: 12px;
}
```

### Decorate Backgrounds

Break monotony with:
- Subtle background color changes between sections
- Gradients (keep hues within 30° of each other)
- Low-contrast repeating patterns
- Simple geometric shapes or illustrations

### Don't Overlook Empty States

Empty states are first impressions. Include:
- Illustrations or icons
- Clear call-to-action
- Hide filters/tabs until content exists

### Use Fewer Borders

Instead of borders for separation:

| Alternative | When to Use |
|-------------|-------------|
| Box shadows | Outline elements on same-color backgrounds |
| Different background colors | Adjacent sections |
| Extra spacing | Group separation |

### Think Outside the Box

Challenge assumptions about component design:
- Dropdowns can have multiple columns, icons, and descriptions
- Tables can combine columns and add hierarchy
- Radio buttons can be selectable cards
- Forms can use creative layouts

---
