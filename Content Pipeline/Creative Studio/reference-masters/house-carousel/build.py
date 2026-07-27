"""'Which one's your house?' — 5-slide TikTok photo carousel.

The engagement mechanic is the whole point: a number is the cheapest comment
anyone can leave, and comments are the strongest reach lever TikTok has. So
every slide carries its number, and slide 1 carries the ask.

Overlay treatment is the cream pill Max already approved on the diffuser
carousel, so it reads as the same account rather than a new look.
"""
import base64
import os
import subprocess
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = ("/home/user/daisy-maison-os/projects/diffuser/reel-pipeline/fonts/"
        "Fraunces-600.woff2")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

W, H = 1080, 1350
NUM_TOP = 74                 # clear of TikTok's own top UI, over wall not face
ASK_TOP = 1074               # below the sign, on her shirt, above TikTok's caption

SLIDES = [
    ("1-madhouse.png",  "1"),
    ("2-showhome.png",  "2"),
    ("3-dog.png",       "3"),
    ("4-lost.png",      "4"),
    ("5-quiet.png",     "5"),
]
ASK = "Which one&rsquo;s your house? \U0001F447"


def fit(path):
    """896x1200 source -> 1080x1350. Same crop the approved singles used."""
    im = Image.open(path).convert("RGB").crop((0, 40, 896, 1160))
    return im.resize((W, H), Image.LANCZOS)


def overlay(number, ask):
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    ask_el = ("<div class='row ask'><div class='pill wide'>%s</div></div>" % ASK
              if ask else "")
    html = f"""<!doctype html><meta charset=utf8><style>
@font-face{{font-family:'Fr';src:url(data:font/woff2;base64,{b64}) format('woff2');
  font-weight:600;font-display:block}}
*{{margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;background:transparent}}
.row{{position:absolute;left:0;width:{W}px;display:flex;justify-content:center}}
.num{{top:{NUM_TOP}px}}
.ask{{top:{ASK_TOP}px}}
.pill{{
  font-family:'Fr',Georgia,serif;font-weight:600;color:#4A3A2C;
  background:rgba(250,246,238,.94);border-radius:999px;white-space:nowrap;
  box-shadow:0 6px 22px rgba(30,25,20,.28);line-height:1;
}}
.num .pill{{font-size:56px;padding:26px 44px 30px;min-width:34px;text-align:center}}
.wide{{font-size:50px;padding:26px 48px 30px}}
</style>
<div class="row num"><div class="pill">{number}</div></div>{ask_el}"""
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
    out = os.path.join(HERE, "carousel")
    os.makedirs(out, exist_ok=True)
    for i, (fn, number) in enumerate(SLIDES, 1):
        base = fit(os.path.join(HERE, fn)).convert("RGBA")
        base.alpha_composite(overlay(number, ask=(i == 1)))
        p = os.path.join(out, "DM-house-%d.jpg" % i)
        base.convert("RGB").save(p, quality=95, subsampling=0)
        print("wrote", p)


if __name__ == "__main__":
    main()
