"""Build the rebuilt homepage template (templates/index.json) from the original.

Usage:  python3 build_index.py            -> writes index.json next to this file
Inputs: index.before.json (the live homepage as of 23 Sep 2026, byte-exact)
        dm-home-styles.liquid (the one custom-liquid block)

Every section reuses an Ella 6.6.2 section that already exists in the theme.
Setting ids come from each section's {% schema %}; validate_template.py checks them.
"""
import copy
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
HEADER = """/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
"""


def load_template(path):
    text = path.read_text(encoding="utf-8")
    return json.loads(re.sub(r"^\s*/\*.*?\*/", "", text, flags=re.S))


before = load_template(HERE / "index.before.json")
old = before["sections"]
img = lambda name: f"shopify://shop_images/{name}"
col = lambda handle: f"shopify://collections/{handle}"
prod = lambda handle: f"shopify://products/{handle}"

SECTION_BG = "#fafaf9"
INK = "#2b2b2b"
SAGE = "#b0af9b"


# ---------------------------------------------------------------- 0. CSS block
styles = {
    "type": "custom-liquid",
    "settings": {"custom_liquid": (HERE / "dm-home-styles.liquid").read_text(encoding="utf-8").strip()},
}

# ---------------------------------------------------------------- 2. Hero
hero = copy.deepcopy(old["image_banner_UJGTQq"])
hero["settings"].update({"container": "fullwidth"})
hero["blocks"]["large_img_nMR3HH"]["settings"].update({
    # desktop keeps the existing landscape banner; phones get a real-room Christmas photo
    "mobile_image": img("FullSizeRender_879ae487-f623-4a13-9a53-350cf75daac1.heic"),
    "sub_title": "Handmade to order in Lytham St Annes",
    "font_size_sub_title_mb": 12,
    "margin_bottom_sub_title": 8,
    "heading": "Personalised gifts, handmade to order",
    "font_size_heading_mb": 26,
    "border_title": "none",
    "border_color_title_mobile": "#232323",
    "text": "<span style=\"color:#c6a45a;letter-spacing:1px\">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 10,000+ five-star reviews",
    "font_size_des": 14,
    "font_size_des_mb": 14,
    "line_height_des": 20,
    "margin_bottom_des": 16,
    "btn_text": "Shop Christmas gifts",
    "link": col("christmas"),
    "btn_text_2": "Wedding & engagement",
    "link_2": col("wedding-engagement"),
})


# ---------------------------------------------------------------- tile helpers
def tile(title, image, link):
    return {"type": "image", "settings": {
        "enable_image": True, "image": img(image), "link": link,
        "title": title, "title_align": "center", "enable_absolute": False, "align_items": "center",
        "align_items_spacing_top": 0, "align_items_spacing_bottom": 0, "align_items_spacing_lr": 0,
        "align_items_spacing_top_bottom_position": 0, "align_items_spacing_top_bottom_position_mb": 0,
        "bg_color_content": "", "sub_title": "", "border_sub_title": False,
        "color_title": "#232323", "fontsize_title": 16, "fontsize_title_mb": 14, "font_weight_title": "500",
        "enable_style_italic": False, "border_title": "none", "border_color_title": "",
        "des": "", "enable_des_hover": False, "button": "", "btn_icon": "",
    }}


def tile_row(title, tiles, prefix, *, layout, column, column_mb, mg_top_mb, mg_bottom_mb):
    blocks, order = {}, []
    for i, t in enumerate(tiles, 1):
        key = f"{prefix}_{i}"
        blocks[key] = t
        order.append(key)
    return {"type": "spotlight-block", "blocks": blocks, "block_order": order, "settings": {
        "container": "1200", "padding_full_width": 0, "disable_padding_content": False, "mg_minus_desktop": 0,
        "block_layout": "grid", "spotlight_block_swipe_on_mobile": layout, "column": column, "column_mb": column_mb,
        "enable_arrows": False, "enable_arrows_mb": False, "enable_dots": False, "enable_dots_mb": False,
        "display_border_bottom": False, "spotlight_bg": SECTION_BG, "spotlight_bg_gradient": "",
        "spotlight_block_title": title, "enable_border_title": False, "enable_custom_position_title": False,
        "color_title": "#232323", "fontsize_title": 28, "fontsize_title_mb": 22, "margin_bottom_title": 25,
        "spotlight_block_des": "", "title_align": "center", "item_distance": 15, "item_radius": 8,
        "view_all": "", "link_view_all": "", "display_spotlight_button": False, "spotlight_button_text": "",
        "enable_shadow": False, "enable_plus_icon": False, "enable_content_border": False,
        "mg_top_desktop": 50 if title else 0, "mg_top_tablet": 40 if title else 0, "mg_top_mobile": mg_top_mb,
        "mg_bottom_desktop": 50, "mg_bottom_tablet": 40, "mg_bottom_mobile": mg_bottom_mb,
    }}


