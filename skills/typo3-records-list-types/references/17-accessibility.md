# 17. Accessibility

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 17. Accessibility

- **Keyboard drag-and-drop**: Space/Enter to grab, arrows to move, Space/Enter to drop, Escape to cancel
- **ARIA live regions**: Announce drag state and position ("Position 3 of 12")
- **Semantic markup**: interactive card grids should use the ARIA grid pattern: `role="grid"` on the container, `role="row"` on row wrappers, and `role="gridcell"` on cards. `listbox` / `option` is wrong here because options must not contain separate interactive controls such as drag handles and action buttons.
- **Focus management**: Visible focus indicators, proper tab order
