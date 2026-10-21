import base64
from playwright.sync_api import sync_playwright
from PIL import Image
f=base64.b64encode(open("/home/user/daisy-maison-os/Content Pipeline/Creative Studio/video/DM-C020-CORRECTION/fonts/TikTokSans-ExtraBold.woff2","rb").read()).decode()
css="@font-face{font-family:TTS;src:url(data:font/woff2;base64,"+f+") format('woff2');font-weight:800}"
css+="*{margin:0;padding:0}html,body{width:1080px;height:1920px;background:transparent}"
css+=".l{position:absolute;left:80px;right:80px;top:@@TOP@@px;display:flex;flex-direction:column;align-items:center;gap:14px;font-family:TTS;font-weight:800}"
css+=".p{display:inline-block;white-space:nowrap;font-size:68px;line-height:1.12;letter-spacing:-.01em;padding:.24em .6em;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.16)}"
css+=".w{color:#0E0E0E;background:rgba(255,255,255,.94)}.b{color:#fff;background:#6E1B2D;font-size:54px}"
import sys
top=int(sys.argv[1])
html="<html><head><style>"+css.replace("@@TOP@@",str(top))+"</style></head><body><div class=l><span class='p w'>&ldquo;Just nipping to the shed&rdquo;</span><span class='p b'>&mdash; Dad, 3 hours ago</span></div></body></html>"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920}); pg.set_content(html); pg.evaluate("document.fonts.ready.then(()=>1)"); pg.wait_for_timeout(800); print(pg.evaluate("document.fonts.check(\"800 68px TTS\")"))
    pg.screenshot(path="hook.png",omit_background=True); b.close()
bg=Image.open("alan-shed2.png").convert("RGB").crop((0,20,1080,1940))
out=Image.alpha_composite(bg.convert("RGBA"),Image.open("hook.png").convert("RGBA")).convert("RGB")
out.save("DM-SHED-LAUGH-final.jpg","JPEG",quality=93,subsampling=0)
print(out.size)
