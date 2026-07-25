# Engineering workflow — "Sign in situ" & "Type it → make it real"

**Status: APPROVED by Max, 25 Jul 2026.** This is now the default way we make
video. Changes to it need his sign-off.

---

## 1. The discovery (why this replaces turnaround videos as the default)

The cat clip (`PUSSY PALACE` sign on a wall above a cat house) was made on
**`minimax_hailuo`**, not Seedance. Compare the real preflight costs for one
9:16 clip:

| Route | Model | Spec | Credits |
|---|---|---|---|
| Sign in situ | **minimax_hailuo** | 6s **1080** (cat quality) | **10** |
| Sign in situ, budget tier | minimax-2.3-fast / veo3_1_lite / seedance1_5 | 4–6s, 768/720p | 4 – 4.8 |
| In-situ still (nano_banana_pro) | — | 1k, 9:16 | 2 |
| Synthetic turnaround (identity-locked) | seedance_2_0 | 5s 720p | 22.5 |

**A finished in-situ ad = still (2) + clip (10) = ~12 credits at cat quality**, or
~6–7 on the budget tier. That is roughly **half** a Seedance turnaround, not a
fifth — an earlier draft of this doc quoted 4 credits from a 768/fast preflight
and understated it. Corrected here.

**Still the better default, and arguably better content.** A sign living in a real room —
above a cat house, on a fence, by a front door — is more relatable and more
shareable than a man rotating a plaque in a workshop. It also needs no
presenter, which matters because **Max does not film** (see
`CONTENT_BRIEF_GATE.md`).

The second half of the saving: the **configurator and CTA cards cost nothing.**
They are HTML/Playwright renders, not generations — so the whole story wrapper
is free, and only the one in-situ clip is ever paid for.

## 2. The two formats

### Format A — Sign in situ (simplest, ~12 credits at cat quality)
One continuous ambient shot. The sign is **razor-sharp and static**; the motion
comes from something *else* in frame.

- The sign never moves, never warps, never re-renders. State this explicitly in
  the prompt — it is the single most important instruction.
- Motion budget goes to one ambient element: a cat, a feather toy on a string,
  BBQ smoke, a lawnmower crossing the lawn, a curtain, firelight.
- Camera locked off or near-static. No fake Ken-Burns.
- Our two-beat caption goes on in post (never model-burned).

### Format B — Type it → make it real (same ~12 credits, higher perceived effort)
Format A wrapped in a configurator story. This is the DM-C006 Potter structure,
now rebuilt cross-platform in `templates/sign-in-situ/build-typereal.py`.

1. **Configurator (≈2.9s, 0 credits).** Cream screen: `DAISY MAISON` /
   "Make it theirs." / "Personalise the sign as you order" / an input field that
   **types the wording live** with a blinking caret, and a sign plate preview
   that fills in as it types. Rendered locally with the real bundled Times.
2. **Cut to the real thing (≈4.5s).** The in-situ clip, with a cream-pill
   caption ("Made for them." / "Made for him.").
3. **CTA card (≈1.6s, 0 credits).** `ADD THEIR NAMES →` + `daisymaison.co.uk`.

Total ≈9s. Reads as a proper ad, because the viewer watches the product get
made for someone.

## 3. The build steps

1. **Brief it** — fill `CONTENT_BRIEF_GATE.md`. Caption written before the visual.
2. **Generate the in-situ clip** on a budget model, silent, 9:16, ~5–6s.
   Preflight with `get_cost:true`. Never escalate to seedance_2_0 unless the
   product must stay pixel-locked through a *motion* of the sign itself.
3. **QC as video, not stills.** Sample frames across the whole clip. Reject on
   any sign/lettering warp, vibration on static elements, or deforming hands or
   paws — per the AI-slop checklist in `Personas/VOICE_AND_CAPTION_GUIDE.md`.
4. **Caption in post** — `templates/hook-frames/caption-overlay.py`. Two locked
   treatments; pick by engine:
   - **LAUGH → house native bold white** (looks native, not like an ad)
   - **FEEL / premium → cream pill** (Fraunces brown on `rgba(250,246,238,.94)`)
   - Beat 1 **3–7 words**. Long captions have been rejected repeatedly as
     unreadable at phone speed.
   - Position `top:~300` on product shots, `top:~648` when a person is in frame
     (drops it into the chest space, clear of chin and product).
   - If the clip contains a reveal, the hook **must clear before the payoff is
     legible**, or the loop is spoiled.
5. **Wrap in Format B** if the idea benefits from the made-to-order story.
6. **Deliver the file + the caption in chat.** Max posts manually from his
   phone. Captions pasted into chat, not buried in a file.
7. **Before publishing:** trending audio added in-app (files ship silent), and
   the platform **AI-content label switched on** whenever a synthetic person or
   synthetic product still appears.

## 4. Distribution

One 9:16 silent master serves all of it. Instagram Reels cross-posts to
Facebook automatically — two platforms for one upload. TikTok and YouTube
Shorts to follow once logged in. **Four platforms, one file.**

## 5. Idea bank (Format A unless noted)

Priority order reflects the season read: summer gifting trough, weddings
carrying, Results Day mid-August, Christmas ramp already started at TreatBox.

| # | Engine | Sign wording | Scene + the ambient motion | Hook → payoff |
|---|---|---|---|---|
| 1 | LAUGH | `DAD'S BAR & GRILL` | Garden fence, BBQ smoking beside it — **smoke** is the motion | "He doesn't own a restaurant." → "Try telling him that." |
| 2 | LAUGH | `THE DOG LIVES HERE` *(we just pay the bills)* | Hallway, dog wanders past — **the dog** is the motion | "Whose house is it, really?" → let the sign answer |
| 3 | FEEL | `THE [SURNAME]S · EST. 2026` | New front door, keys still in the lock, **leaves moving** | "First thing they hung up." → "Before the kettle." |
| 4 | SOLVE · Format B | `MR & MRS [NAME]` | Stone pillar with flowers — the Potter setup, proven | "Type the name." → "Made for them." |
| 5 | SOLVE | `[NAME]'S CLASSROOM` | Classroom door, **light shifting** | Hold for **September**, not now — the July teacher window is closed |
| 6 | FEEL · seasonal | `THE [SURNAME]S` | Mantelpiece, stockings, **firelight flicker** | Build in **August** to land the Christmas ramp early |
| 7 | LAUGH | `MUM'S KITCHEN` *(it's this or nothing)* | Kitchen shelf, **steam from a pan** | "You asked what's for dinner." → the sign |

Ideas 1 and 2 are the cheapest reach; 6 is the one with a deadline attached.

## 6. Hard rules

- No filming, no presenter (`CONTENT_BRIEF_GATE.md`).
- No invented customer stories. Real surnames used as product wording are fine
  — a name on a sign *is* the product — but never narrate a specific couple's
  order, and never show invoices, addresses or contact details.
- Preflight every generation; no paid spend without Max's explicit go.
- Propose, never publish.
