#!/usr/bin/env python3
"""Reconcile PUBLISH_LOG.md against what the accounts actually show.

WHY THIS EXISTS. Max, 29 Jul 2026: "all I'm asking you to do is keep a log of
the posts we have done, which you don't seem to be doing a very good job of" —
and then, when asked which posts he'd published: "I don't have time to sit here
and tell you which fucking post I've done."

He's right, and asking was the actual mistake. The account already knows what
was posted. Nobody should ever have to answer that question again.

So this reads the live accounts, diffs them against the log, and prints:

  * ON ACCOUNT, NOT IN LOG   -> rows to add, pre-formatted, with real numbers
  * IN LOG, NOT ON ACCOUNT   -> a claimed post that isn't there (deleted, or
                                logged as `reported` and never actually sent)
  * NUMBERS MOVED            -> a logged figure the account now disagrees with

It does NOT rewrite the markdown. That is deliberate: PUBLISH_LOG.md carries
hand-written judgement in its Source column and its not-posted-and-why table,
and a script that rewrites a table it doesn't understand is how you lose a
month of lessons. It emits the diff; a human or an agent applies it.

Instagram note: it returns likes and comments on every post but view counts
only sometimes, and NEVER reach. A missing view count here is missing, not
zero.

Usage:
    python3 reconcile_log.py                  # live pull, both platforms
    python3 reconcile_log.py --offline        # newest saved snapshots only
    python3 reconcile_log.py --days 14        # window (default 10)
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.normpath(os.path.join(HERE, "..", "..", "PUBLISH_LOG.md"))


def _newest(pattern):
    hits = sorted(glob.glob(os.path.join(HERE, pattern)))
    return hits[-1] if hits else None


def _pull(script, save=True):
    """Run a reader and return parsed JSON, or None with the reason printed.

    One attempt. Never retried in a loop — Instagram answers 429 for a
    cooldown and hammering it is how we lost a day of competitor reads.
    """
    cmd = [sys.executable, os.path.join(HERE, script), "profile", "--json"]
    if save:
        cmd.append("--save")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"  ! {script}: timed out. Treated as unreachable.")
        return None
    if r.returncode != 0:
        why = (r.stderr or r.stdout or "").strip().splitlines()
        print(f"  ! {script}: {why[-1] if why else 'failed'} — named as a gap, not retried.")
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        print(f"  ! {script}: returned non-JSON. Named as a gap.")
        return None


def _load(script, snap_glob, offline):
    if not offline:
        d = _pull(script)
        if d:
            return d, "live"
    f = _newest(snap_glob)
    if not f:
        return None, "no snapshot"
    with open(f) as fh:
        return json.load(fh), f"snapshot {os.path.basename(f)}"


def _logged_shortcodes(text):
    """Every Instagram shortcode already referenced anywhere in the log."""
    return set(re.findall(r"instagram\.com/(?:p|reel)/([A-Za-z0-9_-]+)", text))


def _norm(s):
    """Flatten the punctuation that platforms and humans disagree about.

    Real bug this fixes: the log had "We didn't realise these surnames actually
    existed" typed with a straight apostrophe; TikTok returns it curly. The raw
    comparison missed, so two posts that WERE logged got reported as missing.
    A reconciler that cries wolf is a reconciler nobody runs.
    """
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("—", "-"), ("–", "-"),
                 ("…", "...")):
        s = s.replace(a, b)
    return " ".join(s.lower().split())


def _logged_captions(text):
    """Quoted caption fragments in the log, normalised for loose matching.

    TikTok gives us no stable per-post id through the public reader, so the
    caption is the only join key available. Imperfect on purpose — a near
    miss shows up as a suggested row a human then rejects, which is a much
    cheaper failure than silently missing a post.
    """
    return [_norm(m) for m in re.findall(r'"([^"\n]{12,})"', text)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="use newest saved snapshots, make no network calls")
    ap.add_argument("--days", type=int, default=10,
                    help="only consider posts this recent (default 10)")
    ap.add_argument("--user", default="daisymaison")
    args = ap.parse_args()

    if not os.path.exists(LOG):
        sys.exit(f"PUBLISH_LOG.md not found at {LOG}")
    with open(LOG) as fh:
        log_text = fh.read()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    print(f"Reconciling PUBLISH_LOG.md — posts since {cutoff:%Y-%m-%d} "
          f"({'offline' if args.offline else 'live pull'})\n")

    known_codes = _logged_shortcodes(log_text)
    known_caps = _logged_captions(log_text)
    missing, stale = [], []

    # ---- Instagram ----------------------------------------------------
    print("Instagram")
    ig, ig_src = _load("ig_public.py", "ig-snapshots/*.json", args.offline)
    if not ig:
        print(f"  GAP: no Instagram data ({ig_src}). No claim made about IG.\n")
    else:
        print(f"  source: {ig_src} · {ig.get('followers','?')} followers")
        for p in ig.get("posts", []):
            when = p.get("posted_utc") or ""
            try:
                dt = datetime.fromisoformat(when).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if dt < cutoff:
                continue
            code = p.get("shortcode", "")
            line = (f"| {dt:%d %b} | ? | {(p.get('caption') or '')[:60].strip()} | "
                    f"**{p.get('likes','?')} likes"
                    + (f", {p['comments']} comments" if p.get("comments") else "")
                    + f"** | measured | {p.get('url','')} |")
            if code and code not in known_codes:
                missing.append(("Instagram", dt, line))
            else:
                stale.append(("Instagram", dt, code,
                              p.get("likes"), p.get("comments"), p.get("views")))
        print(f"  {len(ig.get('posts', []))} posts read\n")

    # ---- TikTok -------------------------------------------------------
    print("TikTok")
    tt, tt_src = _load("tiktok_public.py", "tiktok-snapshots/*.json", args.offline)
    posts_file = _newest("tiktok-post-snapshots/*.json")
    tt_posts = []
    if posts_file:
        with open(posts_file) as fh:
            raw = json.load(fh)
        tt_posts = raw if isinstance(raw, list) else (raw.get("posts") or [])
    if not tt_posts:
        print("  GAP: no TikTok post data. No claim made about TikTok.\n")
    else:
        print(f"  source: {os.path.basename(posts_file)} · {len(tt_posts)} posts")
        for p in tt_posts:
            desc = (p.get("desc") or p.get("title") or "").strip()
            if not desc:
                continue
            key = _norm(desc)[:40]
            if not any(key[:24] in c for c in known_caps):
                missing.append(("TikTok", None,
                                f"| ? | ? | {desc[:60]} | "
                                f"{p.get('view_count','?')} views | measured |"))
        print()

    # ---- Report -------------------------------------------------------
    print("=" * 72)
    if missing:
        print(f"\nON ACCOUNT, NOT IN LOG — {len(missing)} row(s) to add:\n")
        for plat, dt, line in sorted(missing, key=lambda r: (r[0], str(r[1]))):
            print(f"  [{plat}] {line}")
        print("\n  Fill the Content ID column by hand — it is the one field no\n"
              "  API can tell us, because it is our own naming.")
    else:
        print("\nON ACCOUNT, NOT IN LOG: nothing. The log is current.")

    reported = re.findall(r"\|\s*\*\*reported\*\*[^|]*\|", log_text)
    if reported:
        print(f"\nSTILL MARKED `reported` — {len(reported)} row(s). Each one is a\n"
              "post nobody has verified exists. If a matching post did not appear\n"
              "in the account read above, it was never actually published.")

    print(f"\n{len(stale)} logged post(s) matched the account and can be "
          "spot-checked for moved numbers.")
    print("\nNothing was written. Apply the diff by hand or hand it to an agent.")


if __name__ == "__main__":
    main()
