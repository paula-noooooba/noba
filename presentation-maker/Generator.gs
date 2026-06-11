/**
 * Builds a Google Slides deck from a slide plan produced by classifySourceText.
 * Copies the template (keeping theme + layouts), removes the template's own
 * example slides, then appends one slide per plan entry.
 *
 * Returns the URL of the new deck.
 */
function buildDeck(plan, deckName) {
  var templateId = getRequiredProperty_('TEMPLATE_ID');
  var copy = DriveApp.getFileById(templateId).makeCopy(deckName);
  var deck = SlidesApp.openById(copy.getId());

  var layoutsByName = {};
  deck.getLayouts().forEach(function (layout) {
    layoutsByName[layout.getLayoutName().toLowerCase()] = layout;
  });
  var fallbackLayout = resolveFallbackLayout_(deck, layoutsByName);

  plan.forEach(function (slide) {
    if (slide.layout === '__fallback__') {
      appendFallbackSlide_(deck, fallbackLayout, slide);
      return;
    }
    var layout = layoutsByName[slide.layout.toLowerCase()];
    if (!layout) {
      Logger.log('Layout "%s" not found in deck — using fallback.', slide.layout);
      appendFallbackSlide_(deck, fallbackLayout, slide);
      return;
    }
    var newSlide = deck.appendSlide(layout);
    fillPlaceholders_(newSlide, slide.placeholders);
  });

  // Remove the template's pre-existing showcase slides (everything that was
  // there before we appended ours).
  var slides = deck.getSlides();
  var originalCount = slides.length - plan.length;
  for (var i = 0; i < originalCount; i++) {
    slides[i].remove();
  }

  deck.saveAndClose();
  var url = 'https://docs.google.com/presentation/d/' + copy.getId();
  Logger.log('Deck created: %s', url);
  return url;
}

/** Fills layout placeholders addressed by TYPE_INDEX keys (see Catalog.gs). */
function fillPlaceholders_(slide, placeholderValues) {
  var byKey = {};
  slide.getPlaceholders().forEach(function (ph) {
    byKey[placeholderKey_(ph)] = ph;
  });

  placeholderValues.forEach(function (pv) {
    var ph = byKey[pv.key];
    if (!ph) {
      Logger.log('Slide has no placeholder "%s" — skipped.', pv.key);
      return;
    }
    ph.asShape().getText().setText(pv.value);
  });
}

/**
 * Fallback layout: Script Property FALLBACK_LAYOUT if set, otherwise the
 * first layout whose name contains "blank", otherwise the first layout.
 */
function resolveFallbackLayout_(deck, layoutsByName) {
  var configured = PropertiesService.getScriptProperties().getProperty('FALLBACK_LAYOUT');
  if (configured && layoutsByName[configured.toLowerCase()]) {
    return layoutsByName[configured.toLowerCase()];
  }
  var layouts = deck.getLayouts();
  for (var i = 0; i < layouts.length; i++) {
    if (layouts[i].getLayoutName().toLowerCase().indexOf('blank') !== -1) {
      return layouts[i];
    }
  }
  return layouts[0];
}

/** Appends a fallback slide: chosen blank-ish layout + one plain text box. */
function appendFallbackSlide_(deck, fallbackLayout, slide) {
  var newSlide = deck.appendSlide(fallbackLayout);
  var text = slide.placeholders.map(function (p) { return p.value; }).join('\n\n');
  var width = deck.getPageWidth() - 80;
  var height = deck.getPageHeight() - 80;
  newSlide.insertTextBox(text, 40, 40, width, height);
}
