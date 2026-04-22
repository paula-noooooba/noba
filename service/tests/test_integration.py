"""Integration test — hits the real Anthropic API.

Skipped unless both ANTHROPIC_API_KEY and NOBA_RUN_INTEGRATION are set.
Validates that the assembled skill bundle + tool-use contract produces
a parsable deck_spec with sensible shape.

Run:
    ANTHROPIC_API_KEY=sk-ant-... \\
    NOBA_API_KEY=test \\
    NOBA_RUN_INTEGRATION=1 \\
    PYTHONPATH=. pytest -q tests/test_integration.py
"""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


pytestmark = pytest.mark.skipif(
    not (os.environ.get("ANTHROPIC_API_KEY") and os.environ.get("NOBA_RUN_INTEGRATION")),
    reason="ANTHROPIC_API_KEY and NOBA_RUN_INTEGRATION must both be set.",
)


SAMPLE_BRIEF = """\
Client: Lavazza
Industry: Coffee — vending channel
Goal: Validate three next-gen vending blend directions and pick the
winner for a European pilot rollout in Q3.

Context:
- Vending buyers skew 25-45 year-old commuters and office workers.
- Current market share has stalled at flat year-over-year.
- Three blend directions are in prototype: "Fuel", "Craft", and "Ritual".
- We have eight weeks to decide.

Key metrics to nail: repeat-purchase rate, willingness-to-pay vs the
4€ reference cup, claim believability.
"""


@pytest.fixture(autouse=True)
def _env(monkeypatch, tmp_path):
    monkeypatch.setenv("NOBA_API_KEY", "test-key")
    monkeypatch.setenv("NOBA_STORAGE_ROOT", str(tmp_path))
    monkeypatch.delenv("NOBA_STUB_CLAUDE", raising=False)


def test_real_deck_from_brief():
    from app import app

    client = TestClient(app)
    r = client.post(
        "/v1/decks",
        headers={"Authorization": "Bearer test-key"},
        json={
            "brief": SAMPLE_BRIEF,
            "mode": "pptx",
            "defaults": {"accent_cover": "pink", "methodology_phases": 4},
            "requested_by": "paula@noba.com",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()

    # Shape checks
    assert body["id"].startswith("dck_")
    assert body["mode"] == "pptx"
    # Outline contains per-slide headings. Claude may prepend an
    # `## Assumptions` preamble (the system prompt invites it to) — so
    # we don't require the outline to *start* with "## Slide 1", only
    # to contain it.
    assert "## Slide 1" in body["outline"], (
        f"No '## Slide 1' heading in outline; got:\n{body['outline'][:500]}"
    )
    assert body["slide_count"] >= 10, f"Got {body['slide_count']} slides; spine should be larger."
    assert body["download_url"]

    # Every slide has a layout key and at least one other field
    layouts = {s["layout"] for s in body["spec"]["slides"]}
    assert "cover" in layouts, f"Missing cover slide; got layouts {layouts}"

    # Downloaded .pptx opens
    f = client.get(
        f"/v1/decks/{body['id']}/file",
        headers={"Authorization": "Bearer test-key"},
    )
    assert f.status_code == 200
    assert f.content[:2] == b"PK"
    assert len(f.content) > 5_000, "pptx suspiciously small"
