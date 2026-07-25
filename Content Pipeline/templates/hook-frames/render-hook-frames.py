import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright

BROWN="#5C463A"; FACE="#FBF8F2"; HEART="#C0544A"; CREAM=(237,230,219)

def b64(p): return "data:font/woff2;base64,"+base64.b64encode(open("fonts/"+p,"rb").read()).decode()
FACES=("@font-face{font-family:'TTS';src:url("+b64('TikTokSans-ExtraBold.woff2')+") format('woff2');font-weight:800}"
 "@font-face{font-family:'Fr';src:url("+b64('Fraunces-600.woff2')+") format('woff2');font-weight:600;font-style:normal}"
 "@font-face{font-family:'Fr';src:url("+b64('Fraunces-500i.woff2')+") format('woff2');font-weight:500;font-style:italic}")
HEAD=("<!doctype html><html><head><meta charset=utf8><style>*{margin:0;padding:0}"
      "html,body{width:1080px;height:1920px;background:transparent}"+FACES+"</style></head>"
      "<body><div style='position:relative;width:1080px;height:1920px'>")
TAIL="</div></body></html>"

def native(t,top,size=56,col="#fff"):
    return (f"<div style=\"position:absolute;top:{top}px;left:70px;right:70px;text-align:center;"
            f"font-family:TTS;font-weight:800;font-size:{size}px;line-height:1.2;color:{col};letter-spacing:-.005em;"
            f"text-shadow:0 2px 5px rgba(0,0,0,.6),0 0 24px rgba(0,0,0,.4)\">{t}</div>")
def edit(t,top,size=62,col="#F5EDE1",sh=True):
    s="text-shadow:0 2px 20px rgba(0,0,0,.5);" if sh else ""
    return (f"<div style=\"position:absolute;top:{top}px;left:96px;right:96px;text-align:center;"
            f"font-family:Fr;font-weight:600;font-size:{size}px;line-height:1.22;color:{col};letter-spacing:.004em;{s}\">{t}</div>")
def it(w): return f'<span style="font-style:italic;font-weight:500">{w}</span>'

OV={
 "i1":  native("POV: you asked<br>what&rsquo;s for dinner", 700),
 "i2n": native("This surname didn&rsquo;t<br>exist last summer.", 600),
 "i2e": edit("This surname didn&rsquo;t<br>exist "+it("last summer"), 230, 60, BROWN, sh=False),
 "i3h": edit("For the mate who says<br>&ldquo;honestly, "+it("don&rsquo;t")+" get me anything&rdquo;", 200, 55),
 "i3p": edit("Fine. Something with<br>their "+it("name")+" on it, then.", 200, 60),
}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=1)
    for k,h in OV.items():
        pg.set_content(HEAD+h+TAIL); pg.wait_for_timeout(250)
        pg.screenshot(path=f"o_{k}.png",omit_background=True)
    b.close()

