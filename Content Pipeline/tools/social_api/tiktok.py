#!/usr/bin/env python3
"""TikTok, direct. Metrics for free; publishing has a real catch.

    read:
        python tiktok.py whoami
        python tiktok.py videos --limit 20
        python tiktok.py refresh          # roll the access token

    publish:
        python tiktok.py post --url https://....mp4 --caption "..." --draft
        python tiktok.py post --url https://....mp4 --caption "..."   # direct

THE CATCH, up front, because it decides how we work:

TikTok's Content Posting API only allows **direct public posting** from an app
that has passed TikTok's audit. Until then an unaudited app can push a video to
the account's **inbox as a draft** — it lands in TikTok, you open the app, and
you tap post. Every unaudited app is also forced into `SELF_ONLY` privacy for
direct posts, which is not a public post at all.

So the honest split:
  - **metrics**: this script, free, no audit needed for our own account.
  - **publishing today**: either `--draft` here (one tap on your phone to
    finish), or Higgsfield's `tiktok_connect` / `tiktok_publish`, which already
    holds an audited app so it can post publicly with no dev work at all.
  - **direct public posting from this script**: only worth applying for the
    audit if the draft tap becomes annoying.

Auth. Env vars:
    TIKTOK_CLIENT_KEY
    TIKTOK_CLIENT_SECRET
    TIKTOK_ACCESS_TOKEN     expires in 24h
    TIKTOK_REFRESH_TOKEN    lasts a year; `refresh` uses it to mint a new access token

Scopes needed: user.info.basic, user.info.stats, video.list (metrics), plus
video.upload (draft) or video.publish (direct). See SOCIAL_API_SETUP.md.
"""
import argparse
import json
import os
import sys
import time

import requests

API = "https://open.tiktokapis.com/v2"

VIDEO_FIELDS = ("id,title,video_description,create_time,duration,cover_image_url,"
                "share_url,view_count,like_count,comment_count,share_count")


class ApiError(RuntimeError):
    pass


def need(var):
    v = os.environ.get(var)
    if not v:
        sys.exit("%s is not set. See SOCIAL_API_SETUP.md." % var)
    return v


def call(path, params=None, body=None, method="GET"):
    url = API + path
    headers = {"Authorization": "Bearer " + need("TIKTOK_ACCESS_TOKEN")}
    if body is not None:
        headers["Content-Type"] = "application/json; charset=UTF-8"
    r = requests.request(method, url, params=params, json=body,
                         headers=headers, timeout=60)
    try:
        out = r.json()
    except ValueError:
        raise ApiError("non-JSON reply (HTTP %d): %s" % (r.status_code, r.text[:400]))
    err = out.get("error") or {}
    if err.get("code") not in (None, "ok"):
        raise ApiError("%s: %s" % (err.get("code"), err.get("message")))
    return out.get("data", out)


def cmd_refresh(a):
    r = requests.post("https://open.tiktokapis.com/v2/oauth/token/", timeout=60,
                      headers={"Content-Type": "application/x-www-form-urlencoded"},
                      data={"client_key": need("TIKTOK_CLIENT_KEY"),
                            "client_secret": need("TIKTOK_CLIENT_SECRET"),
                            "grant_type": "refresh_token",
                            "refresh_token": need("TIKTOK_REFRESH_TOKEN")})
    out = r.json()
    if "access_token" not in out:
        sys.exit("Refresh failed: %s" % json.dumps(out)[:400])
    print("  export TIKTOK_ACCESS_TOKEN=%s" % out["access_token"])
    print("  export TIKTOK_REFRESH_TOKEN=%s" % out["refresh_token"])
    print("\nAccess token good for %s seconds." % out.get("expires_in"))


def cmd_whoami(a):
    d = call("/user/info/", params={
        "fields": "open_id,union_id,display_name,follower_count,following_count,"
                  "likes_count,video_count,profile_deep_link"})
    print(json.dumps(d.get("user", d), indent=2))


def cmd_videos(a):
    d = call("/video/list/", params={"fields": VIDEO_FIELDS},
             body={"max_count": min(a.limit, 20)}, method="POST")
    rows = d.get("videos", [])
    if a.json:
        print(json.dumps(rows, indent=2)); return
    print("%-19s %8s %7s %6s %6s  %s"
          % ("posted", "views", "likes", "comm", "share", "description"))
    for v in rows:
        ts = time.strftime("%Y-%m-%d %H:%M", time.gmtime(v.get("create_time", 0)))
        desc = (v.get("video_description") or v.get("title") or "").replace("\n", " ")[:44]
        print("%-19s %8s %7s %6s %6s  %s"
              % (ts, v.get("view_count", "-"), v.get("like_count", "-"),
                 v.get("comment_count", "-"), v.get("share_count", "-"), desc))
        print("    %s" % v.get("share_url", ""))


def cmd_post(a):
    """PULL_FROM_URL needs the URL's domain verified in the developer portal."""
    if not a.yes:
        print("\nAbout to send to TikTok (%s):\n  %s\n  caption: %s\n"
              % ("DRAFT — you finish it in the app" if a.draft else "DIRECT POST",
                 a.url, a.caption[:160]))
        if input("Type 'post' to go ahead: ").strip().lower() != "post":
            sys.exit("Cancelled. Nothing was sent.")

    if a.draft:
        d = call("/post/publish/inbox/video/init/", method="POST", body={
            "source_info": {"source": "PULL_FROM_URL", "video_url": a.url}})
    else:
        d = call("/post/publish/video/init/", method="POST", body={
            "post_info": {"title": a.caption,
                          "privacy_level": a.privacy,
                          "disable_comment": False},
            "source_info": {"source": "PULL_FROM_URL", "video_url": a.url}})
    pid = d.get("publish_id")
    print("publish_id %s — polling status..." % pid)
    for _ in range(100):
        st = call("/post/publish/status/fetch/", method="POST",
                  body={"publish_id": pid})
        s = st.get("status")
        if s in ("PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"):
            print("done: %s" % s)
            if a.draft:
                print("Open TikTok on your phone — it is waiting in your inbox.")
            return
        if s == "FAILED":
            sys.exit("TikTok failed it: %s" % json.dumps(st)[:300])
        print("  %s" % s)
        time.sleep(5)
    sys.exit("Gave up waiting on %s" % pid)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("refresh", help="mint a new access token").set_defaults(fn=cmd_refresh)
    sub.add_parser("whoami", help="account + follower stats").set_defaults(fn=cmd_whoami)
    v = sub.add_parser("videos", help="recent videos with metrics")
    v.add_argument("--limit", type=int, default=20)
    v.add_argument("--json", action="store_true")
    v.set_defaults(fn=cmd_videos)
    s = sub.add_parser("post", help="send a video (draft, or direct if audited)")
    s.add_argument("--url", required=True)
    s.add_argument("--caption", default="")
    s.add_argument("--draft", action="store_true",
                   help="to the inbox as a draft — works without TikTok's audit")
    s.add_argument("--privacy", default="PUBLIC_TO_EVERYONE",
                   choices=["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"])
    s.add_argument("--yes", action="store_true")
    s.set_defaults(fn=cmd_post)

    a = p.parse_args()
    try:
        a.fn(a)
    except ApiError as exc:
        sys.exit("TikTok API said: %s" % exc)


if __name__ == "__main__":
    main()
