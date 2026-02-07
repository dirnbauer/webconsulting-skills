---
name: macos-design-guidelines
description: Apple Human Interface Guidelines for Mac. Use when building macOS apps with SwiftUI or AppKit, implementing menu bars, toolbars, window management, or keyboard shortcuts. Triggers on tasks involving Mac UI, desktop apps, or Mac Catalyst.
version: 1.0.0
license: MIT
triggers:
  - macos
  - mac app
  - appkit
  - swiftui mac
  - mac catalyst
  - menu bar
  - toolbar
  - window management
  - mac keyboard shortcuts
---

# macOS Human Interface Guidelines

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Apple Human Interface Guidelines for AI agents.

Mac apps serve power users who expect deep keyboard control, persistent menu bars, resizable multi-window layouts, and tight system integration.

---

## 1. Menu Bar [CRITICAL]

Every Mac app must have a menu bar. It is the primary discovery mechanism for commands.

### Rule 1.1 — Provide Standard Menus

Every app must include at minimum: **App**, **File**, **Edit**, **View**, **Window**, **Help**.

```swift
@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
    .commands {
      CommandGroup(after: .newItem) {
        Button("New from Template...") { newFromTemplate() }
          .keyboardShortcut("T", modifiers: [.command, .shift])
      }
      CommandMenu("Canvas") {
        Button("Zoom to Fit") { zoomToFit() }
          .keyboardShortcut("0", modifiers: .command)
      }
    }
  }
}
```

### Rule 1.2 — Keyboard Shortcuts for All Menu Items

Every menu item that performs an action must have a keyboard shortcut.

**Standard Shortcut Reference:**

| Action | Shortcut |
|--------|----------|
| New | Cmd+N |
| Open | Cmd+O |
| Close | Cmd+W |
| Save | Cmd+S |
| Save As | Cmd+Shift+S |
| Print | Cmd+P |
| Undo | Cmd+Z |
| Redo | Cmd+Shift+Z |
| Cut | Cmd+X |
| Copy | Cmd+C |
| Paste | Cmd+V |
| Select All | Cmd+A |
| Find | Cmd+F |
| Preferences/Settings | Cmd+, |
| Quit | Cmd+Q |

### Rule 1.3 — Dynamic Menu Updates

Menu items must reflect current state. Disable items that are not applicable. Update titles to match context.

### Rule 1.4 — Contextual Menus

Provide right-click context menus on all interactive elements.

```swift
Text(item.name)
  .contextMenu {
    Button("Rename...") { rename(item) }
    Button("Duplicate") { duplicate(item) }
    Divider()
    Button("Delete", role: .destructive) { delete(item) }
  }
```

---

## 2. Windows [CRITICAL]

Mac users expect full control over window size, position, and lifecycle.

### Rule 2.1 — Resizable with Sensible Minimums

All main windows must be freely resizable. Set a minimum size that keeps the UI usable.

```swift
WindowGroup {
  ContentView()
    .frame(minWidth: 600, minHeight: 400)
}
.defaultSize(width: 900, height: 600)
```

### Rule 2.2 — Support Fullscreen and Split View

Opt into native fullscreen. The green traffic-light button must work.

### Rule 2.3 — Multiple Windows

Support multiple windows. Document-based apps must allow multiple documents open simultaneously.

```swift
@main
struct TextEditorApp: App {
  var body: some Scene {
    DocumentGroup(newDocument: TextDocument()) { file in
      TextEditorView(document: file.$document)
    }
  }
}
```

### Rule 2.4 — Title Bar Shows Document Info

For document-based apps, the title bar must show the document name. Support proxy icon dragging.

### Rule 2.5 — Remember Window State

Persist window position, size, and state across launches.

### Rule 2.6 — Traffic Light Buttons

Never hide or reposition the close, minimize, or zoom buttons.

---

## 3. Toolbars [HIGH]

Toolbars are the secondary command surface after the menu bar.

### Rule 3.1 — Unified Title Bar and Toolbar

Use the unified title bar + toolbar style for a modern appearance.

```swift
WindowGroup {
  ContentView()
    .toolbar {
      ToolbarItem(placement: .primaryAction) {
        Button(action: compose) {
          Label("Compose", systemImage: "square.and.pencil")
        }
      }
    }
}
.windowToolbarStyle(.unified)
```

### Rule 3.2 — User-Customizable Toolbars

Allow users to add, remove, and rearrange toolbar items.

```swift
.toolbar(id: "main") {
  ToolbarItem(id: "compose", placement: .primaryAction) {
    Button(action: compose) {
      Label("Compose", systemImage: "square.and.pencil")
    }
  }
}
.toolbarRole(.editor)
```

### Rule 3.3 — Search Field in Toolbar

Place the search field in the trailing area of the toolbar.

```swift
NavigationSplitView {
  SidebarView()
} detail: {
  ContentListView()
    .searchable(text: $searchText, placement: .toolbar, prompt: "Search items")
}
```

---

## 4. Sidebars [HIGH]

Sidebars are the primary navigation surface for Mac apps.

### Rule 4.1 — Leading Edge, Collapsible

Place the sidebar on the left edge. Make it collapsible via the toolbar button or Cmd+Ctrl+S.

```swift
NavigationSplitView(columnVisibility: $columnVisibility) {
  List(selection: $selection) {
    Section("Library") {
      Label("All Items", systemImage: "tray.full")
      Label("Favorites", systemImage: "star")
      Label("Recent", systemImage: "clock")
    }
  }
  .navigationSplitViewColumnWidth(min: 180, ideal: 220, max: 320)
} detail: {
  DetailView(selection: selection)
}
.navigationSplitViewStyle(.prominentDetail)
```

