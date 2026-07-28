# Cat advert — mastered build

`CAT-ADVERT-master.mp4` — 1080×1934, 24fps, 6.36s, silent.

## Structure
| Time | Beat |
|---|---|
| 0.0–0.30 | cold open, no graphics |
| 0.30–0.72 | hook rises in, ease-out-quint |
| 0.72–2.55 | holds; feather lowers, cat tracks it |
| 2.55–2.85 | hook leaves downward |
| 2.85–3.85 | clean beat — cat bats the feather, no graphics |
| 3.85–4.25 | payoff rises in |
| 4.9–5.16 | payoff leaves |
| 5.06–6.36 | wordmark drops in and settles |

Captions: POV-B, house native white bold (LAUGH engine → native, not the pill).
"POV: you thought it was your house" → "It isn't."

## The sign is locked, provably
The raw clip drifted **4px** and the feather crossed the sign face in the first
0.6s. Both fixed for free:
1. Trimmed the first 0.65s so the feather never occludes the product.
2. **The approved still's sign region is composited onto every single frame**
   through a feathered mask. The still aligned to the clip within 2px, so it
   drops in seamlessly.

Measured on the finished file: **x-drift 0px, y-drift 1px** (threshold noise).
The model no longer touches the product — it is our approved pixels on every
frame. This is the guarantee, not a hope.

## Two things still open
1. **The wordmark is a PLACEHOLDER**, typeset in the signs' own Times. There is
   no logo asset in this repo. Max must supply the real one.
2. **End-card placement** — it currently sits over the cat house. Better over the
   wall space to the right, or higher. Easy change, free.

Reusable builder: `Content Pipeline/templates/sign-in-situ/master-advert.py`.
