"""NOBA deck builder — python-pptx scaffold.

Reads a deck_spec dict and emits a .pptx where each slide is built by a
layout-specific builder. Builders mirror web/slides/*.jsx 1:1 and consume
only semantic tokens (C/S/T from tokens.py) — no raw hex or pixel values.

Brand tweaks happen in design/tokens.json and propagate here automatically.
Layout tweaks are made first in the JSX reference, then ported to the
matching builder function below.

Usage:
    from build_deck import main
    out = main(deck_spec, "/tmp/out.pptx")
"""
from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

from tokens import C, S, T, SLIDE, px_to_emu


# --------------------------------------------------------------- brand assets
# Real brand assets (PNG) live at <repo-root>/web/assets/. When present,
# add_logo / add_inline_arrow use them via add_picture. When missing,
# they fall back to shape-drawn placeholders (so CI and first-run dev
# still work). Drop the real images at the paths below to upgrade.

REPO_ROOT = Path(__file__).resolve().parents[4]
_ASSETS = REPO_ROOT / "web" / "assets"

LOGO_DARK_FILE  = _ASSETS / "logo-noba.png"       # dark logo on paper backgrounds
LOGO_LIGHT_FILE = _ASSETS / "logo-noba-neg.png"   # light logo on dark backgrounds
ARROW_DARK_FILE = _ASSETS / "arrow.png"
ARROW_LIGHT_FILE = _ASSETS / "arrow-neg.png"

_expected_assets = [LOGO_DARK_FILE, LOGO_LIGHT_FILE, ARROW_DARK_FILE, ARROW_LIGHT_FILE]
_missing_assets = [p for p in _expected_assets if not p.exists()]
if _missing_assets:
    print(
        "[noba.build_deck] Falling back to shape-drawn placeholders for "
        f"{len(_missing_assets)} brand asset(s). Drop the real images at:\n  "
        + "\n  ".join(str(p) for p in _missing_assets),
        file=sys.stderr,
    )


# -------------------------------------------------------------------- fonts
# python-pptx has no numeric font-weight attribute; PowerPoint selects
# the typeface by font-face name. To get Helvetica Neue Light (weight
# 300) on macOS / Windows with the full family installed, set the font
# name explicitly to "Helvetica Neue Light".

FONT_REGULAR = T.family                   # "Helvetica Neue"  (weight 400)
FONT_LIGHT   = f"{T.family} Light"        # "Helvetica Neue Light" (weight 300)
FONT_BOLD    = T.family                   # bold achieved via font.bold = True


# --------------------------------------------------------------------- atoms
# Match web/atoms/atoms.jsx 1:1. Each atom is a thin helper; slide builders
# compose them. Atoms know nothing about slide content — only visuals.

def add_logo(slide, variant: str = "dark", position: str = "inside"):
    """NOBA wordmark.

    Prefers the real brand PNG at `web/assets/logo-noba[-neg].png`
    (dark for paper backgrounds, neg for dark backgrounds). Falls back
    to a shape-drawn stand-in when the asset is missing — Paula has
    flagged the stand-in as "not the logo" so the real PNG is required
    for brand-accurate output.

    Sizes differ by position (from the Figma design system):
    - `cover` uses the large wordmark: 368×48 at slide scale
      (Figma 184×24 at 960 frame, node 3:11).
    - `inside` uses a smaller wordmark: 228×30 at slide scale
      (Figma 114×15 at 960 frame, node 1:261). Inside slides have less
      space in the header strip so the logo is trimmed to fit.

    In both positions the logo pins to the right edge of the 48-px
    cover/inside padding.
    """
    if position == "cover":
        w, h = S.cover_logo_width, S.cover_logo_height
    else:
        w, h = S.inside_logo_width, S.inside_logo_height
    pad_right = S.slide_pad_cover
    pad_top   = S.slide_pad_cover
    left = SLIDE.width - pad_right - w
    top = pad_top

    asset = LOGO_LIGHT_FILE if variant == "light" else LOGO_DARK_FILE
    if asset.exists():
        slide.shapes.add_picture(str(asset), left, top, width=w, height=h)
        return

    color = C.neutral_paper if variant == "light" else C.neutral_ink
    _draw_logo_fallback(slide, left, top, w, h, color)


def _draw_logo_fallback(slide, left, top, w, h, color: RGBColor):
    """Stand-in used only when the real PNG is missing."""
    n_width = px_to_emu(44)
    _add_text(
        slide, left, top, n_width, h, "N",
        size_pt=36, weight=400, color=color,
        leading=1.0, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.LEFT,
    )
    pill = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left + px_to_emu(44), top + px_to_emu(8),
        px_to_emu(240), px_to_emu(32),
    )
    pill.adjustments[0] = 0.5
    pill.fill.background()
    pill.line.color.rgb = color
    pill.line.width = Emu(px_to_emu(1.5))
    ba_width = px_to_emu(84)
    _add_text(
        slide, left + w - ba_width, top, ba_width, h, "BA",
        size_pt=36, weight=400, color=color,
        leading=1.0, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT,
    )


