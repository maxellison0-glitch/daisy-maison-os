(function () {
  'use strict';

  var model = window.DaisyPebblePictureCartModel;
  var submitting = false;
  var handles = [
    'always-forever-personalised-pebble-artwork',
    'our-world-family-personalised-pebble-artwork',
    'to-the-moon-back-personalised-pebble-artwork',
    'wedding-flower-arch-personalised-pebble-picture',
    'wedding-church-personalised-pebble-picture',
    'beach-proposal-personalised-pebble-picture-gift',
    'graduation-personalised-pebble-picture',
    'beach-wedding-personalised-pebble-picture',
    'mum-flutterby-blossom-tree-personalised-pebble-picture',
    'family-flutterby-blossom-tree-personalised-pebble-picture-copy',
    'on-your-christening-personalised-pebble-picture',
    'engagement-proposal-love-tree-personalised-pebble-picture-copy',
    'always-my-sister-personalised-pebble-picture',
    'family-blossom-tree-personalised-pebble-picture-gift-2',
    'golden-skies-family-pebble-picture',
    'same-stars-family-pebble-picture',
    'together-family-pebble-picture',
    'grandparent-flutterby-blossom-tree-personalised-pebble-picture',
    'grandparent-personalised-pebble-sketch-picture',
    'family-swing-personalised-pebble-picture',
    'engagement-proposal-personalised-pebble-artwork',
    'new-home-personalised-pebble-picture',
    'mum-personalised-pebble-sketch-picture',
    'birthday-blossom-tree-personalised-pebble-picture',
    'a-little-bit-of-crazy-personalised-pebble-picture',
    'family-walk-in-the-park-personalised-pebble-picture',
    'everything-to-me-personalised-pebble-artwork',
    'wedding-swing-personalised-pebble-picture',
    'beside-you-personalised-pebble-artwork',
    'heart-strings-personalised-pebble-artwork',
    'true-friends-personalised-pebble-picture',
    'simple-moments-personalised-pebble-picture',
    'dad-grandad-simple-moments-personalised-pebble-picture',
    'mum-nanny-our-world-personalised-pebble-artwork',
    'home-sweet-home-personalised-pebble-picture',
    'couple-love-tree-personalised-pebble-picture-6-colour-options',
    'on-your-wedding-day-family-personalised-pebble-picture-gift',
    'mum-hands-hearts-personalised-pebble-picture'
  ];

  function qs(root, selector) { return (root || document).querySelector(selector); }
  function qsa(root, selector) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); }
  function clean(value) { return String(value || '').replace(/\s+/g, ' ').trim(); }
  function money(cents, currency) {
    return new Intl.NumberFormat(document.documentElement.lang || 'en-GB', { style: 'currency', currency: currency || 'GBP' }).format(cents / 100);
  }
  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, function (char) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char];
    });
  }
  function cygThumb(addon, alt) {
    if (!addon || !addon.thumb) return '';
    return '<img class="dm-cyg__thumb" src="' + escapeHtml(addon.thumb) + '" alt="' + escapeHtml(alt) + '" width="64" height="64" loading="lazy" data-dm-zoomable' + (addon.zoom ? ' data-dm-zoom-src="' + escapeHtml(addon.zoom) + '"' : '') + '>';
  }
  // ---- matching-heart upsell ----
  function heartCard() { return qs(document, '[data-heart-offer]'); }
  // Personalisation copied slot for slot from the picture. Read live rather than
  // cached on tick, so a late typo fix upstairs still reaches the heart.
  function heartInherited(root, config) {
    var out = {};
    var vals = state(root).values || {};
    ((config.heartOffer || {}).fields || []).forEach(function (field) {
      out[field.key] = clean(vals[field.source] || '');
    });
    return out;
  }
  function heartIsCustom(card) {
    return card.getAttribute('data-heart-wording') === 'custom';
  }
  function setHeartMode(card, mode) {
    card.setAttribute('data-heart-wording', mode);
    qsa(card, '[data-heart-mode]').forEach(function (btn) {
      var active = btn.getAttribute('data-heart-mode') === mode;
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }
  function heartValues(root, config, card) {
    var inherited = heartInherited(root, config);
    if (!heartIsCustom(card)) return inherited;
    var out = {};
    ((config.heartOffer || {}).fields || []).forEach(function (field) {
      var input = qs(card, '[data-heart-value="' + field.key.replace(/"/g, '\\"') + '"]');
      // No fallback to the picture here on purpose: in custom mode the customer's
      // box is authoritative, so clearing a line must actually remove it. The
      // prefill on switching to custom already saves them retyping.
      out[field.key] = clean(input ? input.value : '');
    });
    return out;
  }
  function renderHeartOffer(config) {
    var heart = config.heartOffer;
    if (!heart) return '';
    var price = money(heart.price, config.currency);
    // Reuses the none/single/double segmented control: 'double' here means
    // heart + gift box, so data-pair-price carries the combined price and the
    // shared addonTotalCents() maths needs no special case.
    var withBox = heart.box ? heart.price + heart.box.price : heart.price;
    return [
      '<div class="dm-cyg__card dm-cyg__card--heart" data-variant="' + heart.variantId + '" data-price="' + heart.price + '" data-pair-price="' + withBox + '" data-name="' + escapeHtml(heart.name) + '" data-addon-mode="none" data-heart-wording="same" data-heart-offer>',
      '<div class="dm-cyg__inner">',
      '<div class="dm-cyg__media">',
      heart.thumb ? '<img class="dm-cyg__thumb dm-cyg__thumb--heart" src="' + escapeHtml(heart.thumb) + '" alt="' + escapeHtml(heart.name) + '" width="120" height="120" loading="lazy" data-dm-zoomable' + (heart.zoom ? ' data-dm-zoom-src="' + escapeHtml(heart.zoom) + '"' : '') + '>' : '',
      '<div class="dm-cyg__body">',
      '<div class="dm-cyg__top"><span class="dm-cyg__name">Add matching heart</span><span class="dm-cyg__price">' + price + '</span></div>',
      '<p class="dm-cyg__note">Personalised to match your picture — add the matching gift box too.</p>',
      '</div></div>',
      '<div class="dm-addon-mode">',
      '<button class="dm-addon-mode__option is-active" type="button" data-dm-addon-mode="none" aria-pressed="true">No thanks</button>',
      '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="single" aria-pressed="false">Add heart \xb7 ' + price + '</button>',
      heart.box ? '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="double" aria-pressed="false">Heart + gift box \xb7 ' + money(withBox, config.currency) + '</button>' : '',
      '</div>',
      '<div class="dm-heart-offer" data-heart-personalise hidden aria-hidden="true">',
      '<p class="dm-heart-offer__label">Wording on the heart</p>',
      '<div class="dm-addon-mode dm-heart-offer__modes">',
      '<button class="dm-addon-mode__option is-active" type="button" data-heart-mode="same" aria-pressed="true">Same as my picture</button>',
      '<button class="dm-addon-mode__option" type="button" data-heart-mode="custom" aria-pressed="false">Personalise separately</button>',
      '</div>',
      '<p class="dm-heart-offer__preview" data-heart-preview></p>',
      '<div class="dm-heart-offer__fields" data-heart-fields hidden>',
      (heart.fields || []).map(function (field) {
        return '<label class="dm-heart-offer__field"><span>' + escapeHtml(field.label) + '</span>' +
          '<input type="text" data-heart-value="' + escapeHtml(field.key) + '" data-heart-source="' + escapeHtml(field.source) + '"' + (field.required ? ' data-heart-required="1"' : '') + '></label>';
      }).join(''),
      '</div></div>',
      '</div></div>'
    ].join('');
  }
  function currentHandle() {
    var match = window.location.pathname.match(/\/products\/([^/?#]+)/);
    return match ? match[1] : '';
  }
  function getForm() {
    return qs(document, 'product-form form[data-type="add-to-cart-form"]') || qs(document, 'form[action*="/cart/add"]');
  }
  function readConfig(root) {
    try { return JSON.parse(qs(root, '[data-daisy-pebble-picture-config]').textContent); } catch (error) { return null; }
  }
  function choiceOptions(values, selected) {
    return ['<option value="">Please select</option>'].concat((values || []).map(function (value) {
      return '<option value="' + escapeHtml(value) + '"' + (value === selected ? ' selected' : '') + '>' + escapeHtml(value) + '</option>';
    })).join('');
  }
  function renderField(field, offer) {
    var dataAttr = offer ? 'data-pebble-offer-value' : 'data-pebble-value';
    var required = field.required ? ' data-required="true"' : '';
    var placeholder = field.placeholder ? ' placeholder="' + escapeHtml(field.placeholder) + '"' : '';
    if (field.type === 'toggletext') {
      var defaultVal = escapeHtml(field.default || '');
      var radioName = (offer ? 'offer' : 'main') + '-wording-' + (field.source || field.key).replace(/\W+/g, '-').toLowerCase();
      var rs = ' style="position:absolute;opacity:0;width:0;height:0;pointer-events:none"';
      return [
        '<div class="dm-pebble-picture__field--wording">',
        '<div class="dm-pebble-picture__wording-choices">',
        '<label class="dm-pebble-picture__wording-choice dm-pebble-picture__wording-choice--selected">',
        '<input type="radio" name="' + radioName + '" value="no" checked' + rs + '>',
        '<span class="dm-pebble-picture__wording-choice-title">Keep wording</span>',
        '<span class="dm-pebble-picture__wording-choice-note">&ldquo;' + defaultVal + '&rdquo;</span>',
        '</label>',
        '<label class="dm-pebble-picture__wording-choice">',
        '<input type="radio" name="' + radioName + '" value="yes"' + rs + '>',
        '<span class="dm-pebble-picture__wording-choice-title">I\'ll write my own wording</span>',
        '</label>',
        '</div>',
        '<div data-pebble-wording-wrap hidden>',
        '<label class="dm-pebble-picture__field">',
        '<span class="dm-pebble-picture__label">Your wording</span>',
        '<input type="text" ' + dataAttr + '="' + escapeHtml(field.source || field.key) + '"' + placeholder + ' value="' + defaultVal + '" data-toggle-default="' + defaultVal + '" autocomplete="off">',
        '</label>',
        '</div>',
        '</div>'
      ].join('');
    }
    if (field.type === 'wordingpair') {
      var keepVal = (field.keepPrefix || 'NO KEEP ') + (field.default || '');
      var yesVal = field.yesValue || "Yes I'll add my own words";
      var wpRadioName = (offer ? 'offer' : 'main') + '-wording-pair-' + field.key.replace(/\W+/g, '-').toLowerCase();
      var rs2 = ' style="position:absolute;opacity:0;width:0;height:0;pointer-events:none"';
      return [
        '<div class="dm-pebble-picture__field--wording">',
        '<div class="dm-pebble-picture__wording-choices">',
        '<label class="dm-pebble-picture__wording-choice dm-pebble-picture__wording-choice--selected">',
        '<input type="radio" name="' + wpRadioName + '" value="no" checked' + rs2 + '>',
        '<span class="dm-pebble-picture__wording-choice-title">Keep wording</span>',
        '<span class="dm-pebble-picture__wording-choice-note">&ldquo;' + escapeHtml(field.default || '') + '&rdquo;</span>',
        '</label>',
        '<label class="dm-pebble-picture__wording-choice">',
        '<input type="radio" name="' + wpRadioName + '" value="yes"' + rs2 + '>',
        '<span class="dm-pebble-picture__wording-choice-title">I\'ll write my own wording</span>',
        '</label>',
        '</div>',
        '<input type="hidden" ' + dataAttr + '="' + escapeHtml(field.key) + '" value="' + escapeHtml(keepVal) + '" data-wordingpair-keep="' + escapeHtml(keepVal) + '" data-wordingpair-yes="' + escapeHtml(yesVal) + '">',
        '<div data-pebble-wording-wrap hidden>',
        '<label class="dm-pebble-picture__field">',
        '<span class="dm-pebble-picture__label">Your wording</span>',
        '<input type="text" ' + dataAttr + '="' + escapeHtml(field.wordingKey || (offer ? '(Offer) Wording' : 'Wording')) + '"' + placeholder + ' autocomplete="off">',
        '</label>',
        '</div>',
        '</div>'
      ].join('');
    }
    var label = [
      '<label class="dm-pebble-picture__field">',
      '<span class="dm-pebble-picture__label">' + escapeHtml(field.label || field.key) + (field.required ? ' *' : '') + '</span>'
    ];
    if (field.type === 'select') {
      label.push('<select ' + dataAttr + '="' + escapeHtml(field.source || field.key) + '"' + required + '>' + choiceOptions(field.values) + '</select>');
    } else {
      label.push('<input type="text" ' + dataAttr + '="' + escapeHtml(field.source || field.key) + '"' + required + placeholder + '>');
    }
    label.push('</label>');
    return label.join('');
  }
  function renderVariablePeople(config, offer) {
    var people = config.people || {};
    var prefix = offer ? 'data-pebble-offer' : 'data-pebble-main';
    if (people.mode === 'variable') {
      // The extra-people charge is one flat add-on (config.extraPeople) once the
      // count passes the threshold; say so on the options and under the select.
      var extra = config.extraPeople;
      var maxCount = people.max || 8;
      var threshold = extra ? (parseInt(extra.threshold, 10) || 6) : maxCount;
      var extraPrice = extra ? money(extra.price, config.currency).replace(/\.00$/, '') : '';
      var html = [
        '<div class="dm-pebble-picture__people" ' + prefix + '-people>',
        '<label class="dm-pebble-picture__field">',
        '<span class="dm-pebble-picture__label">Number of pebble characters</span>',
        '<select ' + prefix + '-count>'
      ];
      for (var count = people.min || 1; count <= maxCount; count += 1) {
        html.push('<option value="' + count + '">' + count + ' (Inc dog/cat)' + (extra && count > threshold ? ' +' + extraPrice : '') + '</option>');
      }
      html.push('</select>');
      if (extra && maxCount > threshold) {
        var extraRange = threshold + 1 === maxCount ? String(maxCount) : (threshold + 1) + ' or ' + maxCount;
        html.push('<span class="dm-pebble-picture__extra-note">Up to ' + threshold + ' pebble characters included. Choose ' + extraRange + ' for <span style="white-space:nowrap">+' + extraPrice + '</span>.</span>');
      }
      html.push('</label>');
      for (var index = 1; index <= (people.max || 8); index += 1) {
        html.push('<div class="dm-pebble-picture__person-row" data-pebble-person="' + index + '">');
        html.push(
          '<label class="dm-pebble-picture__field">',
          '<span class="dm-pebble-picture__label">Pebble ' + index + '</span>',
          '<select ' + prefix + '-pebble="' + index + '" data-required="true">',
          choiceOptions(['Adult', 'Teen', 'Child', 'Baby', 'Dog', 'Cat']),
          '</select>',
          '</label>'
        );
        if (people.names) {
          html.push(
            '<label class="dm-pebble-picture__field">',
            '<span class="dm-pebble-picture__label">Name</span>',
            '<input type="text" ' + prefix + '-name="' + index + '" placeholder="Optional" autocomplete="off">',
            '</label>'
          );
        }
        html.push('</div>');
      }
      html.push('</div>');
      return html.join('');
    }
    if (people.mode === 'weddingfamily') {
      var fixedCount = parseInt(people.fixedCount, 10) || 2;
      var extraOptions = people.extraOptions || ['Teen', 'Child', 'Baby', 'Dog', 'Cat'];
      var maxVariable = (people.max || 6) - fixedCount;
      var wfHtml = [
        '<div class="dm-pebble-picture__people" ' + prefix + '-people>',
        '<label class="dm-pebble-picture__field">',
        '<span class="dm-pebble-picture__label">Number of pebble characters</span>',
        '<select ' + prefix + '-count>'
      ];
      for (var wfCount = people.min || 3; wfCount <= (people.max || 6); wfCount += 1) {
        wfHtml.push('<option value="' + wfCount + '">' + wfCount + '</option>');
      }
      wfHtml.push('</select></label>');
      for (var vi = 1; vi <= maxVariable; vi += 1) {
        wfHtml.push('<div class="dm-pebble-picture__person-row" data-pebble-person="' + vi + '">');
        wfHtml.push(
          '<label class="dm-pebble-picture__field">',
          '<span class="dm-pebble-picture__label">Pebble ' + (fixedCount + vi) + '</span>',
          '<select ' + prefix + '-pebble="' + vi + '" data-required="true">',
          choiceOptions(extraOptions),
          '</select>',
          '</label>'
        );
        if (people.names) {
          wfHtml.push(
            '<label class="dm-pebble-picture__field">',
            '<span class="dm-pebble-picture__label">Name</span>',
            '<input type="text" ' + prefix + '-name="' + vi + '" placeholder="Optional" autocomplete="off">',
            '</label>'
          );
        }
        wfHtml.push('</div>');
      }
      wfHtml.push('</div>');
      return wfHtml.join('');
    }
    return '';
  }
  function render(root, config) {
    var mainSelect = (config.fields || []).filter(function (f) { return f.type === 'select'; });
    var mainToggle = (config.fields || []).filter(function (f) { return f.type === 'toggletext' || f.type === 'wordingpair'; });
    var mainText = (config.fields || []).filter(function (f) { return f.type === 'text'; });
    var offerSelect = (config.offerFields || []).filter(function (f) { return f.type === 'select'; });
    var offerToggle = (config.offerFields || []).filter(function (f) { return f.type === 'toggletext' || f.type === 'wordingpair'; });
    var offerText = (config.offerFields || []).filter(function (f) { return f.type === 'text'; });
    root.innerHTML = qs(root, '[data-daisy-pebble-picture-config]').outerHTML + [
      '<p class="dm-pebble-picture__eyebrow">' + escapeHtml(config.eyebrow) + '</p>',
      '<h2 class="dm-pebble-picture__title">' + escapeHtml(config.heading) + '</h2>',
      '<p class="dm-pebble-picture__copy">' + escapeHtml(config.copy) + '</p>',
      '<div class="dm-pebble-picture__layout">',
      '<div class="dm-pebble-picture__panel">',
      '<div class="dm-pebble-picture__group"><h3 class="dm-pebble-picture__group-title">Personalisation</h3>',
      '<div class="dm-pebble-picture__grid">' + mainSelect.map(function (field) { return renderField(field, false); }).join('') + '</div>',
      renderVariablePeople(config, false),
      mainToggle.map(function (field) { return renderField(field, false); }).join(''),
      mainText.length ? '<div class="dm-pebble-picture__grid">' + mainText.map(function (field) { return renderField(field, false); }).join('') + '</div>' : '',
      '</div>',
      '<div class="dm-pebble-picture__group"><h3 class="dm-pebble-picture__group-title">Incredible offer</h3>',
      '<label class="dm-pebble-picture__offer"><input type="checkbox" data-pebble-second-frame><div class="dm-pebble-picture__offer-inner"><div class="dm-pebble-picture__offer-header"><strong>' + escapeHtml(config.secondOffer.label) + '</strong><em>' + escapeHtml(config.secondOffer.priceLabel) + '</em></div><small>' + escapeHtml(config.secondOffer.note) + '</small></div></label>',
      '<div class="dm-pebble-picture__second" data-pebble-second-wrap hidden aria-hidden="true">',
      '<h3 class="dm-pebble-picture__group-title">Second frame</h3>',
      '<div class="dm-pebble-picture__grid">' + offerSelect.map(function (field) { return renderField(field, true); }).join('') + '</div>',
      renderVariablePeople(config, true),
      offerToggle.map(function (field) { return renderField(field, true); }).join(''),
      offerText.length ? '<div class="dm-pebble-picture__grid">' + offerText.map(function (field) { return renderField(field, true); }).join('') + '</div>' : '',
      '</div></div>',
      (config.giftWrap || config.luckySixpence || config.easel || config.spray || config.heartOffer) ? [
        '<div class="dm-pebble-picture__group"><h3 class="dm-pebble-picture__group-title">Add-ons</h3>',
        renderHeartOffer(config),
        config.easel ? [
          '<div class="dm-cyg__card" data-variant="' + config.easel.variantId + '" data-pair-variant="' + config.easel.variantId + '" data-price="' + config.easel.price + '" data-pair-price="' + (config.easel.price * 2) + '" data-name="Wooden Display Easel" data-addon-mode="none">',
          '<div class="dm-cyg__inner">',
          '<div class="dm-cyg__media">',
          cygThumb(config.easel, 'Wooden display easel'),
          '<div class="dm-cyg__body">',
          '<div class="dm-cyg__top"><span class="dm-cyg__name">Wooden Display Easel</span><span class="dm-cyg__price">' + money(config.easel.price, config.currency) + '</span></div>',
          '<p class="dm-cyg__note">Display it on a shelf or mantelpiece the moment it\'s unwrapped.</p>',
          '</div></div>',
          '<div class="dm-addon-mode">',
          '<button class="dm-addon-mode__option is-active" type="button" data-dm-addon-mode="none" aria-pressed="true">No thanks</button>',
          '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="single" aria-pressed="false">Add an easel \xb7 ' + money(config.easel.price, config.currency) + '</button>',
          '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="double" aria-pressed="false" disabled hidden>One each \xb7 ' + money(config.easel.price * 2, config.currency) + '</button>',
          '</div></div></div>'
        ].join('') : '',
        config.spray ? [
          '<div class="dm-cyg__card" data-variant="' + config.spray.variantId + '" data-price="' + config.spray.price + '" data-name="Picture Cleaning Spray" data-addon-mode="none">',
          '<div class="dm-cyg__inner">',
          '<div class="dm-cyg__media">',
          cygThumb(config.spray, 'Picture cleaning spray'),
          '<div class="dm-cyg__body">',
          '<div class="dm-cyg__top"><span class="dm-cyg__name">Picture Cleaning Spray</span><span class="dm-cyg__price">' + money(config.spray.price, config.currency) + '</span></div>',
          '<p class="dm-cyg__note">Keep the glass smudge-free — microfibre cloth included.</p>',
          '</div></div>',
          '<div class="dm-addon-mode">',
          '<button class="dm-addon-mode__option is-active" type="button" data-dm-addon-mode="none" aria-pressed="true">No thanks</button>',
          '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="single" aria-pressed="false">Add cleaning spray \xb7 ' + money(config.spray.price, config.currency) + '</button>',
          '</div></div></div>'
        ].join('') : '',
        config.giftWrap ? [
          '<div class="dm-cyg__card" data-variant="' + config.giftWrap.variantId + '" data-pair-variant="' + config.giftWrap.variantId + '" data-price="' + config.giftWrap.price + '" data-pair-price="' + (config.giftWrap.price * 2) + '" data-name="Gift Wrap Kit" data-addon-mode="none">',
          '<div class="dm-cyg__inner">',
          '<div class="dm-cyg__media">',
          cygThumb(config.giftWrap, 'Gift wrap kit'),
          '<div class="dm-cyg__body">',
          '<div class="dm-cyg__top"><span class="dm-cyg__name">Gift Wrap Kit</span><span class="dm-cyg__price">' + money(config.giftWrap.price, config.currency) + '</span></div>',
          '</div></div>',
          '<div class="dm-addon-mode">',
          '<button class="dm-addon-mode__option is-active" type="button" data-dm-addon-mode="none" aria-pressed="true">No thanks</button>',
          '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="single" aria-pressed="false">Add gift wrap \xb7 ' + money(config.giftWrap.price, config.currency) + '</button>',
          '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="double" aria-pressed="false" disabled hidden>Two wraps \xb7 ' + money(config.giftWrap.price * 2, config.currency) + '</button>',
          '</div></div></div>'
        ].join('') : '',
        config.luckySixpence ? [
          '<div class="dm-cyg__card" data-variant="' + config.luckySixpence.variantId + '" data-price="' + config.luckySixpence.price + '" data-name="' + escapeHtml(config.luckySixpence.name || 'Lucky Sixpence') + '" data-addon-mode="none">',
          '<div class="dm-cyg__inner">',
          '<div class="dm-cyg__media">',
          cygThumb(config.luckySixpence, config.luckySixpence.name || 'Lucky Sixpence'),
          '<div class="dm-cyg__body">',
          '<div class="dm-cyg__top"><span class="dm-cyg__name">' + escapeHtml(config.luckySixpence.name || 'Lucky Sixpence') + '</span><span class="dm-cyg__price">' + money(config.luckySixpence.price, config.currency) + '</span></div>',
          config.luckySixpence.note ? '<p class="dm-cyg__note">' + escapeHtml(config.luckySixpence.note) + '</p>' : '',
          '</div></div>',
          '<div class="dm-addon-mode">',
          '<button class="dm-addon-mode__option is-active" type="button" data-dm-addon-mode="none" aria-pressed="true">No thanks</button>',
          '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="single" aria-pressed="false">Add lucky sixpence \xb7 ' + money(config.luckySixpence.price, config.currency) + '</button>',
          '</div></div></div>'
        ].join('') : '',
        '</div>'
      ].join('') : '',
      '<p class="dm-pebble-picture__error" data-pebble-error role="alert"></p>',
      '<p class="dm-pebble-picture__total">Total <strong data-pebble-total>' + money(config.prices.base, config.currency) + '</strong></p>',
      '</div>',
      '</div>'
    ].join('');
  }
  function values(root, selector) {
    var out = {};
    qsa(root, selector).forEach(function (field) {
      out[field.getAttribute(selector.indexOf('offer') !== -1 ? 'data-pebble-offer-value' : 'data-pebble-value')] = clean(field.value);
    });
    return out;
  }
  function pebbles(root, offer) {
    var attr = offer ? '[data-pebble-offer-pebble]' : '[data-pebble-main-pebble]';
    return qsa(root, attr).map(function (field) { return field.value; });
  }
  function names(root, offer) {
    var attr = offer ? '[data-pebble-offer-name]' : '[data-pebble-main-name]';
    return qsa(root, attr).map(function (field) { return field.value; });
  }
  function state(root) {
    return {
      values: values(root, '[data-pebble-value]'),
      peopleCount: parseInt((qs(root, '[data-pebble-main-count]') || {}).value, 10) || 1,
      pebbles: pebbles(root, false),
      names: names(root, false),
      secondFrame: !window.DaisyCleanProduct && !!(qs(root, '[data-pebble-second-frame]') || {}).checked,
      offerValues: values(root, '[data-pebble-offer-value]'),
      offerPeopleCount: parseInt((qs(root, '[data-pebble-offer-count]') || {}).value, 10) || 1,
      offerPebbles: pebbles(root, true),
      offerNames: names(root, true)
    };
  }
  function updatePeople(root, offer, fixedCount) {
    var countNode = qs(root, offer ? '[data-pebble-offer-count]' : '[data-pebble-main-count]');
    if (!countNode) return;
    var count = parseInt(countNode.value, 10) || 1;
    var varCount = count - (fixedCount || 0);
    var attr = offer ? '[data-pebble-offer-people]' : '[data-pebble-main-people]';
    qsa(qs(root, attr), '[data-pebble-person]').forEach(function (row, index) {
      var visible = index < varCount;
      row.hidden = !visible;
      qsa(row, 'select,input').forEach(function (field) { field.disabled = !visible; });
    });
  }
  function syncSubtotal(total, currency) {
    qsa(document, '.money-subtotal').forEach(function (node) {
      node.textContent = money(total.current, currency);
    });
  }
  function updateHeartOffer(root, config) {
    var card = heartCard();
    if (!card || !config.heartOffer) return;
    var on = addonMode(card) !== 'none';
    var panel = qs(card, '[data-heart-personalise]');
    if (panel) {
      panel.hidden = !on;
      panel.setAttribute('aria-hidden', on ? 'false' : 'true');
      qsa(panel, 'input').forEach(function (field) { field.disabled = !on; });
    }
    var custom = heartIsCustom(card);
    var fields = qs(card, '[data-heart-fields]');
    if (fields) {
      fields.hidden = !custom;
      qsa(fields, 'input').forEach(function (field) { field.disabled = !on || !custom; });
    }
    var preview = qs(card, '[data-heart-preview]');
    if (preview) {
      var inherited = heartInherited(root, config);
      var parts = ((config.heartOffer || {}).fields || []).map(function (field) {
        return inherited[field.key];
      }).filter(Boolean);
      preview.textContent = parts.length ? parts.join(' \xb7 ') : 'Fill in your picture above and it copies across.';
      preview.hidden = custom;
    }
  }
  function update(root, config) {
    var current = state(root);
    root.dataset.secondFrame = current.secondFrame ? 'true' : 'false';
    root.dataset.peopleCount = String(current.peopleCount || 2);
    var second = qs(root, '[data-pebble-second-wrap]');
    second.hidden = !current.secondFrame;
    second.setAttribute('aria-hidden', current.secondFrame ? 'false' : 'true');
    qsa(second, 'input,select').forEach(function (field) { field.disabled = !current.secondFrame; });
    var wfFixed = (config.people || {}).mode === 'weddingfamily' ? (parseInt((config.people || {}).fixedCount, 10) || 2) : 0;
    updatePeople(root, false, wfFixed);
    updatePeople(root, true, wfFixed);
    var total = model.calculateTotal(current, config);
    var gwCard = qs(document, '.dm-cyg__card[data-name="Gift Wrap Kit"]');
    if (gwCard && config.giftWrap) {
      var doubleBtn = qs(gwCard, '[data-dm-addon-mode="double"]');
      var gwMode = addonMode(gwCard);
      if (current.secondFrame) {
        if (doubleBtn) { doubleBtn.hidden = false; doubleBtn.disabled = false; }
      } else {
        if (doubleBtn) { doubleBtn.hidden = true; doubleBtn.disabled = true; }
        if (gwMode === 'double') { setAddonMode(gwCard, 'single'); }
      }
    }
    var easelCard = qs(document, '.dm-cyg__card[data-name="Wooden Display Easel"]');
    if (easelCard && config.easel) {
      var easelDoubleBtn = qs(easelCard, '[data-dm-addon-mode="double"]');
      var easelMode = addonMode(easelCard);
      if (current.secondFrame) {
        if (easelDoubleBtn) { easelDoubleBtn.hidden = false; easelDoubleBtn.disabled = false; }
      } else {
        if (easelDoubleBtn) { easelDoubleBtn.hidden = true; easelDoubleBtn.disabled = true; }
        if (easelMode === 'double') { setAddonMode(easelCard, 'single'); }
      }
    }
    updateHeartOffer(root, config);
    var grandTotal = total.current + addonTotalCents();
    qs(root, '[data-pebble-total]').textContent = money(grandTotal, config.currency);
    syncSubtotal({ current: grandTotal }, config.currency);
    syncCygTotal(total.current, config.currency);
    qsa(root, '.dm-pebble-picture__wording-choice').forEach(function (card) {
      var inp = qs(card, 'input[type="radio"]');
      card.classList.toggle('dm-pebble-picture__wording-choice--selected', !!(inp && inp.checked));
    });
    qsa(root, '[data-pebble-wording-wrap]').forEach(function (wrap) {
      var wordingField = wrap.closest('.dm-pebble-picture__field--wording');
      if (!wordingField) return;
      var radio = qs(wordingField, 'input[type="radio"]');
      if (!radio) return;
      var checkedRadio = qs(wordingField, '[name="' + radio.name + '"]:checked');
      var isCustom = !!(checkedRadio && checkedRadio.value === 'yes');
      wrap.hidden = !isCustom;
      var textInput = qs(wrap, 'input[type="text"]');
      if (textInput) {
        textInput.disabled = !isCustom;
        if (!isCustom) {
          textInput.value = textInput.getAttribute('data-toggle-default') || '';
        } else if (textInput.value === (textInput.getAttribute('data-toggle-default') || '')) {
          textInput.value = '';
        }
      }
    });
    // Sync wordingpair hidden Change Text? inputs
    qsa(root, '[data-wordingpair-keep]').forEach(function (hiddenInput) {
      var wrapper = hiddenInput.closest('.dm-pebble-picture__field--wording');
      if (!wrapper) return;
      var radio = qs(wrapper, 'input[type="radio"]');
      if (!radio) return;
      var checkedRadio = qs(wrapper, '[name="' + radio.name + '"]:checked');
      var isCustom = !!(checkedRadio && checkedRadio.value === 'yes');
      hiddenInput.value = isCustom
        ? hiddenInput.getAttribute('data-wordingpair-yes')
        : hiddenInput.getAttribute('data-wordingpair-keep');
    });
    var previewLine = qs(root, '[data-preview-line]');
    if (previewLine) previewLine.textContent = current.values['Line 1'] || current.values.Names || '';
  }
  function validate(root, config) {
    var missing = model.validate(state(root), config);
    if (missing.length) return 'Please complete: ' + missing[0] + '.';
    return '';
  }
  function globoTarget() {
    var node = qs(document, '.gpo-product-variants') ||
      qs(document, '.gpo-container') ||
      qs(document, '.gpo-app') ||
      qs(document, '.gpo-options') ||
      qs(document, '.globo-product-options') ||
      qs(document, '.globo-options') ||
      qs(document, '[data-gpo]') ||
      qs(document, '[data-globo]');
    return node && (node.closest('.shopify-app-block') || node);
  }
  function mountBuilder(root, form) {
    var target = globoTarget();
    if (target && target.parentNode && !target.contains(form) && !form.contains(target)) {
      target.parentNode.insertBefore(root, target);
    } else if (form.parentNode) {
      form.parentNode.insertBefore(root, form);
    }
    root.hidden = false;
    root.removeAttribute('hidden');
  }
  function hideGlobo(form, root) {
    qsa(document, '.gpo-product-variants,.gpo-container,.gpo-app,.gpo-options,.globo-product-options,.globo-options,[data-gpo],[data-globo]').forEach(function (node) {
      var target = node.closest('.shopify-app-block') || node;
      if (target.contains(form) || form.contains(target) || target.contains(root) || root.contains(target)) return;
      target.hidden = true;
      target.style.display = 'none';
      qsa(target, 'input,select,textarea,button').forEach(function (field) { field.disabled = true; });
    });
  }
  function submit(root, config) {
    if (submitting) return;
    var error = validate(root, config);
    var message = qs(root, '[data-pebble-error]');
    if (error) { message.textContent = error; return; }
    message.textContent = '';
    submitting = true;
    var button = qs(document, '#product-add-to-cart') || qs(document, 'button[name="add"]');
    var original = button && button.textContent;
    if (button) { button.disabled = true; button.textContent = 'Adding...'; }
    var bundleId = 'pebble-picture-' + Date.now();
    var cur = state(root);
    var cartItems = model.buildCartItems(cur, config, bundleId).map(function (item) {
      return { id: item.id, quantity: item.quantity, properties: item.properties };
    }).concat(addonCartItems(bundleId, root, config));
    fetch('/cart/add.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({ items: cartItems })
    }).then(function (response) {
      if (!response.ok) throw new Error('Unable to add your pebble picture to basket.');
      return response.json();
    }).then(function () {
      if (button) button.classList.add('dm-celebrate');
      qsa(document, '#product-add-to-cart,.product-form__submit,.dm-sticky-btn').forEach(function(b){ b.classList.add('dm-celebrate'); });
      var go = function(){ window.location.href = window.routes && window.routes.cart || '/cart'; };
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (reduce) { go(); } else { setTimeout(go, 800); }
    }).catch(function (err) {
      submitting = false;
      if (button) { button.disabled = false; button.textContent = original; }
      message.textContent = err.message || 'Something went wrong adding this to basket.';
    });
  }
  // ---- dm-cyg addon cards (gift wrap, lucky sixpence) ----
  function addonMode(card) {
    return card.getAttribute('data-addon-mode') || 'none';
  }

  function setAddonMode(card, mode) {
    card.setAttribute('data-addon-mode', mode);
    qsa(card, '[data-dm-addon-mode]').forEach(function (btn) {
      var active = btn.getAttribute('data-dm-addon-mode') === mode;
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  function addonCartItems(bundleId, root, config) {
    var items = [];
    qsa(document, '.dm-cyg__card').forEach(function (card) {
      var mode = addonMode(card);
      if (mode === 'none') return;
      var variantId = parseInt(card.getAttribute('data-variant'), 10);
      if (!variantId) return;
      // The heart carries personalisation and drags its free gift box along, so
      // it can't use the plain add-on path below.
      if (card.hasAttribute('data-heart-offer')) {
        var heart = (config || {}).heartOffer;
        if (!heart) return;
        var props = { '_Bundle ID': bundleId, 'Add-on': card.getAttribute('data-name') || 'Matching Heart' };
        if (heart.sizeKey) props[heart.sizeKey] = heart.sizeValue;
        var chosen = heartValues(root, config, card);
        Object.keys(chosen).forEach(function (key) { if (chosen[key]) props[key] = chosen[key]; });
        items.push({ id: variantId, quantity: 1, properties: props });
        // 'double' on this card means they also took the gift box — a real
        // product at its real price, so it gets its own line as boxes always have.
        if (mode === 'double' && heart.box) {
          items.push({
            id: heart.box.variantId,
            quantity: 1,
            properties: { '_Bundle ID': bundleId, 'Add-on': heart.box.name || 'Gift Box' }
          });
        }
        return;
      }
      var isDouble = mode === 'double';
      var qty = isDouble && card.getAttribute('data-pair-variant') === card.getAttribute('data-variant') ? 2 : 1;
      items.push({
        id: variantId,
        quantity: qty,
        properties: { '_Bundle ID': bundleId, 'Add-on': card.getAttribute('data-name') || 'Add-on' }
      });
    });
    return items;
  }

  function addonTotalCents() {
    return qsa(document, '.dm-cyg__card').reduce(function (sum, card) {
      var mode = addonMode(card);
      if (mode === 'none') return sum;
      if (mode === 'double') return sum + parseInt(card.getAttribute('data-pair-price'), 10);
      return sum + parseInt(card.getAttribute('data-price'), 10);
    }, 0);
  }

  function syncCygTotal(builderCents, currency) {
    var total = qs(document, '#dm-cyg-total');
    if (total) total.textContent = money(builderCents + addonTotalCents(), currency);
  }


  function initAddons(root, config) {
    document.addEventListener('click', function (event) {
      var btn = event.target.closest('[data-dm-addon-mode]');
      if (!btn) return;
      var card = btn.closest('.dm-cyg__card');
      if (!card) return;
      event.preventDefault();
      setAddonMode(card, btn.getAttribute('data-dm-addon-mode'));
      update(root, config);
    });
    document.addEventListener('click', function (event) {
      var modeBtn = event.target.closest('[data-heart-mode]');
      if (!modeBtn) return;
      var card = heartCard();
      if (!card) return;
      event.preventDefault();
      var wasCustom = heartIsCustom(card);
      var mode = modeBtn.getAttribute('data-heart-mode');
      setHeartMode(card, mode);
      // Prefill only when ENTERING custom mode. Re-clicking the already-active
      // button must not resurrect a line the customer deliberately cleared —
      // unlike a radio, a button fires on every click.
      if (mode === 'custom' && !wasCustom) {
        var inherited = heartInherited(root, config);
        qsa(card, '[data-heart-value]').forEach(function (input) {
          if (!clean(input.value)) input.value = inherited[input.getAttribute('data-heart-value')] || '';
        });
      }
      update(root, config);
    });
  }

  function renderProof(form) {
    var proof = window.DAISY_PROOF || {};
    var pills = qs(document, '.dm-trust-badges');
    if (!proof.quote && !pills) return;
    if (proof.quote && !qs(document, '.dm-product-proof--quote')) {
      // Repurpose the theme's pill trust-badges element when present so the
      // pills never render; otherwise build the proof box fresh.
      var box = pills || document.createElement('aside');
      box.className = 'dm-product-proof dm-product-proof--quote';
      box.setAttribute('aria-label', 'Customer review');
      box.innerHTML =
        '<div class="dm-product-proof__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>' +
        '<blockquote class="dm-product-proof__quote">' + proof.quote + '</blockquote>' +
        '<p class="dm-product-proof__meta">' + (proof.meta || 'Verified customer') + '</p>';
      var price = qs(document, '.productView-price');
      if (price && price.parentNode) price.parentNode.insertBefore(box, price.nextSibling);
    } else if (!proof.quote && pills) {
      // No personal review yet — pills go away; aggregate shows once, in the bar
      pills.setAttribute('aria-hidden', 'true');
      pills.style.setProperty('display', 'none', 'important');
    }
    if (!qs(document, '.dm-product-quote--proof')) {
      var atcBtn = qs(document, '#product-add-to-cart') || qs(form, 'button[name="add"]');
      var target = atcBtn && (atcBtn.closest('.productView-group') || atcBtn.closest('.product-form__buttons') || atcBtn.parentElement);
      if (target && target.parentNode) {
        var bar = document.createElement('aside');
        bar.className = 'dm-product-quote dm-product-quote--proof';
        bar.setAttribute('aria-label', 'Customer rating');
        bar.innerHTML = '<div class="dm-product-quote__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="dm-product-quote__text">' + (proof.line || 'Loved by over 8,300 customers across the UK') + '</p>';
        target.parentNode.insertBefore(bar, target);
      }
    }
  }

  function init() {
    var handle = currentHandle();
    if (handles.indexOf(handle) === -1 || !model) return;
    var root = qs(document, '[data-daisy-pebble-picture]');
    var form = getForm();
    var config = root && readConfig(root);
    if (!root || !form || !config) return;
    if (window.DaisyCleanProduct) {
      config.giftWrap = null;
      config.heartOffer = null;
      config.spray = null;
      config.luckySixpence = null;
    }
    render(root, config);
    mountBuilder(root, form);
    hideGlobo(form, root);
    // Qty is always 1 for personalised pebble pictures; hide the qty stepper so it doesn't mislead.
    qsa(document, '.productView-quantity').forEach(function (el) { el.hidden = true; });
    initAddons(root, config);
    renderProof(form);
    // Phone keyboards: label Return as "Done" and let it close the keyboard
    // instead of leaving it open (or submitting the form).
    qsa(root, 'input[type="text"]').forEach(function (input) { input.setAttribute('enterkeyhint', 'done'); });
    root.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' && event.target.matches('input[type="text"]')) {
        event.preventDefault();
        event.target.blur();
      }
    });
    root.addEventListener('input', function () { update(root, config); });
    root.addEventListener('change', function () { update(root, config); });
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      submit(root, config);
    }, true);
    document.addEventListener('click', function (event) {
      if (event.target.closest('#product-add-to-cart')) {
        event.preventDefault();
        event.stopImmediatePropagation();
        submit(root, config);
      }
    }, true);
    update(root, config);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
