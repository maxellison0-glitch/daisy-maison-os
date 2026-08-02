// Regression net for the Mr & Mrs cart payload.
//
// The 2 Aug 2026 layout change (tap-the-sign -> visible Line 1 / Line 2 boxes)
// rewrote how the inputs are built but deliberately did not touch
// daisy-street-sign-cart-model.js. These tests pin the contract that the
// artwork generator and the order workflow depend on: every personalised line
// item carries 'Line 1' and 'Line 2', and second-sign text never leaks into the
// cart when the offer is off.
//
// Run: node --test projects/daisy-street-sign/personaliser/tests/cart-payload.test.js

const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

// The live copy of the cart model, tracked alongside the personaliser assets.
// Deliberately not read from a dated backup folder — those are rollback
// material and may be pruned.
const model = require(path.join(__dirname, '..', 'daisy-street-sign-cart-model.js'));

// Real values, read from the live product data block on 2 Aug 2026.
const variants = {
  main: 50189214187859,
  medium: 54100431962451,
  large: 54100431995219,
  second: 52473837355347,
  mountingSingle: 50706678514003,
  mountingPair: 54066025759059
};

const prices = {
  base: 1125,
  compareAt: 2895,
  medium: 599,
  large: 899,
  second: 995,
  mountingSingle: 199,
  mountingPair: 399
};

function baseState(overrides = {}) {
  return {
    quantity: 1,
    lineOne: 'MR & MRS CHAPMAN',
    lineTwo: 'FROM THIS DAY FORWARD - 14.08.2026',
    size: 'standard',
    secondSign: false,
    secondLineOne: '',
    secondLineTwo: '',
    secondSize: 'standard',
    gifts: [],
    ...overrides
  };
}

const build = (state, id = 'bundle-test') => model.buildCartItems(state, variants, prices, id);
const mainLine = (items) => items.find((line) => line.id === variants.main);
const secondLine = (items) => items.find((line) => line.id === variants.second);

test('main sign carries Line 1 and Line 2 verbatim', () => {
  const main = mainLine(build(baseState()));
  assert.equal(main.properties['Line 1'], 'MR & MRS CHAPMAN');
  assert.equal(main.properties['Line 2'], 'FROM THIS DAY FORWARD - 14.08.2026');
  assert.equal(main.properties.Size, 'Small 28 x 12cm');
});

test('an empty Line 2 is sent as an empty string, never undefined', () => {
  const main = mainLine(build(baseState({ lineTwo: '' })));
  assert.equal(main.properties['Line 2'], '');
  assert.ok('Line 2' in main.properties);
});

test('second sign text never reaches the cart while the offer is off', () => {
  const items = build(baseState({ secondLineOne: 'MUST NOT SUBMIT', secondLineTwo: 'NOR THIS' }));
  assert.equal(secondLine(items), undefined);
  assert.equal(JSON.stringify(items).includes('MUST NOT SUBMIT'), false);
});

test('both signs carry their own wording when the offer is on', () => {
  const items = build(baseState({
    secondSign: true,
    secondLineOne: 'MR & MRS NICHOLS',
    secondLineTwo: 'OUR FIRST HOME'
  }));
  assert.equal(mainLine(items).properties['Line 1'], 'MR & MRS CHAPMAN');
  assert.equal(secondLine(items).properties['Line 1'], 'MR & MRS NICHOLS');
  assert.equal(secondLine(items).properties['Line 2'], 'OUR FIRST HOME');
  assert.equal(secondLine(items).properties.Offer, 'Second sign');
});

test('each sign gets its own size label and upgrade line', () => {
  const items = build(baseState({
    size: 'large',
    secondSign: true,
    secondLineOne: 'MR & MRS NICHOLS',
    secondSize: 'medium'
  }));
  assert.equal(mainLine(items).properties.Size, 'Large 57 x 12cm (+£8.99)');
  assert.equal(secondLine(items).properties.Size, 'Medium 45 x 12cm (+£5.99)');

  const upgrades = items.filter((line) => line.properties.Upgrade);
  assert.equal(upgrades.length, 2);
  // The second sign's upgrade must be attributable, or fulfilment cannot tell
  // which of the two signs the extra length belongs to.
  const secondUpgrade = upgrades.find((line) => line.properties['Applies to'] === 'Second sign');
  assert.equal(secondUpgrade.id, variants.medium);
  assert.equal(upgrades.find((line) => !line.properties['Applies to']).id, variants.large);
});

test('mirrored sizes produce two upgrade lines of the same variant', () => {
  const items = build(baseState({
    size: 'large',
    secondSign: true,
    secondLineOne: 'MR & MRS NICHOLS',
    secondSize: 'large'
  }));
  const upgrades = items.filter((line) => line.properties.Upgrade);
  assert.equal(upgrades.length, 2);
  assert.ok(upgrades.every((line) => line.id === variants.large));
});

test('every line in a bundle shares one bundle id', () => {
  const items = build(baseState({
    size: 'large',
    secondSign: true,
    secondLineOne: 'MR & MRS NICHOLS',
    secondSize: 'large'
  }), 'street-sign-123');
  assert.ok(items.length > 1);
  assert.ok(items.every((line) => line.properties['_Bundle ID'] === 'street-sign-123'));
});

test('add-ons only reach quantity two once a second sign exists', () => {
  assert.equal(model.normaliseAddonMode(false, 'double'), 'none');
  assert.equal(model.normaliseAddonMode(true, 'double'), 'double');
  assert.equal(model.normaliseAddonMode(false, 'single'), 'single');
});

test('two mounting packs collapse to the dedicated pair variant', () => {
  const line = model.giftCartLine(
    { key: 'mounting', id: variants.mountingSingle, price: prices.mountingSingle },
    'double', variants, prices
  );
  assert.equal(line.id, variants.mountingPair);
  assert.equal(line.quantity, 1);
  assert.equal(line.linePrice, prices.mountingPair);
});

test('quantity multiplies both signs and both upgrades', () => {
  const items = build(baseState({
    quantity: 3,
    size: 'large',
    secondSign: true,
    secondLineOne: 'MR & MRS NICHOLS',
    secondSize: 'large'
  }));
  assert.ok(items.every((line) => line.quantity === 3));
});

test('total matches the sum of the line prices', () => {
  const state = baseState({
    size: 'large',
    secondSign: true,
    secondLineOne: 'MR & MRS NICHOLS',
    secondSize: 'medium'
  });
  const expected = prices.base + prices.large + prices.second + prices.medium;
  assert.equal(model.calculateTotal(state, variants, prices).current, expected);
  assert.equal(expected, 3618);
});

test('preview mirrors the number of signs being bought', () => {
  assert.equal(model.previewSigns(baseState()).length, 1);
  assert.equal(model.previewSigns(baseState({ secondSign: true })).length, 2);
});
