# Phase 5: TTS Audio Generation

Continues `webconsulting-create-documentation` from [full guide](full-guide.md).

## Phase 5: TTS Audio Generation

### Script: `scripts/generate-narration.ts`

The script supports two backends and auto-generates `remotion/narration-format.ts`
so the video composition always uses the correct file extension.

| Backend | Trigger | Output | Quality |
|---------|---------|--------|---------|
| ElevenLabs | `ELEVENLABS_API_KEY` set in `.env` | `.mp3` | Production |
| macOS `say` + `afconvert` | No API key, macOS detected | `.wav` | Development preview |

```bash
# Production: use ElevenLabs (add key to .env first)
npm run narration:generate

# Development: macOS fallback (no key needed)
npm run narration:generate
```

The script automatically:
1. Cleans old audio files (prevents mixing formats)
2. Generates audio files in `public/narration/`
3. Probes each file's duration using `afinfo` (macOS) or `ffprobe`
4. Writes `remotion/narration-format.ts` with the correct extension (`"mp3"` or `"wav"`)
5. Writes `remotion/narration-durations.ts` with per-scene frame counts (audio + 2s padding)
6. The Remotion composition imports both configs for synced playback

### ElevenLabs voice settings for Jony Ive style

```json
{
  "voice_id": "onwK4e9ZLuTAKqWW03F9",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.75,
    "similarity_boost": 0.70,
    "style": 0.35,
    "use_speaker_boost": true
  }
}
```

### Audio file location

```
public/narration/
├── intro.mp3 (or .wav)
├── dashboard.mp3
├── clients.mp3
├── wizard.mp3
├── security.mp3
└── outro.mp3

remotion/
├── narration-format.ts      ← auto-generated, audio extension ("mp3" | "wav")
└── narration-durations.ts   ← auto-generated, per-scene frame counts + total
```

### Audio-video sync (critical)

Scene durations are driven by audio length, not hardcoded. The generate script:
1. Probes each audio file's duration (e.g., intro = 8.5s)
2. Adds 2s padding for visual animation breathing room
3. Writes frame count: `ceil((8.5 + 2) * 30) = 317 frames`
4. `ProductTour.tsx` imports these and uses them for `Sequence` durations

Each scene also has:
- **Audio fade-out** (last 1s) — prevents abrupt cut-off between scenes
- **Visual fade-to-black** (last 0.5s) — smooth scene transitions
- **Total video duration** is computed from sum of all scene frames

### Important: format config

`staticFile()` in Remotion does NOT throw when a file is missing — it returns a URL
that 404s at render time. That's why the generate script writes `narration-format.ts`
to ensure the video only references files that actually exist. Always run
`npm run narration:generate` before `npm run remotion:render`.

### Full narration script (prompt)

This is the exact text sent to ElevenLabs. Copy and adapt for your product:

The narration text lives in `remotion/ProductTour.tsx` as `NARRATION_SCRIPT`.
The generate script imports it — **never edit narration text in two places**.

To see the current script, read `NARRATION_SCRIPT` in `ProductTour.tsx`.
To change it, edit only that file, then re-run:

```bash
npm run narration:generate   # Regenerates audio from the updated text
npm run remotion:render      # Subtitles already read from the same source
```