def to916(path):
    im=Image.open(path).convert("RGB"); w,h=im.size; tw=int(h*9/16)
    if tw<=w: im=im.crop(((w-tw)//2,0,(w-tw)//2+tw,h))
    else:
        th=int(w*16/9); im=im.crop((0,(h-th)//2,w,(h-th)//2+th))
    return im.resize((1080,1920),Image.LANCZOS)

def padded(path,y=520):
    """square/near-square photo padded into 9:16 on cream — premium reel layout"""
    bg=Image.new("RGB",(1080,1920),CREAM)
    im=Image.open(path).convert("RGB")
    w,h=im.size; nh=int(1080*h/w)
    bg.paste(im.resize((1080,nh),Image.LANCZOS),(0,y))
    return bg

def over(bg,ovp,out):
    o=Image.open(ovp).convert("RGBA")
    Image.alpha_composite(bg.convert("RGBA"),o).convert("RGB").save(out,quality=94)

# --- Idea 1: type-treatment preview on neutral slate (footage not filmed) ----
sl=Image.new("RGB",(1080,1920),(46,42,40))
d=ImageDraw.Draw(sl)
for i in range(1920):  # subtle vertical warmth
    d.line([(0,i),(1080,i)],fill=(46+int(i/1920*14),42+int(i/1920*11),40+int(i/1920*9)))
over(sl,"o_i1.png","F_i1_hook.jpg")

# --- Idea 2: real wedding sign photo, both treatments ------------------------
over(padded("base/wedding.jpg",520),"o_i2n.png","F_i2_hook_native.jpg")
over(padded("base/wedding.jpg",620),"o_i2e.png","F_i2_hook_edit.jpg")

# --- Idea 3: real diffuser assets -------------------------------------------
over(to916("base/box.jpg"),"o_i3h.png","F_i3_hook.jpg")
over(to916("base/bottle.jpg"),"o_i3p.png","F_i3_pay.jpg")

# --- accurate sign-face wording mock ---------------------------------------
def fit(d,txt,path,maxw,start):
    s=start
    while s>12:
        f=ImageFont.truetype(path,s)
        if d.textlength(txt,font=f)<=maxw: return f
        s-=2
    return ImageFont.truetype(path,12)

def plate(main_l,main_r,sub,heart,W=1020,H=250):
    im=Image.new("RGB",(W,H),BROWN); d=ImageDraw.Draw(im)
    b=16
    d.rectangle([b,b,W-b-1,H-b-1],fill=FACE)
    n=34
    for (cx,cy,dx,dy) in [(0,0,1,1),(W,0,-1,1),(0,H,1,-1),(W,H,-1,-1)]:
        d.polygon([(cx,cy),(cx+dx*n,cy),(cx,cy+dy*n)],fill=BROWN)
    for x in (b+18,W-b-18):
        d.ellipse([x-3,H//2-3,x+3,H//2+3],fill=BROWN)
    inner=W-2*b-70
    full=main_l+("  " if heart else "")+main_r
    fm=fit(d,full,"fonts/times.ttf",inner,116)
    wl=d.textlength(main_l,font=fm); wr=d.textlength(main_r,font=fm)
    hf=ImageFont.truetype("fonts/times.ttf",int(fm.size*0.42)) if heart else None
    wh=(d.textlength("♥",font=hf)+22) if heart else d.textlength(" ",font=fm)
    total=wl+wh+wr
    x=(W-total)/2; y=42
    d.text((x,y),main_l,font=fm,fill=BROWN)
    if heart:
        d.text((x+wl+11,y+fm.size*0.20),"♥",font=hf,fill=HEART)
    d.text((x+wl+wh,y),main_r,font=fm,fill=BROWN)
    fs=fit(d,sub,"fonts/times.ttf",inner,46)
    d.text(((W-d.textlength(sub,font=fs))/2,y+fm.size+10),sub,font=fs,fill=BROWN)
    return im

def payoff(pl,out):
    bg=Image.new("RGB",(1080,1920),CREAM)
    pw=980; ph=int(pl.height*pw/pl.width)
    p=pl.resize((pw,ph),Image.LANCZOS)
    top=(1920-ph)//2 - 60
    sh=Image.new("RGBA",(1080,1920),(0,0,0,0))
    ImageDraw.Draw(sh).rectangle([(1080-pw)//2+8,top+16,(1080-pw)//2+pw+8,top+ph+16],fill=(70,55,45,70))
    bg=Image.alpha_composite(bg.convert("RGBA"),sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB")
    bg.paste(p,((1080-pw)//2,top))
    bg.save(out,quality=94)

payoff(plate("MUM'S","KITCHEN","(IT'S THIS OR NOTHING, AND IT'S LOVELY)",False),"F_i1_pay.jpg")
payoff(plate("MR &","MRS HALE","EST. 2026",True),"F_i2_pay.jpg")
print("ok")
