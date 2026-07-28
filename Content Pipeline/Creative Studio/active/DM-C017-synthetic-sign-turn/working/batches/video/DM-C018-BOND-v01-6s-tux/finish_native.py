#!/usr/bin/env python3
"""Automated 'native-looking' finish for the DM-C018 Bond turn.

Captions are rendered by a REAL browser (Chromium via Playwright) from HTML/CSS
with the real Raleway font + native-style treatment, screenshotted per frame
with transparency, then composited over a subtly-graded copy of the approved
native video, with an original synthetic reveal sting. The product surface is
never touched — text lives only in the top/bottom safe zones.
"""
from __future__ import annotations
import base64, subprocess, wave
from pathlib import Path
import numpy as np, cv2, imageio_ffmpeg
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
DEL = BASE / "delivery"
RAW = DEL / "DM-C018-BOND-native-6s-raw.mp4"
SCRATCH = Path("/tmp/claude-0/-home-user-daisy-maison-os/ca3fd967-4016-55c0-8aeb-b065a3c9b6fe/scratchpad")
FONT_B64 = (SCRATCH / "raleway-latin.b64").read_text().strip()
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CHROME = "/opt/pw-browsers/chromium"
W, H, FPS = 1080, 1920, 24

# ---------- 1. subtle cool grade + vignette ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_rad = np.sqrt(((xx-W/2)/(W*0.62))**2 + ((yy-H/2)/(H*0.62))**2)
VIG = np.clip(1.0 - 0.14*np.clip(_rad-0.55, 0, 1)/0.45, 0.86, 1.0)[..., None]

def grade(fr):
    f = fr.astype(np.float32)/255.0
    luma = (0.2126*f[...,2]+0.7152*f[...,1]+0.0722*f[...,0])[...,None]
    f = 0.5 + (f-0.5)*1.05
    sh = np.clip(1.0 - luma*1.15, 0, 1)
    f[...,0] += 0.017*sh[...,0]; f[...,1] += 0.005*sh[...,0]; f[...,2] -= 0.009*sh[...,0]
    f = f*0.986 + 0.011
    return (np.clip(f,0,1)*255).astype(np.uint8)

def grade_frames():
    gd = DEL / "_graded"; gd.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(RAW)); i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        fr = grade(fr); fr = (fr.astype(np.float32)*VIG).clip(0,255).astype(np.uint8)
        Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).save(gd / f"{i:05d}.png")
        i += 1
    cap.release(); return i

# ---------- 2. HTML caption stage (native look) ----------
HTML = """<!doctype html><html><head><meta charset='utf-8'><style>
@font-face{font-family:'Raleway';src:url(data:font/woff2;base64,__FONT__) format('woff2');font-weight:400 800;}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:'Raleway',sans-serif}
.cap{position:absolute;left:50%;transform:translateX(-50%);text-align:center;width:88%;opacity:0;will-change:opacity,transform}
.chip{display:inline-block;background:rgba(15,17,19,.36);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);
  border-radius:26px;padding:16px 30px;box-shadow:0 6px 26px rgba(0,0,0,.28)}
.hook{top:300px}
.hook .t{color:#fff;font-weight:700;font-size:60px;line-height:1.16;letter-spacing:.3px;
  text-shadow:0 2px 10px rgba(0,0,0,.5),0 1px 2px rgba(0,0,0,.5)}
.cta{top:1470px}
.cta .t{color:#fff;font-weight:700;font-size:64px;letter-spacing:.4px;text-shadow:0 2px 10px rgba(0,0,0,.5),0 1px 2px rgba(0,0,0,.5)}
.cta .arw{font-family:sans-serif;font-weight:700}
.cta .heart{color:#ff3b52;font-size:52px;vertical-align:-2px}
.cta .sub{display:block;margin-top:12px;color:#fff;font-weight:600;font-size:30px;letter-spacing:5px;
  text-shadow:0 1px 6px rgba(0,0,0,.55)}
</style></head><body>
<div class='cap hook' id='hook'><span class='chip'><span class='t'>Some surnames<br>deserve an entrance.</span></span></div>
<div class='cap cta' id='cta'><span class='chip'><span class='t'>Personalise yours <span class='arw'>&#8594;</span></span><span class='sub'>DAISYMAISON.CO.UK</span></span></div>
<script>
function easeOut(x){return 1-Math.pow(1-x,3)}
function easeIn(x){return x*x*x}
function win(t,a,inD,c,outD){ // fade-in at a, hold, fade-out ending at c
  if(t<a||t>c) return 0;
  if(t<a+inD) return easeOut((t-a)/inD);
  if(t>c-outD) return 1-easeIn((t-(c-outD))/outD);
  return 1;
}
function setEl(el,al){el.style.opacity=al; var y=(1-al)*18; var s=0.985+al*0.015;
  el.style.transform='translateX(-50%) translateY('+y+'px) scale('+s+')';}
window.setT=function(t){
  setEl(document.getElementById('hook'), win(t,0.30,0.42,2.90,0.40));
  setEl(document.getElementById('cta'),  win(t,4.55,0.42,6.10,0.001));
};
window.setT(0);
</script></body></html>"""

