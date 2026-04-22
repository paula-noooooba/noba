"""API request and response schemas.

`DeckSpec` mirrors the shape documented in
`noba-core/.claude/skills/noba-presentation/references/layout-map.md`.
Every layout key corresponds to a primitive builder in
`noba-core/.claude/skills/noba-presentation/scripts/build_deck.py`.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Mode = Literal["text", "pptx"]


class DeckRequest(BaseModel):
    brief: str = Field(..., min_length=1, max_length=50_000,
                       description="Pasted client brief, notes, or source material.")
    mode: Mode = "text"
    defaults: dict[str, Any] = Field(default_factory=dict,
                                     description="Optional overrides (accent_cover, methodology_phases, etc.).")
    requested_by: str | None = Field(None, max_length=200,
                                     description="Email or identity of the teammate issuing the request.")


class SlideSpec(BaseModel):
    layout: str
    model_config = {"extra": "allow"}


class DeckSpec(BaseModel):
    slides: list[SlideSpec]


class DeckResponse(BaseModel):
    id: str
    mode: Mode
    outline: str
    spec: DeckSpec
    download_url: str | None = None
    expires_at: str | None = None
    slide_count: int


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
