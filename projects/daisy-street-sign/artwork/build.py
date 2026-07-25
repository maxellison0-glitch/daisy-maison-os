#!/usr/bin/env python
"""
Canonical Daisy Maison large street-sign artwork generator.
  python build.py [order] [line1] [line2] [targetWidthMm]
Defaults to the TEST-001 / WINDSOR sample.

Ground truth (from D:\\sean\\max\\lARGE STREET SIGN PSD.psd, audited read-only):
  font  = Times New Roman regular (times.ttf), no faux bold, tracking 0, vertical scale 1.4
  subtitle = Times New Roman regular (times.ttf), tracking 0, vertical scale 1.4
  color = #010101 ; panel = white ; frame = uniform 12.4 mm inset of the real 409-vtx cut contour
  heart = the actual 236x229 raster from the PSD (assets/heart.png). Placement
          reproduces the approved NICHOLS relationship: the pointed bottom pixel
          of the red heart meets the outer edge of the rendered black upstroke.
"""
import json, base64, io, os, sys, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
A = os.path.join(HERE, "assets")
REGULAR_FONT_PATH = os.path.join(A, "times.ttf")
BOLD_FONT_PATH = os.path.join(A, "timesbd.ttf")

# ---- args ----
ORDER  = sys.argv[1] if len(sys.argv) > 1 else "TEST-001"
LINE1  = sys.argv[2] if len(sys.argv) > 2 else "MR & MRS WINDSOR"
LINE2  = sys.argv[3] if len(sys.argv) > 3 else "FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024"
TARGET_W = float(sys.argv[4]) if len(sys.argv) > 4 else 486.0   # fit line-1 to this width
OUT    = sys.argv[5] if len(sys.argv) > 5 else os.path.join(HERE, "mr-mrs-large-preview.svg")

# ---- constants from the PSD ----
BORDER=12.4; VSCALE=1.4
# Colourway is a product option: override per render without touching geometry.
# ---- REAL colourways, sampled from the live listing swatch (Mow-It-Swatch-Final).
# These are the ONLY colours the product is sold in. Do not invent others.
# Panel is the same warm cream across all five.
COLOURWAYS = {
    "BLACK": ("#000000", "#F2EEE3"),
    "GREY":  ("#7C7C7E", "#F2EEE3"),
    "SAGE":  ("#BEC0AA", "#F2EEE3"),
    "GRASS": ("#6E8F40", "#F2EEE3"),
    "BLUE":  ("#7A9EAA", "#F2EEE3"),
}
_cw = os.environ.get("SIGN_COLOURWAY")
if _cw:
    key = _cw.strip().upper()
    if key not in COLOURWAYS:
        raise SystemExit("Unknown colourway %r. Real options: %s"
                         % (_cw, ", ".join(COLOURWAYS)))
    COLOR, PANEL = COLOURWAYS[key]
else:
    # raw overrides kept for the legacy black-on-pure-white master
    COLOR=os.environ.get("SIGN_COLOR","#010101")   # frame + lettering
    PANEL=os.environ.get("SIGN_PANEL","#FFFFFF")   # inset panel
