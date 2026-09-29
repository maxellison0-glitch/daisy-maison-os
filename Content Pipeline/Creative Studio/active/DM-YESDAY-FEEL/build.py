"""DM-YESDAY-FEEL: burn the hook pill onto the chosen take, export 1080x1920 JPEG.
Pill spec: VIDEO_CAPTION_SYSTEM.md - TikTok Sans ExtraBold 78px, white block pill, ink text,
second line on the burgundy #6E1B2D pill. Bottom caption layer (top 1180px) so the pills sit
on her shirt, below the sign, clear of her face and the TikTok UI. Zero credits."""
import base64, glob, os
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "../../video/DM-C020-CORRECTION/fonts/TikTokSans-ExtraBold.woff2")
SRC = os.path.join(HERE, "take-02-chosen.png")
OUT = os.path.join(HERE, "DM-YESDAY-FEEL-final.jpg")
CHROME = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1]

ff = base64.b64encode(open(FONT, "rb").read()).decode()
HTML = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:TTS;src:url(data:font/woff2;base64,{ff}) format('woff2');font-weight:800}}
*{{margin:0;padding:0}} html,body{{width:1080px;height:1920px;background:transparent}}
.layer{{position:absolute;top:1180px;left:80px;right:80px;display:flex;flex-direction:column;align-items:center;gap:14px}}
.pill{{display:inline-block;font-family:TTS;font-weight:800;font-size:78px;line-height:1.12;letter-spacing:-.01em;text-align:center;
 color:#0E0E0E;background:rgba(255,255,255,.94);padding:.2em .55em;border-radius:22px;box-shadow:0 4px 14px rgba(0,0,0,.16)}}
.hl{{color:#fff;background:#6E1B2D;border-radius:999px}}
</style></head><body><div class=layer>
<div class=pill>Your best mate<br>just said yes.</div>
<div class="pill hl">Skip the card.</div>
</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(HERE, "overlay.png"), omit_background=True)
    b.close()

im = Image.open(SRC).convert("RGB")
w, h = im.size; th = int(w * 16 / 9)
im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th)).resize((1080, 1920), Image.LANCZOS)
ov = Image.open(os.path.join(HERE, "overlay.png")).convert("RGBA")
Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").save(OUT, "JPEG", quality=92)
os.remove(os.path.join(HERE, "overlay.png"))
print(OUT, Image.open(OUT).size, os.path.getsize(OUT))
