/**
 * Reads the Slides template and logs a JSON catalog of its layouts and
 * placeholders. Run once, then paste the output into ANNOTATED_CATALOG in
 * Classifier.gs and fill in the "use_when" descriptions.
 */
function dumpLayoutCatalog() {
  var templateId = getRequiredProperty_('TEMPLATE_ID');
  var presentation = SlidesApp.openById(templateId);
  var layouts = presentation.getLayouts();

  var catalog = layouts.map(function (layout) {
    var placeholders = layout.getPlaceholders().map(function (ph) {
      return {
        // The key the classifier and generator use to address this placeholder.
        key: placeholderKey_(ph),
        type: String(ph.getPlaceholderType()),
        index: ph.getIndex()
      };
    });
    return {
      layout: layout.getLayoutName(),
      use_when: '',
      placeholders: placeholders
    };
  });

  Logger.log(JSON.stringify(catalog, null, 2));
  return catalog;
}

/** Stable placeholder key: TYPE_INDEX, e.g. "TITLE_0", "BODY_1". */
function placeholderKey_(placeholder) {
  return String(placeholder.getPlaceholderType()) + '_' + placeholder.getIndex();
}

function getRequiredProperty_(name) {
  var value = PropertiesService.getScriptProperties().getProperty(name);
  if (!value) {
    throw new Error('Missing Script Property "' + name + '". Set it under Project Settings → Script Properties.');
  }
  return value;
}