# ---------------------------------------------------------------- 3. Shop by occasion (2 rows of 4: Ella caps spotlight-block at 4)
occasion_1 = copy.deepcopy(old["spotlight_block_JFKrLj"])  # was "Our Most Cherished Gifts"
occasion_1.update(tile_row("Shop by occasion", [
    tile("Christmas", "FullSizeRender_b9407277-ce92-4c69-8ec6-fd657cd64155.heic", col("christmas")),
    tile("Wedding", "Beach-Wedding-Pebble-3.jpg", col("wedding-engagement")),
    tile("Engagement", "Engagement.jpg", col("engagement")),
    tile("Christening", "Baby-Blue.jpg", col("christening-new-baby")),
], "occasion", layout="scroll", column="4", column_mb="1", mg_top_mb=30, mg_bottom_mb=0))
occasion_2 = tile_row("", [
    tile("New home", "New-Home-Christmas.jpg", col("my-home")),
    tile("Anniversary", "Pink_4f1f5235-141a-45e8-9380-015342809a7b.jpg", col("anniversary")),
    tile("Teacher", "Star-Keyring-BLUE-2.jpg", col("teachers-gifts")),
    tile("For Mum", "Mothers-Day-S.S-Img-5-Grey.jpg", col("mothers-day")),
], "occasion2", layout="scroll", column="4", column_mb="1", mg_top_mb=10, mg_bottom_mb=20)

# ---------------------------------------------------------------- 4. Best sellers (was "Trending Now")
best = copy.deepcopy(old["product_block_QcxFaJ"])
best["settings"].update({
    "product_block_title": "Best sellers",
    "product_block_collection": "best-sellers",
    "product_block_limit": 8,
    "enable_border_title": False,
    "fontsize_title": 28, "fontsize_title_mb": 22,
    "view_all": "Shop all best sellers", "link_view_all": col("best-sellers"),
    "mg_top_mobile": 30, "mg_bottom_mobile": 30,
})


# ---------------------------------------------------------------- 5. Proof strip (reuses the image-icon service block)
def svg(inner, filled=False):
    fill = "currentColor" if filled else "none"
    return ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner.replace("FILL", fill)}</svg>')


ICONS = {
    "star": svg('<polygon fill="FILL" points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>', True),
    "heart": svg('<path fill="FILL" d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>'),
    "clock": svg('<circle fill="FILL" cx="12" cy="12" r="10"/><polyline fill="FILL" points="12 6 12 12 16 14"/>'),
    "van": svg('<rect fill="FILL" x="1" y="3" width="15" height="13"/><polygon fill="FILL" points="16 8 20 8 23 11 23 16 16 16 16 8"/>'
               '<circle fill="FILL" cx="5.5" cy="18.5" r="2.5"/><circle fill="FILL" cx="18.5" cy="18.5" r="2.5"/>'),
}


def proof_item(icon, html):
    return {"type": "Text", "settings": {
        "bg_color_block": "#f3f2ee", "border_block": "#f3f2ee",
        "icon_type": "text", "icon": ICONS[icon], "width_icon": 26, "height_icon": 26, "mg_bottom_icon": 8,
        "color_icon": "#8c8b74", "text": "", "type_tab_font": "font_1",
        "description": html, "fontsize_des_block": 15, "fontsize_des_block_mb": 13, "lineheight_des_block": 18,
        "mg_bottom_des": 0, "color_des_block": INK, "button": "", "link": "",
    }}


proof = copy.deepcopy(old["16393870238958f868"])
proof["blocks"] = {
    "proof_reviews": proof_item("star", "<strong>10,000+</strong> five-star reviews"),
    "proof_handmade": proof_item("heart", "<strong>Handmade</strong> in Lancashire"),
    "proof_dispatch": proof_item("clock", "<strong>Made and dispatched</strong> in 5–7 working days, express 2–3"),
    "proof_delivery": proof_item("van", "<strong>Free UK delivery</strong> over £50"),
}
proof["block_order"] = list(proof["blocks"])
proof["settings"].update({
    "container": "container", "service_block_swipe_on_mobile": "list", "service_block_style": "style_1",
    "policies_bg": SECTION_BG, "service_block_title": "", "service_block_des": "", "view_all": "",
    "border_item": "none", "item_padding_top": 16, "item_padding_bottom": 12, "item_padding_left_right": 16,
    "item_radius": 12, "grid_gap": 10, "enable_block_bottom": False,
    "mg_top_desktop": 30, "mg_top_tablet": 20, "mg_top_mobile": 0,
    "mg_bottom_desktop": 40, "mg_bottom_tablet": 30, "mg_bottom_mobile": 30,
})

