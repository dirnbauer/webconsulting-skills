---
name: ios-design-guidelines
description: Apple Human Interface Guidelines for iPhone. Use when building, reviewing, or refactoring SwiftUI/UIKit interfaces for iOS. Triggers on tasks involving iPhone UI, iOS components, accessibility, Dynamic Type, Dark Mode, or HIG compliance.
version: 1.0.0
license: MIT
triggers:
  - ios
  - iphone
  - swiftui
  - uikit
  - ios accessibility
  - dynamic type
  - ios dark mode
  - hig
  - human interface guidelines
---

# iOS Design Guidelines for iPhone

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Apple Human Interface Guidelines for AI agents.

Comprehensive rules derived from Apple's Human Interface Guidelines. Apply these when building, reviewing, or refactoring any iPhone app interface.

---

## 1. Layout & Safe Areas [CRITICAL]

### Rule 1.1: Minimum 44pt Touch Targets
All interactive elements must have a minimum tap target of 44x44 points.

```swift
Button("Save") { save() }
  .frame(minWidth: 44, minHeight: 44)
```

### Rule 1.2: Respect Safe Areas
Never place interactive or essential content under the status bar, Dynamic Island, or home indicator.

```swift
struct ContentView: View {
  var body: some View {
    VStack {
      Text("Content")
    }
    // SwiftUI respects safe areas by default
  }
}
```

Use `.ignoresSafeArea()` only for background fills, images, or decorative elements — never for text or interactive controls.

### Rule 1.3: Primary Actions in the Thumb Zone
Place primary actions at the bottom of the screen where the user's thumb naturally rests.

### Rule 1.4: Support All iPhone Screen Sizes
Design for iPhone SE (375pt wide) through iPhone Pro Max (430pt wide). Use flexible layouts, avoid hardcoded widths.

### Rule 1.5: 8pt Grid Alignment
Align spacing, padding, and element sizes to multiples of 8 points (8, 16, 24, 32, 40, 48).

---

## 2. Navigation [CRITICAL]

### Rule 2.1: Tab Bar for Top-Level Sections
Use a tab bar at the bottom of the screen for 3 to 5 top-level sections.

```swift
TabView {
  HomeView()
    .tabItem {
      Label("Home", systemImage: "house")
    }
  SearchView()
    .tabItem {
      Label("Search", systemImage: "magnifyingglass")
    }
  ProfileView()
    .tabItem {
      Label("Profile", systemImage: "person")
    }
}
```

### Rule 2.2: Never Use Hamburger Menus
Hamburger menus hide navigation, reduce discoverability, and violate iOS conventions. Use a tab bar instead.

### Rule 2.3: Large Titles in Primary Views
Use `.navigationBarTitleDisplayMode(.large)` for top-level views.

```swift
NavigationStack {
  List(items) { item in
    ItemRow(item: item)
  }
  .navigationTitle("Messages")
  .navigationBarTitleDisplayMode(.large)
}
```

### Rule 2.4: Never Override Back Swipe
The swipe-from-left-edge gesture for back navigation is a system-level expectation. Never attach custom gesture recognizers that interfere with it.

### Rule 2.5: Use NavigationStack for Hierarchical Content
Use `NavigationStack` (not the deprecated `NavigationView`) for drill-down content.

---

## 3. Typography & Dynamic Type [HIGH]

### Rule 3.1: Use Built-in Text Styles
Always use semantic text styles rather than hardcoded sizes. These scale automatically with Dynamic Type.

```swift
VStack(alignment: .leading, spacing: 4) {
  Text("Section Title")
    .font(.headline)
  Text("Body content that explains the section.")
    .font(.body)
  Text("Last updated 2 hours ago")
    .font(.caption)
    .foregroundStyle(.secondary)
}
```

### Rule 3.2: Support Dynamic Type Including Accessibility Sizes
Dynamic Type can scale text up to approximately 200% at the largest accessibility sizes. Layouts must reflow — never truncate or clip essential text.

```swift
@Environment(\.dynamicTypeSize) var dynamicTypeSize

var body: some View {
  if dynamicTypeSize.isAccessibilitySize {
    VStack { content }
  } else {
    HStack { content }
  }
}
```

### Rule 3.3: Custom Fonts Must Use UIFontMetrics
If you use a custom typeface, scale it with `UIFontMetrics` so it responds to Dynamic Type.

