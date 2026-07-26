#!/usr/bin/env python3
"""Instagram, direct. No Windsor, no monthly fee.

Windsor.ai wanted $118 for the fourth data source, and its only Instagram write
action was `create_image_post` — a single feed photo, with carousels, Reels and
stories explicitly unsupported. Meta's own API does all of those and the insights
too, for nothing, so this is an upgrade rather than a workaround.

    read:
        python instagram.py whoami
        python instagram.py media --limit 20
        python instagram.py insights --media-id 179...
        python instagram.py account-insights --days 28
        python instagram.py limit

    publish (always asks first unless --yes):
        python instagram.py post-image --url https://... --caption "..."
        python instagram.py post-reel  --url https://....mp4 --caption "..."
        python instagram.py post-carousel --url https://a.jpg --url https://b.jpg

Auth. Two env vars:
    IG_ACCESS_TOKEN   a long-lived Page access token
    IG_USER_ID        the Instagram Business account id

Run `python instagram.py bootstrap` with a short-lived user token in
IG_ACCESS_TOKEN and it will find both for you and print what to export.
See SOCIAL_API_SETUP.md for the click path.

Metric names: Meta renames and deprecates Instagram metrics regularly (the
`impressions` family gave way to `views` during 2024-25). Nothing here hardcodes
a metric list as if it were permanent — `--metrics` is a flag, the defaults are
tried in order, and a rejected metric is reported with Meta's own error text
rather than being silently swallowed. If a metric name has moved again, the tool
tells you what Meta said instead of returning a confident zero.
"""
import argparse
import json
import os
import sys
import time

import requests

GRAPH = os.environ.get("IG_GRAPH_BASE", "https://graph.facebook.com/v21.0")

# Tried in order; the first set the API accepts wins. Meta moves these.
MEDIA_METRIC_SETS = [
    ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions"],
    ["plays", "reach", "likes", "comments", "shares", "saved"],
    ["impressions", "reach", "engagement", "saved"],
]
ACCOUNT_METRIC_SETS = [
    ["reach", "profile_views", "website_clicks", "accounts_engaged"],
    ["reach", "profile_views", "website_clicks"],
    ["impressions", "reach", "profile_views"],
]


class ApiError(RuntimeError):
    pass


def call(path, params=None, method="GET", token=None):
    params = dict(params or {})
    params["access_token"] = token or need("IG_ACCESS_TOKEN")
    url = path if path.startswith("http") else GRAPH + "/" + path.lstrip("/")
    r = requests.request(method, url, params=params if method == "GET" else None,
                         data=None if method == "GET" else params, timeout=60)
    try:
        body = r.json()
    except ValueError:
        raise ApiError("non-JSON reply (HTTP %d): %s" % (r.status_code, r.text[:400]))
    if "error" in body:
        e = body["error"]
        raise ApiError("%s: %s%s" % (e.get("type", "Error"), e.get("message", "?"),
                                     "" if not e.get("error_user_msg")
                                     else " — " + e["error_user_msg"]))
    return body


def need(var):
    v = os.environ.get(var)
    if not v:
        sys.exit("%s is not set. Run `python instagram.py bootstrap` or see "
                 "SOCIAL_API_SETUP.md." % var)
    return v


def try_metric_sets(path, sets, extra, label):
    """Ask for each candidate metric set until one is accepted."""
    last = None
    for metrics in sets:
        try:
            p = dict(extra); p["metric"] = ",".join(metrics)
            return call(path, p), metrics
        except ApiError as exc:
            last = exc
            if "metric" not in str(exc).lower():
                raise
    raise ApiError("no known metric set accepted for %s. Meta's last word: %s\n"
                   "Pass --metrics with current names from Meta's changelog."
                   % (label, last))


