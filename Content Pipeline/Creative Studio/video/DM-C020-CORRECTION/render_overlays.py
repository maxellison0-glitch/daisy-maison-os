#!/usr/bin/env python3
"""Render transparent 1080x1920 caption overlays for DM-C020 The Correction.

Two styles, three placements, so Max can judge style and position separately.
Zero credits - this is local Chromium + the fonts in ./fonts.

  python3 render_overlays.py
"""
import pathlib, base64, asyncio
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE / "overlays"
OUT.mkdir(exist_ok=True)

CSS = (HERE / "overlay.html").read_text()

# The hook. Documentary register - the brand reporting a customer, not selling.
# The second sign is the punchline, so the hook must not give it away.
HOOK_A = ("same order.", "both signs.")
HOOK_B = ("we just print", "what they send")

def style_a(placement, l1, l2, key_second=True):
    second = f'<span class="key">{l2}</span>' if key_second else f'<span class="line">{l2}</span>'
    return f'''<div class="rail {placement} a">
      <span class="line">{l1}</span>
      {second}
    </div>'''

def style_b(placement, l1, l2):
    return f'''<div class="rail {placement} b">
      <span class="line">{l1}</span>
      <span class="rule"></span>
      <span class="line small">{l2}</span>
    </div>'''

JOBS = [
    # name                          builder   placement  copy
    ("A-native-top",        style_a, "top",   HOOK_A),
    ("A-native-upper",      style_a, "upper", HOOK_A),
    ("A-native-low",        style_a, "low",   HOOK_A),
    ("A-native-top-altcopy",style_a, "top",   HOOK_B),
    ("B-doc-top",           style_b, "top",   HOOK_B),
    ("B-doc-upper",         style_b, "upper", HOOK_B),
    ("B-doc-low",           style_b, "low",   HOOK_B),
    ("B-doc-top-altcopy",   style_b, "top",   HOOK_A),
]

async def main():
    async with async_playwright() as p:
        # The pinned playwright build here is newer than the browser on the
        # image, so point it at the chromium that actually exists.
        browser = await p.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        page = await browser.new_page(viewport={"width": 1080, "height": 1920},
                                      device_scale_factor=1)
        for name, builder, placement, (l1, l2) in JOBS:
            body = builder(placement, l1, l2)
            html = CSS.replace("<body></body>", f"<body>{body}</body>")
            (HERE / "_tmp.html").write_text(html)
            await page.goto((HERE / "_tmp.html").as_uri())
            await page.wait_for_timeout(350)          # let woff2 settle
            await page.screenshot(path=str(OUT / f"{name}.png"), omit_background=True)
            print("rendered", name)
        await browser.close()
    (HERE / "_tmp.html").unlink(missing_ok=True)

asyncio.run(main())
