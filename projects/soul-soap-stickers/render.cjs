// Renders build/*.html (from build.py) to print PDFs and PNG previews, and
// checks that every text line fits its label: inside the 3 mm safe zone and
// no wider than the line's data-fit (mm).
//
//   node render.cjs            # PDFs + previews + fit check
//   node render.cjs --review   # also writes large per-label crops to build/review
const path = require('path');
const fs = require('fs');
let playwright;
try { playwright = require('playwright'); } catch { playwright = require('/opt/node22/lib/node_modules/playwright'); }

const HERE = __dirname;
const OUT = path.join(HERE, 'output');
const REVIEW = path.join(HERE, 'build', 'review');
const MM = 96 / 25.4;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await playwright.chromium.launch();

  // ---- fit check + PDF ----
  const page = await browser.newPage();
  await page.goto('file://' + path.join(HERE, 'build', 'print.html'));
  await page.evaluate(() => document.fonts.ready);
  const report = await page.evaluate((MM) => {
    const rows = [];
    for (const lab of document.querySelectorAll('[data-label]')) {
      const lr = lab.getBoundingClientRect();
      for (const el of lab.querySelectorAll('[data-fit]')) {
        const range = document.createRange();
        range.selectNodeContents(el);
        const r = range.getBoundingClientRect();
        const cs = getComputedStyle(el);
        const trail = parseFloat(cs.letterSpacing) || 0;   // trailing tracking after the last glyph
        const w = (r.width - trail) / MM;
        const left = (r.left - lr.left) / MM;
        const right = (lr.right - r.right + trail) / MM;
        const fit = parseFloat(el.dataset.fit);
        rows.push({ sheet: lab.closest('[data-sheet]').dataset.sheet, label: lab.dataset.label, text: el.textContent,
                    w: +w.toFixed(2), fit, left: +left.toFixed(2), right: +right.toFixed(2),
                    bad: w > fit + 0.01 || left < 2.99 || right < 2.99 });
      }
    }
    return rows;
  }, MM);
  const seen = new Set();
  let bad = 0;
  for (const r of report) {
    const id = r.label + '|' + r.text;
    if (seen.has(id)) continue;
    seen.add(id);
    if (r.bad) bad++;
    if (r.bad || process.argv.includes('--all')) {
      console.log(`${r.bad ? 'OVER' : 'ok  '} ${r.label.padEnd(20)} ${JSON.stringify(r.text).padEnd(28)} w=${r.w}mm fit=${r.fit} L=${r.left} R=${r.right}`);
    }
  }
  console.log(bad ? `${bad} line(s) break the safe zone or their fit width` : 'fit check: every line inside its label safe zone');

  // Where Chrome put each untracked line (baseline + centre, mm from its sheet's
  // top-left), so finish_pdf.py can prove the PDF text sits exactly there too.
  const layout = await page.evaluate((MM) => {
    const out = [];
    document.querySelectorAll('[data-sheet]').forEach((sheet, index) => {
      const sr = sheet.getBoundingClientRect();
      for (const el of sheet.querySelectorAll('[data-label] [data-fit]')) {
        if (parseFloat(getComputedStyle(el).letterSpacing) > 0) continue;   // tracked caps split into many PDF spans
        const range = document.createRange();
        range.selectNodeContents(el);
        const r = range.getBoundingClientRect();
        const mark = document.createElement('span');
        mark.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
        el.appendChild(mark);
        const base = mark.getBoundingClientRect().top;
        mark.remove();
        out.push({ sheet: index, text: el.textContent, baseline: (base - sr.top) / MM, centre: ((r.left + r.right) / 2 - sr.left) / MM });
      }
    });
    return out;
  }, MM);
  fs.writeFileSync(path.join(HERE, 'build', 'layout.json'), JSON.stringify(layout, null, 1));

  await page.pdf({ path: path.join(OUT, 'soul-soap-stickers-LP15-51SQ.pdf'), width: '210mm', height: '297mm', printBackground: true });

  // ---- previews ----
  const ctx = await browser.newContext({ deviceScaleFactor: 2 });
  const p2 = await ctx.newPage();
  await p2.setViewportSize({ width: 800, height: 1130 });
  await p2.goto('file://' + path.join(HERE, 'build', 'preview.html'));
  await p2.evaluate(() => document.fonts.ready);
  for (const key of ['everyday', 'mum']) {
    await p2.locator(`[data-sheet="${key}"]`).screenshot({ path: path.join(OUT, `preview-${key}.png`) });
  }

  if (process.argv.includes('--review')) {
    fs.mkdirSync(REVIEW, { recursive: true });
    const ctx6 = await browser.newContext({ deviceScaleFactor: 6 });
    const p6 = await ctx6.newPage();
    await p6.setViewportSize({ width: 800, height: 1130 });
    await p6.goto('file://' + path.join(HERE, 'build', 'preview.html'));
    await p6.evaluate(() => document.fonts.ready);
    const labels = await p6.$$('[data-label]');
    const done = new Set();
    for (const el of labels) {
      const key = await el.getAttribute('data-label');
      if (done.has(key)) continue;
      done.add(key);
      await el.screenshot({ path: path.join(REVIEW, `${key}.png`) });
    }
  }

  // ---- alignment test ----
  const pa = await browser.newPage();
  await pa.goto('file://' + path.join(HERE, 'build', 'alignment.html'));
  await pa.evaluate(() => document.fonts.ready);
  await pa.pdf({ path: path.join(OUT, 'alignment-test-LP15-51SQ.pdf'), width: '210mm', height: '297mm', printBackground: true });

  await browser.close();
  process.exit(bad ? 1 : 0);
})();
