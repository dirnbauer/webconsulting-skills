---
name: tvos-design-guidelines
description: Apple Human Interface Guidelines for Apple TV. Use when building tvOS apps with focus-based navigation, Siri Remote input, or living room viewing experiences. Triggers on tasks involving Apple TV, tvOS, 10-foot UI, or media playback.
version: 1.0.0
license: MIT
triggers:
  - tvos
  - apple tv
  - 10-foot ui
  - siri remote
  - focus navigation
  - tv app
  - media playback
  - living room
---

# tvOS Design Guidelines

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Apple Human Interface Guidelines for AI agents.

Apple TV is a living room device driven entirely by focus-based navigation and the Siri Remote. There is no pointer, no touch screen, and no mouse. Every design decision must account for the 10-foot viewing distance, the simplicity of the remote, and the lean-back nature of TV consumption.

---

## 1. Focus-Based Navigation [CRITICAL]

The focus system is the foundation of all tvOS interaction. There is no cursor -- users move focus between elements using the Siri Remote touch surface.

### Rules

**FOCUS-01: Every interactive element must have a clearly visible focus state.**
Use scaling (typically 1.05x-1.1x), elevation via shadow, brightness changes, or border highlights. Never rely on color alone.

**FOCUS-02: Focus movement must be predictable and follow a logical spatial layout.**
When a user swipes right, focus must move to the element visually to the right.

**FOCUS-03: Use focus guides (UIFocusGuide) to bridge gaps in layouts.**
When visual gaps exist between focusable elements, add invisible focus guides.

**FOCUS-04: Apply the parallax effect to focused items.**
Focused cards, posters, and icons should exhibit a subtle parallax tilt. Use layered images (LSR format) with foreground, midground, and background layers.

**FOCUS-05: Make focus targets large enough for comfortable navigation.**
Minimum recommended size is 250x150pt for cards.

**FOCUS-06: Provide a default focused element on every screen.**
When a view appears, one element must already hold focus.

**FOCUS-07: Preserve focus memory when returning to a screen.**
Focus should restore to the last focused item, not reset to the default.

**FOCUS-08: Never trap focus.**
Users must always be able to move focus away from any element.

### Parallax Layer Reference

| Layer | Purpose | Movement Amount |
|-------|---------|-----------------|
| Background | Static backdrop, blurred imagery | Minimal (1-2pt) |
| Midground | Primary artwork or content image | Moderate (3-5pt) |
| Foreground | Title text, logos, badges | Maximum (5-8pt) |

---

## 2. Siri Remote [CRITICAL]

The Siri Remote is the primary input device. It has a touch surface, Menu button, Play/Pause button, Siri/microphone button, and volume buttons.

### Rules

**REMOTE-01: Touch surface swipes control focus movement.**
Swiping moves focus. Clicking the touch surface selects the focused item.

**REMOTE-02: Menu button must always navigate back.**
Pressing Menu should dismiss the current screen or navigate up the hierarchy.

**REMOTE-03: Play/Pause button must control media playback.**
If media is playing, Play/Pause should toggle playback regardless of what screen is visible.

**REMOTE-04: Never require complex or multi-finger gestures.**
The Siri Remote touch surface is small. Stick to single-finger swipe and click.

**REMOTE-05: Swipe directions must be intuitive and consistent.**
Horizontal swipes scroll horizontally; vertical swipes scroll vertically.

**REMOTE-06: Support Siri voice input for search and text entry.**
Text input via the on-screen keyboard is tedious on tvOS.

**REMOTE-07: Provide click feedback.**
When the user clicks to select an item, provide immediate visual feedback.

---

## 3. 10-Foot UI [HIGH]

Apple TV content is viewed from across a room, typically 8-12 feet (2.5-3.5 meters) from the screen.

### Rules

**DISTANCE-01: Minimum body text size is 29pt.**
Text below 29pt becomes difficult to read. Titles should be 48pt or larger.

**DISTANCE-02: Maintain high contrast between text and backgrounds.**
Use light text on dark backgrounds as the default. tvOS uses a dark theme.

**DISTANCE-03: Limit text per screen.**
TV is a visual medium. Show headlines, short descriptions, and metadata -- not paragraphs.

**DISTANCE-04: Use bold, clear imagery at high resolution.**
Full-screen background images should be 1920x1080 or 3840x2160 (4K).

**DISTANCE-05: Keep layouts simple and spacious.**
A single row of 5-7 cards is preferable to a dense grid of 20+ thumbnails.

**DISTANCE-06: Use the TV-safe area.**
Keep all critical content within the safe area (60pt inset from edges).

