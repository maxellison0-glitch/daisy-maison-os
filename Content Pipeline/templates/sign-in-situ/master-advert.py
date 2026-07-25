import base64, os, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
W,H,FPS=1080,1934,24
TRIM=0.65                      # drop the frames where the feather crosses the sign
CLIP="cat-toy.mp4"
OUT="CAT-ADVERT-master.mp4"

# ---------- 1. extract trimmed frames ----------
shutil.rmtree("fr",ignore_errors=True); os.makedirs("fr")
subprocess.run([FF,"-y","-loglevel","error","-ss",str(TRIM),"-i",CLIP,
                "-vf",f"fps={FPS}","fr/f%04d.png"],check=True)
frames=sorted(os.listdir("fr"))
N=len(frames); print("frames",N, "dur %.2fs"%(N/FPS))

# ---------- 2. lock the sign: composite the approved still's sign onto every frame ----
still=Image.open("still-1080.png").convert("RGB")
BOX=(214,516,866,696)                     # sign bbox + margin
mask=Image.new("L",(W,H),0)
ImageDraw.Draw(mask).rounded_rectangle(BOX,radius=10,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(9))   # feather so there is no seam

# ---------- 3. captions: native white bold, POV style ----------
def f64(p): return "data:font/woff2;base64,"+base64.b64encode(open("fonts/"+p,"rb").read()).decode()
FACES=("@font-face{font-family:'TT';src:url("+f64('TikTokSans-ExtraBold.woff2')+") format('woff2');font-weight:800}")
HEAD=("<!doctype html><html><head><meta charset=utf8><style>*{margin:0;padding:0}"
 f"html,body{{width:{W}px;height:{H}px;background:transparent}}"+FACES+"</style></head>"
 f"<body><div style='position:relative;width:{W}px;height:{H}px'>")
def native(t,top,size=60):
    return (f"<div style=\"position:absolute;top:{top}px;left:64px;right:64px;text-align:center;"
            f"font-family:TT;font-weight:800;font-size:{size}px;line-height:1.16;color:#fff;"
            f"letter-spacing:-.005em;text-shadow:0 2px 7px rgba(0,0,0,.62),0 0 30px rgba(0,0,0,.45)\">{t}</div>")
CAPS={"c1":native("POV: you thought<br>it was your house",210,58),
      "c2":native("It isn&rsquo;t.",250,72)}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                        args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":W,"height":H},device_scale_factor=1)
    for k,h in CAPS.items():
        pg.set_content(HEAD+h+"</div></body></html>"); pg.wait_for_timeout(260)
        pg.screenshot(path=f"cap_{k}.png",omit_background=True)
    # end card wordmark - PLACEHOLDER typeset in the sign's own Times
    pg.set_content(HEAD+
      "<div style=\"position:absolute;top:820px;left:0;right:0;text-align:center\">"
      "<div style=\"display:inline-block;background:rgba(250,247,241,.96);border-radius:6px;"
      "padding:26px 54px;box-shadow:0 14px 40px rgba(0,0,0,.34)\">"
      "<div style=\"font-family:Times,serif;font-size:56px;letter-spacing:.30em;color:#161616\">DAISY MAISON</div>"
      "<div style=\"font-family:Times,serif;font-size:23px;letter-spacing:.18em;color:#6A6A6A;margin-top:12px\">PERSONALISED STREET SIGNS</div>"
      "</div></div>"+"</div></body></html>")
    pg.wait_for_timeout(260); pg.screenshot(path="cap_logo.png",omit_background=True)
    b.close()
C1=Image.open("cap_c1.png").convert("RGBA")
C2=Image.open("cap_c2.png").convert("RGBA")
LG=Image.open("cap_logo.png").convert("RGBA")

def ease_out_quint(u): return 1-pow(1-u,5)
def win(t,a,b):
    if t<=a: return 0.0
    if t>=b: return 1.0
    return (t-a)/(b-a)

def maskup(layer, t, tin0,tin1, tout0,tout1, travel=34):
    """eased mask-reveal: text rises into place, then leaves downward"""
    if t<tin0 or t>tout1: return None
    if t<=tin1:
        p=ease_out_quint(win(t,tin0,tin1)); out=False
    elif t<tout0:
        p=1.0; out=False
    else:
        p=1-ease_out_quint(win(t,tout0,tout1)); out=True
    if p<=0.002: return None
    dy=int((1-p)*travel)*(1 if out else 1)
    l=layer.copy()
    if dy:
        l=Image.new("RGBA",layer.size,(0,0,0,0))
        l.paste(layer,(0,dy))
    if p<0.999:
        l.putalpha(l.getchannel("A").point(lambda v:int(v*p)))
    return l

CLIP_DUR=N/FPS
LOGO_HOLD=1.15
TOTAL=CLIP_DUR+LOGO_HOLD
last=None
shutil.rmtree("out",ignore_errors=True); os.makedirs("out")
n_out=int(round(TOTAL*FPS))
for i in range(n_out):
    t=i/FPS
    if i < N:
        base=Image.open(f"fr/{frames[i]}").convert("RGB")
        if base.size!=(W,H): base=base.resize((W,H),Image.LANCZOS)
        base=Image.composite(still,base,mask)          # <-- sign locked, 0px drift
        last=base
    else:
        base=last.copy()
    f=base.convert("RGBA")
    c1=maskup(C1,t,0.30,0.72,2.55,2.85)
    c2=maskup(C2,t,3.85,4.25,CLIP_DUR-0.30,CLIP_DUR-0.05)
    for L in (c1,c2):
        if L is not None: f=Image.alpha_composite(f,L)
    if t>=CLIP_DUR-0.15:
        u=win(t,CLIP_DUR-0.15,CLIP_DUR+0.42)
        p=ease_out_quint(u)
        dy=int((1-p)*-70)
        lg=Image.new("RGBA",(W,H),(0,0,0,0)); lg.paste(LG,(0,dy))
        lg.putalpha(lg.getchannel("A").point(lambda v:int(v*min(1.0,p*1.25))))
        f=Image.alpha_composite(f,lg)
    f.convert("RGB").save(f"out/o{i:04d}.jpg",quality=95,subsampling=1)
print("composited",n_out)
subprocess.run([FF,"-y","-loglevel","error","-framerate",str(FPS),"-i","out/o%04d.jpg",
  "-f","lavfi","-t",str(TOTAL),"-i","anullsrc=channel_layout=stereo:sample_rate=44100",
  "-c:v","libx264","-preset","slow","-crf","18","-pix_fmt","yuv420p","-profile:v","high","-level","4.0",
  "-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",OUT],check=True)
print("BUILT",OUT,"%.2fs"%TOTAL)