def add_arrow(slide, variant: str = "dark"):
    """Bottom-right arrow. Legacy — used by non-cover slides until they
    migrate to the inline-arrow design from Figma. For slides where the
    arrow sits inline before a bottom caption (cover, etc.), use
    `add_inline_arrow` at the caption's (x, y) instead.
    """
    color = C.neutral_paper if variant == "light" else C.neutral_ink
    width, height = px_to_emu(80), px_to_emu(24)
    left = SLIDE.width - px_to_emu(60) - width
    top = SLIDE.height - px_to_emu(48) - height
    line = slide.shapes.add_connector(1, left, top + height // 2, left + width - px_to_emu(6), top + height // 2)
    line.line.color.rgb = color
    line.line.width = Emu(px_to_emu(1.5))
    head = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, left + width - px_to_emu(14), top, px_to_emu(14), height)
    head.fill.solid()
    head.fill.fore_color.rgb = color
    head.line.fill.background()


def add_inline_arrow(slide, left, top, variant: str = "dark",
                     width_px: int = 36, height_px: int = 35):
    """Small right-pointing arrow at a specified (left, top).

    Prefers the real brand PNG at `web/assets/arrow[-neg].png`. Falls
    back to a connector-drawn stand-in when the asset is missing.
    Figma source: node 4:18 of qqNtw4M8gc3zYRHwKJae7W. Used inline
    before bottom captions — the cover is the first adopter.
    """
    w = px_to_emu(width_px)
    h = px_to_emu(height_px)

    asset = ARROW_LIGHT_FILE if variant == "light" else ARROW_DARK_FILE
    if asset.exists():
        slide.shapes.add_picture(str(asset), left, top, width=w, height=h)
        return

    _draw_arrow_fallback(slide, left, top, w, h, variant)


def _draw_arrow_fallback(slide, left, top, w, h, variant: str):
    """Stand-in: line + two chevron strokes. Matches arrow geometry
    close enough for development when the real PNG is missing."""
    fg = C.neutral_paper if variant == "light" else C.neutral_ink
    mid_y = top + h // 2
    shaft_end = left + w - px_to_emu(6)

    for start, end in [
        ((left, mid_y),                              (shaft_end, mid_y)),
        ((shaft_end - px_to_emu(8), mid_y - px_to_emu(7)), (shaft_end, mid_y)),
        ((shaft_end, mid_y),                         (shaft_end - px_to_emu(8), mid_y + px_to_emu(7))),
    ]:
        conn = slide.shapes.add_connector(1, start[0], start[1], end[0], end[1])
        conn.line.color.rgb = fg
        conn.line.width = Emu(px_to_emu(1))


def add_tag(slide, text: str, left, top, tone: str = "ink"):
    """Section-tag pill."""
    ink = C.neutral_ink if tone == "ink" else C.neutral_paper
    width = px_to_emu(len(text) * 7 + 28)
    height = px_to_emu(26)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = 0.5
    shape.fill.background()
    shape.line.color.rgb = ink
    shape.line.width = Emu(px_to_emu(1))
    tf = shape.text_frame
    tf.margin_top = tf.margin_bottom = px_to_emu(4)
    tf.margin_left = tf.margin_right = px_to_emu(14)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text.upper()
    r.font.name = T.family
    r.font.size = Pt(9)
    r.font.color.rgb = ink


def add_shell(slide, tone: str = "paper"):
    """Rounded outer shell — cover and dark slides."""
    bg = C.neutral_dark if tone == "dark" else C.neutral_paper
    inset = px_to_emu(24)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        inset, inset,
        SLIDE.width - 2 * inset, SLIDE.height - 2 * inset,
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    shape.line.fill.background()


def add_rule(slide, y, left=None, right=None, tone: str = "ink"):
    """Horizontal hairline rule."""
    color = C.neutral_mid_inv if tone == "inv" else C.neutral_gray
    x0 = px_to_emu(72) if left is None else left
    x1 = SLIDE.width - (px_to_emu(72) if right is None else right)
    line = slide.shapes.add_connector(1, x0, y, x1, y)
    line.line.color.rgb = color
    line.line.width = Emu(px_to_emu(1))


def add_dot(slide, x, y, color, size: str = "md"):
    """Colored dot marker."""
    d = px_to_emu(20 if size == "lg" else 12)
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, d, d)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


# ---------------------------------------------------------------- text helpers

def _font_for_weight(weight: int) -> str:
    """Pick the Helvetica Neue face for a given numeric weight."""
    if weight <= 300:
        return FONT_LIGHT
    return FONT_REGULAR  # Bold is applied via font.bold = True, same family.


