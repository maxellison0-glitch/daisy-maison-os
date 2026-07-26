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

# ---- size profiles ----
# All three read their blank contour from source/size-contours.json.
# Large is the audited original and its numbers are unchanged. Medium is measured
# from the June-2026 production PSDs and its own cut file. Small is derived from
# the master shape inside the Medium cut file and validated against the 8-up
# production PSD - see the note on its entry.
PSD_PX_PER_MM=11.8719
LARGE_HEART_W=236/PSD_PX_PER_MM      # 19.879 mm, the source raster at PSD scale

SIZES={
 "large":{
   "label":"Large","blankW":570.0,"blankH":125.0,
   "border":12.4,"maxFs":59.0,"capCenterY":55.3,"targetW":486.0,
   "dateBaseline":104.0,"dateTargetW":470.0,"dateMaxFs":11.5,
   "heartTopMm":39.76,"heartW":LARGE_HEART_W,
   "signatureScaleX":None,                 # None = compute, preserving today's behaviour
   "contour":"large",                      # source/size-contours.json
   "source":"lARGE STREET SIGN PSD.psd + LARGE SIGN.lbrn2 contour",
   "status":"VISUAL APPROVED BY MAX 2026-07-14 - office production check required",
 },
 "medium":{
   # Blank 450x120 confirmed two ways: the cut file's XForm scales are exactly
   # 450/290 and 120/85, and solving the plate for a uniform frame inset gives
   # 120.05mm. The interior height is UNCHANGED from Large (100.2mm), so type
   # does not shrink - vertical constants shift by -2.5mm, they do not scale.
   "label":"Medium","blankW":450.0,"blankH":120.0,
   "border":9.9,"maxFs":59.0,"capCenterY":52.80,"targetW":383.7,
   "dateBaseline":103.4,"dateTargetW":371.1,"dateMaxFs":11.5,
   "heartTopMm":37.26,"heartW":LARGE_HEART_W,   # heart unchanged: interior height is unchanged
   "signatureScaleX":0.8644,                # pinned to Large's locked unit - see note below
   "contour":"medium",
   "source":"MIDDLE size  halfbed JUN26.lbrn2 contour + JUN26 production PSDs",
   "status":"DERIVED FROM MEASURED PSD - awaiting Max visual approval",
 },
 "small":{
   # Blank 290x85. There is no Small cut file and none is needed: the Medium
   # cut file's XForm is a NON-UNIFORM scale (1.55172, 1.41176) over local
   # geometry spanning exactly 290.000 x 85.000 mm, and 290*1.55172 = 450.0,
   # 85*1.41176 = 120.0. Medium was authored by scaling Small up, so the Small
   # contour is that master at unit scale - read from a real Daisy file, not
   # invented. See source/extract-size-contours.py.
   #
   # Confirmed against real production artwork (the 8-up Small bed PSD at 300
   # dpi): buffering the 290x85 master out by 1.00 mm reproduces the printed
   # silhouette to mean 0.182 mm, all 2750 sampled edge points within 1.0 mm.
   #
   # NOT the "MINI TRADITIONAL ROAD SIGN SHAPE" file - that is the Personalised
   # Traditional Road Sign, a different product with deliberately un-edged
   # corners (convex, area/hull 1.0000 against 0.9927 here). Max confirmed the
   # distinction on 2026-07-26.
   #
   # Unlike Medium, Small's 85 mm blank is SHORTER than Large's 100.2 mm
   # interior, so no inset can preserve the interior and the type genuinely must
   # shrink. Everything vertical therefore scales by 85/125 = 0.68, including
   # the heart - the agreed exception to the otherwise fixed-heart rule.
   # Type sizes are MEASURED off two real Small signs on the 8-up production bed,
   # not scaled. Both signs agreed to 0.1 mm, and the measurement is trustworthy
   # because it cross-checks: the plate reads 86.87 mm against an 85 mm blank,
   # i.e. 0.94 mm bleed per edge, matching the 1.00 mm found independently from
   # the contour. A pure 0.68 scale of Large would have made the caps 37.2 mm
   # when the real product is 40.13 - 8% small, and visibly so on a 85 mm sign.
   #
   # border and capCenterY are the 0.68-scaled values kept deliberately: the
   # measurement corroborates border (~8.6 mm) and matches capCenterY on one sign
   # but not the other (the ALL-COLOUR master stacks variants, and the two cells'
   # black layers sit 3 mm apart), so there is no sound basis to move it.
   "label":"Small","blankW":290.0,"blankH":85.0,
   "border":12.4*0.68,                      # 8.432 - measured ~8.6, kept
   "maxFs":43.29,                            # -> cap height 40.13 mm, measured
   "capCenterY":55.3*0.68,                  # 37.604 - unverified, see note
   "targetW":0.8914*(290.0-2*12.4*0.68),    # same fraction of the interior as Large
   "dateBaseline":69.7,                      # measured 69.50 / 69.93
   "dateTargetW":0.8621*(290.0-2*12.4*0.68),
   "dateMaxFs":7.54,                         # -> line-2 cap 6.99 mm, measured
   "heartTopMm":39.76*0.68,                 # 27.037
   "heartW":LARGE_HEART_W*0.68,             # 13.52 mm - Max approved
   "signatureScaleX":0.8644,                # pinned to Large's locked unit
   "contour":"small",
   "source":"MIDDLE size  halfbed JUN26.lbrn2 local master + 8-up Small production PSD",
   "status":"DERIVED AND VALIDATED AGAINST PRODUCTION ARTWORK - awaiting Max visual approval",
 },
}