def render_captions(n):
    cd = DEL / "_caps"; cd.mkdir(exist_ok=True)
    html = HTML.replace("__FONT__", FONT_B64)
    (DEL / "_caption_stage.html").write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width":W,"height":H}, device_scale_factor=1)
        pg.set_content(html, wait_until="networkidle")
        pg.wait_for_timeout(200)
        for i in range(n):
            pg.evaluate(f"window.setT({i/FPS})")
            pg.screenshot(path=str(cd / f"{i:05d}.png"), omit_background=True)
        b.close()

# ---------- 3. original reveal sting ----------
def synth_audio(dur):
    sr=48000; N=int(dur*sr); t=np.linspace(0,dur,N,endpoint=False)
    def fade(x,a,b,c,d):
        if x<a or x>d: return 0.0
        if x<b: e=(x-a)/(b-a); return e*e*(3-2*e)
        if x<=c: return 1.0
        e=(x-c)/(d-c); return 1-e*e*(3-2*e)
    env=np.array([fade(x,4.0,4.5,5.6,6.1) for x in t])
    imp=np.array([fade(x,3.7,3.9,3.95,4.7) for x in t])
    who=np.array([fade(x,3.4,3.6,3.85,4.05) for x in t])
    rng=np.random.default_rng(7); noise=rng.standard_normal(N)
    lp=np.zeros(N); a=0.02
    for i in range(1,N): lp[i]=lp[i-1]+a*(noise[i]-lp[i-1])
    au=np.zeros(N)
    riser=np.clip(t/3.9,0,1)**2*(t<4.0)
    au+=0.15*lp*riser
    fsw=55+55*np.clip(t/3.9,0,1)
    au+=0.09*np.sin(2*np.pi*np.cumsum(fsw)/sr)*riser
    au+=0.5*np.sin(2*np.pi*58*t)*np.exp(-np.clip(t-3.88,0,None)*6)*(t>3.85)
    for fr,g in [(392,0.13),(523.25,0.11),(659.25,0.09)]:
        au+=g*np.sin(2*np.pi*fr*t)*np.exp(-np.clip(t-3.9,0,None)*7)*(t>3.88)
    au+=0.22*lp*who
    for fr,g in [(130.8,0.10),(196.0,0.09),(261.6,0.08),(329.6,0.06)]:
        au+=g*np.sin(2*np.pi*fr*t)*env
    au=np.tanh(au*1.1); au/=(np.max(np.abs(au))+1e-6); au*=0.72
    st=np.stack([au, np.concatenate([[0],au[:-1]])*0.6+au*0.4],axis=1)
    pcm=(st*32767).astype(np.int16)
    wp=DEL/"DM-C018-BOND-original-soundtrack.wav"
    with wave.open(str(wp),"wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
    return wp

# ---------- 4. composite + encode ----------
def encode(wp):
    g=str(DEL/"_graded"/"%05d.png"); c=str(DEL/"_caps"/"%05d.png")
    master=DEL/"DM-C018-BOND-master-1080x1920-24fps.mp4"
    subprocess.run([FFMPEG,"-y","-framerate",str(FPS),"-i",g,"-framerate",str(FPS),"-i",c,"-i",str(wp),
        "-filter_complex","[0:v][1:v]overlay=0:0:format=auto[v]","-map","[v]","-map","2:a",
        "-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p","-crf","18",
        "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(master)],
        check=True, capture_output=True)
    preview=DEL/"DM-C018-BOND-phone-preview-720x1280.mp4"
    subprocess.run([FFMPEG,"-y","-i",str(master),"-vf","scale=720:1280",
        "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-c:a","aac","-b:a","160k",
        "-movflags","+faststart",str(preview)], check=True, capture_output=True)
    return master, preview

if __name__ == "__main__":
    n = grade_frames(); print("graded", n)
    render_captions(n); print("captions rendered")
    wp = synth_audio(n/FPS); print("audio", wp.stat().st_size)
    m, pv = encode(wp)
    print("master", m.stat().st_size, "preview", pv.stat().st_size)
