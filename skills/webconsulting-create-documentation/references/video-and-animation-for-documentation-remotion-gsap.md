# Video & Animation for Documentation (Remotion + GSAP)

Continues `webconsulting-create-documentation` from [full guide](full-guide.md).

## Video & Animation for Documentation (Remotion + GSAP)

When generating visual documentation, integrating **Remotion** with **GSAP** allows for complex, sequenced, and dynamic visual storytelling.

### Prerequisites

GSAP must be installed alongside your existing Remotion setup. GSAP's core is free for all use cases; premium plugins require a paid license.

**Install GSAP core:**

```bash
npm install gsap
```

**Optional premium plugins** (require [GSAP Club](https://gsap.com/pricing/) license):

```bash
# Install from GSAP's private registry (requires auth token)
npm install gsap@npm:@gsap/shockingly
```

Premium plugins used in this guide:
- `MorphSVGPlugin` -- morph between SVG shapes (chart transitions)
- `SplitText` -- split text into characters/words for kinetic typography
- `Flip` -- animate layout changes (code diff walkthroughs)
- `MotionPathPlugin` -- animate along SVG paths (included free since GSAP 3.x)

**Register plugins** in your Remotion entry point (e.g., `src/Root.tsx` or the component file):

```tsx
import gsap from "gsap";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";

gsap.registerPlugin(MotionPathPlugin);
// Add other plugins as needed:
// gsap.registerPlugin(Flip, MorphSVGPlugin, SplitText);
```

**Remotion compatibility notes:**
- GSAP works in Remotion's rendering pipeline because it manipulates DOM elements directly, which Remotion captures frame-by-frame.
- Always use `gsap.context()` for proper React cleanup on unmount.
- Never use GSAP's `ScrollTrigger` in Remotion -- there is no scroll context during rendering.

### Core Concept: Deterministic Syncing
Remotion is frame-based; GSAP is time-based. To ensure videos render correctly without tearing or skipping during export, **never let GSAP run on its own timer**. Map Remotion's `useCurrentFrame()` to a strictly paused GSAP timeline.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useRef } from "react";
import gsap from "gsap";

export const GsapSequence = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  
  // 1. Create a strictly paused timeline
  const timeline = useMemo(() => gsap.timeline({ paused: true }), []);

  // 2. Build your animation sequence (use GSAP seconds)
  useEffect(() => {
    let ctx = gsap.context(() => {
      timeline.to(".box", { x: 200, rotation: 360, duration: 2, stagger: 0.2 });
    }, containerRef);
    
    return () => ctx.revert(); // React cleanup
  }, [timeline]);

  // 3. THE MAGIC: Sync GSAP playhead to Remotion frame
  useEffect(() => {
    timeline.seek(frame / fps); 
  }, [frame, fps, timeline]);

  return (
    <div ref={containerRef} className="box-container">
      <div className="box">Item 1</div>
      <div className="box">Item 2</div>
    </div>
  );
};
```

### Creative Directives for AI Agents

When prompted to create visual documentation, utilize the following animation patterns:

#### 1. Diagram Animations
- **Data Flow Tracing:** Use GSAP `MotionPathPlugin` or animate `stroke-dashoffset` to show data packets moving along SVG lines between architecture nodes (e.g., Load Balancer → DB).
- **Node Pulses:** Add glowing/pulsing loops (`box-shadow` and `scale`) to servers/components when they become "active" in the explanation.
- **Elastic Reveals:** Animate nodes popping into existence with `ease: "back.out(1.5)"` and a `stagger: 0.1`.

#### 2. Animation of Screenshots
- **3D Exploded View:** Separate UI components into layers (background, modal, button) and rotate the parent container in 3D (`rotateX: 60deg`, `rotateZ: -45deg`). Animate the `translateZ` of inner layers to pull the interface apart conceptually.
- **Glass Morph Spotlight:** Smoothly zoom into an active UI area using a `clip-path` circle, while dimming and applying a CSS blur (`backdrop-filter: blur(10px)`) to the rest of the screenshot.
- **Simulated User Journeys:** Animate a custom SVG cursor moving across the UI, synchronizing button scaling and ripple effects to simulate clicks.

#### 3. Infographics & Tables
- **Staggered Row Reveals:** Slide and fade in table rows one-by-one (`stagger: 0.1`, `x: -20`, `opacity: 0`) to pace the viewer's reading.
- **Data Odometers:** Animate a numeric object's value from 0 to target (using `onUpdate` to format text), making financial or performance numbers tick up dynamically.
- **Cell Highlighting:** Animate a floating background div that smoothly translates its `y` coordinate from row to row to highlight active talking points.

#### 4. Animations of Charts
- **Spring-loaded Bar Charts:** Set CSS `transform-origin: bottom`. Animate SVG `<rect>` `scaleY` from 0 to target with GSAP's `elastic.out` easing for a playful reveal.
- **Progressive Charts:** Animate SVG circles with `stroke-dasharray` and `stroke-dashoffset` to draw out pie chart segments proportionally over time.
- **Morphing Data:** Use `MorphSVGPlugin` to seamlessly transition a bar chart into a line chart, visually connecting two different ways of looking at the same data.

#### 5. Code & Text
- **Code Diff Walkthroughs:** Use GSAP's `Flip` plugin. When code changes, removed lines shrink and glow red, new lines expand and glow green, and unchanged lines glide to their new line numbers smoothly.
- **Kinetic Typography:** Use GSAP `SplitText` to stagger headers character-by-character.

---

### Concrete Code Examples (Remotion + GSAP Patterns)

Use these blueprints as starting points when generating Remotion + GSAP code to ensure correct CSS contexts, React lifecycle management, and frame syncing.

#### Example 1: 3D Exploded Screenshot (UI Layers)
Requires a strict CSS 3D context. The parent needs `perspective`, and the container needs `transformStyle: "preserve-3d"`.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useRef } from "react";
import gsap from "gsap";

export const ExplodedScreenshot = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tl = useMemo(() => gsap.timeline({ paused: true }), []);

  useEffect(() => {
    let ctx = gsap.context(() => {
      // 1. Tilt the whole container into isometric space
      tl.to(".wrapper", { rotateX: 60, rotateZ: -45, duration: 1, ease: "power2.inOut" })
        // 2. Explode the layers upward on the Z-axis (Using "<" to sync with rotation end)
        .to(".ui-layer", {
          z: (index) => (index + 1) * 80, // Stagger height based on index
          boxShadow: "0px 20px 40px rgba(0,0,0,0.4)",
          duration: 1.5,
          ease: "back.out(1.2)",
          stagger: 0.2
        }, "-=0.2"); 
    }, containerRef);
    
    return () => ctx.revert(); // Crucial for React StrictMode cleanup
  }, [tl]);

  // Deterministic Frame Sync
  useEffect(() => { tl.seek(frame / fps); }, [frame, fps, tl]);

  return (
    <div ref={containerRef} style={{ perspective: 1000, width: "100%", height: "100%" }}>
      <div className="wrapper" style={{ transformStyle: "preserve-3d", position: "relative", width: 800, height: 600 }}>
        <img src="/bg-layer.png" className="ui-layer" style={{ position: "absolute", inset: 0 }} />
        <img src="/modal-layer.png" className="ui-layer" style={{ position: "absolute", inset: 0 }} />
        <img src="/dropdown-layer.png" className="ui-layer" style={{ position: "absolute", inset: 0 }} />
      </div>
    </div>
  );
};
```

#### Example 2: SVG Architecture Diagram (Drawing Data Flows)
Use native SVG `strokeDasharray` and GSAP `strokeDashoffset` to draw connection lines between nodes without needing external plugins.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useRef } from "react";
import gsap from "gsap";