# The heart is the Mr & Mrs signature unit. It is applied automatically to any
# ampersand in line 1; set SIGN_HEART=0 for non-wedding wording such as BAR & GRILL.
HEART_ENABLED=os.environ.get("SIGN_HEART","1")!="0"
# The two mounting holes are real production geometry from the LightBurn cut file,
# so they stay ON by default and the cut path is unaffected either way. But they
# are a manufacturing feature, not a design one, and Max's call on 25 Jul 2026 is
# that they read as a laser-cutter artefact in content: "that's literally for the
# laser printer... if we had no holes and just a flat surface with the same
# borders, that's perfect." Set SIGN_HOLES=0 for any content render.
HOLES_ENABLED=os.environ.get("SIGN_HOLES","1")!="0"
# Short wordings render NARROWER than the plate because line1ScaleX was capped at
# min(1.0, ...) — it could only ever compress, never expand. Max, 25 Jul 2026, on
# MUM'S TAXI and THE SNUG: "the text, it doesn't stretch out very far. It's quite
# condensed. Usually we'd stretch out a bit more." SIGN_STRETCH lifts that cap so a
# short line expands to the target width. Off by default so production output is
# unchanged; STRETCH_MAX stops it turning into a caricature.
STRETCH=os.environ.get("SIGN_STRETCH","0")!="0"
STRETCH_MAX=float(os.environ.get("SIGN_STRETCH_MAX","1.6"))
# Line 2 weight. REGULAR IS THE ANSWER — do not turn this on.
# Tested properly on 25 Jul 2026: same terrace, same light, same pose, only line 2's
# weight changed. Max: "the bold makes the text way too big. I would definitely take
# it back to the non-bold for everything on line two."
# It also matches the real product: both live landing-page hero photos show line 2 in
# regular weight, same face as line 1, just smaller. Shipping regular while
# photographing bold would hand the customer something different from the picture.
# The flag survives only so the test is repeatable, and because making line 2 bold on
# the ACTUAL product would be a production change (new print files), not a content one.
LINE2_BOLD=os.environ.get("SIGN_LINE2_BOLD","0")!="0"
MAX_FS=59.0                 # production height; long names compress horizontally to TARGET_W
STROKE_FRAC=float(os.environ.get("STROKE_FRAC","0"))  # regular weight (no faux-bold) is the rule
CAP_CENTER_Y=55.3           # vertical centre of the name caps (mm), from real NASH
DATE_BASELINE=104.0; DATE_TARGET_W=470.0; DATE_MAX_FS=11.5   # real subtitle ~10.4mm caps
PSD_PX_PER_MM=11.8719
HEART_W=float(os.environ.get("HW",str(236/PSD_PX_PER_MM)))
HEART_H=HEART_W*229/236.0

# NICHOLS is Max's approved golden example. The ampersand and heart form one
# immutable signature unit: the heart stays at source size and its pointed red
# tip sits 3 source pixels inside the black upstroke's outer edge. Only the
# surrounding customer names compress to fit.
HEART_TOP_MM=39.76
HEART_TIP_EDGE_INSET_PX=3

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# ---- source contour ----
D = json.loads(open(os.path.join(ROOT,"source","source-data.js"),encoding="utf-8").read().split("=",1)[1].strip().rstrip(";"))
pts=[(p["x"],p["y"]) for p in D["lightBurn"]["contour"]["points"]]
holes=D["lightBurn"]["mountingHoles"]
poly=Polygon(pts); inner=poly.buffer(-BORDER, join_style="round", quad_segs=24)
inner=max(inner.geoms,key=lambda g:g.area) if inner.geom_type=="MultiPolygon" else inner
def path(seq): return "M "+" L ".join(f"{x:.3f},{y:.3f}" for x,y in seq)+" Z"

# ---- font metrics (real Times New Roman regular + bold) ----
f=TTFont(REGULAR_FONT_PATH); upem=f["head"].unitsPerEm
cmap=f.getBestCmap(); hmtx=f["hmtx"]; glyf=f["glyf"]; capH=f["OS/2"].sCapHeight/upem
_SPACE = hmtx["space"][0] if "space" in hmtx.metrics else upem//2
def natw(s):  # robust to arbitrary text: missing glyphs fall back to a space advance
    return sum((hmtx[cmap[ord(c)]][0] if ord(c) in cmap else _SPACE) for c in s)/upem
UNSUPPORTED=[c for c in dict.fromkeys(LINE1) if ord(c) not in cmap and not c.isspace()]
if UNSUPPORTED: print("WARNING: font has no glyph for", UNSUPPORTED, "- flag for manual review")
UNSUPPORTED_SUBTITLE=[c for c in dict.fromkeys(LINE2) if ord(c) not in cmap and not c.isspace()]
if UNSUPPORTED_SUBTITLE: print("WARNING: regular font has no glyph for", UNSUPPORTED_SUBTITLE, "- flag for manual review")
CX=285.0

