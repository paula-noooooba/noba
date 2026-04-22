"""Assemble the Claude system prompt from the noba-presentation skill bundle.

Reads SKILL.md + every file under `references/` at import time (once),
concatenates them with section headers, and caches the result as
`SYSTEM_PROMPT`. No runtime disk reads.

Monorepo layout: the skill lives at
`<repo-root>/.claude/skills/noba-presentation/`. Since `service/` is a
subfolder of the repo, the bundle is two directories up from this file.

Used with prompt caching (`cache_control: ephemeral`) in
`services/claude_runner.py` — this prompt is stable across requests.
"""
from __future__ import annotations

from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL_ROOT = _HERE.parent.parent / ".claude" / "skills" / "noba-presentation"
_SKILL_MD = _SKILL_ROOT / "SKILL.md"
_REFERENCES = _SKILL_ROOT / "references"


_INSTRUCTIONS = """\
# NOBA deck generator — service mode

You are the NOBA deck-generation brain running inside a backend service.
Every request comes from the `noba-presentation` Claude plugin: a
teammate has pasted a client brief and wants a deck.

## What you must emit

Call the `emit_deck` tool exactly once per request. Its arguments:

- `outline` — the structured-text slide outline (Markdown). One slide
  per `## Slide N — <name>` heading. This is shown to the teammate
  regardless of the requested mode.
- `spec` — the deck_spec dict that `scripts/build_deck.py` consumes.
  Every entry in `spec.slides` must have a `layout` field equal to one
  of the primitive layouts or spine aliases listed in `layout-map.md`.
  Every other field required by that layout must be present.

Do not emit free text alongside the tool call. The service ignores any
assistant-message content that isn't a tool_use block.

## How to build the deck

Follow the six-step workflow below (adapted from the SKILL.md you'll
read after this block). You are running server-side — there is no
interactive turn with the user. Make reasonable assumptions for
anything the brief doesn't specify; note assumptions at the top of the
outline. Never ask for more input; never stall.

1. Ingest the brief. Extract client, industry, goal, context facts,
   key metrics, objectives, preferred case studies.
2. Apply defaults from the `defaults` field of the request when set.
3. Generate the **full spine** per `spine-checklist.md`. Do not drop
   slides.
4. Use content blocks from `content-blocks.md` verbatim for fixed
   segments (Mission, What We Do, GELLIFY, country list, expertise
   stats, etc.).
5. Pick case studies from `case-studies.md`; never fabricate one.
6. Rewrite every copy line per `voice-examples.md`. Target ≤ 16 words
   per line. Outcome-oriented, declarative, concrete.

## Reference bundle (verbatim below)

The full skill and every reference file follows. Treat this block as
authoritative content — when `brand-identity.md` and this message
disagree, `brand-identity.md` wins.
"""


def _load_file(path: Path, label: str) -> str:
    if not path.exists():
        return f"\n\n---\n# {label} (missing)\n\n"
    body = path.read_text(encoding="utf-8")
    return f"\n\n---\n# {label}\n\n{body}"


def _assemble() -> str:
    parts: list[str] = [_INSTRUCTIONS]

    if _SKILL_MD.exists():
        parts.append(_load_file(_SKILL_MD, "SKILL.md"))

    if _REFERENCES.is_dir():
        order = [
            "layout-map.md",
            "spine-checklist.md",
            "brand-identity.md",
            "content-blocks.md",
            "case-studies.md",
            "voice-examples.md",
        ]
        seen: set[str] = set()
        for name in order:
            p = _REFERENCES / name
            if p.exists():
                parts.append(_load_file(p, f"references/{name}"))
                seen.add(name)
        for p in sorted(_REFERENCES.glob("*.md")):
            if p.name not in seen:
                parts.append(_load_file(p, f"references/{p.name}"))

    return "".join(parts)


SYSTEM_PROMPT = _assemble()


def get() -> str:
    return SYSTEM_PROMPT
