---
name: ipados-design
description: >-
  Apple Human Interface Guidelines for iPad. Use when building iPad-optimized interfaces,
  implementing multitasking, pointer support, keyboard shortcuts, or responsive layouts.
  Triggers on tasks involving iPad, Split View, Stage Manager, sidebar navigation, or
  trackpad support.
license: MIT
metadata:
  version: "1.0.0"
---

# iPadOS Design Guidelines

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Apple Human Interface Guidelines for AI agents.

Comprehensive rules for building iPad-native apps following Apple's Human Interface Guidelines. iPad is not a big iPhone -- it demands adaptive layouts, multitasking support, pointer interactions, keyboard shortcuts, and inter-app drag and drop.

---

## 1. Responsive Layout [CRITICAL]

### 1.1 Use Adaptive Size Classes

iPad presents two horizontal size classes: **regular** (full screen, large splits) and **compact** (Slide Over, narrow splits). Design for both.

```swift
struct AdaptiveView: View {
  @Environment(\.horizontalSizeClass) var sizeClass

  var body: some View {
    if sizeClass == .regular {
      TwoColumnLayout()
    } else {
      StackedLayout()
    }
  }
}
```

### 1.2 Don't Scale Up iPhone UI

iPad layouts must be purpose-built. Stretching an iPhone layout across a 13" display wastes space. Use multi-column layouts, master-detail patterns, and increased information density in regular width.

### 1.3 Support All iPad Screen Sizes

Design for the full range: iPad Mini (8.3"), iPad (10.9"), iPad Air (11"/13"), and iPad Pro (11"/13").

### 1.4 Column-Based Layouts for Regular Width

In regular width, organize content into columns. Two-column is the most common (sidebar + detail). Three-column works for deep hierarchies.

```swift
struct ThreeColumnLayout: View {
  var body: some View {
    NavigationSplitView {
      SidebarView()
    } content: {
      ContentListView()
    } detail: {
      DetailView()
    }
  }
}
```

---

## 2. Multitasking [CRITICAL]

### 2.1 Support Split View

Your app must function correctly at 1/3, 1/2, and 2/3 screen widths in Split View. At 1/3 width, your app receives compact horizontal size class.

### 2.2 Support Slide Over

Slide Over presents your app as a compact-width overlay on the right edge. Ensure all functionality remains accessible in this narrow mode.

### 2.3 Handle Stage Manager

Stage Manager allows freely resizable windows and multiple windows simultaneously. Your app must:
- Resize fluidly to arbitrary dimensions
- Support multiple scenes (windows) showing different content
- Not assume any fixed size or aspect ratio

```swift
@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
    WindowGroup("Detail", for: Item.ID.self) { $itemId in
      DetailView(itemId: itemId)
    }
  }
}
```

### 2.4 Never Assume Full Screen

The app may launch directly into Split View or Stage Manager. Do not depend on full-screen dimensions during setup or onboarding.

### 2.5 Support Multiple Scenes

Use `UIScene` / SwiftUI `WindowGroup` to let users open multiple instances of your app showing different content.

---

## 3. Navigation [HIGH]

### 3.1 Sidebar for Primary Navigation

In regular width, replace the iPhone tab bar with a sidebar.

```swift
struct AppNavigation: View {
  @State private var selection: NavigationItem? = .inbox

  var body: some View {
    NavigationSplitView {
      List(selection: $selection) {
        Section("Main") {
          Label("Inbox", systemImage: "tray")
            .tag(NavigationItem.inbox)
          Label("Drafts", systemImage: "doc")
            .tag(NavigationItem.drafts)
          Label("Sent", systemImage: "paperplane")
            .tag(NavigationItem.sent)
        }
      }
      .navigationTitle("Mail")
    } detail: {
      DetailView(for: selection)
    }
  }
}
```

### 3.2 Automatic Tab-to-Sidebar Conversion

SwiftUI `TabView` with `.sidebarAdaptable` style automatically converts to a sidebar in regular width.

```swift
TabView {
  Tab("Home", systemImage: "house") { HomeView() }
  Tab("Search", systemImage: "magnifyingglass") { SearchView() }
  Tab("Profile", systemImage: "person") { ProfileView() }
}
.tabViewStyle(.sidebarAdaptable)
```

### 3.3 Toolbar at Top

On iPad, toolbars live at the top of the screen in the navigation bar area, not at the bottom like iPhone.

```swift
.toolbar {
  ToolbarItemGroup(placement: .primaryAction) {
    Button("Compose", systemImage: "square.and.pencil") { }
  }
  ToolbarItemGroup(placement: .secondaryAction) {
    Button("Archive", systemImage: "archivebox") { }
    Button("Delete", systemImage: "trash") { }
  }
}
```

### 3.4 Detail View Should Never Be Empty

When no item is selected in a list/sidebar, show a meaningful empty state in the detail area.

---

## 4. Pointer & Trackpad [HIGH]

### 4.1 Add Hover Effects to Interactive Elements

All tappable elements should respond to pointer hover.

```swift
Button("Action") { }
  .hoverEffect(.highlight) // Subtle highlight on hover

MyCustomView()
  .hoverEffect(.lift) // Lifts and adds shadow
```

### 4.2 Pointer Magnetism on Buttons

The pointer should snap to button bounds. Standard UIKit/SwiftUI buttons get this automatically.

### 4.3 Support Right-Click Context Menus

Right-click (secondary click) should present context menus. Use `.contextMenu` which automatically supports both long-press (touch) and right-click (pointer).

```swift
Text(item.title)
  .contextMenu {
    Button("Copy", systemImage: "doc.on.doc") { }
    Button("Share", systemImage: "square.and.arrow.up") { }
    Divider()
    Button("Delete", systemImage: "trash", role: .destructive) { }
  }
```

