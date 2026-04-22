# Spine checklist

Every NOBA commercial proposal ships with this 20-slide spine unless the
user explicitly approves dropping specific slides. Half 1 (slides 1–11)
is NOBA credentials; half 2 (slides 12–20) is project-specific.

Run through this list in step 6 of the skill workflow as the final
self-check before emitting a draft.

---

## Half 1 — NOBA credentials

| # | Slide | Layout (primitive) | Source content |
|---|---|---|---|
| 1 | **Cover** | `cover` | Brief — client + title + date |
| 2 | **Mission** | `dark_outro` (via `mission`) | `content-blocks.md` — Mission |
| 3 | **What We Do** | `content_cards` (via `what_we_do`) | `content-blocks.md` — What We Do |
| 4 | **Clients** | `content_cards` (via `clients_grid`) | `content-blocks.md` — Country list (20) |
| 5 | **Our Expertise** | `stats` (via `expertise_stats`) | `content-blocks.md` — Our Expertise |
| 6 | **Why NOBA** | `content_cards` (via `why_us_overview`) | `content-blocks.md` — Why They Choose Us |
| 7 | **Why NOBA — depth** | `deliverables` (via `why_us_deepdive`) | `content-blocks.md` — Driving New Growth |
| 8 | **Team** | `activities` (via `multidisciplinary_team`) | `content-blocks.md` — Multidisciplinary Team |
| 9 | **GELLIFY ecosystem** | `context` (via `gellify`) | `content-blocks.md` — GELLIFY |
| 10 | **Case study** | `content_cards` (via `case_study`) | `case-studies.md` — pick closest fit |
| 11 | **NOBA way — divider** | `dark_outro` (via `noba_way_divider`) | `content-blocks.md` — NOBA way tagline |

## Half 2 — Project

| # | Slide | Layout (primitive) | Source content |
|---|---|---|---|
| 12 | **Context** | `context` | Step-2 extracted context facts |
| 13 | **Objectives** | `objectives` | Step-2 extracted objectives |
| 14 | **Methodology overview** | `timeline` (via `methodology_overview`) | 4 phases default |
| 15 | **Phase detail — Sense** | `activities` (via `phase_detail`) | Activities + deliverables |
| 16 | **Phase detail — Shape** | `activities` (via `phase_detail`) |   |
| 17 | **Phase detail — Stress** | `activities` (via `phase_detail`) |   |
| 18 | **Phase detail — Ship** | `activities` (via `phase_detail`) |   |
| 19 | **Timings** | `gantt` (via `timings`) | 8 weeks default |
| 20 | **Budget** | `costs` (via `budget`) | Based on phase count + scope |
| 21 | **Closing — The NOBA way** | `dark_outro` (via `ending_03`) | `content-blocks.md` — NOBA way tagline |

---

## Self-check — every slide must have

- [ ] Section tag (except cover, mission, dark outros)
- [ ] Arrow atom, bottom-right (every slide)
- [ ] Correct Logo variant (`dark` on paper, `light` on shell)
- [ ] Layout name that matches a row in `layout-map.md`
- [ ] No raw hex or pixel values in the outline

## When dropping slides

The user can ask to drop slides for a credentials-only or short deck.
Rules:

- **Never silently drop.** List the slides you propose to drop and get
  an explicit "yes" before dropping any.
- **Minimum viable deck** (for pitches under 5 minutes): slides 1, 2,
  3, 5, 9, 11, 20, 21.
- **Credentials-only deck** (no project): drop slides 12–20.
- **Project-only deck** (known client, no intro needed): drop slides
  2–11.

Record the drop in the outline header: *"Short deck — slides 4, 6, 7,
8 dropped per user instruction."*