### Rule 3.5: Minimum 11pt Text
Never display text smaller than 11pt. Prefer 17pt for body text.

---

## 4. Color & Dark Mode [HIGH]

### Rule 4.1: Use Semantic System Colors
Use system-provided semantic colors that automatically adapt to light and dark modes.

```swift
Text("Primary text")
  .foregroundStyle(.primary) // Adapts to light/dark

Text("Secondary info")
  .foregroundStyle(.secondary)

VStack { }
  .background(Color(.systemBackground)) // White in light, black in dark
```

### Rule 4.2: Provide Light and Dark Variants for Custom Colors
Define custom colors in the asset catalog with both Any Appearance and Dark Appearance variants.

### Rule 4.3: Never Rely on Color Alone
Always pair color with text, icons, or shapes to convey meaning. Approximately 8% of men have some form of color vision deficiency.

```swift
HStack {
  Image(systemName: "exclamationmark.triangle.fill")
    .foregroundStyle(.red)
  Text("Error: Invalid email address")
    .foregroundStyle(.red)
}
```

### Rule 4.4: 4.5:1 Contrast Ratio Minimum
All text must meet WCAG AA contrast ratios: 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt+ bold).

### Rule 4.7: One Accent Color for Interactive Elements
Choose a single tint/accent color for all interactive elements (buttons, links, toggles).

```swift
@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
        .tint(.indigo) // All interactive elements use indigo
    }
  }
}
```

---

## 5. Accessibility [CRITICAL]

### Rule 5.1: VoiceOver Labels on All Interactive Elements
Every button, control, and interactive element must have a meaningful accessibility label.

```swift
Button(action: addToCart) {
  Image(systemName: "cart.badge.plus")
}
.accessibilityLabel("Add to cart")
```

### Rule 5.2: Logical VoiceOver Navigation Order
Use `.accessibilitySortPriority()` to adjust when the visual layout doesn't match the reading order.

### Rule 5.3: Support Bold Text
When the user enables Bold Text in Settings, use the `.bold` dynamic type variants.

### Rule 5.4: Support Reduce Motion
Disable decorative animations and parallax when Reduce Motion is enabled.

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

