# Image-model reference pipeline (optional)

Use an image model (OpenAI **GPT Image 2** or Google **Gemini / Nano Banana**) to
*ideate* an icon, then **redraw the result as a clean TYPO3 v14 SVG**. The raster
is a reference, never the shipped asset.

## Why reference-only, never ship the raster

TYPO3 v14 backend icons are **monochrome line-art SVGs**: `currentColor` for the
silhouette, one optional accent, transparent background, crisp at 16px and 64px,
and they must flip with the light/dark scheme. Image models emit **raster PNG**.
Shipping the PNG (or a naive auto-trace of it) gives fuzzy edges, baked-in colors
that break dark mode, and bloated paths — the exact "junk" this skill exists to
prevent. So the model informs the *silhouette and composition*; a human/agent then
authors the SVG to spec and runs `verify-icon.sh`.

This stage is **optional**. For simple glyphs, authoring the SVG directly from the
icon's meaning is usually faster and cleaner than redrawing a raster. Reach for the
image model when a metaphor is non-obvious or you want to explore a family look.

## The two scripts

```
scripts/generate-icon-reference.sh "<concept>" <out.png> [--accent "..."] [--transparent] [--family "..."]
scripts/verify-icon.sh <icon.svg> [module|small|content]
```

`generate-icon-reference.sh` picks the model from whichever key is present
(`OPENAI_API_KEY` → GPT Image, else `GEMINI_API_KEY`/`GOOGLE_API_KEY` → Gemini),
writes a reference PNG, and reminds you to redraw it. `verify-icon.sh` is the hard
gate — it fails on wrong viewBox, embedded raster, scheme-breaking fills, missing
`currentColor`, background rects, or `prefers-color-scheme`.

## Verified model facts (mid-2026 — confirm against live docs)

Sources: `developers.openai.com/api/docs/guides/image-generation`,
`ai.google.dev/gemini-api/docs/image-generation`. APIs change — re-verify before
relying on these.

### OpenAI GPT Image — `POST https://api.openai.com/v1/images/generations`
- Auth: `Authorization: Bearer $OPENAI_API_KEY`. JSON body with `model` + `prompt`.
- Models: **`gpt-image-2`** (current/recommended, the "GPT Image 2" / "ChatGPT Image 2.0"),
  `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`, `chatgpt-image-latest`.
- **Transparency trap:** `gpt-image-2` does **not** support `background:"transparent"`.
  Only `gpt-image-1` / `gpt-image-1.5` / `gpt-image-1-mini` do — and those are
  deprecation-flagged. For icon references this rarely matters: prompt `gpt-image-2`
  for a **flat white background** and drop it in the redraw. Use `--transparent`
  (→ `gpt-image-1-mini` + `background:"transparent"`) only if you truly need an
  alpha raster.
- Params: `size` ∈ `1024x1024|1536x1024|1024x1536|auto` (gpt-image-1/1.5 only these;
  gpt-image-2 also accepts custom/larger). `quality` ∈ `low|medium|high|auto` (NOT
  dall-e's `standard|hd`). `output_format` ∈ `png|webp|jpeg`. **Do not** send
  `response_format` (invalid for gpt-image).
- Response: **always** base64 at `data[0].b64_json` (no `url`). Base64-decode it.
- Gotchas: the org may need **API Organization Verification** or calls are rejected;
  cost scales with model+quality+size (`gpt-image-1-mini` cheapest); `platform.openai.com/docs`
  now redirects to `developers.openai.com`.

### Google Gemini "Nano Banana" — `:generateContent` (v1beta)
- `POST https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent`,
  header `x-goog-api-key: $GEMINI_API_KEY`.
- Models: `gemini-2.5-flash-image` (stable), `gemini-3-pro-image-preview` ("Nano Banana Pro", preview).
- Body: `{contents:[{parts:[{text:PROMPT}]}], generationConfig:{responseModalities:["IMAGE"]}}`.
- Response: base64 at `candidates[0].content.parts[].inlineData.data` (mime `image/png`).
- Gotchas: `responseModalities` must include `IMAGE`; **no transparent-bg option**;
  every image carries a **SynthID watermark**; endpoint is `v1beta`, not `v1`.

## Prompt template (icon reference)

The generator builds this for you, but the shape is:

```
A single centered pictographic UI icon representing: {concept}. Exactly one small
accent detail: {accent}. Flat 2D line-art, one uniform medium-weight dark stroke on
a plain solid white background, no color fills, no gradients, no drop shadows, no 3D,
no perspective, no background scene, no text/letters/numbers. {family}. Simple
geometric shapes, minimal detail (one clear idea), crisp at 16x16 px. Symmetrical.
```

**Always avoid:** gradients, drop shadows, 3D/bevel, photorealism, colored fills,
background scenes, text in the image, busy detail.

**Two field-tested tips:**
- Vague adjectives ("minimalist", "clean", "modern") underperform — name concrete
  shapes and the metaphor instead ("a shield outline with a check mark inside").
- Ask for a **plain white** background, not transparent: Gemini often renders the
  word "transparent" as a literal gray checkerboard, and `gpt-image-2` ignores it.
  The redraw discards the background anyway.

**Family cohesion:** pass the SAME `--family` string to every sibling icon
(e.g. `"centered glyph, 8px padding on a 64 grid, 4px stroke"`) so the set shares a
grid, stroke weight, and padding. Redraw all siblings in one sitting and compare at
16px.

## Evaluate the reference before redrawing

- Does the silhouette read at 16px? (squint / shrink it)
- Is there one clear metaphor, not five tiny details?
- Symmetric, even padding? Single stroke weight?
If not, regenerate with a tighter concept — don't redraw a weak reference.

## Redraw → verify → register

1. Author the SVG by hand from the reference: correct viewBox (`0 0 64 64` module,
   `0 0 16 16` small), `currentColor` silhouette, one accent (a fixed brand hex is
   fine for a family accent if it reads on both schemes, else
   `var(--icon-color-accent, #ff8700)`), transparent background, minimal markup.
2. `verify-icon.sh <file> <type>` — must print `RESULT: PASS`.
3. Register in `Configuration/Icons.php`, wire consumers, clear caches, check both
   light and dark in the real backend context.
