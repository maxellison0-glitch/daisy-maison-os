#!/usr/bin/env python3
"""Lay an audio bed under a Daisy Maison cut, and cut the edit to its beat.

WHY. Max, 30 Jul 2026, looking at the account's best post: the 9,400-view one
reports `track = original sound, artist = DaisyMaison`, which means the music was
baked into the file rather than attached as a TikTok sound. Every post this
system has published went out silent. That is a whole switch we were not using.

WHAT IT TAKES. Any local audio file. Where it came from is a decision made
outside this script, and the routes that don't need one are:

  * Higgsfield `generate_audio` - original, ours outright, no third party
  * TikTok's Commercial Music Library - `tiktok_music_trending`, then attach the
    `song_clip_id` at publish instead of muxing (keeps the sound-page traffic)
  * YouTube Audio Library / Uppbeat / Epidemic / Artlist - a licence we hold
  * anything Max drops in `audio/` himself

Usage:
    python3 audio_bed.py in.mp4 bed.mp3 out.mp4 --start 41.5 --gain -6
    python3 audio_bed.py --beats bed.mp3 --start 41.5 --window 6

    # stills -> a cut whose hard cuts land on the beat
    python3 audio_bed.py --slideshow a.jpg b.jpg --audio bed.mp3 \
        --start 41.5 --beats-per-slide 4 -o out.mp4
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, check=False, **kw)


def probe_bpm(path, start=0.0, window=30.0):
    """Estimate BPM over the window we are actually going to use.

    Deliberately not the whole track: a 3-minute song has an intro at a
    different energy from the drop, and we only ever use ~6-30 seconds of it.
    Returns (bpm, first_beat_offset_sec).
    """
    try:
        import librosa
        import numpy as np
    except ImportError:
        return None, None
    y, sr = librosa.load(path, offset=start, duration=window, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    bpm = float(tempo if not hasattr(tempo, "__len__") else tempo[0])
    first = float(beats[0]) if len(beats) else 0.0
    return round(bpm, 1), round(first, 3)


def duration(path):
    """Seconds, read off ffmpeg's own banner.

    NOT ffprobe. It ships with most ffmpeg builds and is absent from this one -
    found by the tool failing on its first run - so a script that assumes it is
    a script that works on one machine.
    """
    err = _run(["ffmpeg", "-i", path, "-f", "null", "-"]).stderr
    for line in err.splitlines():
        if "Duration:" in line:
            hh, mm, ss = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(hh) * 3600 + int(mm) * 60 + float(ss)
    sys.exit(f"could not read a duration from {path}")


def mux(video, audio, out, start=0.0, gain=-6.0, fade=0.35, keep_original=False):
    """Lay the bed under an existing cut, trimmed to the video's own length."""
    dur = duration(video)
    af = (f"atrim=start={start}:duration={dur},asetpts=N/SR/TB,"
          f"volume={gain}dB,afade=t=in:st=0:d={fade},"
          f"afade=t=out:st={max(0, dur - fade):.3f}:d={fade}")
    cmd = ["ffmpeg", "-y", "-i", video, "-i", audio, "-filter_complex"]
    if keep_original:
        cmd += [f"[1:a]{af}[bed];[0:a][bed]amix=inputs=2:duration=first[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        cmd += [f"[1:a]{af}[a]", "-map", "0:v", "-map", "[a]"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    r = _run(cmd)
    if r.returncode:
        sys.exit(r.stderr.strip().splitlines()[-1] if r.stderr else "ffmpeg failed")
    return out


def slideshow(images, audio, out, start=0.0, beats_per_slide=4, gain=-6.0,
              fade=0.35, size="1080x1920", pad="white"):
    """Stills -> video whose slide changes land on the beat.

    This is the point of the script. A slideshow with 2.6s hard-coded per slide
    is a slideshow with music behind it; a slideshow whose cuts land on the beat
    reads as an edit. Falls back to 2.6s if librosa is not installed, and SAYS SO
    rather than silently producing the worse thing.
    """
    bpm, first = probe_bpm(audio, start, window=beats_per_slide * len(images) * 2.0)
    if bpm:
        per = (60.0 / bpm) * beats_per_slide
        offset = start + (first or 0.0)
        print(f"  {bpm} BPM · {beats_per_slide} beats/slide · {per:.3f}s per slide "
              f"· first beat at +{first:.3f}s")
    else:
        per, offset = 2.6, start
        print("  ! librosa not installed - falling back to a flat 2.6s per slide. "
              "The cuts will NOT land on the beat. pip install librosa to fix.")

    w, h = size.split("x")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        for p in images:
            fh.write(f"file '{os.path.abspath(p)}'\nduration {per:.4f}\n")
        fh.write(f"file '{os.path.abspath(images[-1])}'\n")
        lst = fh.name
    total = per * len(images)
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={pad},fps=30")
    af = (f"atrim=start={offset}:duration={total},asetpts=N/SR/TB,"
          f"volume={gain}dB,afade=t=in:st=0:d={fade},"
          f"afade=t=out:st={max(0, total - fade):.3f}:d={fade}")
    r = _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
              "-i", audio, "-filter_complex", f"[1:a]{af}[a]",
              "-map", "0:v", "-map", "[a]", "-vf", vf,
              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
              "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    os.unlink(lst)
    if r.returncode:
        sys.exit(r.stderr.strip().splitlines()[-1] if r.stderr else "ffmpeg failed")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("audio_pos", nargs="?")
    ap.add_argument("out_pos", nargs="?")
    ap.add_argument("--beats", metavar="AUDIO",
                    help="just report BPM and the first beat, write nothing")
    ap.add_argument("--slideshow", nargs="+", metavar="IMG")
    ap.add_argument("--audio")
    ap.add_argument("-o", "--out")
    ap.add_argument("--start", type=float, default=0.0,
                    help="seconds into the track to start (the hook, not the intro)")
    ap.add_argument("--window", type=float, default=30.0)
    ap.add_argument("--gain", type=float, default=-6.0)
    ap.add_argument("--fade", type=float, default=0.35)
    ap.add_argument("--beats-per-slide", type=int, default=4)
    ap.add_argument("--keep-original", action="store_true",
                    help="mix the bed UNDER the video's own audio instead of replacing it")
    ap.add_argument("--size", default="1080x1920")
    a = ap.parse_args()

    if a.beats:
        bpm, first = probe_bpm(a.beats, a.start, a.window)
        if bpm is None:
            sys.exit("librosa not installed - cannot measure. pip install librosa")
        print(f"{bpm} BPM · first beat +{first}s · one bar (4 beats) = "
              f"{4 * 60 / bpm:.3f}s · 8 beats = {8 * 60 / bpm:.3f}s")
        return

    if a.slideshow:
        if not (a.audio and a.out):
            sys.exit("--slideshow needs --audio and -o")
        print(slideshow(a.slideshow, a.audio, a.out, a.start,
                        a.beats_per_slide, a.gain, a.fade, a.size))
        return

    if not (a.video and (a.audio_pos or a.audio)):
        ap.error("need: video audio out   (or --slideshow / --beats)")
    out = a.out_pos or a.out
    if not out:
        ap.error("need an output path")
    print(mux(a.video, a.audio_pos or a.audio, out, a.start, a.gain,
              a.fade, a.keep_original))


if __name__ == "__main__":
    main()
