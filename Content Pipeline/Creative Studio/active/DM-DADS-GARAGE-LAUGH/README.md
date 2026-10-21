# DM-DADS-GARAGE-LAUGH — slot 1, 30 Sep 2026 (LAUGH engine)

**Status:** agent-pass, publish session staged; waiting on Max to submit the TikTok widget.

## Slot gate (CONTENT_STRATEGY.md §2b)
1. **Trio:** hook "So what does Dad / *actually do in there?*" → sign line 1 `DAD'S GARAGE`, line 2 `WHERE NOTHING HAPPENS, VERY SLOWLY`. The hook opens the question and line 2 answers it. If you cover the sign, the question hangs.
2. **Presenter:** Alan (a man, standing in a workshop that reads as a garage) holds a sign about Dad's garage. Deadpan, looking at it. He is the dad in the joke, so it makes sense for him to hold it.
3. **Why:** LAUGH engine. Audience: partners and adult kids of garage dads. Mechanic: a relatable callout that gets tagged. Metric: shares, tags, comments.
4. **Record:** the last logged post is 12 Aug. This avoids Mow It (rejected), Freya holding a first-person sign, and Dave's Bar (DM-C020).
5. **Hook burned in:** TikTok Sans 800 at 78px, a white pill plus a burgundy #6E1B2D pill, y=585. It clears his chin and the sign. Checked on the final file.

## Product
Shopify: *Personalised Street Sign Gift — Create Your Own Custom Text* (`kitchen-personalised-street-sign`), Small £18.95 / Medium £24.94 / Large £27.94. Black-on-white colourway. No mounting holes.

## Generation
- `nano_banana_2` at 2k, 9:16. Ref 1 = `ALAN-LOCK-black-tee-workshop-APPROVED.jpg` (object, person, scale). Ref 2 = `build.py` print (`SIGN_HOLES=0 SIGN_HEART=0`). Prompt = DM-C017 validated print edit, adapted.
- take 0 `00c92cac-b6b1-4b28-938e-1f89162c64ef`: spelled correctly, but line 1 reads slightly heavy.
- **take 1 `b65959b8-fa38-44c0-916f-56d6d4b0015a` — selected.** Spelled exactly right, line 2 small and regular weight, holes removed, scale taken from the approved lock.
- Credits: 4 (2 × 2).
- The phone-snapshot pass was skipped deliberately. Ref 1 is already a real photograph and this was a print-only edit.

## Publish
- Higgsfield media `4b7d5593-de75-4e7e-a760-300b9b81ba4e` (JPEG 1080×1920).
- `tiktok_prepare_publish` session `c6ad1a28-70b7-4d6d-b209-7e23f3b792b2`, expires 12:46 UTC. Prefilled: public, comments on, AIGC on, commercial off.
- Suggested sound: *I Don't Wanna Stop*, The Bamboos (GB trending #58, song_clip_id 6739921523634604034). Fallback: *Ok I Like It*, Milky Chance (#36).
- **Blocker:** the Higgsfield flow requires the user to submit the publish-form widget. Agents cannot call `tiktok_publish`, and headless runs cannot finish a post.
