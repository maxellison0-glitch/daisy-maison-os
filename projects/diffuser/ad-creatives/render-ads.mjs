import { chromium } from 'playwright';

const ads = [
  { html: 'ad-gift-table.html', out: 'ad-gift-table.png' },
  { html: 'ad-price-anchor.html', out: 'ad-price-anchor.png' },
  { html: 'ad-made-today.html', out: 'ad-made-today.png' },
];

const dir = '/home/user/daisy-maison-os/projects/diffuser/ad-creatives';

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox'],
});

for (const ad of ads) {
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 1350 });
  await page.goto(`file://${dir}/${ad.html}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${dir}/${ad.out}`, type: 'png' });
  console.log(`Rendered ${ad.out}`);
  await page.close();
}

await browser.close();
console.log('Done');
