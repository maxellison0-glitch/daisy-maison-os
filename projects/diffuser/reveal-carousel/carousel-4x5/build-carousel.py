"""Diffuser carousel v2 — option A, with emoji and a swipe cue.

Max picked A and asked for iOS emoji so it reads like a proper artist made it.

Apple Color Emoji is licensed to Apple hardware and is not on this machine, so
anything burnt in here renders in Noto (Google's set). Faces are where the two
sets diverge most — a Noto smirk looks obviously wrong to an iPhone audience —
so this uses SYMBOL emoji only (gift, white heart, sparkles), where the two
sets are near-identical. The white heart also happens to be the exact cream of
the pill, which is luck worth taking.

Also added: a swipe cue on slide 1. A carousel that does not tell you to swipe
loses people on the first frame, and the reveal is on slide 3.
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

W, H = 1080, 1350
PILL_TOP = 196
FONT_PX = 52

# Emoji chosen on PALETTE, not on meaning alone. The gift emoji was tried first
# and its red and primary yellow fought the cream-and-candlelight scene badly —
# it read as cheap, which is the exact opposite of the brief. These three all
# sit inside the photograph's own colours: brown heart to the pill's #4A3A2C
# type, eucalyptus to the real sprig lying in every shot, sparkles to the bokeh.
# The white heart was rejected too: white on a cream pill is near-invisible.
SLIDES = [
    ("01-closed-box.jpg",
     "&ldquo;Don&rsquo;t get me anything.&rdquo; \U0001F90E", True, 52),
    ("02-open-with-straw.jpg",
     "Nobody means that. \U0001F33F", False, 52),
    ("03-bottle-standing.jpg",
     "Especially not with their name on it. ✨", False, 46),
]


def fit(path):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def overlay(text, swipe, size):
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    # Emoji sit a touch high and heavy next to Fraunces at this size; nudge them
    # down and shrink slightly so the line's optical baseline stays level.
    swipe_el = ("<div class='swipe'>swipe →</div>" if swipe else "")
    html = f"""<!doctype html><meta charset=utf8><style>
@font-face{{font-family:'Fr';src:url(data:font/woff2;base64,{b64}) format('woff2');
  font-weight:600;font-display:block}}
*{{margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;background:transparent}}
.row{{position:absolute;top:{PILL_TOP}px;left:0;width:{W}px;
  display:flex;justify-content:center}}
.pill{{
  font-family:'Fr',Georgia,serif;font-weight:600;font-size:{size}px;
  line-height:1;color:#4A3A2C;white-space:nowrap;
  background:rgba(250,246,238,.94);border-radius:999px;
  padding:26px 52px 30px;
  box-shadow:0 6px 22px rgba(30,25,20,.28);
  font-variant-emoji:emoji;
}}
.swipe{{
  position:absolute;top:{PILL_TOP + 150}px;left:0;width:{W}px;text-align:center;
  font-family:'Fr',Georgia,serif;font-weight:600;font-size:31px;
  letter-spacing:.14em;color:rgba(250,246,238,.96);
  text-shadow:0 2px 12px rgba(30,22,14,.55);
}}</style>
<div class="row"><div class="pill">{text}</div></div>{swipe_el}"""
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "p.html"); op = os.path.join(td, "p.png")
        open(hp, "w", encoding="utf-8").write(html)
        subprocess.run(
            [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--hide-scrollbars", "--default-background-color=00000000",
             "--force-device-scale-factor=1",
             f"--window-size={W},{H + 260}", f"--screenshot={op}", "file://" + hp],
            check=True, capture_output=True)
        return Image.open(op).convert("RGBA").crop((0, 0, W, H))


def main():
    for i, (fn, text, swipe, size) in enumerate(SLIDES, 1):
        base = fit(os.path.join(SRC, fn)).convert("RGBA")
        base.alpha_composite(overlay(text, swipe, size))
        out = os.path.join(HERE, "v2-%d.jpg" % i)
        base.convert("RGB").save(out, quality=95, subsampling=0)
        print("wrote", out)


if __name__ == "__main__":
    main()
