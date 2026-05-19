# Phase 4: Narration (Jony Ive Style)

Continues `webconsulting-create-documentation` from [full guide](full-guide.md).

## Phase 4: Narration (Jony Ive Style)

### Voice characteristics

- **Tone**: Calm, deliberate, aspirational
- **Pace**: ~140 words per minute (slow, measured)
- **Style**: Short declarative sentences. Dramatic pauses. Marketing-punchy.
- **Influence**: Sir Jonathan Ive — think Apple product launch presentations

### Writing narration copy

```
BAD:  "This is a dashboard that shows you statistics about your clients."
GOOD: "Your dashboard. Beautifully considered. Every metric, thoughtfully
       placed, to give you immediate clarity."
```

### Export the narration script (single source of truth)

Define all narration text in `ProductTour.tsx` as an **exported** constant.
This is the single source of truth for both subtitles and audio generation:

```tsx
// remotion/ProductTour.tsx
export const NARRATION_SCRIPT: Record<string, string> = {
  intro: "Imagine seeing every TYPO3 installation you manage...",
  dashboard: "Your dashboard gives you the full picture...",
  // ... one entry per scene
};
```

**Critical**: The generate script **imports** this constant — never duplicate the text:

```tsx
// scripts/generate-narration.ts
import { NARRATION_SCRIPT } from "../remotion/ProductTour.js";
const NARRATION = NARRATION_SCRIPT; // Same text for audio + subtitles
```

This guarantees spoken audio always matches the on-screen subtitles.
If you edit `NARRATION_SCRIPT`, just re-run `npm run narration:generate` and
`npm run remotion:render` — both audio and subtitles update automatically.

### NarrationSubtitle component

Cinematic lower-third with word-by-word reveal, slide-up entrance, and active-word glow.
**Always reads from `NARRATION_SCRIPT`** — update the script and subtitles auto-sync.

```tsx
function NarrationSubtitle({ text }: { text: string }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Slide-up + fade entrance (0.4s → 0.9s)
  const fadeIn = interpolate(frame, [fps * 0.4, fps * 0.9], [0, 1], { ... });
  const slideUp = interpolate(frame, [fps * 0.4, fps * 0.9], [20, 0], { ... });

  const words = text.split(" ");
  const framesPerWord = fps / 2.8; // calm pace, ~2.8 words/sec

  return (
    <div style={{ position: "absolute", bottom: 60, opacity: fadeIn,
                  transform: `translateY(${slideUp}px)` }}>
      <div style={{
        maxWidth: 1100, padding: "24px 56px",
        background: "linear-gradient(135deg, rgba(0,0,0,0.72), rgba(20,20,30,0.68))",
        borderRadius: 20, border: "1px solid rgba(255,255,255,0.08)",
        boxShadow: "0 8px 32px rgba(0,0,0,0.4), 0 0 80px rgba(255,120,50,0.04)",
      }}>
        {/* Subtle top accent line */}
        <div style={{ position: "absolute", top: 0, left: 40, right: 40, height: 1,
          background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent)" }} />
        {words.map((word, i) => {
          const wordDelay = fps * 0.5 + i * framesPerWord;
          const wordOpacity = interpolate(frame, [wordDelay, wordDelay + framesPerWord * 0.5],
            [0.25, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const isActive = frame >= wordDelay && frame < wordDelay + framesPerWord * 1.2;
          return (
            <span key={i} style={{
              fontSize: 30, fontWeight: 300, color: "#fff",
              fontFamily: "'SF Pro Display', 'Inter', system-ui",
              opacity: isActive ? 1 : wordOpacity, letterSpacing: "0.02em",
              textShadow: isActive ? "0 0 20px rgba(255,255,255,0.15)" : "none",
            }}>{word}</span>
          );
        })}
      </div>
    </div>
  );
}
```

### Subtitle styling principles

- **Auto-sync**: Component reads `NARRATION_SCRIPT[scene]` directly — change the
  script text and the subtitles update automatically on next render
- **Slide-up entrance**: Subtitles slide up 20px while fading in (0.4s–0.9s), feels organic
- **Glass morphism container**: Dark gradient background with subtle border and box-shadow,
  plus a thin accent line at the top for depth
- **Word-by-word reveal**: Each word fades from 0.25 to 1.0 opacity at ~2.8 words/second
- **Active word glow**: The currently spoken word gets full opacity + a soft white `text-shadow`
- **Typography**: SF Pro Display / Inter, weight 300 (light), 30px, generous letter-spacing
- **Positioning**: 60px from bottom, centered, max-width 1100px

### When to update subtitles

Subtitles auto-update whenever you change `NARRATION_SCRIPT` in `ProductTour.tsx`.
The full pipeline after editing narration text:

```bash
# 1. Edit NARRATION_SCRIPT in remotion/ProductTour.tsx
# 2. Regenerate audio (subtitles already match the new text)
npm run narration:generate
# 3. Re-render video
npm run remotion:render
```
