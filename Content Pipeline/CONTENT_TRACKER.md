# Content Tracker — what has been posted, what must not repeat

*Added 31 Aug 2026 after Max flagged zero automated tracking of sign names,
concepts, colourways and backgrounds. "Zero excuse for not adding a tracker
that monitors what you're posting on the signs."*

This file is the human-readable companion to `CONTENT_TRACKER.json`.
The JSON is the machine-readable source of truth — every automated slot
reads it before picking a concept, and writes to it the moment a post ships
or is rejected. This markdown is the quick-glance view.

---

## How the tracker works

### Before every slot

1. Load `CONTENT_TRACKER.json`.
2. Check every rotation rule against the candidate trio (line 1, line 2,
   hook, colourway, plate, engine, POV, sign family).
3. If any rule is violated, **pick a different concept** — do not override.
4. After publishing (or rejecting), append the new entry to the JSON
   immediately, before the slot ends. A post not in the tracker does not
   exist for the next slot.

### Rotation rules

| Dimension | Cooldown | Rule |
|---|---|---|
| **line 1** (the name/concept) | 14 days | Same line 1 text cannot reappear within 14 days |
| **Concept** (sign family) | 7 days / 3 posts | Same sign family (wedding, cat, dog, family…) cannot appear within 7 days or 3 posts, whichever is longer |
| **Colourway** | 3 posts | Same colourway cannot be used 3 posts in a row; must rotate through at least 3 different colourways in any window of 5 posts |
| **Plate / background** | 2 posts | Same plate cannot be used on consecutive posts; must use a different plate or generation method next |
| **Engine** | 2 consecutive max | No more than 2 LAUGH, 2 FEEL, or 2 SOLVE posts in a row |
| **POV** | 3 posts | Same POV type cannot be used 3 posts in a row |
| **Hook** | 14 days | Same hook text cannot reappear within 14 days |

### Colourway rotation target

Eight colourways exist. The feed should show the product range, not just
black. Rotation priority (most to least urgent):

1. **Black** — proven hero, use freely but not exclusively
2. **Blue** — validated end-to-end, use confidently
3. **Grass** — official five, untested in content, **test next**
4. **Grey** — official five, untested in content, queue after grass
5. **Sage** — official five but poor contrast; avoid on dark backgrounds
6. **Lightsage / blush / duskypink** — extra range; introduce one per week max

Rule: in any 5-post window, at least 2 different colourways must appear.
In any 10-post window, at least 3 must appear.

### Plate / background variety

Only 4 approved plates exist today (cat, dog, dog_v2, freya_hallway).
Repetition is inevitable, but the tracker enforces:

- Never the same plate twice in a row
- Log which plate was used so Max can see the pattern and expand the library
- When generation is used instead of reprint, log "generated" with the
  background description so repeated scenes are visible

---

## Current post history

| # | Date | Content ID | Line 1 | Line 2 | Colourway | Plate | Hook | Engine | Family | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 25 Jul | DM-C018-BOND | MR & MRS BOND | — | black | generated | (manual post) | FEEL | wedding | published |
| 2 | 26 Jul | DM-CAT-HOUSE | THE CAT'S HOUSE | YOU JUST PAY THE MORTGAGE | black | cat | (manual post) | LAUGH | cat | published |
| 3 | 27 Jul | DM-DIFFUSER-TEASE | (diffuser product) | (diffuser product) | N/A | N/A | live this week | SOLVE | diffuser | published |
| 4 | 27 Jul | DM-HOUSE-QUIZ | (quiz — multiple) | (quiz — multiple) | mixed | freya_hallway | Which house are you? | LAUGH | quiz | published |
| 5 | 28 Jul | DM-C017-JANNAWAY | JANNAWAY | 15 AUG 2026 | black | generated | (pill hook) | FEEL | wedding | published |
| 6 | 28 Jul | DM-C018-BOND-REPOST | MR & MRS BOND | — | black | generated | (manual post) | FEEL | wedding | published |
| 7 | 12 Aug | DM-MOWIT-LAUGH | I'M SEXY & I MOW IT | DAVE'S GARDEN | black | freya_hallway | (none — bare) | LAUGH | garden | **FAILED** |
| 8 | 31 Aug | DM-FAMILY-CARTERS | THE CARTERS | EST. 2019 | black | freya_hallway | Every family deserves their own street | FEEL | family | published |

### What this history shows

- **Colourway problem:** 7 of 8 posts used black. Blue, grass, grey, sage
  have never appeared. The range is invisible to the audience.
- **Plate problem:** freya_hallway used 3 times, cat once, dog never.
  Only 2 of 4 plates used.
- **Name/concept problem:** "BOND" appeared twice (rows 1 + 6). Wedding
  family appeared 3 times in 4 days (rows 1, 5, 6). No home-bar, no
  kitchen, no stadium, no teacher content posted yet.
- **Engine problem:** FEEL appeared 5 times, LAUGH 3, SOLVE 1 (the
  diffuser, which isn't a sign). The 70/20/10 LAUGH-heavy target is
  inverted.

### What the next 5 posts must do

1. Use at least 2 colourways that are NOT black (grass and blue are ready)
2. Use the dog or cat plate (freya_hallway needs a break)
3. Post at least 2 LAUGH-engine concepts (home-bar, kitchen, dog, cat humour)
4. Introduce a new sign family not yet posted (home-bar, stadium, teacher,
   retirement, kitchen, memorial, man-cave)
5. No repeated line 1 text from the history above

---

## Rejected concepts (do not reuse)

| Date | Line 1 | Line 2 | Reason |
|---|---|---|---|
| 12 Aug | I'M SEXY & I MOW IT | DAVE'S GARDEN | Presenter mismatch, no hook, concept repeat |

---

## How to add a new entry

After every post (published or rejected), add to `CONTENT_TRACKER.json`:

```json
{
  "content_id": "DM-EXAMPLE",
  "date": "2026-09-01",
  "platform": "tiktok",
  "line1": "THE DOG'S HOUSE",
  "line2": "WE JUST PAY FOR IT",
  "colourway": "blue",
  "plate": "dog",
  "hook": "Tell me you have a dog without telling me you have a dog",
  "engine": "LAUGH",
  "pov": "pov-relatable",
  "sign_family": "dog",
  "status": "published"
}
```

Then update the table in this file. Both files must stay in sync.