# ---- args ----
argv=sys.argv[1:]
SIZE="large"
if "--size" in argv:
    i=argv.index("--size"); SIZE=argv[i+1].lower(); del argv[i:i+2]
if SIZE not in SIZES:
    raise SystemExit(f"Unknown --size {SIZE!r}. Choose from: {', '.join(SIZES)}")
P=SIZES[SIZE]

ORDER  = argv[0] if len(argv) > 0 else "TEST-001"
LINE1  = argv[1] if len(argv) > 1 else "MR & MRS WINDSOR"
LINE2  = argv[2] if len(argv) > 2 else "FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024"
TARGET_W = float(argv[3]) if len(argv) > 3 else P["targetW"]   # fit line-1 to this width
OUT    = argv[4] if len(argv) > 4 else os.path.join(HERE, f"mr-mrs-{SIZE}-preview.svg")

# ---- constants ----
BORDER=P["border"]; VSCALE=1.4; COLOR="#010101"; PANEL="#FFFFFF"
MAX_FS=P["maxFs"]           # production height; long names compress horizontally to TARGET_W
STROKE_FRAC=float(os.environ.get("STROKE_FRAC","0"))  # regular weight (no faux-bold) is the rule
CAP_CENTER_Y=P["capCenterY"]   # vertical centre of the name caps (mm), from real NASH at Large
DATE_BASELINE=P["dateBaseline"]; DATE_TARGET_W=P["dateTargetW"]; DATE_MAX_FS=P["dateMaxFs"]
HEART_W=float(os.environ.get("HW",str(P["heartW"])))
HEART_H=HEART_W*229/236.0
# The heart raster is 236px wide however large it is drawn, so its own pixel
# scale must be derived from the drawn width - using PSD_PX_PER_MM here would
# misplace a scaled heart by the scale ratio.
HEART_PX_PER_MM=236.0/HEART_W

# NICHOLS is Max's approved golden example. The ampersand and heart form one
# immutable signature unit: its proportions never change, and the heart's pointed
# red tip sits 3 source pixels inside the black upstroke's outer edge. Only the
# surrounding customer names compress to fit. At Mini the whole unit scales
# together, so the relationship is preserved even though the heart is smaller.
HEART_TOP_MM=P["heartTopMm"]
HEART_TIP_EDGE_INSET_PX=3
HEART_TIP_EDGE_INSET_MM=HEART_TIP_EDGE_INSET_PX/PSD_PX_PER_MM*(HEART_W/LARGE_HEART_W)

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# ---- source contour ----
# ONE file holds all three blank contours. source/source-data.js is retained as
# the audited original and is checked against by extract-size-contours.py, but it
# is deliberately not a second runtime source - two files that must agree are a
# bug waiting to happen.
SD = json.load(open(os.path.join(ROOT,"source","size-contours.json"),encoding="utf-8"))
if SIZE not in SD["sizes"]:
    raise SystemExit(f"{SIZE}: no contour in source/size-contours.json (has: {', '.join(SD['sizes'])})")