export const ArchitectureFlow = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const svgRef = useRef<SVGSVGElement>(null);
  const tl = useMemo(() => gsap.timeline({ paused: true }), []);

  useEffect(() => {
    let ctx = gsap.context(() => {
      // Setup: ensure path is hidden initially (Assuming path length ~500)
      gsap.set(".connection-line", { strokeDasharray: 500, strokeDashoffset: 500 });

      // 1. Pop the nodes in
      tl.from(".node", { scale: 0, transformOrigin: "center", duration: 0.5, stagger: 0.3, ease: "back.out(1.5)" })
      // 2. Draw the line between them
        .to(".connection-line", { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" })
      // 3. Pulse the receiving node to indicate data arrival
        .to(".node-db", { scale: 1.15, repeat: 1, yoyo: true, duration: 0.2, fill: "#10b981" });
    }, svgRef);
    
    return () => ctx.revert();
  }, [tl]);

  useEffect(() => { tl.seek(frame / fps); }, [frame, fps, tl]);

  return (
    <svg ref={svgRef} width="800" height="400" viewBox="0 0 800 400">
      {/* Connecting Line */}
      <path className="connection-line" d="M 100 200 C 300 200, 500 200, 700 200" stroke="#cbd5e1" strokeWidth="6" fill="none" />
      {/* Nodes */}
      <circle className="node node-client" cx="100" cy="200" r="40" fill="#3b82f6" />
      <rect className="node node-db" x="660" y="160" width="80" height="80" rx="12" fill="#6366f1" />
    </svg>
  );
};
```

#### Example 3: Number Odometer (For Infographics & Tables)
To animate a number counting up (e.g., "0" to "10,000") smoothly, animate a dummy object and use `onUpdate` to safely set React state synchronously with the frame.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useState } from "react";
import gsap from "gsap";

export const AnimatedNumber = ({ targetValue = 10000 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [displayValue, setDisplayValue] = useState(0);
  
  const tl = useMemo(() => gsap.timeline({ paused: true }), []);

  useEffect(() => {
    const counter = { val: 0 };
    
    // gsap.context isn't strictly necessary for JS objects, but good for consistency
    let ctx = gsap.context(() => {
      tl.to(counter, {
        val: targetValue,
        duration: 2,
        ease: "power2.out",
        onUpdate: () => {
          // Update React state safely as GSAP manipulates the dummy object
          setDisplayValue(Math.round(counter.val));
        }
      });
    });
    
    return () => ctx.revert();
  }, [tl, targetValue]);

  useEffect(() => { tl.seek(frame / fps); }, [frame, fps, tl]);

  return (
    <div style={{ fontSize: "64px", fontFamily: "monospace", fontWeight: "bold" }}>
      ${displayValue.toLocaleString()}
    </div>
  );
};
```


Source: https://github.com/dirnbauer/webconsulting-skills
