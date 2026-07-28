#!/usr/bin/env python3
"""
Daisy Maison wordmark — refined lockup, rendered to a transparent PNG.

Provenance and honesty note
---------------------------
There is still no supplied Daisy Maison logo file anywhere in the repo. The
first version of this lockup was typeset from scratch to fill that gap, and Max
called it "quite nice… we could probably make that even nicer with some more
thought." This is that second pass. It remains a house-built wordmark, not a
delivered brand asset — if a real logo arrives, this is replaced, not defended.

What changed from v1, and why
-----------------------------
v1 was a hard pure-white rectangle with both lines set at the same wide
tracking, the descriptor in neutral grey.

  * warm cream, not white. Pure #FFF on a warm daylit wall reads as a UI
    element pasted on top. #FAF6EE is the same cream as the sign panel, so the
    lockup belongs to the product rather than to the app.
  * hairline rule between the two lines. It does the work the extra letter-
    spacing was doing badly — separating name from descriptor — and it echoes
    the sign's own printed border.
  * differentiated tracking. The name is the voice, the descriptor is the
    footnote: 0.22em against 0.34em, so they read as a hierarchy rather than
    two versions of the same thing.
  * warm brown descriptor (#4A3F35), not grey. Grey is a browser default; brown
    is a decision, and it ties to the Fraunces brown already in house captions.
  * a soft directional shadow and a 3px radius. Barely-there, but it seats the
    panel on the wall instead of floating it.
  * real padding. The cheapest way to look expensive is space.
"""

import base64, os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CREAM = "#FAF6EE"
BROWN = "#4A3F35"
INK = "#1A1613"


def wordmark_html(w, h, name_px, desc_px, pad_x, pad_y):
    return f"""<!doctype html><meta charset=utf8>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:{w}px;height:{h}px;background:transparent}}
  .wrap{{width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center}}
  .panel{{
    background:{CREAM};
    padding:{pad_y}px {pad_x}px;
    border-radius:3px;
    box-shadow:0 {max(2,int(h*0.02))}px {max(8,int(h*0.09))}px rgba(40,32,24,.20),
               0 1px 2px rgba(40,32,24,.10);
    text-align:center;
  }}
  .name{{
    font-family:'Times New Roman',Times,serif;
    font-size:{name_px}px; line-height:1;
    letter-spacing:.22em; text-indent:.22em;   /* indent cancels the trailing space */
    color:{INK}; white-space:nowrap;
  }}
  .rule{{
    width:34%; height:1px; margin:{int(name_px*0.42)}px auto {int(name_px*0.34)}px;
    background:{BROWN}; opacity:.38;
  }}
  .desc{{
    font-family:'Times New Roman',Times,serif;
    font-size:{desc_px}px; line-height:1;
    letter-spacing:.34em; text-indent:.34em;
    color:{BROWN}; white-space:nowrap;
  }}
</style>
<div class=wrap><div class=panel>
  <div class=name>DAISY MAISON</div>
  <div class=rule></div>
  <div class=desc>PERSONALISED STREET SIGNS</div>
</div></div>"""


def render(out, w=1400, h=480, name_px=96, desc_px=29, pad_x=104, pad_y=66):
    html = wordmark_html(w, h, name_px, desc_px, pad_x, pad_y)
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "w.html")
        open(hp, "w").write(html)
        subprocess.run(
            [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--hide-scrollbars", "--default-background-color=00000000",
             f"--window-size={w},{h}", f"--screenshot={out}", "file://" + hp],
            check=True, capture_output=True)
    return out


if __name__ == "__main__":
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "wordmark.png"))
    print("wrote wordmark")