entry=SD["sizes"][SIZE]
pts=[(p["x"],p["y"]) for p in entry["contour"]["points"]]
if abs(entry["blankWidthMm"]-P["blankW"])>0.05 or abs(entry["blankHeightMm"]-P["blankH"])>0.05:
    raise SystemExit(f"{SIZE}: contour is {entry['blankWidthMm']}x{entry['blankHeightMm']}mm "
                     f"but the profile says {P['blankW']}x{P['blankH']} - refusing to mismatch.")
# The scalloped street sign sits at ~0.993. A convex 1.0000 outline is the
# Traditional Road Sign, a different product that must never be printed as this one.
if not (0.985 < entry["areaOverHull"] < 0.9985):
    raise SystemExit(f"{SIZE}: contour area/hull is {entry['areaOverHull']} - not the scalloped "
                     f"street-sign family. Refusing to print a different product's shape.")
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
CX=P["blankW"]/2.0

def fit(s,target,maxfs,measure=natw):
    width=measure(s)
    return maxfs if width == 0 else min(maxfs, target/width)
fs1=MAX_FS
HAS_HEART="&" in LINE1
heartManualReview=False
if HAS_HEART:
    prefix,suffix=LINE1.split("&",1)
    goldenLine="MR & MRS NICHOLS"
    # Pinned on the smaller sizes. Left to compute, a smaller TARGET_W silently
    # condenses the ampersand (0.8644 -> 0.6824 at Medium) while the heart keeps
    # its proportion - i.e. the signature unit would drift with size, which the
    # spec forbids. Pinning keeps the unit identical at every size.
    signatureScaleX=(P["signatureScaleX"] if P["signatureScaleX"] is not None
                     else min(1.0,TARGET_W/(natw(goldenLine)*fs1)))
    signatureAdvance=natw("&")*fs1*signatureScaleX
    surroundingNatural=(natw(prefix)+natw(suffix))*fs1
    available=max(1.0,TARGET_W-signatureAdvance)
    line1ScaleX=1.0 if surroundingNatural == 0 else min(1.0,available/surroundingNatural)
    prefixW=natw(prefix)*fs1*line1ScaleX
    suffixW=natw(suffix)*fs1*line1ScaleX
    w1=prefixW+signatureAdvance+suffixW
    lineStart=CX-w1/2
    ampOrigin=lineStart+prefixW
    suffixOrigin=ampOrigin+signatureAdvance
else:
    signatureScaleX=1.0
    naturalW1=natw(LINE1)*fs1
    line1ScaleX=1.0 if naturalW1 == 0 else min(1.0,TARGET_W/naturalW1)
    w1=naturalW1*line1ScaleX
fs2=fit(LINE2,DATE_TARGET_W,DATE_MAX_FS,natw); w2=natw(LINE2)*fs2
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
    # heartTipY is in HEART-image pixels, so it converts with the heart's own
    # scale; the ampersand mask is rendered at PSD_PX_PER_MM and converts with
    # that. Using one scale for both only works while the heart is unscaled.
    ampTipRow=round((heartY+heartTipY/HEART_PX_PER_MM-ampTopY)*PSD_PX_PER_MM)
    if not 0<=ampTipRow<amp_mask.shape[0]:
        raise RuntimeError("Unable to place heart: red-tip height misses the ampersand")
    stroke_pixels=np.flatnonzero(amp_mask[ampTipRow])
    if not len(stroke_pixels):
        raise RuntimeError("Unable to place heart: no black stroke exists at red-tip height")
    blackEdgeX=int(stroke_pixels.max())
    heartX=ampL+blackEdgeX/PSD_PX_PER_MM-heartTipX/HEART_PX_PER_MM-HEART_TIP_EDGE_INSET_MM
    heartManualReview=line1ScaleX<0.55

# ---- embed the real regular font subset for both lines + real heart raster ----
def subset_woff(font_path, text):
    opt=Options(); opt.flavor="woff"; opt.desubroutinize=True
    sub=TTFont(font_path); ss=Subsetter(options=opt)
    ss.populate(text="".join(sorted(set(text or " ")))); ss.subset(sub)
    buf=io.BytesIO(); sub.save(buf)
    return base64.b64encode(buf.getvalue()).decode()

regular_woff64=subset_woff(REGULAR_FONT_PATH,LINE1 + LINE2)
heart64=base64.b64encode(open(os.path.join(A,"heart.png"),"rb").read()).decode()
heart_el=(f'<image id="signature-heart" x="{heartX:.3f}" y="{heartY:.3f}" width="{hw:.3f}" '
          f'height="{hh:.3f}" xlink:href="data:image/png;base64,{heart64}" preserveAspectRatio="xMidYMid meet"/>') if HAS_HEART else ""

