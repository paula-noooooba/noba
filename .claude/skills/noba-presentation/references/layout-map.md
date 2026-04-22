# Layout map

One entry per primitive layout. Each row links **JSX reference**,
**python-pptx builder**, **atoms used**, **`deck_spec` shape**, and
**demo reference** (which slide in which HTML template shows this layout
rendered). When drafting a deck, pick the layout row first, then fill
the data shape.

---

## `cover`

- **JSX:** `web/slides/TitleSlide.jsx`
- **Builder:** `build_cover` (primitive)
- **Figma:** [NOBA PPT Design System — node 3:5](https://www.figma.com/design/qqNtw4M8gc3zYRHwKJae7W/NOBA-PPT-Design-System?node-id=3-5)
- **Atoms:** Logo (dark, cover), inline Arrow. **No Shell.**
- **Data shape:**
  ```py
  {
    "layout":   "cover",
    "title":    "Next-Generation Coffee Innovation",  # ink, not accent
    "subtitle": "Identifying and testing new growth opportunities",
    "client":   "lavazza",
    "date":     "september 2025",
  }
  ```
- **Intentionally not supported:**
  - `eyebrow` — Figma cover has no eyebrow. Ignore if present in spec.
  - `accent` — title is always ink (`#1A1A1A`). No accent.
- **Visual anatomy:**
  - Full-bleed white, 48 px padding all sides (`slide-pad-cover`).
  - Logo pinned top-right at 48/48, size 368×48.
  - Title left-aligned at (48, 322), 1094 px wide, 140 px Helvetica Light.
  - Subtitle directly below title at y=622, 36 px Helvetica Light.
  - Caption bottom-left at (48, 997): small arrow then
    "Prepared for {client} | {date}" in 24 px Helvetica Regular, solid
    ink `#1A1A1A` (design override of the Figma's 50 % black for full
    contrast).
- **Demo:** `web/templates/template-snackin.html` — slide 1 (to be
  refreshed after the template migration).

## `context`

- **JSX:** `web/slides/ContextSlide.jsx`
- **Builder:** `build_context`
- **Atoms:** Logo (dark), Tag, Arrow (dark) + photo placeholder
- **Data shape:**
  ```py
  {
    "layout": "context",
    "tag": "Context",
    "headline": "Healthy snacking is crowded.",     # big
    "lead": "Three SKUs are ready.",                 # 23px
    "body": "We want to know which hero SKU earns…",# 17px
    # image: future — path under web/assets/
  }
  ```
- **Demo:** template-snackin, slide 2

## `content_cards`

- **JSX:** `web/slides/ContentSlide.jsx`
- **Builder:** `build_content_cards`
- **Atoms:** Logo, Tag, Arrow
- **Data shape:**
  ```py
  {
    "layout": "content_cards",
    "tag": "Approach",
    "title": "Three moves that matter.",
    "cards": [
      {"num": "01", "title": "Read the shelf",      "body": "…"},
      {"num": "02", "title": "Put SKUs to the test","body": "…"},
      {"num": "03", "title": "Sharpen the pitch",   "body": "…"},
    ],
  }
  ```
- **Demo:** template-snackin, slide 3

## `objectives`

- **JSX:** `web/slides/ObjectivesSlide.jsx`
- **Builder:** `build_objectives`
- **Atoms:** Logo, Tag, Rules (between rows), Arrow
- **Data shape:**
  ```py
  {
    "layout": "objectives",
    "tag": "Objectives",
    "statement": "Decide, fast, on the hero SKU.",   # accent colour
    "accent": "orange",
    "items": [
      {"title": "Clarify demand",   "body": "Which SKU wins…"},
      {"title": "Validate claims",  "body": "…"},
      {"title": "Shape the pitch",  "body": "…"},
    ],
  }
  ```
- **Demo:** template-snackin, slide 4 / template-basic, slide 3

## `activities`

- **JSX:** `web/slides/ActivitiesSlide.jsx`
- **Builder:** `build_activities`
- **Atoms:** Logo, Tag, Dots (lg, accent), Rule, deliverable pills, Arrow
- **Data shape:**
  ```py
  {
    "layout": "activities",
    "tag": "Activities",
    "title": "Three tracks, one proof point.",
    "cards": [
      {"color": "orange", "title": "Shelf ethnography", "body": "…"},
      {"color": "lime",   "title": "Blind SKU tests",   "body": "…"},
      {"color": "pink",   "title": "Pitch workshop",    "body": "…"},
    ],
    "deliverables": ["Insight report", "Workshop playback", "Five-second pitch"],
  }
  ```
- **Demo:** template-snackin, slide 5

## `timeline`

- **JSX:** `web/slides/TimelineSlide.jsx`
- **Builder:** `build_timeline`
- **Atoms:** Logo, Tag, axis line, Dots (lg), Arrow
- **Data shape:**
  ```py
  {
    "layout": "timeline",
    "tag": "Methodology",
    "title": "A four-phase path to clarity.",
    "phases": [
      {"num": "01", "name": "Sense",  "range": "Wk 1–2", "body": "…"},
      {"num": "02", "name": "Shape",  "range": "Wk 3–4", "body": "…"},
      {"num": "03", "name": "Stress", "range": "Wk 5–6", "body": "…"},
      {"num": "04", "name": "Ship",   "range": "Wk 7–8", "body": "…"},
    ],
  }
  ```
- **Demo:** template-snackin, slide 6

## `deliverables`

- **JSX:** `web/slides/DeliverablesSlide.jsx`
- **Builder:** `build_deliverables`
- **Atoms:** Logo, Tag, Dots (lg, accent), Rules, Arrow
- **Data shape:**
  ```py
  {
    "layout": "deliverables",
    "tag": "Deliverables",
    "statement": "What you walk away with.",
    "accent": "blue",
    "items": [
      {"color": "orange", "title": "Insight report",    "body": "…"},
      {"color": "lime",   "title": "Workshop playback", "body": "…"},
      {"color": "pink",   "title": "Go-to-market brief","body": "…"},
    ],
  }
  ```

## `framework`

- **JSX:** `web/slides/FrameworkSlide.jsx`
- **Builder:** `build_framework`
- **Atoms:** Logo, Tag, axis line, 4 coloured cards, Arrow
- **Data shape:**
  ```py
  {
    "layout": "framework",
    "tag": "Framework",
    "title": "Four directions on the spectrum.",
    "axis_left": "Functional",
    "axis_right": "Emotional",
    "cards": [
      {"color": "orange",   "title": "Fuel",   "body": "…"},
      {"color": "lime-alt", "title": "Craft",  "body": "…"},
      {"color": "lavender", "title": "Ritual", "body": "…"},
      {"color": "pink",     "title": "Joy",    "body": "…"},
    ],
  }
  ```
- **Demo:** template-snackin, slide 7

## `stats`

- **JSX:** `web/slides/StatsSlide.jsx`
- **Builder:** `build_stats`
- **Atoms:** Logo, Tag, 4 overlapping circles, Arrow
- **Data shape:**
  ```py
  {
    "layout": "stats",
    "tag": "Our expertise",
    "title": "Four numbers, one story.",
    "stats": [
      {"num": "120+", "label": "Projects shipped", "color": "orange"},
      {"num": "20",   "label": "Countries",        "color": "lime"},
      {"num": "40+",  "label": "Active brands",    "color": "pink"},
      {"num": "10y",  "label": "Track record",     "color": "blue"},
    ],
  }
  ```
- **Demo:** template-snackin, slide 8

## `gantt`

- **JSX:** `web/slides/GanttSlide.jsx`
- **Builder:** `build_gantt`
- **Atoms:** Logo, Tag, Rules, gantt bars (accent), Arrow
- **Data shape:**
  ```py
  {
    "layout": "gantt",
    "tag": "Timings",
    "big_number": "8",
    "caption": "From kickoff to shareable direction.",
    "weeks": 8,
    "phases": [
      {"name": "Sense",  "start": 0, "len": 2, "color": "orange"},
      {"name": "Shape",  "start": 2, "len": 2, "color": "lime"},
      {"name": "Stress", "start": 4, "len": 2, "color": "pink"},
      {"name": "Ship",   "start": 6, "len": 2, "color": "blue"},
    ],
  }
  ```

## `costs`

- **JSX:** `web/slides/CostsSlide.jsx`
- **Builder:** `build_costs`
- **Atoms:** Shell (dark), Logo (light), Tag (inv), Rules (inv), circles, Arrow (light)
- **Data shape:**
  ```py
  {
    "layout": "costs",
    "tag": "Investment",
    "statement": "One fee. Every moment.",
    "circle_colors": ["orange", "lime", "pink", "blue"],
    "rows": [
      {"label": "Sense + Shape", "amount": "€ 24,000"},
      {"label": "Stress",        "amount": "€ 18,000"},
      {"label": "Ship",          "amount": "€ 12,000"},
    ],
    "total": {"label": "Total", "amount": "€ 54,000"},
  }
  ```

## `dark_outro`

- **JSX:** `web/slides/DarkSlide.jsx`
- **Builder:** `build_dark_outro`
- **Atoms:** Shell (dark), Logo (light), Arrow (light)
- **Data shape:**
  ```py
  {
    "layout": "dark_outro",
    "eyebrow": "The NOBA way",
    "headline": "Move decisively. Test early. Ship the story.",
    "footnote": "",   # optional
  }
  ```
- **Demo:** template-snackin, slide 9 / template-basic, slide 4

---

## Spine aliases

Semantic slide names used by `spine-checklist.md` that map onto a
primitive layout via `SPINE_ALIASES` in `build_deck.py`:

| Spine name | Primitive |
|---|---|
| `mission`                | `dark_outro` |
| `what_we_do`             | `content_cards` |
| `clients_grid`           | `content_cards` |
| `expertise_stats`        | `stats` |
| `why_us_overview`        | `content_cards` |
| `why_us_deepdive`        | `deliverables` |
| `multidisciplinary_team` | `activities` |
| `gellify`                | `context` |
| `case_study`             | `content_cards` |
| `team`                   | `activities` |
| `timings`                | `gantt` |
| `budget`                 | `costs` |
| `noba_way_divider`       | `dark_outro` |
| `methodology_overview`   | `timeline` |
| `phase_detail`           | `activities` |
| `ending_03`              | `dark_outro` |

When adding a new spine name, update the alias table in
`build_deck.py` **and** the corresponding row here.
