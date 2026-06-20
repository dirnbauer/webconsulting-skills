#!/usr/bin/env bash
#
# verify-icon.sh — hard conformance gate for a TYPO3 v14 icon SVG.
#
# Exits non-zero if the SVG would render as "junk" in the v14 backend: hardcoded
# scheme-breaking fills, a solid background, a wrong viewBox for its type, raster
# data, or no currentColor. Run this on every authored/redrawn icon before
# registering it.
#
# Usage:
#   verify-icon.sh <icon.svg> [module|small|content]
#     module  -> expects viewBox 0 0 64 64 (module-*.svg, Extension.svg)
#     small   -> expects viewBox 0 0 16 16 (actions/record/plugin)
#     content -> Content Blocks wizard thumbnail (square viewBox; color+bg allowed)
#     (omitted -> inferred from filename)
#
set -euo pipefail
svg="${1:?usage: verify-icon.sh <icon.svg> [module|small|content]}"
[ -f "$svg" ] || { echo "ERROR: no such file: $svg" >&2; exit 2; }
kind="${2:-auto}"
base="$(basename "$svg")"

if [ "$kind" = auto ]; then
  case "$base" in
    module-*|Extension.svg) kind=module;;
    actions-*|record-*|plugin-*) kind=small;;
    *) case "$svg" in */ContentBlocks/*) kind=content;; *) kind=module;; esac;;
  esac
fi

content="$(cat "$svg")"
fail=0
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=1; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }

echo "verify-icon: $svg  (type: $kind)"

# 1. Must be a real SVG, not embedded raster.
echo "$content" | grep -qi '<svg' || bad "not an <svg> document"
if echo "$content" | grep -qiE 'data:image/(png|jpe?g|webp)|<image[ >]'; then
  bad "contains embedded raster (data:image / <image>) — author real vector paths, do not ship a traced bitmap"
else
  ok "pure vector (no embedded raster)"
fi

# 2. viewBox per type.
vb="$(echo "$content" | grep -o 'viewBox="[^"]*"' | head -1 | sed 's/viewBox="//;s/"//')"
case "$kind" in
  module)  [ "$vb" = "0 0 64 64" ] && ok "viewBox $vb" || bad "viewBox is '$vb' — module/Extension icons must be 0 0 64 64";;
  small)   [ "$vb" = "0 0 16 16" ] && ok "viewBox $vb" || bad "viewBox is '$vb' — action/record/plugin icons must be 0 0 16 16";;
  content) echo "$vb" | grep -qE '^0 0 ([0-9]+) \1$' && ok "viewBox $vb (square)" || warn "viewBox '$vb' is not square (Content Blocks thumbs are usually square)";;
esac

# 3/4/5 apply to backend icons (module/small), where light/dark theming is mandatory.
if [ "$kind" != content ]; then
  # 3. No scheme-breaking hardcoded fills/strokes.
  if echo "$content" | grep -qiE '(fill|stroke)\s*[:=]\s*"?(#000(000)?|#111|#222|#333|#fff(fff)?|#eee|white|black)"?'; then
    bad "hardcoded #000/#111/#222/#333/#eee/#fff/white/black on fill or stroke (vanishes in one scheme)"
  else
    ok "no scheme-breaking hardcoded black/white/gray"
  fi
  # 4. Uses currentColor for the primary geometry.
  echo "$content" | grep -q 'currentColor' && ok "uses currentColor" \
    || bad "no currentColor — the primary silhouette must use currentColor so it flips light/dark"
  # 5. No full-canvas background rectangle (heuristic without PCRE lookahead).
  bgrect="$(echo "$content" | grep -oiE '<rect[^>]*>' | grep -iE 'width="(100%|64|48|16)"' | grep -iE 'fill=' | grep -viE 'fill="none"' || true)"
  if [ -n "$bgrect" ]; then
    warn "a full-canvas <rect> with a fill may be a solid background — remove it so the scheme shows through"
  else
    ok "no obvious solid background rect"
  fi
  # 6. Accent guidance (informational): a fixed brand accent hex is allowed if it
  #    contrasts in both schemes; var(--icon-color-accent,#ff8700) is the Core idiom.
  if echo "$content" | grep -q 'var(--icon-color-accent'; then
    ok "accent uses var(--icon-color-accent, …) (Core idiom)"
  elif echo "$content" | grep -qiE '(fill|stroke)\s*[:=]\s*"?#[0-9a-f]{3,6}'; then
    warn "fixed accent hex present — fine for a brand-color family accent IF it reads on both light+dark; otherwise use var(--icon-color-accent,#ff8700)"
  fi
fi

# 7. prefers-color-scheme must not drive the icon.
echo "$content" | grep -qi 'prefers-color-scheme' \
  && bad "uses prefers-color-scheme — the Core switches schemes via a root attribute, not media queries" \
  || ok "no prefers-color-scheme dependency"

echo
if [ "$fail" -eq 0 ]; then echo "RESULT: PASS"; else echo "RESULT: FAIL — fix the ✗ items before registering"; fi
exit "$fail"
