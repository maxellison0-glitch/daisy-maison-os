# DM-THERMOSTAT-LAUGH (slot 1, LAUGH), 28 Sep 2026

**State: agent-pass. Prepared, NOT published.** The Higgsfield TikTok publish
session `4d7745c0-ba0a-49b1-8343-01eb20e9e7ab` needs Max to submit the form
(expires 12:50 UTC 28 Sep).

## Slot gate (CONTENT_STRATEGY.md §2b)
1. **Trio:** line 1 `THERMOSTAT ROAD` / line 2 `HANDS OFF TILL NOVEMBER` /
   hook "Dad's one rule" (white pill) + "every autumn:" (burgundy #6E1B2D).
   Cover the sign and you want to know what the rule is. The sign tells you.
2. **Presenter:** Alan (ALAN-LOCK) holds his own rule, standing by the
   thermostat in just a t-shirt. The t-shirt is part of the joke.
3. **Why:** LAUGH engine. It's timely (end of September, the heating debate
   is peaking in UK homes), aimed at adult children and partners. Scroll-stop
   = instantly recognisable dad behaviour; share mechanic = tag the one who
   guards the dial.
4. **Record check:** last 7 days were kitchen/chore rules (WASHUP, KITCHEN
   CLOSED, SOAKING LANE), SHED (Alan, 25 Sep), SPARE ROOM, SPOOKY, and
   FEEL family signs. This one uses a new joke, a new room (the hallway) and
   a new colourway (BROWN, first use in a slot). Nothing in VERDICTS rules it out.
5. **Hook burnt in** with `hook.html` → Playwright → `comp.py`, TikTok Sans
   ExtraBold 78px. It sits on his chest directly above the sign, because in
   every good take his head fills the top third. Opened and checked.

## Product (Shopify, live 28 Sep)
"Personalised Street Sign Gift — Create Your Own Custom Text" (9436230418771,
`kitchen-personalised-street-sign`). Small £18.95 / Medium £24.94 /
Large £27.94. BROWN colourway (cream face, brown border and print).

## Generation: nano_banana_2 (runs as nano_banana_flash), 2k, 9:16. 8 credits total
Refs: `street-sign-BROWN-on-cream-held-MASTER.jpg` (media 78f26d17-2c44-4322-9e20-5eee3f1c492c),
`ALAN-LOCK-black-tee-workshop-APPROVED.jpg` (media 3afea9e8-bcaf-4ed8-9e2e-4993731ed87f).
- Round 1, product ref first (fd594439-bb43-4d7a-8424-dae72af6aaf9, 8930e311-0f21-429d-90fd-a65436e370d3):
  spelled exactly, but sign/shoulder about 1.60–1.65, which **fails the 1.20–1.45 gate**.
- Round 2, scale spelled out in the prompt (21603bf4-da7f-4481-9597-84f32fdd15b4, bd7abf9f-9d41-4cbe-9334-0a9e99616dd9):
  still about 1.58, and take D drifted off Alan's face. Rejected.
- Round 3, **EDIT the Alan lock** (lock as image 1, keep the sign's size, change
  only the colourway, wording and room): 15cf95fd-c953-40cb-8374-6e3ec9f0d4d1 (~1.44),
  **3dd90967-fd6c-467d-bb46-a9db9304a473 (picked, ~1.38)**. Both spelled exactly.
  **Lesson: to get scale right, edit the lock image rather than generating a new
  scene with the lock as a reference.**
- Outpaint (2 credits, 2b78c33f-5dc1-4cc5-83d5-621151b22ce2) to buy headroom
  for the hook. It re-rendered the whole frame and turned the grey trousers
  black. Not used.

Final: `DM-THERMOSTAT-LAUGH-final.jpg`, 1080x1920 JPEG q93, Higgsfield media
65687ebc-43ef-4f05-aafe-08c19b4985bc.

## Post settings
DIRECT_POST, PHOTO, public, comments on, AIGC on, commercial disclosure off.
Music (select in form): "Polar Winds (Lofi)", Muspace Lofi, GB trending #21,
song_clip_id 7221171716369631233. The title does the joke for it.
Caption: `post-caption.txt`.