### Rule 4.2 — Source List Style

Use the source list style (`.listStyle(.sidebar)`) for content-library navigation.

### Rule 4.3 — Badge Counts

Show badge counts on sidebar items for unread counts.

```swift
Label("Inbox", systemImage: "tray")
  .badge(unreadCount)
```

---

## 5. Keyboard [CRITICAL]

Mac users rely on keyboard shortcuts more than any other platform.

### Rule 5.1 — Cmd Shortcuts for Everything

Every action reachable by mouse must have a keyboard equivalent.

| Modifier Pattern | Usage |
|-----------------|-------|
| Cmd+letter | Primary actions |
| Cmd+Shift+letter | Variant of primary |
| Cmd+Option+letter | Alternative mode |
| Cmd+Ctrl+letter | Window/view controls |

### Rule 5.2 — Full Keyboard Navigation

Support Tab to move between controls. Support arrow keys within lists, grids, and tables.

### Rule 5.3 — Escape to Cancel or Close

Esc must dismiss popovers, sheets, dialogs, and cancel in-progress operations.

### Rule 5.4 — Return for Default Action

In dialogs and forms, Return/Enter activates the default button.

```swift
Button("Save") { save() }
  .keyboardShortcut(.defaultAction)

Button("Cancel") { cancel() }
  .keyboardShortcut(.cancelAction)
```

### Rule 5.5 — Delete for Removal

The Delete key must remove selected items in lists, tables, and collections.

### Rule 5.6 — Space for Quick Look

Space bar should invoke Quick Look for items that support previewing.

---

## 6. Pointer and Mouse [HIGH]

### Rule 6.1 — Hover States

All interactive elements must have a visible hover state.

```swift
struct HoverableRow: View {
  @State private var isHovered = false

  var body: some View {
    HStack {
      Text(item.name)
      Spacer()
      if isHovered {
        Button("Edit") { edit() }
          .buttonStyle(.borderless)
      }
    }
    .padding(8)
    .background(isHovered ? Color.primary.opacity(0.05) : .clear)
    .cornerRadius(6)
    .onHover { hovering in isHovered = hovering }
  }
}
```

### Rule 6.2 — Right-Click Context Menus

Every interactive element must respond to right-click with a contextual menu.

### Rule 6.3 — Drag and Drop

Support drag and drop for content manipulation.

```swift
ForEach(items) { item in
  ItemView(item: item)
    .draggable(item)
}
.dropDestination(for: Item.self) { items, location in
  handleDrop(items, at: location)
  return true
}
```

### Rule 6.6 — Multi-Selection

Support Cmd+Click for non-contiguous selection and Shift+Click for range selection.

---

## 7. Visual Design [HIGH]

### Rule 9.1 — Use System Fonts

Use SF Pro (the system font) at standard dynamic type sizes.

```swift
Text("Title").font(.title)
Text("Headline").font(.headline)
Text("Body text").font(.body)
Text("let x = 42").font(.system(.body, design: .monospaced))
```

### Rule 9.2 — Vibrancy and Materials

Use system materials for sidebar and toolbar backgrounds.

```swift
List { ... }
  .listStyle(.sidebar) // Automatic vibrancy
```

### Rule 9.3 — Respect System Accent Color

Use the system accent color for selection and interactive elements.

### Rule 9.4 — Support Dark Mode

Every view must support both Light and Dark appearances. Use semantic colors.

```swift
Text("Title").foregroundStyle(.primary)
Text("Subtitle").foregroundStyle(.secondary)
```

---

## Evaluation Checklist

### Menu Bar
- [ ] App has a complete menu bar with standard menus
- [ ] All actions have keyboard shortcuts
- [ ] Menu items dynamically update
- [ ] Context menus on all interactive elements

### Windows
- [ ] Windows are freely resizable with sensible minimums
- [ ] Fullscreen and Split View work
- [ ] Multiple windows supported
- [ ] Window position and size persist across launches
- [ ] Traffic light buttons visible and functional

### Toolbars
- [ ] Toolbar present with common actions
- [ ] Toolbar is user-customizable
- [ ] Search field available in toolbar

### Sidebars
- [ ] Sidebar for navigation
- [ ] Sidebar is collapsible
- [ ] Source list style with vibrancy

### Keyboard
- [ ] Full keyboard navigation (Tab, arrows, Enter, Esc)
- [ ] Cmd+Z undo for all destructive actions
- [ ] Space for Quick Look previews
- [ ] Delete key removes selected items

### Visual Design
- [ ] System fonts at semantic sizes
- [ ] Dark Mode fully supported
- [ ] System accent color respected

---

## Anti-Patterns

1. **No menu bar** — Every Mac app needs a menu bar.

2. **Hamburger menus** — Never use hamburger menus on Mac.

3. **Tab bars at the bottom** — Mac apps use sidebars and toolbars.

4. **Large touch-sized targets** — Mac controls should be compact (22-28pt height).

5. **Floating action buttons** — FABs are Material Design. Use toolbar or menu bar.

6. **Custom window chrome** — Don't replace the standard title bar or traffic lights.

7. **Ignoring keyboard** — If a power user must reach for the mouse for common actions, keyboard support is insufficient.

8. **Fixed window size** — Non-resizable windows feel broken on Mac.

9. **No Cmd+Z undo** — Every destructive or modifying action must be undoable.

10. **Ignoring Dark Mode** — Always test both appearances.

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
