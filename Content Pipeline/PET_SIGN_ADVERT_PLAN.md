# Pet-sign advert plan — the template, and the dog version

**Status: PROPOSED. Nothing else gets generated until Max approves.**
Two cat clips are already rendering (20 credits). Everything below is costed but
unspent.

---

## 1. The template that now works (proven today)

| Step | What | Cost |
|---|---|---|
| 1 | `build.py` renders the sign face — any wording, any real colourway | **free** |
| 2 | Printing swapped onto a **wall-mounted master** via the validated print-edit | ~6 cr |
| 3 | Animate: locked-off camera, sign static, **only the animal and a toy move** | ~10 cr |
| 4 | Hook captions, logo, mastering — all local | **free** |

**The unlock was step 2.** Earlier attempts generated an empty wall and asked the
model to mount a sign on it — it invented placement, scale and lighting and
failed three times. The fix: a frame from Max's own cat clip is now the
**wall-mounted reference master**, so the sign is already correctly mounted, sized
and lit, and the model only has to swap the printing. Same operation that produced
Hale and Harpers.

`Creative Studio/reference-masters/` now holds two masters:
- `street-sign-BLACK-on-white-MASTER.jpg` — sign **held**, for product shots
- **wall-mounted master** (cat-clip frame) — sign **on a wall**, for in-situ

## 2. The advert structure — 7 seconds, beat by beat

Timings are the point. This is what separates "high-end mastered" from adequate.

| Time | Beat |
|---|---|
| 0.0–0.3 | Cold open on the room. Sign already there, cat settled. No graphics. |
| **0.3–0.7** | **Hook masks up** into the wall space above the sign — eased translate + tiny scale settle. Not a fade. |
| 0.7–2.6 | Hook holds. Feather toy lowers into frame on its string. Cat tracks it. |
| 2.6–2.9 | Hook masks away, downward, same easing. |
| 2.9–4.6 | Cat bats at the feather, twice. Clean beat, no graphics — let it be charming. |
| **4.6–5.0** | Payoff caption masks up. |
| 5.0–5.9 | Payoff holds over the cat settling. |
| 5.9–6.2 | Payoff clears. |
| **6.2–7.0** | **Daisy Maison logo drops in** from above with a soft settle, letterspacing tightening as it lands. Holds. |
| 7.0 | Cut back to frame 0 so it loops seamlessly — TikTok pays for loops. |

**Motion rules (the actual craft):**
- Every move eased (ease-out-quint ~0.35s). **Nothing linear, ever.**
- Captions mask-reveal, not fade. Scale 0.96 → 1.00 with a 1–2% overshoot.
- Logo drops with one soft settle, no bounce-castle wobble.
- **The footage never moves.** Locked-off plate; only graphics animate. This is
  the rule that keeps it off the AI-slop list.
- Silent master; audio and a licensed feather-swish added in post.

## 3. Hook options — cat

| | Beat 1 | Beat 2 |
|---|---|---|
| **A** *(Freya's)* | "It's not your house." | "He knows." |
| B | "He pays nothing." | "He owns everything." |
| C | "Whose house is it, really?" | *let the sign answer — no beat 2* |

C is the boldest: it trusts the sign to land the joke and keeps the screen clean.

## 4. The dog version — three scene options

Sign: **`MURPHY'S LAW` / `IF IT'S ON THE FLOOR, IT'S MINE`**, Black, already
rendered and approved.

The problem to solve: our wall-mounted master is a *cat* scene. So the dog needs
either a scene change on top of the printing swap (slightly riskier), or its own
master. Options, cheapest first:

| | Scene | The engaging beat | Risk |
|---|---|---|---|
| **D1** | Boot room, dog settled on a bed, sign on the wall above | **A hand enters frame to lift a lead off a hook** — dog's ears prick and head lifts. Hand stays low, never crosses the sign. | Hand is the risk; crop it to forearm only |
| **D2** | Same boot room | **A tennis ball rolls slowly into frame** — dog's eyes track it, head follows | Safest motion in the set. No anatomy to break |
| **D3** | Same boot room | Dog simply lifts its head and yawns, light shifting | Dullest, but bulletproof |

**My recommendation: D2.** It gives the same "something engages the animal" beat
Max liked, with none of the hand/gait risk. A rolling ball is rigid-body motion —
the one thing these models never get wrong. D1 second if he wants a human present.

Dog hooks:
| | Beat 1 | Beat 2 |
|---|---|---|
| **A** | "House rules, written by the dog." | "He wrote them himself." |
| B | "Whose floor is it?" | "Ask him." |
| C | "He has one rule." | *sign answers* |

## 5. The gap I need Max to close: there is no logo file

**Searched the whole repo — there is no Daisy Maison logo, wordmark or monogram
asset anywhere.** For "the logo drops in" I need the real thing. Options:

1. **Max supplies the logo** (PNG/SVG with transparency) — best, and correct.
2. I lift the `HOME BY DAISY MAISON` / `DS` lockup from the diffuser label
   artwork already in the repo — workable, but it is a *product label*, not
   necessarily the brand logo.
3. I typeset a wordmark in Times to match the signs — fast, but I would be
   inventing brand identity, which is not my call.

**Option 1 unless told otherwise. I will not invent a logo.**

## 6. Costs to finish

| Item | Cost |
|---|---|
| Cat clips (already running) | 20 cr *(spent)* |
| Dog: printing swap onto a boot-room wall scene, 3-up | 6 cr |
| Dog: ambient clip | 10 cr |
| Captions, logo animation, mastering, both films | **free** |
| **To finish both adverts** | **~16 cr more** |

Balance is ~1,100, so cost is not the constraint. Approval is.

## 7. What I need from Max

1. **The logo file** (or permission to use the diffuser `DS` lockup).
2. **Hook choice** — cat and dog, or tell me to pick.
3. **Dog scene** — D1, D2 or D3. I recommend D2.
4. **Go** for the 16 credits.
