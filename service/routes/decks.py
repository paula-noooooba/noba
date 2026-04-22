"""Deck endpoints.

POST /v1/decks          — create a deck from a brief
GET  /v1/decks/:id      — fetch metadata + download URL
GET  /v1/decks/:id/file — download the .pptx

Step 1 uses a stubbed claude_runner (hardcoded spec) and the minimal
inline deck_builder. Step 2 swaps in the real bundle.
"""
from __future__ import annotations

import secrets
import time
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status

from audit import emit
from auth import require_team_key
from models.schemas import DeckRequest, DeckResponse
from services import claude_runner, deck_builder, storage


router = APIRouter(prefix="/v1/decks", tags=["decks"])

TTL_DAYS = 30


def _new_id() -> str:
    return "dck_" + secrets.token_urlsafe(12)


@router.post("", response_model=DeckResponse, dependencies=[Depends(require_team_key)])
async def create_deck(req: DeckRequest) -> DeckResponse:
    t0 = time.monotonic()
    deck_id = _new_id()

    outline, spec = claude_runner.run(req)

    download_url = None
    expires_at = None
    if req.mode == "pptx":
        pptx_bytes = deck_builder.render(spec)
        storage.save(deck_id, pptx_bytes)
        download_url = storage.url_for(deck_id)
        expires_at = (datetime.now(timezone.utc) + timedelta(days=TTL_DAYS)).isoformat()

    duration_ms = int((time.monotonic() - t0) * 1000)
    emit(
        "deck.generated",
        deck_id=deck_id,
        mode=req.mode,
        slide_count=len(spec.slides),
        duration_ms=duration_ms,
        requested_by=req.requested_by,
    )

    return DeckResponse(
        id=deck_id,
        mode=req.mode,
        outline=outline,
        spec=spec,
        download_url=download_url,
        expires_at=expires_at,
        slide_count=len(spec.slides),
    )


@router.get("/{deck_id}/file", dependencies=[Depends(require_team_key)])
async def download_deck(deck_id: str) -> Response:
    data = storage.read(deck_id)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck not found or expired.")
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f'attachment; filename="{deck_id}.pptx"'},
    )
