#!/usr/bin/env bash
#
# generate-icon-reference.sh — produce a RASTER icon REFERENCE for a TYPO3 v14 icon.
#
# IMPORTANT: the PNG this writes is a *design reference*, never the shipped asset.
# TYPO3 v14 backend icons are monochrome line-art SVGs (currentColor + one accent,
# transparent background). This script gives you a clean reference glyph that an
# agent/human then REDRAWS as a conformant SVG (see verify-icon.sh). Shipping the
# raster — or a naive auto-trace of it — is exactly the junk this skill avoids.
#
# Model selection (whichever key is present; OpenAI preferred when both are set):
#   OPENAI_API_KEY              -> OpenAI GPT Image   (default model: gpt-image-2)
#   GEMINI_API_KEY / GOOGLE_API_KEY -> Google Gemini  (default: gemini-2.5-flash-image, "Nano Banana")
#
# Overrides:
#   OPENAI_IMAGE_MODEL   (default gpt-image-2; --transparent forces gpt-image-1-mini)
#   GEMINI_IMAGE_MODEL   (default gemini-2.5-flash-image)
#
# Usage:
#   generate-icon-reference.sh "<concept>" [out.png] [--accent "<accent element>"] [--transparent] [--family "<shared grid>"]
#
# Examples:
#   generate-icon-reference.sh "agent streaming events to a UI speech bubble" module-agui.ref.png \
#       --accent "a single spark mark top-right" --family "centered glyph, 8px padding, 4px stroke"
#
# Notes on the models (verified mid-2026, official docs):
#   - gpt-image-2 is current/recommended but does NOT support transparent backgrounds.
#     We therefore prompt for a FLAT WHITE background and drop it in the redraw.
#     --transparent switches to gpt-image-1-mini + background:transparent (deprecation-flagged).
#   - GPT-image models always return base64 at data[0].b64_json (no url, no response_format).
#   - GPT-image may require API Organization Verification on the OpenAI org.
#   - Gemini returns base64 at candidates[0].content.parts[].inlineData.data; carries a SynthID
#     watermark and has no transparent-bg option.
#
set -euo pipefail

die() { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }
need curl; need jq; need base64

[ $# -ge 1 ] || die 'usage: generate-icon-reference.sh "<concept>" [out.png] [--accent "..."] [--transparent] [--family "..."]'

concept="$1"; shift
out="icon-reference.png"
accent=""
family="centered single glyph, generous even padding, one uniform medium stroke weight"
transparent=0

# First positional after concept (if not a flag) is the output path.
if [ $# -ge 1 ] && [[ "$1" != --* ]]; then out="$1"; shift; fi
while [ $# -gt 0 ]; do
  case "$1" in
    --accent) accent="${2:-}"; shift 2;;
    --family) family="${2:-}"; shift 2;;
    --transparent) transparent=1; shift;;
    *) die "unknown arg: $1";;
  esac
done

# Prompt tuned to yield a reference that translates cleanly into v14 line-art:
# one centered pictogram, flat, single stroke weight, no color/gradient/shadow/3D/text,
# legible at 16px. Background is flat white for gpt-image-2 (dropped in the redraw);
# transparent only on the gpt-image-1-mini path.
bg_clause="on a plain solid white background"
[ "$transparent" -eq 1 ] && bg_clause="on a fully transparent background"
accent_clause=""
[ -n "$accent" ] && accent_clause=" Exactly one small accent detail: ${accent}."

prompt="A single centered pictographic user-interface icon representing: ${concept}.${accent_clause} \
Flat 2D line-art, one uniform medium-weight dark stroke ${bg_clause}, no color fills, no gradients, \
no drop shadows, no 3D, no perspective, no background scene, no text, letters or numbers. \
${family}. Simple geometric shapes, minimal detail expressing one clear idea, crisp and unmistakable \
when scaled down to 16x16 pixels. Symmetrical, balanced composition."

if [ -n "${OPENAI_API_KEY:-}" ]; then
  model="${OPENAI_IMAGE_MODEL:-gpt-image-2}"
  body=$(jq -n --arg m "$model" --arg p "$prompt" \
    '{model:$m, prompt:$p, size:"1024x1024", quality:"high", output_format:"png", n:1}')
  if [ "$transparent" -eq 1 ]; then
    # gpt-image-2 rejects transparent; use the transparent-capable (deprecation-flagged) mini.
    model="${OPENAI_IMAGE_MODEL:-gpt-image-1-mini}"
    body=$(jq -n --arg m "$model" --arg p "$prompt" \
      '{model:$m, prompt:$p, background:"transparent", size:"1024x1024", quality:"high", output_format:"png", n:1}')
  fi
  echo "→ OpenAI GPT Image: $model (transparent=$transparent)" >&2
  resp=$(curl -fsS https://api.openai.com/v1/images/generations \
    -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" -d "$body") \
    || die "OpenAI request failed (check key, org verification, model availability)"
  echo "$resp" | jq -e '.data[0].b64_json' >/dev/null 2>&1 \
    || die "unexpected OpenAI response: $(echo "$resp" | jq -c '.error // .' 2>/dev/null | head -c 300)"
  echo "$resp" | jq -r '.data[0].b64_json' | base64 --decode > "$out"

elif [ -n "${GEMINI_API_KEY:-${GOOGLE_API_KEY:-}}" ]; then
  key="${GEMINI_API_KEY:-${GOOGLE_API_KEY}}"
  model="${GEMINI_IMAGE_MODEL:-gemini-2.5-flash-image}"
  echo "→ Google Gemini (Nano Banana): $model" >&2
  body=$(jq -n --arg p "$prompt" \
    '{contents:[{parts:[{text:$p}]}], generationConfig:{responseModalities:["IMAGE"]}}')
  resp=$(curl -fsS "https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent" \
    -H "x-goog-api-key: $key" -H "Content-Type: application/json" -d "$body") \
    || die "Gemini request failed (check key, model availability)"
  data=$(echo "$resp" | jq -r '.candidates[0].content.parts[]? | select(.inlineData!=null) | .inlineData.data' | head -1)
  [ -n "$data" ] || die "no image in Gemini response: $(echo "$resp" | jq -c '.error // .promptFeedback // .' 2>/dev/null | head -c 300)"
  echo "$data" | base64 --decode > "$out"

else
  cat >&2 <<'EOF'
ERROR: no image-model API key found.
  Set one of:
    export OPENAI_API_KEY=sk-...     # GPT Image 2 (preferred)
    export GEMINI_API_KEY=...        # Google "Nano Banana"
  Then re-run. Without a key, SKIP this stage and author the v14 SVG directly
  from the icon's meaning per the skill rules — that still produces a perfect icon.
EOF
  exit 3
fi

bytes=$(wc -c < "$out" | tr -d ' ')
[ "$bytes" -gt 100 ] || die "output looks empty ($bytes bytes)"
echo "✓ reference saved: $out ($bytes bytes) — now REDRAW it as a clean v14 SVG and run verify-icon.sh" >&2
