# DM-FAMILY-COLLINS — slot 2 (FEEL), 24 Sep 2026

**Slot gate (CONTENT_STRATEGY §2b)**
1. Trio: line 1 `THE COLLINS FAMILY` / line 2 `PAUL & SUE · EST. 1991` / hook "Mum & Dad's house never had a name" (burgundy on *name*). Cover the sign: the hook makes you need to see what the name is. The sign closes it with the surname and the year.
2. Presenter: a family sign isn't first person, so anyone can hold it. The hook uses the viewer's parents ("Mum & Dad"), not Freya's, so we make no claims about Freya's personal life (VOICE guide).
3. Why: FEEL engine. Audience: adult children buying for parents (anniversary, Christmas lead-in). Scroll-stop: a curiosity gap on a universal feeling. Metric: saves and profile visits.
4. Record: nothing published since 12 Aug. No repeat of Mow It / Dave or any rejected wording. Blue is an approved colourway, not sage.
5. Hook is burnt in: checked by opening the final JPEG.

**Product (Shopify, live 24 Sep):** Personalised Family Street Sign, handle `family-personalised-street-sign`. Small £14.95 / Medium £20.94 / Large £23.94. Up to two lines of personalised text. Colourway: BLUE (muted steel-blue on cream).

**Generation:** `nano_banana_2` at 2k, 3:4, count 2, about 2 credits. Job IDs are `20bf41bd-9ab6-4cbc-8ff6-a4a51643101c` (take 00, **selected**) and `6a810d30-9249-4152-915c-a34fd2d8a2e8` (take 01).
- Ref 1: `reference-masters/street-sign-BLUE-held-SIZE-MASTER.jpg` (the real product: object, typeface, colour).
- Ref 2: `reference-masters/FREYA-holding-sign-BLUE-MASTER.jpg` (identity and scale).
- Both takes spell the wording correctly with no mounting holes. Take 00 was picked because its line 2 is smaller, which is closer to the "line 2 is always small" rule.
- The phone-snapshot block was folded into the generation prompt instead of run as a separate edit pass. The sign did not drift.

**Build:** 3:4 take scaled to 1080 wide and padded to 1080×1920 with a wall-matched band above (the 9:16 rule: pad, never crop). Hook pill is TikTok Sans ExtraBold 78px, white 0.94 pill with a 22px radius, and a burgundy #6E1B2D pill on the keyword. The pill sits at y=190–402. The sign sits at y≈1160–1360, clear of the bottom 450px. The right shaped end may sit under TikTok's action rail, but the wording ends before it. Script: `build.py`.

**Agent verdict:** agent-pass, not max-approved. Known nits: (a) the room reads a little clean and polished even after the snapshot block; (b) there's a faint cornice line at the pad seam that reads as the ceiling; (c) the sign-to-shoulder ratio is roughly 1.7 by eye, under the ≥1.9 Freya target from DM-C018, although the blue master Max passed measures similarly by the same rough method.
