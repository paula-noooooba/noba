"""FastAPI application entrypoint.

Local dev:
    uvicorn app:app --reload

Modal:
    modal deploy modal_app.py
"""
from __future__ import annotations

from fastapi import FastAPI

from routes import decks, health


def create_app() -> FastAPI:
    app = FastAPI(
        title="NOBA Deck Service",
        version="0.1.0",
        description="Generate NOBA commercial proposals and other decks from pasted briefs.",
    )
    app.include_router(health.router)
    app.include_router(decks.router)
    return app


app = create_app()
