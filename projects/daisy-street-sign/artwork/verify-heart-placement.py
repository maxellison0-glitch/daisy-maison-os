#!/usr/bin/env python
"""Verify the locked NICHOLS signature across short, long, and compressed names."""

import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont


HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, "assets", "times.ttf")
HEART_PATH = os.path.join(HERE, "assets", "heart.png")
BUILD_PATH = os.path.join(HERE, "build.py")
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
DAISY_NS = "https://daisymaison.co.uk/ns/production"
REQUIRED_IDS = {
    "outer-plate",
    "inset-panel",
    "line-1",
    "signature-heart",
    "line-2",
}

# The mounting holes were REMOVED from this set on 2026-07-27, not forgotten.
# They are physical holes drilled in the acrylic, so drawing them printed black
# rings around absent material; e1146fa dropped them from build.py. This fixture
# kept requiring the IDs, which meant it asserted on its first sample and every
# geometry check below it silently stopped running. Do not add them back.
FORBIDDEN_IDS = {"mounting-hole-left", "mounting-hole-right"}

TARGET_W = 486.0
FONT_SIZE = 59.0
VSCALE = 1.4
CAP_CENTER_Y = 55.3
PX_PER_MM = 11.8719
HEART_W = 236 / PX_PER_MM
HEART_H = 229 / PX_PER_MM
CX = 285.0

font = TTFont(FONT_PATH)
upem = font["head"].unitsPerEm
cmap = font.getBestCmap()
hmtx = font["hmtx"]
glyph = font["glyf"][cmap[ord("&")]]
cap_height = font["OS/2"].sCapHeight / upem
space_advance = hmtx["space"][0]
heart_alpha = np.asarray(Image.open(HEART_PATH).convert("RGBA").getchannel("A")) > 8


def natural_width(text):
    return sum(hmtx[cmap[ord(ch)]][0] if ord(ch) in cmap else space_advance for ch in text) / upem


def amp_geometry(text, horizontal_scale, signature_scale):
    prefix, suffix = text.split("&", 1)
    prefix_width = natural_width(prefix) * FONT_SIZE * horizontal_scale
    signature_advance = natural_width("&") * FONT_SIZE * signature_scale
    suffix_width = natural_width(suffix) * FONT_SIZE * horizontal_scale
    text_width = prefix_width + signature_advance + suffix_width
    baseline = CAP_CENTER_Y + cap_height * FONT_SIZE * VSCALE / 2
    amp_origin = CX - text_width / 2 + prefix_width
    amp_left = (
        amp_origin
        + glyph.xMin / upem * FONT_SIZE * signature_scale
    )
    amp_width = (glyph.xMax - glyph.xMin) / upem * FONT_SIZE * signature_scale
    amp_top = baseline - glyph.yMax / upem * FONT_SIZE * VSCALE
    amp_height = (glyph.yMax - glyph.yMin) / upem * FONT_SIZE * VSCALE
    return amp_left, amp_top, amp_width, amp_height


def render_amp_mask(width_mm, height_mm):
    pixel_size = max(32, round(FONT_SIZE * PX_PER_MM))
    pillow_font = ImageFont.truetype(FONT_PATH, pixel_size)
    probe = Image.new("L", (pixel_size * 3, pixel_size * 3), 0)
    draw = ImageDraw.Draw(probe)
    bbox = draw.textbbox((pixel_size, pixel_size), "&", font=pillow_font)
    draw.text((pixel_size - bbox[0], pixel_size - bbox[1]), "&", font=pillow_font, fill=255)
    rendered = probe.crop(probe.getbbox())
    rendered = rendered.resize(
        (max(1, round(width_mm * PX_PER_MM)), max(1, round(height_mm * PX_PER_MM))),
        Image.Resampling.LANCZOS,
    )
    return np.asarray(rendered) > 8


def red_tip_to_black_edge_delta(amp_mask, offset_x, offset_y):
    heart_rows, _ = np.nonzero(heart_alpha)
    tip_y = int(heart_rows.max())
    tip_x = int(round(np.flatnonzero(heart_alpha[tip_y]).mean()))
    amp_row = offset_y + tip_y
    assert 0 <= amp_row < amp_mask.shape[0]
    stroke = np.flatnonzero(amp_mask[amp_row])
    assert len(stroke), "No black ampersand stroke exists at the red-heart tip"
    return offset_x + tip_x - int(stroke.max())


