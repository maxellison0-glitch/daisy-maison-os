(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.DaisyStreetSignCartModel = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';

  function integer(value, fallback) {
    var parsed = parseInt(value, 10);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function normaliseAddonMode(secondSign, requested) {
    if (requested === 'single') return 'single';
    if (secondSign && requested === 'double') return 'double';
    return 'none';
  }

  function giftCartLine(gift, requestedMode, variants, prices) {
    var mode = normaliseAddonMode(true, requestedMode || gift.mode);
    if (mode === 'none') return null;
    if (gift.key === 'mounting' && mode === 'double') {
      return {
        id: variants.mountingPair,
        quantity: 1,
        linePrice: prices.mountingPair,
        properties: gift.properties || {}
      };
    }
    return {
      id: gift.id,
      quantity: mode === 'double' ? 2 : 1,
      linePrice: integer(gift.price, 0) * (mode === 'double' ? 2 : 1),
      properties: gift.properties || {}
    };
  }

  function linkedProperties(bundleId) {
    return {
      '_Linked product': 'Mr & Mrs Personalised Street Sign Gift',
      '_Bundle ID': bundleId
    };
  }

  function mergeProperties(base, extra) {
    var merged = {};
    Object.keys(base || {}).forEach(function (key) { merged[key] = base[key]; });
    Object.keys(extra || {}).forEach(function (key) { merged[key] = extra[key]; });
    return merged;
  }

  function poundsLabel(pence) {
    return '£' + ((Number(pence) || 0) / 100).toFixed(2);
  }

  function sizeLabel(size, prices) {
    prices = prices || {};
    if (size === 'medium') return 'Medium 45 x 12cm (+' + poundsLabel(prices.medium) + ')';
    if (size === 'large') return 'Large 57 x 12cm (+' + poundsLabel(prices.large) + ')';
    return 'Small 28 x 12cm';
  }

  function sizeUpgradeLine(size, quantity, variants, prices, bundleId, appliesTo) {
    var medium = size === 'medium';
    var large = size === 'large';
    if (!medium && !large) return null;
    var label = medium ? 'Medium 45 x 12cm' : 'Large 57 x 12cm';
    var properties = { 'Upgrade': label };
    if (appliesTo) properties['Applies to'] = appliesTo;
    return {
      id: medium ? variants.medium : variants.large,
      quantity: quantity,
      linePrice: (medium ? prices.medium : prices.large) * quantity,
      properties: mergeProperties(linkedProperties(bundleId), properties)
    };
  }

  function buildCartItems(state, variants, prices, bundleId) {
    var quantity = Math.max(1, integer(state.quantity, 1));
    var items = [{
      id: variants.main,
      quantity: quantity,
      linePrice: prices.base * quantity,
      properties: {
        'Line 1': state.lineOne,
        'Line 2': state.lineTwo || '',
        'Size': sizeLabel(state.size, prices),
        '_Custom option flow': 'Daisy native street sign options',
        '_Bundle ID': bundleId
      }
    }];

    var mainUpgrade = sizeUpgradeLine(state.size, quantity, variants, prices, bundleId);
    if (mainUpgrade) items.push(mainUpgrade);

    if (state.secondSign) {
      items.push({
        id: variants.second,
        quantity: quantity,
        linePrice: prices.second * quantity,
        properties: mergeProperties(linkedProperties(bundleId), {
          'Offer': 'Second sign',
          'Line 1': state.secondLineOne,
          'Line 2': state.secondLineTwo || '',
          'Size': sizeLabel(state.secondSize, prices)
        })
      });
      var secondUpgrade = sizeUpgradeLine(state.secondSize, quantity, variants, prices, bundleId, 'Second sign');
      if (secondUpgrade) items.push(secondUpgrade);
    }

    (state.gifts || []).forEach(function (gift) {
      var mode = normaliseAddonMode(state.secondSign, gift.mode);
      var line = giftCartLine(gift, mode, variants, prices);
      if (!line) return;
      line.properties = mergeProperties(linkedProperties(bundleId), gift.properties);
      line.properties['Add-on mode'] = mode;
      items.push(line);
    });

    return items;
  }

  function calculateTotal(state, variants, prices) {
    var current = buildCartItems(state, variants, prices, 'total-preview').reduce(function (sum, item) {
      return sum + item.linePrice;
    }, 0);
    var quantity = Math.max(1, integer(state.quantity, 1));
    var compareAt = prices.compareAt > prices.base ? current + ((prices.compareAt - prices.base) * quantity) : null;
    return { current: current, compareAt: compareAt };
  }

  function previewSigns(state) {
    var signs = [{ lineOne: state.lineOne || '', lineTwo: state.lineTwo || '' }];
    if (state.secondSign) signs.push({ lineOne: state.secondLineOne || '', lineTwo: state.secondLineTwo || '' });
    return signs;
  }

  return {
    normaliseAddonMode: normaliseAddonMode,
    giftCartLine: giftCartLine,
    buildCartItems: buildCartItems,
    calculateTotal: calculateTotal,
    previewSigns: previewSigns
  };
});