fb=TTFont(BOLD_FONT_PATH) if os.environ.get("SIGN_LINE2_BOLD","0")!="0" else None
if fb is not None:
    _bupem=fb["head"].unitsPerEm; _bcmap=fb.getBestCmap(); _bhmtx=fb["hmtx"]
    _bspace=_bhmtx["space"][0] if "space" in _bhmtx.metrics else _bupem//2
    def natw_bold(t):
        return sum((_bhmtx[_bcmap[ord(c)]][0] if ord(c) in _bcmap else _bspace) for c in t)/_bupem
else:
    natw_bold=None

def xcap(v):
    """Horizontal scale cap. Compression is always allowed; expansion only when
    SIGN_STRETCH is on, and never past STRETCH_MAX."""
    return min(v, STRETCH_MAX) if STRETCH else min(v, 1.0)

def fit(s,target,maxfs,measure=natw):
    width=measure(s)
    return maxfs if width == 0 else min(maxfs, target/width)
fs1=MAX_FS
HAS_HEART=("&" in LINE1) and HEART_ENABLED
heartManualReview=False
if HAS_HEART:
    prefix,suffix=LINE1.split("&",1)
    goldenLine="MR & MRS NICHOLS"
    signatureScaleX=xcap(TARGET_W/(natw(goldenLine)*fs1))
    signatureAdvance=natw("&")*fs1*signatureScaleX
    surroundingNatural=(natw(prefix)+natw(suffix))*fs1
    available=max(1.0,TARGET_W-signatureAdvance)
    line1ScaleX=1.0 if surroundingNatural == 0 else xcap(available/surroundingNatural)
    prefixW=natw(prefix)*fs1*line1ScaleX
    suffixW=natw(suffix)*fs1*line1ScaleX
    w1=prefixW+signatureAdvance+suffixW
    lineStart=CX-w1/2
    ampOrigin=lineStart+prefixW
    suffixOrigin=ampOrigin+signatureAdvance
else:
    signatureScaleX=1.0
    naturalW1=natw(LINE1)*fs1
    line1ScaleX=1.0 if naturalW1 == 0 else xcap(TARGET_W/naturalW1)
    w1=naturalW1*line1ScaleX
_m2 = natw_bold if natw_bold is not None else natw
fs2=fit(LINE2,DATE_TARGET_W,DATE_MAX_FS,_m2)
line2ScaleX=1.0 if _m2(LINE2)*fs2 == 0 else xcap(DATE_TARGET_W/(_m2(LINE2)*fs2))
w2=_m2(LINE2)*fs2*line2ScaleX
cap1=capH*fs1*VSCALE; base1=round(CAP_CENTER_Y+cap1/2,3)

# ---- locked NICHOLS signature unit + rendered red-tip/black-edge placement ----
if HAS_HEART:
    g=glyf[cmap[ord("&")]]
    ampL=ampOrigin+g.xMin/upem*fs1*signatureScaleX
    ampW=(g.xMax-g.xMin)/upem*fs1*signatureScaleX
    ampTopY=base1-(g.yMax/upem*fs1*VSCALE); ampH=(g.yMax-g.yMin)/upem*fs1*VSCALE
    hw=HEART_W; hh=HEART_H

    def render_amp_mask():
        # Pillow renders the actual font outline; resizing to the analytic SVG
        # ink box keeps pixel analysis and emitted browser geometry in lockstep.
        pixel_size=max(32,round(fs1*PSD_PX_PER_MM))
        font=ImageFont.truetype(REGULAR_FONT_PATH,pixel_size)
        probe=Image.new("L",(pixel_size*3,pixel_size*3),0)
        draw=ImageDraw.Draw(probe)
        bbox=draw.textbbox((pixel_size,pixel_size),"&",font=font)
        draw.text((pixel_size-bbox[0],pixel_size-bbox[1]),"&",font=font,fill=255)
        rendered=probe.crop(probe.getbbox())
        target=(max(1,round(ampW*PSD_PX_PER_MM)),max(1,round(ampH*PSD_PX_PER_MM)))
        rendered=rendered.resize(target,Image.Resampling.LANCZOS)
        return np.asarray(rendered)>8

    heart_alpha=np.asarray(Image.open(os.path.join(A,"heart.png")).convert("RGBA").getchannel("A"))>8

    amp_mask=render_amp_mask()
    heart_rows,heart_cols=np.nonzero(heart_alpha)
    heartTipY=int(heart_rows.max())
    heartTipX=int(round(np.flatnonzero(heart_alpha[heartTipY]).mean()))
    heartY=HEART_TOP_MM
    ampTipRow=round((heartY+heartTipY/PSD_PX_PER_MM-ampTopY)*PSD_PX_PER_MM)
    if not 0<=ampTipRow<amp_mask.shape[0]:
        raise RuntimeError("Unable to place heart: red-tip height misses the ampersand")
    stroke_pixels=np.flatnonzero(amp_mask[ampTipRow])
    if not len(stroke_pixels):
        raise RuntimeError("Unable to place heart: no black stroke exists at red-tip height")
    blackEdgeX=int(stroke_pixels.max())
    heartX=ampL+(blackEdgeX-heartTipX-HEART_TIP_EDGE_INSET_PX)/PSD_PX_PER_MM
    heartManualReview=line1ScaleX<0.55

