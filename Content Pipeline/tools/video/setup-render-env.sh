#!/usr/bin/env bash
# Rebuild the local video render environment. Run this once per container.
#
# Why this file exists
# --------------------
# Everything Daisy Maison *thinks* lives in git. The two things that cannot are
# the render binaries: a full FFmpeg build and the Chrome that HyperFrames pins.
# Together they are ~250 MB of platform-specific binary, so they are fetched, not
# committed. Without them `hyperframes render` fails, and the failure looks like
# a broken pipeline rather than a missing dependency.
#
# The trap this script exists to avoid
# ------------------------------------
# This container DOES ship an ffmpeg, at /opt/pw-browsers/ffmpeg-1011/ffmpeg-linux.
# It is Playwright's build and it is compiled with --disable-everything: VP8 and
# WebM only, no H.264, no MP4 muxer. It answers `ffmpeg -version` perfectly and
# then cannot encode anything either platform accepts. Do not reach for it.
# Measured 28 Jul 2026.
#
# Usage
# -----
#   source "Content Pipeline/tools/video/setup-render-env.sh"
#
# Source it rather than running it - the point is the PATH export. Then:
#   cd "Content Pipeline/Creative Studio/video/<project>"
#   npx hyperframes check && npx hyperframes render --quality high --output out.mp4
set -euo pipefail

DM_VIDEO_HOME="${DM_VIDEO_HOME:-$HOME/.daisy-video}"
mkdir -p "$DM_VIDEO_HOME/bin"

if [ ! -x "$DM_VIDEO_HOME/bin/ffmpeg" ]; then
  echo "Fetching a full FFmpeg (H.264 + MP4)..."
  npm i ffmpeg-static ffprobe-static --no-save --prefix "$DM_VIDEO_HOME/ff" >/dev/null
  ln -sf "$DM_VIDEO_HOME/ff/node_modules/ffmpeg-static/ffmpeg" "$DM_VIDEO_HOME/bin/ffmpeg"
  ln -sf "$DM_VIDEO_HOME/ff/node_modules/ffprobe-static/bin/linux/x64/ffprobe" \
         "$DM_VIDEO_HOME/bin/ffprobe"
fi

export PATH="$DM_VIDEO_HOME/bin:$PATH"

# Confirm we got a real build and not a stripped one. A silent VP8-only ffmpeg
# is the exact failure this script is written to prevent, so check the encoder
# rather than the version string.
#
# Retried, and stderr kept: ffmpeg-static downloads its binary in a postinstall,
# and on 28 Jul 2026 `npm i` returned before the file was fully written. The
# encoder probe then failed on a half-written binary and, because stderr was
# being discarded, reported "no libx264" for a build that has libx264 compiled
# in. A missing codec and a truncated download need different fixes, so the
# script must not print the first message for the second cause.
enc_err=""
for attempt in 1 2 3; do
  if enc_err=$(ffmpeg -hide_banner -encoders 2>&1) && \
     printf '%s' "$enc_err" | grep -q libx264; then
    enc_err=""
    break
  fi
  [ "$attempt" -lt 3 ] && sleep 2
done
if [ -n "$enc_err" ]; then
  echo "FFmpeg on PATH cannot encode H.264. Its own output was:" >&2
  printf '%s\n' "$enc_err" | tail -5 >&2
  echo "If that lists no libx264, the build is stripped - refetch, do not use" >&2
  echo "Playwright's ffmpeg. Aborting." >&2
  return 1 2>/dev/null || exit 1
fi

# HyperFrames pins a Chrome build because rendered pixels drift between Chrome
# versions. Let it fetch its own; the container's Chromium is a different build.
npx --yes hyperframes browser ensure >/dev/null 2>&1 || true

echo "Render environment ready."
echo "  ffmpeg  $(ffmpeg -version | head -1 | cut -d' ' -f3)"
echo "  chrome  $(npx --yes hyperframes browser path 2>/dev/null | tail -1)"