# --------------------------------------------------------------------- commands
def cmd_bootstrap(a):
    """Turn a short-lived user token into the two values this tool needs."""
    tok = need("IG_ACCESS_TOKEN")
    if a.app_id and a.app_secret:
        print("Exchanging for a long-lived (60-day) user token...")
        tok = call("oauth/access_token", {
            "grant_type": "fb_exchange_token", "client_id": a.app_id,
            "client_secret": a.app_secret, "fb_exchange_token": tok,
        }, token=tok)["access_token"]
        print("  done.")
    else:
        print("No --app-id/--app-secret given, so using the token as supplied.")
        print("  A short-lived token dies in about an hour. Pass both to get 60 days.")

    pages = call("me/accounts", {"fields": "id,name,access_token"}, token=tok)
    found = []
    for pg in pages.get("data", []):
        try:
            info = call(pg["id"], {"fields": "instagram_business_account{id,username}"},
                        token=tok)
        except ApiError:
            continue
        iba = info.get("instagram_business_account")
        if iba:
            found.append((pg["name"], iba["username"], iba["id"], pg["access_token"]))

    if not found:
        sys.exit("No Instagram Business account found on any Page this token can see.\n"
                 "Check: the IG account is Business or Creator (not personal), and it is\n"
                 "linked to a Facebook Page you administer. See SOCIAL_API_SETUP.md.")
    print()
    for name, user, uid, ptok in found:
        print("Page %r -> @%s (id %s)" % (name, user, uid))
        print()
        print("  export IG_USER_ID=%s" % uid)
        print("  export IG_ACCESS_TOKEN=%s" % ptok)
        print()
    print("A Page token derived from a long-lived user token does not expire on a")
    print("timer, but it dies if the password changes or permissions are revoked.")


def cmd_whoami(a):
    uid = need("IG_USER_ID")
    print(json.dumps(call(uid, {
        "fields": "id,username,name,followers_count,follows_count,media_count,"
                  "profile_picture_url,biography"}), indent=2))


def cmd_media(a):
    uid = need("IG_USER_ID")
    res = call(uid + "/media", {
        "fields": "id,caption,media_type,media_product_type,permalink,timestamp,"
                  "like_count,comments_count,thumbnail_url",
        "limit": a.limit})
    rows = res.get("data", [])
    if a.json:
        print(json.dumps(rows, indent=2)); return
    print("%-19s %-11s %6s %6s  %s" % ("posted", "type", "likes", "comm", "caption"))
    for m in rows:
        cap = (m.get("caption") or "").replace("\n", " ")[:52]
        print("%-19s %-11s %6s %6s  %s" % (
            m.get("timestamp", "")[:19].replace("T", " "),
            m.get("media_product_type") or m.get("media_type", ""),
            m.get("like_count", "-"), m.get("comments_count", "-"), cap))
        print("    %s  id=%s" % (m.get("permalink", ""), m["id"]))


def cmd_insights(a):
    sets = [a.metrics.split(",")] if a.metrics else MEDIA_METRIC_SETS
    res, used = try_metric_sets(a.media_id + "/insights", sets, {}, "media " + a.media_id)
    print("metrics accepted: %s" % ",".join(used))
    for row in res.get("data", []):
        vals = row.get("values") or [{}]
        print("  %-20s %s" % (row.get("name"), vals[0].get("value")))


def cmd_account_insights(a):
    uid = need("IG_USER_ID")
    sets = [a.metrics.split(",")] if a.metrics else ACCOUNT_METRIC_SETS
    now = int(time.time())
    extra = {"period": "day", "metric_type": "total",
             "since": now - a.days * 86400, "until": now}
    try:
        res, used = try_metric_sets(uid + "/insights", sets, extra, "account")
    except ApiError:
        extra.pop("metric_type")
        res, used = try_metric_sets(uid + "/insights", sets, extra, "account")
    print("metrics accepted: %s (last %d days)" % (",".join(used), a.days))
    for row in res.get("data", []):
        vals = row.get("values") or []
        total = sum(v.get("value", 0) for v in vals if isinstance(v.get("value"), int))
        print("  %-20s %s" % (row.get("name"), total if vals else row.get("total_value")))


def cmd_limit(a):
    uid = need("IG_USER_ID")
    res = call(uid + "/content_publishing_limit",
               {"fields": "config,quota_usage"})
    for row in res.get("data", []):
        print("published in the last 24h: %s of %s" % (
            row.get("quota_usage"), (row.get("config") or {}).get("quota_total", 50)))


def _wait_for_container(cid, timeout=600):
    """Video containers are processed asynchronously. Poll until FINISHED."""
    start = time.time()
    while time.time() - start < timeout:
        st = call(cid, {"fields": "status_code,status"})
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise ApiError("container %s came back %s: %s"
                           % (cid, code, st.get("status")))
        print("  %s... (%ds)" % (code, int(time.time() - start)))
        time.sleep(6)
    raise ApiError("container %s still not FINISHED after %ds" % (cid, timeout))


