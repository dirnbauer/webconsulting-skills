---
name: "webconsulting-create-documentation"
description: "Creates product documentation systems with help pages, AI-generated screenshots, Remotion product tours, GSAP animation, narration scripts, TTS, background music, README visuals, and deployment steps. Use when the user asks for product docs, help pages, documentation videos, narrated tours, screenshots, README media, Remotion docs workflows, or webconsulting-style documentation assets."
metadata:
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# webconsulting — Create Documentation

> Source: https://github.com/dirnbauer/webconsulting-skills

End-to-end workflow for building product documentation: help pages, AI-generated illustrations, narrated product tour videos (Remotion + ElevenLabs TTS + Suno AI music), and GitHub README visual documentation.

## Prerequisites

### Required

| Dependency | Install | Purpose |
|------------|---------|---------|
| Node.js 20+ | Pre-installed | Runtime |
| Remotion | `npm install remotion @remotion/cli @remotion/player` | Video composition |
| qrcode.react | `npm install qrcode.react` | QR codes in end card |
| tsx | `npm install -D tsx` | Run TypeScript scripts |

### Optional (for production quality)

| Dependency | Install | Purpose |
|------------|---------|---------|
| ElevenLabs API key | [elevenlabs.io](https://elevenlabs.io) | Premium TTS narration (Jony Ive voice) |
| ffmpeg | `brew install ffmpeg` | Convert audio to MP3 (smaller files) |
| macOS `say` + `afconvert` | Built-in on macOS | Fallback TTS (Daniel voice, outputs WAV) |
| Suno API key | [api.box](https://www.api.box) | AI-generated background music |

### ElevenLabs Setup

1. Create a free account at [elevenlabs.io](https://elevenlabs.io)
2. Navigate to **Profile + API key** in the sidebar
3. Copy your API key
4. Add to your `.env` file:

```bash
ELEVENLABS_API_KEY=your-api-key-here
```

Also add to `.env.example` (commented out) for team documentation:

```bash
# ELEVENLABS_API_KEY=your-elevenlabs-api-key
```

**Voice selection**: The default voice is "Daniel" (`onwK4e9ZLuTAKqWW03F9`) — British, calm.
Browse [elevenlabs.io/voice-library](https://elevenlabs.io/voice-library) and update
the `VOICE_ID` in `scripts/generate-narration.ts` if a better match is found.

**Free tier limits**: ~10,000 characters/month. The full narration script is ~600 characters,
so you can regenerate ~16 times per month on the free tier.

## Workflow Overview

```
1. Create help page       → React component with collapsible sections
2. Generate illustrations → AI image generation tool (GenerateImage)
3. Build Remotion video   → Animated scenes with narration subtitles
4. Generate TTS audio     → ElevenLabs API or macOS `say` fallback
5. Generate music         → Suno AI background music (optional)
6. Render final video     → npm run remotion:render
7. GitHub README          → Embed screenshots + video in README.md
```

## Phase 1: Help Page

Create an in-app help page at `src/app/(dashboard)/help/page.tsx`.

### Structure pattern

```tsx
// Collapsible section wrapper
function HelpSection({ id, icon, title, description, children, defaultOpen }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <Card id={id}>
      <button onClick={() => setOpen(o => !o)}>
        {/* Header with icon, title, description, chevron */}
      </button>
      {open && <CardContent>{children}</CardContent>}
    </Card>
  );
}

// Step-by-step instruction
function Step({ number, title, children }) { /* numbered step */ }

// Pro tip callout
function Tip({ children }) { /* highlighted tip box */ }

// Screenshot placeholder
function Screenshot({ src, alt, caption }) { /* Next/Image with caption */ }
```

### Key sections to include

1. **Table of Contents** — auto-generated from section data with anchor links
2. **Getting Started** — first-time user orientation (default open)
3. **Feature sections** — one per major feature (Dashboard, Clients, Extensions, etc.)
4. **Product Video** — embedded `<video>` element pointing to rendered MP4
5. **FAQ / Troubleshooting** — common questions

### Writing guidelines

- Target audience: users with **low technical knowledge**
- Write as a **senior technical writer** — clear, friendly, no jargon
- Every section has numbered steps with screenshots
- Include "Tip" callouts for pro tips
- Use Tailwind v4 syntax (`mt-3!` not `!mt-3`)

## Phase 2: Screenshots / Illustrations

Since browser automation for screenshots can be unreliable, use AI-generated illustrations.

### Using the GenerateImage tool

```
GenerateImage({
  description: "Modern flat illustration of a monitoring dashboard with
    stat cards showing Total Clients, Extensions, Security Issues.
    Dark theme, clean UI, subtle orange accents.",
  filename: "dashboard.png"
})
```

Place generated images in `public/help/`:

```
public/help/
├── dashboard.png
├── clients.png
├── wizard.png
└── product-tour.mp4   (rendered later)
```

Reference in the help page:

```tsx
<Screenshot src="/help/dashboard.png" alt="Dashboard overview" caption="The main dashboard" />
```

## Phase 3: Remotion Product Video

### Directory structure

```
remotion/
├── index.ts          # registerRoot entry point
├── Root.tsx          # Composition definitions
└── ProductTour.tsx   # All scenes + narration script
```

### Composition setup (`Root.tsx`)

```tsx
import { Composition } from "remotion";
import { ProductTour } from "./ProductTour";

export const RemotionRoot = () => (
  <Composition
    id="ProductTour"
    component={ProductTour}
    durationInFrames={30 * 45}  // 45 seconds at 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

### Scene pattern

Each scene follows this structure:

```tsx
function SceneComponent() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: DARK_BG, padding: 80 }}>
      <SceneAudio scene="scene-name" />           {/* TTS audio */}
      <FadeInText fontSize={56}>Title</FadeInText> {/* Animated heading */}
      {/* Scene-specific content with spring/interpolate animations */}
      <NarrationSubtitle text={NARRATION_SCRIPT.sceneName} />  {/* Subtitles */}
    </AbsoluteFill>
  );
}
```

### Recommended scenes (7 total, ~75 seconds)

Durations are **dynamic** — driven by narration audio length (see Phase 5).
The video includes a **1.5s lead-in** (dark + exponential volume ramp) and
a **4s end card** with social links that fades to black.

| # | Scene | ~Duration | Content |
|---|-------|-----------|---------|
| — | Lead-in | 1.5s | Dark screen, music fades in (exponential t^2.5) |
| 1 | Intro | 13s | Logo + tagline + brand identity |
| 2 | Dashboard | 12s | Stat cards with spring animations |
| 3 | Clients | 12s | Client list with slide-in rows |
| 4 | Wizard | 11s | Step indicator with progressive activation |
| 5 | Security | 11s | Feature grid with staggered fade-in |
| 6 | Outro | 11s | Logo + CTA + credits + website (highlight blog) |
| 7 | End Card | 7s | 4 QR codes (website, GitHub, YouTube, X) + scale-up finale |

### Lead-in and end card

The lead-in uses an **exponential volume curve** (`Math.pow(t, 2.5)`) because
human hearing follows a logarithmic scale (Weber-Fechner law). A linear ramp
sounds "sudden" in the middle; the power curve feels perceptually smooth.

The end card shows 4 QR codes with social/website links (staggered slide-up).
**No fade-to-black** — the QR codes stay fully visible so viewers can scan them.
In the **final 2 seconds**, the entire card scales up dramatically (1.0 → 1.5)
with the T3 Monitoring logo, creating a confident, cinematic close.
The "Find us on" heading scales up in sync but also **moves upward** (-120px)
so it doesn't get covered by the expanding QR code row.

QR codes are rendered inline using `qrcode.react` (`npm install qrcode.react`).

```tsx
export const LEAD_IN_FRAMES = Math.round(30 * 1.5); // 45 frames
export const END_CARD_FRAMES = Math.round(30 * 7);   // 210 frames
```

These are added to `TOTAL_FRAMES` in `Root.tsx` for the composition duration.

#### End card links

| # | Platform | Handle | Highlight |
|---|----------|--------|-----------|
| 1 | Website | webconsulting.at | Orange border, `/blog` callout with description |
| 2 | GitHub | @dirnbauer | — |
| 3 | YouTube | @webconsulting-curt | — |
| 4 | X | @KDirnbauer | — |

The website card is **emphasized**: orange handle text, orange QR border,
and a `/blog` pill badge below — glass-style container with orange border,
glow shadow, and "Tutorials & deep dives" label.

#### QR code pattern

```tsx
import { QRCodeSVG } from "qrcode.react";

<QRCodeSVG value="https://webconsulting.at" size={140}
  bgColor="#ffffff" fgColor="#0f172a" level="M" />
```

Each social card shows: platform icon + handle, QR code (white bg, dark fg,
rounded container), URL text, and optional highlight callout.

### Animation toolkit

```tsx
// Fade + slide up
const opacity = interpolate(frame - delay, [0, fps * 0.6], [0, 1], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});

// Spring bounce for cards
const scale = spring({ fps, frame: frame - i * 8, config: { damping: 80 } });

// Staggered slide-in for list items
const slideX = interpolate(frame - i * 10, [0, fps * 0.5], [100, 0], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
```


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
