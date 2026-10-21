# Resize a 9:16 take to 1080x1920, burn in hook.png, save JPEG. Zero credits.
import sys
from PIL import Image
src = Image.open(sys.argv[1]).convert("RGB")
W, H = 1080, 1920
# cover-fit: scale to fill, centre-crop the few px of rounding
s = max(W / src.width, H / src.height)
img = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
l, t = (img.width - W) // 2, (img.height - H) // 2
img = img.crop((l, t, l + W, t + H)).convert("RGBA")
img.alpha_composite(Image.open("hook.png").convert("RGBA"))
img.convert("RGB").save(sys.argv[2], "JPEG", quality=93, subsampling=0)
