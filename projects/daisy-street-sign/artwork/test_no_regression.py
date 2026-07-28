#!/usr/bin/env python3
"""
Prove that build.py's DEFAULT output has not moved.

Run this after any change to build.py:

    python3 test_no_regression.py <reference-build.py>

where the reference is the last known-good version (e.g. `git show
HEAD:./build.py > /tmp/ref.py`).

Why it is not a byte compare
----------------------------
A naive `diff` on the SVG reports a failure every single time, because two
timestamps are written on every run: `<daisy:generatedAt>`, and one buried inside
the `head` table of the embedded WOFF font subset. That second one cost real time
to track down — the diff surfaced as a single changed byte deep in a 42,000-character
base64 payload, which looks exactly like a corrupted font.

So: strip every base64 payload and every timestamp, then compare. Anything left
is real.
"""

import re
import subprocess
import sys
import tempfile
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Cases chosen to exercise the branches that matter: the compressed heart path, the
# no-heart path, a colourway, and a short wording that the stretch option affects.
CASES = [
    ("heart, compressed", {},
     ["MR & MRS WINDSOR", "FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024", "486"]),
    ("no heart, colourway", {"SIGN_COLOURWAY": "SAGE", "SIGN_HEART": "0"},
     ["THE HARPERS", "EST. 2026", "486"]),
    ("short wording", {"SIGN_COLOURWAY": "BLACK", "SIGN_HEART": "0"},
     ["MUM'S TAXI", "NO TIPS, NO THANKS", "486"]),
    ("holes off", {"SIGN_HOLES": "0"},
     ["MR & MRS HALE", "WHEN TWO NAMES BECOME ONE", "486"]),
]


def render(script, env_extra, args, out):
    env = dict(os.environ)
    # clear every option so the "default" really is the default
    for k in ("SIGN_COLOURWAY", "SIGN_COLOR", "SIGN_PANEL", "SIGN_HEART",
              "SIGN_HOLES", "SIGN_STRETCH", "SIGN_STRETCH_MAX", "SIGN_LINE2_BOLD"):
        env.pop(k, None)
    env.update(env_extra)
    r = subprocess.run([sys.executable, script, "REG"] + args + [out],
                       capture_output=True, env=env, cwd=HERE)
    if r.returncode:
        raise SystemExit("render failed for %s:\n%s" % (script, r.stderr.decode()[-800:]))
    return [l for l in r.stdout.decode().splitlines() if l.startswith("REG:")]


def canonical(path):
    s = open(path).read()
    s = re.sub(r"base64,[A-Za-z0-9+/=]+", "base64,<PAYLOAD>", s)
    s = re.sub(r"<daisy:generatedAt>[^<]*</daisy:generatedAt>", "<daisy:generatedAt/>", s)
    return s


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    # The reference has to run from inside this directory: build.py resolves its
    # contour source and font assets relative to its own location, so a copy left
    # in /tmp looks for /source/source-data.js and dies.
    import shutil
    ref_src = os.path.abspath(sys.argv[1])
    ref = os.path.join(HERE, "_ref_build_tmp.py")
    shutil.copyfile(ref_src, ref)

    cur = os.path.join(HERE, "build.py")
    failures = 0
    try:
      with tempfile.TemporaryDirectory() as td:
        for name, env_extra, args in CASES:
            a, b = os.path.join(td, "a.svg"), os.path.join(td, "b.svg")
            ma = render(ref, env_extra, args, a)
            mb = render(cur, env_extra, args, b)
            same_geom = canonical(a) == canonical(b)
            same_metrics = ma == mb
            ok = same_geom and same_metrics
            print("%-22s %s" % (name, "PASS" if ok else "FAIL"))
            if not ok:
                failures += 1
                if not same_metrics:
                    print("   metrics differ:\n     ref %s\n     cur %s" % (ma, mb))
                if not same_geom:
                    import difflib
                    d = list(difflib.unified_diff(
                        canonical(a).split("\n"), canonical(b).split("\n"), lineterm=""))
                    for line in d[:12]:
                        print("   " + line[:200])
    finally:
        if os.path.exists(ref):
            os.remove(ref)
    print()
    print("REGRESSION %s" % ("PASS — default output unchanged" if not failures
                             else "FAIL — %d case(s) moved" % failures))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
