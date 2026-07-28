#!/usr/bin/env python3
"""Trending audio: find it, measure it, cut the edit to it.

    # 1. save the chart (paste tiktok_music_trending's JSON on stdin)
    tiktok_music_trending  ->  python3 trend_audio.py chart --save

    # 2. pull the previews so they can be measured
    python3 trend_audio.py fetch --top 20

    # 3. measure them - this is the point of the tool
    python3 trend_audio.py analyse --all
    python3 trend_audio.py analyse --track "Ok I Like It"

    # 4. get animation cues that land ON the beat
    python3 trend_audio.py cues --track "Ok I Like It" --dur 4.04 --events 3

    # 5. lay a bed under a cut (see the licence note before you do)
    python3 trend_audio.py bed --track "..." --video in.mp4 --out out.mp4 --at 12.5

WHY THIS EXISTS
---------------
Two separate problems, one tool.

The obvious one is that our videos were silent. The less obvious one, and the
bigger one, is that our animation cues were numbers somebody typed. Pills at
0.25 / 1.35, tag at 2.20 - chosen because they looked about right. On a platform
where everything is watched with sound on, a cue that lands 80ms off the beat
reads as cheap even when the viewer cannot say why. `cues` fixes that: it takes
the track's actual beat grid and snaps our events to it.

THE LICENCE LINE - READ IT, IT IS NOT DECORATION
------------------------------------------------
TikTok's Commercial Music Library tracks are licensed for use ON TIKTOK, through
TikTok. That covers exactly one route:

  ROUTE A (clean): attach the track at publish time with `music_sound_id`
  (the song_clip_id from the chart). Nothing is downloaded, TikTok mixes it, and
  the platform boosts its own audio - which is the whole reason to use a
  trending sound in the first place.

  ROUTE B (NOT covered by that licence): download the preview, mux it into an
  mp4, post that file anywhere - Instagram, the website, an ad. That is a
  different use and the CML licence does not grant it.

So: `fetch` downloads previews for MEASUREMENT. `cues` uses the measurement and
touches no audio. Both are fine for either platform, because the output is
timing numbers, not sound. `bed` actually embeds audio, and you must supply a
track you hold the rights to - our own, a library we pay for, or the artist's
permission. It will not stop you pointing it at a CML preview; it just means
you did that knowingly.

WHAT THE MEASUREMENTS ARE FOR, GIVEN NOBODY HERE CAN LISTEN
-----------------------------------------------------------
An agent cannot hear a track, so "does this slap" is not answerable from here.
These are answerable, and they are the ones that change an edit:

  bpm          does a 4s cut land on a whole number of bars? 120bpm = 8 beats
               in 4.0s, which is exactly two bars. That is a clean loop point.
  beats        where to put a pill, a tag, a cut.
  lift_at      where the track stops being intro and starts being the bit
               people know. Trim to here, not to 0:00.
  brightness   spectral centroid in Hz. Low is warm/mellow, high is bright and
               busy. Brand is "premium and frictionless, never AI spectacle" -
               so this is a real filter, not a stat.
  busyness     onsets per second. High means a lot happening; a 4s product cut
               with two captions will fight it.

Say what these are: measurements, plus heuristics on top (the downbeat guess
assumes 4/4). They narrow a 100-track list to a handful. A human still picks.
"""
import argparse, json, pathlib, subprocess, sys, datetime, re, math

