"""'Type it -> make it real' ad builder. Configurator + CTA rendered locally (0 credits);
middle segment is an existing clip."""
import base64, os, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
W,H,FPS=1080,1920,24

WORD="PUSSY PALACE"
FIELD_LABEL="SIGN WORDING"
CLIP="/root/.claude/uploads/ca3fd967-4016-55c0-8aeb-b065a3c9b6fe/bb24b737-hf_20260520_082919_21a0fb65dcd4412895cf0cfa3f6b743d.mp4"
CLIP_USE=4.9
OUT="CAT-typereal.mp4"

def f64(p): return "data:font/woff2;base64,"+base64.b64encode(open("fonts/"+p,"rb").read()).decode()
FACES=("@font-face{font-family:'Fr';src:url("+f64('Fraunces-600.woff2')+") format('woff2');font-weight:600}"
 "@font-face{font-family:'Jo';src:url("+f64('Jost-400.woff2')+") format('woff2');font-weight:400}"
 "@font-face{font-family:'Jo';src:url("+f64('Jost-300.woff2')+") format('woff2');font-weight:300}")

# ---- sign plate rendered with the real Times, black-bordered like the cat sign ----
def plate(text, w=870, h=192):
    im=Image.new("RGB",(w,h),"#17171A"); d=ImageDraw.Draw(im)
    b=11
    d.rectangle([b,b,w-b-1,h-b-1],fill="#F7F4EC")
    n=26
    for (cx,cy,dx,dy) in [(0,0,1,1),(w,0,-1,1),(0,h,1,-1),(w,h,-1,-1)]:
        d.polygon([(cx,cy),(cx+dx*n,cy),(cx,cy+dy*n)],fill="#17171A")
    for x in (b+14,w-b-14):
        d.ellipse([x-3,h//2-3,x+3,h//2+3],fill="#17171A")
    if text:
        s=92
        while s>12:
            f=ImageFont.truetype("fonts/times.ttf",s)
            if d.textlength(text,font=f)<=w-2*b-56: break
            s-=2
        f=ImageFont.truetype("fonts/times.ttf",s)
        tw=d.textlength(text,font=f)
        d.text(((w-tw)/2,(h-s)/2-6),text,font=f,fill="#17171A")
    return im

def plate_b64(text):
    p=plate(text); p.save("_p.png")
    return "data:image/png;base64,"+base64.b64encode(open("_p.png","rb").read()).decode()

def configurator(typed, caret):
    c='<span style="opacity:%s">|</span>'%("1" if caret else "0")
    return f"""
    <div style="position:absolute;inset:0;background:linear-gradient(178deg,#F7F2EA 0%,#EFE7DB 100%)"></div>
    <div style="position:absolute;top:400px;left:0;right:0;text-align:center;
      font-family:Jo;font-weight:400;font-size:25px;letter-spacing:.42em;color:#93816C">DAISY MAISON</div>
    <div style="position:absolute;top:462px;left:0;right:0;text-align:center;
      font-family:Fr;font-weight:600;font-size:86px;color:#2B231C;letter-spacing:.002em">Make it theirs.</div>
    <div style="position:absolute;top:596px;left:0;right:0;text-align:center;
      font-family:Jo;font-weight:300;font-size:30px;color:#7E6C58">Personalise the sign as you order</div>
    <div style="position:absolute;top:730px;left:150px;right:150px">
      <div style="font-family:Jo;font-weight:400;font-size:19px;letter-spacing:.2em;color:#9A8973;margin-bottom:14px">{FIELD_LABEL}</div>
      <div style="background:#fff;border:2px solid #DCD0BE;border-radius:16px;padding:24px 26px;
        box-shadow:0 3px 14px rgba(90,70,50,.09);text-align:left;
        font-family:Jo;font-weight:400;font-size:40px;color:#2B231C;letter-spacing:.03em">{typed}{c}</div>
    </div>
    <div style="position:absolute;top:990px;left:0;right:0;text-align:center">
      <img src="{plate_b64(typed)}" style="width:870px;filter:drop-shadow(0 10px 26px rgba(60,45,30,.22))">
    </div>"""

def cta():
    return f"""
    <div style="position:absolute;inset:0;background:linear-gradient(178deg,#F7F2EA 0%,#EFE7DB 100%)"></div>
    <div style="position:absolute;top:790px;left:0;right:0;text-align:center;
      font-family:Jo;font-weight:400;font-size:26px;letter-spacing:.42em;color:#93816C">DAISY MAISON</div>
    <div style="position:absolute;top:864px;left:0;right:0;text-align:center">
      <div style="display:inline-block;background:#2B231C;border-radius:999px;padding:28px 64px;
        font-family:Jo;font-weight:400;font-size:40px;letter-spacing:.16em;color:#F7F2EA">ADD THEIR NAMES &nbsp;&rarr;</div></div>
    <div style="position:absolute;top:1010px;left:0;right:0;text-align:center;
      font-family:Jo;font-weight:300;font-size:28px;color:#8A7862;letter-spacing:.06em">daisymaison.co.uk</div>"""

def pill(text,top=300):
    return (f'<div style="position:absolute;top:{top}px;left:0;right:0;text-align:center">'
      f'<div style="display:inline-block;white-space:nowrap;background:rgba(250,246,238,.94);'
      f'border-radius:999px;padding:20px 44px;box-shadow:0 6px 22px rgba(20,18,15,.30);'
      f'font-family:Fr;font-weight:600;font-size:46px;color:#4A3A2C">{text}</div></div>')

HEAD=("<!doctype html><html><head><meta charset=utf8><style>*{margin:0;padding:0}"
 f"html,body{{width:{W}px;height:{H}px;background:transparent}}"+FACES+"</style></head>"
 f"<body><div style='position:relative;width:{W}px;height:{H}px;overflow:hidden'>")

shutil.rmtree("seg",ignore_errors=True); os.makedirs("seg")
states=[]
for i in range(len(WORD)+1):
    states.append(WORD[:i])

with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                        args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":W,"height":H},device_scale_factor=1)
    for i,s in enumerate(states):
        for cv in (0,1):
            pg.set_content(HEAD+configurator(s,cv)+"</div></body></html>"); pg.wait_for_timeout(90)
            pg.screenshot(path=f"seg/cfg_{i:02d}_{cv}.png")
    pg.set_content(HEAD+cta()+"</div></body></html>"); pg.wait_for_timeout(200)
    pg.screenshot(path="seg/cta.png")
    pg.set_content(HEAD+pill("Made for him.",300)+"</div></body></html>"); pg.wait_for_timeout(200)
    pg.screenshot(path="seg/pill.png",omit_background=True)
    b.close()
print("states rendered")

# ---- assemble configurator segment -----------------------------------------
os.makedirs("segA",exist_ok=True)
frames=[]
def hold(img,n): frames.extend([img]*n)
blink=lambda i,cv: f"seg/cfg_{i:02d}_{cv}.png"
hold(blink(0,1),9); hold(blink(0,0),9); hold(blink(0,1),6)     # ~1.0s empty, caret blinking
for i in range(1,len(states)):                                   # typing
    hold(blink(i,1),3)
hold(blink(len(states)-1,1),10); hold(blink(len(states)-1,0),8); hold(blink(len(states)-1,1),10)
for n,src in enumerate(frames):
    dst=f"segA/f{n:04d}.png"
    if not os.path.exists(dst): shutil.copy(src,dst)
print("segA frames",len(frames))
subprocess.run([FF,"-y","-loglevel","error","-framerate",str(FPS),"-i","segA/f%04d.png",
  "-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-vf",f"scale={W}:{H}","segA.mp4"],check=True)
# ---- cat segment: crop to 1080x1920, add pill ------------------------------
subprocess.run([FF,"-y","-loglevel","error","-t",str(CLIP_USE),"-i",CLIP,"-loop","1","-t",str(CLIP_USE),"-i","seg/pill.png",
  "-filter_complex",
  f"[0:v]crop={W}:{H}:0:(ih-{H})/2,setsar=1[v0];"
  f"[1:v]format=rgba,fade=t=in:st=0.55:d=0.30:alpha=1,fade=t=out:st=3.9:d=0.30:alpha=1[p];"
  f"[v0][p]overlay,format=yuv420p[v]",
  "-map","[v]","-r",str(FPS),"-c:v","libx264","-crf","16","-pix_fmt","yuv420p","segB.mp4"],check=True)
# ---- CTA segment -----------------------------------------------------------
subprocess.run([FF,"-y","-loglevel","error","-loop","1","-t","1.6","-i","seg/cta.png",
  "-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-r",str(FPS),"-vf",f"scale={W}:{H}","segC.mp4"],check=True)
# ---- concat with short crossfades -----------------------------------------
subprocess.run([FF,"-y","-loglevel","error","-i","segA.mp4","-i","segB.mp4","-i","segC.mp4",
  "-f","lavfi","-t","30","-i","anullsrc=channel_layout=stereo:sample_rate=44100",
  "-filter_complex",
  "[0:v][1:v]xfade=transition=fade:duration=0.25:offset=2.85[a];"
  "[a][2:v]xfade=transition=fade:duration=0.30:offset=7.30,format=yuv420p[v]",
  "-map","[v]","-map","3:a","-shortest",
  "-c:v","libx264","-preset","slow","-crf","18","-pix_fmt","yuv420p","-profile:v","high","-level","4.0",
  "-c:a","aac","-b:a","128k","-movflags","+faststart",OUT],check=True)
print("BUILT",OUT)
