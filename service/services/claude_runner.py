"""Claude brain — brief → deck_spec.

Step 1 (current): returns a hardcoded demo spec. Plumbing only.
Step 2: loads SKILL.md + every references/*.md from the noba-core
submodule, assembles a system prompt, calls the Anthropic Messages API
with prompt caching, parses the JSON deck_spec out of the response.
"""
from __future__ import annotations

from models.schemas import DeckRequest, DeckSpec, SlideSpec


DEMO_OUTLINE = """\
## Slide 1 — Cover  (layout: cover)
- Eyebrow: Commercial proposal
- Title: Next-gen innovation.
- Accent: pink
- Client: Demo client
- Date: April 2026

## Slide 2 — Closing  (layout: dark_outro)
- Eyebrow: The NOBA way
- Headline: Move decisively. Test early. Ship the story.
"""


def run(req: DeckRequest) -> tuple[str, DeckSpec]:
    """Return (outline_markdown, deck_spec). Currently stubbed."""
    spec = DeckSpec(
        slides=[
            SlideSpec.model_validate({
                "layout": "cover",
                "eyebrow": "Commercial proposal",
                "title": "Next-gen innovation.",
                "accent": "pink",
                "client": "Demo client",
                "date": "April 2026",
            }),
            SlideSpec.model_validate({
                "layout": "dark_outro",
                "eyebrow": "The NOBA way",
                "headline": "Move decisively. Test early. Ship the story.",
            }),
        ],
    )
    return DEMO_OUTLINE, spec
