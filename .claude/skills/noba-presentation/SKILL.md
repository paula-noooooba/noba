---
name: noba-presentation
description: Build NOBA consulting decks — commercial proposals by default, credentials / internal / case-study decks on request. Invoke when the user pastes a brief and asks for a NOBA deck, slides, proposal, pitch, or PowerPoint for a NOBA engagement. The skill handles content extraction, voice, full-spine enforcement, and either structured-text output (default) or .pptx export (on request).
---

# NOBA Presentation Skill

## When to invoke

Trigger when any of these match the user's request:

- *"build a NOBA deck"*, *"NOBA proposal"*, *"NOBA slides"*, *"NOBA pitch"*
- *"commercial proposal for <client>"* in a NOBA context
- The user pastes a client brief / meeting notes and asks for a deck
- `/noba-presentation` is invoked explicitly

Do **not** invoke for: generic "make me slides" requests with no NOBA
context, or for non-deck NOBA work (reports, emails, strategy docs).

## Workflow — follow these six steps in order

### 1. Detect mode

- **Default: structured text.** Produce a slide-by-slide outline in
  Markdown — one slide per heading, with the exact content, layout name,
  and any layout-specific directives (section tag, arrow, logo variant).
- **.pptx mode: only on explicit request** — e.g. *"export to pptx"*,
  *"generate the file"*, *"build the deck as a download"*. When in
  .pptx mode, still show the structured outline first for approval
  unless the user has already approved the outline in this session.

### 2. Ingest source material *(do this before drafting anything)*

If the user pasted text, docs, or notes, extract these fields **before**
writing slides:

- Client name + industry
- Project goal in one sentence
- Context facts (what is happening in the client's world right now)
- Key metrics or constraints the client cares about
- Existing objectives / hypotheses if stated
- Preferred case studies or benchmarks if mentioned

Summarise what was extracted back to the user in **3–5 bullets** and ask
them to confirm or correct before drafting. If the user didn't paste
anything, skip to step 3.

### 3. Confirm minimum brief

Ask for missing fields only from this set: `{client, deck title, project
goal, methodology step count}`. Default everything else per the defaults
table below. Keep clarifying questions to **at most three** in one turn.

### 4. Generate the full spine

Build every slide in the spine — **no truncation**. Use
`references/spine-checklist.md` as the canonical slide list. If the user
asks for a "short deck", list the slides you propose to drop and get
explicit permission before dropping any. Never silently omit.

For each spine slide, use `references/layout-map.md` to pick the correct
layout and pull the matching content from `references/content-blocks.md`
or `references/case-studies.md`. Fixed content blocks (Mission, What We
Do, GELLIFY ecosystem, country list, expertise stats, etc.) should be
used **verbatim** — do not rewrite them slide-to-slide.

### 5. Apply voice

Rewrite every copy line per `references/voice-examples.md`:

- Short, declarative sentences. Target ≤ 16 words per line.
- Outcome-oriented. Lead with what the client walks away with.
- Specific. Replace "leverage", "synergy", "journey", "ecosystem" (when
  generic), "solution" with concrete nouns and verbs.
- Zero corporate hedging ("aim to", "seek to", "strive to", "best-in-class").

Run one pass per slide. If a sentence still reads like a LinkedIn post,
rewrite it using the closest pair in `voice-examples.md` as the pattern.

### 6. Final self-check

Before emitting the final draft, run through `references/spine-checklist.md`
line by line and verify each slide has:

- Section tag (where applicable)
- Arrow atom (bottom-right, every slide except cover/outro as specified)
- Correct Logo variant (`dark` on paper, `light` on shell)
- Correct layout per `references/layout-map.md`
- No raw hex / pixel values bleeding into the outline

If any check fails, fix before emitting. State the self-check outcome in
one line at the end of the draft.

## Output modes

### Structured text (default)

One slide per H2 heading, e.g.:

```
## Slide 3 — Context  (layout: context)

- **Section tag:** Context
- **Headline:** A single moment of truth.
- **Lead:** <outcome-oriented sentence>
- **Body:** <2–3 concrete sentences>
- **Image:** Client workplace photography (TBD)
- **Logo:** dark, inside
- **Arrow:** yes
```

Match the field names from `references/layout-map.md` so the outline
maps cleanly to the .pptx builder.

### .pptx

1. Build a Python `deck_spec` dict matching the layout contracts in
   `references/layout-map.md`.
2. Call `main(deck_spec, out_path)` from `scripts/build_deck.py`.
3. Confirm the output file path to the user.

Never hand-edit the resulting .pptx — all design changes happen via
`design/tokens.json` or via adjusting the layout in `web/slides/*.jsx`
and porting the change to the matching builder.

## Reference files (load on demand)

| File | When to load |
|---|---|
| `references/spine-checklist.md`  | Step 4 (generate spine), step 6 (self-check) |
| `references/layout-map.md`       | Step 4 (pick layouts), anytime building `deck_spec` |
| `references/brand-identity.md`   | .pptx mode, or when the user asks about visual intent |
| `references/content-blocks.md`   | Step 4 (fixed blocks: Mission, What We Do, …) |
| `references/case-studies.md`     | Step 4 (case-study slides) |
| `references/voice-examples.md`   | Step 5 (voice pass) |

## Defaults

| Field | Default |
|---|---|
| Language | English (Spanish variants to come later) |
| Currency | EUR (`€`) |
| Slide count | Full spine — no truncation without permission |
| Methodology phases | 4 (Sense, Shape, Stress, Ship) |
| Accent for cover headline | `pink` |
| Accent for objectives statement | `orange` |
| Accent for deliverables statement | `blue` |
| Timeline | 8 weeks |
| Deck aspect ratio | 16:9 (1920×1080) |

When the user specifies otherwise, their value overrides the default for
the whole deck — don't re-ask per slide.

## Scope

- ✅ Commercial proposals, credentials decks, internal decks, case-study
  decks
- ❌ Non-NOBA decks (use a different skill / built-in capability)
- ❌ Post-build editing of a specific .pptx (regenerate from spec instead)
