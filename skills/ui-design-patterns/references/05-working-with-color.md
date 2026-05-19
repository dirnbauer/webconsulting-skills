# 5. Working with Color

Continues `ui-design-patterns` from [full guide](full-guide.md).

## 5. Working with Color

### Ditch Hex for HSL

HSL (Hue, Saturation, Lightness) makes color relationships intuitive:

```css
/* HSL is easier to reason about */
--primary-500: hsl(220, 80%, 50%);
--primary-600: hsl(220, 80%, 40%); /* Just darken lightness */
--primary-400: hsl(220, 80%, 60%); /* Just lighten */
```

### You Need More Colors Than You Think

A complete palette includes:

| Category | Shades Needed |
|----------|---------------|
| **Greys** | 8-10 shades (true black looks unnatural) |
| **Primary** | 5-10 shades |
| **Accent colors** | 5-10 shades each (red, yellow, green, etc.) |

### Define Shades Up Front

Don't use `lighten()` or `darken()` functions. Pre-define all shades:

1. Pick your **base** color (good for button backgrounds)
2. Pick your **darkest** shade (for text on light backgrounds)
3. Pick your **lightest** shade (for tinted backgrounds)
4. Fill in 6-7 shades between them

### Don't Let Lightness Kill Saturation

As lightness approaches 0% or 100%, increase saturation to maintain vibrancy.

### Perceived Brightness Varies by Hue

Yellow appears brighter than blue at the same lightness. To make a color lighter without washing it out, rotate hue toward yellow, cyan, or magenta. To darken, rotate toward red, green, or blue.

### Greys Don't Have to Be Grey

Saturate greys slightly for personality:
- **Cool greys**: Add blue (hue ~210)
- **Warm greys**: Add yellow/orange (hue ~40)

```css
--grey-500: hsl(210, 10%, 50%); /* Cool grey */
--grey-500-warm: hsl(40, 10%, 50%); /* Warm grey */
```

### Accessible Contrast

| Text Type | Minimum Ratio |
|-----------|---------------|
| Body text (<18px) | 4.5:1 |
| Large text (18px+ bold or 24px+) | 3:1 |

**Flip the contrast** when colored backgrounds make white text too dark—use dark colored text on light colored backgrounds instead.

### Don't Rely on Color Alone

Always pair color with another indicator (icons, patterns, text) for colorblind users.

### System Colors for Status

Use traffic light colors with familiar meanings:

| Color | Usage | When to Use |
|-------|-------|-------------|
| **Red** | Error | Negative messages, failures requiring attention |
| **Amber** | Warning | Caution, potentially risky actions |
| **Green** | Success | Positive messages, completed actions |

Always pair with icons for color blind accessibility.

### APCA: The Future of Contrast Measurement

WCAG 3 introduces the **Accessible Perceptual Contrast Algorithm (APCA)**—a more accurate contrast measurement:

| APCA Value | Use For |
|------------|---------|
| ≥90 | Preferred for body text (14px+) |
| ≥75 | Minimum for body text (18px+) |
| ≥60 | Other text (24px or 16px bold+) |
| ≥45 | Large text (36px or 24px bold+), UI elements |
| ≥30 | Placeholder text, disabled buttons |
| ≥15 | Non-text decorative elements |

**Key difference:** APCA handles dark backgrounds better than WCAG 2, and swapping text/background colors affects the score.

### Transparent Colors for Flexibility

Use transparent colors (with alpha values) for:

- Hover states that work on any background
- Overlays that adapt to underlying content
- Subtle backgrounds that maintain harmony

```css
/* Transparent overlays that work on any background */
--hover-overlay: hsla(0, 0%, 0%, 0.05);
--active-overlay: hsla(0, 0%, 0%, 0.1);
--disabled-overlay: hsla(0, 0%, 100%, 0.5);
```

---