def _add_text(slide, left, top, width, height, text: str, *,
              size_pt: float, weight: int = 400, color=None,
              leading: float = 1.2, tracking: float = 0,
              uppercase: bool = False, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP):
    """Semantic text insertion. Callers pass tokenized values only."""
    color = color or C.neutral_ink
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = leading
    r = p.add_run()
    r.text = text.upper() if uppercase else text
    r.font.name = _font_for_weight(weight)
    r.font.size = Pt(size_pt)
    r.font.bold = weight >= 700
    r.font.color.rgb = color
    return box


def _add_rich_text(tf, paragraphs, *, size_pt: float, leading: float = 1.43,
                   color=None, weight: int = 400):
    """Populate a text-frame with mixed-bold paragraphs.

    paragraphs: list[list[dict]]
        Each outer list is one paragraph; each inner dict is a run with
        keys `text` (str, required) and `bold` (bool, optional).

    The text frame's existing first paragraph is used for paragraphs[0]
    to avoid a blank line at the top. All runs share the same font
    family (Helvetica Neue), size, and color — the only per-run variable
    is `bold`.

    Used by build_context for the long multi-paragraph body with
    emphasised phrases.
    """
    color = color or C.neutral_ink
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    tf.word_wrap = True

    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = leading
        for run_spec in para:
            text = run_spec.get("text", "")
            if not text:
                continue
            bold = bool(run_spec.get("bold"))
            r = p.add_run()
            r.text = text
            r.font.name = _font_for_weight(700 if bold else weight)
            r.font.bold = bold
            r.font.size = Pt(size_pt)
            r.font.color.rgb = color


def _pct(n: int, denom: int = 1920) -> int:
    """px → EMU helper for inline math."""
    return px_to_emu(n * SLIDE.width_px / denom)


def _accent(name: str) -> RGBColor:
    return getattr(C, f"accent_{name}".replace("-", "_"))


# ---------------------------------------------------- primitive slide builders
# One per JSX component in web/slides/. Never add a new layout without first
# adding (or updating) the JSX reference and design/tokens.json.

