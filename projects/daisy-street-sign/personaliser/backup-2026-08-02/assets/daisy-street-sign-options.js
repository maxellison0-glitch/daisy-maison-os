(function () {
  'use strict';

  var PRODUCT_HANDLE = 'mr-mrs-personalised-street-sign-gift';
  var CART_TIMEOUT_MS = 12000;
  var submitting = false;
  var model = window.DaisyStreetSignCartModel;
  var PREVIEW = window.DAISY_PREVIEW || null;
  var PREVIEW_FONT = 'DaisyStreetSignTimes';
  var measureCanvas = document.createElement('canvas');
  var measureContext = measureCanvas.getContext('2d');

  function qs(root, selector) { return (root || document).querySelector(selector); }
  function qsa(root, selector) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); }
  function clean(value) { return String(value || '').replace(/\s+/g, ' ').trim(); }
  function signWording(value) { return clean(value).replace(/\bAND\b/gi, '&').toUpperCase(); }
  function integer(value, fallback) {
    var parsed = parseInt(value, 10);
    return Number.isFinite(parsed) ? parsed : fallback;
  }
  function fitText(el, maxWidth, baseSize, maxSize) {
    el.style.fontSize = baseSize + 'px';
    var w = el.getBBox ? el.getBBox().width : 0;
    if (!w) return;
    el.style.fontSize = Math.min(Math.floor(baseSize * maxWidth / w), maxSize) + 'px';
  }

  function previewNumber(value) { return Math.round(value * 1000) / 1000; }
  function naturalWidth(text) {
    if (!text || !measureContext) return 0;
    measureContext.font = '400 100px "' + PREVIEW_FONT + '", "Times New Roman", serif';
    return measureContext.measureText(text).width / 100;
  }

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character];
    });
  }
  function isTargetProduct() { return window.location.pathname.indexOf('/products/' + PRODUCT_HANDLE) !== -1; }

  function productData() {
    var node = qs(document, '#daisy-street-sign-product-data');
    if (!node) return null;
    try { return JSON.parse(node.textContent); } catch (error) { return null; }
  }

  function money(cents, currency) {
    try {
      return new Intl.NumberFormat(document.documentElement.lang || 'en-GB', {
        style: 'currency',
        currency: currency || 'GBP'
      }).format(integer(cents, 0) / 100);
    } catch (error) {
      return '£' + (integer(cents, 0) / 100).toFixed(2);
    }
  }

  function getForm() {
    return qs(document, 'product-form form[data-type="add-to-cart-form"]') ||
      qs(document, 'form#product-form-9702132711763') ||
      qs(document, 'form[action*="/cart/add"]');
  }

  function getProductColumn(form) {
    return form && (form.closest('.halo-productView-right') || form.closest('.productView-details') || form.parentElement);
  }

  function accuratePreviewSvg(key, label) {
    var p = PREVIEW;
    if (!p) {
      return '<svg class="dm-sign-preview__sign" data-dm-preview="' + key + '" viewBox="0 0 570 125" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + label + '"><rect width="570" height="125" fill="#010101"></rect><rect x="12.4" y="12.4" width="545.2" height="100.2" fill="#fff"></rect></svg>';
    }
    var holes = (p.holes || []).map(function (hole) {
      return '<circle cx="' + hole.x + '" cy="' + hole.y + '" r="' + hole.r + '" fill="' + p.PANEL + '" stroke="' + p.COLOR + '" stroke-width="0.4"></circle>';
    }).join('');
    return [
      '<svg class="dm-sign-preview__sign" data-dm-preview="' + key + '" viewBox="0 0 ' + p.viewW + ' ' + p.viewH + '" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="' + label + '">',
      '<path d="' + p.outer + '" fill="' + p.COLOR + '"></path>',
      '<path d="' + p.inner + '" fill="' + p.PANEL + '"></path>',
      holes,
      '<g data-dm-accurate-line-one>',
      '<g data-dm-line1-prefix><text x="0" y="0" xml:space="preserve" font-family="' + PREVIEW_FONT + ', Times New Roman, serif" font-weight="400" font-size="' + p.MAX_FS + '" letter-spacing="0" text-anchor="start" fill="#010101"></text></g>',
      '<g data-dm-line1-amp><text x="0" y="0" xml:space="preserve" font-family="' + PREVIEW_FONT + ', Times New Roman, serif" font-weight="400" font-size="' + p.MAX_FS + '" letter-spacing="0" text-anchor="start" fill="#010101">&amp;</text></g>',
      '<g data-dm-line1-suffix><text x="0" y="0" xml:space="preserve" font-family="' + PREVIEW_FONT + ', Times New Roman, serif" font-weight="400" font-size="' + p.MAX_FS + '" letter-spacing="0" text-anchor="start" fill="#010101"></text></g>',
      '<g data-dm-line1-single><text x="0" y="0" xml:space="preserve" font-family="' + PREVIEW_FONT + ', Times New Roman, serif" font-weight="400" font-size="' + p.MAX_FS + '" letter-spacing="0" text-anchor="middle" fill="#010101"></text></g>',
      '</g>',
      '<g data-dm-accurate-heart><image width="' + p.HEART_W + '" height="' + p.HEART_H + '" href="' + p.heart + '" xlink:href="' + p.heart + '" preserveAspectRatio="xMidYMid meet"></image></g>',
      '<g data-dm-accurate-line-two><text x="0" y="0" xml:space="preserve" font-family="' + PREVIEW_FONT + ', Times New Roman, serif" font-weight="400" letter-spacing="0" text-anchor="middle" fill="#010101"></text></g>',
      '<rect class="dm-sign-preview__caret" data-dm-preview-caret x="0" y="0" width="3.4" height="0" rx="1.2" fill="#111111" aria-hidden="true"></rect>',
      '</svg>'
    ].join('');
  }

  function directEditorFields(lineOneAttr, lineTwoAttr, secondSign) {
    return [
      '<div class="dm-direct-sign-editor__fields">',
      '<label class="dm-direct-sign-editor__field dm-direct-sign-editor__field--one">',
      '<span class="dm-direct-sign-editor__sr-only">' + (secondSign ? 'Second sign main text' : 'Main sign text') + '</span>',
      '<input type="text" ' + lineOneAttr + ' data-dm-direct-line="one" maxlength="75" autocomplete="off" spellcheck="false" aria-label="' + (secondSign ? 'Second sign main text' : 'Main sign text') + '" placeholder="MR &amp; MRS SMITH"' + (secondSign ? '' : ' required') + '>',
      '</label>',
      '<label class="dm-direct-sign-editor__field dm-direct-sign-editor__field--two">',
      '<span class="dm-direct-sign-editor__sr-only">' + (secondSign ? 'Second sign smaller text' : 'Smaller sign text') + '</span>',
      '<input type="text" ' + lineTwoAttr + ' data-dm-direct-line="two" maxlength="75" autocomplete="off" spellcheck="false" aria-label="' + (secondSign ? 'Second sign smaller text' : 'Smaller sign text') + '" placeholder="FROM THIS DAY FORWARD - 14.08.2026">',
      '</label>',
      '</div>'
    ].join('');
  }

  function createSignEditor(key, label, lineOneAttr, lineTwoAttr, secondSign) {
    return [
      '<div class="dm-direct-sign-editor' + (secondSign ? ' dm-direct-sign-editor--offer' : '') + '" data-dm-direct-sign-editor>',
      accuratePreviewSvg(key, label),
      directEditorFields(lineOneAttr, lineTwoAttr, secondSign),
      '</div>'
    ].join('');
  }

  function createPreview() {
    return [
      '<div class="dm-sign-preview dm-sign-preview--main" data-dm-sign-preview aria-label="Live preview of your personalised sign">',
      '<div class="dm-sign-tap-hint" aria-hidden="true">',
      '<span class="dm-sign-tap-hint__text">Tap the sign to type your wording</span>',
      '<svg class="dm-sign-tap-hint__arrow" viewBox="0 0 24 24" width="24" height="24" focusable="false"><path d="M12 3v15m0 0-6-6m6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
      '</div>',
      createSignEditor('main', 'Main sign preview', 'data-daisy-line-one', 'data-daisy-line-two', false),
      '</div>'
    ].join('');
  }

  function createSecondPreview() {
    return [
      '<div class="dm-sign-preview dm-sign-preview--second" data-dm-sign-preview-second aria-label="Live preview of your second personalised sign">',
      createSignEditor('second', 'Second sign preview', 'data-daisy-second-line-one', 'data-daisy-second-line-two', true),
      '</div>'
    ].join('');
  }

  function createPanel(config) {
    var panel = document.createElement('div');
    panel.className = 'daisy-street-options daisy-mr-mrs-options';
    panel.setAttribute('data-daisy-street-options', '');
    panel.setAttribute('data-second-sign', 'false');
    panel.setAttribute('data-size', 'standard');
    panel.setAttribute('data-size-two', 'standard');
    panel.innerHTML = [
      '<div class="daisy-street-options__header">',
      '<p class="daisy-street-options__eyebrow">Personalised to order</p>',
      '<h2 class="daisy-street-options__title">Mr &amp; Mrs street sign</h2>',
      '<p class="daisy-street-options__copy">Then choose your size and extras below.</p>',
      '</div>',
      createPreview(),
      '<div class="daisy-street-options__ready" data-daisy-ready role="status" aria-live="polite" aria-hidden="true">',
      '<span class="daisy-street-options__ready-tick" aria-hidden="true">&#10003;</span>',
      '<span class="daisy-street-options__ready-copy"><strong>Personalisation complete</strong><span>Ready to add to cart</span></span>',
      '</div>',
      '<div class="daisy-street-options__group">',
      '<h3 class="daisy-street-options__group-title">Size</h3>',
      '<div class="daisy-street-options__size-grid">',
      '<label class="daisy-street-options__choice daisy-street-options__choice--size is-selected"><input type="radio" name="daisy_sign_size" value="standard" checked><span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">Small</span><span class="daisy-street-options__choice-note">28 x 12cm</span></span><span class="daisy-street-options__price">Included</span></label>',
      '<label class="daisy-street-options__choice daisy-street-options__choice--size"><input type="radio" name="daisy_sign_size" value="medium"><span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">Medium</span><span class="daisy-street-options__choice-note">45 x 12cm</span></span><span class="daisy-street-options__price">+' + money(config.prices.medium, config.currency) + '</span></label>',
      '<label class="daisy-street-options__choice daisy-street-options__choice--size"><input type="radio" name="daisy_sign_size" value="large"><span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">Large</span><span class="daisy-street-options__choice-note">57 x 12cm</span></span><span class="daisy-street-options__price">+' + money(config.prices.large, config.currency) + '</span></label>',
      '</div>',
      '</div>',
      '<div class="daisy-street-options__group">',
      '<h3 class="daisy-street-options__group-title">Incredible offer</h3>',
      '<label class="daisy-street-options__choice daisy-street-options__offer">',
      '<input type="checkbox" data-daisy-second-sign aria-expanded="false">',
      '<span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">INCREDIBLE OFFER: Get a second sign for just ' + money(config.prices.second, config.currency) + '</span><span class="daisy-street-options__choice-note">Add another personalised sign</span></span>',
      '<span class="daisy-street-options__price">+' + money(config.prices.second, config.currency) + '</span>',
      '</label>',
      '<div class="daisy-street-options__second-sign-copy daisy-street-options__nested" data-daisy-second-sign-wrap aria-hidden="true" style="display:none;">',
      createSecondPreview(),
      '<div class="daisy-street-options__nested-size">',
      '<h3 class="daisy-street-options__group-title">Second sign size</h3>',
      '<div class="daisy-street-options__size-grid">',
      '<label class="daisy-street-options__choice daisy-street-options__choice--size is-selected"><input type="radio" name="daisy_second_size" value="standard" checked><span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">Small</span><span class="daisy-street-options__choice-note">28 x 12cm</span></span><span class="daisy-street-options__price">Included</span></label>',
      '<label class="daisy-street-options__choice daisy-street-options__choice--size"><input type="radio" name="daisy_second_size" value="medium"><span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">Medium</span><span class="daisy-street-options__choice-note">45 x 12cm</span></span><span class="daisy-street-options__price">+' + money(config.prices.medium, config.currency) + '</span></label>',
      '<label class="daisy-street-options__choice daisy-street-options__choice--size"><input type="radio" name="daisy_second_size" value="large"><span class="daisy-street-options__choice-main"><span class="daisy-street-options__choice-title">Large</span><span class="daisy-street-options__choice-note">57 x 12cm</span></span><span class="daisy-street-options__price">+' + money(config.prices.large, config.currency) + '</span></label>',
      '</div>',
      '</div>',
      '</div>',
      '</div>',
      '<div class="daisy-street-options__error" data-daisy-error role="alert"></div>'
    ].join('');
    return panel;
  }

  // ---- matching heart ----
  // The heart's couple configuration is guessed from the sign's own wording. Free
  // text, so this is a guess: the buttons stay visible so a customer can correct it,
  // and anything unrecognised falls back to Male & Female.
  function inferHeartConfig(lineOne) {
    var text = String(lineOne || '').toUpperCase().replace(/[^A-Z]+/g, ' ');
    if (/\bMRS\b[^A-Z]*\bMRS\b/.test(text)) return 'Female & Female';
    if (/\bMR\b[^A-Z]*\bMR\b/.test(text) && !/\bMRS\b/.test(text)) return 'Male & Male';
    return 'Male & Female';
  }
  function heartConfigValue(card, lineOne) {
    return card.dataset.heartConfig || inferHeartConfig(lineOne);
  }
  function selectedGiftItems(secondSign) {
    var signLineOne = clean((qs(document, '[data-daisy-line-one]') || {}).value);
    var signLineTwo = clean((qs(document, '[data-daisy-line-two]') || {}).value);
    return qsa(document, '.dm-cyg__card').map(function (card) {
      var key = card.dataset.addonKey || 'gift';
      var mode = model.normaliseAddonMode(secondSign, card.dataset.addonMode || 'none');
      var messageOne = qs(document, '#dm-cyg-msg-text-one') || qs(document, '#dm-cyg-msg-text');
      var messageTwo = qs(document, '#dm-cyg-msg-text-two');
      var messageOneValue = clean(messageOne && messageOne.value);
      var messageTwoValue = clean(messageTwo && messageTwo.value);
      var properties = { 'Add-on': card.dataset.name || 'Gift add-on' };
      if (key === 'wedding' && messageOneValue) properties['Personalisation'] = messageOneValue;
      if (key === 'wedding' && mode === 'double' && messageTwoValue) properties['Personalisation 2'] = messageTwoValue;
      if (key === 'heart') {
        // Read at add-to-cart, not when the card is ticked, so a late edit to the
        // sign carries through to the heart.
        properties.Size = 'Small 9 x 9cm (£' + (integer(card.dataset.price, 1495) / 100).toFixed(2) + ')';
        properties.Configuration = heartConfigValue(card, signLineOne);
        var custom = card.dataset.heartWording === 'custom';
        // In custom mode the customer's boxes are authoritative — clearing one must
        // clear it, never silently fall back to the sign's wording.
        var leftValue = custom ? clean((qs(card, '[data-heart-left]') || {}).value) : signLineTwo;
        var rightValue = custom ? clean((qs(card, '[data-heart-right]') || {}).value) : signLineOne;
        if (leftValue) properties['Left text'] = leftValue;
        if (rightValue) properties['Right text'] = rightValue;
      }
      return {
        key: key,
        id: integer(card.dataset.variant, 0),
        name: card.dataset.name || 'Gift add-on',
        price: integer(card.dataset.price, 0),
        mode: mode,
        properties: properties
      };
    }).filter(function (gift) { return gift.id > 0; });
  }

  // The heart's gift box rides along as its own cart line at its real price. It
  // can't reuse the card's 'double' mode, which already means "one per sign".
  function withHeartBox(gifts) {
    var card = qs(document, '.dm-cyg__card[data-addon-key="heart"]');
    if (!card) return gifts;
    var heart = null;
    gifts.forEach(function (gift) { if (gift.key === 'heart') heart = gift; });
    if (!heart || heart.mode === 'none') return gifts;
    if (card.dataset.heartBoxMode !== 'add') return gifts;
    var boxId = integer(card.dataset.boxVariant, 0);
    if (!boxId) return gifts;
    var boxName = card.dataset.boxName || 'Gift Box';
    return gifts.concat([{
      key: 'heartbox',
      id: boxId,
      name: boxName,
      price: integer(card.dataset.boxPrice, 0),
      // Matches the heart's mode, so two hearts for two signs get two boxes.
      mode: heart.mode,
      properties: { 'Add-on': boxName }
    }]);
  }

  function state(form, panel) {
    var secondSign = !!(qs(panel, '[data-daisy-second-sign]') || {}).checked;
    var quantityInput = qs(form, 'input[name="quantity"]');
    return {
      quantity: Math.max(1, integer(quantityInput && quantityInput.value, 1)),
      lineOne: clean((qs(panel, '[data-daisy-line-one]') || {}).value),
      lineTwo: clean((qs(panel, '[data-daisy-line-two]') || {}).value),
      size: ((qs(panel, 'input[name="daisy_sign_size"]:checked') || {}).value || 'standard'),
      secondSign: secondSign,
      secondLineOne: clean((qs(panel, '[data-daisy-second-line-one]') || {}).value),
      secondLineTwo: clean((qs(panel, '[data-daisy-second-line-two]') || {}).value),
      secondSize: ((qs(panel, 'input[name="daisy_second_size"]:checked') || {}).value || 'standard'),
      gifts: withHeartBox(selectedGiftItems(secondSign))
    };
  }

  function setTextGroup(group, x, y, scaleX, scaleY, text) {
    if (!group) return;
    group.setAttribute('transform', 'translate(' + previewNumber(x) + ' ' + previewNumber(y) + ') scale(' + previewNumber(scaleX) + ' ' + previewNumber(scaleY) + ')');
    var node = qs(group, 'text');
    if (node) node.textContent = text || '';
  }

  function renderAccuratePreview(signNode, lineOne, lineTwo) {
    var p = PREVIEW;
    if (!p || !signNode) return;
    var fs1 = p.MAX_FS;
    var cap1 = p.CAP_H * fs1 * p.VSCALE;
    var base1 = p.CAP_CENTER_Y + cap1 / 2;
    var ampIndex = lineOne.indexOf('&');
    var prefixGroup = qs(signNode, '[data-dm-line1-prefix]');
    var ampGroup = qs(signNode, '[data-dm-line1-amp]');
    var suffixGroup = qs(signNode, '[data-dm-line1-suffix]');
    var singleGroup = qs(signNode, '[data-dm-line1-single]');
    var heart = qs(signNode, '[data-dm-accurate-heart] image');

    if (ampIndex !== -1) {
      var prefix = lineOne.slice(0, ampIndex);
      var suffix = lineOne.slice(ampIndex + 1);
      var signatureScaleX = Math.min(1, p.TARGET_W / (naturalWidth('MR & MRS NICHOLS') * fs1));
      var signatureAdvance = naturalWidth('&') * fs1 * signatureScaleX;
      var surroundingNatural = (naturalWidth(prefix) + naturalWidth(suffix)) * fs1;
      var available = Math.max(1, p.TARGET_W - signatureAdvance);
      var lineScaleX = surroundingNatural ? Math.min(1, available / surroundingNatural) : 1;
      var prefixWidth = naturalWidth(prefix) * fs1 * lineScaleX;
      var suffixWidth = naturalWidth(suffix) * fs1 * lineScaleX;
      var totalWidth = prefixWidth + signatureAdvance + suffixWidth;
      var lineStart = p.CX - totalWidth / 2;
      var ampOrigin = lineStart + prefixWidth;
      var suffixOrigin = ampOrigin + signatureAdvance;

      prefixGroup.style.display = '';
      ampGroup.style.display = '';
      suffixGroup.style.display = '';
      singleGroup.style.display = 'none';
      setTextGroup(prefixGroup, lineStart, base1, lineScaleX, p.VSCALE, prefix);
      setTextGroup(ampGroup, ampOrigin, base1, signatureScaleX, p.VSCALE, '&');
      setTextGroup(suffixGroup, suffixOrigin, base1, lineScaleX, p.VSCALE, suffix);

      if (heart) {
        var ampLeft = ampOrigin + p.AMP.xMin * fs1 * signatureScaleX;
        var ampWidth = p.AMP.w * fs1 * signatureScaleX;
        var ampTop = base1 - p.AMP.yMax * fs1 * p.VSCALE;
        var ampHeight = p.AMP.h * fs1 * p.VSCALE;
        heart.setAttribute('x', previewNumber(ampLeft + p.AMP_TIP_X * ampWidth - p.HEART_PIN_X * p.HEART_W));
        heart.setAttribute('y', previewNumber(ampTop + p.AMP_TIP_Y * ampHeight - p.HEART_PIN_Y * p.HEART_H));
      }
    } else {
      var natural = naturalWidth(lineOne) * fs1;
      var singleScaleX = natural ? Math.min(1, p.TARGET_W / natural) : 1;
      prefixGroup.style.display = 'none';
      ampGroup.style.display = 'none';
      suffixGroup.style.display = 'none';
      singleGroup.style.display = '';
      setTextGroup(singleGroup, p.CX, base1, singleScaleX, p.VSCALE, lineOne);
      if (heart) {
        heart.setAttribute('x', previewNumber(p.viewW - p.HEART_W - 40));
        heart.setAttribute('y', '27');
      }
    }

    var line2Group = qs(signNode, '[data-dm-accurate-line-two]');
    var line2Natural = naturalWidth(lineTwo);
    var fs2 = line2Natural ? Math.min(p.DATE_MAX_FS, p.DATE_TARGET_W / line2Natural) : p.DATE_MAX_FS;
    setTextGroup(line2Group, p.CX, p.DATE_BASELINE, 1, p.VSCALE, lineTwo);
    var line2Node = qs(line2Group, 'text');
    if (line2Node) line2Node.setAttribute('font-size', previewNumber(fs2));
    line2Group.setAttribute('opacity', lineTwo ? '0.9' : '0');
  }

  function fitDirectInput(editor, input, line) {
    if (!editor || !input || !PREVIEW) return;
    var width = editor.clientWidth || 0;
    if (!width) return;
    var text = line === 'one' ? signWording(input.value || input.placeholder) : clean(input.value || input.placeholder).toUpperCase();
    var baseSize = width * (line === 'one' ? PREVIEW.MAX_FS : PREVIEW.DATE_MAX_FS) * PREVIEW.VSCALE / PREVIEW.viewW;
    var maxWidth = width * (line === 'one' ? 0.82 : 0.78);
    var measured = naturalWidth(text);
    var fittedSize = measured ? Math.min(baseSize, maxWidth / measured) : baseSize;
    input.style.fontSize = previewNumber(Math.max(line === 'one' ? 10 : 7, fittedSize)) + 'px';
  }

  function updateDirectEditors(panel) {
    qsa(panel, '[data-dm-direct-sign-editor]').forEach(function (editor) {
      fitDirectInput(editor, qs(editor, '[data-dm-direct-line="one"]'), 'one');
      fitDirectInput(editor, qs(editor, '[data-dm-direct-line="two"]'), 'two');
    });
  }

  function caretPoint(group, characterCount, centered) {
    var textNode = group && qs(group, 'text');
    var transform = group && group.transform && group.transform.baseVal.consolidate();
    if (!textNode || !transform) return null;
    var textLength = (textNode.textContent || '').length;
    var offset = Math.max(0, Math.min(characterCount, textLength));
    var totalWidth = textNode.getComputedTextLength ? textNode.getComputedTextLength() : 0;
    var prefixWidth = offset && textNode.getSubStringLength ? textNode.getSubStringLength(0, offset) : 0;
    var localX = (centered ? -totalWidth / 2 : 0) + prefixWidth;
    var matrix = transform.matrix;
    var fontSize = parseFloat(textNode.getAttribute('font-size')) || PREVIEW.MAX_FS;
    var height = Math.max(8, Math.abs(matrix.d) * fontSize * PREVIEW.CAP_H);
    return {
      x: matrix.a * localX + matrix.e,
      y: matrix.f - height,
      height: height,
      scaleX: matrix.a,
      fontSize: fontSize
    };
  }

  function updatePreviewCaret(panel) {
    qsa(panel, '[data-dm-preview-caret]').forEach(function (caret) { caret.style.display = 'none'; });
    var input = document.activeElement;
    if (!input || !panel.contains(input) || !input.hasAttribute('data-dm-direct-line') || !PREVIEW) return;
    var editor = input.closest('[data-dm-direct-sign-editor]');
    var signNode = editor && qs(editor, '[data-dm-preview]');
    var caret = signNode && qs(signNode, '[data-dm-preview-caret]');
    if (!signNode || !caret) return;

    var line = input.getAttribute('data-dm-direct-line');
    var raw = input.value || '';
    var selection = typeof input.selectionStart === 'number' ? input.selectionStart : raw.length;
    var point = null;

    if (!raw) {
      var emptyFontSize = line === 'one' ? PREVIEW.MAX_FS : PREVIEW.DATE_MAX_FS;
      var emptyHeight = Math.max(8, emptyFontSize * PREVIEW.VSCALE * PREVIEW.CAP_H);
      var baseline = line === 'one' ? PREVIEW.CAP_CENTER_Y + emptyHeight / 2 : PREVIEW.DATE_BASELINE;
      point = { x: PREVIEW.CX, y: baseline - emptyHeight, height: emptyHeight, scaleX: 1, fontSize: emptyFontSize };
    } else if (line === 'two') {
      var lineTwoPrefix = clean(raw.slice(0, selection)).toUpperCase();
      point = caretPoint(qs(signNode, '[data-dm-accurate-line-two]'), lineTwoPrefix.length, true);
    } else {
      var lineOneText = signWording(raw);
      var lineOnePrefix = signWording(raw.slice(0, selection));
      var ampIndex = lineOneText.indexOf('&');
      if (ampIndex === -1) {
        point = caretPoint(qs(signNode, '[data-dm-line1-single]'), lineOnePrefix.length, true);
      } else {
        var fullPrefix = lineOneText.slice(0, ampIndex);
        var prefixAmpIndex = lineOnePrefix.indexOf('&');
        if (prefixAmpIndex === -1) {
          point = lineOnePrefix.length <= fullPrefix.length
            ? caretPoint(qs(signNode, '[data-dm-line1-prefix]'), lineOnePrefix.length, false)
            : caretPoint(qs(signNode, '[data-dm-line1-amp]'), 0, false);
        } else {
          var suffixPrefix = lineOnePrefix.slice(prefixAmpIndex + 1);
          point = suffixPrefix.length
            ? caretPoint(qs(signNode, '[data-dm-line1-suffix]'), suffixPrefix.length, false)
            : caretPoint(qs(signNode, '[data-dm-line1-amp]'), 1, false);
        }
      }
    }

    if (!point) return;
    var trailingSpaces = raw.slice(0, selection).match(/ +$/);
    if (trailingSpaces && clean(raw)) {
      point.x += Math.abs(point.scaleX) * naturalWidth(trailingSpaces[0]) * point.fontSize / 2;
    }
    caret.setAttribute('x', previewNumber(point.x - 1.7));
    caret.setAttribute('y', previewNumber(point.y));
    caret.setAttribute('height', previewNumber(point.height));
    caret.style.display = 'block';
  }

  function updatePreview(panel, current) {
    var signs = model.previewSigns(current);
    qsa(panel, '[data-dm-preview]').forEach(function (signNode) {
      var secondSign = signNode.getAttribute('data-dm-preview') === 'second';
      var sign = secondSign ? signs[1] : signs[0];
      var editor = signNode.closest('[data-dm-direct-sign-editor]');
      signNode.hidden = !sign;
      if (editor) editor.hidden = !sign;
      if (!sign) return;
      signNode.dataset.size = secondSign ? current.secondSize : current.size;
      var lineOne = signWording(sign.lineOne || 'MR & MRS SMITH');
      var lineTwo = clean(sign.lineTwo || 'FROM THIS DAY FORWARD - 14.08.2026').toUpperCase();
      renderAccuratePreview(signNode, lineOne, lineTwo);
      var lineOneGroup = qs(signNode, '[data-dm-accurate-line-one]');
      if (lineOneGroup) {
        lineOneGroup.setAttribute('opacity', sign.lineOne ? '1' : '0.4');
        lineOneGroup.classList.toggle('dm-is-placeholder', !sign.lineOne);
      }
      var lineTwoGroup = qs(signNode, '[data-dm-accurate-line-two]');
      if (lineTwoGroup) {
        lineTwoGroup.setAttribute('opacity', sign.lineTwo ? '0.9' : '0.4');
        lineTwoGroup.classList.toggle('dm-is-placeholder', !sign.lineTwo);
      }
    });
    updateDirectEditors(panel);
    updatePreviewCaret(panel);
  }

  function updateChoiceStates(panel) {
    qsa(panel, '.daisy-street-options__choice').forEach(function (choice) {
      var input = qs(choice, 'input');
      choice.classList.toggle('is-selected', !!(input && input.checked));
    });
  }

  function updateReadyState(panel, current) {
    var ready = qs(panel, '[data-daisy-ready]');
    if (!ready) return;
    var complete = !!(current && current.lineOne);
    ready.classList.toggle('is-visible', complete);
    ready.setAttribute('aria-hidden', complete ? 'false' : 'true');
  }

  function updateHeartCard(current) {
    var card = qs(document, '.dm-cyg__card[data-addon-key="heart"]');
    if (!card) return;
    var wrap = qs(card, '[data-heart-config-wrap]');
    var on = (card.dataset.addonMode || 'none') !== 'none';
    if (wrap) {
      wrap.hidden = !on;
      wrap.setAttribute('aria-hidden', on ? 'false' : 'true');
    }
    var value = heartConfigValue(card, current.lineOne);
    qsa(card, '[data-heart-config]').forEach(function (button) {
      var active = button.getAttribute('data-heart-config') === value;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
      button.disabled = !on;
    });
    var combo = !on ? 'none' : (card.dataset.heartBoxMode === 'add' ? 'heartbox' : 'heart');
    qsa(card, '[data-heart-combo]').forEach(function (button) {
      var active = button.getAttribute('data-heart-combo') === combo;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    var custom = card.dataset.heartWording === 'custom';
    qsa(card, '[data-heart-wording-mode]').forEach(function (button) {
      var active = button.getAttribute('data-heart-wording-mode') === (custom ? 'custom' : 'same');
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
      button.disabled = !on;
    });
    var fields = qs(card, '[data-heart-fields]');
    if (fields) {
      fields.hidden = !custom;
      qsa(fields, 'input').forEach(function (input) { input.disabled = !on || !custom; });
    }
    var preview = qs(card, '[data-heart-preview]');
    if (preview) {
      var parts = [current.lineTwo, current.lineOne].filter(Boolean);
      preview.textContent = parts.length
        ? 'Heart will read: ' + parts.join(' · ')
        : 'Fill in your sign above and it copies across.';
      preview.hidden = custom;
    }
  }
  function updateGiftModes(current) {
    updateHeartCard(current);
    qsa(document, '.dm-cyg__card').forEach(function (card) {
      var controls = qs(card, '.dm-addon-mode');
      if (!controls) return;
      var mode = model.normaliseAddonMode(current.secondSign, card.dataset.addonMode || 'none');
      card.dataset.addonMode = mode;
      card.classList.toggle('is-checked', mode !== 'none');
      qsa(controls, '[data-dm-addon-mode]').forEach(function (button) {
        var buttonMode = button.dataset.dmAddonMode;
        var doubleOption = buttonMode === 'double';
        button.hidden = doubleOption && !current.secondSign;
        button.disabled = doubleOption && !current.secondSign;
        var active = buttonMode === mode;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      var message = qs(document, '#dm-cyg-msg');
      if (card.dataset.addonKey === 'wedding' && message) {
        message.hidden = mode === 'none';
        var messageOne = qs(message, '#dm-cyg-msg-text-one') || qs(message, '#dm-cyg-msg-text');
        var messageTwo = qs(message, '#dm-cyg-msg-text-two');
        var secondMessageWrap = qs(message, '#dm-cyg-msg-two');
        if (messageOne) messageOne.required = mode !== 'none';
        if (messageTwo) messageTwo.required = mode === 'double';
        if (secondMessageWrap) secondMessageWrap.hidden = mode !== 'double';
      }
    });
  }

  function totalRows(current, config) {
    var rows = [{ label: 'Street sign', price: config.prices.base * current.quantity }];
    if (current.size === 'medium') rows.push({ label: 'Medium sign upgrade', price: config.prices.medium * current.quantity });
    if (current.size === 'large') rows.push({ label: 'Large sign upgrade', price: config.prices.large * current.quantity });
    if (current.secondSign) rows.push({ label: 'Second personalised sign', price: config.prices.second * current.quantity });
    if (current.secondSign && current.secondSize === 'medium') rows.push({ label: 'Medium second sign upgrade', price: config.prices.medium * current.quantity });
    if (current.secondSign && current.secondSize === 'large') rows.push({ label: 'Large second sign upgrade', price: config.prices.large * current.quantity });
    current.gifts.forEach(function (gift) {
      var line = model.giftCartLine(gift, gift.mode, config.variants, config.prices);
      if (!line) return;
      rows.push({ label: gift.name + (gift.quantity === 2 ? ' × 2' : ''), price: line.linePrice });
    });
    return rows;
  }

  function ensureSticky() {
    var sticky = qs(document, '#dm-sticky-cart');
    if (!sticky) return null;
    sticky.style.removeProperty('display');
    sticky.classList.add('is-ready');
    var button = qs(sticky, '.dm-sticky-btn');
    if (button) button.removeAttribute('onclick');
    if (!qs(sticky, '.dm-sticky-total')) {
      var total = document.createElement('span');
      total.className = 'dm-sticky-total';
      total.setAttribute('aria-live', 'polite');
      total.innerHTML = '<span class="dm-sticky-total__was" hidden></span><span class="dm-sticky-total__current"></span>';
      sticky.insertBefore(total, button || null);
    }
    return sticky;
  }

  function updateTotals(form, panel, current, config) {
    var totals = model.calculateTotal(current, config.variants, config.prices);
    var rows = totalRows(current, config);
    var subtotal = qs(document, '#dm-cyg-subtotal');
    var lines = qs(document, '#dm-cyg-subtotal-lines');
    var total = qs(document, '#dm-cyg-total');
    if (subtotal) subtotal.classList.add('is-visible');
    if (lines) {
      lines.innerHTML = rows.map(function (row) {
        return '<div class="dm-cyg__subtotal-row"><span class="dm-cyg__subtotal-label">' + escapeHtml(row.label) + '</span><span class="dm-cyg__subtotal-value">' + money(row.price, config.currency) + '</span></div>';
      }).join('');
    }
    if (total) total.textContent = money(totals.current, config.currency);

    var sticky = ensureSticky();
    if (!sticky) return;
    var currentPrice = qs(sticky, '.dm-sticky-total__current');
    var wasPrice = qs(sticky, '.dm-sticky-total__was');
    if (currentPrice) currentPrice.textContent = money(totals.current, config.currency);
    if (wasPrice) {
      wasPrice.hidden = !totals.compareAt;
      wasPrice.textContent = totals.compareAt ? money(totals.compareAt, config.currency) : '';
    }
  }

  function updateInterface(form, panel, config) {
    var current = state(form, panel);
    panel.dataset.secondSign = current.secondSign ? 'true' : 'false';
    panel.dataset.size = current.size;
    panel.dataset.sizeTwo = current.secondSize;
    panel.setAttribute('data-size-two', current.secondSize);
    var secondWrap = qs(panel, '[data-daisy-second-sign-wrap]');
    var secondToggle = qs(panel, '[data-daisy-second-sign]');
    if (secondWrap) {
      secondWrap.style.display = current.secondSign ? '' : 'none';
      secondWrap.classList.toggle('is-visible', current.secondSign);
      secondWrap.setAttribute('aria-hidden', current.secondSign ? 'false' : 'true');
    }
    if (secondToggle) secondToggle.setAttribute('aria-expanded', current.secondSign ? 'true' : 'false');
    var requiredSecondLine = qs(panel, '[data-daisy-second-line-one]');
    if (requiredSecondLine) requiredSecondLine.required = current.secondSign;
    updateChoiceStates(panel);
    updateReadyState(panel, current);
    updateGiftModes(current);
    current = state(form, panel);
    updatePreview(panel, current);
    updateTotals(form, panel, current, config);
  }

  function showError(panel, message) {
    var error = qs(panel, '[data-daisy-error]');
    if (!error) return;
    error.textContent = message;
    error.classList.add('is-visible');
    error.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function clearError(panel) {
    var error = qs(panel, '[data-daisy-error]');
    if (!error) return;
    error.textContent = '';
    error.classList.remove('is-visible');
  }

  function weddingCardNeedsMessage(current) {
    return (current.gifts || []).some(function (gift) {
      if (gift.key !== 'wedding' || gift.mode === 'none') return false;
      if (!clean((gift.properties || {}).Personalisation)) return true;
      return gift.mode === 'double' && !clean((gift.properties || {})['Personalisation 2']);
    });
  }

  function validationMessage(current) {
    if (!current.lineOne) return 'Please add line 1 for the main sign.';
    if (current.secondSign && !current.secondLineOne) return 'Please add line 1 for the second sign.';
    if (weddingCardNeedsMessage(current)) return 'Please add the wedding card message.';
    return '';
  }

  function setLoading(loading) {
    submitting = loading;
    qsa(document, '#product-add-to-cart,.dm-sticky-btn').forEach(function (button) {
      if (!button.dataset.daisyOriginalText) button.dataset.daisyOriginalText = button.textContent;
      button.textContent = loading ? 'Adding...' : button.dataset.daisyOriginalText;
      button.disabled = loading;
    });
  }

  function addBundle(items) {
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timeout = window.setTimeout(function () { if (controller) controller.abort(); }, CART_TIMEOUT_MS);
    return fetch('/cart/add.js', {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({ items: items.map(function (item) {
        return { id: item.id, quantity: item.quantity, properties: item.properties };
      }) }),
      signal: controller ? controller.signal : undefined
    }).then(function (response) {
      window.clearTimeout(timeout);
      if (response.ok) return response.json();
      return response.json().catch(function () { return {}; }).then(function (body) {
        throw new Error(body.description || body.message || 'The selected products could not be added to basket.');
      });
    }).catch(function (error) {
      window.clearTimeout(timeout);
      if (error && error.name === 'AbortError') throw new Error('Adding to basket timed out. Please try again.');
      throw error;
    });
  }

  function submitBundle(form, panel, config) {
    if (submitting) return;
    clearError(panel);
    var current = state(form, panel);
    var message = validationMessage(current);
    if (message) { showError(panel, message); return; }
    setLoading(true);
    var bundleId = 'street-sign-' + Date.now();
    addBundle(model.buildCartItems(current, config.variants, config.prices, bundleId)).then(function () {
      var go = function () { window.location.href = (window.routes && window.routes.cart) || '/cart'; };
      qsa(document, '#product-add-to-cart,.dm-sticky-btn').forEach(function (b) { b.classList.add('dm-celebrate'); });
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (reduce) { go(); } else { setTimeout(go, 800); }
    }).catch(function (error) {
      setLoading(false);
      showError(panel, error.message || 'Something went wrong adding these items to basket.');
    });
  }

  function stopNative(event) {
    event.preventDefault();
    event.stopPropagation();
    if (event.stopImmediatePropagation) event.stopImmediatePropagation();
  }

  function hideOldOptions() {
    qsa(document, '.gpo-container,.gpo-app,.gpo-options,.globo-product-options,.globo-options,.globo-formbuilder,[class*="globo-product"],[id*="globo-product"],[data-gpo],[data-globo]').forEach(function (node) {
      if (node.closest('.daisy-street-options')) return;
      node.hidden = true;
      node.setAttribute('aria-hidden', 'true');
      qsa(node, 'input,select,textarea,button').forEach(function (field) { field.disabled = true; });
    });
  }

  function placePanel(form, panel) {
    var giftBlock = qs(document, '#dm-cyg');
    // On phones the gallery + title + price push the sign preview a full
    // viewport down, and most visitors never realise the sign is the form.
    // Personalise-first: move the panel (and its add-ons block, so the
    // configurator stays one unbroken flow) directly under the gallery.
    // Price and CTA remain permanently visible in the mobile sticky bar.
    if (window.matchMedia('(max-width: 767px)').matches) {
      var titleNode = qs(document, '.productView-product .productView-title');
      var titleItem = titleNode && titleNode.closest('.productView-moreItem');
      if (titleItem && titleItem.parentElement) {
        // Target order: [panel][gift block][title]. The settled check keeps the
        // repeated placement timers from re-moving nodes on every tick.
        var settled = panel.parentElement === titleItem.parentElement &&
          panel.nextElementSibling === (giftBlock || titleItem) &&
          (!giftBlock || giftBlock.nextElementSibling === titleItem);
        if (!settled) {
          titleItem.parentElement.insertBefore(panel, titleItem);
          if (giftBlock) titleItem.parentElement.insertBefore(giftBlock, titleItem);
        }
        return;
      }
    }
    if (giftBlock && giftBlock.parentElement) {
      if (giftBlock.previousElementSibling !== panel) giftBlock.parentElement.insertBefore(panel, giftBlock);
      return;
    }
    var anchor = qs(form, '.productView-group') || form.firstElementChild;
    if (anchor) form.insertBefore(panel, anchor);
    else form.appendChild(panel);
  }

  function placePreview() {
    /* preview position is set in createPanel HTML order — no DOM move needed */
  }

  function bindStickyVisibility() {
    var sticky = ensureSticky();
    var primary = qs(document, '#product-add-to-cart');
    if (!sticky || !primary || sticky.dataset.daisyStickyBound) return;
    sticky.dataset.daisyStickyBound = 'true';
    var media = window.matchMedia('(max-width: 767px)');
    var observer = new IntersectionObserver(function (entries) {
      if (media.matches) {
        sticky.classList.add('dm-sticky-visible');
        return;
      }
      sticky.classList.toggle('dm-sticky-visible', !entries[0].isIntersecting);
    }, { threshold: 0 });
    observer.observe(primary);
    var updateForViewport = function () {
      if (media.matches) sticky.classList.add('dm-sticky-visible');
    };
    window.addEventListener('scroll', updateForViewport, { passive: true });
    if (media.addEventListener) media.addEventListener('change', updateForViewport);
    else media.addListener(updateForViewport);
  }

  function fixGalleryHeight() {
    // The theme's slick gallery keeps a stale track height from init (~1.7x
    // the square hero image on phones), leaving a large blank band under the
    // photo. adaptiveHeight makes the track hug whichever slide is showing.
    if (!window.matchMedia('(max-width: 767px)').matches) return;
    var jq = window.jQuery;
    if (!jq || !jq.fn || !jq.fn.slick) return;
    // Two slick instances live in the gallery (main .productView-for and the
    // thumbnail nav) — apply to every initialized one; targeting only the
    // first silently fixes the wrong slider.
    var gallery = jq('.halo-productView[data-product-handle="' + PRODUCT_HANDLE + '"] .productView-images-wrapper .slick-initialized').not('[data-daisy-adaptive-height]');
    if (!gallery.length) return;
    try {
      gallery.slick('slickSetOption', 'adaptiveHeight', true, false);
      gallery.slick('setPosition');
      gallery.attr('data-daisy-adaptive-height', 'true');
    } catch (error) { /* slick unavailable or mid-teardown — leave the gallery alone */ }
  }

  function moveTrustBadgesNearCart() {
    var badges = qs(document, '.dm-trust-badges');
    if (!badges || badges.dataset.daisyStreetMoved) return;
    var proof = window.DAISY_PROOF || {};
    badges.className = 'dm-product-proof dm-product-proof--quote';
    badges.setAttribute('aria-label', 'Customer review');
    badges.innerHTML = [
      '<div class="dm-product-proof__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>',
      '<blockquote class="dm-product-proof__quote">' + escapeHtml(proof.quote || 'Rated 5 stars by verified customers') + '</blockquote>',
      '<p class="dm-product-proof__meta">' + escapeHtml(proof.meta || 'Verified customer') + '</p>'
    ].join('');
    var price = qs(document, '.productView-price');
    if (!price || !price.parentNode) return;
    price.parentNode.insertBefore(badges, price.nextSibling);
    badges.dataset.daisyStreetMoved = 'true';
    addProofBarNearCart();
  }

  function addProofBarNearCart() {
    var proof = window.DAISY_PROOF || {};
    if (!proof.line) return;
    var bar = qs(document, '.dm-product-quote--proof');
    if (!bar) {
      var subtotal = qs(document, '.dm-cyg__subtotal');
      if (!subtotal || !subtotal.parentNode) return;
      bar = document.createElement('aside');
      bar.className = 'dm-product-quote dm-product-quote--proof';
      bar.setAttribute('aria-label', 'Customer rating');
      subtotal.parentNode.insertBefore(bar, subtotal.nextSibling);
    }
    bar.innerHTML = '<div class="dm-product-quote__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="dm-product-quote__text">' + escapeHtml(proof.line) + '</p>';
    groupProofWithQuote(bar);
  }

  function groupProofWithQuote() {
    // On phones the configurator carries the whole sale (panel + add-ons +
    // live total), so the theme's title and static price below it are pure
    // duplication — the title repeats the panel header and the price never
    // reflects chosen extras. Those are hidden by CSS; here the customer
    // quote becomes a single trust card straight after the configurator,
    // with the "chosen by 1,600+" line folded into its meta row instead of
    // standing as a second star bar.
    if (!window.matchMedia('(max-width: 767px)').matches) return;
    var quote = qs(document, '.dm-product-proof--quote');
    var giftBlock = qs(document, '#dm-cyg');
    if (!quote || !giftBlock || !giftBlock.parentElement) return;
    if (giftBlock.nextElementSibling !== quote) {
      giftBlock.parentElement.insertBefore(quote, giftBlock.nextSibling);
    }
    var proof = window.DAISY_PROOF || {};
    if (proof.line && !quote.dataset.daisyProofMerged) {
      var meta = qs(quote, '.dm-product-proof__meta');
      if (meta) {
        meta.textContent = (proof.meta || 'Verified 5-star review') + ' · ' + proof.line;
        quote.dataset.daisyProofMerged = 'true';
      }
    }
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (char) {
      return {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }[char];
    });
  }

  function bind(form, panel, config) {
    if (document.body.dataset.daisyStreetSubmitBound) return;
    document.body.dataset.daisyStreetSubmitBound = 'true';
    document.addEventListener('click', function (event) {
      var submit = event.target.closest && event.target.closest('#product-add-to-cart,.dm-sticky-btn');
      if (submit) {
        stopNative(event);
        submitBundle(getForm() || form, qs(document, '[data-daisy-street-options]') || panel, config);
        return;
      }
      var modeButton = event.target.closest && event.target.closest('[data-dm-addon-mode]');
      if (modeButton) {
        stopNative(event);
        var modeCard = modeButton.closest('.dm-cyg__card');
        modeCard.dataset.addonMode = modeButton.dataset.dmAddonMode;
        updateInterface(getForm() || form, panel, config);
        return;
      }
      var heartComboButton = event.target.closest && event.target.closest('[data-heart-combo]');
      if (heartComboButton && !heartComboButton.disabled) {
        stopNative(event);
        var comboCard = heartComboButton.closest('.dm-cyg__card');
        if (comboCard) {
          var combo = heartComboButton.getAttribute('data-heart-combo');
          comboCard.dataset.addonMode = combo === 'none' ? 'none' : 'single';
          comboCard.dataset.heartBoxMode = combo === 'heartbox' ? 'add' : 'none';
        }
        updateInterface(getForm() || form, panel, config);
        return;
      }
      var heartWordingButton = event.target.closest && event.target.closest('[data-heart-wording-mode]');
      if (heartWordingButton && !heartWordingButton.disabled) {
        stopNative(event);
        var wordingCard = heartWordingButton.closest('.dm-cyg__card');
        if (wordingCard) {
          var nextMode = heartWordingButton.getAttribute('data-heart-wording-mode');
          var wasCustom = wordingCard.dataset.heartWording === 'custom';
          wordingCard.dataset.heartWording = nextMode;
          // Prefill only when ENTERING custom. Re-clicking the active button must
          // not resurrect a line the customer deliberately cleared.
          if (nextMode === 'custom' && !wasCustom) {
            var signOne = clean((qs(document, '[data-daisy-line-one]') || {}).value);
            var signTwo = clean((qs(document, '[data-daisy-line-two]') || {}).value);
            var leftInput = qs(wordingCard, '[data-heart-left]');
            var rightInput = qs(wordingCard, '[data-heart-right]');
            if (leftInput && !clean(leftInput.value)) leftInput.value = signTwo;
            if (rightInput && !clean(rightInput.value)) rightInput.value = signOne;
          }
        }
        updateInterface(getForm() || form, panel, config);
        return;
      }
      var heartConfigButton = event.target.closest && event.target.closest('[data-heart-config]');
      if (heartConfigButton && !heartConfigButton.disabled) {
        stopNative(event);
        var heartCard = heartConfigButton.closest('.dm-cyg__card');
        // Once they pick, their choice sticks and the inferred value stops applying.
        if (heartCard) heartCard.dataset.heartConfig = heartConfigButton.getAttribute('data-heart-config');
        updateInterface(getForm() || form, panel, config);
        return;
      }
    }, true);
    form.addEventListener('submit', function (event) {
      stopNative(event);
      submitBundle(form, panel, config);
    }, true);
    panel.addEventListener('input', function () { updateInterface(form, panel, config); });
    panel.addEventListener('change', function () { updateInterface(form, panel, config); });
    panel.addEventListener('focusin', function () { window.requestAnimationFrame(function () { updatePreviewCaret(panel); }); });
    panel.addEventListener('focusout', function () { window.requestAnimationFrame(function () { updatePreviewCaret(panel); }); });
    panel.addEventListener('keyup', function () { updatePreviewCaret(panel); });
    panel.addEventListener('click', function () { window.requestAnimationFrame(function () { updatePreviewCaret(panel); }); });
    panel.addEventListener('select', function () { updatePreviewCaret(panel); });
    panel.addEventListener('blur', function (event) {
      var field = event.target.closest && event.target.closest('[data-daisy-line-one],[data-daisy-line-two],[data-daisy-second-line-one],[data-daisy-second-line-two]');
      if (!field) return;
      field.value = signWording(field.value);
      updateInterface(form, panel, config);
    }, true);
    window.addEventListener('resize', function () { placePreview(panel); updateDirectEditors(panel); });
    qsa(document, '#dm-cyg-msg-text-one,#dm-cyg-msg-text-two,#dm-cyg-msg-text').forEach(function (message) {
      message.addEventListener('input', function () {
        var counter = qs(message.parentElement, '[data-dm-cyg-counter]') || qs(document, '#dm-cyg-count');
        if (counter) counter.textContent = String(200 - message.value.length);
        updateInterface(form, panel, config);
      });
    });
    window.addEventListener('pageshow', function () { setLoading(false); });
  }

  function init() {
    if (!isTargetProduct() || !model) return;
    var config = productData();
    var form = getForm();
    if (!config || !form) return;
    document.body.classList.add('daisy-street-sign-options-ready', 'daisy-mr-mrs-sign-ready');
    hideOldOptions();
    var panel = qs(document, '[data-daisy-street-options]') || createPanel(config);
    placePanel(form, panel);
    placePreview(panel);
    ensureSticky();
    bind(form, panel, config);
    bindStickyVisibility();
    updateInterface(form, panel, config);
    if (document.fonts && document.fonts.load) {
      document.fonts.load('400 100px "' + PREVIEW_FONT + '"').then(function () {
        updateInterface(getForm() || form, panel, config);
      });
    }
    moveTrustBadgesNearCart();
    fixGalleryHeight();
    groupProofWithQuote();
    [400, 1000, 2200].forEach(function (delay) {
      window.setTimeout(function () {
        hideOldOptions();
        placePanel(getForm() || form, panel);
        placePreview(panel);
        updateInterface(getForm() || form, panel, config);
        moveTrustBadgesNearCart();
        fixGalleryHeight();
        groupProofWithQuote();
      }, delay);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