def _confirm(what, yes):
    if yes:
        return
    print("\nAbout to PUBLISH to Instagram:\n  %s\n" % what)
    if input("Type 'post' to go ahead: ").strip().lower() != "post":
        sys.exit("Cancelled. Nothing was published.")


def _publish(uid, container_id):
    res = call(uid + "/media_publish", {"creation_id": container_id}, method="POST")
    mid = res["id"]
    perma = call(mid, {"fields": "permalink"}).get("permalink", "(no permalink)")
    print("PUBLISHED  id=%s\n  %s" % (mid, perma))
    return mid


def cmd_post_image(a):
    uid = need("IG_USER_ID")
    _confirm("image %s\n  caption: %s" % (a.url[0], (a.caption or "")[:160]), a.yes)
    c = call(uid + "/media", {"image_url": a.url[0], "caption": a.caption or ""},
             method="POST")
    _publish(uid, c["id"])


def cmd_post_reel(a):
    uid = need("IG_USER_ID")
    _confirm("REEL %s\n  caption: %s" % (a.url[0], (a.caption or "")[:160]), a.yes)
    c = call(uid + "/media", {"media_type": "REELS", "video_url": a.url[0],
                              "caption": a.caption or "",
                              "share_to_feed": "true" if a.share_to_feed else "false"},
             method="POST")
    print("container %s created; waiting for Meta to process the video..." % c["id"])
    _wait_for_container(c["id"])
    _publish(uid, c["id"])


def cmd_post_carousel(a):
    uid = need("IG_USER_ID")
    if not 2 <= len(a.url) <= 10:
        sys.exit("A carousel needs between 2 and 10 items; got %d." % len(a.url))
    _confirm("CAROUSEL of %d\n  %s\n  caption: %s"
             % (len(a.url), "\n  ".join(a.url), (a.caption or "")[:160]), a.yes)
    kids = []
    for u in a.url:
        is_video = u.lower().split("?")[0].endswith((".mp4", ".mov"))
        p = {"is_carousel_item": "true"}
        p["video_url" if is_video else "image_url"] = u
        if is_video:
            p["media_type"] = "VIDEO"
        cid = call(uid + "/media", p, method="POST")["id"]
        if is_video:
            _wait_for_container(cid)
        kids.append(cid)
        print("  child %s ready" % cid)
    c = call(uid + "/media", {"media_type": "CAROUSEL", "children": ",".join(kids),
                              "caption": a.caption or ""}, method="POST")
    _wait_for_container(c["id"])
    _publish(uid, c["id"])


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bootstrap", help="find IG_USER_ID and a long-lived token")
    b.add_argument("--app-id"); b.add_argument("--app-secret")
    b.set_defaults(fn=cmd_bootstrap)

    sub.add_parser("whoami", help="account profile").set_defaults(fn=cmd_whoami)

    m = sub.add_parser("media", help="recent posts with likes and comments")
    m.add_argument("--limit", type=int, default=12)
    m.add_argument("--json", action="store_true")
    m.set_defaults(fn=cmd_media)

    i = sub.add_parser("insights", help="per-post metrics")
    i.add_argument("--media-id", required=True)
    i.add_argument("--metrics", help="comma-separated, overrides the defaults")
    i.set_defaults(fn=cmd_insights)

    ai = sub.add_parser("account-insights", help="account metrics over a window")
    ai.add_argument("--days", type=int, default=28)
    ai.add_argument("--metrics")
    ai.set_defaults(fn=cmd_account_insights)

    sub.add_parser("limit", help="posts left in the 24h publishing quota"
                   ).set_defaults(fn=cmd_limit)

    for name, fn, helptext in (
            ("post-image", cmd_post_image, "publish one feed photo"),
            ("post-reel", cmd_post_reel, "publish a Reel"),
            ("post-carousel", cmd_post_carousel, "publish a 2-10 item carousel")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--url", action="append", required=True,
                       help="publicly reachable URL; repeat for carousels")
        s.add_argument("--caption", default="")
        s.add_argument("--yes", action="store_true", help="skip the confirmation")
        if name == "post-reel":
            s.add_argument("--share-to-feed", action="store_true", default=True)
        s.set_defaults(fn=fn)

    a = p.parse_args()
    try:
        a.fn(a)
    except ApiError as exc:
        sys.exit("Instagram API said: %s" % exc)


if __name__ == "__main__":
    main()
