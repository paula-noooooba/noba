"""Assemble the Claude system prompt from noba-core skill material.

Step 1: returns a placeholder. Step 2: reads
`noba-core/.claude/skills/noba-presentation/SKILL.md` and every file
under `.../references/*.md`, concatenates into a single system prompt
with section headers. Re-assembled once at service start (module
import); no runtime disk reads.

Use with prompt caching — the assembled prompt is stable across
requests, so every request after the first hits the cache.
"""
from __future__ import annotations

SYSTEM_PROMPT = """\
You are the NOBA presentation-generation model.

(Step 2 will replace this with the full skill + reference bundle. For
now this placeholder is enough to smoke-test the plumbing.)
"""


def get() -> str:
    return SYSTEM_PROMPT
