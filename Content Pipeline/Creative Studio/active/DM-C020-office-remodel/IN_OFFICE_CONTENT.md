# In-office content — the first three matched pairs

Max, 28 Jul 2026: *"Think about what this is actually being posted to before you
even make the sign. Literally think of an on-screen hook to match it… It can't
just be some bullshit that people wouldn't actually have in their house, like
'day four of summer holidays.' No one's buying that."*

He is right, and the sales data says why.

---

## 1. Who actually buys — from Shopify, trailing 365 days

| Product | Orders | Gross |
|---|---|---|
| Personalised **Mr & Mrs** street sign | **4,558** | £58,692 |
| **Large Street Sign** (custom wording) | 4,187 | £27,653 |
| Personalised **Valentine's** street sign | 2,203 | £33,146 |
| Personalised **Family name** street sign | 1,540 | £22,254 |
| **Dad Bar & Grill** street sign | 817 | £9,884 |
| **Football Stadium** street sign | 587 | £6,691 |
| **Number Plate** sign | 408 | £5,007 |
| **Retirement** street sign | 214 | £4,051 |

**The read: this is an occasion-gift audience, not a home-decor audience.** They
are buying *for* someone — a couple, a dad, a family, a fan, a colleague leaving.
Nobody browses for a sign; they arrive with a person and a date in mind.

Which is exactly why *"THE SUMMER HOLIDAYS — DAY 4 OF 42"* dies. It is an
observation, not a gift. There is no one to give it to and no occasion to give it
on. **Every sign that goes in a reel has to be a thing someone would hand over.**

Second read, worth keeping in view: the pebble pictures are enormous (Mum
£37.7k / 1,251 orders, Wedding £29.3k / 1,375). Signs are the format we can film;
they are not the whole business.

---

## 2. The three engines, mapped to what sells

Per `CONTENT_STRATEGY.md` §3, every sign maps to one engine, and the engine
decides the hook and the metric.

| Engine | The sellers it covers | The job |
|---|---|---|
| **FEEL** | Mr & Mrs (4,558), Valentine's (2,203) | saves + gifting intent |
| **LAUGH** | Large custom (4,187), home bar, family "rules" | reach + shares + tags |
| **SOLVE** | Dad Bar & Grill (817), Stadium (587), Retirement (214) | link clicks, "what do I get him" |

One concept per engine, below. Each is a matched pair — cover the sign and the
hook should still make you need to see it.

---

## 3. The three concepts

### A — FEEL. "MR & MRS PRESTON"

**Platform:** Instagram Reels first, TikTok second. Saves-led.

**On-screen hook (frame 1):**
> the only note on this order was
> **"don't send it to the house"**

**The turn:** Alan holds it square to camera, deadpan.
**Sign:** `MR & MRS PRESTON` / `SHE SAID YES 12TH JULY 2026`

**Why it works.** The hook opens a loop with one detail and no explanation — *why
can't it go to the house?* The sign closes it: she doesn't know yet. It reframes
the whole thing as a proposal gift in under two seconds, and it lands on the
single biggest-selling product in the shop. It also does something a plain
product shot cannot: it makes the buyer the interesting person in the story.

**Caption:** *He ordered it three weeks early so it would be sitting there when
she said yes. Personalised street signs, made in our unit.*

**Working images:** `working/ideas-A-preston/`

---

### B — SOLVE. "DAVE'S BAR & GRILL"

**Platform:** TikTok first (search-led — "gifts for dad" is a query, not a mood),
Reels second.

**On-screen hook (frame 1):**
> he said he didn't want anything this year

**The turn:** Alan holds it, completely unbothered.
**Sign:** `DAVE'S BAR & GRILL` / `BURGERS BEER AND BAD JOKES`

**Why it works.** "He said he didn't want anything" is the single most universal
sentence in British gift-buying, and it is a *problem* — the SOLVE engine's whole
job. The sign is the answer, and it is a real top-ten seller at 817 orders. The
name is swappable, which makes this one template we can run all autumn with a
different name each time.

**Caption:** *Dads who "don't want anything" always want this one. Any name,
any wording.*

**Working images:** `working/ideas-B-bargrill/`

---