HERE = pathlib.Path(__file__).parent
LIB = HERE / "library"
CHARTS = HERE / "charts"


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def _ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _load(path):
    """Decode to mono 22.05k.

    Route it through ffmpeg rather than letting librosa reach for audioread ->
    mpg123. These CDN previews have junk before the first MPEG header, so
    mpg123 floods stderr with resync errors on every single track and buries
    the actual table. ffmpeg decodes them silently and identically.
    """
    import numpy as np
    r = subprocess.run([_ffmpeg(), "-v", "quiet", "-i", str(path),
                        "-f", "f32le", "-ac", "1", "-ar", "22050", "-"],
                       capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None, 22050
    return np.frombuffer(r.stdout, dtype=np.float32).copy(), 22050


def _dur(path):
    """Duration via ffmpeg stderr - this container has no ffprobe."""
    out = subprocess.run([_ffmpeg(), "-i", str(path)],
                         capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", out)
    if not m:
        return None
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


# ---------------------------------------------------------------- chart

def chart(save):
    """Read tiktok_music_trending JSON on stdin and file it."""
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"stdin was not JSON: {e}", file=sys.stderr)
        return 1
    tracks = data.get("tracks", data if isinstance(data, list) else [])
    if not tracks:
        print("No tracks in that payload.", file=sys.stderr)
        return 1

    print(f"{len(tracks)} tracks")
    for t in tracks[:20]:
        print(f"{t.get('rank','-'):>4}  {t.get('name','?')[:44]:<44} "
              f"{t.get('artist','?')[:26]:<26} {t.get('duration_sec','?')}s")
    if len(tracks) > 20:
        print(f"... and {len(tracks)-20} more")

    if save:
        CHARTS.mkdir(exist_ok=True)
        p = CHARTS / f"tiktok-trending-{datetime.date.today()}.json"
        p.write_text(json.dumps({"pulled_utc": datetime.datetime.utcnow().isoformat(),
                                 "source": "tiktok_music_trending",
                                 "tracks": tracks}, indent=1))
        print(f"\nsaved {p}")
        print("The chart is a SNAPSHOT. Trending means it moves - re-pull before "
              "you build a week's content on it.")
    return 0


def _latest_chart():
    if not CHARTS.exists():
        return None
    ps = sorted(CHARTS.glob("tiktok-trending-*.json"))
    return json.loads(ps[-1].read_text()) if ps else None


# ---------------------------------------------------------------- fetch

def fetch(top):
    c = _latest_chart()
    if not c:
        print("No chart saved. Run `chart --save` first.", file=sys.stderr)
        return 1
    LIB.mkdir(exist_ok=True)
    meta_path = LIB / "index.json"
    index = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    got = 0
    for t in c["tracks"][:top]:
        url = t.get("preview_url")
        if not url:
            continue
        name = _slug(f"{t.get('name','')}-{t.get('artist','')}")
        dest = LIB / f"{name}.mp3"
        if not dest.exists():
            r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60",
                                "-o", str(dest), url], capture_output=True, text=True)
            if r.returncode != 0 or not dest.exists() or dest.stat().st_size < 4096:
                dest.unlink(missing_ok=True)
                print(f"  fail  {t.get('name','?')[:40]}  {r.stderr.strip()[:60]}")
                continue
        index[name] = {"name": t.get("name"), "artist": t.get("artist"),
                       "song_clip_id": t.get("song_clip_id"),
                       "rank": t.get("rank"), "file": dest.name}
        got += 1
        print(f"  ok    {t.get('name','?')[:40]:<42} rank {t.get('rank')}")

    meta_path.write_text(json.dumps(index, indent=1))
    print(f"\n{got} tracks in {LIB}")
    print("These are PREVIEWS, downloaded to be measured. To use one on TikTok, "
          "pass its song_clip_id as music_sound_id at publish - do not mux it.")
    return 0


# ---------------------------------------------------------------- analyse

def _measure(path):
    import numpy as np, librosa
    y, sr = _load(path)
    if y is None or len(y) < sr:
        return None
    dur = len(y) / sr

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    tempo = float(np.atleast_1d(tempo)[0])

    rms = librosa.feature.rms(y=y)[0]
    rt = librosa.times_like(rms, sr=sr)
    # Reference level is the 95th percentile, NOT the max. The max is one
    # transient - a single snare crack - so thresholding against it means a
    # track never "reaches" its own loud section and lift comes back empty.
    # That was the first version of this and it returned nothing on 15 of 20
    # tracks. The percentile is the level the track actually sits at when busy.
    ref = float(np.percentile(rms, 95)) or 1e-9
    hold = max(1, int(0.5 / (rt[1] - rt[0]))) if len(rt) > 1 else 1
    lift = None
    for i in range(max(1, len(rms) - hold)):
        if (rms[i:i + hold] > 0.60 * ref).all():
            lift = float(rt[i])
            break

    onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")
    centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())

    return {"file": path.name, "dur": dur, "bpm": tempo,
            "beats": [float(b) for b in beats],
            "lift_at": lift, "busyness": len(onsets) / dur,
            "brightness": centroid,
            "rms_db": float(20 * math.log10(ref))}


def _bars(bpm, dur):
    """How many beats/bars fit a cut of `dur`. Whole bars loop cleanly."""
    beats = dur / (60.0 / bpm)
    return beats, beats / 4.0


