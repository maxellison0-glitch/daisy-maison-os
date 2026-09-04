import { chromium } from 'playwright';

const ads = [
  { html: 'ad-01-headline.html',     out: 'ad-01-headline.png',     w: 1080, h: 1350 },
  { html: 'ad-02-wedding-table.html', out: 'ad-02-wedding-table.png', w: 1080, h: 1350 },
  { html: 'ad-03-dark-romance.html',  out: 'ad-03-dark-romance.png',  w: 1080, h: 1080 },
  { html: 'ad-04-flatlay.html',       out: 'ad-04-flatlay.png',       w: 1080, h: 1080 },
  { html: 'ad-05-luxury-price.html',  out: 'ad-05-luxury-price.png',  w: 1080, h: 1350 },
];

const dir = '/home/user/daisy-maison-os/projects/diffuser/ad-creatives';

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox'],
});

for (const ad of ads) {
  const page = await browser.newPage();
  await page.setViewportSize({ width: ad.w, height: ad.h });
  await page.goto(`file://${dir}/${ad.html}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: `${dir}/${ad.out}`, type: 'png' });
  console.log(`Rendered ${ad.out} (${ad.w}x${ad.h})`);
  await page.close();
}

await browser.close();
console.log('Done — all 5 ads rendered');