# ---------------------------------------------------------------- 6. The Christmas edit (2 x 2), replaces "New Arrivals"
christmas_edit = tile_row("The Christmas edit", [
    tile("Christmas street signs", "Xmas-Sign-BS-Family.jpg", col("christmas-street-signs")),
    tile("First Christmas hearts", "1st-Christmas-as-Mummy-and-Daddy-copy.jpg", col("christmas-pebble-hanging-hearts")),
    tile("Christmas reed diffuser", "christmas_reed_diffuser.png", prod("personalised-christmas-reed-diffuser-gift")),
    tile("Elf arrival postcard", "elvie.png", prod("personalised-elf-arrival-postcard-with-optional-elf-toy")),
], "xmas", layout="list", column="4", column_mb="2", mg_top_mb=20, mg_bottom_mb=30)


# ---------------------------------------------------------------- 7. How it works (Ella service block with images)
def step(image, title, text, link=""):
    return {"type": "Text", "settings": {
        "bg_color_block": "#ffffff", "border_block": "#ffffff",
        "icon_type": "image", "image": img(image), "icon": "", "width_icon": 64, "height_icon": 64, "mg_bottom_icon": 14,
        "color_icon": INK, "text": title, "type_tab_font": "font_1",
        "fontsize_title_block": 18, "fontsize_title_block_mb": 16, "title_block_font_weight": "700",
        "mg_bottom_title": 6, "mg_bottom_title_mb": 4, "color_block": INK,
        "description": text, "fontsize_des_block": 15, "fontsize_des_block_mb": 14, "lineheight_des_block": 20,
        "mg_bottom_des": 0, "color_des_block": "#4a4a4a", "button": "", "link": link,
    }}


how = {"type": "custom-service-block", "blocks": {
    "how_1": step("rn-image_picker_lib_temp_58b6d173-9a7f-478e-9825-759fc1d8df8d.png", "1. Choose the gift",
                  "Browse by occasion or by who it is for.", col("best-sellers")),
    "how_2": step("dm-how-it-works-live-sign-preview.jpg", "2. Personalise it and see it live",
                  "Add your names and dates. On our street signs the preview updates as you type.",
                  prod("mr-mrs-personalised-street-sign-gift")),
    "how_3": step("street_sign_christmas_wrapped.png", "3. We make it by hand and dispatch it",
                  "Handmade to order in Lytham St Annes and dispatched in 5–7 working days, or 2–3 with express."),
}, "block_order": ["how_1", "how_2", "how_3"], "settings": {
    "id_section": "", "container": "1170", "padding_full_width": 0, "display_border_top": False, "display_border_bottom": False,
    "service_block_swipe_on_mobile": "list", "service_block_style": "style_1", "policies_bg": SECTION_BG,
    "service_block_title": "How it works", "enable_border_title": False, "color_title": "#232323",
    "fontsize_title": 28, "fontsize_title_mb": 22, "mg_bottom_title_service_block": 25, "mg_bottom_title_service_block_mb": 20,
    "service_block_des": "", "view_all": "", "title_align": "center",
    "item_width": "full_width", "border_item": "none", "enable_item_distance": True, "enable_hover_box_shadow": False,
    "enable_hover_effects_top": False, "item_padding_top": 16, "item_padding_bottom": 12, "item_padding_left_right": 16,
    "item_radius": 12, "grid_gap": 20, "item_align": "center", "enable_block_bottom": False,
    "mg_top_desktop": 50, "mg_top_tablet": 40, "mg_top_mobile": 30, "mg_bottom_desktop": 50, "mg_bottom_tablet": 40, "mg_bottom_mobile": 30,
}}


# ---------------------------------------------------------------- 8. Reviews (verbatim quotes from snippets/dm-proof.liquid)
def review(image, product_name, handle, quote):
    return {"type": "review", "settings": {
        "avatar": img(image), "heading": f'<a href="/products/{handle}">{product_name}</a>', "sub_heading": "",
        "rating": "star5", "name": "Verified 5-star review", "date": "", "body": quote,
    }}


