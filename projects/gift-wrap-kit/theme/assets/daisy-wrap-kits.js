/* daisy-wrap-kits.js — Christmas gift wrap kit: one card, two styles.
 *
 * Loaded by snippets/dm-wrap-kits.liquid ONLY while the Christmas kit product
 * (handle christmas-gift-wrap-kit) is active, published and purchasable. Off
 * season this file is not even requested and nothing on the page changes.
 *
 * It layers a Classic / Christmas choice onto every place a builder already
 * offers the classic Gift Wrap Kit, without editing the builders:
 *
 *  A) dm-cyg cards — Mr & Mrs (snippets/dm-gc.liquid) and the pebble-picture
 *     builder (assets/daisy-pebble-picture.js). The "Add gift wrap" button
 *     becomes two buttons (Classic / Christmas) and the thumbnail becomes a
 *     pair. Choosing a style rewrites the card's data-variant / data-price,
 *     which is exactly what those builders read at add-to-cart, so their own
 *     cart code adds the right product. No cart hooks are involved here.
 *
 *  B) checkbox rows in the street-sign clones (input name matches gift-wrap /
 *     giftwrap: daisy-create-own-gift-wrap, daisy-ret-giftwrap,
 *     daisy-teacher-gift-wrap ...) — a style row appears under the ticked row.
 *
 *  C) "Add a Gift Wrap Kit" extras in the heart / diffuser builders
 *     ([data-heart-extra] checkboxes) — the same style row.
 *
 *  For B and C the builders keep the classic variant id inside their own
 *  closures, so the chosen kit is swapped in at submit time through three
 *  hooks: DaisyCartSubmit.create().add, DaisyNativeStreetSizes.submit/add and
 *  window.fetch for direct /cart/add.js posts (JSON and FormData bodies).
 *  Every hook is a no-op unless a style row exists on the page AND Christmas
 *  is the chosen style, so A-family pages and the cart page are untouched.
 *  B/C default to Classic (the safe kit for a wedding or christening gift);
 *  A has no default because choosing a style IS the add action.
 */