def analyse(which, all_):
    LIB.mkdir(exist_ok=True)
    idx = json.loads((LIB / "index.json").read_text()) if (LIB / "index.json").exists() else {}
    files = sorted(LIB.glob("*.mp3"))
    if which:
        files = [f for f in files if _slug(which) in f.stem]
    elif not all_:
        print("Pass --all or --track <name>.", file=sys.stderr)
        return 1
    if not files:
        print("Nothing in the library. Run `fetch` first.", file=sys.stderr)
        return 1

    print(f"{'track':<40} {'bpm':>6} {'dur':>6} {'lift':>6} {'busy':>6} "
          f"{'bright':>7}  4.0s fits")
    print("-" * 92)
    rows = []
    for f in files:
        m = _measure(f)
        if not m:
            continue
        meta = idx.get(f.stem, {})
        label = (meta.get("name") or f.stem)[:38]
        b, bars = _bars(m["bpm"], 4.0)
        fit = f"{b:.1f} beats / {bars:.2f} bars"
        flag = " <-- clean" if abs(bars - round(bars)) < 0.06 and bars >= 1 else ""
        lift = "-" if m["lift_at"] is None else f"{m['lift_at']:.1f}"
        print(f"{label:<40} {m['bpm']:>6.1f} {m['dur']:>6.1f} {lift:>6} "
              f"{m['busyness']:>6.1f} {m['brightness']:>7.0f}  {fit}{flag}")
        rows.append((label, m))

    print("\nbpm      measured tempo.  dur  preview length.  lift  where it stops")
    print("         being intro: first point holding 60% of the track's 95th-")
    print("         percentile level for 0.5s. '-' means it never settles there.")
    print("busy     onsets/sec. Over ~5 will fight two captions in a 4s cut.")
    print("bright   spectral centroid Hz. Low = warm, high = bright/busy.")
    print("'clean'  the cut length is a whole number of bars, so it loops without")
    print("         a musical seam. That is the one to want for a 4s product cut.")
    print("\nNone of this says whether a track is GOOD. It says which ones can be")
    print("cut to 4 seconds without sounding chopped. A human still picks.")
    return 0


# ---------------------------------------------------------------- sounds

def sounds(users, limit):
    """What sound is each post using, and did that post do numbers?

    This is the one that answers "find popular audio" with evidence instead of
    a chart. A chart tells you what is popular in general. This tells you what
    is on posts in OUR niche that actually performed - which is a different and
    much more useful list.

    YouTube is not the source for this and cannot be from here (see the note in
    `grab`). TikTok is, and it works.
    """
    rows = []
    for user in users:
        u = user.lstrip("@")
        url = f"https://www.tiktok.com/@{u}"
        r = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--skip-download", "--ignore-errors",
             "--print", "%(view_count)s|%(track)s|%(artist)s|%(title)s|%(webpage_url)s",
             url, "--playlist-end", str(limit)],
            capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if line.count("|") < 4:
                continue
            v, track, artist, title, link = line.split("|", 4)
            rows.append({"user": u,
                         "views": int(v) if v.isdigit() else None,
                         "track": None if track in ("NA", "None", "") else track,
                         "artist": None if artist in ("NA", "None", "") else artist,
                         "title": title, "url": link})
        if not r.stdout.strip():
            print(f"  @{u}: nothing returned", file=sys.stderr)

    if not rows:
        print("No posts returned.", file=sys.stderr)
        return 1

    rows.sort(key=lambda d: d["views"] or -1, reverse=True)
    print(f"{'views':>8}  {'account':<16} {'sound':<34} {'artist':<20} post")
    print("-" * 104)
    for d in rows:
        print(f"{d['views'] if d['views'] is not None else '-':>8}  "
              f"@{d['user']:<15} {(d['track'] or '(original / not returned)')[:32]:<34} "
              f"{(d['artist'] or '-')[:18]:<20} {d['title'][:30]}")

    # which sounds recur, and what they averaged
    agg = {}
    for d in rows:
        if not d["track"]:
            continue
        a = agg.setdefault((d["track"], d["artist"]), [])
        if d["views"] is not None:
            a.append(d["views"])
    ranked = sorted(((k, v) for k, v in agg.items() if v),
                    key=lambda kv: sum(kv[1]) / len(kv[1]), reverse=True)
    if ranked:
        print(f"\n{'sound':<36} {'uses':>5} {'mean views':>11}")
        for (t, ar), vs in ranked[:15]:
            print(f"{(t or '?')[:34]:<36} {len(vs):>5} {sum(vs)//len(vs):>11}")

    print("\nA sound name here is what TikTok reports for that post. To USE one,")
    print("attach it at publish - searching TikTok for the sound name gives you")
    print("the sound page and its id. Do NOT rip the audio and mux it: a muxed")
    print("file is not attached to the sound, so it does not appear in that")
    print("sound's feed, which is where the discovery actually comes from.")
    print("Small samples move a lot. Two posts on one sound is not a finding.")
    return 0


# ---------------------------------------------------------------- grab

