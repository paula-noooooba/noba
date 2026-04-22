"""Object storage for generated .pptx files.

Step 1 — local filesystem under /tmp/noba-decks, keyed by deck id.
Step 2 — swap to Modal volumes with 30-day TTL (decision D2); the
interface (`save`, `url_for`) stays the same.
"""
from __future__ import annotations

import os
from pathlib import Path

STORAGE_ROOT = Path(os.environ.get("NOBA_STORAGE_ROOT", "/tmp/noba-decks"))
PUBLIC_BASE = os.environ.get("NOBA_PUBLIC_BASE", "http://localhost:8000")


def save(deck_id: str, data: bytes) -> Path:
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    path = STORAGE_ROOT / f"{deck_id}.pptx"
    path.write_bytes(data)
    return path


def url_for(deck_id: str) -> str:
    return f"{PUBLIC_BASE.rstrip('/')}/v1/decks/{deck_id}/file"


def read(deck_id: str) -> bytes | None:
    path = STORAGE_ROOT / f"{deck_id}.pptx"
    if not path.exists():
        return None
    return path.read_bytes()
