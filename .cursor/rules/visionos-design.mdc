---
name: visionos-design
description: >-
  Apple Human Interface Guidelines for Apple Vision Pro. Use when building spatial
  computing apps, implementing eye/hand input, or designing immersive experiences.
  Triggers on tasks involving visionOS, RealityKit, spatial UI, or mixed reality.
license: MIT
metadata:
  version: "1.0.0"
---

# visionOS Design Guidelines

> **Source:** This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** 
> by ehmo. Apple Human Interface Guidelines for AI agents.

Comprehensive design rules for Apple Vision Pro based on Apple Human Interface Guidelines. These rules ensure spatial computing apps are comfortable, intuitive, and consistent with platform conventions.

---

## 1. Spatial Layout [CRITICAL]

Spatial layout determines user comfort and usability. Poor placement causes neck strain, disorientation, or inaccessible content.

### Rules

**SL-01: Center content in the field of view.**
Place primary windows and content directly ahead of the user at eye level. The comfortable vertical viewing range is approximately 30 degrees above and below eye level.

**SL-02: Maintain comfortable distance.**
Position content at a natural distance from the user, typically 1-2 meters for windows. The system default placement is approximately 1.5 meters.

**SL-03: Never place content behind the user.**
All UI elements must appear within the forward-facing hemisphere.

**SL-04: Respect personal space.**
Do not place 3D objects or windows closer than arm's length (~0.5 meters) from the user's head.

**SL-05: Use Z-depth to establish hierarchy.**
Elements closer to the user appear more prominent. Use subtle depth offsets (a few centimeters) between layered elements.

**SL-06: Manage multiple windows thoughtfully.**
Arrange multiple windows in a gentle arc around the user rather than stacking or overlapping.

**SL-07: Anchor content to the environment, not the head.**
Windows and objects should stay fixed in world space as the user moves their head. Head-locked content causes motion sickness.

---

## 2. Eye & Hand Input [CRITICAL]

visionOS uses indirect interaction as its primary input model: users look at a target and pinch to select.

### Rules

**EH-01: Design for look-and-pinch as the primary interaction.**
User looks at an element (eyes provide targeting), then pinches thumb and index finger together (hand provides confirmation).

**EH-02: Minimum interactive target size is 60pt.**
Eye tracking has inherent imprecision. All tappable elements must be at least 60 points in diameter.

**EH-03: Provide hover feedback on gaze.**
When the user's eyes rest on an interactive element, show a visible highlight or subtle expansion.

**EH-04: Support direct touch for close-range objects.**
When 3D objects or UI elements are within arm's reach, allow direct touch interaction.

**EH-05: Never track gaze for content purposes.**
Eye position is used exclusively for system interaction targeting. This is a core privacy principle.

**EH-06: Keep custom gestures simple and intuitive.**
Avoid gestures that require sustained hand raising, complex finger patterns, or two-handed coordination.

**EH-07: Do not require precise hand positioning.**
Users interact with hands resting naturally in their lap or at their sides.

### Target Size Reference

| Element | Minimum Size | Recommended Size |
|---|---|---|
| Buttons | 60pt | 60-80pt |
| List rows | 60pt height | 80pt height |
| Tab bar items | 60pt | 72pt |
| Close/dismiss | 60pt | 60pt |
| Toolbar items | 60pt | 60pt |

---

## 3. Windows [HIGH]

Windows in visionOS float in the user's physical space. They use a glass material that blends with the real-world environment.

### Rules

**WN-01: Use glass material as the default window background.**
The system glass material dynamically adapts to the user's surroundings.

**WN-02: Maintain standard window controls.**
Windows include a system-provided window bar at the bottom for repositioning and a close button.

**WN-03: Make windows resizable when appropriate.**

**WN-04: Place the tab bar as a leading ornament (left side).**
On visionOS, the tab bar is positioned as a vertical ornament on the leading edge of the window.

**WN-05: Place the toolbar as a bottom ornament.**
Primary action controls appear in a toolbar ornament anchored to the bottom edge.

**WN-06: Windows float in space with no fixed screen.**
Design content that looks correct when viewed from slight angles and at varying distances.

---

## 4. Volumes [HIGH]

Volumes display 3D content within a bounded box.

### Rules

**VL-01: Contain 3D content within the volume bounds.**
All content must fit within the defined volume dimensions.

**VL-02: Design for viewing from all angles.**
Users can physically walk around a volume. Ensure 3D content looks correct from all viewing angles.

**VL-03: Do not require a specific viewing position.**