def grab(url, query, out):
    """Pull audio from a URL (TikTok/IG/direct) or search YouTube.

    YOUTUBE MEDIA DOWNLOAD DOES NOT WORK FROM THIS CONTAINER. Measured
    28 Jul 2026: search and metadata come through fine, but every player client
    is refused on the actual stream -

        default / web_embedded  HTTP 403 Forbidden
        web / ios               "Sign in to confirm you're not a bot"
        tv / mweb               requested format not available

    That is YouTube blocking a datacenter IP, not a missing flag. A JS runtime
    IS present and wired up (`--js-runtimes node:/opt/node22/bin/node`, which
    clears the deprecation warning) and it changes nothing. The only fix is
    real YouTube cookies, which are a credential and do not belong in this repo
    or this container.

    TikTok downloads work. That is the route that is actually open.
    """
    out = pathlib.Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if query:
        r = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--skip-download", "--flat-playlist",
             "--print", "%(title)s | %(duration)s s | %(view_count)s views | %(webpage_url)s",
             f"ytsearch10:{query}"], capture_output=True, text=True)
        print(r.stdout or r.stderr[-500:])
        print("\nSearch works; DOWNLOAD from YouTube does not from here - see the")
        print("note in this function. Use these results to identify a track, then")
        print("obtain it somewhere you hold rights to.")
        return 0

    tmp = out.with_suffix(".src")
    r = subprocess.run([sys.executable, "-m", "yt_dlp",
                        "--js-runtimes", "node:/opt/node22/bin/node",
                        "-o", str(tmp), "--force-overwrites", "--no-playlist", url],
                       capture_output=True, text=True)
    got = next(iter(sorted(out.parent.glob(tmp.stem + ".*"))), None)
    if r.returncode != 0 or not got:
        print(r.stderr[-800:], file=sys.stderr)
        if "not a bot" in r.stderr or "403" in r.stderr:
            print("\nThat host refused the download from this IP. YouTube does this "
                  "to datacenter addresses; TikTok does not.", file=sys.stderr)
        return 1

    dst = out.with_suffix(".mp3")
    subprocess.run([_ffmpeg(), "-y", "-v", "error", "-i", str(got),
                    "-vn", "-acodec", "libmp3lame", "-q:a", "2", str(dst)], check=False)
    got.unlink(missing_ok=True)
    if not dst.exists():
        print("Downloaded, but no audio stream to extract.", file=sys.stderr)
        return 1
    print(f"wrote {dst}  ({_dur(dst):.1f}s)")
    print("This is someone else's recording. Fine to MEASURE (analyse/cues).")
    print("Embedding it in a post we publish is a rights decision, not a "
          "technical one - that call is Max's, not this tool's.")
    return 0


# ---------------------------------------------------------------- cues

