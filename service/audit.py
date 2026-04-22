"""Per-request structured audit log.

One JSON line per completed request. Emitted to stdout; Modal collects.
No PII from the brief itself — brief content is not logged. We log only
metadata (timing, slide count, size, requester identity if forwarded).
"""
from __future__ import annotations

import structlog


_logger = structlog.get_logger("noba.audit")


def emit(event: str, **fields) -> None:
    _logger.info(event, **fields)
