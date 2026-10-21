import sys
from PIL import Image
import numpy as np
src=Image.open(sys.argv[1]).convert("RGB"); out=sys.argv[2]
W,H=1080,1920
img=src.resize((1080, round(src.height*1080/src.width)), Image.LANCZOS)
top=H-img.height
a=np.asarray(img).astype(float)
band=a[:40].reshape(-1,3); col=np.median(band,axis=0)
canvas=np.zeros((H,W,3)); canvas[:]=col
# per-column colour of top band for a seamless continuation
colcol=a[:30].mean(axis=0)  # (W,3)
for y in range(top):
    t=y/top
    canvas[y]=col*(1-t)+colcol*t
canvas[top:]=a
# soft blend seam over 60px
for i in range(60):
    t=i/60; y=top+i
    canvas[y]=colcol*(1-t)+a[i]*t
base=Image.fromarray(canvas.clip(0,255).astype('uint8'))
hook=Image.open("hook.png").convert("RGBA")
base=base.convert("RGBA"); base.alpha_composite(hook)
base.convert("RGB").save(out,"JPEG",quality=93,subsampling=0)
print(top)