(function () {
  'use strict';

  var KITS = window.DAISY_WRAP_KITS;
  if (!KITS || !KITS.classic || !KITS.christmas) return;
  var CLASSIC = KITS.classic;
  var XMAS = KITS.christmas;
  var classicId = Number(CLASSIC.variantId);
  var xmasId = Number(XMAS.variantId);
  if (!classicId || !xmasId || classicId === xmasId) return;

  var state = { style: 'classic', rows: 0 };

  function qs(root, sel) { return (root || document).querySelector(sel); }
  function qsa(root, sel) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function kit(style) { return style === 'christmas' ? XMAS : CLASSIC; }
  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function money(pence) {
    try {
      return new Intl.NumberFormat('en-GB', { style: 'currency', currency: KITS.currency || 'GBP' }).format((Number(pence) || 0) / 100);
    } catch (e) {
      return '£' + ((Number(pence) || 0) / 100).toFixed(2);
    }
  }

  /* ---------------- A) dm-cyg cards ---------------- */

  function styleLabel(k) {
    return '<span class="dm-wrap-style__label">' + esc(k.label) + '</span>' +
      '<span class="dm-wrap-style__price">' + esc(money(k.price)) + '</span>';
  }

  function thumbFigure(style, img) {
    var k = kit(style);
    var fig = document.createElement('figure');
    fig.className = 'dm-wrap-thumb';
    fig.setAttribute('data-wrap-thumb', style);
    if (!img) {
      img = document.createElement('img');
      img.className = 'dm-cyg__thumb';
      img.width = 64;
      img.height = 64;
      img.loading = 'lazy';
      img.setAttribute('data-dm-zoomable', '');
    }
    img.src = k.thumb;
    img.alt = k.name;
    if (k.zoom) img.setAttribute('data-dm-zoom-src', k.zoom);
    var cap = document.createElement('figcaption');
    cap.textContent = k.label;
    fig.appendChild(img);
    fig.appendChild(cap);
    return fig;
  }

  function enhanceCygCard(card) {
    if (card.dataset.wrapEnhanced || Number(card.dataset.variant) !== classicId) return;
    var controls = qs(card, '.dm-addon-mode');
    var single = controls && qs(controls, '[data-dm-addon-mode="single"]');
    var media = qs(card, '.dm-cyg__media');
    var thumb = media && qs(media, 'img.dm-cyg__thumb');
    var body = media && qs(media, '.dm-cyg__body');
    if (!controls || !single || !media || !thumb || !body) return;
    card.dataset.wrapEnhanced = 'true';
    card.classList.add('dm-cyg__card--wrap-styles');

    var pair = document.createElement('div');
    pair.className = 'dm-wrap-thumbs';
    pair.appendChild(thumbFigure('classic', thumb));
    pair.appendChild(thumbFigure('christmas', null));
    media.insertBefore(pair, body);

    // The builder's existing "single" button becomes Classic; Christmas is a
    // second "single" button. Both carry data-dm-addon-mode="single" so the
    // builders' own click handling (mode, totals, sticky bar) keeps working.
    single.classList.add('dm-wrap-style');
    single.setAttribute('data-dm-wrap-style', 'classic');
    single.innerHTML = styleLabel(CLASSIC);
    var xmasBtn = document.createElement('button');
    xmasBtn.type = 'button';
    xmasBtn.className = 'dm-addon-mode__option dm-wrap-style';
    xmasBtn.setAttribute('data-dm-addon-mode', 'single');
    xmasBtn.setAttribute('data-dm-wrap-style', 'christmas');
    xmasBtn.setAttribute('aria-pressed', 'false');
    xmasBtn.innerHTML = styleLabel(XMAS);
    single.parentNode.insertBefore(xmasBtn, single.nextSibling);

    var desc = qs(body, '.dm-cyg__desc, .dm-cyg__note');
    if (!desc) {
      desc = document.createElement('p');
      desc.className = 'dm-cyg__desc';
      body.appendChild(desc);
    }
    if (KITS.copy) desc.textContent = KITS.copy;

    var name = qs(body, '.dm-cyg__name');
    if (name && !name.dataset.wrapBaseName) name.dataset.wrapBaseName = name.textContent.trim();

    syncCygCard(card);
    watchCard(card);
  }

  function applyCygStyle(card, style) {
    var k = kit(style);
    card.dataset.variant = String(k.variantId);
    card.dataset.price = String(k.price);
    if (card.hasAttribute('data-pair-variant')) card.dataset.pairVariant = String(k.variantId);
    if (card.hasAttribute('data-pair-price')) card.dataset.pairPrice = String(k.price * 2);
    // Mr & Mrs keys its card on data-addon-key, so its data-name (the cart
    // "Add-on" property) can follow the kit. The pebble builder keys on
    // data-name="Gift Wrap Kit" for its second-frame logic, so leave it alone.
    if (card.hasAttribute('data-addon-key')) card.dataset.name = k.name;
    card.dataset.wrapStyle = style;
    state.style = style;
    var price = qs(card, '.dm-cyg__price');
    if (price) price.textContent = money(k.price);
    var dbl = qs(card, '[data-dm-addon-mode="double"]');
    if (dbl && /£/.test(dbl.textContent)) dbl.textContent = dbl.textContent.replace(/£\s?[\d.,]+/, money(k.price * 2));
  }

  function syncCygCard(card) {
    var style = card.dataset.wrapStyle || '';
    var on = !!style && (card.dataset.addonMode || 'none') !== 'none';
    qsa(card, '[data-dm-wrap-style]').forEach(function (btn) {
      var active = on && btn.getAttribute('data-dm-wrap-style') === style;
      if (active) {
        if (!btn.hasAttribute('data-wrap-active')) btn.setAttribute('data-wrap-active', '');
      } else if (btn.hasAttribute('data-wrap-active')) {
        btn.removeAttribute('data-wrap-active');
      }
      var pressed = active ? 'true' : 'false';
      if (btn.getAttribute('aria-pressed') !== pressed) btn.setAttribute('aria-pressed', pressed);
    });
    qsa(card, '[data-wrap-thumb]').forEach(function (fig) {
      var mine = fig.getAttribute('data-wrap-thumb') === style;
      fig.classList.toggle('is-selected', on && mine);
      fig.classList.toggle('is-dimmed', on && !mine);
    });
    var name = qs(card, '.dm-cyg__name');
    if (name && name.dataset.wrapBaseName) {
      var wanted = on ? name.dataset.wrapBaseName + ' · ' + kit(style).label : name.dataset.wrapBaseName;
      if (name.textContent !== wanted) name.textContent = wanted;
    }
  }

  function watchCard(card) {
    if (!window.MutationObserver) return;
    // The builders re-mark is-active / aria-pressed on every update (both
    // style buttons are "single" to them). Re-sync after each change; writes
    // above are conditional, so this settles in one pass.
    new MutationObserver(function () { syncCygCard(card); })
      .observe(card, { attributes: true, subtree: true, attributeFilter: ['class', 'aria-pressed', 'data-addon-mode'] });
  }

  // Capture phase, registered before the builders' own document/root
  // listeners (this script is deferred ahead of them), so the card's data is
  // swapped before the builder reads the mode and recalculates totals.
  document.addEventListener('click', function (event) {
    var btn = event.target && event.target.closest && event.target.closest('.dm-cyg__card--wrap-styles [data-dm-addon-mode]');
    if (!btn) return;
    var card = btn.closest('.dm-cyg__card');
    if (!card) return;
    var style = btn.getAttribute('data-dm-wrap-style');
    var mode = btn.getAttribute('data-dm-addon-mode');
    if (style) applyCygStyle(card, style);
    else if (mode === 'none') delete card.dataset.wrapStyle;
    else if (mode === 'double' && !card.dataset.wrapStyle) applyCygStyle(card, 'classic');
    window.setTimeout(function () { syncCygCard(card); }, 0);
  }, true);

  /* ---------------- B/C) checkbox rows ---------------- */

  function choiceHtml(style) {
    var k = kit(style);
    var on = state.style === style;
    return '<button type="button" class="dm-wrap-choice' + (on ? ' is-selected' : '') + '" data-wrap-choice="' + style + '" aria-pressed="' + (on ? 'true' : 'false') + '">' +
      '<img src="' + esc(k.thumb) + '" alt="" width="44" height="44" loading="lazy">' +
      '<span><span class="dm-wrap-choice__label">' + esc(k.label) + '</span>' +
      '<span class="dm-wrap-choice__price">' + esc(money(k.price)) + '</span></span></button>';
  }

  function isWrapCheckbox(input) {
    if (input.type !== 'checkbox' || input.dataset.wrapEnhanced) return false;
    if (/gift[-_]?wrap/i.test(input.name || '')) return true;
    if (input.hasAttribute('data-heart-extra')) {
      var label = input.closest('label');
      return !!(label && /gift wrap kit/i.test(label.textContent || ''));
    }
    return false;
  }

  function enhanceCheckbox(input) {
    input.dataset.wrapEnhanced = 'true';
    var host = input.closest('label') || input.parentNode;
    if (!host || !host.parentNode) return;
    var row = document.createElement('div');
    row.className = 'dm-wrap-row';
    row.hidden = !input.checked;
    row.innerHTML = '<p class="dm-wrap-row__title">Choose your kit</p>' +
      '<div class="dm-wrap-row__choices">' + choiceHtml('classic') + choiceHtml('christmas') + '</div>';
    host.parentNode.insertBefore(row, host.nextSibling);
    input.addEventListener('change', function () { row.hidden = !input.checked; });
    row.addEventListener('click', function (event) {
      var choice = event.target.closest && event.target.closest('[data-wrap-choice]');
      if (!choice) return;
      event.preventDefault();
      event.stopPropagation();
      setStyle(choice.getAttribute('data-wrap-choice'));
    });
    state.rows += 1;
  }

  function setStyle(style) {
    state.style = style === 'christmas' ? 'christmas' : 'classic';
    qsa(document, '[data-wrap-choice]').forEach(function (btn) {
      var on = btn.getAttribute('data-wrap-choice') === state.style;
      btn.classList.toggle('is-selected', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  /* ---------------- cart hooks (B/C only) ---------------- */

  function renameAddon(value) {
    return (typeof value === 'string' && /gift wrap kit/i.test(value) && !/christmas/i.test(value))
      ? value.replace(/gift wrap kit/i, 'Christmas Gift Wrap Kit')
      : value;
  }

  function rewriteItems(items) {
    if (state.style !== 'christmas' || !state.rows || !Array.isArray(items)) return items;
    return items.map(function (item) {
      if (!item || Number(item.id) !== classicId) return item;
      var copy = {};
      Object.keys(item).forEach(function (key) { copy[key] = item[key]; });
      copy.id = xmasId;
      if (item.properties && typeof item.properties === 'object') {
        var props = {};
        Object.keys(item.properties).forEach(function (key) { props[key] = renameAddon(item.properties[key]); });
        copy.properties = props;
      }
      return copy;
    });
  }

  function hookCartSubmit() {
    var lib = window.DaisyCartSubmit;
    if (!lib || lib.__dmWrapKits || typeof lib.create !== 'function') return;
    var create = lib.create;
    lib.create = function () {
      var api = create.apply(this, arguments);
      if (api && typeof api.add === 'function' && !api.__dmWrapKits) {
        var add = api.add;
        api.add = function (items, onSlow) { return add.call(api, rewriteItems(items), onSlow); };
        api.__dmWrapKits = true;
      }
      return api;
    };
    lib.__dmWrapKits = true;
  }

  function hookNativeSizes() {
    var lib = window.DaisyNativeStreetSizes;
    if (!lib || lib.__dmWrapKits) return;
    if (typeof lib.submit === 'function') {
      var submit = lib.submit;
      lib.submit = function (items) { return submit.call(lib, rewriteItems(items)); };
    }
    if (typeof lib.add === 'function') {
      var add = lib.add;
      lib.add = function (items, config) { return add.call(lib, rewriteItems(items), config); };
    }
    lib.__dmWrapKits = true;
  }

  function rewriteBody(body) {
    if (typeof body === 'string') {
      var trimmed = body.trim();
      if (trimmed.charAt(0) === '{') {
        var data = JSON.parse(trimmed);
        if (Array.isArray(data.items)) data.items = rewriteItems(data.items);
        else if (Number(data.id) === classicId) data = rewriteItems([data])[0];
        return JSON.stringify(data);
      }
      if (/(^|&)id=/.test(trimmed)) {
        var params = new URLSearchParams(trimmed);
        if (Number(params.get('id')) === classicId) {
          params.set('id', String(xmasId));
          if (params.has('properties[Add-on]')) params.set('properties[Add-on]', renameAddon(params.get('properties[Add-on]')));
        }
        return params.toString();
      }
      return body;
    }
    var formLike = (typeof FormData !== 'undefined' && body instanceof FormData) ||
      (typeof URLSearchParams !== 'undefined' && body instanceof URLSearchParams);
    if (formLike) {
      if (Number(body.get('id')) === classicId) {
        body.set('id', String(xmasId));
        if (body.has('properties[Add-on]')) body.set('properties[Add-on]', renameAddon(body.get('properties[Add-on]')));
      }
      var i = 0;
      while (body.has('items[' + i + '][id]')) {
        if (Number(body.get('items[' + i + '][id]')) === classicId) body.set('items[' + i + '][id]', String(xmasId));
        i += 1;
      }
    }
    return body;
  }

  function hookFetch() {
    if (!window.fetch || window.fetch.__dmWrapKits) return;
    var original = window.fetch;
    var wrapped = function (input, init) {
      try {
        var url = typeof input === 'string' ? input : ((input && input.url) || '');
        if (state.rows && state.style === 'christmas' && /\/cart\/add(\.js)?(\?|$)/.test(url) && init && init.body) {
          init = Object.assign({}, init, { body: rewriteBody(init.body) });
        }
      } catch (e) { /* never block a cart post */ }
      return original.call(this, input, init);
    };
    wrapped.__dmWrapKits = true;
    window.fetch = wrapped;
  }

  /* ---------------- boot ---------------- */

  function scan() {
    qsa(document, '.dm-cyg__card').forEach(enhanceCygCard);
    qsa(document, 'input[type="checkbox"]').forEach(function (input) { if (isWrapCheckbox(input)) enhanceCheckbox(input); });
  }

  function init() {
    hookCartSubmit();
    hookNativeSizes();
    hookFetch();
    scan();
    if (window.MutationObserver) {
      var pending = null;
      new MutationObserver(function () {
        if (pending) return;
        pending = window.setTimeout(function () { pending = null; scan(); }, 40);
      }).observe(document.body, { childList: true, subtree: true });
    }
    window.DaisyWrapKits = { kits: KITS, state: state, rewriteItems: rewriteItems, setStyle: setStyle };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
