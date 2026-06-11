/**
 * Entry points. Run these from the Apps Script editor.
 */

/** Build a deck from any text. Returns the new deck's URL. */
function makeDeckFromText(sourceText, deckName, targetSlides) {
  var plan = classifySourceText(sourceText, targetSlides);
  Logger.log('Slide plan (%s slides):\n%s', plan.length, JSON.stringify(plan, null, 2));
  return buildDeck(plan, deckName || 'Generated deck');
}

/** Build a deck from a Google Doc URL. Returns the new deck's URL. */
function makeDeckFromDoc(docUrl, deckName) {
  var doc = DocumentApp.openByUrl(docUrl);
  var text = doc.getBody().getText();
  return makeDeckFromText(text, deckName || (doc.getName() + ' — deck'));
}

/** First end-to-end test: builds a deck from the Fluidra proposal sample. */
function testFluidra() {
  return makeDeckFromText(FLUIDRA_SAMPLE, 'Fluidra Venture Validation — generated');
}
