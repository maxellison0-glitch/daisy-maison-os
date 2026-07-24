import base64
from playwright.sync_api import sync_playwright
def b64(p): return "data:font/woff2;base64,"+base64.b64encode(open("fonts/"+p,"rb").read()).decode()
face=(
 "@font-face{font-family:'Fraunces';src:url("+b64('Fraunces-600.woff2')+") format('woff2');font-weight:600;font-style:normal}"
 "@font-face{font-family:'Fraunces';src:url("+b64('Fraunces-500i.woff2')+") format('woff2');font-weight:500;font-style:italic}"
)
def block(html):
    return ('<div style="position:absolute;top:165px;left:96px;right:96px;text-align:center;'
            'font-family:Fraunces;font-weight:600;font-size:66px;line-height:1.2;color:#F5EDE1;'
            'letter-spacing:.004em;text-shadow:0 2px 20px rgba(0,0,0,.5)">'+html+'</div>')
def ital(w): return '<span style="font-style:italic;font-weight:500">'+w+'</span>'
BEATS=[
 block("The "+ital("one")+" that doesn’t<br>end up in a drawer"),
 block("Handmade, and<br>actually "+ital("theirs")),
 block("The one and "+ital("only")),
]
HEAD="<!doctype html><html><head><meta charset=utf8><style>*{margin:0;padding:0}html,body{width:1080px;height:1920px;background:transparent}"+face+"</style></head><body><div style='position:relative;width:1080px;height:1920px'>"
TAIL="</div></body></html>"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--force-color-profile=srgb"])
    pg=b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=1)
    for i,inner in enumerate(BEATS,1):
        pg.set_content(HEAD+inner+TAIL); pg.wait_for_timeout(300)
        pg.screenshot(path="v2cap%d.png"%i,omit_background=True); print(i)
    b.close()
