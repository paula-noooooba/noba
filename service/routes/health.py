"""Health and version endpoints — no auth, no audit."""
from __future__ import annotations

import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}


@router.get("/version")
async def version() -> dict:
    return {
        "service": "noba-deck-service",
        "version": os.environ.get("NOBA_VERSION", "dev"),
        "noba_core_sha": os.environ.get("NOBA_CORE_SHA", "unpinned"),
    }
