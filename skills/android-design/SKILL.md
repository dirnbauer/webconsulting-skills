---
name: android-design-guidelines
description: Material Design 3 and Android platform guidelines. Use when building Android apps with Jetpack Compose or XML layouts, implementing Material You, navigation, or accessibility. Triggers on tasks involving Android UI, Compose components, dynamic color, or Material Design compliance.
version: 1.0.0
license: MIT
triggers:
  - android
  - material design
  - jetpack compose
  - android ui
  - material you
  - dynamic color
  - android accessibility
  - android navigation
---

# Android Platform Design Guidelines — Material Design 3

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Android/Material Design 3 guidelines for AI agents.

## 1. Material You & Theming [CRITICAL]

### 1.1 Dynamic Color

Enable dynamic color derived from the user's wallpaper. Dynamic color is the default on Android 12+ and should be the primary theming strategy.

```kotlin
// Compose: Dynamic color theme
@Composable
fun AppTheme(
  darkTheme: Boolean = isSystemInDarkTheme(),
  dynamicColor: Boolean = true,
  content: @Composable () -> Unit
) {
  val colorScheme = when {
    dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
      val context = LocalContext.current
      if (darkTheme) dynamicDarkColorScheme(context)
      else dynamicLightColorScheme(context)
    }
    darkTheme -> darkColorScheme()
    else -> lightColorScheme()
  }
  MaterialTheme(
    colorScheme = colorScheme,
    typography = AppTypography,
    content = content
  )
}
```

**Rules:**
- R1.1: Always provide a fallback static color scheme for devices below Android 12.
- R1.2: Never hardcode color hex values in components. Always reference color roles from the theme.
- R1.3: Test with at least 3 different wallpapers to verify dynamic color harmony.

### 1.2 Color Roles

Material 3 defines a structured set of color roles. Use them semantically, not aesthetically.

| Role | Usage | On-Role |
|------|-------|---------|
| `primary` | Key actions, active states, FAB | `onPrimary` |
| `primaryContainer` | Less prominent primary elements | `onPrimaryContainer` |
| `secondary` | Supporting UI, filter chips | `onSecondary` |
| `secondaryContainer` | Navigation bar active indicator | `onSecondaryContainer` |
| `tertiary` | Accent, contrast, complementary | `onTertiary` |
| `tertiaryContainer` | Input fields, less prominent accents | `onTertiaryContainer` |
| `surface` | Backgrounds, cards, sheets | `onSurface` |
| `surfaceVariant` | Decorative elements, dividers | `onSurfaceVariant` |
| `error` | Error states, destructive actions | `onError` |
| `errorContainer` | Error backgrounds | `onErrorContainer` |
| `outline` | Borders, dividers | — |
| `outlineVariant` | Subtle borders | — |
| `inverseSurface` | Snackbar background | `inverseOnSurface` |

```kotlin
// Correct: semantic color roles
Text(
  text = "Error message",
  color = MaterialTheme.colorScheme.error
)
Surface(color = MaterialTheme.colorScheme.errorContainer) {
  Text(text = "Error detail", color = MaterialTheme.colorScheme.onErrorContainer)
}

// WRONG: hardcoded colors
Text(text = "Error", color = Color(0xFFB00020)) // Anti-pattern
```

**Rules:**
- R1.4: Every foreground element must use the matching `on` color role for its background (e.g., `onPrimary` text on `primary` background).
- R1.5: Use `surface` and its variants for backgrounds. Never use `primary` or `secondary` as large background areas.
- R1.6: Use `tertiary` sparingly for accent and complementary contrast only.

### 1.3 Light and Dark Themes

Support both light and dark themes. Respect the system setting by default.

```kotlin
// Compose: Detect system theme
val darkTheme = isSystemInDarkTheme()
```

