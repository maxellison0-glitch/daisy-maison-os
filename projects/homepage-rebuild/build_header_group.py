"""Rebuild sections/header-group.json with the new announcement bar (site-wide on the theme).

Only section announcement_bar_a4ALfD changes; everything else is copied as-is from
header-group.before.json (the copy theme's file as returned by the Admin API on 23 Sep 2026).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
raw = (HERE / "header-group.before.json").read_text(encoding="utf-8")
header = re.match(r"^\s*/\*.*?\*/\s*", raw, flags=re.S)
group = json.loads(raw[header.end():] if header else raw)

bar = group["sections"]["announcement_bar_a4ALfD"]
bar["blocks"] = {
    # the Christmas cut-off line ("Order by <date> for guaranteed Christmas dispatch") goes back in once Max sets the date
    "announcement_delivery": {"type": "announcement", "settings": {
        "text": "<p>Free UK delivery over £50</p>",
        "btn_color": "#2b2b2b", "btn_border_color": "#2b2b2b", "btn_bg_color": "#f3f2ee", "btn_bg_color_gradient": ""}},
}
bar["block_order"] = ["announcement_delivery"]
bar["settings"].update({
    "enable_announcement": True, "layout": "slider", "enable_close": False, "arrow_active": False,
    "color_text": "#2b2b2b", "bg_color_text": "#f3f2ee", "bg_color_text_gradient": "",
    "font_size_text": 13, "font_style_text": "normal", "font_weight_text": "500",
    "content_max_width": 38, "padding_top": 2, "padding_bottom": 2,
})
out = HERE / "header-group.json"
out.write_text((header.group(0) if header else "") + json.dumps(group, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out)
