from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "projects" / "daisy-maison-care" / "source"
ARTWORK = ROOT / "projects" / "daisy-maison-care" / "artwork"
OUTPUT = ARTWORK / "daisy-maison-daily-collagen-mockup.jpg"


def build_mockup():
    label_path = next(ARTWORK.glob("PL-489*.jpg"))
    label = Image.open(label_path).convert("RGB")

    # The front-facing third of the wrap is the dedicated Daisy Maison hero panel.
    x0 = round(label.width * 69 / 204)
    x1 = round(label.width * 135 / 204)
    y0 = round(label.height * 2 / 104)
    y1 = round(label.height * 102 / 104)
    front = label.crop((x0, y0, x1, y1))

    bg = Image.new("RGB", (2000, 2400), "#F4F0E8")
    draw = ImageDraw.Draw(bg)
    draw.ellipse((360, 2190, 1640, 2350), fill="#D6D0C5")
    bg = bg.filter(ImageFilter.GaussianBlur(24))

    jar = Image.open(SOURCE / "nutribl-blank-jar.jpg").convert("RGBA")
    jar = jar.resize((1400, 1969), Image.Resampling.LANCZOS)
    jar = ImageEnhance.Contrast(jar).enhance(1.04)
    jar_x, jar_y = 300, 170
    bg.paste(jar, (jar_x, jar_y), jar)

    label_w, label_h = 1360, 1360
    front = front.resize((label_w, label_h), Image.Resampling.LANCZOS).convert("RGBA")

    # Gently shade and fade the artwork at the cylinder edges so the flat artwork
    # reads as a wrapped label while keeping the centre typography exact.
    shade = Image.new("L", (label_w, label_h), 255)
    shade_px = shade.load()
    for x in range(label_w):
        edge = min(x / (label_w - 1), 1 - x / (label_w - 1)) * 2
        alpha = int(125 + 130 * min(1, edge * 3.7))
        for y in range(label_h):
            shade_px[x, y] = alpha
    front.putalpha(shade)

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    overlay.alpha_composite(front, (jar_x + 20, jar_y + 390))

    gloss = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.rounded_rectangle((910, 560, 1010, 1810), radius=50, fill=(255, 255, 255, 34))
    gloss = gloss.filter(ImageFilter.GaussianBlur(30))

    composed = Image.alpha_composite(bg.convert("RGBA"), overlay)
    composed = Image.alpha_composite(composed, gloss).convert("RGB")
    composed.save(OUTPUT, quality=96, optimize=True, progressive=True)
    print(OUTPUT)


if __name__ == "__main__":
    build_mockup()