**Rules:**
- R1.7: Always support both light and dark themes. Never ship light-only.
- R1.8: Dark theme surfaces use elevation-based tonal mapping, not pure black (#000000). Use `surface` color roles which handle this automatically.
- R1.9: Provide a manual theme override in app settings (System / Light / Dark).

---

## 2. Navigation [CRITICAL]

### 2.1 Navigation Bar (Bottom)

The primary navigation pattern for phones with 3-5 top-level destinations.

```kotlin
// Compose: Navigation Bar
NavigationBar {
  items.forEachIndexed { index, item ->
    NavigationBarItem(
      icon = {
        Icon(
          imageVector = if (selectedItem == index) item.filledIcon else item.outlinedIcon,
          contentDescription = item.label
        )
      },
      label = { Text(item.label) },
      selected = selectedItem == index,
      onClick = { selectedItem = index }
    )
  }
}
```

**Rules:**
- R2.1: Use Navigation Bar for 3-5 top-level destinations on compact screens. Never use for fewer than 3 or more than 5.
- R2.2: Always show labels on navigation bar items. Icon-only navigation bars are not permitted.
- R2.3: Use filled icons for the selected state and outlined icons for unselected states.
- R2.4: The active indicator uses `secondaryContainer` color. Do not override this.

### 2.2 Navigation Rail

For medium and expanded screens (tablets, foldables, desktop).

```kotlin
// Compose: Navigation Rail for larger screens
NavigationRail(
  header = {
    FloatingActionButton(
      onClick = { /* primary action */ },
      containerColor = MaterialTheme.colorScheme.tertiaryContainer
    ) {
      Icon(Icons.Default.Add, contentDescription = "Create")
    }
  }
) {
  items.forEachIndexed { index, item ->
    NavigationRailItem(
      icon = { Icon(item.icon, contentDescription = item.label) },
      label = { Text(item.label) },
      selected = selectedItem == index,
      onClick = { selectedItem = index }
    )
  }
}
```

### 2.3 Navigation Component Selection

| Screen Size | 3-5 Destinations | 5+ Destinations |
|-------------|-------------------|-----------------|
| Compact (< 600dp) | Navigation Bar | Modal Drawer + Navigation Bar |
| Medium (600-839dp) | Navigation Rail | Modal Drawer + Navigation Rail |
| Expanded (840dp+) | Navigation Rail | Permanent Drawer |

---

## 3. Layout & Responsive [HIGH]

### 3.1 Window Size Classes

Use window size classes for adaptive layouts, not raw pixel breakpoints.

```kotlin
// Compose: Window size classes
val windowSizeClass = calculateWindowSizeClass(this)
when (windowSizeClass.widthSizeClass) {
  WindowWidthSizeClass.Compact -> CompactLayout()
  WindowWidthSizeClass.Medium -> MediumLayout()
  WindowWidthSizeClass.Expanded -> ExpandedLayout()
}
```

| Class | Width | Typical Device | Columns |
|-------|-------|----------------|---------|
| Compact | < 600dp | Phone portrait | 4 |
| Medium | 600-839dp | Tablet portrait, foldable | 8 |
| Expanded | 840dp+ | Tablet landscape, desktop | 12 |

**Rules:**
- R3.1: Always use `WindowSizeClass` from `material3-window-size-class` for responsive layout decisions.
- R3.2: Never use fixed pixel breakpoints. Device categories are fluid.
- R3.3: Support all three width size classes. At minimum, compact and expanded.

### 3.2 Edge-to-Edge Display

Android 15+ enforces edge-to-edge. All apps should draw behind system bars.

```kotlin
// Compose: Edge-to-edge setup
class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    enableEdgeToEdge()
    super.onCreate(savedInstanceState)
    setContent {
      Scaffold(
        modifier = Modifier.fillMaxSize(),
      ) { innerPadding ->
        Content(modifier = Modifier.padding(innerPadding))
      }
    }
  }
}
```

---

## 4. Typography [HIGH]

### 4.1 Material Type Scale

| Role | Default Size | Default Weight | Usage |
|------|-------------|----------------|-------|
| displayLarge | 57sp | 400 | Hero text, onboarding |
| displayMedium | 45sp | 400 | Large feature text |
| displaySmall | 36sp | 400 | Prominent display |
| headlineLarge | 32sp | 400 | Screen titles |
| headlineMedium | 28sp | 400 | Section headers |
| headlineSmall | 24sp | 400 | Card titles |
| titleLarge | 22sp | 400 | Top app bar title |
| titleMedium | 16sp | 500 | Tabs, navigation |
| titleSmall | 14sp | 500 | Subtitles |
| bodyLarge | 16sp | 400 | Primary body text |
| bodyMedium | 14sp | 400 | Secondary body text |
| bodySmall | 12sp | 400 | Captions |
| labelLarge | 14sp | 500 | Buttons, prominent labels |
| labelMedium | 12sp | 500 | Chips, smaller labels |
| labelSmall | 11sp | 500 | Timestamps, annotations |

**Rules:**
- R4.1: Always use `sp` units for text sizes to support user font scaling preferences.
- R4.2: Never set text below 12sp for body content. Labels may go to 11sp minimum.
- R4.3: Reference typography roles from `MaterialTheme.typography`, not hardcoded sizes.
- R4.4: Support dynamic type scaling. Test at 200% font scale.

---

## 5. Components [HIGH]

### 5.1 Floating Action Button (FAB)

```kotlin
// Extended FAB (with label - preferred for clarity)
ExtendedFloatingActionButton(
  onClick = { /* action */ },
  icon = { Icon(Icons.Default.Edit, contentDescription = null) },
  text = { Text("Compose") }
)
```

**Rules:**
- R5.1: Use at most one FAB per screen. It represents the primary action.
- R5.2: Place the FAB at the bottom-end of the screen.
- R5.3: The FAB should use `primaryContainer` color by default.
- R5.4: Prefer `ExtendedFloatingActionButton` with a label for clarity.

### 5.2 Snackbar

```kotlin
val snackbarHostState = remember { SnackbarHostState() }
Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) {
  LaunchedEffect(key) {
    val result = snackbarHostState.showSnackbar(
      message = "Item archived",
      actionLabel = "Undo",
      duration = SnackbarDuration.Short
    )
    if (result == SnackbarResult.ActionPerformed) { /* undo */ }
  }
}
```

**Rules:**
- R5.14: Use snackbars for brief, non-critical feedback.
- R5.15: Snackbars appear at the bottom, above Navigation Bar and below FAB.
- R5.16: Include an action (e.g., "Undo") when the operation is reversible.

---

## 6. Accessibility [CRITICAL]

### 6.1 TalkBack and Content Descriptions

```kotlin
// Compose: Accessible components
Icon(
  Icons.Default.Favorite,
  contentDescription = "Add to favorites" // Descriptive, not "heart icon"
)

// Decorative elements
Icon(
  Icons.Default.Star,
  contentDescription = null // null for purely decorative
)

// Merge semantics for compound elements
Row(modifier = Modifier.semantics(mergeDescendants = true) {}) {
  Icon(Icons.Default.Event, contentDescription = null)
  Text("March 15, 2026")
}
```

**Rules:**
- R6.1: Every interactive element must have a `contentDescription` (or `null` if purely decorative).
- R6.2: Content descriptions must describe the action or meaning, not the visual appearance.
- R6.3: Use `mergeDescendants = true` to group related elements.
- R6.5: All interactive elements must have a minimum touch target of 48x48dp.

### 6.2 Color Contrast

**Rules:**
- R6.7: Text contrast ratio must be at least 4.5:1 for normal text and 3:1 for large text.
- R6.8: Never use color as the only means of conveying information.

---

## 7. Gestures & Input [MEDIUM]

### 7.1 Common Gesture Patterns

```kotlin
// Compose: Pull to refresh
PullToRefreshBox(
  isRefreshing = isRefreshing,
  onRefresh = { viewModel.refresh() }
) {
  LazyColumn { /* content */ }
}

// Compose: Swipe to dismiss
SwipeToDismissBox(
  state = rememberSwipeToDismissBoxState(),
  backgroundContent = {
    Box(
      modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.error),
      contentAlignment = Alignment.CenterEnd
    ) {
      Icon(Icons.Default.Delete, contentDescription = "Delete",
        tint = MaterialTheme.colorScheme.onError)
    }
  }
) {
  ListItem(headlineContent = { Text("Swipeable item") })
}
```

**Rules:**
- R7.1: Never place interactive elements within system gesture inset zones.
- R7.3: All swipe-to-dismiss actions must be undoable or require confirmation.
- R7.4: Provide alternative non-gesture ways to trigger all gesture-based actions.

---

## Design Evaluation Checklist

### Theme & Color
- [ ] Dynamic color enabled with static fallback
- [ ] All colors reference Material theme roles (no hardcoded hex)
- [ ] Light and dark themes both supported
- [ ] On-colors match their background color roles

### Navigation
- [ ] Correct navigation component for screen size and destination count
- [ ] Navigation bar labels always visible
- [ ] Predictive back gesture opted in and handled

### Layout
- [ ] All three window size classes supported
- [ ] Edge-to-edge with proper inset handling
- [ ] Content does not span full width on large screens

### Accessibility
- [ ] All interactive elements have contentDescription
- [ ] All touch targets >= 48dp
- [ ] Color contrast >= 4.5:1 for text
- [ ] No information conveyed by color alone
- [ ] Full TalkBack traversal tested

---

## Anti-Patterns

| Anti-Pattern | Why It Is Wrong | Correct Approach |
|-------------|----------------|------------------|
| Hardcoded color hex values | Breaks dynamic color and dark theme | Use `MaterialTheme.colorScheme` roles |
| Using `dp` for text size | Ignores user font scaling | Use `sp` units |
| Custom bottom navigation bar | Inconsistent with platform | Use Material `NavigationBar` |
| Navigation bar without labels | Violates Material guidelines | Always show labels |
| FAB for secondary actions | Dilutes primary action prominence | One FAB for the primary action only |
| Touch targets < 48dp | Accessibility violation | Ensure minimum 48x48dp |
| Pure black (#000000) dark theme | Eye strain; not Material 3 | Use Material surface color roles |
| Full-width content on tablets | Wastes space; poor readability | Max width or list-detail layout |

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