def cues(track, dur, events, start):
    """Snap N animation events onto the track's beat grid."""
    files = [f for f in sorted(LIB.glob("*.mp3")) if _slug(track) in f.stem]
    if not files:
        print(f"No track matching '{track}' in the library.", file=sys.stderr)
        return 1
    m = _measure(files[0])
    if not m:
        return 1

    period = 60.0 / m["bpm"]
    origin = start if start is not None else (m["lift_at"] or 0.0)
    # beats from `origin`, expressed relative to the start of our cut
    grid = [b - origin for b in m["beats"] if origin - 1e-6 <= b <= origin + dur + period]
    if not grid:
        grid = [i * period for i in range(int(dur / period) + 2)]
    grid = [round(g, 3) for g in grid if -0.02 <= g <= dur + 0.02]

    beats_in, bars_in = _bars(m["bpm"], dur)
    print(f"{files[0].stem}")
    print(f"  bpm {m['bpm']:.1f}   beat every {period:.3f}s")
    print(f"  trim start {origin:.2f}s  (the lift, so the cut opens on the good bit)")
    print(f"  a {dur:.2f}s cut = {beats_in:.2f} beats = {bars_in:.2f} bars")
    if abs(bars_in - round(bars_in)) > 0.06:
        want = round(bars_in) * 4 * period
        print(f"  NOT a whole number of bars. {want:.2f}s would be {round(bars_in)} "
              f"bars exactly - retime the cut to that if you want it to loop clean.")
    print(f"\n  beat grid: {', '.join(f'{g:.2f}' for g in grid)}")

    # place events on beats, spread across the cut, skipping beat 0 (too early
    # to read) unless there is only one event.
    usable = [g for g in grid if g >= 0.15]
    if not usable:
        print("No usable beat inside the cut.", file=sys.stderr)
        return 1
    step = max(1, len(usable) // max(events, 1))
    picks = [usable[min(i * step, len(usable) - 1)] for i in range(events)]

    print(f"\n  {events} events snapped to beats:")
    names = ["PILL_1_IN", "PILL_2_IN", "TAG_IN", "EVENT_4", "EVENT_5", "EVENT_6"]
    for i, p in enumerate(picks):
        print(f"    {names[i] if i < len(names) else f'EVENT_{i+1}':<12} = {p:.2f}")
    print("\n  Paste these into build_v2.py in place of the hand-typed numbers.")
    print("  Beat detection is an estimate; if a cue looks wrong on the frame,")
    print("  trust the frame.")
    return 0


# ---------------------------------------------------------------- bed

def bed(track, video, out, at, vol, duck):
    files = [f for f in sorted(LIB.glob("*.mp3")) if _slug(track) in f.stem]
    src = pathlib.Path(track) if pathlib.Path(track).exists() else (files[0] if files else None)
    if not src:
        print(f"No track matching '{track}'.", file=sys.stderr)
        return 1

    print("LICENCE: this embeds audio into a file you will post. A TikTok")
    print("Commercial Music Library preview is NOT licensed for that - use")
    print("music_sound_id at publish instead. Continue only with a track you")
    print("hold the rights to.\n")

    vdur = _dur(video)
    if vdur is None:
        print("Could not read the video duration.", file=sys.stderr)
        return 1

    fade_out = max(0.0, vdur - 0.35)
    if duck:
        # keep the SFX on top: the video's own audio ducks the bed
        af = (f"[1:a]atrim={at}:{at+vdur},asetpts=PTS-STARTPTS,"
              f"afade=t=in:st=0:d=0.20,afade=t=out:st={fade_out:.2f}:d=0.35,"
              f"volume={vol}[bedraw];"
              f"[0:a]asplit=2[sfx][sc];"
              f"[bedraw][sc]sidechaincompress=threshold=0.05:ratio=8:attack=5:release=200[bed];"
              f"[sfx][bed]amix=inputs=2:duration=first:dropout_transition=0,"
              f"alimiter=limit=0.95[a]")
    else:
        af = (f"[1:a]atrim={at}:{at+vdur},asetpts=PTS-STARTPTS,"
              f"afade=t=in:st=0:d=0.20,afade=t=out:st={fade_out:.2f}:d=0.35,"
              f"volume={vol}[bed];"
              f"[0:a][bed]amix=inputs=2:duration=first:dropout_transition=0,"
              f"alimiter=limit=0.95[a]")

    cmd = [_ffmpeg(), "-y", "-i", str(video), "-i", str(src),
           "-filter_complex", af, "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:], file=sys.stderr)
        return 1
    print(f"wrote {out}  ({vdur:.2f}s, bed from {at:.2f}s, vol {vol}"
          f"{', ducked under SFX' if duck else ''})")
    return 0


# ---------------------------------------------------------------- cli

ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)

c = sub.add_parser("chart", help="file a tiktok_music_trending payload from stdin")
c.add_argument("--save", action="store_true")

f = sub.add_parser("fetch", help="download previews for measurement")
f.add_argument("--top", type=int, default=20)

a = sub.add_parser("analyse", help="bpm / lift / busyness / brightness")
a.add_argument("--track"); a.add_argument("--all", action="store_true")

u = sub.add_parser("cues", help="snap animation events to the beat grid")
u.add_argument("--track", required=True)
u.add_argument("--dur", type=float, required=True)
u.add_argument("--events", type=int, default=3)
u.add_argument("--start", type=float, default=None)

s = sub.add_parser("sounds", help="what sound is on posts that actually performed")
s.add_argument("--users", nargs="+", required=True)
s.add_argument("--limit", type=int, default=12)

g = sub.add_parser("grab", help="pull audio from a URL, or search YouTube")
g.add_argument("--url"); g.add_argument("--query")
g.add_argument("--out", default="library/grabbed")

b = sub.add_parser("bed", help="mux a bed under a cut (rights required)")
b.add_argument("--track", required=True); b.add_argument("--video", required=True)
b.add_argument("--out", required=True); b.add_argument("--at", type=float, default=0.0)
b.add_argument("--vol", type=float, default=0.35)
b.add_argument("--duck", action="store_true")

n = ap.parse_args()
sys.exit({
    "chart":   lambda: chart(n.save),
    "fetch":   lambda: fetch(n.top),
    "analyse": lambda: analyse(n.track, n.all),
    "sounds":  lambda: sounds(n.users, n.limit),
    "grab":    lambda: grab(n.url, n.query, n.out),
    "cues":    lambda: cues(n.track, n.dur, n.events, n.start),
    "bed":     lambda: bed(n.track, n.video, n.out, n.at, n.vol, n.duck),
}[n.cmd]())
