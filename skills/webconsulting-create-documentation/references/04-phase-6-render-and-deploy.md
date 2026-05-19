# Phase 6: Render & Deploy

Continues `webconsulting-create-documentation` from [full guide](full-guide.md).

## Phase 6: Render & Deploy

```bash
# Full pipeline: narration → music → render
npm run narration:generate   # ElevenLabs narration (or macOS fallback)
npm run music:generate       # Suno background music (optional)
npm run remotion:render      # Final MP4 with both audio layers

# Preview in Remotion Studio
npm run remotion:studio

# Output: public/help/product-tour.mp4
# The help page references the video:
# <video src="/help/product-tour.mp4" controls />
```

### package.json scripts

```json
{
  "remotion:studio": "npx remotion studio remotion/index.ts",
  "remotion:render": "npx remotion render remotion/index.ts ProductTour public/help/product-tour.mp4",
  "narration:generate": "tsx scripts/generate-narration.ts",
  "music:generate": "tsx scripts/generate-music.ts"
}
```