reviews = {"type": "customer-review-block", "blocks": {
    "review_wedding": review("hf_20260514_153532_bdebf4f5-4393-4714-ad49-e9e8060eb6fe.png", "Wedding pebble picture",
                             "wedding-flower-arch-personalised-pebble-picture",
                             "The first one was a gift for my friends who are getting married and they absolutely loved it so much that I have bought another."),
    "review_mrmrs": review("Wed.S.Sign-5.jpg", "Mr &amp; Mrs street sign", "mr-mrs-personalised-street-sign-gift",
                           "Excellent product, beautifully made. The streetsign will be a lasting gift for my sons wedding."),
    "review_engagement": review("hf_20260515_131422_4394adef-99bd-47df-92f3-00a7180783a9.png", "Engagement love tree picture",
                                "engagement-proposal-love-tree-personalised-pebble-picture-copy",
                                "5* from beginning to end. Beautiful unique item… 100% recommend to anyone looking for a unique personalised gift."),
}, "block_order": ["review_wedding", "review_mrmrs", "review_engagement"], "settings": {
    "container": "1170", "padding_full_width": 0, "section_style": "style_1", "review_bg": SECTION_BG, "review_bg_gradient": "",
    "enable_heading_style_2": False, "review_title": "What our customers say", "color_title": "#232323", "mg_bottom_title": 25,
    "fontsize_title": 28, "fontsize_title_mb": 22, "review_des": "", "title_align": "center",
    "block_layout_style": "layout2", "review_rows": "3", "show_arrow": False, "center_mode": False,
    "avatar_margin_bottom": 12, "color_heading": "#232323", "fontsize_heading": 16, "heading_margin_bottom": 8,
    "heading_font_weight": "600", "color_sub_heading": "#808080", "fontsize_sub_heading": 13, "sub_heading_margin_bottom": 10,
    "color_name": "#5a5a5a", "fontsize_name": 13, "name_margin_bottom": 0, "color_date": "#808080", "fontsize_date": 13,
    "color_body": INK, "fontsize_body": 15, "body_margin_bottom": 12, "star_font_size": 16, "star_margin_bottom": 8,
    "show_avatar": True, "start_position": "above_title", "star_color": "#c6a45a",
    "mg_top_desktop": 50, "mg_top_tablet": 40, "mg_top_mobile": 30, "mg_bottom_desktop": 30, "mg_bottom_tablet": 20, "mg_bottom_mobile": 10,
}}

# ---------------------------------------------------------------- 9. Shop by recipient (2 rows of 3)
recipient_1 = tile_row("Shop by recipient", [
    tile("For couples", "Valentines-Heart-Final_80e362b5-5510-489a-bb14-cb8ba7587d06.jpg", col("anniversary")),
    tile("For Mum", "hf_20260515_132358_a1bfb14f-8008-4208-9c9c-7b90c24cd034.png", col("mothers-day")),
    tile("For grandparents", "Grandparent-Festive-pebble.jpg", col("christmas-pebble-pictures")),
], "recipient", layout="list", column="3", column_mb="2", mg_top_mb=30, mg_bottom_mb=0)
recipient_2 = tile_row("", [
    tile("For teachers", "Apple-Bookmark-RED.jpg", col("teachers-gifts")),
    tile("For the family", "PERFECTLY-IMPERFECT-SEPT-20_1.jpg", col("pebble-sketch-pictures")),
    tile("For friends", "hf_20260515_134703_d6d4f816-2534-4fd6-b717-2511f043a17d.png", col("friendship-special-occasions")),
], "recipient2", layout="list", column="3", column_mb="2", mg_top_mb=0, mg_bottom_mb=30)

# ---------------------------------------------------------------- 10. Made in Lytham (enable the video block, real copy, sage panel)
video = copy.deepcopy(old["video_block_86qWNA"])
video.pop("disabled", None)
video["settings"].update({
    "container": "container", "spotlight_bg": SAGE, "spotlight_bg_gradient": "",
    "video_block_title": "Personalised by you. Handmade by us in Lytham St Annes.",
    "color_title": INK, "fontsize_title": 28, "fontsize_title_mb": 22, "margin_bottom_title": 12,
    "video_block_des": ("<p>Every sign, pebble picture and keepsake is made to order in our Lytham St Annes workshop. "
                        "You choose the words and we make it by hand, just for you. "
                        "Orders are made and dispatched in 5–7 working days, or 2–3 with express.</p>"),
    "color_des": INK, "fontsize_des": 16, "title_align": "center",
    # the 480p Shopify rendition (3.7 MB) instead of the 19.3 MB original; url_mp4_mb stays blank
    # because custom.css shows both videos when it is set
    "url_mp4": "https://cdn.shopify.com/videos/c/vp/15750962af724ca592911f46cc1d8a13/15750962af724ca592911f46cc1d8a13.SD-480p-1.5Mbps-34610101.mp4",
    "url_mp4_mb": "",
    # the theme appends "%"; the saved "66%"/"100%" rendered as "100%%" and collapsed the video on phones
    "video_height": "56.25", "video_height_mb": "56.25",
    "full_width": False, "heading": "", "text": "", "btn_text": "", "link": "",
    "mg_top_desktop": 50, "mg_top_tablet": 40, "mg_top_mobile": 30,
    "mg_bottom_desktop": 50, "mg_bottom_tablet": 40, "mg_bottom_mobile": 30,
})

