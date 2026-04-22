# web/assets

Brand image assets. Drop the real PNGs from the NOBA brand manual at
the paths below. When present, the python-pptx builders in
`scripts/build_deck.py` embed them via `add_picture`; when missing, a
shape-drawn fallback is used and a one-line warning is printed to
stderr.

## Required files

| File | Purpose | Recommended spec |
|---|---|---|
| `logo-noba.png`     | Dark NOBA wordmark — used on paper (white) slides | Transparent background, solid black `#1A1A1A`. Aspect ratio **7.68 : 1** (e.g. 1920×250). The builder renders it at 368×48 px at slide scale, so anywhere from 368×48 to ~1920×250 will look crisp. |
| `logo-noba-neg.png` | Light NOBA wordmark — used on dark (`#393939`) slides | Same spec, white `#FFFFFF` fill. |
| `arrow.png`         | Right-pointing arrow, solid black — used inline before bottom captions | Transparent background, solid black. Aspect ratio **1.03 : 1**. The builder renders it at 36×35 px at slide scale. |
| `arrow-neg.png`     | Same arrow, white | Same spec, white fill. |

## SVG versions

Kept as an approximation for the HTML reference in `web/templates/`. The
SVGs render in-browser; python-pptx only uses the PNGs. When the brand
PNGs land, the SVGs can stay as fallbacks for any web-only viewer.

## Sizes are hints, not hard constraints

python-pptx resizes the image to the target on-slide dimensions. Any
reasonable resolution above the target pixel size will look good;
lower-res will look fuzzy when PowerPoint zooms. Use at least 2× the
target size (i.e. logo ≥ 736×96, arrow ≥ 72×70) for a safety margin on
4K displays.