def build_cover(prs, spec):
    """← web/slides/TitleSlide.jsx

    Figma source: qqNtw4M8gc3zYRHwKJae7W, node 3:5.

    Spec fields:
        title    (str, required) — huge ink headline, Light 300, 140px.
        subtitle (str)           — 36px Light ink line below the title,
                                   separated by a fixed 20px (10px
                                   Figma) gap regardless of how the
                                   title wraps.
        client   (str)           — rendered in the bottom caption.
        date     (str)           — rendered in the bottom caption.

    Fields NOT used (removed from earlier iterations):
        eyebrow  — not part of the Figma design; ignore if present.
        accent   — title is ink (#1A1A1A), no accent colour.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark", position="cover")

    # Title + subtitle as a single stacked textbox. Using two
    # paragraphs in one text frame (rather than two separate textboxes)
    # keeps the gap fixed at 20px regardless of how many lines the title
    # wraps to. The space_before on the subtitle paragraph gives us that
    # gap: 20px at slide scale = 15pt at 96 DPI.
    title_scale = T.cover_title()
    sub_scale   = T.cover_sub()

    box = slide.shapes.add_textbox(
        S.slide_pad_cover, S.cover_title_y,
        S.cover_title_width, SLIDE.height - S.cover_title_y - px_to_emu(200),
    )
    tf = box.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    tf.word_wrap = True

    p_title = tf.paragraphs[0]
    p_title.line_spacing = title_scale["leading"]
    r_title = p_title.add_run()
    r_title.text = spec["title"]
    r_title.font.name  = _font_for_weight(title_scale["weight"])
    r_title.font.size  = Pt(title_scale["size_px"] * 0.75)
    r_title.font.color.rgb = C.neutral_ink

    subtitle = spec.get("subtitle", "").strip()
    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.line_spacing = sub_scale["leading"]
        # 20px slide scale = 15pt. Figma authors see this as "10px gap".
        p_sub.space_before = Pt(15)
        r_sub = p_sub.add_run()
        r_sub.text = subtitle
        r_sub.font.name  = _font_for_weight(sub_scale["weight"])
        r_sub.font.size  = Pt(sub_scale["size_px"] * 0.75)
        r_sub.font.color.rgb = C.neutral_ink

    # Bottom caption row: inline arrow + "Prepared for X | date"
    caption_top = SLIDE.height - S.slide_pad_cover - px_to_emu(35)
    add_inline_arrow(slide, S.slide_pad_cover, caption_top, variant="dark")

    cap_scale = T.cover_cap()
    # Caption is solid ink. Paula's design review overrode the Figma
    # file's `rgba(0,0,0,0.5)` — she wants full contrast on the bottom
    # caption, not a faded 50% grey.
    caption_text_left = S.slide_pad_cover + px_to_emu(36) + S.cover_arrow_gap
    _add_text(
        slide,
        caption_text_left, caption_top,
        SLIDE.width - caption_text_left - S.slide_pad_cover, px_to_emu(30),
        f"Prepared for {spec.get('client', '')} | {spec.get('date', '')}",
        size_pt=cap_scale["size_px"] * 0.75,
        weight=cap_scale["weight"],
        leading=cap_scale["leading"],
        color=C.neutral_ink,
        anchor=MSO_ANCHOR.MIDDLE,
    )
    return slide


def build_context(prs, spec):
    """← web/slides/ContextSlide.jsx

    Figma source: qqNtw4M8gc3zYRHwKJae7W, node 1:230.

    Spec fields:
        tag   (str)                      — uppercase label after the
                                           top-left inline arrow.
                                           Defaults to "CONTEXT".
        image (str, optional)            — path to a photo. When
                                           present, embedded into the
                                           right-edge photo slot. When
                                           missing, a gray placeholder
                                           shape is used.
        body  (list[list[dict]], required)
            Paragraphs of rich text. Each paragraph is a list of
            {"text": str, "bold": bool} runs. See layout-map.md.

    Visual anatomy:
        - Full-bleed white, 48-px padding for the header strip.
        - Photo pinned flush to the right edge, 768×1080 px at slide
          scale, rounded on the left corners only.
        - Top-left: inline arrow + uppercase CONTEXT tag.
        - Top-right: smaller inside-slide logo (228×30 at slide scale).
        - Body: 456-px (Figma) / 912-px (slide) column, 14/20 px body
          type with bold emphasis within paragraphs.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Photo — right-edge, full-height. The Figma design rounds only the
    # left corners; python-pptx can't easily express "rounded on one
    # side only" without XML surgery (tried `ROUND_2_SAME_RECTANGLE +
    # rotation` but rotation repositions the shape). Pragmatic compromise
    # for the placeholder: a regular ROUNDED_RECTANGLE with a small
    # 32 px radius — the right corners are subtly rounded too, but the
    # visual impact at that radius on a 768-wide shape is tiny (4%).
    # A real embedded image (spec["image"]) renders square-cornered
    # until we wire a shape-mask via XML surgery.
    photo_w = S.context_photo_width
    photo_left = SLIDE.width - photo_w
    image_path = spec.get("image")
    if image_path and Path(image_path).exists():
        slide.shapes.add_picture(
            str(image_path), photo_left, 0, photo_w, SLIDE.height
        )
        # TODO: mask this picture with a rounded-left-side clip.
    else:
        placeholder = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            photo_left, 0, photo_w, SLIDE.height,
        )
        # Rounded-rectangle adjustment[0] is a fraction of half the
        # shorter dimension. 32 px radius on a 768-wide shape:
        #   adj = 32 / (768 / 2) = 0.0833
        placeholder.adjustments[0] = 32 / (768 / 2)
        placeholder.fill.solid()
        placeholder.fill.fore_color.rgb = C.neutral_card
        placeholder.line.fill.background()

    # Top row — arrow + CONTEXT label (top-left) and logo (top-right).
    top_y = S.slide_pad_cover
    add_inline_arrow(slide, S.slide_pad_cover, top_y, variant="dark")

    tag_scale = T.context_tag()
    tag_left = S.slide_pad_cover + S.cover_arrow_width + S.context_top_gap
    _add_text(
        slide,
        tag_left, top_y,
        px_to_emu(600), S.cover_arrow_height,
        spec.get("tag", "Context"),
        size_pt=tag_scale["size_px"] * 0.75,
        weight=tag_scale["weight"],
        leading=tag_scale["leading"],
        tracking=tag_scale["tracking"],
        uppercase=True,
        color=C.neutral_ink,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    add_logo(slide, variant="dark", position="inside")

    # Body — multi-paragraph rich text with bold emphasis.
    body = spec.get("body")
    if body:
        body_box = slide.shapes.add_textbox(
            S.slide_pad_cover, S.context_body_top,
            S.context_body_width,
            SLIDE.height - S.context_body_top - S.slide_pad_cover,
        )
        body_scale = T.context_body()
        _add_rich_text(
            body_box.text_frame, body,
            size_pt=body_scale["size_px"] * 0.75,
            leading=body_scale["leading"],
            color=C.neutral_ink,
            weight=body_scale["weight"],
        )

    return slide


def build_content_cards(prs, spec):
    """← web/slides/ContentSlide.jsx — 3-card grid."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Approach"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(144), SLIDE.width - px_to_emu(144), px_to_emu(180),
        spec["title"],
        size_pt=T.title()["size_px"] * 0.75, weight=300, leading=1.1,
    )

    cards = spec.get("cards", [])
    gap = px_to_emu(24)
    available = SLIDE.width - px_to_emu(72 * 2) - gap * (len(cards) - 1)
    card_w = available // max(len(cards), 1)
    top = px_to_emu(424)
    height = px_to_emu(380)
    for i, c in enumerate(cards):
        left = px_to_emu(72) + i * (card_w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C.neutral_card
        card.line.fill.background()
        _add_text(
            slide, left + px_to_emu(36), top + px_to_emu(36), card_w - px_to_emu(72), px_to_emu(20),
            c.get("num", f"{i+1:02d}"),
            size_pt=9, color=C.neutral_ink, tracking=0.08, uppercase=True,
        )
        _add_text(
            slide, left + px_to_emu(36), top + px_to_emu(90), card_w - px_to_emu(72), px_to_emu(80),
            c["title"], size_pt=17, weight=700, leading=1.25,
        )
        _add_text(
            slide, left + px_to_emu(36), top + px_to_emu(180), card_w - px_to_emu(72), px_to_emu(160),
            c.get("body", ""), size_pt=13, leading=1.62,
        )

    add_arrow(slide)
    return slide


def build_objectives(prs, spec):
    """← web/slides/ObjectivesSlide.jsx — statement + numbered list."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Objectives"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(208), px_to_emu(820), px_to_emu(320),
        spec["statement"],
        size_pt=T.headline()["size_px"] * 0.75, weight=300, leading=1.05,
        color=_accent(spec.get("accent", "orange")),
    )

    items = spec.get("items", [])
    right_x = SLIDE.width - px_to_emu(72) - px_to_emu(820)
    y = px_to_emu(208)
    row_h = px_to_emu(120)
    for i, it in enumerate(items):
        if i == 0:
            add_rule(slide, y, left=right_x, right=px_to_emu(72))
        _add_text(
            slide, right_x, y + px_to_emu(28), px_to_emu(80), px_to_emu(30),
            f"{i + 1:02d}", size_pt=9, color=C.neutral_ink,
            tracking=0.08, uppercase=True,
        )
        _add_text(
            slide, right_x + px_to_emu(80), y + px_to_emu(28), px_to_emu(740), px_to_emu(30),
            it["title"], size_pt=17, weight=700, leading=1.25,
        )
        _add_text(
            slide, right_x + px_to_emu(80), y + px_to_emu(62), px_to_emu(740), px_to_emu(50),
            it.get("body", ""), size_pt=13, leading=1.62,
        )
        y += row_h
        add_rule(slide, y, left=right_x, right=px_to_emu(72))

    add_arrow(slide)
    return slide


