import base64
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright
FONT="/home/user/daisy-maison-os/Content Pipeline/Creative Studio/video/DM-C020-CORRECTION/fonts/TikTokSans-ExtraBold.woff2"
f64="data:font/woff2;base64,"+base64.b64encode(open(FONT,"rb").read()).decode()
html=f"""<!doctype html><html><head><meta charset=utf8><style>*{{margin:0;padding:0}}
@font-face{{font-family:'TTS';src:url({f64}) format('woff2');font-weight:800}}
html,body{{width:1080px;height:1920px;background:transparent}}
.w{{position:absolute;top:190px;left:0;right:0;text-align:center}}
.p{{display:inline-block;background:rgba(255,255,255,.94);border-radius:22px;padding:.24em .6em;
font-family:TTS;font-weight:800;font-size:78px;line-height:1.12;letter-spacing:-.01em;color:#0E0E0E;
box-shadow:0 4px 14px rgba(0,0,0,.16)}}
.k{{background:#6E1B2D;color:#fff;border-radius:999px;padding:0 .22em}}
</style></head><body><div class=w><div class=p>Mum &amp; Dad&rsquo;s house<br>never had a <span class=k>name</span></div></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920}); pg.set_content(html); pg.wait_for_timeout(400)
    box=pg.eval_on_selector(".p","e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}")
    print("pill box",box)
    pg.screenshot(path="pill.png",omit_background=True); b.close()
im=Image.open("t0.png").convert("RGB")
nh=round(1080*im.height/im.width); im=im.resize((1080,nh),Image.LANCZOS)
y0=1920-nh
# wall-matched pad: stretch the image's top row band upward, blurred, then feather the seam
band=im.crop((0,0,1080,40)).resize((1080,y0+40),Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
bg=Image.new("RGB",(1080,1920)); bg.paste(band,(0,0)); 
mask=Image.new("L",(1080,nh),255)
for y in range(60): 
    for_row=int(255*y/60); mask.paste(for_row,(0,y,1080,y+1))
bg.paste(im,(0,y0),mask)
o=Image.open("pill.png").convert("RGBA")
out=Image.alpha_composite(bg.convert("RGBA"),o).convert("RGB")
out.save("DM-FAMILY-COLLINS-916.jpg","JPEG",quality=93)
print(out.size,"image top",y0)