**VL-04: Scale content appropriately for the space.**

**VL-05: Use volumes for self-contained 3D experiences.**

---

## 5. Immersive Spaces [HIGH]

visionOS supports a spectrum of immersion from shared space (apps alongside reality) to full immersion (complete virtual environment).

### Rules

**IS-01: Start in the Shared Space.**
Apps launch into the Shared Space by default. Only transition to more immersive experiences when the user explicitly requests it.

**IS-02: Use progressive immersion.**
Move through immersion levels gradually: Shared Space → Full Space → Full Immersion.

**IS-03: Always provide an exit path.**
Users must always be able to return to a less immersive state. The Digital Crown is the system-level escape.

**IS-04: Use passthrough for safety.**
In experiences where users might move physically, maintain passthrough of the real environment.

**IS-05: Dim passthrough gradually.**
Use smooth, animated transitions between immersion levels.

**IS-06: Do not assume room layout or size.**
Gracefully adapt to whatever physical space is available.

**IS-07: Provide spatial audio cues.**
Use spatial audio to help users orient. Sounds should come from the direction of their source.

---

## 6. Materials & Depth [MEDIUM]

visionOS uses a physically-based material system that responds to real-world lighting.

### Rules

**MD-01: Use the system glass material for UI surfaces.**

**MD-02: Specular highlights respond to the environment.**

**MD-03: Layer materials to create depth hierarchy.**
Use lighter/thicker glass for foreground elements and darker/thinner glass for background.

**MD-04: Apply vibrancy for text readability.**
Text over glass materials uses vibrancy effects to remain legible.

**MD-05: Use shadows and highlights for elevation.**

**MD-06: Avoid fully opaque backgrounds in shared space.**
Opaque surfaces create visual holes in the environment.

---

## 7. Ornaments [MEDIUM]

Ornaments are UI controls that attach to the edges of windows.

### Rules

**OR-01: Attach controls as ornaments rather than inline.**
Toolbars, tab bars, and persistent action buttons belong as ornaments.

**OR-02: Place primary actions in the bottom ornament.**

**OR-03: Place navigation in the leading (left) ornament.**

**OR-04: Do not occlude window content with ornaments.**
Ornaments extend outward from the window edge.

**OR-05: Show ornaments contextually when appropriate.**
Toolbars can appear on hover and fade when the user looks away.

**OR-06: Use standard ornament styling.**

---

## Evaluation Checklist

### Spatial Layout
- [ ] Primary content centered in forward field of view
- [ ] Content placed at comfortable distance (1-2m for windows)
- [ ] No content placed behind the user
- [ ] Personal space respected (nothing closer than ~0.5m)
- [ ] Z-depth used meaningfully for hierarchy
- [ ] Content anchored to world space, not head-locked

### Eye & Hand Input
- [ ] All interactions work with look-and-pinch
- [ ] All interactive targets >= 60pt
- [ ] Hover states visible on all interactive elements
- [ ] Direct touch supported for close-range objects
- [ ] No gaze tracking for content or analytics purposes

### Windows
- [ ] Glass material used as default background
- [ ] Standard window bar and close button present
- [ ] Tab bar positioned as leading ornament
- [ ] Toolbar positioned as bottom ornament

### Volumes
- [ ] Content contained within volume bounds
- [ ] Content looks correct from all viewing angles
- [ ] No specific viewing position required

### Immersive Spaces
- [ ] App starts in Shared Space
- [ ] Immersion increases progressively
- [ ] Clear exit path always available
- [ ] Passthrough maintained where safety requires it
- [ ] Transitions between immersion levels are smooth

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|---|---|---|
| Head-locked UI | Causes motion sickness | Anchor UI to world space |
| Tiny tap targets | Eye tracking cannot reliably target < 60pt | Minimum 60pt interactive targets |
| No hover states | Users cannot tell what is interactive | Always show highlight on gaze |
| Opaque windows in shared space | Creates visual holes in environment | Use system glass material |
| Forced full immersion | Disorienting, traps users | Start in shared space, progressive immersion |
| Content behind user | Invisible, requires full body rotation | Keep content in forward hemisphere |
| Gaze-driven content | Privacy violation, feels surveilled | Use gaze only for system targeting |
| Flat 3D volumes | Looks like cardboard cutout from side | Design for all viewing angles |
| Sustained arm raising | Physical fatigue in minutes | Design for hands resting at sides |

---

## Credits & Attribution

This skill is adapted from **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo.

**Copyright (c) platform-design-skills** - MIT License  
Adapted by webconsulting.at for this skill collection
