#!/usr/bin/env python3
"""Render the on-screen hook pill for DM-THERMOSTAT-LAUGH (0 credits).
Spec: VIDEO_CAPTION_SYSTEM.md - TikTok Sans ExtraBold 78px, white pill, burgundy #6E1B2D keyword.
"""
import pathlib, asyncio
from playwright.async_api import async_playwright
HERE = pathlib.Path(__file__).parent
HTML = """<!doctype html><html><head><style>
@font-face{font-family:"TikTok Sans";src:url("TikTokSans-ExtraBold.woff2") format("woff2");font-weight:800;font-display:block}
html,body{margin:0;background:transparent}
.stage{position:relative;width:1080px;height:1920px;font-family:"TikTok Sans",sans-serif;-webkit-font-smoothing:antialiased}
.layer{position:absolute;left:80px;right:80px;top:1180px;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center}
.pill{display:inline-block;font-weight:800;font-size:78px;line-height:1.12;letter-spacing:-0.01em;color:#0E0E0E;
 background:rgba(255,255,255,0.94);padding:0.24em 0.60em;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,0.16);white-space:nowrap}
.kw{color:#fff;background:#6E1B2D;padding:0.12em 0.34em;border-radius:999px}
</style></head><body><div class="stage"><div class="layer">
<span class="pill">POV: you touched the</span>
<span class="pill"><span class="kw">heating</span> in September</span>
</div></div></body></html>"""
async def main():
    (HERE/"_pill.html").write_text(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto((HERE/"_pill.html").as_uri()); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(HERE/"hook-pill.png"), omit_background=True)
        await b.close()
    (HERE/"_pill.html").unlink()
asyncio.run(main())
