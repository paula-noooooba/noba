"""Unit tests for claude_runner._resolve_model — no network."""
from __future__ import annotations

import pytest

from models.schemas import DeckRequest
from services.claude_runner import DEFAULT_MODEL, _resolve_model


def _req(**kw) -> DeckRequest:
    return DeckRequest(brief="x", **kw)


def test_default_when_nothing_set(monkeypatch):
    monkeypatch.delenv("NOBA_MODEL", raising=False)
    assert _resolve_model(_req()) == DEFAULT_MODEL


def test_env_override(monkeypatch):
    monkeypatch.setenv("NOBA_MODEL", "opus")
    assert _resolve_model(_req()) == "claude-opus-4-7"


def test_request_wins_over_env(monkeypatch):
    monkeypatch.setenv("NOBA_MODEL", "opus")
    assert _resolve_model(_req(model="sonnet")) == "claude-sonnet-4-6"


@pytest.mark.parametrize(
    "alias,expected",
    [
        ("sonnet", "claude-sonnet-4-6"),
        ("opus",   "claude-opus-4-7"),
        ("haiku",  "claude-haiku-4-5-20251001"),
        ("SONNET", "claude-sonnet-4-6"),  # case-insensitive
        ("Opus",   "claude-opus-4-7"),
    ],
)
def test_aliases(monkeypatch, alias, expected):
    monkeypatch.delenv("NOBA_MODEL", raising=False)
    assert _resolve_model(_req(model=alias)) == expected


def test_full_id_passes_through(monkeypatch):
    monkeypatch.delenv("NOBA_MODEL", raising=False)
    full_id = "claude-opus-4-7"
    assert _resolve_model(_req(model=full_id)) == full_id


def test_unknown_alias_passes_through_unchanged(monkeypatch):
    """Forward-compat: if someone passes a future model ID we don't know
    about yet, we don't reject it — we pass it through to the Anthropic
    SDK which will give a clearer error if it's actually invalid."""
    monkeypatch.delenv("NOBA_MODEL", raising=False)
    assert _resolve_model(_req(model="claude-future-9-9")) == "claude-future-9-9"
