"""Run a brief through the service end-to-end, save the .pptx, print the outline.

Interactive helper for validating the Claude runner + python-pptx
builders against real briefs. Bypasses the HTTP layer — calls the
runner and builder directly, so you don't need to start uvicorn.

Requires:
- ANTHROPIC_API_KEY in the environment

Usage:
    # Pipe a brief from stdin
    cat brief.txt | python3 scripts/run_brief.py --out /tmp/deck.pptx

    # Or pass a file
    python3 scripts/run_brief.py --brief brief.txt --out /tmp/deck.pptx

    # Override model
    python3 scripts/run_brief.py --brief brief.txt --model opus --out /tmp/deck.pptx
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--brief", type=Path,
                   help="Path to a brief text file. Omit to read from stdin.")
    p.add_argument("--out", type=Path, default=Path("/tmp/noba_deck.pptx"),
                   help="Where to write the generated .pptx (default: /tmp/noba_deck.pptx)")
    p.add_argument("--model", default=None,
                   help="Model alias (sonnet|opus|haiku) or full model ID. "
                        "Default: sonnet.")
    p.add_argument("--mode", choices=["text", "pptx"], default="pptx")
    p.add_argument("--requested-by", default=os.environ.get("USER", "unknown"))
    args = p.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        return 1

    brief_text = args.brief.read_text() if args.brief else sys.stdin.read()
    if not brief_text.strip():
        print("ERROR: brief is empty.", file=sys.stderr)
        return 1

    # Make sibling packages importable.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    from models.schemas import DeckRequest
    from services import claude_runner, deck_builder

    req = DeckRequest(
        brief=brief_text,
        mode=args.mode,
        model=args.model,
        requested_by=args.requested_by,
    )

    print(f">>> calling Claude ({claude_runner._resolve_model(req)}) …", file=sys.stderr)
    outline, spec = claude_runner.run(req)

    print("=" * 72)
    print("OUTLINE")
    print("=" * 72)
    print(outline)
    print("=" * 72)
    print(f"SPEC — {len(spec.slides)} slides")
    print("=" * 72)
    for i, s in enumerate(spec.slides, 1):
        print(f"  {i:2d}. {s.layout}")

    if args.mode == "pptx":
        print(">>> rendering .pptx …", file=sys.stderr)
        pptx_bytes = deck_builder.render(spec)
        args.out.write_bytes(pptx_bytes)
        print(f">>> wrote {args.out} ({len(pptx_bytes):,} bytes)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
