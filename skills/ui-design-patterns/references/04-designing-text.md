# 4. Designing Text

Continues `ui-design-patterns` from [full guide](full-guide.md).

## 4. Designing Text

### Establish a Type Scale

Hand-pick sizes rather than using mathematical ratios:

```
12px, 14px, 16px, 18px, 20px, 24px, 30px, 36px, 48px, 60px, 72px
```

Use `px` or `rem`, not `em` (to avoid compounding issues with nesting).

### Use Good Fonts

**Safe choices:**
- System font stack for familiarity
- Fonts with 5+ weights indicate quality craftsmanship
- High x-height fonts for UI text (better legibility at small sizes)

**Filter by weight count** on Google Fonts to find quality options.

### Keep Line Length in Check

Optimal: **45-75 characters per line** (20-35em width).

```css
.prose { max-width: 65ch; } /* Character-based width */
```

### Baseline, Not Center

When mixing font sizes on one line, align by baseline, not vertical center.

```css
.header-row { align-items: baseline; } /* Not center */
```

### Line Height Is Proportional

| Font Size | Line Height |
|-----------|-------------|
| Small text (14px) | 1.5-1.75 |
| Body (16-18px) | 1.5-1.65 |
| Headlines (24px+) | 1.1-1.25 |
| Large headlines (36px+) | 1.0-1.1 |

Wider paragraphs need taller line heights.

### Not Every Link Needs a Color

In link-heavy interfaces, use subtle differentiation (font weight, darker color) instead of blue underlines everywhere. Reserve bold link styling for important navigation.

### Align with Readability in Mind

- **Left-align** most text
- **Center** only short, independent blocks (headings, CTAs)
- **Right-align** numbers in tables for easy comparison
- **Hyphenate** justified text

### Use Letter-Spacing Effectively

- **Tighten** headlines slightly: `letter-spacing: -0.02em;`
- **Widen** all-caps text: `letter-spacing: 0.05em;`
- Leave body text alone

---
