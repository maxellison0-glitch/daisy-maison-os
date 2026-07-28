
## tiktok_posts.py — per-post TikTok, added 28 Jul 2026

Supersedes the "TikTok has no per-post data" claim. Needs `pip install yt-dlp`.

    python3 tiktok_posts.py posts --user daisymaison --limit 12 --save
    python3 tiktok_posts.py look  --url <video url>     # download + contact sheet

Never install `curl_cffi`/yt-dlp's impersonation extra — its TLS handshake is
reset by the agent proxy and every request fails with `curl: (35)`.
