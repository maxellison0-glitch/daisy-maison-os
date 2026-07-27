"""Diffuser reveal — a proper Instagram carousel.

Three slides at 1080x1350 (4:5, the tallest ratio the feed allows, so it takes
the most screen). The swipe is the reveal: closed box -> opened -> the bottle
standing. Match Law, bought without a video budget.

The hook treatment is Max's own pick from a five-way comparison: a cream pill
in Fraunces, which is also exactly the shape Instagram's own text tool makes,
so it reads as native rather than as a designer's overlay.

Zero credits. The photography already exists.
"""
import base64
import os
import subprocess
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/user/daisy-maison-os/projects/diffuser/reveal-carousel"
FONT = ("/home/user/daisy-maison-os/projects/diffuser/reel-pipeline/fonts/"
        "Fraunces-600.woff2")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

W, H = 1080, 1350          # 4:5
PILL_TOP = 196             # 14.5% down — over the bokeh on all three frames,
                           # clear of Instagram's header and well above the product
FONT_PX = 52

SLIDES = [
    ("01-closed-box.jpg",      "&ldquo;Don&rsquo;t get me anything.&rdquo;"),
    ("02-open-with-straw.jpg", "They always mean it."),
    ("03-bottle-standing.jpg", "Fine. Their name on it, then."),
]


def fit(path):
    """Scale to cover 1080x1350 and centre-crop. The source is 1856x2304
    (0.8056) against a 4:5 target (0.8000), so this trims ~4px a side and
    nothing in frame is lost."""
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def pill(text):
    """Render the cream pill as a transparent overlay."""
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    html = f"""<!doctype html><meta charset=utf8><style>
@font-face{{font-family:'Fr';src:url(data:font/woff2;base64,{b64}) format('woff2');
  font-weight:600;font-display:block}}
*{{margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;background:transparent}}
.row{{position:absolute;top:{PILL_TOP}px;left:0;width:{W}px;
  display:flex;justify-content:center}}
.pill{{
  font-family:'Fr',Georgia,serif;font-weight:600;font-size:{FONT_PX}px;
  line-height:1;color:#4A3A2C;white-space:nowrap;
  background:rgba(250,246,238,.94);border-radius:999px;
  padding:26px 52px 30px;
  box-shadow:0 6px 22px rgba(30,25,20,.28);
}}</style>
<div class="row"><div class="pill">{text}</div></div>"""
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "p.html"); op = os.path.join(td, "p.png")
        open(hp, "w").write(html)
        subprocess.run(
            [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--hide-scrollbars", "--default-background-color=00000000",
             "--force-device-scale-factor=1",
             # the usable viewport comes back ~87px shorter than the window,
             # so ask for slack and crop it off
             f"--window-size={W},{H + 260}", f"--screenshot={op}", "file://" + hp],
            check=True, capture_output=True)
        return Image.open(op).convert("RGBA").crop((0, 0, W, H))


def main():
    outs = []
    for i, (fn, text) in enumerate(SLIDES, 1):
        base = fit(os.path.join(SRC, fn)).convert("RGBA")
        base.alpha_composite(pill(text))
        out = os.path.join(HERE, "DM-diffuser-carousel-%d.jpg" % i)
        base.convert("RGB").save(out, quality=95, subsampling=0)
        outs.append(out)
        print("wrote", out)
    return outs


if __name__ == "__main__":
    main()