# ---- embed the real regular font subset for both lines + real heart raster ----
def subset_woff(font_path, text):
    opt=Options(); opt.flavor="woff"; opt.desubroutinize=True
    sub=TTFont(font_path); ss=Subsetter(options=opt)
    ss.populate(text="".join(sorted(set(text or " ")))); ss.subset(sub)
    buf=io.BytesIO(); sub.save(buf)
    return base64.b64encode(buf.getvalue()).decode()

regular_woff64=subset_woff(REGULAR_FONT_PATH,LINE1 + LINE2)
# Real Times New Roman Bold for line 2 when SIGN_LINE2_BOLD=1. A genuine bold face,
# not a stroke-widened fake — STROKE_FRAC stays at 0 and the rule against faux bold
# is intact.
bold_woff64=subset_woff(BOLD_FONT_PATH, LINE2) if LINE2_BOLD else None
BOLD_FAM="DaisyTimesBold"
heart64=base64.b64encode(open(os.path.join(A,"heart.png"),"rb").read()).decode()
holes_el=("\n  ".join(
    '<circle id="mounting-hole-%s" cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="0.4"/>'
    % (side, h["x"], h["y"], h["radius"], PANEL, COLOR)
    for side, h in (("left", holes[0]), ("right", holes[1]))) if HOLES_ENABLED else "")
heart_el=(f'<image id="signature-heart" x="{heartX:.3f}" y="{heartY:.3f}" width="{hw:.3f}" '
          f'height="{hh:.3f}" xlink:href="data:image/png;base64,{heart64}" preserveAspectRatio="xMidYMid meet"/>') if HAS_HEART else ""

REGULAR_FAM="DaisyTimesRegular"
bold_face_css=("@font-face{font-family:'%s';font-weight:700;src:url(data:font/woff;base64,%s) format('woff');}"
               % (BOLD_FAM, bold_woff64)) if LINE2_BOLD else ""
LINE2_FAM = BOLD_FAM if LINE2_BOLD else "DaisyTimesRegular"
LINE2_WEIGHT = 700 if LINE2_BOLD else 400
def text_g(id_, s, x, y, fs, family, weight, scale_x=1.0, anchor="middle"):
    sw=fs*STROKE_FRAC
    return (f'<g transform="translate({x} {y}) scale({scale_x:.6f} {VSCALE})">'
            f'<text id="{id_}" x="0" y="0" xml:space="preserve" font-family="\'{family}\',\'Times New Roman\',serif" font-weight="{weight}" '
            f'font-size="{fs:.3f}" fill="{COLOR}" stroke="{COLOR}" stroke-width="{sw:.3f}" '
            f'stroke-linejoin="round" text-anchor="{anchor}" style="letter-spacing:0">{esc(s)}</text></g>')

if HAS_HEART:
    line1_el=(f'<g id="line-1" data-text="{esc(LINE1)}">'
              f'{text_g("line-1-prefix",prefix,lineStart,base1,fs1,REGULAR_FAM,400,line1ScaleX,"start")}'
              f'{text_g("line-1-ampersand","&",ampOrigin,base1,fs1,REGULAR_FAM,400,signatureScaleX,"start")}'
              f'{text_g("line-1-suffix",suffix,suffixOrigin,base1,fs1,REGULAR_FAM,400,line1ScaleX,"start")}'
              f'</g>')
