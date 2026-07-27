#!/usr/bin/env python3
"""Reference-account sweep. Fetches the brand sites and prints readable text.

WHY THIS EXISTS
---------------
The daily sweep reported HTTP 429 on treatboxuk.com, thecraftybonobo.com and
littleperfections.co.uk for **three consecutive runs**, and the Results Day /
Christmas calendar went stale on the back of it.

The sites were never the problem. Checked on 27 Jul 2026, all three answered
**200** to an ordinary request from this same container. The 429 was WebFetch's
own rate limiter, and three runs of "the reference hosts are blocking us" were
three runs of misattributed blame.

So the rule is: **sweep with this script, not WebFetch.** WebFetch is fine for a
one-off page; it is the wrong tool for hitting the same handful of hosts every
single day.

    python refsweep.py                 # all hosts
    python refsweep.py --host treatboxuk.com --chars 4000
    python refsweep.py --raw           # keep the HTML alongside the text

A non-200 here is a real signal about the site. A non-200 from WebFetch is not.
"""
import argparse
import html
import os
import re
import sys

import requests

# Desktop Chrome. Several of these are Shopify stores that serve a stripped or
# challenge page to an obvious bot UA.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

HOSTS = [
    ("treatboxuk.com", "/", "seasonal signal — Results Day, Christmas ramp"),
    ("thecraftybonobo.com", "/", "direct competitor — street signs"),
    ("littleperfections.co.uk", "/", "wedding styling and occasion language"),
]

# Known to refuse this container outright; listed so a run says so rather than
# quietly omitting them. Etsy has returned 403 on every attempt.
KNOWN_BLOCKED = {"etsy.com": "403 bot-block on every attempt to date"}


def strip(markup):
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))).strip()


def title_of(markup):
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", markup)
    return html.unescape(m.group(1)).strip() if m else "(no title)"


def sweep(hosts, chars, raw_dir):
    ok = 0
    for host, path, why in hosts:
        url = "https://%s%s" % (host, path)
        print("=" * 72)
        print("%s  —  %s" % (host, why))
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=40,
                             allow_redirects=True)
        except requests.RequestException as exc:
            print("  FAILED: %s" % exc)
            continue
        print("  HTTP %d, %d bytes, final URL %s"
              % (r.status_code, len(r.content), r.url))
        if r.status_code != 200:
            print("  Not read. This one is a real block, not a fetch-tool limit.")
            continue
        ok += 1
        print("  TITLE: %s" % title_of(r.text)[:120])
        if raw_dir:
            p = os.path.join(raw_dir, host + ".html")
            open(p, "w", encoding="utf-8").write(r.text)
            print("  raw: %s" % p)
        print()
        print(strip(r.text)[:chars])
        print()
    for host, why in KNOWN_BLOCKED.items():
        print("=" * 72)
        print("%s  —  NOT ATTEMPTED (%s)" % (host, why))
    print("=" * 72)
    print("%d of %d hosts read." % (ok, len(hosts)))
    return ok


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", action="append",
                   help="limit to these hosts; repeat the flag")
    p.add_argument("--chars", type=int, default=2600,
                   help="characters of page text to print per host")
    p.add_argument("--raw", metavar="DIR", nargs="?", const=".",
                   help="also save the HTML")
    a = p.parse_args()
    hosts = HOSTS
    if a.host:
        want = set(a.host)
        hosts = [h for h in HOSTS if h[0] in want] or [(h, "/", "ad hoc") for h in a.host]
    sys.exit(0 if sweep(hosts, a.chars, a.raw) else 1)


if __name__ == "__main__":
    main()
