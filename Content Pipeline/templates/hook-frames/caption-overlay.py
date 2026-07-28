"""Overlay two-beat on-screen hooks onto an existing 9:16 clip. 0 credits.
Usage: python3 caption.py config.json"""
import base64, json, subprocess, sys, os
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()

def f64(p): return "data:font/woff2;base64,"+base64.b64encode(open("fonts/"+p,"rb").read()).decode()
FACES=("@font-face{font-family:'Fr';src:url("+f64('Fraunces-600.woff2')+") format('woff2');font-weight:600;font-style:normal}"
 "@font-face{font-family:'Fr';src:url("+f64('Fraunces-500i.woff2')+") format('woff2');font-weight:500;font-style:italic}"
 "@font-face{font-family:'TT';src:url("+f64('TikTokSans-ExtraBold.woff2')+") format('woff2');font-weight:800}")

def pill(text, top, size):
    """Style A - cream pill, Fraunces brown. Premium-native."""
    return ('<div style="position:absolute;top:%dpx;left:0;right:0;text-align:center">'
      '<div style="display:inline-block;white-space:nowrap;background:rgba(250,246,238,.94);'
      'border-radius:999px;padding:20px 44px;box-shadow:0 6px 22px rgba(30,25,20,.28);'
      'font-family:Fr;font-weight:600;font-size:%dpx;color:#4A3A2C;letter-spacing:.002em">%s</div></div>')%(top,size,text)

def bold(text, top, size):
    """Style B - house native white bold sans. Pure-native IG/TikTok."""
    return ('<div style="position:absolute;top:%dpx;left:64px;right:64px;text-align:center;'
      'font-family:TT;font-weight:800;font-size:%dpx;line-height:1.18;color:#fff;letter-spacing:-.004em;'
      'text-shadow:0 2px 6px rgba(0,0,0,.6),0 0 26px rgba(0,0,0,.42)">%s</div>')%(top,size,text)

STYLES={"pill":pill,"bold":bold}
HEAD=("<!doctype html><html><head><meta charset=utf8><style>*{margin:0;padding:0}"
 "html,body{width:1080px;height:1920px;background:transparent}"+FACES+"</style></head>"
 "<body><div style='position:relative;width:1080px;height:1920px'>")

def render_overlays(jobs):
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                            args=["--no-sandbox","--force-color-profile=srgb"])
        pg=b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=1)
        for out,html in jobs:
            pg.set_content(HEAD+html+"</div></body></html>"); pg.wait_for_timeout(300)
            pg.screenshot(path=out,omit_background=True)
        b.close()

def build(cfg):
    src=cfg["src"]; out=cfg["out"]; st=STYLES[cfg["style"]]
    dur=cfg["dur"]
    h=cfg["hook"]; pay=cfg["payoff"]
    top=cfg.get("top",300); size=cfg.get("size",50)
    o1,o2="_o1.png","_o2.png"
    render_overlays([(o1,st(h["text"],top,size)),(o2,st(pay["text"],top,size))])
    fc=(f"[1:v]format=rgba,fade=t=in:st={h['in']}:d=0.30:alpha=1,fade=t=out:st={h['out']}:d=0.28:alpha=1[c1];"
        f"[2:v]format=rgba,fade=t=in:st={pay['in']}:d=0.30:alpha=1,fade=t=out:st={pay['out']}:d=0.25:alpha=1[c2];"
        f"[0:v][c1]overlay[x];[x][c2]overlay,format=yuv420p[v]")
    cmd=[FF,"-y","-loglevel","error","-i",src,
         "-loop","1","-t",str(dur),"-i",o1,"-loop","1","-t",str(dur),"-i",o2,
         "-f","lavfi","-t",str(dur),"-i","anullsrc=channel_layout=stereo:sample_rate=44100",
         "-filter_complex",fc,"-map","[v]","-map","3:a",
         "-c:v","libx264","-preset","slow","-crf","18","-pix_fmt","yuv420p",
         "-profile:v","high","-level","4.0","-c:a","aac","-b:a","128k",
         "-movflags","+faststart",out]
    subprocess.run(cmd,check=True)
    print("built",out)

if __name__=="__main__":
    for cfg in json.load(open(sys.argv[1])): build(cfg)
