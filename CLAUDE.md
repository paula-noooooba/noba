# NOBA Presentation Generator

Deck-generator for NOBA, a strategic design consultancy. Starting with
**commercial proposals** and expanding to credentials, internal updates,
and case-study decks. The workflow is skill-driven: a user pastes source
material into the chat, Claude invokes the `noba-presentation` skill,
and the skill produces either a structured-text outline (default) or a
`.pptx` file.

## Tech stack

- **Python + `python-pptx`** — the only output format the skill emits.
  Google Slides consumes the `.pptx` via import.
- **`design/tokens.json`** — single source of truth for every colour,
  type scale, spacing, and shape value used in a deck.
- **`web/`** — the canonical visual reference. Authored in React/JSX
  so the layouts can be proofed in a browser before being ported to
  python-pptx. Not an output format; not loaded at skill runtime.
- **`.claude/skills/noba-presentation/`** — the Agent Skill that orchestrates
  everything.

## How to use

In a Claude Code session rooted at this repo:

1. Paste the client brief / source material into the chat.
2. Say *"build a NOBA deck for this"* or invoke `/noba-presentation`.
3. Default mode is **structured text** — Claude returns a slide-by-slide
   outline for review. Ask for *"export to pptx"* to run
   `scripts/build_deck.py` and produce a file.

## Project conventions

- **All visual values live in `design/tokens.json`.** Changing a brand
  colour = editing one line. Never hardcode hex or pixel values in
  python-pptx builders.
- **`web/slides/*.jsx` is the visual spec.** Each JSX component has a
  1:1 counterpart in `scripts/build_deck.py` (see
  `.claude/skills/noba-presentation/references/layout-map.md`).
  Changes to layout happen first in JSX, then port to the matching
  builder and token file.
- **`web/templates/template-*.html`** are rendered reference decks. Use
  them as the side-by-side visual check when reviewing a generated
  `.pptx`.
- **Source material is pasted, not fetched.** The skill's step 2 extracts
  client / goal / context from the pasted text and summarises it back
  before drafting.
- **Full spine is the default.** Short decks require explicit permission
  to drop slides — never silent truncation.

## Directory map

```
design/tokens.json               Visual values (hex, px, scale)
web/                             Visual reference — JSX + HTML demos
  slides/                        12 layout components
  atoms/                         Logo, Arrow, Tag, Shell, Rule, Dot
  templates/                     Rendered demo decks
  runtime/deck-stage.js          <deck-stage> web component
.claude/skills/noba-presentation/
  SKILL.md                       Procedural workflow (~200 lines)
  references/                    Content-level guardrails
  scripts/
    tokens.py                    Loads tokens.json → C, S, T, SLIDE
    build_deck.py                python-pptx builders (1:1 with JSX)
service/                         Phase 2 — deck-generation API (see service/README.md)
  app.py                         FastAPI app
  modal_app.py                   Modal deployment entrypoint
  routes/                        /healthz, /version, /v1/decks
  services/                      claude_runner, deck_builder, storage
  models/schemas.py              DeckRequest / DeckResponse / DeckSpec
  tests/                         End-to-end smoke tests
```

Plans:
- Phase 1 (this repo's skill): `~/.claude/plans/hey-claude-i-want-polymorphic-church.md`
- Phase 2 (the service): `~/.claude/plans/noba-deck-service.md`
