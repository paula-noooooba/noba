# NOBA Presentation Maker (prototype)

Turns source text (a proposal, a doc) into a Google Slides deck built from the
layouts of the NOBA template. Classification is done by Claude; the deck is
assembled natively in Google Slides, so it stays fully editable and on-brand.

Pipeline:

```
source text ──▶ Claude (layout catalog + density/reordering rules)
                      │  strict JSON slide plan
                      ▼
        Apps Script generator: copy template → one slide per plan entry
                      ▼
            new Google Slides file in your Drive
```

Everything runs inside your Google account as a Google Apps Script project —
no servers, no OAuth setup.

## Setup (one time, ~15 minutes)

1. **Create the project.** Go to [script.google.com](https://script.google.com)
   → *New project*. Name it "Presentation Maker".

2. **Paste the files.** For each `.gs` file in this folder (`Catalog.gs`,
   `Classifier.gs`, `Generator.gs`, `Main.gs`, `SampleInput.gs`), create a file
   with the same name in the Apps Script editor (＋ → *Script*) and paste the
   contents.

3. **Set Script Properties.** Project Settings (gear icon) → *Script
   Properties* → add:

   | Property | Value |
   |---|---|
   | `TEMPLATE_ID` | `1tV_2_SJ6s6jXofmlEoSB8gX3x0aFKZqYwbnnBa_oalk` (the NOBA template) |
   | `ANTHROPIC_API_KEY` | your Claude API key (console.anthropic.com → API keys) |
   | `CLAUDE_MODEL` | *(optional)* defaults to `claude-sonnet-4-6`; set `claude-opus-4-8` for higher quality |
   | `FALLBACK_LAYOUT` | *(optional)* layout name to use for unclassifiable content; defaults to the first layout whose name contains "blank" |

4. **Extract the layout catalog.** In the editor, select the function
   `dumpLayoutCatalog` and click *Run* (first run asks for permissions —
   approve). Open *Execution log*: it prints a JSON catalog of every layout in
   the template with its placeholders and an empty `"use_when"` field per
   layout.

5. **Annotate the catalog.** Copy the logged JSON into `Classifier.gs`,
   replacing the placeholder value of `ANNOTATED_CATALOG`. Fill in each
   `use_when` with one sentence describing when that layout should be used,
   e.g. `"A timeline of phases or milestones"`, `"3–4 highlights as cards"`.
   This is the only manual mapping work — Claude does the rest.

## First test run

Select `testFluidra` and click *Run*. It classifies the Fluidra proposal text
(in `SampleInput.gs`) and builds a deck from your template. The execution log
prints the URL of the new file; it also appears in your Drive as
*"Fluidra Venture Validation — generated"*.

Review the deck, then tune the `use_when` descriptions in the catalog — that's
the main quality lever.

## Everyday use

- `makeDeckFromDoc("https://docs.google.com/document/d/...")` — builds a deck
  from a Google Doc.
- `makeDeckFromText(text, "Deck name")` — builds a deck from any string.

Run either from the editor, or wire them to a Sheets/Docs menu later
(upgradeable to a sidebar add-on).

## Behavior rules baked into the classifier

- **Dense slides**: related sections are merged (phases on one or two slides,
  effort + pricing together) targeting ~10–12 slides for a proposal-sized doc.
  Pass a different `targetSlides` to `classifySourceText` to override.
- **Reordering allowed**: content is restructured into a proposal narrative
  (context → objectives → approach → timeline → team → investment → impact)
  rather than kept in document order.
- **Fallback**: anything that doesn't fit a layout lands on a fallback slide
  with a plain text box, never dropped.

## Known limits (v1)

Text only (no images/charts), single template, no speaker notes. Bullets are
filled as newline-separated text into the layout's body placeholders.