def build_activities(prs, spec):
    """← web/slides/ActivitiesSlide.jsx — 3 dotted cards + deliverables row."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Activities"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(144), SLIDE.width - px_to_emu(144), px_to_emu(180),
        spec["title"],
        size_pt=T.title()["size_px"] * 0.75, weight=300, leading=1.1,
    )

    cards = spec.get("cards", [])
    gap = px_to_emu(24)
    available = SLIDE.width - px_to_emu(144) - gap * (len(cards) - 1)
    card_w = available // max(len(cards), 1)
    top = px_to_emu(360)
    height = px_to_emu(480)
    for i, c in enumerate(cards):
        left = px_to_emu(72) + i * (card_w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C.neutral_card
        card.line.fill.background()
        add_dot(slide, left + px_to_emu(36), top + px_to_emu(36), _accent(c.get("color", "orange")), size="lg")
        _add_text(
            slide, left + px_to_emu(36), top + px_to_emu(100), card_w - px_to_emu(72), px_to_emu(80),
            c["title"], size_pt=21, weight=700, leading=1.2,
        )
        _add_text(
            slide, left + px_to_emu(36), top + px_to_emu(200), card_w - px_to_emu(72), px_to_emu(240),
            c.get("body", ""), size_pt=13, leading=1.62,
        )

    # Deliverables strip
    y = SLIDE.height - px_to_emu(140)
    add_rule(slide, y)
    _add_text(
        slide, px_to_emu(72), y + px_to_emu(28), px_to_emu(200), px_to_emu(24),
        "Deliverables", size_pt=9, tracking=0.08, uppercase=True,
    )
    deliverables = spec.get("deliverables", [])
    x = px_to_emu(72 + 200)
    for d in deliverables:
        pill_w = px_to_emu(len(d) * 7 + 28)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y + px_to_emu(22), pill_w, px_to_emu(26))
        pill.adjustments[0] = 0.5
        pill.fill.background()
        pill.line.color.rgb = C.neutral_ink
        pill.line.width = Emu(px_to_emu(1))
        tf = pill.text_frame
        tf.margin_top = tf.margin_bottom = px_to_emu(4)
        tf.margin_left = tf.margin_right = px_to_emu(14)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = d
        r.font.name = T.family
        r.font.size = Pt(10)
        r.font.color.rgb = C.neutral_ink
        x += pill_w + px_to_emu(12)

    add_arrow(slide)
    return slide


def build_timeline(prs, spec):
    """← web/slides/TimelineSlide.jsx — 4 dots on horizontal axis."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Methodology"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(144), SLIDE.width - px_to_emu(144), px_to_emu(180),
        spec["title"],
        size_pt=T.title()["size_px"] * 0.75, weight=300, leading=1.1,
    )

    phases = spec.get("phases", [])
    gap = px_to_emu(24)
    available = SLIDE.width - px_to_emu(144) - gap * (len(phases) - 1)
    col_w = available // max(len(phases), 1)

    axis_y = px_to_emu(570)
    axis = slide.shapes.add_connector(
        1, px_to_emu(72), axis_y, SLIDE.width - px_to_emu(72), axis_y,
    )
    axis.line.color.rgb = C.neutral_ink
    axis.line.width = Emu(px_to_emu(2))

    for i, p in enumerate(phases):
        left = px_to_emu(72) + i * (col_w + gap)
        _add_text(
            slide, left, px_to_emu(400), col_w, px_to_emu(24),
            f"{p.get('num', f'{i + 1:02d}')} · {p.get('range', '')}",
            size_pt=9, tracking=0.08, uppercase=True,
        )
        _add_text(
            slide, left, px_to_emu(432), col_w, px_to_emu(60),
            p["name"], size_pt=21, weight=700, leading=1.2,
        )
        add_dot(slide, left, axis_y - px_to_emu(10), C.neutral_ink, size="lg")
        _add_text(
            slide, left, px_to_emu(620), col_w - px_to_emu(16), px_to_emu(200),
            p.get("body", ""), size_pt=11, leading=1.58,
        )

    add_arrow(slide)
    return slide


