/**
 * Classifies source text into a slide plan by calling the Claude API.
 *
 * ANNOTATED_CATALOG: paste the output of dumpLayoutCatalog() here and fill in
 * each "use_when" with one sentence describing when to use that layout.
 */
var ANNOTATED_CATALOG = [
  // Example shape — replace with your real catalog from dumpLayoutCatalog():
  // {
  //   "layout": "Title and body",
  //   "use_when": "A short list of bullet points under one heading",
  //   "placeholders": [
  //     { "key": "TITLE_0", "type": "TITLE", "index": 0 },
  //     { "key": "BODY_0", "type": "BODY", "index": 0 }
  //   ]
  // }
];

var ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
var DEFAULT_MODEL = 'claude-sonnet-4-6';
var DEFAULT_TARGET_SLIDES = '10-12';

/**
 * Returns a slide plan: [{layout, placeholders: [{key, value}]}].
 * Slides whose layout/placeholders fail validation are converted to fallback
 * entries ({layout: "__fallback__", text}) so content is never dropped.
 */
function classifySourceText(sourceText, targetSlides) {
  if (!ANNOTATED_CATALOG.length) {
    throw new Error('ANNOTATED_CATALOG is empty. Run dumpLayoutCatalog() and paste the annotated result into Classifier.gs.');
  }
  var raw = callClaude_(buildPrompt_(sourceText, targetSlides || DEFAULT_TARGET_SLIDES));
  var plan = JSON.parse(raw);
  return validatePlan_(plan);
}

function buildPrompt_(sourceText, targetSlides) {
  return [
    'You convert a source document into a Google Slides plan using a fixed set of template layouts.',
    '',
    'AVAILABLE LAYOUTS (with placeholder keys and when to use each):',
    JSON.stringify(ANNOTATED_CATALOG, null, 2),
    '',
    'RULES:',
    '1. Restructure freely into a clear narrative. For proposals use: cover, context, objectives, approach, timeline, team, investment, expected impact, why us. Do NOT mirror the document order if a better narrative exists.',
    '2. Prefer DENSE slides over one slide per document section. Merge related sections: all engagement phases belong on one or at most two slides; effort tables and pricing belong together on one slide. Target about ' + targetSlides + ' slides for a proposal-sized document.',
    '3. For each slide pick exactly one layout from the catalog and fill its placeholders. Use the placeholder "key" values exactly as listed. Multi-line/bullet content goes into one placeholder value with lines separated by "\\n". Leave a placeholder out if you have nothing for it.',
    '4. If a piece of content fits no layout, use layout name "__fallback__" and put the content in a single placeholder with key "TEXT" — never drop content.',
    '5. Do not invent facts; only reorganize and condense what is in the source.',
    '',
    'SOURCE DOCUMENT:',
    sourceText
  ].join('\n');
}

/** Schema for structured output — the API guarantees the response matches it. */
var SLIDE_PLAN_SCHEMA = {
  type: 'object',
  properties: {
    slides: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          layout: { type: 'string' },
          placeholders: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                key: { type: 'string' },
                value: { type: 'string' }
              },
              required: ['key', 'value'],
              additionalProperties: false
            }
          }
        },
        required: ['layout', 'placeholders'],
        additionalProperties: false
      }
    }
  },
  required: ['slides'],
  additionalProperties: false
};

/** Calls the Messages API and returns the JSON text of the slide plan. */
function callClaude_(prompt) {
  var apiKey = getRequiredProperty_('ANTHROPIC_API_KEY');
  var model = PropertiesService.getScriptProperties().getProperty('CLAUDE_MODEL') || DEFAULT_MODEL;

  var response = UrlFetchApp.fetch(ANTHROPIC_API_URL, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify({
      model: model,
      max_tokens: 16000,
      output_config: { format: { type: 'json_schema', schema: SLIDE_PLAN_SCHEMA } },
      messages: [{ role: 'user', content: prompt }]
    }),
    muteHttpExceptions: true
  });

  var code = response.getResponseCode();
  if (code !== 200) {
    throw new Error('Claude API error ' + code + ': ' + response.getContentText());
  }
  var data = JSON.parse(response.getContentText());
  if (data.stop_reason === 'refusal') {
    throw new Error('Claude declined the request: ' + JSON.stringify(data.stop_details));
  }
  if (data.stop_reason === 'max_tokens') {
    throw new Error('Slide plan was truncated (max_tokens). Shorten the source document or split it.');
  }
  var textBlock = (data.content || []).filter(function (b) { return b.type === 'text'; })[0];
  if (!textBlock) {
    throw new Error('Unexpected API response: no text content. ' + response.getContentText());
  }
  return textBlock.text;
}

/**
 * Validates the plan against the catalog. Slides referencing unknown layouts
 * are rewritten as fallback slides; unknown placeholder keys are dropped with
 * a log line (the generator also skips gracefully).
 */
function validatePlan_(plan) {
  var byName = {};
  ANNOTATED_CATALOG.forEach(function (entry) {
    byName[entry.layout.toLowerCase()] = entry;
  });

  return plan.slides.map(function (slide) {
    if (slide.layout === '__fallback__') return slide;

    var entry = byName[String(slide.layout).toLowerCase()];
    if (!entry) {
      Logger.log('Unknown layout "%s" — routing slide to fallback.', slide.layout);
      var text = slide.placeholders.map(function (p) { return p.value; }).join('\n\n');
      return { layout: '__fallback__', placeholders: [{ key: 'TEXT', value: text }] };
    }

    var validKeys = {};
    entry.placeholders.forEach(function (p) { validKeys[p.key] = true; });
    var kept = slide.placeholders.filter(function (p) {
      if (!validKeys[p.key]) {
        Logger.log('Layout "%s" has no placeholder "%s" — skipping that value.', entry.layout, p.key);
        return false;
      }
      return true;
    });
    return { layout: entry.layout, placeholders: kept };
  });
}
