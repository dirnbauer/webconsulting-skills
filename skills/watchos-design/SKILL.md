---
name: watchos-design-guidelines
description: Apple Human Interface Guidelines for Apple Watch. Use when building watchOS apps, complications, or workout features. Triggers on tasks involving Watch UI, Digital Crown, glanceable interfaces, or wrist-based interactions.
version: 1.0.0
license: MIT
triggers:
  - watchos
  - apple watch
  - watch app
  - complications
  - digital crown
  - glanceable
  - workout app
  - wrist
---

# watchOS Design Guidelines

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Apple Human Interface Guidelines for AI agents.

Apple Watch is a personal, glanceable device worn on the wrist. Interactions are measured in seconds, not minutes. Every design decision must prioritize speed of comprehension and brevity of interaction.

---

## 1. Glanceable Design [CRITICAL]

The defining constraint of watchOS. If a user cannot extract the key information within 2 seconds of raising their wrist, the design has failed.

### Rules

- **W-GL-01**: Primary information must be visible without scrolling. The first screen is the only guaranteed screen.
- **W-GL-02**: Target interaction sessions of 5 seconds or less. Design for raise-glance-lower.
- **W-GL-03**: Use large, high-contrast text. Minimum effective body text is 16pt (system font). Titles should be 18pt or larger.
- **W-GL-04**: Limit text to essential content. Use SF Symbols instead of text labels where meaning is unambiguous.
- **W-GL-05**: Respect wrist-down time. When the wrist lowers, the app enters an inactive state.
- **W-GL-06**: Prioritize a single piece of information per screen.

### Screen Dimensions Reference

| Device | Screen Width | Screen Height | Corner Radius |
|--------|-------------|---------------|---------------|
| 41mm (Series 9/10) | 176px | 215px | 36px |
| 45mm (Series 9/10) | 198px | 242px | 39px |
| 49mm (Ultra 2) | 205px | 251px | 40px |

### Anti-Patterns

- Walls of text requiring scroll to understand context
- Small, dense data tables
- Requiring multiple taps before showing useful information

---

## 2. Digital Crown [HIGH]

The Digital Crown is the primary physical input for scrolling and precise value selection.

### Rules

- **W-DC-01**: Use the Digital Crown as the primary scroll mechanism for vertical content.
- **W-DC-02**: For value pickers (time, quantity, sliders), bind the Crown to precise adjustments with haptic detents.
- **W-DC-03**: Do not override or conflict with system Crown behaviors.
- **W-DC-04**: Provide visual feedback synchronized with Crown rotation.

### Anti-Patterns

- Ignoring the Crown and forcing all interaction through touch
- Missing haptic feedback on discrete value changes
- Laggy or batched responses to Crown rotation

---

## 3. Navigation [HIGH]

Watch navigation must be shallow and predictable.

### Rules

- **W-NV-01**: Use vertical page scrolling as the default content navigation pattern.
- **W-NV-02**: Use `TabView` for top-level sections (max 5 tabs). Swipe horizontally between tabs.
- **W-NV-03**: Use `NavigationStack` for hierarchical drill-down. Limit hierarchy to 2-3 levels maximum.
- **W-NV-04**: Avoid modal sheets for primary flows. Reserve for focused, single-purpose tasks.
- **W-NV-05**: The app's most important action should be reachable within 1 tap from launch.

### Navigation Pattern Reference

| Pattern | Use Case | Gesture |
|---------|----------|---------|
| Vertical scroll | Long-form content | Digital Crown / swipe up-down |
| TabView (horizontal pages) | Top-level app sections | Swipe left-right |
| NavigationStack (push/pop) | Hierarchical drill-down | Tap to push, swipe right to pop |
| Modal sheet | Confirmation, focused input | Dismiss via button or swipe down |

### Anti-Patterns

- Deep navigation hierarchies (4+ levels)
- Hamburger menus or hidden navigation drawers
- Tab bars with more than 5 items

---

## 4. Complications [HIGH]

Complications are the most visible surface of a Watch app. They live on the watch face and provide at-a-glance data.

### Rules

- **W-CP-01**: Support multiple complication families. At minimum support `circularSmall`, `graphicCorner`, and `graphicRectangular`.
- **W-CP-02**: Provide both tinted (single-color) and full-color variants.
- **W-CP-03**: Update complications via `TimelineProvider`. Keep data fresh.
- **W-CP-04**: Complication content must be meaningful without context. (e.g., "72°F" not "72").
- **W-CP-05**: Tapping a complication must launch the app to a relevant context.

