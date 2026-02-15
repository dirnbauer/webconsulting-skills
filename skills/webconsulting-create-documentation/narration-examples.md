# Narration Examples — Jony Ive Style

Full narration script from the T3 Monitoring product tour, plus guidelines for writing new narration.

## Complete Script

Scene durations are **driven by audio length** (not hardcoded). The generate script
probes each file and writes `remotion/narration-durations.ts` with frame counts.
Timings below are approximate for reference.

### Scene 1: Intro (~8.5s audio → 10.6s scene)

> We believe in something profoundly simple. The ability to see everything — at a glance. This is T3 Monitoring.

### Scene 2: Dashboard (~10.2s audio → 12.2s scene)

> Your dashboard. Beautifully considered. Every metric, thoughtfully placed, to give you immediate clarity across all your installations.

### Scene 3: Clients (~9.8s audio → 11.8s scene)

> Every TYPO3 website. Every client. Connected, monitored, and deeply understood — all from a single, unified view.

### Scene 4: Wizard (~9.3s audio → 11.3s scene)

> Adding a new client should feel effortless. Four deliberate steps. No complexity. No confusion. Just, done.

### Scene 5: Security (~7.5s audio → 9.5s scene)

> Security isn't a feature. It's a foundation. The moment something needs your attention, you'll know.

### Scene 6: Outro (~10.7s audio → 12.7s scene)

> T3 Monitoring. Your TYPO3 installations — always under your care. Open source. Beautifully engineered. Unmistakably purposeful.

## The Prompt

This is the exact prompt used to produce the narration script above. Adapt it for new products:

```
You are Sir Jonathan Paul "Jony" Ive giving a keynote voiceover for a product video.
Write narration for a 6-scene product tour of [PRODUCT NAME].

Scenes:
1. Intro — what the product is and why it matters
2. Dashboard — the main overview screen
3. Client list — managing multiple entities
4. Wizard — the guided setup flow
5. Security — monitoring and alerts
6. Outro — closing statement with brand values

Rules:
- Each scene: 15–25 words. Short, declarative sentences.
- Start with the subject. "Your dashboard." not "The dashboard allows you to..."
- Use fragments for rhythm. "Connected, monitored, and deeply understood."
- Em dashes (—) for dramatic pauses.
- Aspirational tone: what the product means, not what it does.
- Avoid: "allows you to", "utilizes", "functionality", "in order to", "simple".
- Prefer: "effortless", "deliberate", "considered", "purposeful", "deeply".
- End with brand values (open source, beautiful engineering, purpose).
```

## Writing Guidelines

### Sentence structure

- Start with the **subject**, then add a period. Short fragments work.
- "Your dashboard." not "The dashboard allows you to..."
- "Four deliberate steps." not "There are four steps in the wizard."

### Word choice

| Avoid | Prefer |
|-------|--------|
| allows you to | lets you / gives you |
| utilizes | uses |
| functionality | feature |
| in order to | to |
| a number of | several / many |
| simple | effortless / deliberate |
| interface | view / experience |

### Rhythm patterns

1. **Statement. Expansion. Conclusion.**
   > "Security isn't a feature. It's a foundation. The moment something needs your attention, you'll know."

2. **Feature. Feature. Feature. Summary.**
   > "Connected, monitored, and deeply understood — all from a single, unified view."

3. **Aspiration. Contrast. Resolution.**
   > "Adding a new client should feel effortless. No complexity. No confusion. Just, done."

### Timing

- ~20 words per scene (audio typically runs 8–11 seconds at 140 WPM)
- Scene duration is auto-calculated: `ceil((audioSeconds + 2) * fps)` frames
- The 2s padding gives visual animations room to settle before and after speech
- Audio fades out over the last 1s; visual fades to black over the last 0.5s
- Use em dashes (—) for dramatic pauses in the text

### Voice direction (for ElevenLabs or voice actor)

- Speak at 140 WPM (slower than conversational)
- Slight upward inflection on product names
- Downward inflection at the end of declarative statements
- 0.5s pause at periods, 0.3s at commas
- No vocal fry, no uptalk on statements
