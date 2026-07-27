# DM-C018-FREYA-CAKE — validated case record

Approved by Max, 24 July 2026, as the saved Freya engineering prompt
("that's definitely more realistic... keep that saved in the engineering
prompt. Again, this is specifically for Freya").

## Job chain

| Stage | Job ID | Model | Refs | Cost |
|---|---|---|---|---|
| A: printing replacement | `c0644e05-c041-45e7-8da3-ceaa743b1fe9` | nano_banana_2 (catalog: nano_banana_pro) | real front crop (media `c97b8302-79b9-4786-aa08-5b9f8622556f`) | 2 cr |
| B: Freya hero, scale-locked | `84696b99-06fc-4d05-9ead-c1b36dbc4b04` | nano_banana_2 | Stage A job + Freya hero `368014cd-bd1a-402f-9d1e-cebbea50c60e` + scale frame (media `9f0cf355-f2e7-4c67-99e3-3bd8309df556`) | 2 cr |

## Reference files (repo paths)

- Real front crop: `Content Pipeline/Creative Studio/active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/product-only-crops/01-front-product-only.jpg`
- Human-scale frame: `.../instagram-DPjdseCDbDR/selected/01-front-frame-240-t08.000.jpg`
- Freya identity: `Content Pipeline/Creative Studio/active/FREYA-character-build/working/stage-0-hero-candidates/candidate-03.png`
- Outputs + measured QC: `Content Pipeline/Creative Studio/active/DM-C018-freya-synthetic-sign-turn/`

## Pass criteria applied

1. Scale first, numerically: sign:shoulder ratio ≥ 1.9 for Freya
   (male benchmark 1.63; take-02 measured 2.32).
2. Lettering exact vs the Stage A source, checked side by side.
3. Identity: warm brown eyes, no hair-highlight drift, freckles, matte
   skin, no editorial gloss.
4. Brand: cream linen, warm neutral/workshop setting (Max likes the
   workshop background — keep it).