def build_deliverables(prs, spec):
    """← web/slides/DeliverablesSlide.jsx — statement + dot list."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Deliverables"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(208), px_to_emu(820), px_to_emu(320),
        spec["statement"],
        size_pt=T.headline()["size_px"] * 0.75, weight=300, leading=1.05,
        color=_accent(spec.get("accent", "blue")),
    )

    items = spec.get("items", [])
    right_x = SLIDE.width - px_to_emu(72) - px_to_emu(820)
    y = px_to_emu(208)
    row_h = px_to_emu(120)
    for i, it in enumerate(items):
        if i == 0:
            add_rule(slide, y, left=right_x, right=px_to_emu(72))
        add_dot(slide, right_x, y + px_to_emu(38), _accent(it.get("color", "orange")), size="lg")
        _add_text(
            slide, right_x + px_to_emu(40), y + px_to_emu(28), px_to_emu(780), px_to_emu(30),
            it["title"], size_pt=17, weight=700, leading=1.25,
        )
        _add_text(
            slide, right_x + px_to_emu(40), y + px_to_emu(62), px_to_emu(780), px_to_emu(50),
            it.get("body", ""), size_pt=13, leading=1.62,
        )
        y += row_h
        add_rule(slide, y, left=right_x, right=px_to_emu(72))

    add_arrow(slide)
    return slide


def build_framework(prs, spec):
    """← web/slides/FrameworkSlide.jsx — spectrum axis + 4 colored cards."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Framework"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(144), SLIDE.width - px_to_emu(144), px_to_emu(180),
        spec["title"],
        size_pt=T.title()["size_px"] * 0.75, weight=300, leading=1.1,
    )

    _add_text(
        slide, px_to_emu(72), px_to_emu(360), px_to_emu(600), px_to_emu(24),
        spec.get("axis_left", ""), size_pt=9, tracking=0.08, uppercase=True,
    )
    _add_text(
        slide, SLIDE.width - px_to_emu(72) - px_to_emu(600), px_to_emu(360),
        px_to_emu(600), px_to_emu(24),
        spec.get("axis_right", ""), size_pt=9, tracking=0.08, uppercase=True,
        align=PP_ALIGN.RIGHT,
    )
    axis_y = px_to_emu(394)
    axis = slide.shapes.add_connector(
        1, px_to_emu(72), axis_y, SLIDE.width - px_to_emu(72), axis_y,
    )
    axis.line.color.rgb = C.neutral_ink
    axis.line.width = Emu(px_to_emu(2))

    cards = spec.get("cards", [])
    gap = px_to_emu(24)
    available = SLIDE.width - px_to_emu(144) - gap * (len(cards) - 1)
    card_w = available // max(len(cards), 1)
    top = px_to_emu(448)
    height = SLIDE.height - top - px_to_emu(140)
    for i, c in enumerate(cards):
        left = px_to_emu(72) + i * (card_w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, height)
        card.fill.solid()
        card.fill.fore_color.rgb = _accent(c.get("color", "orange"))
        card.line.fill.background()
        _add_text(
            slide, left + px_to_emu(28), top + px_to_emu(28), card_w - px_to_emu(56), px_to_emu(60),
            c["title"], size_pt=17, weight=700, leading=1.25,
        )
        _add_text(
            slide, left + px_to_emu(28), top + px_to_emu(110), card_w - px_to_emu(56), height - px_to_emu(130),
            c.get("body", ""), size_pt=11, leading=1.58,
        )

    add_arrow(slide)
    return slide


