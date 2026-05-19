# 9. Forms and Buttons

Continues `ui-design-patterns` from [full guide](full-guide.md).

## 9. Forms and Buttons

### Button Weights

Define three distinct button styles based on importance:

| Weight | Style | Use For |
|--------|-------|---------|
| **Primary** | Solid, high contrast, brand color | Main action (one per screen) |
| **Secondary** | Outline or muted fill | Alternative actions |
| **Tertiary** | Text-only, link style | Least important actions |

### Form Field Best Practices

1. **Use conventional styles**—don't reinvent form fields
2. **Visible borders**—minimum 3:1 contrast ratio
3. **Clear focus states**—visible keyboard focus indicators
4. **Inline validation**—show errors as users type, not only on submit
5. **Helpful placeholders**—example input, not labels

### Form Layout

- **One column** for most forms (faster to complete)
- **Group related fields** with clear visual separation
- **Labels above inputs** (faster scanning than left-aligned labels)
- **Required field indicators**—mark optional fields, not required ones

### Avoid Disabled Buttons

Disabled buttons create confusion. Instead:

- Hide buttons until they're usable
- Show buttons but explain why action isn't available
- Use inline validation to guide users

```css
/* If you must use disabled buttons */
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

---
