# DM-C020 — putting Alan and Freya in the office

Four batches, sixteen takes, 32 credits. Max, 28 Jul: *"You're using two
references already, and then you've got Alan and Freya also being referenced, so
it's a multi-image reference. Trying to create Alan and Freya inside the office
perfectly."*

| Batch | Room plate | People | Agent pick | **Max approved** |
|---|---|---|---|---|
| **cast-A** | F — shutter bay | Alan | none | **02, 04** |
| **cast-B** | H — packing bay | Alan | take-02 | **02** |
| **cast-C** | H — packing bay | Freya | take-02 | **02, 03** |
| **cast-D** | H — packing bay | Alan + Freya | take-02 | **03, 04** |

Seven of sixteen approved, reviewed by Max 28 Jul 2026. Note that the agent pick
and the human pick disagree in three of the four batches — on cast-A the agent
would have binned everything, and on cast-D the agent picked 02 where Max picked
04. The gate is Max's, and this is the evidence for why.

---

## What each approved image is actually FOR

Max, 28 Jul: *"You should all note as well what references we can actually use
these for."* An approved image is not just "good" — it has a job.

| Image | Job |
|---|---|
| **cast-A / take-04** | **Lead shutter-bay frame.** *"A weird angle, but it actually looks more realistic than the other ones."* The odd viewpoint is the reason it works. |
| **cast-A / take-02** | **Second angle on the same setup.** *"Do take two to take four… really help with angles. Probably use both those in one reference video."* Use the pair together, not separately. |
| **cast-B / take-02** | **Alan hero, packing bay.** Clean, straight to camera. The base plate for wording swaps, and the matched partner to Freya below — same room, same camera, so they read as colleagues. |
| **cast-C / take-02** | **Freya hero, packing bay.** Matches cast-B/02. Also the only clean-panel output in the run — no mounting holes. |
| **cast-C / take-03** | **Scale and composition reference — not a publishable image.** The body is broken (the sign floats between two hands) but the *sign* is the right size in the frame, which is the hard part. Max: *"the size is a really good size… Take three can be used for anyone. We could implement me in there."* Use it as the composition target when dropping any character into this room, including an eventual synthetic Max. |
| **cast-D / take-04** | **Lead two-hander.** *"Perfect size and engaging."* Best sign scale in the entire run. This is the frame to build the turnaround video on. |
| **cast-D / take-03** | **Second two-hander angle, with a fix outstanding.** *"Nearly"* — Alan wants to be slightly taller in frame. Keep, correct before it leads anything. |

---

## 1. The footage was already here

Max asked me to dig through Instagram for the clips of him turning signs in the
office. Instagram was rate-limited (429, hours not minutes) — but the reel is
already in this repo, pulled during DM-C017:

`active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/`

It is the *"Customer of the year, probably"* post — 11,889 views, 101 likes,
filmed in the open shutter bay, which is **plate F**: the plate Max independently
picked as *"a really good one for a street [sign] video"*. Same room, same
camera height, same daylight.

The head is cropped off the frame used as reference
(`source/pose-scale-reference/POSE-SCALE-real-sign-hold-HEADLESS.jpg`) so it
answers pose and scale only and cannot leak a face into a synthetic character.

## 2. The scale gate needs rebuilding before it means anything

The gate in `VERDICTS.md` says sign width ÷ shoulder width should land
**1.20–1.45**. Measuring it automatically off these frames does **not** work, and
this file records that rather than pretending otherwise.

Four different detectors were written against the same sixteen images. They
returned four different sets of numbers, because "shoulder width" is not one
measurement: at the sleeve seam it is one number, at the upper arm another, at
the elbow — where the arms are out holding the sign — another again, and each
detector latched onto a different one. Run against the real ground-truth frame,
the same code returned 0.73, 1.49 and 1.30 depending on which row it chose.

**Ground truth, read off the real footage by hand:** sign ≈ 975px, shoulders at
the sleeve line ≈ 720px → **≈ 1.35**. That is the number to calibrate against,
and 1.20–1.45 is the right window.

**What is needed:** a measurement anchored to a named anatomical row — the sleeve
seam — not "the widest run above the sign". Until that exists, this gate is a
by-eye judgement and should be described as one.

By eye: cast-B take-02 and cast-D take-02 are close to the real footage.
Every cast-A take renders the sign too wide.

## 3. Mounting holes: the lock outranks the prompt

Every prompt in this run carried **NO MOUNTING HOLES ANYWHERE - the panel is
unbroken**. The result:

| Batch | Character lock used | Holes in output |
|---|---|---|
| cast-A | Alan (lock **has** holes) | **yes** |
| cast-B | Alan (lock **has** holes) | **yes** |
| cast-C | Freya (lock has **none**) | **no** |
| cast-D | Alan + Freya | **yes**, on Alan's sign |

That is a clean natural experiment, and it settles the question the character-lock
system could only warn about. **A negative instruction does not beat a reference
image.** The holes are not coming from the prompt failing to say "no holes"; they
are being copied from the photograph.

So there are only two real fixes:

1. **Produce a hole-free Alan lock** — take the approved black-tee lock, remove
   the two holes once, approve that as the lock, and every future generation
   inherits a clean panel. One edit, permanent.
2. **Remove them in post** on each output — two small dark dots on a flat cream
   panel, trivial to patch, but it is per-image work forever.

Option 1 is the one worth doing. It needs Max's approval because it changes the
lock, and changing a lock is the one move this system treats as expensive.

## 4. What actually worked

**In-prompt role labelling.** Four references, each explicitly assigned:
*"IMAGE 1 is the ROOM… IMAGE 2 is THE MAN… IMAGE 4 is THE POSE AND THE SCALE"*,
each with a matching *"DO NOT take X from this image"*. Every reference landed in
its intended role on the first attempt — including the hardest one, the headless
pose frame, which could easily have contributed a body or a face and did not.

**The two-hander worked first time.** Alan straight to camera, Freya crossing
behind mid-stride with a stack of blank panels, clear floor between them, and the
depth relationship correct — she is smaller because she is further away.

**Freya's anatomy is the weak point.** Two of her four takes broke: one rendered
the sign floating between disembodied hands, one lost the connection between
forearm and shoulder. Her lock is a chest-height hold; the prompt asked for a
waist-height hold. Match the hold to the lock and this should stop.

---

## Status

| | |
|---|---|
| Sixteen takes | generated, **reviewed and picked by Max 28 Jul 2026** |
| Approved | cast-A 02 + 04, cast-B 02, cast-C 02 + 03, cast-D 03 + 04 |
| Blocking the next step | the hole-free Alan lock decision |
| Next | the turnaround video, built on cast-D take-04 |
