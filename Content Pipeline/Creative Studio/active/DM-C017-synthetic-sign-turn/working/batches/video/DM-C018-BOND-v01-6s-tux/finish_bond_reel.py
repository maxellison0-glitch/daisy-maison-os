#!/usr/bin/env python3
"""Finish the DM-C018 Bond native turn WITHOUT touching the product surface.

Allowed finishing only: top hook typography, bottom CTA typography, an original
synthetic reveal sting, a subtle cool grade, and H.264/AAC encode + delivery
scaling. The exact sign is never overlaid, tracked or replaced.
"""
from __future__ import annotations
import os, subprocess, wave, math
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

BASE = Path(__file__).resolve().parent
RAW = BASE / "delivery" / "DM-C018-BOND-native-6s-raw.mp4"
DEL = BASE / "delivery"
FONT = Path("/tmp/claude-0/-home-user-daisy-maison-os/ca3fd967-4016-55c0-8aeb-b065a3c9b6fe/scratchpad/Raleway-latin.ttf")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H, FPS = 1080, 1920, 24
INK = (35, 35, 35)
PAPER = (251, 249, 245)
PUTTY = (176, 175, 155)

HOOK = "Some surnames deserve an entrance."
CTA = "Personalise yours"
HANDLE = "DAISYMAISON.CO.UK"

def font(weight, size):
    f = ImageFont.truetype(str(FONT), size)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

def make_pill(lines, weights, sizes, sub=None, arrow=False, pad_x=54, pad_y=30, gap=10, radius=34):
    """Render a soft off-white rounded pill with centered Raleway lines on RGBA."""
    fonts = [font(w, s) for w, s in zip(weights, sizes)]
    tmp = Image.new("RGBA", (10, 10)); td = ImageDraw.Draw(tmp)
    widths, heights = [], []
    for ln, f in zip(lines, fonts):
        b = td.textbbox((0, 0), ln, font=f); widths.append(b[2]-b[0]); heights.append(b[3]-b[1])
    arrow_w = int(sizes[0]*0.9) if arrow else 0
    subfont = font(600, int(sizes[0]*0.42)) if sub else None
    subh = 0; subw = 0
    if sub:
        b = td.textbbox((0,0), sub, font=subfont); subw = b[2]-b[0]; subh = (b[3]-b[1]) + 14
    content_w = max([widths[0] + arrow_w + (18 if arrow else 0)] + widths[1:] + ([subw] if sub else []))
    content_h = sum(heights) + gap*(len(lines)-1) + subh
    pw, ph = content_w + pad_x*2, content_h + pad_y*2
    # shadow canvas
    canvas = Image.new("RGBA", (pw+48, ph+48), (0,0,0,0))
    sh = Image.new("RGBA", canvas.size, (0,0,0,0)); sd = ImageDraw.Draw(sh)
    rounded(sd, (28, 34, 28+pw, 34+ph), radius, (20,20,20,90))
    canvas = Image.alpha_composite(canvas, sh.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(14)))
    d = ImageDraw.Draw(canvas)
    x0, y0 = 24, 24
    rounded(d, (x0, y0, x0+pw, y0+ph), radius, PAPER+(244,))
    d.rounded_rectangle((x0, y0, x0+pw, y0+ph), radius=radius, outline=PUTTY+(150,), width=2)
    cy = y0 + pad_y
    for i, (ln, f, h) in enumerate(zip(lines, fonts, heights)):
        b = d.textbbox((0,0), ln, font=f)
        lw = b[2]-b[0]
        total = lw + (arrow_w+18 if (arrow and i==0) else 0)
        lx = x0 + (pw-total)//2
        d.text((lx - b[0], cy - b[1]), ln, font=f, fill=INK+(255,))
        if arrow and i == 0:
            ax = lx + lw + 18; ah = sizes[0]*0.5; acy = cy + h/2
            # draw a clean right arrow
            d.line([(ax, acy), (ax+arrow_w*0.72, acy)], fill=INK+(255,), width=max(4,int(sizes[0]*0.07)))
            d.polygon([(ax+arrow_w*0.62, acy-ah*0.34),(ax+arrow_w*0.95, acy),(ax+arrow_w*0.62, acy+ah*0.34)], fill=INK+(255,))
        cy += h + gap
    if sub:
        b = d.textbbox((0,0), sub, font=subfont); sw = b[2]-b[0]
        sx = x0 + (pw-sw)//2
        d.text((sx - b[0], cy + 2 - b[1]), sub, font=subfont, fill=PUTTY+(255,))
    return canvas

def smoothstep(x): x = min(1.0, max(0.0, x)); return x*x*(3-2*x)
def fade(t, a, b, c, d):
    if t < a or t > d: return 0.0
    if t < b: return smoothstep((t-a)/(b-a))
    if t <= c: return 1.0
    return 1.0 - smoothstep((t-c)/(d-c))

def grade(frame):
    f = frame.astype(np.float32)/255.0
    luma = (0.2126*f[...,2] + 0.7152*f[...,1] + 0.0722*f[...,0])[...,None]
    # mild contrast around 0.5
    f = 0.5 + (f-0.5)*1.055
    # cool shadows (cinematic), protect highlights
    shadow = np.clip(1.0 - luma*1.15, 0, 1)
    f[...,0] += 0.020*shadow[...,0]   # B (BGR)
    f[...,1] += 0.006*shadow[...,0]   # G
    f[...,2] -= 0.010*shadow[...,0]   # R
    # tiny lifted blacks
    f = f*0.985 + 0.012
    f = np.clip(f, 0, 1)
    return (f*255).astype(np.uint8)