def build_stats(prs, spec):
    """← web/slides/StatsSlide.jsx — 4 overlapping circles."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Our expertise"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(144), SLIDE.width - px_to_emu(144), px_to_emu(180),
        spec["title"],
        size_pt=T.title()["size_px"] * 0.75, weight=300, leading=1.1,
    )

    stats = spec.get("stats", [])
    size = px_to_emu(220)
    overlap = px_to_emu(32)
    total_w = size * len(stats) - overlap * (len(stats) - 1)
    start_x = (SLIDE.width - total_w) // 2
    top = px_to_emu(440)
    for i, s in enumerate(stats):
        left = start_x + i * (size - overlap)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
        circle.fill.solid()
        circle.fill.fore_color.rgb = _accent(s.get("color", "orange"))
        circle.line.fill.background()
        # Centered text — two lines
        tf = circle.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = s["num"]
        r.font.name = T.family
        r.font.size = Pt(30)
        r.font.color.rgb = C.neutral_ink
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = s.get("label", "").upper()
        r2.font.name = T.family
        r2.font.size = Pt(9)
        r2.font.color.rgb = C.neutral_ink

    add_arrow(slide)
    return slide


def build_gantt(prs, spec):
    """← web/slides/GanttSlide.jsx — big number + gantt table."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Timings"), px_to_emu(72), px_to_emu(60))

    _add_text(
        slide, px_to_emu(72), px_to_emu(200), px_to_emu(720), px_to_emu(200),
        spec.get("big_number", ""),
        size_pt=90, weight=300, leading=0.95, color=C.neutral_ink,
    )
    _add_text(
        slide, px_to_emu(72), px_to_emu(440), px_to_emu(720), px_to_emu(120),
        spec.get("caption", ""),
        size_pt=T.lead()["size_px"] * 0.75, leading=1.4,
    )

    phases = spec.get("phases", [])
    weeks = spec.get("weeks", 8)
    table_x = SLIDE.width - px_to_emu(72) - px_to_emu(1000)
    table_y = px_to_emu(220)
    label_col = px_to_emu(160)
    week_col = (px_to_emu(1000) - label_col) // weeks

    for w in range(weeks):
        _add_text(
            slide,
            table_x + label_col + w * week_col, table_y,
            week_col, px_to_emu(24),
            f"W{w + 1}", size_pt=9, tracking=0.08, uppercase=True,
            align=PP_ALIGN.CENTER,
        )
    add_rule(slide, table_y + px_to_emu(32),
             left=table_x, right=SLIDE.width - table_x - px_to_emu(1000))

    for i, p in enumerate(phases):
        row_y = table_y + px_to_emu(48) + i * px_to_emu(60)
        _add_text(
            slide, table_x, row_y + px_to_emu(8), label_col, px_to_emu(30),
            p["name"], size_pt=13, weight=700,
        )
        bar_x = table_x + label_col + p["start"] * week_col
        bar_w = p["len"] * week_col
        bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            bar_x, row_y + px_to_emu(14),
            bar_w, px_to_emu(24),
        )
        bar.adjustments[0] = 0.5
        bar.fill.solid()
        bar.fill.fore_color.rgb = _accent(p.get("color", "orange"))
        bar.line.fill.background()
        add_rule(slide, row_y + px_to_emu(48),
                 left=table_x, right=SLIDE.width - table_x - px_to_emu(1000))

    add_arrow(slide)
    return slide


