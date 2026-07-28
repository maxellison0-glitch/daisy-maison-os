import json, base64
from playwright.sync_api import sync_playwright
BEATS = json.load(open("captions.json"))
def b64(p): return "data:font/woff2;base64,"+base64.b64encode(open(p,"rb").read()).decode()
F={"__TT800__":"fonts/TikTokSans-ExtraBold.woff2","__TT900__":"fonts/TikTokSans-Black.woff2","__POP__":"fonts/Poppins-SemiBold.woff2"}
CSS = """
@font-face{font-family:'TikTok Sans';src:url(__TT800__) format('woff2');font-weight:800;font-display:block}
@font-face{font-family:'TikTok Sans';src:url(__TT900__) format('woff2');font-weight:900;font-display:block}
@font-face{font-family:'Poppins';src:url(__POP__) format('woff2');font-weight:600;font-display:block}
:root{--ink:#0E0E0E;--paper:#fff;--pill-white:rgba(255,255,255,.94);--burgundy:#6E1B2D;
--caption-font:'TikTok Sans','Poppins',system-ui,sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent}
.stage{position:relative;width:1080px;height:1920px;font-family:var(--caption-font);-webkit-font-smoothing:antialiased}
.caption-layer{position:absolute;left:80px;right:80px;display:flex;flex-direction:column;align-items:center;text-align:center}
.pill{display:inline-block;font-weight:800;font-size:62px;line-height:1.14;letter-spacing:-.01em;color:var(--ink);
background:var(--pill-white);padding:.26em .58em;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.18);max-width:100%}
.pill.block{border-radius:36px}
.kw{color:var(--paper);background:var(--burgundy);padding:.06em .26em;border-radius:14px;
box-decoration-break:clone;-webkit-box-decoration-break:clone}
"""
for k,v in F.items(): CSS=CSS.replace(k,b64(v))
HTML="<!doctype html><html><head><meta charset=utf8><style>"+CSS+"</style></head><body><div class=stage>__L__</div></body></html>"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--force-color-profile=srgb","--no-sandbox"])
    pg=b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=1)
    for i,beat in enumerate(BEATS,1):
        y=beat.get("y",1180)
        layer='<div class="caption-layer" style="top:%dpx">%s</div>'%(y,beat["inner"])
        pg.set_content(HTML.replace("__L__",layer)); pg.wait_for_timeout(300)
        pg.screenshot(path="cap%d.png"%i, omit_background=True); print("cap%d.png"%i)
    b.close()
