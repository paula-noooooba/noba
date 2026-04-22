"""Render a DeckSpec to .pptx bytes.

Step 1 (current): emits a minimal inline deck using python-pptx
directly — just enough to prove the pipeline end-to-end. Each slide is
a blank with the spec's `title` field written once in Helvetica.

Step 2: import from `noba-core` submodule —
    from noba_core.build_deck import main
    main(spec.model_dump(), out_path)
— which renders the full NOBA design. The in-memory spec format is
already compatible (see noba-core/.claude/skills/noba-presentation/
references/layout-map.md).
"""
from __future__ import annotations

import io

from pptx import Presentation
from pptx.util import Inches, Pt

from models.schemas import DeckSpec


def render(spec: DeckSpec) -> bytes:
    prs = Presentation()
    prs.slide_width = Inches(20)
    prs.slide_height = Inches(11.25)

    blank_layout = prs.slide_layouts[6]
    for s in spec.slides:
        slide = prs.slides.add_slide(blank_layout)
        data = s.model_dump()
        label = data.get("title") or data.get("headline") or data.get("layout", "slide")
        tb = slide.shapes.add_textbox(Inches(1), Inches(4), Inches(18), Inches(3))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = label
        r.font.name = "Helvetica Neue"
        r.font.size = Pt(54)

    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()
