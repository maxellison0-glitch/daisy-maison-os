# sign-reprint

Put any wording onto an approved photographic plate, for free.

    # one design
    python3 reprint.py --plate cat \
        --line1 "THE LITTLE MADAM" --line2 "SHE RUNS THIS HOUSE" --out out.png

    # a whole carousel, 4:5 slides + wordmark end-slide + contact sheet
    python3 carousel.py cat designs-cat.txt ../../../projects/sign-carousels/cat-house

    # the lockup on its own, transparent PNG
    python3 wordmark.py wordmark.png

Plates and their measured sign boxes live in `plates.json`.
Method, gates and the five silent bugs this cost: `../../SIGN_CAROUSEL_ENGINE.md`.

Runtime: ~1.5s per slide. 22 slides across two plates cost 0 credits.