**DISTANCE-07: Avoid thin fonts and hairline borders.**
Thin strokes disappear on TV displays.

### Text Size Reference

| Element | Minimum Size | Recommended Size |
|---------|-------------|-----------------|
| Body text | 29pt | 31-35pt |
| Secondary labels | 25pt | 29pt |
| Titles | 48pt | 52-76pt |
| Large headers | 64pt | 76-96pt |
| Buttons | 29pt | 35-38pt |

---

## 4. Top Shelf [HIGH]

The Top Shelf is a prominent content area displayed when the user focuses on your app icon on the Apple TV home screen.

### Rules

**SHELF-01: Provide a Top Shelf extension.**
Apps should include a TVTopShelfProvider that returns dynamic content.

**SHELF-02: Use the correct layout style for your content.**
- **Inset banner**: Best for featured or editorial content.
- **Sectioned content**: Best for media libraries.

**SHELF-03: Top Shelf items must deep-link into the app.**
Each item must open the corresponding content when selected.

**SHELF-04: Use high-quality, engaging imagery.**
Recommended image sizes:
- Inset banner: 1940x624pt (@1x) or 3880x1248pt (@2x)
- Sectioned items: 404x608pt (@1x)

**SHELF-05: Keep Top Shelf content fresh.**
Update regularly to reflect recently added or trending content.

---

## 5. Media & Playback [MEDIUM]

Apple TV is primarily a media consumption device.

### Rules

**MEDIA-01: Use standard transport controls.**
Provide play, pause, skip forward (10s), skip back (10s), and a scrubber timeline.

**MEDIA-02: Show an info overlay on swipe-down during playback.**
Swiping down should reveal an info panel showing title, description, and metadata.

**MEDIA-03: Support scrubbing via the touch surface.**
Swiping left/right during playback should scrub through the timeline.

**MEDIA-04: Support subtitles and alternative audio tracks.**

**MEDIA-05: Support Picture in Picture where appropriate.**

**MEDIA-06: Remember playback position.**
Display a progress indicator on content thumbnails.

**MEDIA-07: Handle interruptions gracefully.**
Save position and pause cleanly when the user switches apps.

---

## 6. Tab Bar [MEDIUM]

The tvOS tab bar sits at the top of the screen.

### Rules

**TAB-01: Place the tab bar at the top of the screen.**
This is the standard tvOS convention.

**TAB-02: Tab bar should be translucent and overlay content.**

**TAB-03: Use 3-7 tabs.**

**TAB-04: Every tab must have a text label.**
Icon-only tabs are insufficient at TV viewing distances.

**TAB-05: Focus on the tab bar should feel lightweight.**

**TAB-06: Remember the selected tab across app launches.**

---

## Evaluation Checklist

### Focus System
- [ ] Every interactive element has a visible, distinct focus state
- [ ] Focus movement is predictable in all directions
- [ ] No focus traps exist anywhere in the app
- [ ] Parallax effect is applied to content cards and icons
- [ ] Default focus is set on every screen
- [ ] Focus memory is preserved when navigating back

### Siri Remote
- [ ] Menu button navigates back on every screen
- [ ] Play/Pause controls media playback globally
- [ ] No complex gestures are required
- [ ] Click feedback is immediate and visible
- [ ] Siri/dictation supported for text input

### 10-Foot UI
- [ ] Body text is 29pt or larger
- [ ] High contrast ratios on all text
- [ ] Text content is concise, not paragraph-heavy
- [ ] Imagery is high resolution and visually clear
- [ ] Layout uses generous spacing with TV-safe margins

### Top Shelf
- [ ] Top Shelf extension provides dynamic content
- [ ] All Top Shelf items deep-link correctly
- [ ] Images are high quality and correctly sized

### Media & Playback
- [ ] Standard transport controls are available
- [ ] Scrubbing works via touch surface
- [ ] Subtitles and audio tracks are accessible
- [ ] Playback position is remembered

### Tab Bar
- [ ] Tab bar is at the top of the screen
- [ ] Tabs have text labels
- [ ] 3-7 tabs are used
- [ ] Selected tab persists across launches

---

## Anti-Patterns for TV

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Bottom tab bar | iOS convention; feels wrong on TV | Use top tab bar |
| Small touch targets | Cannot precisely target with swipe navigation | Minimum 250x150pt cards |
| Dense text screens | Unreadable at 10-foot distance | Headlines + short descriptions only |
| Hamburger menus | No tap-to-reveal interaction on TV | Use tab bar or focus-driven menus |
| Pull-to-refresh | No pull gesture on Siri Remote | Auto-refresh or explicit refresh button |
| Thin/light typography | Disappears on TV displays | Medium weight minimum |

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