def build_and_read(temp_dir, text, subtitle="EST 2026"):
    output = os.path.join(temp_dir, text.replace(" ", "-").replace("&", "and") + ".svg")
    env = os.environ.copy()
    for key in ("HW", "STROKE_FRAC"):
        env.pop(key, None)
    subprocess.run(
        [sys.executable, BUILD_PATH, "VERIFY", text, subtitle, str(TARGET_W), output],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    root = ET.parse(output).getroot()
    assert root.attrib["width"] == "570mm"
    assert root.attrib["height"] == "125mm"
    assert root.attrib["viewBox"] == "0 0 570 125"
    ids = {node.attrib["id"] for node in root.iter() if "id" in node.attrib}
    assert not (REQUIRED_IDS - ids), f"Missing IDs for {text}: {sorted(REQUIRED_IDS - ids)}"
    assert not (FORBIDDEN_IDS & ids), (
        f"{text}: build.py drew {sorted(FORBIDDEN_IDS & ids)} - mounting holes are "
        "physical holes in the acrylic and must never be printed."
    )
    line_one = root.find(".//*[@id='line-1']")
    assert line_one is not None and line_one.attrib["data-text"] == text
    line_one_parts = list(line_one.iterfind(f".//{{{SVG_NS}}}text"))
    assert "".join(part.text or "" for part in line_one_parts) == text
    assert all("DaisyTimesRegular" in part.attrib["font-family"] for part in line_one_parts)
    assert all(part.attrib["font-weight"] == "400" for part in line_one_parts)
    line_two = root.find(".//*[@id='line-2']")
    assert line_two is not None and (line_two.text or "") == subtitle
    assert "DaisyTimesRegular" in line_two.attrib["font-family"]
    assert line_two.attrib["font-weight"] == "400"
    heart = root.find(f"{{{SVG_NS}}}image[@id='signature-heart']")
    assert heart is not None
    assert heart.attrib[f"{{{XLINK_NS}}}href"].startswith("data:image/png;base64,")
    method = root.find(f".//{{{DAISY_NS}}}heartPlacementMethod")
    assert method is not None and method.text == "locked-nichols-signature-v1"
    scale = root.find(f".//{{{DAISY_NS}}}line1HorizontalScale")
    assert scale is not None
    signature_scale = root.find(f".//{{{DAISY_NS}}}signatureHorizontalScale")
    assert signature_scale is not None
    review = root.find(f".//{{{DAISY_NS}}}heartManualReviewRequired")
    assert review is not None
    return (
        {key: float(heart.attrib[key]) for key in ("x", "y", "width", "height")},
        float(scale.text),
        float(signature_scale.text),
        review.text == "true",
    )


samples = (
    "MR & MRS NASH",
    "MR & MRS FROST",
    "MR & MRS MCGREGOR",
    "MR & MRS FOLLOWS",
    "MR & MRS JANNAWAY",
    "MR & MRS WILKINSON",
)

with tempfile.TemporaryDirectory(prefix="daisy-heart-verify-") as temp_dir:
    widths = []
    scales = []
    for sample in samples:
        heart, horizontal_scale, signature_scale, manual_review = build_and_read(temp_dir, sample)
        amp_left, amp_top, amp_width, amp_height = amp_geometry(
            sample, horizontal_scale, signature_scale
        )
        edge_delta = red_tip_to_black_edge_delta(
            render_amp_mask(amp_width, amp_height),
            round((heart["x"] - amp_left) * PX_PER_MM),
            round((heart["y"] - amp_top) * PX_PER_MM),
        )
        assert abs(heart["width"] - HEART_W) < 0.001
        assert abs(heart["height"] - HEART_H) < 0.001
        assert abs(heart["y"] - 39.76) < 0.001
        assert abs(edge_delta - (-3)) <= 1
        assert not manual_review
        widths.append(heart["width"])
        scales.append(horizontal_scale)
        assert abs(signature_scale - 0.8644) < 0.001
        print(
            f"PASS {sample}: scaleX={horizontal_scale:.4f}, heartY={heart['y']:.2f}mm, "
            f"red-tip/black-edge delta={edge_delta}px"
        )

    assert max(widths) - min(widths) < 0.001
    assert min(scales) < max(scales), "Long-name horizontal compression was not exercised"
    build_and_read(temp_dir, "MR & MRS NASH", "")
    _, extreme_scale, _, extreme_review = build_and_read(
        temp_dir, "MR & MRS ALEXANDER-WILKINSON"
    )
    assert extreme_scale < 0.50 and extreme_review
    print("PASS extreme compression is flagged for manual review instead of silently approved")
    build_source = open(BUILD_PATH, encoding="utf-8").read()
    for rejected_name in ("AMP_TIP_X", "AMP_TIP_Y", "HEART_PIN_X", "HEART_PIN_Y"):
        assert rejected_name not in build_source
    print("PASS blank subtitle and rejected landmark constants are absent")

print(f"Rendered-mask heart verification passed for {len(samples)} name lengths plus blank subtitle.")
