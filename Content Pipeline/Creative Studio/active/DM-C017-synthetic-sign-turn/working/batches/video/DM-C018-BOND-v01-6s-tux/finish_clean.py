#!/usr/bin/env python3
"""Clean finish: subtle cool grade only, NO burned text, NO music.
Delivers a caption-ready master + preview for native (CapCut / in-app) text.
The product surface is never touched."""
from pathlib import Path
import subprocess
import numpy as np, cv2, imageio_ffmpeg
from PIL import Image

BASE = Path(__file__).resolve().parent
RAW = BASE / "delivery" / "DM-C018-BOND-native-6s-raw.mp4"
DEL = BASE / "delivery"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 24

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
rad = np.sqrt(((xx-W/2)/(W*0.62))**2 + ((yy-H/2)/(H*0.62))**2)
vig = np.clip(1.0 - 0.14*np.clip(rad-0.55, 0, 1)/0.45, 0.86, 1.0)[..., None]

def grade(fr):
    f = fr.astype(np.float32)/255.0
    luma = (0.2126*f[...,2]+0.7152*f[...,1]+0.0722*f[...,0])[...,None]
    f = 0.5 + (f-0.5)*1.05                     # mild contrast
    shadow = np.clip(1.0 - luma*1.15, 0, 1)
    f[...,0] += 0.018*shadow[...,0]            # cool shadows (B, BGR)
    f[...,1] += 0.005*shadow[...,0]
    f[...,2] -= 0.009*shadow[...,0]
    f = f*0.986 + 0.011                        # faint lifted blacks
    return (np.clip(f,0,1)*255).astype(np.uint8)

def run():
    fd = DEL / "_frames_clean"; fd.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(RAW)); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        fr = grade(fr)
        fr = (fr.astype(np.float32)*vig).clip(0,255).astype(np.uint8)
        Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).save(fd / f"{i:05d}.png")
        i += 1
    cap.release()
    master = DEL / "DM-C018-BOND-CLEAN-master-1080x1920-24fps.mp4"
    subprocess.run([FFMPEG,"-y","-framerate",str(FPS),"-i",str(fd/'%05d.png'),
                    "-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p","-crf","17",
                    "-movflags","+faststart",str(master)], check=True, capture_output=True)
    preview = DEL / "DM-C018-BOND-CLEAN-phone-preview-720x1280.mp4"
    subprocess.run([FFMPEG,"-y","-i",str(master),"-vf","scale=720:1280",
                    "-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart",str(preview)],
                   check=True, capture_output=True)
    print("frames", i, "master", master.stat().st_size, "preview", preview.stat().st_size)
    return master, preview

if __name__ == "__main__":
    run()
