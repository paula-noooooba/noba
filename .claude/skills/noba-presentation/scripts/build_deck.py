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

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

from tokens import C, S, T, SLIDE, px_to_emu


# --------------------------------------------------------------------- atoms
# Match web/atoms/atoms.jsx 1:1. Each atom is a thin helper; slide builders
# compose them. Atoms know nothing about slide content — only visuals.

def add_logo(slide, variant: str = "dark", position: str = "inside"):
    """Logo atom. Text placeholder until real art lands in web/assets/."""
    color = C.neutral_paper if variant == "light" else C.neutral_ink
    left = SLIDE.width - px_to_emu(72 if position == "cover" else 60) - px_to_emu(140)
    top = px_to_emu(60 if position == "cover" else 48)
    box = slide.shapes.add_textbox(left, top, px_to_emu(140), px_to_emu(40))
    tf = box.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = "noba"
    r.font.name = T.family
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = color
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.RIGHT
    r2 = p2.add_run()
    r2.text = "a gellify company"
    r2.font.name = T.family
    r2.font.size = Pt(8)
    r2.font.color.rgb = color


def add_arrow(slide, variant: str = "dark"):
    """Arrow atom — bottom-right."""
    color = C.neutral_paper if variant == "light" else C.neutral_ink
    width, height = px_to_emu(80), px_to_emu(24)
    left = SLIDE.width - px_to_emu(60) - width
    top = SLIDE.height - px_to_emu(48) - height
    line = slide.shapes.add_connector(1, left, top + height // 2, left + width - px_to_emu(6), top + height // 2)
    line.line.color.rgb = color
    line.line.width = Emu(px_to_emu(1.5))
    # Arrow head (approximation — triangle)
    head = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, left + width - px_to_emu(14), top, px_to_emu(14), height)
    head.fill.solid()
    head.fill.fore_color.rgb = color
    head.line.fill.background()


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
    r.font.name = T.family
    r.font.size = Pt(size_pt)
    r.font.bold = weight >= 700
    r.font.color.rgb = color
    return box


def _pct(n: int, denom: int = 1920) -> int:
    """px → EMU helper for inline math."""
    return px_to_emu(n * SLIDE.width_px / denom)


def _accent(name: str) -> RGBColor:
    return getattr(C, f"accent_{name}".replace("-", "_"))


# ---------------------------------------------------- primitive slide builders
# One per JSX component in web/slides/. Never add a new layout without first
# adding (or updating) the JSX reference and design/tokens.json.

def build_cover(prs, spec):
    """← web/slides/TitleSlide.jsx"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_shell(slide)
    add_logo(slide, variant="dark", position="cover")

    _add_text(
        slide, px_to_emu(72), px_to_emu(320), SLIDE.width - px_to_emu(144), px_to_emu(30),
        spec.get("eyebrow", "Commercial proposal"),
        size_pt=T.label()["size_px"] * 0.75, color=C.neutral_ink,
        tracking=0.08, uppercase=True,
    )
    _add_text(
        slide, px_to_emu(72), px_to_emu(360), SLIDE.width - px_to_emu(144), px_to_emu(360),
        spec["title"],
        size_pt=T.hero()["size_px"] * 0.75,
        weight=300, leading=1.05,
        color=_accent(spec.get("accent", "pink")),
    )

    _add_text(
        slide, px_to_emu(72), SLIDE.height - px_to_emu(132), px_to_emu(600), px_to_emu(24),
        spec.get("client", ""), size_pt=10, weight=700, color=C.neutral_ink,
    )
    _add_text(
        slide, px_to_emu(72), SLIDE.height - px_to_emu(106), px_to_emu(600), px_to_emu(20),
        spec.get("date", ""), size_pt=10, color=C.neutral_ink,
    )

    add_arrow(slide, variant="dark")
    return slide


def build_context(prs, spec):
    """← web/slides/ContextSlide.jsx"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_logo(slide, variant="dark")
    add_tag(slide, spec.get("tag", "Context"), px_to_emu(72), px_to_emu(60))

    left_col_w = px_to_emu(1022)
    _add_text(
        slide, px_to_emu(72), px_to_emu(192), left_col_w, px_to_emu(280),
        spec["headline"],
        size_pt=T.headline()["size_px"] * 0.75, weight=300, leading=1.05,
    )
    if spec.get("lead"):
        _add_text(
            slide, px_to_emu(72), px_to_emu(480), left_col_w, px_to_emu(100),
            spec["lead"],
            size_pt=T.lead()["size_px"] * 0.75, leading=1.4,
        )
    if spec.get("body"):
        _add_text(
            slide, px_to_emu(72), px_to_emu(600), left_col_w, px_to_emu(280),
            spec["body"],
            size_pt=T.body()["size_px"] * 0.75, leading=1.62,
        )

    # Photo placeholder
    img_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        SLIDE.width - px_to_emu(60) - px_to_emu(706),
        px_to_emu(60),
        px_to_emu(706),
        SLIDE.height - px_to_emu(120),
    )
    img_shape.fill.solid()
    img_shape.fill.fore_color.rgb = C.neutral_card
    img_shape.line.fill.background()
    # TODO: replace with slide.shapes.add_picture(...) once web/assets/ has photos.

    add_arrow(slide)
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
            {"layout": "cover", "title": "Next-gen innovation.", "eyebrow": "Commercial proposal",
             "client": "Demo client", "date": "April 2026", "accent": "pink"},
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