### C — LAUGH. "THE JOHNSON ARMS" (the two-hander)

**Platform:** Reels + TikTok. Shares-led — this is the dark-social one.

**On-screen hook (frame 1):**
> POV: your dad has converted the shed

**The turn:** Alan holds it deadpan to camera while Freya crosses behind
mid-stride with an armful of blanks, clocking the camera on her way past.

**Sign:** `THE JOHNSON ARMS` / `LANDLORD DAD - LAST ORDERS NEVER`

**Why it works.** Two jokes stacked. The sign is the punchline to the hook; the
woman walking through the shot is the punchline to the *format* — it reads as a
real workplace where someone is trying to take a photo and a colleague has walked
into it. That second layer is the thing you cannot buy with a stock photo, and it
is the entire reason the office set was worth building.

Home-bar signs are the biggest slice of the 4,187 custom-wording orders, and this
is the most tagged-in-comments category we have.

**Caption:** *Every shed in Britain is one sign away from being a pub.
Tag the landlord.*

**Working images:** `working/ideas-C-johnsonarms/`

---

## 3a. Max's review, 28 Jul — and the mistake that caused it

**The scale reference was approved and then not used.** Max approved
`cast-C-freya-packing-bay/take-03` specifically as the scale reference — *"the
size is a really good size… can be used for anyone"*. These three batches were
generated against the empty room plates and the character locks instead, so
scale went back to being a lottery. His question — *"Have you used the one that
I said to use? It doesn't look like you have"* — is correct, and it is the whole
reason the signs came back oversized.

**The gate was also wrong.** See `prompts/CHARACTER-LOCK-SYSTEM.txt`: the rule is
now *the sign's ends must not extend past the outer edge of his arms*, not a
width ratio. `ideas-B-bargrill/take-02` is the reference for correct scale.

| Image | Verdict against the arm line |
|---|---|
| **B/02** | ends land at his arms, hands not stretched — **the standard** |
| C/04, C/01 | ends just outside — usable |
| A/01, A/03, A/04 | ends far outside the body on both sides — too big |
| B/01, B/03, B/04 | ends past the right arm — too big |
| C/02 | widest of the eleven — *"a fucking massive image"* |

**And the filtering is the agent's job, not Max's.** Four takes come from one
prompt; the variance is the model's. Showing all four and asking which look real
pushes a QC pass onto him that should have happened first. From here: measure
against the arm line, drop the failures, show what survives.

**On the concepts themselves — too basic.** Max: *"It all sounds a bit boring…
genuinely too basic."* The positioning and the characters he rated well; the
ideas he did not. That critique is addressed in section 6.

## 4. What the run proved technically

**Wording swaps off the lock work cleanly.** Three completely new wordings, all
spelled correctly on every take, against a lock that reads MR & MRS JANNAWAY.
The instruction that did it: *"IGNORE THE WORDING PRINTED ON THE SIGN IN IMAGE 2
- the wording below replaces it completely."* Without that line the lock's own
wording is what you get.

**No mounting holes came through on any of the twelve.** Same locks as the cast
run. The difference is that this time the product block described the panel as a
finished printed object with no reference to holes at all, rather than saying
"NO MOUNTING HOLES". Naming a thing you do not want appears to summon it;
describing what the panel *is* does not. That is consistent with the wider rule
in `CHARACTER-LOCK-SYSTEM.txt` — describe, do not negate.

**Asking for an off-axis camera tilts the product, not the camera.** Batch B was
told *"the camera is a little off-axis and low, the way a phone snapshot taken
quickly by a colleague actually is"*. The camera stayed put and the **sign** came
back rotated on all four takes. This is the same failure as the office plates:
**constraints on the camera do not survive; they get applied to the content
instead.** If a candid angle is wanted, it has to come from the room plate, not
from a sentence.

---

## 5. The bank — next matched pairs, not yet built

