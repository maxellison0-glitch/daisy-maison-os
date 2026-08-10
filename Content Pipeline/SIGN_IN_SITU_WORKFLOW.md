# Engineering workflow — "Sign in situ"

> ## ⛔ SUPERSEDED for anything involving the sign itself
> The validated method already exists and produced the Bond and Jannaway
> videos Max approved. **Use it, do not reinvent it:**
> `Creative Studio/REFERENCE_PACK.md` → the validated prompt chain in
> `Creative Studio/prompts/wedding-signs/cases/DM-C017-JANNAWAY/`.
>
> The approved product photograph is always reference 1. The SVG is the
> printing, never the product. §3 Step 4 below ("composite the flat PNG onto
> every frame") is **WRONG** and was written before that was understood — a
> flat vector render pasted onto footage looks like a sticker.
>
> What is still useful here: the *scene and motion* thinking (locked-off shot,
> ambient motion, one paid clip), the caption treatments, and distribution.

**Status: v2 PROPOSED — awaiting Max's approval. v1 is WITHDRAWN.**
v1 was approved on 25 Jul 2026 and produced four unusable stills within the
hour. Do not follow v1. The post-mortem is §1 because the failure is the reason
every rule below exists.

---

## 1. Post-mortem — why v1 failed

Four in-situ stills were generated (`DAD'S BAR & GRILL` ×2, `THE DOG LIVES
HERE`, `THE HARPERS`). All four were rejected on sight by Max. The signs in them
are not the Daisy Maison product — they are a generic "vintage plaque" the image
model invented from a text description.

Measured against `projects/daisy-street-sign/artwork/build.py`, the canonical
renderer whose ground truth is the audited production PSD:

| Attribute | Canonical product | What was generated |
|---|---|---|
| Proportion | **4.56:1** (570 × 125 mm) | ~3:1, squat |
| Border | `#010101`, uniform 12.4 mm inset | grey/charcoal-brown, arbitrary |
| Corner profile | the real **409-vertex LightBurn cut contour** | invented scalloped/ogee |
| Mounting holes | two, at real coordinates | none; decorative dots instead |
| Typography | Times New Roman regular, vertical scale 1.4, tracking 0, line 1 fitted to 486 mm | unidentified serif, wrong weight and fit |
| Heart | real PSD raster, tip inset 3 px into the ampersand upstroke | absent |

**Root causes**

1. **A generative model was allowed to draw the product.** Every generation
   redraws it, so every generation is a different product. Fidelity was never
   possible by this route.
2. **The house method that already works was ignored.** The diffuser stills that
   succeeded used *"EDIT THIS PHOTOGRAPH… keep the product 100 % unchanged and
   pixel-faithful… change ONLY the background."* v1 switched to text-to-image.
3. **No fidelity gate existed.** v1 checked motion for AI-slop tells and never
   checked that the product was ours. Four generations were fired before
   anything was inspected.
4. **Wording was invented for unvalidated templates.** `scripts/README.md` states
   only the **Large Mr & Mrs template (SKU 36961)** is supported and that other
   templates "should be added only after their physical production templates are
   validated." `DAD'S BAR & GRILL` and `THE DOG LIVES HERE` may not be real
   products. The canonical render makes the error visible: it places the
   **wedding heart at the ampersand of a bar sign**.

---

## 2. The rule that replaces all of it

> **The sign is never generated. It is rendered by `build.py` and composited.**

A generative model may produce the *scene*. It may never produce the *product*.
There is no prompt wording that makes this safe — the fix is architectural, not
lexical.

## 3. The production line

**Step 0 — Product check (blocking).**
Confirm the wording corresponds to a **validated template**. Today that is the
Large Mr & Mrs only. Anything else requires Max to confirm the product exists
and the template is validated. Do not proceed on an assumption.

**Step 1 — Render the sign face (free, exact).**
```
python3 projects/daisy-street-sign/artwork/build.py <order> "<LINE 1>" "<LINE 2>" 486 out.svg
```
Rasterise the SVG to PNG with alpha. Deterministic, any wording, zero credits.
*Known constraint:* the heart is bound to the ampersand as the Mr & Mrs
signature unit. Non-wedding wording containing "&" will wrongly receive it —
another reason Step 0 blocks.

**Step 2 — Generate the scene, with NO sign in it.**
Prompt the empty setting only — garden fence, hallway wall, brickwork beside a
door — with a clear, flat, well-lit mounting surface and honest perspective. The
model never sees a sign and is never asked to draw one. Explicitly negative-
prompt signs, plaques and lettering.

**Step 3 — Animate the empty scene (the paid step).**
Locked-off camera, ambient motion only (smoke, a dog, a cat, leaves, firelight).
~10 credits on `minimax_hailuo` at 1080. Still no sign present.

**Step 4 — Composite the canonical sign onto every frame (free, exact).**
Because the shot is locked off, the sign is a static overlay: perspective-
transform once, then apply to all frames. Match lighting with a multiply shadow
and match grain/focus to the plate.
**This is the step that makes drift impossible.** The sign cannot warp,
shimmer or re-letter, because it is our PNG on every frame rather than something
the model redraws 144 times.

**Step 5 — Verify against canon (blocking, automated).**

⚠️ **This gate was wrong as first written and would have failed our own approved
asset.** Alan measured the sign in the approved cat clip at **515 × 138 px =
3.73:1** against a canonical 4.56:1 — the difference is genuine foreshortening on
a wall-mounted sign, not a defect. And at 138 px tall a real mounting hole is
about 2 px, so "both holes present" is unassertable. Never assert canonical
geometry on a raw in-situ frame.

Corrected gate — **rectify the sign region back to a rectangle using the known
wall quad first, then assert on the rectified plate:**
- rectified aspect ratio within **±1.5%** of 4.56:1
- ink within a ΔE tolerance of the chosen colourway **after white-balance
  normalisation** (the plate carries the room's colour temperature)
- wording an exact character-for-character string match
- heart present **iff** `SIGN_HEART=1`
- mounting holes checked **only** where the rectified plate is ≥400 px wide

Plus a motion gate on the clip: **sign bounding-box drift ≤ 1 px across every
frame.** The approved cat clip achieves 0 px (x 296–811, y 535–673, identical at
t=1.0 and t=4.5). That is the bar and it is provably achievable.

Fail any check → back to Step 4. Never "it's close enough".

**Step 6 — Caption in post** — `templates/hook-frames/caption-overlay.py`.
LAUGH → house native bold white. FEEL/premium → cream pill. Beat 1 ≤ 7 words.
If there is a reveal, the hook clears before the payoff is legible.

**Step 7 — Deliver file + caption in chat.** Max posts manually. Trending audio
added in-app; AI-content label on whenever synthetic imagery appears.

## 4. Spend discipline

- **One probe, then verify, then batch.** Never fire a batch before a single
  result has been inspected. v1 spent 8 credits on four unusable stills.
- Preflight every job with `get_cost:true`.
- Costs: scene still ~2 credits; in-situ clip ~10 at 1080 (~4–4.8 on the budget
  tier). Steps 1, 4 and 6 are free. A finished ad is **~12 credits**.

## 5. What survives from v1

These were not implicated in the failure and still stand:

- **"Type it → make it real"** (`templates/sign-in-situ/build-typereal.py`) —
  configurator → real scene → CTA. Its sign preview already renders locally, so
  it is compatible with §2. It should be switched from its own plate drawing to
  `build.py` output for exactness.
- **Caption treatments and placement rules** (`templates/hook-frames/`).
- **Distribution:** one 9:16 silent master serves Instagram, Facebook, TikTok
  and YouTube.
- **The cat clip is unaffected** — its sign came from an earlier pipeline, not
  from v1, and Max has already judged it good.

## 6. Idea bank — REVISED

Every idea below is **blocked at Step 0** until Max confirms the template is a
real, validated product. Only the Mr & Mrs line is currently validated.

**Step-0 blocks RESOLVED 25 Jul 2026.** Freya checked the live catalogue rather
than assuming, and arbitrary wording *is* a real product:

- **SKU 36967 — "Create Your Own Custom Text"**, active, £18.95, up to two lines.
- `DAD'S BAR & GRILL` is its own SKU (**88071**, £11.25, 1,139 sold).
- `FAMILY` (36965, 2,072 sold), `HOUSE RULES` (36963), `HOME` (**38827, single
  line** — so one-line signs are sellable), football create-your-own (89397).
- Colourways are a listed product option — five of them, now locked in
  `artwork/colourways/README.md`.
- `I'M SEXY & I MOW IT` (36926) is live, so cheeky is already the house register.

The `&`-triggers-the-heart problem is fixed separately by `SIGN_HEART=0`.

| # | Engine | Wording | Scene + ambient motion | Status |
|---|---|---|---|---|
| 1 | LAUGH | `MURPHY'S LAW` / *if it's on the floor, it's mine* | Boot room, **settled** dog lifts its head | **Approved** — Black |
| 2 | LAUGH | `THE CAT'S HOUSE` / *you just pay the mortgage* | Cat house, slow blink | **Approved** — Black |
| 3 | FEEL | `THE HARPERS` / `EST. 2026` | Hallway, traffic passing **beside** the sign | **Approved** — Sage |
| 4 | LAUGH | `DAD'S BAR & GRILL` / *burnt to order* | Fence, BBQ smoke | Parked — Max returning to it |
| 5 | FEEL | seasonal, mantelpiece + firelight | Christmas ramp | Build in August |

**Occlusion rule (Alan, non-negotiable):** nothing may cross *in front of* the
sign. The instant a walker occludes the plate it stops being a locked overlay and
the model must redraw our product for those frames — the expensive tier plus
reintroduced drift risk, to buy a moment nobody notices. Choreograph animals and
people to pass **below or beside** the sign. Free, and it protects the only
fidelity guarantee we have.

## 7. Hard rules

- The sign is rendered, never generated. No exceptions.
- No filming, no presenter (`CONTENT_BRIEF_GATE.md`).
- Step 0 and Step 5 are **blocking gates**, not advisory.
- One probe before any batch.
- Organic social posts publish autonomously. No paid spend without Max's explicit go.