### 4.4 Customize Cursor for Content Areas

Change cursor appearance based on context. Text areas show I-beam. Links show pointer hand.

---

## 5. Keyboard [HIGH]

### 5.1 Cmd+Key Shortcuts for All Major Actions

Every primary action must have a keyboard shortcut.

| Shortcut | Action |
|----------|--------|
| Cmd+N | New item |
| Cmd+F | Find/Search |
| Cmd+S | Save |
| Cmd+Z | Undo |
| Cmd+Shift+Z | Redo |
| Cmd+C/V/X | Copy/Paste/Cut |
| Cmd+A | Select all |
| Cmd+, | Settings/Preferences |
| Delete | Delete selected item |

```swift
Button("New Document") { createDocument() }
  .keyboardShortcut("n", modifiers: .command)
```

### 5.2 Discoverability via Cmd-Hold Overlay

When the user holds the Cmd key, iPadOS shows a shortcut overlay. Register all shortcuts using `.keyboardShortcut()`.

### 5.3 Tab Key Navigation Between Fields

Support Tab to move forward and Shift+Tab to move backward between form fields.

```swift
struct FormView: View {
  @FocusState private var focusedField: Field?

  var body: some View {
    Form {
      TextField("Name", text: $name)
        .focused($focusedField, equals: .name)
      TextField("Email", text: $email)
        .focused($focusedField, equals: .email)
    }
  }
}
```

### 5.4 Never Override System Shortcuts

Do not claim Cmd+H (Home), Cmd+Tab (App Switcher), Cmd+Space (Spotlight), or Globe key combinations.

---

## 6. Apple Pencil [MEDIUM]

### 6.1 Support Scribble

iPadOS converts handwriting to text in any standard text field automatically. Do not disable Scribble.

### 6.2 Double-Tap Tool Switching

Apple Pencil 2 and later supports double-tap to switch tools. Implement the `UIPencilInteraction` delegate.

### 6.3 Pressure and Tilt for Drawing

For drawing apps, respond to `force` (pressure) and `altitudeAngle`/`azimuthAngle` (tilt).

### 6.4 Hover Detection (M2+ Pencil)

Apple Pencil with hover provides position data before the pencil touches the screen.

### 6.5 PencilKit Integration

For note-taking and annotation, use `PKCanvasView` from PencilKit.

```swift
import PencilKit

struct DrawingView: UIViewRepresentable {
  @Binding var canvasView: PKCanvasView

  func makeUIView(context: Context) -> PKCanvasView {
    canvasView.tool = PKInkingTool(.pen, color: .black, width: 5)
    canvasView.drawingPolicy = .anyInput
    return canvasView
  }
}
```

---

## 7. Drag and Drop [HIGH]

### 7.1 Inter-App Drag and Drop is Expected

iPad users expect to drag content between apps. Support dragging content out and dropping content in.

```swift
// As drag source
Text(item.title)
  .draggable(item.title)

// As drop destination
DropTarget()
  .dropDestination(for: String.self) { items, location in
    handleDrop(items)
    return true
  }
```

### 7.2 Multi-Item Drag

Users can pick up one item, then tap additional items to add them to the drag. Support multi-item drag.

### 7.3 Spring-Loaded Interactions

When dragging over a navigation element, pause briefly to "spring open" that destination.

### 7.4 Visual Feedback for Drag and Drop

Provide clear visual states: lift, move, drop, and cancel animations.

---

## Evaluation Checklist

### Layout & Multitasking
- [ ] App uses adaptive layout with `horizontalSizeClass`
- [ ] Tested at all Split View ratios (1/3, 1/2, 2/3)
- [ ] Tested in Slide Over (compact width)
- [ ] Stage Manager: resizes fluidly to arbitrary dimensions
- [ ] Multiple scenes/windows supported
- [ ] Both orientations (portrait and landscape) work correctly

### Navigation
- [ ] Sidebar visible in regular width
- [ ] Tab bar used in compact width
- [ ] Detail view shows placeholder when no selection
- [ ] Toolbar items placed at top, not bottom

### Pointer & Trackpad
- [ ] Hover effects on all interactive elements
- [ ] Right-click context menus available
- [ ] Click-and-drag works for reordering

### Keyboard
- [ ] Cmd+key shortcuts for all major actions
- [ ] Shortcuts appear in Cmd-hold overlay
- [ ] Tab key navigates between form fields
- [ ] No system shortcut conflicts

### Apple Pencil
- [ ] Scribble works in all text fields
- [ ] Drawing apps support pressure and tilt

### Drag and Drop
- [ ] Content can be dragged out to other apps
- [ ] Content can be dropped in from other apps
- [ ] Multi-item drag supported

---

## Anti-Patterns

### DO NOT: Scale Up iPhone Layouts
Stretching a single-column iPhone UI to fill an iPad screen wastes space. Always redesign for the larger canvas.

### DO NOT: Disable Multitasking
Never opt out of multitasking support. Users expect every app to work in Split View and Slide Over.

### DO NOT: Ignore the Keyboard
An app with no keyboard shortcuts forces users to reach for the screen constantly.

### DO NOT: Use iPhone-Style Bottom Tab Bars in Regular Width
Tab bars at the bottom waste vertical space on iPad. Convert to sidebar navigation in regular width.

### DO NOT: Show Popovers as Full-Screen Sheets
On iPad, popovers should anchor to their source element as floating panels.

### DO NOT: Ignore Pointer Hover States
Missing hover effects make the app feel broken when using a trackpad.

### DO NOT: Forget Drag and Drop
On iPad, drag and drop between apps is a core workflow.

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
