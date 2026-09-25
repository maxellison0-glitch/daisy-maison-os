# DM-HARRISON-FEEL — slot 2 (FEEL), 25 Sep 2026

State: **agent-pass**, staged for TikTok. Not max-approved.

## Slot gate
1. Trio: line 1 `THE HARRISON FAMILY` / line 2 `MUM, DAD, ELLIE, JOSH & BISCUIT` / hook "Mum said she didn't want anything…"
   The hook opens the loop (what do you give her?); the sign closes it (all of us, dog included).
2. Presenter: hands only (man, black tee, from the approved held-in-room master). He's the gift-giver, so it isn't a first-person sign held by the wrong person.
3. Engine FEEL. Audience: adult children buying for Mum's birthday. Mechanic: the universal "I don't want anything" line, then the dog in line 2 is the smile, and the caption asks "Who's the Biscuit in your house?" to get comments.
4. Record: the last logged post is 12 Aug (LAUGH / Mow It). No family-sign or mum concept has been rejected in VERDICTS.md.
5. Hook burnt in (checked by opening the final file).

## Product (Shopify, live)
Personalised Family Street Sign Gift — Custom Family Name Sign (gid 9436228845907). Small £14.95 / Medium £20.94 / Large £23.94. Two lines. Black on cream. Layout matches the live listing: THE [NAME] FAMILY + names.

## Generation
- Ref 1: `reference-masters/street-sign-BLACK-held-in-room-MASTER.jpg` (media 6ca14675-6f19-4b17-a83d-a00a871a223d)
- nano_banana_2, 2k, 3:4, count 2. Jobs 36a4c850-3cb3-45ae-adb9-80a244c87d5e (A) and **36e2b487-c0a9-4e9f-bafd-f49cde96d4d4 (B, picked)**
  - A: the dog stares at camera, an odd open-box table, and faint mounting-hole dots.
  - B: exact spelling, line 2 small and regular weight, no holes, the dog looks up at the sign.
- Outpaint to 9:16: job d95c4e6c-e433-4720-a562-469ee3ec08f5 (2 credits). It zoomed out and added ceiling, which leaves clean space for the pill. Sign text checked at full resolution.
- A flat wall-colour pad was tried first and **rejected**: hard seam through the black tee at the pad line. Outpaint beats pad for a scene with a person cut by the top edge.
- Pill: TikTok Sans 800, 78px, white pill, "anything" in #8A2338. Local Chromium render, 0 credits.
  Gotcha: the Google Fonts woff2 URL ending `...FoFDpITI` is NOT the latin subset. It silently fell back to a system sans. Use the one ending `...Fo1Dp.woff2`.
- Credits: ~4 total (2 image + 2 outpaint).

## Publish
Higgsfield upload media 6d4e64b3-dfde-4b29-8ba0-b50f6a9798fe → tiktok_prepare_publish session 46ec791e-54c3-4780-a117-9b84b1f07c5a (expires 16:45 UTC).
Music: Little Things, Adrián Berenguer (UK CML #12, song_clip_id 6981828404915996674). It's picked in the form, because prepare_publish takes no music param.
**Blocked:** the MCP now requires the user to submit the publish-form widget, and `tiktok_publish` is no longer callable by the agent.
