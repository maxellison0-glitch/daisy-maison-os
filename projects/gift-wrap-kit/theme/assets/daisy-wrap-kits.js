/* daisy-wrap-kits.js — Christmas gift wrap kit: one card, two styles, plus the
 * half-price second kit.
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
 *     which is exactly what those builders read at add-to-cart.
 *
 *  B) tick-box rows in the street-sign clones (input name matches gift-wrap /
 *     giftwrap) and C) "Add a Gift Wrap Kit" extras in the heart / diffuser
 *     builders ([data-heart-extra]): the row is hidden and replaced with the
 *     same card as A, kept in sync with the hidden tick box so the builder's
 *     own submit code still adds the kit. Those builders keep the classic
 *     variant id in their own closures, so the chosen kit is swapped in at
 *     submit time by the hooks below.
 *
 *  Second kit (DAISY_WRAP_KITS.secondKit): once a kit is chosen, a line offers
 *  a second kit at half price with its own Christmas / Classic chips. It is
 *  added as its own basket line; the price cut itself comes from the store's
 *  automatic "second wrap kit half price" discount, so the basket is always
 *  the source of truth. Turn the flag off in the snippet if that discount is
 *  ever removed.
 *
 *  Hooks: DaisyCartSubmit.create().add, DaisyNativeStreetSizes.submit/add and
 *  window.fetch for direct /cart/add.js posts (JSON, form-encoded, FormData).
 *  Every hook is a pure function of page state: nothing changes unless a kit
 *  choice or a second kit was made on this page.
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
  var SECOND = !!KITS.secondKit;
  var SECOND_LABEL = 'Second gift wrap kit (half price)';
  var FESTIVE_PAGE = /christmas|xmas|santa|elf|festive|stocking|reindeer|sleigh/i.test(window.location.pathname);

  var state = { style: FESTIVE_PAGE ? 'christmas' : 'classic', rows: 0, second: null };

  function qs(root, sel) { return (root || document).querySelector(sel); }
  function qsa(root, sel) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function kit(style) { return style === 'christmas' ? XMAS : CLASSIC; }
  function isKitId(id) { id = Number(id); return id === classicId || id === xmasId; }
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
  function halfPrice(k) { return Math.round(k.price / 2); }
  function pairPrice(k) { return k.price + halfPrice(k); }
  // Write-only-if-different helpers. The card observer below re-syncs on
  // attribute changes, and a no-op classList.toggle / setAttribute still
  // queues a mutation record, so every write here must be conditional.
  function setClass(el, name, on) { if (el.classList.contains(name) !== !!on) el.classList.toggle(name, !!on); }
  function setAttr(el, name, value) { if (el.getAttribute(name) !== value) el.setAttribute(name, value); }
  function setHidden(el, hidden) { if (el.hidden !== !!hidden) el.hidden = !!hidden; }

  /* ---------------- second kit (shared) ---------------- */

  function secondHtml() {
    if (!SECOND) return '';
    return '<div class="dm-wrap-second" hidden>' +
      '<p class="dm-wrap-second__title">Wrapping another present? <strong>Second kit half price</strong> · +' + esc(money(halfPrice(CLASSIC))) + ' at basket</p>' +
      '<div class="dm-wrap-second__chips">' + secondChip('christmas') + secondChip('classic') + '</div></div>';
  }
  function secondChip(style) {
    var k = kit(style);
    return '<button type="button" class="dm-wrap-chip" data-wrap-second="' + style + '" aria-pressed="false">' +
      '<img src="' + esc(k.thumb) + '" alt="" width="24" height="24" loading="lazy">' + esc(k.label) + '</button>';
  }
  function syncSecond(container, on) {
    var block = qs(container, '.dm-wrap-second');
    if (!block) return;
    if (!on && state.second) state.second = null;
    setHidden(block, !on);
    qsa(block, '[data-wrap-second]').forEach(function (btn) {
      var sel = on && btn.getAttribute('data-wrap-second') === state.second;
      setClass(btn, 'is-selected', sel);
      setAttr(btn, 'aria-pressed', sel ? 'true' : 'false');
    });
  }
  function syncAllSecond() {
    qsa(document, '.dm-cyg__card--wrap-styles').forEach(function (card) { syncCygCard(card); });
  }
  document.addEventListener('click', function (event) {
    var chip = event.target && event.target.closest && event.target.closest('[data-wrap-second]');
    if (!chip) return;
    event.preventDefault();
    event.stopPropagation();
    var style = chip.getAttribute('data-wrap-second');
    state.second = state.second === style ? null : style;
    syncAllSecond();
  }, true);

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
    // Christmas first on Christmas products, classic first everywhere else.
    if (FESTIVE_PAGE) {
      pair.appendChild(thumbFigure('christmas', null));
      pair.appendChild(thumbFigure('classic', thumb));
    } else {
      pair.appendChild(thumbFigure('classic', thumb));
      pair.appendChild(thumbFigure('christmas', null));
    }
    media.insertBefore(pair, body);

    // The builder's existing "single" button becomes one style; the other
    // style is a second "single" button. Both carry data-dm-addon-mode="single"
    // so the builders' own click handling (mode, totals, sticky bar) keeps
    // working. Order matches the thumbnails.
    var firstStyle = FESTIVE_PAGE ? 'christmas' : 'classic';
    var secondStyle = FESTIVE_PAGE ? 'classic' : 'christmas';
    single.classList.add('dm-wrap-style');
    single.setAttribute('data-dm-wrap-style', firstStyle);
    single.innerHTML = styleLabel(kit(firstStyle));
    var other = document.createElement('button');
    other.type = 'button';
    other.className = 'dm-addon-mode__option dm-wrap-style';
    other.setAttribute('data-dm-addon-mode', 'single');
    other.setAttribute('data-dm-wrap-style', secondStyle);
    other.setAttribute('aria-pressed', 'false');
    other.innerHTML = styleLabel(kit(secondStyle));
    single.parentNode.insertBefore(other, single.nextSibling);

    var desc = qs(body, '.dm-cyg__desc, .dm-cyg__note');
    if (!desc) {
      desc = document.createElement('p');
      desc.className = 'dm-cyg__desc';
      body.appendChild(desc);
    }
    if (KITS.copy) desc.textContent = KITS.copy;

    var name = qs(body, '.dm-cyg__name');
    if (name && !name.dataset.wrapBaseName) name.dataset.wrapBaseName = name.textContent.trim();

    if (SECOND) {
      var holder = document.createElement('div');
      holder.innerHTML = secondHtml();
      controls.parentNode.insertBefore(holder.firstChild, controls.nextSibling);
    }

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
    if (dbl && /£/.test(dbl.textContent)) {
      // Two of the same kit: the second is half price through the automatic discount.
      dbl.textContent = dbl.textContent.replace(/£\s?[\d.,]+/, money(SECOND ? pairPrice(k) : k.price * 2));
    }
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
      setAttr(btn, 'aria-pressed', active ? 'true' : 'false');
    });
    qsa(card, '[data-wrap-thumb]').forEach(function (fig) {
      var mine = fig.getAttribute('data-wrap-thumb') === style;
      setClass(fig, 'is-selected', on && mine);
      setClass(fig, 'is-dimmed', on && !mine);
    });
    var name = qs(card, '.dm-cyg__name');
    if (name && name.dataset.wrapBaseName) {
      var wanted = on ? name.dataset.wrapBaseName + ' · ' + kit(style).label : name.dataset.wrapBaseName;
      if (name.textContent !== wanted) name.textContent = wanted;
    }
    syncSecond(card, on);
  }

  function watchCard(card) {
    if (!window.MutationObserver) return;
    // The builders re-mark is-active / aria-pressed on every update (both
    // style buttons are "single" to them). Re-sync after each change. Every
    // write in the sync is conditional and the sync's own records are
    // discarded, so this settles in one pass and can never loop.
    var observer = new MutationObserver(function () {
      syncCygCard(card);
      observer.takeRecords(); // drop the records our own writes just queued
    });
    observer.observe(card, { attributes: true, subtree: true, attributeFilter: ['class', 'aria-pressed', 'data-addon-mode'] });
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
    else if (mode === 'double' && !card.dataset.wrapStyle) applyCygStyle(card, state.style);
    window.setTimeout(function () { syncCygCard(card); }, 0);
  }, true);

  /* ---------------- B/C) checkbox rows -> the same card ---------------- */
  // The street-sign clones and the heart / diffuser builders offer the kit as
  // a tick-box row. That row is hidden and replaced with the exact Mr & Mrs
  // card (same markup, same buttons), then enhanced by the same code path as
  // above. The hidden tick box is kept in sync so the builder's own submit
  // code still adds the kit; the hooks below swap in the chosen variant.

  function cardHtml() {
    return '<div class="dm-cyg__card dm-wrap-card" role="group" data-addon-key="giftwrap" data-addon-mode="none" data-variant="' + classicId + '" data-price="' + CLASSIC.price + '" data-name="' + esc(CLASSIC.name) + '">' +
      '<div class="dm-cyg__inner"><div class="dm-cyg__media">' +
      '<img class="dm-cyg__thumb" src="' + esc(CLASSIC.thumb) + '" alt="' + esc(CLASSIC.name) + '" width="64" height="64" loading="lazy" data-dm-zoomable data-dm-zoom-src="' + esc(CLASSIC.zoom || CLASSIC.thumb) + '">' +
      '<div class="dm-cyg__body"><div class="dm-cyg__top"><span class="dm-cyg__name">Gift Wrap Kit</span><span class="dm-cyg__price">' + esc(money(CLASSIC.price)) + '</span></div>' +
      '<p class="dm-cyg__desc"></p></div></div>' +
      '<div class="dm-addon-mode" aria-label="Gift wrap kit">' +
      '<button class="dm-addon-mode__option is-active" type="button" data-dm-addon-mode="none" aria-pressed="true">No thanks</button>' +
      '<button class="dm-addon-mode__option" type="button" data-dm-addon-mode="single" aria-pressed="false">Add gift wrap kit</button>' +
      '</div></div></div>';
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

  function setMode(card, mode) {
    if (card.dataset.addonMode !== mode) card.dataset.addonMode = mode;
    qsa(card, '.dm-addon-mode > [data-dm-addon-mode]').forEach(function (btn) {
      var active = btn.getAttribute('data-dm-addon-mode') === mode;
      setClass(btn, 'is-active', active);
      setAttr(btn, 'aria-pressed', active ? 'true' : 'false');
    });
    syncCygCard(card);
    var input = card.__dmInput;
    if (input) {
      var want = mode !== 'none';
      if (input.checked !== want) {
        input.checked = want;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  }

  function mountCard(input) {
    input.dataset.wrapEnhanced = 'true';
    var host = input.closest('label') || input.parentNode;
    if (!host || !host.parentNode) return;
    var mount = document.createElement('div');
    mount.className = 'dm-wrap-mount';
    mount.innerHTML = cardHtml();
    var card = mount.firstChild;
    card.__dmInput = input;
    host.parentNode.insertBefore(mount, host.nextSibling);
    host.hidden = true;
    host.style.setProperty('display', 'none', 'important');
    enhanceCygCard(card);
    // If anything else unticks the box (a builder reset), the card follows.
    input.addEventListener('change', function () {
      if (!input.checked && (card.dataset.addonMode || 'none') !== 'none') setMode(card, 'none');
    });
    state.rows += 1;
  }

  // Mode clicks on the self-made cards (the builders only handle their own).
  document.addEventListener('click', function (event) {
    var btn = event.target && event.target.closest && event.target.closest('.dm-wrap-card [data-dm-addon-mode]');
    if (!btn) return;
    var card = btn.closest('.dm-wrap-card');
    if (!card) return;
    event.preventDefault();
    setMode(card, btn.getAttribute('data-dm-addon-mode') || 'none');
  });

  /* ---------------- cart hooks ---------------- */

  function renameAddon(value) {
    return (typeof value === 'string' && /gift wrap kit/i.test(value) && !/christmas/i.test(value))
      ? value.replace(/gift wrap kit/i, 'Christmas Gift Wrap Kit')
      : value;
  }

  function rewriteItems(items) {
    if (state.style !== 'christmas' || !state.rows) return items;
    return items.map(function (item) {
      if (!item || Number(item.id) !== classicId) return item;
      // The hooks stack (native sizes -> DaisyCartSubmit -> fetch), so a
      // Classic second kit added by an earlier pass must stay Classic.
      if (item.properties && item.properties['Add-on'] === SECOND_LABEL) return item;
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

  function secondLine(primaryProps) {
    var props = { 'Add-on': SECOND_LABEL };
    if (primaryProps) {
      if (primaryProps['_Bundle ID']) props['_Bundle ID'] = primaryProps['_Bundle ID'];
      if (primaryProps['_Linked product']) props['_Linked product'] = primaryProps['_Linked product'];
    }
    return { id: kit(state.second).variantId, quantity: 1, properties: props };
  }

  function appendSecond(items) {
    if (!SECOND || !state.second) return items;
    if (items.some(function (i) { return i && i.properties && i.properties['Add-on'] === SECOND_LABEL; })) return items;
    var primary = null;
    items.forEach(function (i) { if (!primary && i && isKitId(i.id)) primary = i; });
    if (!primary) return items;
    return items.concat([secondLine(primary.properties)]);
  }

  function transformItems(items) {
    if (!Array.isArray(items)) return items;
    return appendSecond(rewriteItems(items));
  }

  function hookCartSubmit() {
    var lib = window.DaisyCartSubmit;
    if (!lib || lib.__dmWrapKits || typeof lib.create !== 'function') return;
    var create = lib.create;
    lib.create = function () {
      var api = create.apply(this, arguments);
      if (api && typeof api.add === 'function' && !api.__dmWrapKits) {
        var add = api.add;
        api.add = function (items, onSlow) { return add.call(api, transformItems(items), onSlow); };
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
      lib.submit = function (items) { return submit.call(lib, transformItems(items)); };
    }
    if (typeof lib.add === 'function') {
      var add = lib.add;
      lib.add = function (items, config) { return add.call(lib, transformItems(items), config); };
    }
    lib.__dmWrapKits = true;
  }

  // Form-style single-item posts (heart / diffuser builders post one line at a
  // time): rewrite the kit line in place and, when a second kit was chosen,
  // return the extra line to post straight after it.
  function rewriteForm(body) {
    var id = Number(body.get('id'));
    if (!isKitId(id)) return null;
    if (id === classicId && state.rows && state.style === 'christmas') {
      body.set('id', String(xmasId));
      if (body.has('properties[Add-on]')) body.set('properties[Add-on]', renameAddon(body.get('properties[Add-on]')));
    }
    if (!SECOND || !state.second) return null;
    var props = {};
    if (body.has('properties[_Bundle ID]')) props['_Bundle ID'] = body.get('properties[_Bundle ID]');
    if (body.has('properties[_Linked product]')) props['_Linked product'] = body.get('properties[_Linked product]');
    return secondLine(props);
  }

  function hookFetch() {
    if (!window.fetch || window.fetch.__dmWrapKits) return;
    var original = window.fetch;
    var wrapped = function (input, init) {
      var extra = null;
      try {
        var url = typeof input === 'string' ? input : ((input && input.url) || '');
        if (/\/cart\/add(\.js)?(\?|$)/.test(url) && init && init.body) {
          var body = init.body;
          if (typeof body === 'string' && body.trim().charAt(0) === '{') {
            var data = JSON.parse(body);
            if (Array.isArray(data.items)) data.items = transformItems(data.items);
            else if (isKitId(data.id)) { var t = transformItems([data]); data = t[0]; if (t[1]) extra = t[1]; }
            init = Object.assign({}, init, { body: JSON.stringify(data) });
          } else if (typeof body === 'string' && /(^|&)id=/.test(body)) {
            var params = new URLSearchParams(body);
            extra = rewriteForm(params);
            init = Object.assign({}, init, { body: params.toString() });
          } else if ((typeof FormData !== 'undefined' && body instanceof FormData) || (typeof URLSearchParams !== 'undefined' && body instanceof URLSearchParams)) {
            extra = rewriteForm(body);
          }
        }
      } catch (e) { extra = null; /* never block a cart post */ }
      var request = original.call(window, input, init);
      if (!extra) return request;
      return request.then(function (response) {
        if (!response || !response.ok) return response;
        return original.call(window, '/cart/add.js', {
          method: 'POST', credentials: 'same-origin',
          headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: [extra] })
        }).then(function () { return response; }, function () { return response; });
      });
    };
    wrapped.__dmWrapKits = true;
    window.fetch = wrapped;
  }

  /* ---------------- boot ---------------- */

  function scan() {
    qsa(document, '.dm-cyg__card').forEach(enhanceCygCard);
    qsa(document, 'input[type="checkbox"]').forEach(function (input) { if (isWrapCheckbox(input)) mountCard(input); });
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
    window.DaisyWrapKits = { kits: KITS, state: state, transformItems: transformItems };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
