# 6. Creating Depth

Continues `ui-design-patterns` from [full guide](full-guide.md).

## 6. Creating Depth

### Emulate a Light Source

Light comes from above. Apply this consistently:

- **Raised elements**: Lighter top edge, shadow below
- **Inset elements**: Shadow at top, lighter bottom edge

```css
/* Raised button */
.button {
  box-shadow: 
    inset 0 1px 0 hsl(220, 80%, 70%), /* Light top edge */
    0 1px 3px hsla(0, 0%, 0%, 0.2);    /* Shadow below */
}

/* Inset input */
.input {
  box-shadow: inset 0 2px 4px hsla(0, 0%, 0%, 0.1);
}
```

### Use Shadows to Convey Elevation

| Elevation | Shadow | Use for |
|-----------|--------|---------|
| Low | `0 1px 3px rgba(0,0,0,0.12)` | Buttons, cards |
| Medium | `0 4px 6px rgba(0,0,0,0.1)` | Dropdowns, popovers |
| High | `0 15px 35px rgba(0,0,0,0.15)` | Modals, dialogs |

Define 5 shadow levels and stick to them.

### Shadows Can Have Two Parts

Combine a large soft shadow (direct light) with a small tight shadow (ambient occlusion):

```css
box-shadow: 
  0 4px 6px rgba(0, 0, 0, 0.07),   /* Large, soft */
  0 1px 3px rgba(0, 0, 0, 0.1);    /* Small, tight */
```

The tight shadow fades at higher elevations.

### Flat Designs Can Have Depth

Without shadows:
- Use **lighter colors** for raised elements
- Use **darker colors** for inset elements
- Use **solid offset shadows** (no blur) for flat aesthetic with depth

### Overlap Elements to Create Layers

Let cards cross background boundaries. Overlap images with invisible borders to prevent clashing.

---