| Engine | Hook | Sign | Occasion |
|---|---|---|---|
| SOLVE | *"his team have been relegated twice"* | `HARRISON STADIUM` / `EST. 1994 - STILL BELIEVING` | birthday, Father's Day |
| FEEL | *"she kept the receipt from their first date"* | `MR & MRS BAILEY` / `WHERE IT ALL STARTED 2019` | anniversary |
| LAUGH | *"my wife said the kitchen needed a sign"* | `THE ARMSTRONG KITCHEN` / `HEAD CHEF - MUM` | housewarming |
| SOLVE | *"forty-one years at the same company"* | `PAULINE'S RETREAT` / `RETIRED 2026 - GONE FISHING` | retirement, 214 orders |
| FEEL | *"first Christmas in the new place"* | `THE WHITTAKERS` / `EST. 2026 - HOME AT LAST` | Christmas, new home |

Each follows the same rule: a person, an occasion, and a name someone would
actually hand over.

---

## 6. Why the first three were basic, and what replaces them

Max, 28 Jul: *"It all sounds a bit boring… genuinely too basic."*

**The diagnosis: all three were adverts.** Earnest setup, product answer,
brand voice. *"He said he didn't want anything this year"* is a line every
personalised-gift account in the country has already posted.

The account's own best-performing post is not an advert. It is
**documentary**: *"Customer of the year, probably"* → `YOU'RE NOT WELCOME
(UNLESS YOU'VE BROUGHT SNACKS)` — 11,889 views against 4–7 likes on recent
posts. The joke was not written by the brand. It was **ordered by a customer**,
and the brand just held it up.

That reframes what Alan and Freya are for. They are not models holding stock.
**They are the staff who have to make whatever gets ordered** — and the comedy
is what does or doesn't cross their faces. A deadpan man holding something
ridiculous needs no hook line at all.

It also unlocks the one thing no competitor can copy: **two characters in a
real workshop having a relationship**, told entirely in signs.

### The four replacements

**1. THE CORRECTION — two signs, one house, no caption.**
Alan holds `DAD'S BAR` / *EST. 2019 · NO ENTRY WITHOUT SNACKS*. Freya walks
through behind him holding the second sign from the same order:
`DAD'S BAR` / *IT'S A SHED, DAVE*. She is not passing by accident. She is
correcting him. Sells two signs in one frame, needs no on-screen hook, and is
impossible without the set and both characters. **The least basic thing we can
make.**

**2. WE DON'T ASK — documentary register, the proven formula.**
No POV, no setup. Alan deadpan, caption only: *we don't ask what it's for.*
Sign: `KEITH'S SECOND FRIDGE` / *GARAGE · BEER ONLY*. Oddly specific, entirely
plausible as a real order, and the specificity is the joke. This is the closest
thing to the 11,889-view post's actual mechanic.

**3. DAD'S TAXI — the commercial one.**
Hook is a memory, not a sales line: *you're 15, it's raining, and he's outside
beeping.* Sign: `DAD'S TAXI` / *NO FARES PAID SINCE 2009*. Nostalgia then
laugh, aimed straight at the 817-order dad category. The most likely to convert
of the four.

**4. READ IT BACK — needs two frames or video.**
Every sign gets checked before it's packed. Freya reads one out; Alan doesn't
react. Her face is frame one, his non-reaction is frame two. Holds for a
carousel or a 6-second turnaround.

All four keep the rule that killed *"day 4 of 42"*: a person, an occasion, and
a name someone would actually hand over.

## 7. THE CORRECTION — built, one frame approved

Max picked concept 1 to shoot first. Four takes, 8 credits, with
`ideas-B-bargrill/take-02` attached as an explicit SIZE AUTHORITY reference.

**Approved: take 2.** Max: *"They all looked very large. I'd say the most valid
was probably 2. It looks more like a medium street sign, which is fine, so
that's valid… the rest came out weird."*

`working/correction-01-daves-bar/outputs/take-02.png`

**What that proves about scale.** A correctly sized reference plus the size rule
written twice into the prompt got one of four. Better than the lottery, not a
fix. Generate four, keep one, and expect that ratio.

## Status

| | |
|---|---|
| Concepts | three original (rejected as basic) + four replacements |
| Images | 11 idea takes + 4 Correction takes |
| Approved | **`correction-01-daves-bar/take-02`** — the lead Correction frame |
| Not done | on-screen hook text rendered onto frames; the turnaround video |
| Still unbuilt | "We Don't Ask", "Dad's Taxi", "Read It Back" |
