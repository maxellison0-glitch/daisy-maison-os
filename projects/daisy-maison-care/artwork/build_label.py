from pathlib import Path
from PIL import Image

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import portrait
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "projects" / "daisy-maison-care" / "source"
ARTWORK = ROOT / "projects" / "daisy-maison-care" / "artwork"
TMP = ROOT / "tmp" / "pdfs"
OUTPUT = ROOT / "output" / "pdf"

PDF_PATH = OUTPUT / "PL-489$front.pdf"
RECOLOURED_LOGO = TMP / "daisy-maison-logo-olive.png"

MM = 72 / 25.4
PAGE_W = 204 * MM
PAGE_H = 104 * MM

CREAM = colors.HexColor("#F4F0E8")
PAPER = colors.HexColor("#FBF9F4")
SAGE = colors.HexColor("#C8CABA")
PALE_SAGE = colors.HexColor("#E4E4DA")
OLIVE = colors.HexColor("#4F5A48")
CHARCOAL = colors.HexColor("#24231F")
MUSHROOM = colors.HexColor("#837C70")
BLUSH = colors.HexColor("#D8BDB0")
WHITE = colors.white


def mm(value):
    return value * MM


def register_fonts():
    font_dir = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("DM-Sans", str(font_dir / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("DM-Sans-Bold", str(font_dir / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("DM-Serif", str(font_dir / "georgia.ttf")))
    pdfmetrics.registerFont(TTFont("DM-Serif-Bold", str(font_dir / "georgiab.ttf")))


def recolour_logo():
    src = Image.open(SOURCE / "daisy-maison-logo-white.png").convert("RGBA")
    px = src.load()
    olive = (79, 90, 72)
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (*olive, a)
    RECOLOURED_LOGO.parent.mkdir(parents=True, exist_ok=True)
    src.save(RECOLOURED_LOGO)


def style(name, size, leading=None, color=CHARCOAL, alignment=TA_LEFT, space_after=0):
    return ParagraphStyle(
        name,
        fontName=name,
        fontSize=size,
        leading=leading or size * 1.22,
        textColor=color,
        alignment=alignment,
        spaceAfter=space_after,
        allowWidows=0,
        allowOrphans=0,
    )


BODY = style("DM-Sans", 5.35, 6.45)
BODY_TIGHT = style("DM-Sans", 5.15, 5.95)
SMALL = style("DM-Sans", 5.0, 5.6, color=MUSHROOM)
SECTION = style("DM-Sans-Bold", 6.3, 7.1, color=OLIVE)
SECTION_WHITE = style("DM-Sans-Bold", 6.3, 7.1, color=WHITE)
CENTER_SMALL = style("DM-Sans", 6.2, 7.4, color=CHARCOAL, alignment=TA_CENTER)
CENTER_TINY = style("DM-Sans", 5.2, 6.2, color=MUSHROOM, alignment=TA_CENTER)
CLAIM = style("DM-Serif", 6.8, 8.6, color=OLIVE, alignment=TA_CENTER)


def para(c, html, x, y_top, width, pstyle, max_height=1000):
    p = Paragraph(html, pstyle)
    _, h = p.wrap(width, max_height)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def section_title(c, title, x, y_top, width, color=OLIVE):
    c.setFillColor(color)
    c.setFont("DM-Sans-Bold", 6.3)
    c.drawString(x, y_top - 6.3, title.upper())
    c.setStrokeColor(BLUSH)
    c.setLineWidth(0.55)
    c.line(x, y_top - 9.2, x + width, y_top - 9.2)
    return y_top - 13.2


def daisy(c, cx, cy, radius, stroke=BLUSH, fill=PAPER, petals=8):
    import math
    c.saveState()
    c.setStrokeColor(stroke)
    c.setFillColor(fill)
    c.setLineWidth(0.65)
    for i in range(petals):
        a = 2 * math.pi * i / petals
        px = cx + math.cos(a) * radius * 0.68
        py = cy + math.sin(a) * radius * 0.68
        c.saveState()
        c.translate(px, py)
        c.rotate(i * (360 / petals))
        c.ellipse(-radius * 0.24, -radius * 0.64, radius * 0.24, radius * 0.64, fill=1, stroke=1)
        c.restoreState()
    c.setFillColor(CREAM)
    c.circle(cx, cy, radius * 0.24, fill=1, stroke=1)
    c.restoreState()


def table(c, x, y_top, width, rows, col_widths, header=None, font_size=5.05, row_h=8.1):
    y = y_top
    if header:
        c.setFillColor(OLIVE)
        c.roundRect(x, y - 10.3, width, 10.3, 2.2, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("DM-Sans-Bold", 5.25)
        for i, text in enumerate(header):
            tx = x + sum(col_widths[:i]) + 3
            c.drawString(tx, y - 7.1, text)
        y -= 10.3
    for idx, row in enumerate(rows):
        if idx % 2 == 0:
            c.setFillColor(colors.Color(1, 1, 1, alpha=0.48))
            c.rect(x, y - row_h, width, row_h, fill=1, stroke=0)
        c.setFillColor(CHARCOAL)
        c.setFont("DM-Sans", font_size)
        for i, text in enumerate(row):
            tx = x + sum(col_widths[:i]) + 3
            if i == 0:
                c.drawString(tx, y - row_h + 2.15, text)
            else:
                c.drawRightString(x + sum(col_widths[: i + 1]) - 3, y - row_h + 2.15, text)
        y -= row_h
    return y


def build():
    register_fonts()
    recolour_logo()
    OUTPUT.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Daisy Maison Care — Daily Marine Collagen — PL-489")
    c.setAuthor("Daisy Maison")

    # Full bleed background. Finished trim is 2 mm inside each edge.
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    left_x, left_w = mm(5), mm(61)
    centre_x, centre_w = mm(69), mm(66)
    right_x, right_w = mm(138), mm(61)
    top = PAGE_H - mm(5)

    # Soft centre field; no hard label-edge border per printer guidance.
    c.setFillColor(PALE_SAGE)
    c.roundRect(centre_x, mm(4), centre_w, PAGE_H - mm(8), mm(12), fill=1, stroke=0)
    c.setStrokeColor(SAGE)
    c.setLineWidth(0.7)
    c.line(mm(67.4), mm(7), mm(67.4), PAGE_H - mm(7))
    c.line(mm(136.6), mm(7), mm(136.6), PAGE_H - mm(7))

    # LEFT PANEL
    y = top
    y = section_title(c, "Directions", left_x, y, left_w)
    y = para(
        c,
        "Adults, add 1 level scoop of powder to 250ml water or juice. Collagen dissolves more effectively when shaken rather than stirred. It can be used in a cold or warm drink though it will dissolve better under tepid conditions. <b>Do not exceed recommended daily dose.</b>",
        left_x,
        y,
        left_w,
        BODY,
    ) - 4

    y = section_title(c, "Approved health claims", left_x, y, left_w)
    y = para(
        c,
        "Vitamin C contributes to normal collagen formation for the normal function of skin, bones and cartilage.<br/><br/>Riboflavin, Biotin &amp; Niacin contribute to the maintenance of normal skin.",
        left_x,
        y,
        left_w,
        BODY,
    ) - 4

    y = section_title(c, "Allergy advice", left_x, y, left_w)
    y = para(
        c,
        "Potential allergens are shown in bold in the ingredient list. Although rigorous precautions are taken to prevent any cross-contamination, this product is manufactured in a facility that handles allergy-based materials.",
        left_x,
        y,
        left_w,
        BODY_TIGHT,
    ) - 4

    y = section_title(c, "Cautions", left_x, y, left_w)
    y = para(
        c,
        "Always consult your health practitioner before taking nutritional supplements, especially if you are taking medication or are under medical supervision. You should not take supplements as a substitute for a varied balanced diet or healthy lifestyle. Store in a cool, dry &amp; dark place, under 25 degrees, out of reach of children. Not suitable for vegetarians or vegans.",
        left_x,
        y,
        left_w,
        BODY_TIGHT,
    ) - 4

    y = section_title(c, "Made for", left_x, y, left_w)
    para(
        c,
        "Manufactured to the GMP code of practice for:<br/><b>Daisy Maison</b><br/>Unit 6 Juniper Court, Thompson Road,<br/>Blackpool FY4 5QF, United Kingdom<br/>orders@daisymaison.co.uk · daisymaison.co.uk",
        left_x,
        y,
        left_w,
        BODY_TIGHT,
    )

    # CENTRE / FRONT PANEL
    logo = ImageReader(str(RECOLOURED_LOGO))
    logo_w = mm(53)
    logo_h = logo_w * (160 / 1678)
    c.drawImage(logo, centre_x + (centre_w - logo_w) / 2, PAGE_H - mm(12) - logo_h, logo_w, logo_h, mask="auto")
    c.setFillColor(OLIVE)
    c.setFont("DM-Sans-Bold", 5.8)
    c.drawCentredString(centre_x + centre_w / 2, PAGE_H - mm(19), "C  A  R  E")

    daisy(c, centre_x + centre_w / 2, PAGE_H - mm(30), mm(5.2), stroke=BLUSH, fill=PALE_SAGE)

    c.setFillColor(CHARCOAL)
    c.setFont("DM-Serif-Bold", 15.4)
    c.drawCentredString(centre_x + centre_w / 2, PAGE_H - mm(44), "DAILY")
    c.drawCentredString(centre_x + centre_w / 2, PAGE_H - mm(51.5), "COLLAGEN")
    c.setFillColor(OLIVE)
    c.setFont("DM-Sans-Bold", 6.1)
    c.drawCentredString(centre_x + centre_w / 2, PAGE_H - mm(58), "HYDROLYSED MARINE COLLAGEN")

    para(
        c,
        "Powdered Food Supplement providing Marine Collagen, Hyaluronic Acid, Vitamin C and B Vitamins.",
        centre_x + mm(7),
        PAGE_H - mm(63),
        centre_w - mm(14),
        CENTER_SMALL,
    )

    badge_y = mm(21)
    c.setStrokeColor(OLIVE)
    c.setLineWidth(0.75)
    c.roundRect(centre_x + mm(7), badge_y, centre_w - mm(14), mm(13), mm(6.5), fill=0, stroke=1)
    c.setFillColor(OLIVE)
    c.setFont("DM-Serif-Bold", 10.3)
    c.drawCentredString(centre_x + centre_w / 2, badge_y + mm(7.1), "10 g COLLAGEN")
    c.setFont("DM-Sans", 5.1)
    c.drawCentredString(centre_x + centre_w / 2, badge_y + mm(3.2), "PER 10.35 g SERVING")

    c.setFillColor(CHARCOAL)
    c.setFont("DM-Sans-Bold", 6.2)
    c.drawCentredString(centre_x + centre_w / 2, mm(15.1), "UNFLAVOURED  ·  29 SERVINGS")
    c.setFont("DM-Sans", 6.1)
    c.drawCentredString(centre_x + centre_w / 2, mm(10.6), "300 g POWDER")
    c.setFillColor(MUSHROOM)
    c.setFont("DM-Sans-Bold", 5.2)
    c.drawCentredString(centre_x + centre_w / 2, mm(6.5), "FOOD SUPPLEMENT")

    # RIGHT PANEL
    y = top
    y = section_title(c, "Product information", right_x, y, right_w)
    rows = [
        ("Vitamin C", "180 mg", "225%"),
        ("Thiamin (B1)", "4 mg", "364%"),
        ("Riboflavin", "6 mg", "429%"),
        ("Niacin", "17 mg", "106%"),
        ("Vitamin B6", "4 mg", "286%"),
        ("Folic Acid", "200 µg", "100%"),
        ("Vitamin B12", "10 µg", "400%"),
        ("Biotin", "200 µg", "400%"),
        ("Pantothenic Acid (B5)", "21 mg", "350%"),
        ("Hydrolysed Marine Collagen (93% Protein)", "10 g", "—"),
        ("Hyaluronic Acid", "25 mg", "—"),
    ]
    c.setFillColor(MUSHROOM)
    c.setFont("DM-Sans", 5.0)
    c.drawString(right_x, y - 1, "1 scoop (10.35 g) typically provides:")
    y -= 5
    y = table(
        c,
        right_x,
        y,
        right_w,
        rows,
        [right_w * 0.69, right_w * 0.19, right_w * 0.12],
        header=("NUTRIENT", "AMOUNT", "NRV*"),
        font_size=5.0,
        row_h=7.25,
    )
    c.setFillColor(MUSHROOM)
    c.setFont("DM-Sans", 5.0)
    c.drawString(right_x, y - 5.2, "*NRV = Nutrient Reference Value")
    y -= 11

    y = section_title(c, "Ingredients", right_x, y, right_w)
    y = para(
        c,
        "Hydrolysed Marine Collagen (<b>fish</b>), Vitamin C (as Calcium Ascorbate), Sodium Hyaluronate, Pantothenic Acid (as Calcium Pantothenate), Niacin (as Nicotinamide), Riboflavin, Thiamin (as Hydrochloride), Vitamin B6 (as Pyridoxine Hydrochloride), D-Biotin, Folic Acid, Vitamin B12 (as Methylcobalamin).",
        right_x,
        y,
        right_w,
        BODY_TIGHT,
    ) - 4

    y = section_title(c, "Nutritional analysis", right_x, y, right_w)
    nutrition = [
        ("Energy", "1782 kJ / 420 kcal"),
        ("Fat", "<0.5 g"),
        ("Carbohydrate", "<1.0 g"),
        ("of which sugars", "<0.1 g"),
        ("Fibre", "<0.5 g"),
        ("Protein", "92.3 g"),
        ("Salt", "0.16 g"),
    ]
    y = table(c, right_x, y, right_w, nutrition, [right_w * 0.56, right_w * 0.44], header=("PER 100 g", ""), font_size=5.0, row_h=7.05)
    para(c, "For best before end and batch number see base.", right_x, y - 5, right_w, SMALL)

    c.showPage()
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
