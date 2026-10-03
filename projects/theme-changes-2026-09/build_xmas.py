import re
p='layout/theme.liquid'; s=open(p).read()
old="or 'personalised-friendship-reed-diffuser-gift' -%}"
assert s.count(old)==1
s=s.replace(old,"or 'personalised-friendship-reed-diffuser-gift' or 'personalised-merry-bright-family-christmas-pebble-hanging-decoration' or 'personalised-family-festive-christmas-pebble-star-hanging-decoration' -%}")
open(p,'w').write(s)

p='snippets/dm-heart-builder.liquid'; s=open(p).read()
old="""    when 'personalised-wonderland-family-christmas-pebble-hanging-heart'
      assign dm_heart_enabled = true
      assign dm_heart_kind = 'wonderlandheart'
"""
new=old+"""    when 'personalised-merry-bright-family-christmas-pebble-hanging-decoration'
      assign dm_heart_enabled = true
      assign dm_heart_kind = 'merrybrightheart'
    when 'personalised-family-festive-christmas-pebble-star-hanging-decoration'
      assign dm_heart_enabled = true
      assign dm_heart_kind = 'festivestar'
"""
assert s.count(old)==1; s=s.replace(old,new)
start=s.index("      {%- when 'wonderlandheart' -%}"); end=s.index("      {%- when 'lovexmasfamily' -%}")
wl=s[start:end]

# Merry & Bright: its Globo form is Wonderland's schema word for word (keys, "(Large heart +£3)",
# Adult/Child/Dog/Cat, "Size 1", year question). Own heading, offer note and Globo examples.
mb=wl.replace("{%- when 'wonderlandheart' -%}","{%- when 'merrybrightheart' -%}")
for a,b in [('"heading": "Create your Wonderland Christmas heart"','"heading": "Create your Merry & Bright Christmas heart"'),
            ('"note": "Personalise another Wonderland heart at a special price"','"note": "Personalise another Merry & Bright heart at a special price"'),
            ('"placeholder": "e.g. The Smiths"','"placeholder": "e.g. The Green Family"'),
            ('"placeholder": "e.g. Merry Christmas"','"placeholder": "e.g. Daddy, Mummy, Charlie, Ollie & Charlotte"')]:
    assert a in mb, a; mb=mb.replace(a,b)
assert 'Wonderland' not in mb

# Family Festive star: four differences from Wonderland, each verbatim from its Globo form and real
# orders: size key "Size"; count suffix " (Large heart)" at 5+ and 7+; pebble types
# Adult/Teen/Child/Baby/Dog/Cat; no year question. "star" is on-page wording only.
fs=wl.replace("{%- when 'wonderlandheart' -%}","{%- when 'festivestar' -%}")
for a,b in [('"heading": "Create your Wonderland Christmas heart",','"heading": "Create your Family Festive Christmas star",\n      "itemNoun": "star",'),
            ('Five or more pebbles needs the large heart.','Five or more pebbles needs the large star.'),
            ('"note": "Personalise another Wonderland heart at a special price"','"note": "Personalise another Family Festive star at a special price"'),
            ('"label": "Add a second heart"','"label": "Add a second star"'),
            ('"helperName": "Large Decoration (second heart)"','"helperName": "Large Decoration (second star)"'),
            ('"key": "Size 1",','"key": "Size",'),
            ('"largeCountSuffix": " (Large heart +£3)"','"largeCountSuffix": " (Large heart)"'),
            ('"xlCountSuffix": " (Large heart +£5)"','"xlCountSuffix": " (Large heart)"'),
            ('"placeholder": "e.g. The Smiths"','"placeholder": "e.g. A silent night, a star above, a blessed gift of family & love xx"'),
            ('"placeholder": "e.g. Merry Christmas"','"placeholder": "e.g. Mummy, Daddy, Tia, Freddie, Mark & Stanley"'),
            ('"label": "Second heart — text above"','"label": "Second star — text above"'),
            ('"label": "Second heart — text below"','"label": "Second star — text below"')]:
    assert a in fs, a; fs=fs.replace(a,b)
n=0
for blk in re.findall(r'"types": \[\n\s+"Adult",\n\s+"Child",\n\s+"Dog",\n\s+"Cat"\n\s+\]', fs):
    lines=blk.split('\n'); pad=re.match(r'\s*',lines[1]).group(0); endpad=re.match(r'\s*',lines[-1]).group(0)
    fs=fs.replace(blk,'"types": [\n'+',\n'.join(pad+'"'+t+'"' for t in ["Adult","Teen","Child","Baby","Dog","Cat"])+'\n'+endpad+']',1); n+=1
assert n==2, n
assert fs.count('2026?')==3
fs=re.sub(r',\n\s+\{\n\s+"key": "(\(Offer\) )?Add 2026\?",.*?\n\s+\]\n\s+\}', '', fs, flags=re.S)
assert fs.count('2026')==0 or 'Christmas 2026' in fs
assert '2026?' not in fs and 'Wonderland' not in fs and 'Size 1' not in fs and '+£3)' not in fs and '+£5)' not in fs
# No gift boxes on the star: its description says 12 x 12 / 20 x 20 cm, the boxes are 10 x 10 and 14 x 18,
# and its Globo page never offered one. The gift wrap kit (dm-wrap-kits) still applies. Revisit once the
# star's real size is confirmed.
gb=fs.index(',\n      "giftBox": {')
fs=fs[:gb]+'\n'
assert 'giftBox' not in fs
s=s[:end]+mb+fs+s[end:]
open(p,'w').write(s); print('ok')
