# web/assets

Brand image assets used by the JSX reference and to be embedded by
`scripts/build_deck.py` when generating .pptx decks.

Expected files (drop in as they become available):
- `logo-noba.png`     — dark NOBA wordmark (for paper backgrounds)
- `logo-noba-neg.png` — light NOBA wordmark (for dark backgrounds)
- `arrow.png`         — bottom-right arrow glyph (optional; SVG is also fine inline)

Until these exist, the JSX atoms render a text placeholder for the logo
and an inline SVG for the arrow — both visually accurate enough for
reference purposes. Replace with real art files without changing atom code.