# ---------------------------------------------------------------- 11. Inline newsletter under Instagram
newsletter = {"type": "newsletter", "blocks": {"newsletter_dm10": {"type": "newsletter", "settings": {
    "section_title": "10% off your first order", "section_title_font_size": 28, "section_title_font_size_mb": 22,
    "section_title_font_weight": "600", "section_title_text_transform": "none", "section_title_font_style": "normal",
    "section_title_color": INK, "mg_bottom_title": 8, "mg_bottom_title_mb": 8,
    "section_description": "<p>Join our emails for new designs and gift ideas, plus a welcome code for 10% off selected ranges.</p>",
    "section_description_font_size": 16, "section_description_font_size_mb": 15, "section_description_font_weight": "400",
    "section_description_color": "#5a5a5a", "margin_bottom_des": 16, "des_line_height": 22,
    "show_input_field": True, "input_style": "style_1", "input_width": 420, "input_border_radius": 12, "input_text_font_size": 16,
    "input_placeholder": "Your email address", "input_placeholder_color": "#6b6b6b",
    "input_background_color": "#ffffff", "input_border_color": "#d9d2c3", "form_gap": 10,
    "button_text": "Sign up", "button_font_size": 16, "button_width": 200,
    "button_text_color": "#ffffff", "button_border_color": INK, "button_background_color": INK, "button_gradient_color": "",
    "button_text_color_hover": INK, "button_border_color_hover": SAGE, "button_background_color_hover": SAGE,
    "button_gradient_color_hover": "", "button_text_transform": "none", "button_font_weight": "600",
    "newsletter_content_direction": "column", "newsletter_form_justify_content": "center", "input_width_behavior": "auto",
}}}, "block_order": ["newsletter_dm10"], "settings": {
    "container": "container", "padding_full_width": 0, "background": SECTION_BG, "background_gradient": "",
    "section_text_align": "center", "justify_section_content": "center", "section_item_distance": 20,
    "enable_social_media_below": False,
    "mg_top_desktop": 50, "mg_top_tablet": 40, "mg_top_mobile": 30, "mg_bottom_desktop": 50, "mg_bottom_tablet": 40, "mg_bottom_mobile": 35,
}}

# ---------------------------------------------------------------- assemble
sections = {
    "dm_home_styles": styles,
    "image_banner_UJGTQq": hero,
    "spotlight_block_JFKrLj": occasion_1,
    "dm_occasion_row_2": occasion_2,
    "product_block_QcxFaJ": best,
    "16393870238958f868": proof,
    "dm_christmas_edit": christmas_edit,
    "dm_how_it_works": how,
    "dm_reviews": reviews,
    "17394583817a28cc5e": copy.deepcopy(old["17394583817a28cc5e"]),  # Feefo on-page reviews, moved up
    "dm_recipient_row_1": recipient_1,
    "dm_recipient_row_2": recipient_2,
    "video_block_86qWNA": video,
    "16378128152fdd5fe7": copy.deepcopy(old["16378128152fdd5fe7"]),  # Instagram heading, unchanged
    "1726396330d08baf63": copy.deepcopy(old["1726396330d08baf63"]),  # Instafeed app block, unchanged
    "dm_newsletter": newsletter,
}
order = list(sections)

# sections that were already disabled stay in the file, still disabled, at the end
for key in before["order"]:
    sec = old[key]
    if sec.get("disabled") and key not in sections:
        sections[key] = copy.deepcopy(sec)
        order.append(key)

# removed: "Why thousands choose us" (text-only) and "New Arrivals" (sale badges); both remain in index.before.json
REMOVED = [k for k in before["order"] if k not in sections]

template = {"sections": sections, "order": order}
out = HERE / "index.json"
out.write_text(HEADER + json.dumps(template, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size} bytes), {len(order)} sections, removed: {REMOVED}")