# subtle vignette mask
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = W/2, H/2
rad = np.sqrt(((xx-cx)/(W*0.62))**2 + ((yy-cy)/(H*0.62))**2)
vig = np.clip(1.0 - 0.16*np.clip(rad-0.55, 0, 1)/0.45, 0.84, 1.0)[...,None]

def compose():
    hook = make_pill([HOOK], [700], [58], radius=30)
    cta = make_pill([CTA], [600], [62], sub=HANDLE, arrow=True, radius=999)
    frames_dir = DEL / "_frames"; frames_dir.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(RAW)); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(n):
        ok, fr = cap.read()
        if not ok: break
        t = i/FPS
        fr = grade(fr)
        fr = (fr.astype(np.float32)*vig).clip(0,255).astype(np.uint8)
        img = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).convert("RGBA")
        # hook top ~0.25-2.9s
        ah = fade(t, 0.25, 0.7, 2.4, 2.9)
        if ah > 0:
            ov = hook.copy(); a = ov.split()[3].point(lambda p: int(p*ah)); ov.putalpha(a)
            img.alpha_composite(ov, (W//2 - ov.width//2, 300))
        # cta bottom ~4.5-6.0s
        ac = fade(t, 4.5, 4.9, 5.9, 6.1)
        if ac > 0:
            ov = cta.copy(); a = ov.split()[3].point(lambda p: int(p*ac)); ov.putalpha(a)
            img.alpha_composite(ov, (W//2 - ov.width//2, 1470))
        img.convert("RGB").save(frames_dir / f"{i:05d}.png")
    cap.release()
    return n

def synth_audio(dur):
    sr = 48000; N = int(dur*sr); t = np.linspace(0, dur, N, endpoint=False)
    def env(a, b, c, d):
        e = np.zeros_like(t)
        for i, x in enumerate(t):
            e[i] = fade(x, a, b, c, d)
        return e
    rng = np.random.default_rng(1)
    audio = np.zeros(N)
    # tension riser 0 -> 3.9 (filtered noise + low rising sine)
    riser_env = np.clip((t/3.9), 0, 1)**2 * (t < 4.0)
    noise = rng.standard_normal(N)
    # simple one-pole lowpass on noise
    lp = np.zeros(N); a = 0.02
    for i in range(1, N): lp[i] = lp[i-1] + a*(noise[i]-lp[i-1])
    audio += 0.16*lp*riser_env
    f_sweep = 55 + 55*np.clip(t/3.9, 0, 1)
    audio += 0.10*np.sin(2*np.pi*np.cumsum(f_sweep)/sr) * riser_env
    # impact ~3.85s: boom + bright stab + whoosh
    imp = env(3.7, 3.9, 3.95, 4.7)
    boom = np.sin(2*np.pi*58*t) * np.exp(-np.clip(t-3.88,0,None)*6) * (t>3.85)
    audio += 0.5*boom
    for fr, g in [(392,0.14),(523.25,0.12),(659.25,0.10)]:  # G4/C5/E5 bright stab
        audio += g*np.sin(2*np.pi*fr*t)*np.exp(-np.clip(t-3.9,0,None)*7)*(t>3.88)
    whoosh = lp * env(3.4, 3.6, 3.85, 4.05); audio += 0.22*whoosh
    # warm resolve pad 4.0-6.0 (C major)
    pad = env(4.0, 4.5, 5.6, 6.1)
    for fr, g in [(130.8,0.10),(196.0,0.09),(261.6,0.08),(329.6,0.06)]:
        audio += g*np.sin(2*np.pi*fr*t)*pad
    # gentle master
    audio = np.tanh(audio*1.1)
    audio /= (np.max(np.abs(audio))+1e-6); audio *= 0.72
    # subtle stereo width
    left = audio.copy(); right = np.concatenate([[0], audio[:-1]])*0.6 + audio*0.4
    stereo = np.stack([left, right], axis=1)
    pcm = (stereo*32767).astype(np.int16)
    wavp = DEL / "DM-C018-BOND-original-soundtrack.wav"
    with wave.open(str(wavp), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
    return wavp

def encode(n, wavp):
    frames = str(DEL / "_frames" / "%05d.png")
    master = DEL / "DM-C018-BOND-master-1080x1920-24fps.mp4"
    subprocess.run([FFMPEG, "-y", "-framerate", str(FPS), "-i", frames, "-i", str(wavp),
                    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(master)],
                   check=True, capture_output=True)
    preview = DEL / "DM-C018-BOND-phone-preview-720x1280.mp4"
    subprocess.run([FFMPEG, "-y", "-i", str(master), "-vf", "scale=720:1280",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(preview)],
                   check=True, capture_output=True)
    return master, preview

if __name__ == "__main__":
    n = compose()
    dur = n/FPS
    wavp = synth_audio(dur)
    master, preview = encode(n, wavp)
    print("frames:", n, "dur:", round(dur,3))
    print("master:", master, master.stat().st_size, "bytes")
    print("preview:", preview, preview.stat().st_size, "bytes")
    print("soundtrack:", wavp, wavp.stat().st_size, "bytes")
