# 7. Working with Images

Continues `ui-design-patterns` from [full guide](full-guide.md).

## 7. Working with Images

### Use Good Photos

Bad photos ruin designs. Hire professionals or use quality stock (Unsplash, etc.). Don't use smartphone placeholders.

### Text on Images Needs Consistent Contrast

When placing text over images:

1. **Add overlay**: Semi-transparent black (for light text) or white (for dark text)
2. **Lower contrast**: Reduce image contrast, adjust brightness
3. **Colorize**: Desaturate + multiply blend with brand color
4. **Text shadow**: Large blur radius, no offset (glow effect)

### Everything Has an Intended Size

- **Don't scale up icons** designed for 16-24px—they look chunky
- **Don't scale down screenshots**—details become illegible
- **Redraw logos** for small sizes (favicons)

Wrap small icons in colored shapes to fill larger spaces:

```html
<div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
  <svg class="w-6 h-6 text-blue-600"><!-- Icon --></svg>
</div>
```

### User-Uploaded Content

- Force consistent aspect ratios with `object-fit: cover`
- Prevent background bleed with subtle inner shadows
- Control dimensions with fixed containers

```css
.user-image {
  object-fit: cover;
  aspect-ratio: 16/9;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);
}
```

---
