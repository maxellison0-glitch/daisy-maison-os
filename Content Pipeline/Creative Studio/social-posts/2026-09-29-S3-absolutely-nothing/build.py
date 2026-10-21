import base64
from PIL import Image
from playwright.sync_api import sync_playwright
FONT="/home/user/daisy-maison-os/Content Pipeline/Creative Studio/video/DM-C020-CORRECTION/fonts/TikTokSans-ExtraBold.woff2"
f64="data:font/woff2;base64,"+base64.b64encode(open(FONT,"rb").read()).decode()
# base plate: 1536x2752 -> 1080 wide, centre-crop to 1920
im=Image.open("gen2.png").convert("RGB")
h=round(im.height*1080/im.width); im=im.resize((1080,h),Image.LANCZOS)
off=(h-1920)//2; im=im.crop((0,off,1080,off+1920)); im.save("base.png")
html=f"""<!doctype html><html><head><meta charset=utf8><style>
*{{margin:0;padding:0}}
@font-face{{font-family:'TT';src:url({f64}) format('woff2');font-weight:800}}
html,body{{width:1080px;height:1920px;background:transparent}}
.layer{{position:absolute;top:200px;left:0;right:0;text-align:center}}
.pill{{display:inline-block;font-family:TT;font-weight:800;font-size:70px;line-height:1.12;
letter-spacing:-0.01em;color:#0E0E0E;background:rgba(255,255,255,0.94);padding:0.24em 0.60em;
border-radius:22px;white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,0.16)}}
</style></head><body><div class=layer><span class=pill>Mum asked for nothing<br>for her birthday</span></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920}); pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path="overlay.png",omit_background=True); b.close()
ov=Image.open("overlay.png").convert("RGBA")
out=Image.alpha_composite(Image.open("base.png").convert("RGBA"),ov).convert("RGB")
out.save("DM-ABSNOTHING-S3.jpg",quality=92,subsampling=0)
print(out.size)
