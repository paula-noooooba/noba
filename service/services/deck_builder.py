"""Render a DeckSpec to .pptx bytes.

Imports `main` from the noba-presentation skill bundle at
`<repo-root>/.claude/skills/noba-presentation/scripts/build_deck.py`
and delegates rendering to it. That file is the single source of truth
for python-pptx layouts (1:1 with `web/slides/*.jsx`).

The scripts directory is added to `sys.path` at import time so
`build_deck.py` can resolve its sibling `tokens.py`.
"""
from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

from models.schemas import DeckSpec


_HERE = Path(__file__).resolve().parent
_SCRIPTS_DIR = (
    _HERE.parent.parent / ".claude" / "skills" / "noba-presentation" / "scripts"
)

if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# Imported after sys.path adjustment so build_deck can find tokens.py.
import build_deck  # noqa: E402


def render(spec: DeckSpec) -> bytes:
    """Materialise the spec to .pptx bytes using the canonical builder."""
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        build_deck.main(spec.model_dump(), tmp_path)
        return tmp_path.read_bytes()
    finally:
        tmp_path.unlink(missing_ok=True)


def render_to_io(spec: DeckSpec) -> io.BytesIO:
    """Convenience for callers that want a file-like object."""
    return io.BytesIO(render(spec))