var body: some View {
  CardView()
    .animation(reduceMotion ? nil : .spring(), value: isExpanded)
}
```

---

## 6. Gestures & Input [HIGH]

### Rule 6.1: Use Standard Gestures

| Gesture | Standard Use |
|---------|-------------|
| Tap | Primary action, selection |
| Long press | Context menu, preview |
| Swipe horizontal | Delete, archive, navigate back |
| Swipe vertical | Scroll, dismiss sheet |
| Pinch | Zoom in/out |

### Rule 6.2: Never Override System Gestures
These gestures are reserved by the system:
- Swipe from left edge (back navigation)
- Swipe down from top-left (Notification Center)
- Swipe down from top-right (Control Center)
- Swipe up from bottom (home / app switcher)

---

## 7. Components [HIGH]

### Rule 7.1: Button Styles
- `.borderedProminent` — primary call-to-action
- `.bordered` — secondary actions
- `.borderless` — tertiary or inline actions
- `.destructive` role — red tint for delete/remove

```swift
VStack(spacing: 16) {
  Button("Purchase") { buy() }
    .buttonStyle(.borderedProminent)

  Button("Add to Wishlist") { wishlist() }
    .buttonStyle(.bordered)

  Button("Delete", role: .destructive) { delete() }
}
```

### Rule 7.2: Alerts — Critical Info Only
Use alerts sparingly for critical information that requires a decision. Prefer 2 buttons; maximum 3.

### Rule 7.3: Sheets for Scoped Tasks
Present sheets for self-contained tasks. Always provide a way to dismiss.

```swift
.sheet(isPresented: $showCompose) {
  NavigationStack {
    ComposeView()
      .navigationTitle("New Message")
      .toolbar {
        ToolbarItem(placement: .cancellationAction) {
          Button("Cancel") { showCompose = false }
        }
        ToolbarItem(placement: .confirmationAction) {
          Button("Send") { send() }
        }
      }
  }
  .presentationDetents([.medium, .large])
}
```

### Rule 7.4: Lists — Inset Grouped Default
Use the `.insetGrouped` list style as the default. Support swipe actions for common operations.

---

## 8. Patterns [MEDIUM]

### Rule 8.1: Onboarding — Max 3 Pages, Skippable
Keep onboarding to 3 or fewer pages. Always provide a skip option.

### Rule 8.2: Loading — Skeleton Views, No Blocking Spinners
Use skeleton/placeholder views that match the layout of the content being loaded.

```swift
if isLoading {
  ForEach(0..<5) { _ in
    SkeletonRow()
      .redacted(reason: .placeholder)
  }
} else {
  ForEach(items) { item in
    ItemRow(item: item)
  }
}
```

### Rule 8.3: Launch Screen — Match First Screen
The launch storyboard must visually match the initial screen of the app. No splash logos, no branding screens.

### Rule 8.7: Feedback — Visual + Haptic
Provide immediate feedback for every user action with visual state change and haptic feedback.

```swift
Button("Complete") {
  let generator = UINotificationFeedbackGenerator()
  generator.notificationOccurred(.success)
  completeTask()
}
```

---

## 9. Privacy & Permissions [HIGH]

### Rule 9.1: Request Permissions in Context
Request a permission at the moment the user takes an action that needs it — never at app launch.

### Rule 9.2: Explain Before System Prompt
Show a custom explanation screen before triggering the system permission dialog.

### Rule 9.3: Support Sign in with Apple
If the app offers any third-party sign-in, it must also offer Sign in with Apple.

### Rule 9.4: Don't Require Accounts Unless Necessary
Let users explore the app before requiring sign-in.

---

## Quick Reference

| Need | Component | Notes |
|------|-----------|-------|
| Top-level sections (3-5) | `TabView` with `.tabItem` | Bottom tab bar, SF Symbols |
| Hierarchical drill-down | `NavigationStack` | Large title on root, inline on children |
| Self-contained task | `.sheet` | Swipe to dismiss, cancel/done buttons |
| Critical decision | `.alert` | 2 buttons preferred, max 3 |
| Secondary actions | `.contextMenu` | Long press; must also be accessible elsewhere |
| Scrolling content | `List` with `.insetGrouped` | 44pt min row, swipe actions |
| Progress (known) | `ProgressView(value:total:)` | Show percentage or time remaining |
| Progress (unknown) | `ProgressView()` | Inline, never full-screen blocking |
| Haptic feedback | `UIImpactFeedbackGenerator` | `.light`, `.medium`, `.heavy` |
| Destructive action | `Button(role: .destructive)` | Red tint, confirm via alert |

---

## Evaluation Checklist

### Layout & Safe Areas
- [ ] All touch targets are at least 44x44pt
- [ ] No content is clipped under status bar, Dynamic Island, or home indicator
- [ ] Primary actions are in the bottom half of the screen (thumb zone)
- [ ] Layout adapts from iPhone SE to Pro Max without breaking

### Navigation
- [ ] Tab bar is used for 3-5 top-level sections
- [ ] No hamburger/drawer menus
- [ ] Primary views use large titles
- [ ] Swipe-from-left-edge back navigation works throughout

### Typography
- [ ] All text uses built-in text styles or `UIFontMetrics`-scaled custom fonts
- [ ] Dynamic Type is supported up to accessibility sizes
- [ ] Minimum text size is 11pt

### Color & Dark Mode
- [ ] App uses semantic system colors or provides light/dark asset variants
- [ ] No information conveyed by color alone
- [ ] Text contrast meets 4.5:1 (normal) or 3:1 (large)

### Accessibility
- [ ] VoiceOver reads all screens logically with meaningful labels
- [ ] Bold Text preference is respected
- [ ] Reduce Motion disables decorative animations
- [ ] All gestures have alternative access paths

---

## Anti-Patterns

1. **Hamburger menus** — Use a tab bar. Hamburger menus hide navigation.

2. **Custom back buttons that break swipe-back** — Ensure the swipe-from-left-edge gesture still works.

3. **Full-screen blocking spinners** — Use skeleton views or inline progress indicators.

4. **Splash screens with logos** — The launch screen must mirror the first screen of the app.

5. **Requesting all permissions at launch** — Ask in context when needed.

6. **Hardcoded font sizes** — Use text styles. Hardcoded sizes ignore Dynamic Type.

7. **Using only color to indicate state** — Always pair with icons or text.

8. **Alerts for non-critical information** — Use banners or inline messages.

9. **Hiding the tab bar on push** — Tab bars should remain visible throughout navigation.

10. **Ignoring safe areas** — Content will disappear under the notch or Dynamic Island.

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