else:
    line1_el=text_g("line-1",LINE1,CX,base1,fs1,REGULAR_FAM,400,line1ScaleX)

ts=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
svg=f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Daisy Maison - Mr & Mrs Street Sign LARGE 570x125mm. VISUAL APPROVED, not print-ready. -->
<!-- Faithful reproduction from lARGE STREET SIGN PSD.psd: regular Times on both lines, 1.4 vertical scale, real cut contour and heart raster. -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:daisy="https://daisymaison.co.uk/ns/production"
     width="570mm" height="125mm" viewBox="0 0 570 125" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="ttl dsc">
  <title id="ttl">{esc(LINE1)} - large street sign (preview)</title>
  <desc id="dsc">Faithful front-on reproduction from the production PSD.</desc>
  <defs><style>
    @font-face{{font-family:'{REGULAR_FAM}';font-weight:400;src:url(data:font/woff;base64,{regular_woff64}) format('woff');}}{bold_face_css}
  </style></defs>
  <metadata><daisy:production>
    <daisy:orderReference>{esc(ORDER)}</daisy:orderReference>
    <daisy:productHandle>mr-mrs-personalised-street-sign-gift</daisy:productHandle>
    <daisy:sku>36961</daisy:sku><daisy:size>Large</daisy:size><daisy:physicalSize>570 x 125 mm</daisy:physicalSize>
    <daisy:font>Times New Roman regular on both lines (vertical scale 1.4)</daisy:font>
    <daisy:line1>{esc(LINE1)}</daisy:line1><daisy:line2>{esc(LINE2)}</daisy:line2>
    <daisy:line1FontSizeMm>{fs1:.2f}</daisy:line1FontSizeMm>
    <daisy:line1HorizontalScale>{line1ScaleX:.6f}</daisy:line1HorizontalScale>
    <daisy:signatureHorizontalScale>{signatureScaleX:.6f}</daisy:signatureHorizontalScale>
    <daisy:heartPlacementMethod>locked-nichols-signature-v1</daisy:heartPlacementMethod>
    <daisy:heartTipEdgeInsetPx>{HEART_TIP_EDGE_INSET_PX}</daisy:heartTipEdgeInsetPx>
    <daisy:heartManualReviewRequired>{str(heartManualReview).lower()}</daisy:heartManualReviewRequired>
    <daisy:source>lARGE STREET SIGN PSD.psd + LARGE SIGN.lbrn2 contour</daisy:source>
    <daisy:status>VISUAL APPROVED BY MAX 2026-07-14 - office production check required</daisy:status>
    <daisy:generatedAt>{ts}</daisy:generatedAt>
  </daisy:production></metadata>
  <path id="outer-plate" d="{path(pts)}" fill="{COLOR}"/>
  <path id="inset-panel" d="{path(list(inner.exterior.coords))}" fill="{PANEL}"/>
  {holes_el}
  {line1_el}
  {heart_el}
  {text_g("line-2", LINE2, CX, DATE_BASELINE, fs2, LINE2_FAM, LINE2_WEIGHT, line2ScaleX)}
</svg>'''
open(OUT,"w",encoding="utf-8").write(svg)
print(f"{ORDER}: fs1={fs1:.2f} textScaleX={line1ScaleX:.4f} signatureScaleX={signatureScaleX:.4f} w1={w1:.1f}/{TARGET_W} cap1={cap1:.1f} base1={base1}")
print(f"  heart={'box@(%.1f,%.1f) %.1fx%.1f redTip=(%d,%d) blackEdge=%d inset=%dpx'%(heartX,heartY,hw,hh,heartTipX,heartTipY,blackEdgeX,HEART_TIP_EDGE_INSET_PX) if HAS_HEART else 'none'}")
if HAS_HEART and heartManualReview: print("  WARNING: line requires extreme horizontal compression; manual visual review required")
print(f"  fs2={fs2:.2f} w2={w2:.1f}  -> {OUT}")
