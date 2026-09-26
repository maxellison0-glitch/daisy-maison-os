# DM-SPOOKY-NEIGHBOURS-LAUGH: crop take C to a closer 9:16 phone framing, burn in the hook pill, save JPEG.
import base64
from playwright.sync_api import sync_playwright
from PIL import Image
F="/home/user/daisy-maison-os/Content Pipeline/Creative Studio/video/DM-C020-CORRECTION/fonts/TikTokSans-ExtraBold.woff2"
f64="data:font/woff2;base64,"+base64.b64encode(open(F,"rb").read()).decode()
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:'TT';src:url({f64}) format('woff2');font-weight:800}}
*{{margin:0;padding:0}} html,body{{width:1080px;height:1920px;background:transparent}}
.layer{{position:absolute;top:250px;left:80px;right:80px;text-align:center;white-space:nowrap}}
.pill{{display:inline-block;font-family:TT;font-weight:800;font-size:78px;line-height:1.24;letter-spacing:-0.01em;
color:#0E0E0E;background:rgba(255,255,255,0.94);padding:0.24em 0.60em;border-radius:22px;box-shadow:0 4px 14px rgba(0,0,0,0.16)}}
.kw{{color:#fff;background:#6E1B2D;padding:0.04em 0.28em;border-radius:999px}}
</style></head><body><div class=layer><span class=pill>New neighbours asked<br><span class=kw>what we're like</span></span></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path="pill.png",omit_background=True); b.close()
im=Image.open("take-C.png").convert("RGB").crop((333,640,1213,2204)).resize((1080,1920),Image.LANCZOS)
ov=Image.open("pill.png").convert("RGBA")
out=Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB")
out.save("DM-SPOOKY-NEIGHBOURS-final.jpg","JPEG",quality=92)
print(out.size)
