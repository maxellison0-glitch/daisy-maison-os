#!/usr/bin/env python3
"""Read @daisymaison's real Instagram numbers. No login, no Meta app, no Windsor.

    python ig_public.py profile
    python ig_public.py profile --user someoneelse      # any public account
    python ig_public.py profile --json > snapshot.json

Why this exists
---------------
Reading our own engagement was blocked for weeks behind a Meta developer app,
which needs a Facebook login nobody has. Windsor wanted $118 for the same thing.
Max, 28 Jul: "you should be able to just go on Instagram and look autonomously."

He was right, and it turned out to be one unauthenticated request. Instagram's
own web client calls `web_profile_info` to render a public profile page, and it
answers without a session as long as you send the app id the web client sends.
That returns followers, post count, and the last twelve posts with like and
comment counts.

This is READ ONLY and it is not a replacement for the Meta app. It cannot see
impressions, reach, saves, shares, profile visits, follower demographics or
stories - those are owner-only metrics and they still need the token. What it
does give us is the number that actually decides whether a post worked, on our
own account and on any competitor's, today, for free.

Rate limits, honestly
---------------------
Instagram will 429 an IP that asks repeatedly. Instaloader tripped it inside a
minute by making several calls to page through history. This makes exactly ONE
request per run and caches the result, so a normal day's use is a handful of
calls. If you do get a 429 it is a cooldown, not a ban - wait ten minutes.

Twelve posts is the ceiling for a single request. Deeper history needs cursor
pagination, which means more requests, which is what got us limited. Run this
daily and store the snapshots instead: the series is more useful than the depth.
"""
import argparse
import datetime
import json
import os
import sys

import requests

API = "https://www.instagram.com/api/v1/users/web_profile_info/"
# The app id Instagram's own web client sends. Not a secret and not a credential.
WEB_APP_ID = "936619743392459"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_DIR = os.path.join(HERE, "ig-snapshots")


def fetch(username):
    r = requests.get(API, params={"username": username},
                     headers={"User-Agent": UA, "x-ig-app-id": WEB_APP_ID,
                              "Accept": "application/json"},
                     timeout=30)
    if r.status_code == 429:
        sys.exit("Instagram rate-limited us (429). A cooldown, not a ban - but "
                 "MEASURED, NOT GUESSED: on 28 Jul one instaloader burst cost us "
                 "the whole day's competitor reads. Still 429 after three "
                 "attempts across ~50 minutes. Assume HOURS, not minutes, and "
                 "come back tomorrow rather than retrying.")
    if r.status_code != 200:
        sys.exit("Instagram returned HTTP %d. If this is 401 or 403 the "
                 "unauthenticated route may have closed; fall back to the Meta "
                 "app (see SOCIAL_API_SETUP.md)." % r.status_code)
    try:
        return r.json()["data"]["user"]
    except (ValueError, KeyError, TypeError):
        sys.exit("Unexpected reply shape - Instagram changed the endpoint. "
                 "First 300 chars: %s" % r.text[:300])


def posts_of(user):
    out = []
    for edge in user["edge_owner_to_timeline_media"]["edges"]:
        n = edge["node"]
        cap = ""
        ce = n.get("edge_media_to_caption", {}).get("edges", [])
        if ce:
            cap = ce[0]["node"]["text"].replace("\n", " ").strip()
        likes = (n.get("edge_liked_by") or {}).get("count")
        if likes is None:
            likes = (n.get("edge_media_preview_like") or {}).get("count")
        out.append({
            "shortcode": n.get("shortcode"),
            "url": "https://www.instagram.com/p/%s/" % n.get("shortcode"),
            "posted_utc": datetime.datetime.utcfromtimestamp(
                n["taken_at_timestamp"]).isoformat(),
            "type": n.get("__typename", "").replace("XDT", ""),
            "likes": likes,
            "comments": (n.get("edge_media_to_comment") or {}).get("count"),
            # Views only come back on some video posts. Absent is NOT zero -
            # never report a missing view count as a result.
            "views": n.get("video_view_count") or n.get("video_play_count"),
            "caption": cap,
        })
    return out


def cmd_profile(a):
    user = fetch(a.user)
    posts = posts_of(user)
    followers = user["edge_followed_by"]["count"]

    snap = {
        "pulled_utc": datetime.datetime.utcnow().isoformat(),
        "username": a.user,
        "followers": followers,
        "following": user["edge_follow"]["count"],
        "post_count": user["edge_owner_to_timeline_media"]["count"],
        "posts": posts,
    }

    if a.save:
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        p = os.path.join(SNAPSHOT_DIR, "%s-%s.json" % (
            a.user, datetime.date.today().isoformat()))
        json.dump(snap, open(p, "w"), indent=2)
        print("saved %s" % p, file=sys.stderr)

    if a.json:
        print(json.dumps(snap, indent=2))
        return

    print("@%s - %s followers, %s posts" % (
        a.user, f"{followers:,}", f"{snap['post_count']:,}"))

    # Engagement rate against followers. The single most diagnostic number we
    # have: 1-3% is healthy, and anything near zero is a distribution problem,
    # not a creative one. Computed on likes+comments, ignoring pinned posts is
    # not possible here (the API does not flag them) so read the dates - posts
    # out of chronological order at the top of the list ARE the pinned ones.
    scored = [p for p in posts if p["likes"] is not None]
    if scored and followers:
        eng = sum(p["likes"] + (p["comments"] or 0) for p in scored) / len(scored)
        print("mean engagement %.1f per post = %.3f%% of followers"
              % (eng, 100.0 * eng / followers))
    print()
    print("%-11s %-11s %6s %5s %8s  %s"
          % ("posted", "type", "likes", "comm", "views", "caption"))
    for p in posts:
        print("%-11s %-11s %6s %5s %8s  %s" % (
            p["posted_utc"][:10], p["type"],
            "-" if p["likes"] is None else p["likes"],
            "-" if p["comments"] is None else p["comments"],
            p["views"] or "-", p["caption"][:52]))
    print("\nNote: the first few rows may be PINNED posts, which is why their "
          "dates run out of order. Views are absent on most posts - absent is "
          "not zero, so do not log a missing view count as a result.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("profile", help="followers + last 12 posts with engagement")
    p.add_argument("--user", default="daisymaison")
    p.add_argument("--json", action="store_true")
    p.add_argument("--save", action="store_true",
                   help="write a dated snapshot so we build a time series")
    p.set_defaults(fn=cmd_profile)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
