#!/usr/bin/env python3
"""Per-post TikTok data, and the ability to LOOK at a post.

    python3 tiktok_posts.py posts --user daisymaison --limit 12 --save
    python3 tiktok_posts.py posts --user someoneelse --limit 8
    python3 tiktok_posts.py look  --url https://www.tiktok.com/@x/video/123

Why this exists
---------------
`daisy-social-analytics` states that TikTok has no per-post data, because the
grid loads from a signed endpoint that returns an empty body without TikTok's
own obfuscated signature. That was true of the approach it described. It is not
true in general: yt-dlp's TikTok extractor reads the same metadata the web
player uses, and returns per-post view counts, like counts and captions without
any login.

Measured 28 Jul 2026 on @daisymaison: eight posts, views 3-796. The skill's
claim is now superseded and has been corrected.

It also closes the harder gap. `ig_public.py` returns numbers and captions but
never images, so it could never answer "does their content LOOK better than
ours". `look` downloads a post and lays its frames out as a contact sheet, which
can be read directly.

TWO WARNINGS, both learned the hard way
---------------------------------------
1. DO NOT install curl_cffi / yt-dlp's impersonation extra. It performs its own
   TLS handshake, which this container's agent proxy resets - every request dies
   with "curl: (35) Recv failure". yt-dlp's native networking works fine. If you
   see that error, uninstall curl_cffi.

2. Like counts come back 0 on some posts and real on others. A 0 here means
   "not returned", NOT "no likes". View counts have been reliable on every post
   tested. Quote views; treat a zero like-count as missing data and say so.

Rate limits: gentler than Instagram's in testing, but not free. One account per
run, and do not loop.
"""
import argparse, json, pathlib, subprocess, sys, datetime, io

HERE = pathlib.Path(__file__).parent
SNAPS = HERE / "tiktok-post-snapshots"
FIELDS = ["id", "title", "view_count", "like_count", "comment_count",
          "repost_count", "upload_date", "duration", "webpage_url"]


def _ytdlp(args):
    return subprocess.run([sys.executable, "-m", "yt_dlp", *args],
                          capture_output=True, text=True)


def posts(user, limit, save):
    url = f"https://www.tiktok.com/@{user.lstrip('@')}"
    fmt = "|".join(f"%({f})s" for f in FIELDS)
    r = _ytdlp(["--skip-download", "--ignore-errors", "--print", fmt,
                url, "--playlist-end", str(limit)])
    rows = []
    for line in r.stdout.splitlines():
        if line.count("|") < len(FIELDS) - 1:
            continue
        parts = line.split("|")
        d = dict(zip(FIELDS, parts))
        for k in ("view_count", "like_count", "comment_count", "repost_count", "duration"):
            d[k] = int(d[k]) if d[k].isdigit() else None
        rows.append(d)

    if not rows:
        print("No posts returned.", file=sys.stderr)
        if "Unable to extract" in r.stderr:
            print("TikTok did not serve the user page. Retry later, or pass a "
                  "single video URL to `look`.", file=sys.stderr)
        return 1

    print(f"@{user} - {len(rows)} posts")
    print(f"{'views':>8} {'likes':>7} {'cmts':>6}  {'date':<9} caption")
    for d in rows:
        lk = "-" if not d["like_count"] else d["like_count"]
        cm = "-" if not d["comment_count"] else d["comment_count"]
        print(f"{d['view_count'] or '-':>8} {lk:>7} {cm:>6}  {d['upload_date']:<9} "
              f"{(d['title'] or '')[:58]}")

    vs = [d["view_count"] for d in rows if d["view_count"]]
    if vs:
        print(f"\nviews  median {sorted(vs)[len(vs)//2]}  best {max(vs)}  worst {min(vs)}")
    zero = sum(1 for d in rows if not d["like_count"])
    if zero:
        print(f"NOTE: {zero}/{len(rows)} posts returned no like count. "
              "That is missing data, not zero likes.")

    if save:
        SNAPS.mkdir(exist_ok=True)
        p = SNAPS / f"{user}-{datetime.date.today()}.json"
        p.write_text(json.dumps({
            "pulled_utc": datetime.datetime.utcnow().isoformat(),
            "username": user, "source": "yt-dlp", "posts": rows}, indent=1))
        print(f"saved {p}")
    return 0


def look(url, n, out):
    """Download a post and lay its frames out so the content can be judged."""
    from PIL import Image, ImageDraw
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    out = pathlib.Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    vid = out.with_suffix(".mp4")

    r = _ytdlp(["-f", "mp4", "-o", str(vid), "--force-overwrites", url])
    if not vid.exists():
        print(r.stderr[-600:], file=sys.stderr)
        return 1

    dur = float(subprocess.run(
        [FF, "-i", str(vid)], capture_output=True, text=True
    ).stderr.split("Duration: ")[1].split(",")[0].split(":")[-1])

    ims = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.2f}", "-i", str(vid),
                              "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                             capture_output=True).stdout
        if not raw:
            continue
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.thumbnail((340, 605))
        ImageDraw.Draw(im).text((6, 4), f"{t:.1f}s", fill=(255, 60, 60))
        ims.append(im)

    if not ims:
        return 1
    w, h = ims[0].size
    sheet = Image.new("RGB", (len(ims) * (w + 6) + 6, h + 12), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (6 + i * (w + 6), 6))
    sheet.save(out.with_suffix(".png"))
    print(out.with_suffix(".png"))
    return 0


ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
a = sub.add_parser("posts"); a.add_argument("--user", required=True)
a.add_argument("--limit", type=int, default=12); a.add_argument("--save", action="store_true")
b = sub.add_parser("look"); b.add_argument("--url", required=True)
b.add_argument("--frames", type=int, default=5); b.add_argument("--out", default="look/post")
n = ap.parse_args()
sys.exit(posts(n.user, n.limit, n.save) if n.cmd == "posts" else look(n.url, n.frames, n.out))