REGULAR_FAM="DaisyTimesRegular"
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
<!-- Daisy Maison - Mr & Mrs Street Sign {P["label"].upper()} {P["blankW"]:g}x{P["blankH"]:g}mm. -->
<!-- Regular Times on both lines, 1.4 vertical scale, real cut contour and heart raster. -->
<!-- Mounting holes are deliberately NOT drawn: they are physical holes cut in the acrylic, so printing rings around them puts ink on absent material. -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:daisy="https://daisymaison.co.uk/ns/production"
     width="{P["blankW"]:g}mm" height="{P["blankH"]:g}mm" viewBox="0 0 {P["blankW"]:g} {P["blankH"]:g}" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="ttl dsc">
  <title id="ttl">{esc(LINE1)} - {P["label"].lower()} street sign (preview)</title>
  <desc id="dsc">Faithful front-on reproduction from the production PSD.</desc>
  <defs><style>
    @font-face{{font-family:'{REGULAR_FAM}';font-weight:400;src:url(data:font/woff;base64,{regular_woff64}) format('woff');}}
  </style></defs>
  <metadata><daisy:production>
    <daisy:orderReference>{esc(ORDER)}</daisy:orderReference>
    <daisy:productHandle>mr-mrs-personalised-street-sign-gift</daisy:productHandle>
    <daisy:sku>36961</daisy:sku><daisy:size>{P["label"]}</daisy:size><daisy:physicalSize>{P["blankW"]:g} x {P["blankH"]:g} mm</daisy:physicalSize>
    <daisy:frameInsetMm>{BORDER:.3f}</daisy:frameInsetMm>
    <daisy:heartWidthMm>{HEART_W:.3f}</daisy:heartWidthMm>
    <daisy:font>Times New Roman regular on both lines (vertical scale 1.4)</daisy:font>
    <daisy:line1>{esc(LINE1)}</daisy:line1><daisy:line2>{esc(LINE2)}</daisy:line2>
    <daisy:line1FontSizeMm>{fs1:.2f}</daisy:line1FontSizeMm>
    <daisy:line1HorizontalScale>{line1ScaleX:.6f}</daisy:line1HorizontalScale>
    <daisy:signatureHorizontalScale>{signatureScaleX:.6f}</daisy:signatureHorizontalScale>
    <daisy:heartPlacementMethod>locked-nichols-signature-v1</daisy:heartPlacementMethod>
    <daisy:heartTipEdgeInsetPx>{HEART_TIP_EDGE_INSET_PX}</daisy:heartTipEdgeInsetPx>
    <daisy:heartManualReviewRequired>{str(heartManualReview).lower()}</daisy:heartManualReviewRequired>
    <daisy:source>{esc(P["source"])}</daisy:source>
    <daisy:status>{esc(P["status"])}</daisy:status>
    <daisy:generatedAt>{ts}</daisy:generatedAt>
  </daisy:production></metadata>
  <path id="outer-plate" d="{path(pts)}" fill="{COLOR}"/>
  <path id="inset-panel" d="{path(list(inner.exterior.coords))}" fill="{PANEL}"/>
  {line1_el}
  {heart_el}
  {text_g("line-2", LINE2, CX, DATE_BASELINE, fs2, REGULAR_FAM, 400)}
</svg>'''
open(OUT,"w",encoding="utf-8").write(svg)
print(f"{ORDER}: fs1={fs1:.2f} textScaleX={line1ScaleX:.4f} signatureScaleX={signatureScaleX:.4f} w1={w1:.1f}/{TARGET_W} cap1={cap1:.1f} base1={base1}")
print(f"  heart={'box@(%.1f,%.1f) %.1fx%.1f redTip=(%d,%d) blackEdge=%d inset=%dpx'%(heartX,heartY,hw,hh,heartTipX,heartTipY,blackEdgeX,HEART_TIP_EDGE_INSET_PX) if HAS_HEART else 'none'}")
if HAS_HEART and heartManualReview: print("  WARNING: line requires extreme horizontal compression; manual visual review required")
print(f"  fs2={fs2:.2f} w2={w2:.1f}  -> {OUT}")
