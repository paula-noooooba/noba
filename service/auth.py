"""API-key middleware.

Single shared team key per deployment (decision D3). Teammates paste
this key once on plugin install; the plugin forwards it as
`Authorization: Bearer <key>`.

Rotation is a deploy: change `NOBA_API_KEY` in Modal secrets, redeploy,
notify team to update their plugin config.
"""
from __future__ import annotations

import hmac
import os

from fastapi import Header, HTTPException, status


def _extract_bearer(header: str | None) -> str | None:
    if not header:
        return None
    parts = header.split(None, 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1].strip()
    return None


async def require_team_key(authorization: str | None = Header(default=None)) -> None:
    expected = os.environ.get("NOBA_API_KEY")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service missing NOBA_API_KEY — deploy misconfigured.",
        )

    supplied = _extract_bearer(authorization)
    if not supplied or not hmac.compare_digest(supplied, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