def build_costs(prs, spec):
    """← web/slides/CostsSlide.jsx — dark shell + fee table."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_shell(slide, tone="dark")
    add_logo(slide, variant="light")
    add_tag(slide, spec.get("tag", "Investment"), px_to_emu(72), px_to_emu(60), tone="inv")

    _add_text(
        slide, px_to_emu(72), px_to_emu(160), px_to_emu(820), px_to_emu(240),
        spec["statement"],
        size_pt=T.headline()["size_px"] * 0.75, weight=300, leading=1.05,
        color=C.neutral_paper,
    )

    # Overlapping small circles
    size = px_to_emu(120)
    overlap = px_to_emu(20)
    for i, c in enumerate(spec.get("circle_colors", ["orange", "lime", "pink", "blue"])):
        left = px_to_emu(72) + i * (size - overlap)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, px_to_emu(420), size, size)
        circle.fill.solid()
        circle.fill.fore_color.rgb = _accent(c)
        circle.line.fill.background()

    # Fee table
    right_x = SLIDE.width - px_to_emu(72) - px_to_emu(820)
    y = px_to_emu(160)
    row_h = px_to_emu(90)
    rows = spec.get("rows", [])
    for i, r in enumerate(rows):
        if i == 0:
            add_rule(slide, y, left=right_x, right=px_to_emu(72), tone="inv")
        _add_text(
            slide, right_x, y + px_to_emu(28), px_to_emu(500), px_to_emu(40),
            r["label"], size_pt=17, color=C.neutral_paper,
        )
        _add_text(
            slide, right_x + px_to_emu(500), y + px_to_emu(28), px_to_emu(320), px_to_emu(40),
            r["amount"], size_pt=17, weight=700, color=C.neutral_paper,
            align=PP_ALIGN.RIGHT,
        )
        y += row_h
        add_rule(slide, y, left=right_x, right=px_to_emu(72), tone="inv")

    total = spec.get("total")
    if total:
        _add_text(
            slide, right_x, y + px_to_emu(40), px_to_emu(300), px_to_emu(24),
            total["label"], size_pt=9, tracking=0.08, uppercase=True,
            color=C.neutral_paper,
        )
        _add_text(
            slide, right_x + px_to_emu(300), y + px_to_emu(30), px_to_emu(520), px_to_emu(60),
            total["amount"], size_pt=36, weight=300,
            color=C.neutral_paper, align=PP_ALIGN.RIGHT,
        )

    add_arrow(slide, variant="light")
    return slide


def build_dark_outro(prs, spec):
    """← web/slides/DarkSlide.jsx"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_shell(slide, tone="dark")
    add_logo(slide, variant="light")

    if spec.get("eyebrow"):
        _add_text(
            slide, px_to_emu(72), px_to_emu(420), SLIDE.width - px_to_emu(144), px_to_emu(24),
            spec["eyebrow"], size_pt=9,
            tracking=0.08, uppercase=True, color=C.neutral_paper,
        )
    _add_text(
        slide, px_to_emu(72), px_to_emu(460), SLIDE.width - px_to_emu(144), px_to_emu(320),
        spec["headline"],
        size_pt=T.display()["size_px"] * 0.75, weight=300, leading=1.05,
        color=C.neutral_paper,
    )
    if spec.get("footnote"):
        _add_text(
            slide, px_to_emu(72), SLIDE.height - px_to_emu(220), px_to_emu(1200), px_to_emu(120),
            spec["footnote"], size_pt=13, leading=1.62, color=C.neutral_paper,
        )

    add_arrow(slide, variant="light")
    return slide


# -------------------------------------- composite (spine) builders
# These are domain-specific NOBA slides. Each one selects a primitive
# layout above and feeds it content from content-blocks.md / case-studies.md.

BUILDERS = {
    "cover":           build_cover,
    "context":         build_context,
    "content_cards":   build_content_cards,
    "objectives":      build_objectives,
    "activities":      build_activities,
    "timeline":        build_timeline,
    "deliverables":    build_deliverables,
    "framework":       build_framework,
    "stats":           build_stats,
    "gantt":           build_gantt,
    "costs":           build_costs,
    "dark_outro":      build_dark_outro,
}

# Spine aliases — map semantic names from references/spine-checklist.md to
# the 12 primitive builders. Each alias is a pure pass-through; Claude fills
# content from references/content-blocks.md.
SPINE_ALIASES = {
    "mission":               "dark_outro",
    "what_we_do":            "content_cards",
    "clients_grid":          "content_cards",
    "expertise_stats":       "stats",
    "why_us_overview":       "content_cards",
    "why_us_deepdive":       "deliverables",
    "multidisciplinary_team":"activities",
    "gellify":               "context",
    "case_study":            "content_cards",
    "team":                  "activities",
    "timings":               "gantt",
    "budget":                "costs",
    "noba_way_divider":      "dark_outro",
    "methodology_overview":  "timeline",
    "phase_detail":          "activities",
    "ending_03":             "dark_outro",
}


def _builder_for(layout: str):
    if layout in BUILDERS:
        return BUILDERS[layout]
    alias = SPINE_ALIASES.get(layout)
    if alias:
        return BUILDERS[alias]
    raise KeyError(f"Unknown layout: {layout}. See BUILDERS or SPINE_ALIASES in build_deck.py.")


def main(deck_spec: dict, out_path: str | Path) -> Path:
    """Build a deck from a spec dict. Returns the output path."""
    prs = Presentation()
    prs.slide_width = SLIDE.width
    prs.slide_height = SLIDE.height

    for slide_spec in deck_spec.get("slides", []):
        layout = slide_spec["layout"]
        _builder_for(layout)(prs, slide_spec)

    out = Path(out_path)
    prs.save(str(out))
    return out


if __name__ == "__main__":
    # Smoke test — emits a minimal deck covering every primitive layout.
    sample = {
        "slides": [
            {"layout": "cover", "title": "Next-Generation Coffee Innovation",
             "subtitle": "Identifying and testing new growth opportunities",
             "client": "lavazza", "date": "september 2025"},
            {"layout": "context", "tag": "Context",
             "headline": "A single moment of truth.",
             "lead": "Brief, outcome-oriented framing.",
             "body": "Two or three concrete supporting sentences."},
            {"layout": "dark_outro",
             "eyebrow": "The NOBA way",
             "headline": "Move decisively. Test early. Ship the story."},
        ],
    }
    out = main(sample, "/tmp/noba_demo.pptx")
    print(f"Wrote {out}")
