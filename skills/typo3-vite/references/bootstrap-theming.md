# Bootstrap Theming Guide

Standard approach for customizing Bootstrap 5.3+ in sitepackage projects.

## Theming Flow

```
Theme/_colors.scss          -> Project CI colors
Basic/_variables.scss       -> Bootstrap variable overrides
_global-basics.scss         -> Loads Bootstrap foundations with overrides
Vendor/_bootstrap.scss      -> Selective component imports
Theme/_theme-main.scss      -> Post-Bootstrap overrides
```

The order matters: variables must be defined before Bootstrap processes them.

## Essential Variables to Customize

### Colors

```scss
// Theme/_colors.scss
$color-primary: #0069b4;        // Main brand color
$color-secondary: #d1530f;      // Accent color
$color-tertiary: #6c757d;       // Optional third color

// Additional brand colors (project-specific)
$color-success: #198754;
$color-info: #0dcaf0;
$color-warning: #ffc107;
$color-danger: #dc3545;
```

```scss
// Basic/_variables.scss -- Map to Bootstrap
$primary: $color-primary;
$secondary: $color-secondary;

// Extend the Bootstrap color map
$custom-colors: (
    'tertiary': $color-tertiary,
);
```

### Typography

```scss
// Basic/_variables.scss
$font-family-base: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
$font-family-heading: $font-family-base;  // Or a different heading font

$font-size-base: 1rem;          // 16px
$font-size-sm: 0.875rem;        // 14px
$font-size-lg: 1.125rem;        // 18px

$font-weight-normal: 400;
$font-weight-bold: 700;

$line-height-base: 1.6;
$line-height-sm: 1.4;

$h1-font-size: 2.5rem;
$h2-font-size: 2rem;
$h3-font-size: 1.5rem;
$h4-font-size: 1.25rem;
$h5-font-size: 1.125rem;
$h6-font-size: 1rem;

$headings-font-weight: 700;
$headings-line-height: 1.2;
$headings-margin-bottom: 0.75rem;
```

### Spacing

```scss
$spacer: 1rem;
$spacers: (
    0: 0,
    1: $spacer * 0.25,     // 4px
    2: $spacer * 0.5,      // 8px
    3: $spacer,             // 16px
    4: $spacer * 1.5,       // 24px
    5: $spacer * 3,          // 48px
    6: $spacer * 5,          // 80px
);
```

### Grid and Layout

```scss
$grid-breakpoints: (
    xs: 0,
    sm: 576px,
    md: 768px,
    lg: 992px,
    xl: 1200px,
    xxl: 1400px,
);

$container-max-widths: (
    sm: 540px,
    md: 720px,
    lg: 960px,
    xl: 1140px,
    xxl: 1800px,           // Wide content for large screens
);

$grid-columns: 12;
$grid-gutter-width: 1.5rem;
```

### Buttons

```scss
$btn-padding-y: 0.625rem;
$btn-padding-x: 1.5rem;
$btn-font-size: 1rem;
$btn-font-weight: 600;
$btn-border-radius: 0.25rem;

$btn-padding-y-sm: 0.375rem;
$btn-padding-x-sm: 1rem;
$btn-padding-y-lg: 0.75rem;
$btn-padding-x-lg: 2rem;
```

### Forms

```scss
$input-padding-y: 0.625rem;
$input-padding-x: 0.75rem;
$input-font-size: 1rem;
$input-border-radius: 0.25rem;
$input-border-color: #ced4da;
$input-focus-border-color: $primary;
$input-focus-box-shadow: 0 0 0 0.2rem rgba($primary, 0.25);
```

### Cards

```scss
$card-border-radius: 0.5rem;
$card-border-color: rgba(0, 0, 0, 0.1);
$card-spacer-y: 1.25rem;
$card-spacer-x: 1.25rem;
$card-cap-padding-y: 0.75rem;
$card-cap-bg: transparent;
```

### Accordion

```scss
$accordion-padding-y: 1rem;
$accordion-padding-x: 1.25rem;
$accordion-border-color: rgba(0, 0, 0, 0.125);
$accordion-border-radius: 0.25rem;
$accordion-button-active-bg: $primary;
$accordion-button-active-color: #fff;
```

### Navigation

```scss
$navbar-padding-y: 0.75rem;
$navbar-padding-x: 1rem;
$nav-link-padding-y: 0.5rem;
$nav-link-padding-x: 1rem;
$nav-link-font-weight: 600;
$navbar-light-color: rgba(0, 0, 0, 0.7);
$navbar-light-hover-color: $primary;
$navbar-light-active-color: $primary;
```

### Focus and Accessibility

```scss
$focus-ring-width: 0.1875rem;
$focus-ring-opacity: 0.5;
$focus-ring-color: rgba($primary, $focus-ring-opacity);
```

### Transitions

```scss
$transition-base: all 0.2s ease-in-out;
$transition-fade: opacity 0.15s linear;
$transition-collapse: height 0.35s ease;
$transition-collapse-width: width 0.35s ease;
```

## Post-Bootstrap Overrides

For styles that need to override Bootstrap after its CSS is generated:

```scss
// Theme/_theme-main.scss

// Custom link styles
a {
    text-decoration: none;
    transition: color 0.2s ease;

    &:hover {
        text-decoration: underline;
    }
}

// Custom button variants
.btn-primary {
    &:hover {
        background-color: darken($primary, 10%);
    }
}

// Custom container padding
.container,
.container-fluid {
    padding-left: 1.5rem;
    padding-right: 1.5rem;

    @media (min-width: map-get($grid-breakpoints, lg)) {
        padding-left: 4.5rem;
        padding-right: 4.5rem;
    }
}
```

## Theme Checklist

When setting up a new project theme:

- [ ] CI colors defined in `Theme/_colors.scss`
- [ ] Colors mapped to Bootstrap variables in `Basic/_variables.scss`
- [ ] All color combinations meet WCAG AA contrast (4.5:1 text, 3:1 UI)
- [ ] Typography variables set (font family, sizes, weights)
- [ ] Local font files in `Resources/Public/Fonts/`
- [ ] `@font-face` declarations with `font-display: swap`
- [ ] Spacing scale defined
- [ ] Container max-widths adjusted
- [ ] Button and form styles customized
- [ ] Focus ring visible and uses primary color
- [ ] Only needed Bootstrap components imported in `Vendor/_bootstrap.scss`
