# Brand identity — semantic usage

Raw values live in `design/tokens.json`. **This file explains intent**
— which token applies where, which pairings are canonical, and which
rules must not be broken.

Load this file when entering .pptx mode or when the user asks about
visual precision.

---

## Typography

Single family everywhere: **Helvetica Neue** (`T.family`). Three weights
in use: 300 (Light), 400 (Regular), 700 (Bold). No other fonts, no
italics.

| Token | Use for |
|---|---|
| `T.hero()`        | Cover slide headline only. Accent colour, weight 300. |
| `T.display()`     | Dark outro headline. White, weight 300. |
| `T.headline()`    | Two-column statements (objectives / deliverables). Accent colour, weight 300. |
| `T.title()`       | Slide-level section titles (content cards, activities, timeline, framework, stats). Ink, weight 300. |
| `T.stat_number()` | Numbers inside stat circles. Ink, weight 400. |
| `T.lead()`        | Lead paragraph under a headline. Ink, weight 400. |
| `T.body()`        | Default body copy. Ink, weight 400. |
| `T.body_sm()`     | Card body in timeline / framework. Ink, weight 400. |
| `T.caption()`     | Short descriptors. Ink, weight 400. |
| `T.label()`       | Section tags, column headers, eyebrows, numeric prefixes ("01"). Uppercase, tracking +0.08em. |
| `T.micro()`       | Sub-brand ("a gellify company"), fine print. |

**Never** use size values directly in `build_deck.py`. Always go through
`T.<name>()`.

## Colour

### Neutrals

| Token | Use for |
|---|---|
| `C.neutral_paper`    | Slide background when on a paper layout. White. |
| `C.neutral_ink`      | Default text. Lines on paper. Arrows. |
| `C.neutral_dark`     | Shell background for `costs` and `dark_outro`. |
| `C.neutral_card`     | `content_cards`, `activities` card fill. |
| `C.neutral_gray`     | Rule lines between rows on paper. |
| `C.neutral_hairline` | Thin separators — rarely needed. |
| `C.neutral_mid_ink`  | 45% ink — faded secondary text, tag border. |
| `C.neutral_mid_inv`  | 50% white — rule lines and tag borders on dark. |

### Accents

| Token | Primary use |
|---|---|
| `C.accent_pink`     | Cover headline. One framework card. |
| `C.accent_orange`   | Objectives statement. Track 1 dot. |
| `C.accent_lime`     | Track 2 dot. Framework card 2. |
| `C.accent_lime_alt` | Alternative lime for framework variants. |
| `C.accent_pink`     | Track 3 dot. |
| `C.accent_lavender` | Framework card 3. |
| `C.accent_blue`     | Deliverables statement. Stats circle 4. |

**Default rotation for dotted cards** (when the deck doesn't specify):
orange → lime → pink → blue. Stick to this rotation unless the user
picks otherwise — consistency across decks matters more than variety.

### Pairings that work

- Pink headline + ink body on paper ← cover
- Orange headline + ink body on paper ← objectives
- Blue headline + ink body on paper ← deliverables
- White + light logo on `C.neutral_dark` ← outro, costs
- Accent card + white text ← only `pink` and `blue` cards (lime / lime-alt / orange / lavender stay ink)

### Pairings that don't

- Lime text on paper — fails contrast. Use ink.
- Accent on accent — never. Ink / white text only.
- Two accents as headline + body on the same slide. Pick one.

## Spacing

All px values in `design/tokens.json`. In builders, always reference
`S.<name>` (EMU) or `px_to_emu(n)`.

| Token | Use |
|---|---|
| `S.slide_pad_y` = 60 | Top/bottom padding inside a slide frame. |
| `S.slide_pad_x` = 72 | Left/right padding inside a slide. |
| `S.block_gap` = 40  | Between distinct content blocks (headline → body). |
| `S.stack_gap` = 28  | Between items in a stacked list. |
| `S.card_gap` = 24   | Between cards in a row. |
| `S.card_pad` = 36   | Inside a card. |
| `S.inline_gap` = 12 | Between inline items (pill chips). |

## Shape

- Corner radius **24 px** for cards, photos, shells.
- Pills / tags: radius 999 (full round).
- Stat circles: 220 px (large), 120 px (costs variant).
- Stat overlap: -32 px (large), -20 px (costs).
- Rule line: 1 px. Axis line: 2 px. Timeline dot: 20 px.

## Logo & arrow

- **Logo positions:** `cover` (top-right, +60/+72 offsets), `inside`
  (+48/+60 offsets). No other positions.
- **Logo variant:** `dark` on paper, `light` on `C.neutral_dark`.
- **Arrow:** bottom-right, every slide. Dark on paper, light on dark.
- Never rotate, flip, scale, or recolour logo or arrow.

## What not to do

- ❌ Invent a new accent colour. Add to `tokens.json` first if one is
  required, then use by name.
- ❌ Hardcode a hex or pixel value anywhere in `build_deck.py`.
- ❌ Use multiple typefaces. Helvetica only.
- ❌ Use shadows, gradients, or 3D effects. Flat and structural only.
- ❌ Centre-align body copy. Body is always left-aligned (except inside
  stat circles).
