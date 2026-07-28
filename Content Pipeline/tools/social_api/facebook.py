#!/usr/bin/env python3
"""Facebook Page, direct. Same token as Instagram — one login covers both.

    read:
        python facebook.py whoami
        python facebook.py posts --limit 20
        python facebook.py insights --days 28

    publish (asks first unless --yes):
        python facebook.py post-text --message "..."
        python facebook.py post-photo --url https://... --message "..."
        python facebook.py post-reel  --url https://....mp4 --message "..."

Auth. Two env vars, both produced by `instagram.py bootstrap`:
    FB_PAGE_TOKEN     the Page access token
    FB_PAGE_ID        the Page id

The Page token that publishes here is the SAME token that publishes to
Instagram — a Page access token derived from a long-lived user token carries
both. There is no second login and no second app.

Unlike Instagram, a Facebook Page CAN post plain text with no media, and photo
posts accept an uploaded file as well as a URL. Reels still need a public URL,
same as Instagram, because Meta fetches the video itself.
"""
import argparse
import json
import os
import sys
import time

import requests

GRAPH = os.environ.get("FB_GRAPH_BASE", "https://graph.facebook.com/v21.0")

# Meta renames Page metrics regularly; try candidates in order rather than
# hardcoding one set and reporting a confident zero when it moves.
PAGE_METRIC_SETS = [
    ["page_impressions_unique", "page_post_engagements", "page_follows"],
    ["page_impressions", "page_engaged_users", "page_fans"],
]


class ApiError(RuntimeError):
    pass


def need(var):
    v = os.environ.get(var)
    if not v:
        sys.exit("%s is not set. Run `python instagram.py bootstrap` — it prints "
                 "both the Page id and the Page token. See SOCIAL_API_SETUP.md." % var)
    return v


def call(path, params=None, method="GET", files=None):
    params = dict(params or {})
    params["access_token"] = need("FB_PAGE_TOKEN")
    url = path if path.startswith("http") else GRAPH + "/" + path.lstrip("/")
    r = requests.request(method, url,
                         params=params if method == "GET" else None,
                         data=None if method == "GET" else params,
                         files=files, timeout=120)
    try:
        body = r.json()
    except ValueError:
        raise ApiError("non-JSON reply (HTTP %d): %s" % (r.status_code, r.text[:400]))
    if "error" in body:
        e = body["error"]
        raise ApiError("%s: %s" % (e.get("type", "Error"), e.get("message", "?")))
    return body


def _confirm(what, yes):
    if yes:
        return
    print("\nAbout to PUBLISH to the Facebook Page:\n  %s\n" % what)
    if input("Type 'post' to go ahead: ").strip().lower() != "post":
        sys.exit("Cancelled. Nothing was published.")


def cmd_whoami(a):
    print(json.dumps(call(need("FB_PAGE_ID"), {
        "fields": "id,name,username,link,fan_count,followers_count,category"}), indent=2))


def cmd_posts(a):
    res = call(need("FB_PAGE_ID") + "/posts", {
        "fields": "id,message,created_time,permalink_url,"
                  "likes.summary(true),comments.summary(true),shares",
        "limit": a.limit})
    rows = res.get("data", [])
    if a.json:
        print(json.dumps(rows, indent=2)); return
    print("%-19s %6s %6s %6s  %s" % ("posted", "likes", "comm", "share", "message"))
    for p in rows:
        likes = (p.get("likes") or {}).get("summary", {}).get("total_count", "-")
        comms = (p.get("comments") or {}).get("summary", {}).get("total_count", "-")
        shares = (p.get("shares") or {}).get("count", "-")
        msg = (p.get("message") or "").replace("\n", " ")[:48]
        print("%-19s %6s %6s %6s  %s" % (
            p.get("created_time", "")[:19].replace("T", " "), likes, comms, shares, msg))
        print("    %s" % p.get("permalink_url", ""))


def cmd_insights(a):
    now = int(time.time())
    last = None
    for metrics in PAGE_METRIC_SETS:
        try:
            res = call(need("FB_PAGE_ID") + "/insights", {
                "metric": ",".join(metrics), "period": "day",
                "since": now - a.days * 86400, "until": now})
            print("metrics accepted: %s (last %d days)" % (",".join(metrics), a.days))
            for row in res.get("data", []):
                vals = [v.get("value", 0) for v in row.get("values", [])
                        if isinstance(v.get("value"), int)]
                print("  %-28s %s" % (row.get("name"), sum(vals)))
            return
        except ApiError as exc:
            last = exc
    raise ApiError("no known Page metric set accepted. Meta's last word: %s" % last)


def cmd_post_text(a):
    _confirm("text post\n  %s" % a.message[:200], a.yes)
    res = call(need("FB_PAGE_ID") + "/feed", {"message": a.message}, method="POST")
    print("PUBLISHED id=%s" % res.get("id"))


def cmd_post_photo(a):
    _confirm("photo %s\n  %s" % (a.url, a.message[:160]), a.yes)
    res = call(need("FB_PAGE_ID") + "/photos",
               {"url": a.url, "caption": a.message}, method="POST")
    print("PUBLISHED id=%s post_id=%s" % (res.get("id"), res.get("post_id")))


def cmd_post_reel(a):
    """Reels are a three-step upload: start, transfer by URL, finish."""
    _confirm("REEL %s\n  %s" % (a.url, a.message[:160]), a.yes)
    pid = need("FB_PAGE_ID")
    start = call(pid + "/video_reels", {"upload_phase": "start"}, method="POST")
    vid = start["video_id"]
    print("video_id %s — handing Meta the URL..." % vid)
    call(pid + "/video_reels", {"upload_phase": "transfer", "video_id": vid,
                                "file_url": a.url}, method="POST")
    for _ in range(100):
        st = call(vid, {"fields": "status"})
        phase = ((st.get("status") or {}).get("video_status")
                 or (st.get("status") or {}).get("processing_phase", {}).get("status"))
        if phase in ("ready", "complete", "published"):
            break
        if phase == "error":
            raise ApiError("Meta failed the upload: %s" % json.dumps(st)[:300])
        print("  %s" % phase)
        time.sleep(6)
    res = call(pid + "/video_reels", {"upload_phase": "finish", "video_id": vid,
                                      "video_state": "PUBLISHED",
                                      "description": a.message}, method="POST")
    print("PUBLISHED %s" % json.dumps(res))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami", help="Page profile and follower counts"
                   ).set_defaults(fn=cmd_whoami)
    po = sub.add_parser("posts", help="recent posts with likes, comments, shares")
    po.add_argument("--limit", type=int, default=12)
    po.add_argument("--json", action="store_true")
    po.set_defaults(fn=cmd_posts)
    i = sub.add_parser("insights", help="Page metrics over a window")
    i.add_argument("--days", type=int, default=28)
    i.set_defaults(fn=cmd_insights)

    t = sub.add_parser("post-text", help="publish a text-only post")
    t.add_argument("--message", required=True)
    t.add_argument("--yes", action="store_true")
    t.set_defaults(fn=cmd_post_text)
    for name, fn, helptext in (("post-photo", cmd_post_photo, "publish a photo"),
                               ("post-reel", cmd_post_reel, "publish a Reel")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--url", required=True, help="publicly reachable URL")
        s.add_argument("--message", default="")
        s.add_argument("--yes", action="store_true")
        s.set_defaults(fn=fn)

    a = p.parse_args()
    try:
        a.fn(a)
    except ApiError as exc:
        sys.exit("Facebook API said: %s" % exc)


if __name__ == "__main__":
    main()
