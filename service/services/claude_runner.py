"""Claude brain — brief → (outline, DeckSpec).

Calls the Anthropic Messages API with the assembled NOBA skill bundle
as the system prompt, using prompt caching on the system block. The
model is constrained to a single `emit_deck` tool call, so parsing is
trivial and robust.

Environment:
- `ANTHROPIC_API_KEY` (required in prod) — Anthropic Messages API key.
- `NOBA_MODEL` (optional)               — model override. Default:
                                          `claude-opus-4-7` (D7).
- `NOBA_STUB_CLAUDE=1` (optional)       — bypass the API, return a
                                          canned two-slide spec. Used
                                          by tests to avoid hitting
                                          the network.
"""
from __future__ import annotations

import json
import os

from models.schemas import DeckRequest, DeckSpec, SlideSpec
from prompts.system_prompt import SYSTEM_PROMPT


DEFAULT_MODEL = "claude-opus-4-7"
MAX_TOKENS = 16_000


EMIT_DECK_TOOL = {
    "name": "emit_deck",
    "description": (
        "Emit the final NOBA deck. Call exactly once per request. "
        "`outline` is the Markdown slide-by-slide outline shown to the "
        "teammate. `spec` is the deck_spec dict consumed by the "
        "python-pptx renderer — every slide must have a `layout` field "
        "matching a layout or spine alias from layout-map.md."
    ),
    "input_schema": {
        "type": "object",
        "required": ["outline", "spec"],
        "properties": {
            "outline": {
                "type": "string",
                "description": (
                    "Markdown slide-by-slide outline. One H2 heading per slide. "
                    "Starts with `## Slide 1 — <name>`. "
                    "Under each heading, bullet the key fields for that layout "
                    "(tag, title, headline, lead, body, cards, etc.)."
                ),
            },
            "spec": {
                "type": "object",
                "required": ["slides"],
                "properties": {
                    "slides": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["layout"],
                            "properties": {
                                "layout": {
                                    "type": "string",
                                    "description": (
                                        "Must match a key in BUILDERS or "
                                        "SPINE_ALIASES in scripts/build_deck.py "
                                        "(see references/layout-map.md)."
                                    ),
                                },
                            },
                            "additionalProperties": True,
                        },
                    }
                },
                "additionalProperties": False,
            },
        },
    },
}


_STUB_OUTLINE = """\
## Slide 1 — Cover  (layout: cover)
- Eyebrow: Commercial proposal
- Title: Stubbed deck.
- Accent: pink

## Slide 2 — Closing  (layout: dark_outro)
- Eyebrow: The NOBA way
- Headline: Move decisively. Test early. Ship the story.
"""


def _stub_result() -> tuple[str, DeckSpec]:
    spec = DeckSpec(
        slides=[
            SlideSpec.model_validate({
                "layout": "cover",
                "eyebrow": "Commercial proposal",
                "title": "Stubbed deck.",
                "accent": "pink",
                "client": "Test client",
                "date": "April 2026",
            }),
            SlideSpec.model_validate({
                "layout": "dark_outro",
                "eyebrow": "The NOBA way",
                "headline": "Move decisively. Test early. Ship the story.",
            }),
        ],
    )
    return _STUB_OUTLINE, spec


def _build_user_message(req: DeckRequest) -> str:
    parts = [
        "A NOBA teammate has pasted this brief. Generate the full deck.",
        "",
        f"Mode: {req.mode}",
    ]
    if req.defaults:
        parts.append(f"Defaults: {json.dumps(req.defaults)}")
    if req.requested_by:
        parts.append(f"Requested by: {req.requested_by}")
    parts += [
        "",
        "--- BRIEF BEGINS ---",
        req.brief,
        "--- BRIEF ENDS ---",
        "",
        "Call `emit_deck` with the outline and spec.",
    ]
    return "\n".join(parts)


def run(req: DeckRequest) -> tuple[str, DeckSpec]:
    """Send the brief to Claude, parse the `emit_deck` tool call.

    Returns (outline_markdown, deck_spec). Raises RuntimeError on any
    response shape we can't parse — the route maps that to a 502.
    """
    if os.environ.get("NOBA_STUB_CLAUDE") == "1":
        return _stub_result()

    # Imported lazily so the stub path doesn't require the SDK.
    from anthropic import Anthropic

    client = Anthropic()
    resp = client.messages.create(
        model=os.environ.get("NOBA_MODEL", DEFAULT_MODEL),
        max_tokens=MAX_TOKENS,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        tools=[EMIT_DECK_TOOL],
        tool_choice={"type": "tool", "name": "emit_deck"},
        messages=[{"role": "user", "content": _build_user_message(req)}],
    )

    for block in resp.content:
        if getattr(block, "type", None) == "tool_use" and block.name == "emit_deck":
            args = block.input or {}
            outline = args.get("outline", "").strip()
            spec_dict = args.get("spec") or {}
            if not outline or not spec_dict.get("slides"):
                raise RuntimeError(
                    "emit_deck returned empty outline or empty spec.slides."
                )
            spec = DeckSpec.model_validate(spec_dict)
            return outline, spec

    raise RuntimeError(
        "Claude did not call emit_deck. Response stop_reason="
        f"{resp.stop_reason!r}."
    )
