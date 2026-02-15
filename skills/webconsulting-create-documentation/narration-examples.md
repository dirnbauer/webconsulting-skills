# Narration Examples — Jony Ive Style

Full narration script from the T3 Monitoring product tour, plus guidelines for writing new narration.

## Complete Script

Scene durations are **driven by audio length** (not hardcoded). The generate script
probes each file and writes `remotion/narration-durations.ts` with frame counts.
Timings below are approximate for reference.

### Scene 1: Intro (~7.9s audio → 9.9s scene)

> Imagine seeing every TYPO3 installation you manage — health, security, updates — in one place, instantly. That's T3 Monitoring.

### Scene 2: Dashboard (~10.0s audio → 12.0s scene)

> Your dashboard gives you the full picture. Client health, extension status, security alerts — everything you need, the moment you need it.

### Scene 3: Clients (~9.4s audio → 11.4s scene)

> Every website. Every client. One unified view — so you always know exactly where things stand, without digging through servers.

### Scene 4: Wizard (~9.4s audio → 11.4s scene)

> Onboarding a new client takes four steps. Enter the details, connect, and you're monitoring. It really is that quick.

### Scene 5: Security (~7.1s audio → 9.1s scene)

> When a vulnerability appears, you'll see it immediately. No surprises. No delays. Just the clarity to act fast.

### Scene 6: Outro (~10.3s audio → 12.3s scene)

> T3 Monitoring. Built for agencies who care about their clients. Open source. Reliable. Ready when you are.

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

- Lead with what the user **gets**, not what the product does.
- "Imagine seeing every installation" not "This product shows you installations"
- "It really is that quick." not "The process is very fast."
- Short fragments still work, but mix in conversational confidence.

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
