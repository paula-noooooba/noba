# noba-deck-service

NOBA deck-generation API. Called by the `noba-skill` Claude plugin;
returns either a structured-text outline or a `.pptx` download URL.

- **Repo:** monorepo under [`paula-noooooba/noba`](https://github.com/paula-noooooba/noba)
  at `service/` (will split to its own repo later).
- **Source of truth** for visual + content: the same repo at the project
  root (`../design/tokens.json`, `../web/`, `../.claude/skills/noba-presentation/`).
- **Hosting:** Modal (`modal deploy modal_app.py`)
- **Auth:** single shared team key (`NOBA_API_KEY`)
- **Storage:** Modal volume, 30-day TTL

## Status — step 1 of 4 (scaffold)

- [x] FastAPI app + health + version
- [x] POST `/v1/decks` (text / pptx mode)
- [x] GET `/v1/decks/:id/file` (auth-gated download)
- [x] API-key middleware
- [x] Modal deployment entrypoint
- [x] Inline deck builder (minimal — proves plumbing)
- [ ] **Step 2:** wire `noba-core` git submodule + real `build_deck.py` + Claude runner
- [ ] **Step 3:** publish `noba-skill` plugin
- [ ] **Step 4:** dogfood with one teammate

## Local dev

```sh
cp .env.example .env
# edit NOBA_API_KEY to any value for local testing

pip install -e ".[dev]"

uvicorn app:app --reload
```

### Curl smoke test

```sh
# text mode — returns the outline
curl -s -X POST http://localhost:8000/v1/decks \
  -H "Authorization: Bearer $(grep NOBA_API_KEY .env | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"brief": "Lavazza vending proposal", "mode": "text"}' | jq

# pptx mode — returns a download URL
curl -s -X POST http://localhost:8000/v1/decks \
  -H "Authorization: Bearer $(grep NOBA_API_KEY .env | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"brief": "Lavazza vending proposal", "mode": "pptx"}' | jq

# download the file
curl -s -OJ -H "Authorization: Bearer ..." http://localhost:8000/v1/decks/<id>/file
```

### Tests

```sh
NOBA_API_KEY=test pytest -q
```

## Deploy to Modal

```sh
pip install modal
modal token new

modal secret create noba-deck-service-secrets \
  NOBA_API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))") \
  ANTHROPIC_API_KEY=sk-ant-...

modal deploy modal_app.py
```

Modal prints the deployed URL. Save the generated `NOBA_API_KEY` —
this is what teammates paste into the Claude plugin on install.

## Repo layout

```
app.py                 FastAPI app factory
modal_app.py           Modal deployment entrypoint
Dockerfile             Alternative path (Cloud Run / Fly.io)
auth.py                Bearer-token middleware
audit.py               Structured log shim
routes/
  health.py            /healthz, /version
  decks.py             /v1/decks endpoints
services/
  claude_runner.py     brief -> (outline, DeckSpec)   [step 2: real impl]
  deck_builder.py      DeckSpec -> .pptx bytes        [step 2: real impl]
  storage.py           bytes -> url_for(deck_id)
prompts/
  system_prompt.py     Skill + references bundle      [step 2: real impl]
models/
  schemas.py           DeckRequest / DeckResponse / DeckSpec
tests/
  test_decks.py        End-to-end smoke
```

## API — v1

### `POST /v1/decks`

Request:
```json
{
  "brief": "pasted client brief…",
  "mode": "text",
  "defaults": { "accent_cover": "pink", "methodology_phases": 4 },
  "requested_by": "paula@noba.com",
  "model": "sonnet"
}
```

`model` is optional. Accepted values:

| Value | Resolves to |
|---|---|
| `"sonnet"` (default) | `claude-sonnet-4-6` — cost-optimised |
| `"opus"`             | `claude-opus-4-7` — voice-precision for high-stakes briefs |
| `"haiku"`            | `claude-haiku-4-5-20251001` — fastest |
| full model ID        | passes through unchanged |

Precedence: request field beats `NOBA_MODEL` env, which beats the
built-in default.

Response (text mode):
```json
{
  "id": "dck_...",
  "mode": "text",
  "outline": "## Slide 1 — Cover…",
  "spec": { "slides": [...] },
  "slide_count": 21,
  "download_url": null,
  "expires_at": null
}
```

Response (pptx mode): same, with `download_url` + `expires_at`.

### `GET /v1/decks/:id/file`

Returns the `.pptx`. Same `NOBA_API_KEY` required.

### `GET /healthz`, `GET /version`

Unauthenticated.

## Repository layout

This service currently lives as `service/` inside
[`paula-noooooba/noba`](https://github.com/paula-noooooba/noba) —
monorepo for Phase 2 velocity.

The long-term shape (decision D4 in `noba-deck-service.md`) is a
separate `paula-noooooba/noba-deck-service` repo. Split when the
service earns its own release cadence, CI, or dependency tree —
`git subtree split --prefix=service main` will extract this directory
with preserved history.

For now:

- Source of truth for visual + content: **same repo, project root**
  (`../design/tokens.json`, `../web/`, `../.claude/skills/noba-presentation/`).
- Source of truth for API + deployment: **this directory** (`service/`).
- Import path from here to the builder bundle:
  `../.claude/skills/noba-presentation/scripts/build_deck.py` (wired in step 2).