### Complication Family Reference

| Family | Shape | Typical Content |
|--------|-------|-----------------|
| `circularSmall` | Small circle | Single value, icon, or gauge |
| `graphicCorner` | Curved, top corners | Gauge with label, or text with icon |
| `graphicCircular` | Larger circle | Gauge, icon with value, or stack |
| `graphicRectangular` | Wide rectangle | Multi-line text, chart, or detailed view |
| `graphicExtraLarge` | Full-width circle | Large gauge or prominent single value |

### Anti-Patterns

- Supporting only one complication family
- Stale data that does not update for hours
- Complication tap landing on generic app home instead of relevant content

---

## 5. Always On Display [MEDIUM]

When the user's wrist is down, watchOS enters an Always On state showing a dimmed version of the current app.

### Rules

- **W-AO-01**: Reduce visual complexity in the Always On state. Keep only the most critical information visible.
- **W-AO-02**: Hide sensitive or private data (e.g., message content, health details) in the dimmed state.
- **W-AO-03**: Reduce update frequency in Always On. Update no more than once per minute.
- **W-AO-04**: Use the system-provided dimming behaviors.
- **W-AO-05**: Test both active and Always On states. The transition must feel seamless.

### Anti-Patterns

- Showing identical UI in active and Always On states
- Animations or frequent updates in Always On state
- Forgetting to redact sensitive information

---

## 6. Workouts & Health [MEDIUM]

Workout and health apps have unique requirements: extended sessions, live metrics, and body-awareness features.

### Rules

- **W-WK-01**: Display live workout metrics in large, high-contrast text.
- **W-WK-02**: Use haptic feedback for milestones (lap completed, goal reached, heart rate zone change).
- **W-WK-03**: Support auto-pause detection for relevant workout types (running, walking).
- **W-WK-04**: Enable WaterLock during swimming workouts.
- **W-WK-05**: Show a clear summary screen at workout completion with key metrics.

### Anti-Patterns

- Small metric text that requires squinting
- Missing haptic feedback for important workout events
- Requiring complex interaction to end or save a workout

---

## 7. Notifications [MEDIUM]

Watch notifications must be brief and actionable. The user's wrist is raised for only a moment.

### Rules

- **W-NT-01**: Design Short Look notifications with only a title, app icon, and app name.
- **W-NT-02**: Design Long Look notifications with full content and up to 4 action buttons.
- **W-NT-03**: Use appropriate haptic notification types. Match the urgency.
- **W-NT-04**: Do not over-notify. Reserve Watch notifications for time-sensitive or actionable information.

### Haptic Type Reference

| Haptic | Use Case |
|--------|----------|
| `.notification` | General alerts |
| `.directionUp` | Positive event (goal reached, stock up) |
| `.directionDown` | Negative event (stock down, weather warning) |
| `.success` | Action completed successfully |
| `.failure` | Action failed |
| `.start` | Activity beginning |
| `.stop` | Activity ending |
| `.click` | Discrete selection (Crown detent, picker) |

### Anti-Patterns

- Sending every iPhone notification to the Watch
- Notifications without actionable buttons
- Using the same haptic type for all notifications

---

## Evaluation Checklist

### Glanceability
- [ ] Can the user understand the primary content within 2 seconds?
- [ ] Is the most important information visible without scrolling?
- [ ] Is body text at least 16pt with sufficient contrast?
- [ ] Are interactions completable in under 5 seconds?

### Digital Crown
- [ ] Does the Crown scroll vertical content?
- [ ] Do value pickers provide haptic detents?

### Navigation
- [ ] Is the primary action reachable within 1 tap from launch?
- [ ] Is the navigation hierarchy 3 levels or fewer?
- [ ] Does every pushed view have a back button?

### Complications
- [ ] Are multiple complication families supported?
- [ ] Do complications work in both tinted and full-color modes?
- [ ] Is complication data updated via TimelineProvider?
- [ ] Does tapping a complication open relevant context?

### Always On
- [ ] Is sensitive data hidden in the dimmed state?
- [ ] Is visual complexity reduced when inactive?
- [ ] Is the transition between active and dimmed seamless?

### Workouts
- [ ] Are live metrics displayed in large, high-contrast text?
- [ ] Are haptics used for milestones?
- [ ] Is auto-pause supported for applicable workout types?

### Notifications
- [ ] Is the Short Look meaningful (title + icon)?
- [ ] Does the Long Look include inline actions?
- [ ] Are haptic types matched to notification urgency?

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
