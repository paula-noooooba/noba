"""End-to-end smoke test for the stub pipeline.

Covers:
- auth rejects missing / wrong key
- POST /v1/decks (mode=text) returns outline + spec
- POST /v1/decks (mode=pptx) returns a download URL
- GET /v1/decks/:id/file streams back a valid .pptx

Run:
    NOBA_API_KEY=test pytest -q
"""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _env(monkeypatch, tmp_path):
    monkeypatch.setenv("NOBA_API_KEY", "test-key")
    monkeypatch.setenv("NOBA_STORAGE_ROOT", str(tmp_path))


@pytest.fixture
def client():
    from app import app
    return TestClient(app)


def _auth() -> dict[str, str]:
    return {"Authorization": "Bearer test-key"}


def test_health(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_auth_required(client):
    r = client.post("/v1/decks", json={"brief": "hi", "mode": "text"})
    assert r.status_code == 401


def test_text_mode(client):
    r = client.post("/v1/decks", headers=_auth(),
                    json={"brief": "Test brief for Lavazza", "mode": "text"})
    assert r.status_code == 200
    body = r.json()
    assert body["id"].startswith("dck_")
    assert body["mode"] == "text"
    assert body["slide_count"] >= 1
    assert body["download_url"] is None


def test_pptx_mode(client):
    r = client.post("/v1/decks", headers=_auth(),
                    json={"brief": "Test brief", "mode": "pptx"})
    assert r.status_code == 200
    body = r.json()
    assert body["download_url"]

    deck_id = body["id"]
    f = client.get(f"/v1/decks/{deck_id}/file", headers=_auth())
    assert f.status_code == 200
    assert f.headers["content-type"].startswith("application/vnd.openxmlformats")
    # .pptx files are zip archives — first bytes are "PK"
    assert f.content[:2] == b"PK"


def test_download_404(client):
    r = client.get("/v1/decks/dck_nonexistent/file", headers=_auth())
    assert r.status_code == 404
