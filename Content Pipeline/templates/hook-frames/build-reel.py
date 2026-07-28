import base64, os, math, shutil
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

OUT="frames"; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
FPS=30
T_A=3.60; XF=0.45; T_TOTAL=6.80
B_START=T_A-XF                      # 3.15

# ---------- 1. captions: rounded light panel, clear text -------------------
def b64(p): return "data:font/woff2;base64,"+base64.b64encode(open("fonts/"+p,"rb").read()).decode()
FACES="@font-face{font-family:'Pop';src:url("+b64('Poppins-SemiBold.woff2')+") format('woff2');font-weight:600}"
def panel(lines, top=300, size=46):
    inner="<br>".join(lines)
    return ("<div style=\"position:absolute;top:%dpx;left:0;right:0;text-align:center\">"
            "<div style=\"display:inline-block;max-width:880px;"
            "background:rgba(247,242,233,.95);border-radius:34px;padding:30px 46px;"
            "box-shadow:0 10px 34px rgba(0,0,0,.30),0 2px 6px rgba(0,0,0,.16);"
            "font-family:Pop;font-weight:600;font-size:%dpx;line-height:1.34;color:#463629;"
            "letter-spacing:.002em\">%s</div></div>")%(top,size,inner)

HEAD=("<!doctype html><html><head><meta charset=utf8><style>*{margin:0;padding:0}"
      "html,body{width:1080px;height:1920px;background:transparent}"+FACES+"</style></head>"
      "<body><div style='position:relative;width:1080px;height:1920px'>")
CAPS={
 "c1":panel(["For the mate who says","&ldquo;honestly, don&rsquo;t get me anything&rdquo;"],top=300,size=44),
 "c2":panel(["Fine. Something with","their name on it, then."],top=300,size=48),
}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                        args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=1)
    for k,h in CAPS.items():
        pg.set_content(HEAD+h+"</div></body></html>"); pg.wait_for_timeout(280)
        pg.screenshot(path=f"cap_{k}.png",omit_background=True)
    b.close()
C1=Image.open("cap_c1.png").convert("RGBA"); C2=Image.open("cap_c2.png").convert("RGBA")

# ---------- 2. bases: 9:16 crop, PII softened ------------------------------
def crop916(path):
    im=Image.open(path).convert("RGB"); w,h=im.size; tw=int(h*9/16)
    return im.crop(((w-tw)//2,0,(w-tw)//2+tw,h))

A=crop916("base/box.jpg")          # 1296x2304
B=crop916("base/bottle.jpg")
SC=A.width/1080.0                  # scale from 1080-space coords to native

# soften the handwritten name on the gift tag (feathered, reads as shallow DOF)
x0,y0,x1,y1=[int(v*SC) for v in (168,952,558,1288)]
blur=A.filter(ImageFilter.GaussianBlur(int(13*SC)))
mask=Image.new("L",A.size,0)
ImageDraw.Draw(mask).rounded_rectangle([x0,y0,x1,y1],radius=int(26*SC),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(int(30*SC)))
A=Image.composite(blur,A,mask)
A.resize((540,960)).save("qc_pii.jpg",quality=92)

# ---------- 3. eased sub-pixel motion --------------------------------------
def ease(u): return u*u*(3-2*u)                     # smoothstep
def frame(base, u, z0, z1):
    W,H=base.size
    z=z0+(z1-z0)*ease(u)
    cw,ch=W/z,H/z
    l,t=(W-cw)/2.0,(H-ch)/2.0
    return base.resize((1080,1920),Image.LANCZOS,box=(l,t,l+cw,t+ch))

def alpha_at(t, fin0,fin1, fout0,fout1):
    if t<fin0 or t>fout1: return 0.0
    if t<fin1: return ease((t-fin0)/(fin1-fin0))
    if t<=fout0: return 1.0
    return 1.0-ease((t-fout0)/(fout1-fout0))

n=int(round(T_TOTAL*FPS))
for i in range(n):
    t=i/FPS
    fa=frame(A, min(t/T_A,1.0), 1.000, 1.055)
    if t>=B_START:
        ub=min((t-B_START)/(T_TOTAL-B_START),1.0)
        fb=frame(B, ub, 1.000, 1.050)
        if t<T_A:
            k=ease((t-B_START)/XF)
            f=Image.blend(fa,fb,k)
        else: f=fb
    else:
        f=fa
    f=f.convert("RGBA")
    a1=alpha_at(t,0.35,0.75,2.80,3.10)
    a2=alpha_at(t,3.80,4.20,6.55,6.80)
    for cap,a in ((C1,a1),(C2,a2)):
        if a>0.002:
            o=cap.copy()
            if a<0.999:
                al=o.getchannel("A").point(lambda v: int(v*a))
                o.putalpha(al)
            f=Image.alpha_composite(f,o)
    f.convert("RGB").save(f"{OUT}/f{i:04d}.jpg",quality=95,subsampling=1)
print("frames:",n)
