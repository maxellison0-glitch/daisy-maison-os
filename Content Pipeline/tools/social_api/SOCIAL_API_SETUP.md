# Connecting Instagram and TikTok directly — no Windsor

Windsor.ai wanted **$118 for a fourth data source** on top of the $23 for three.
Not worth it, and its Instagram write action was `create_image_post` only —
"carousels, video/Reels and stories are not supported."

Meta's and TikTok's own APIs cost **£0** and do more. This replaces Windsor for
social entirely. Windsor stays useful for what it's already connected to (Meta
Ads, Google Ads) where it saves real work.

| | Windsor ($118/extra source) | Direct (free) |
|---|---|---|
| IG post metrics | yes | yes |
| IG account insights | yes | yes |
| Publish IG photo | yes | yes |
| Publish IG **Reel** | **no** | **yes** |
| Publish IG **carousel** | **no** | **yes** |
| TikTok organic metrics | yes | yes |
| TikTok publish | no | **yes — live via Higgsfield** |
| Publish FB Page photo / Reel / text | no | yes |

---

## Part 1 — Instagram (about 15 minutes, all in a browser)

You need an Instagram **Business or Creator** account linked to a Facebook Page.
You already have the Page — Meta Ads shows "Daisy Maison 2.0".

1. **Create a Meta app.** developers.facebook.com → *My Apps* → *Create App* →
   use case **Other** → type **Business** → link it to your business portfolio.
2. **Add the product.** In the app dashboard, add **Instagram** (the
   "Instagram API setup with Facebook login" option, since you have a Page).
3. **Grant the permissions.** Open *Tools → Graph API Explorer*, pick your app,
   and add these:
   `instagram_basic`, `instagram_manage_insights`,
   `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`.
   Click **Generate Access Token** and approve the dialog.
4. **Copy three things** and paste them to me: that token, and the app's **App
   ID** and **App Secret** (*App settings → Basic*).

Then I run:

```bash
export IG_ACCESS_TOKEN='<the token from step 3>'
python instagram.py bootstrap --app-id <id> --app-secret <secret>
```

which exchanges the one-hour token for a 60-day one, finds the Instagram
account behind your Page, and prints the two exports to keep.

### Why this works without App Review

An app in **Development mode** can be used at full permission by its own admins
against their own accounts. App Review and Business Verification are for acting
on *other people's* accounts. We are only ever touching @daisymaison, so we stay
in development mode indefinitely. Expect to confirm this at step 4 — if Meta
does ask for review, the read side still works and only publishing waits.

### Token lifetime, honestly

A Page token derived from a long-lived user token doesn't expire on a timer, but
it dies if you change your Facebook password or revoke the app. When that
happens, redo steps 3–4. **This container is wiped between sessions, so the
token is not stored here** — it lives wherever you keep secrets and gets pasted
in, or set as a Vercel environment variable I can read.

### The publishing catch: Meta needs a public URL

`post-image` and `post-reel` take a **URL**, not a file — Meta fetches the media
itself, so it has to be reachable from the internet. Our assets live in this
repo. The route is: upload the file to the **Shopify CDN** (Files), which hands
back a permanent `cdn.shopify.com` URL, then pass that. I can do that in one
step with the Shopify tools already connected. Artifact links won't work — they
are private.

Meta's limits: JPEG for photos, 4:5 to 1.91:1 aspect, ≤8MB; Reels up to 15
minutes; **50 API-published posts per 24 hours** (`python instagram.py limit`).

### If the Facebook password stays lost — the Instagram Login route

Meta has two auth paths, and only one of them needs a Facebook *account* at
authorise time:

- **Facebook Login for Business** (the steps above) — the IG account authorises
  through its linked Page. Unlocks Instagram AND Facebook Page publishing with
  one token.
- **Instagram Login** — the Business/Creator account authorises directly on
  instagram.com, no Page and no Facebook sign-in. Different host
  (`graph.instagram.com`) and different scopes (`instagram_business_basic`,
  `instagram_business_content_publish`, `instagram_business_manage_comments`).

**The catch that decides it:** creating the Meta *app* in the first place needs
a Meta developer account, which needs a Facebook login — either way. So the
Facebook password is required **once**, to create the app. After that, if the
Page link is the awkward part, Instagram can authorise itself through Instagram.

And Facebook Page posting always needs the Facebook side. There is no route to
publishing on a Page without it.

---

## Part 2 — Facebook Page

No extra setup. `instagram.py bootstrap` already prints the Page id and the Page
token, because a Page access token derived from a long-lived user token carries
Instagram publishing and Page publishing together. Export them as `FB_PAGE_ID`
and `FB_PAGE_TOKEN` and `facebook.py` works immediately.

What the Page can do that Instagram cannot: post plain text with no media.
What it shares with Instagram: Reels need a publicly reachable URL, because Meta
fetches the file itself.

Permissions to add alongside the Instagram ones in step 3:
`pages_manage_posts`, `pages_read_engagement`, `pages_show_list`,
`read_insights`.

---

## Part 3 — TikTok

TikTok splits into a free half and a gated half.

**Metrics — free, no audit.** developers.tiktok.com → create an app → add
**Login Kit** and **Display API** → request scopes `user.info.basic`,
`user.info.stats`, `video.list`. Authorise it against @daisymaison and I get
views, likes, comments and shares per video.

**Publishing — gated.** The Content Posting API only allows direct *public*
posting from an app that has passed TikTok's audit; an unaudited app is forced
to `SELF_ONLY`, or can push a **draft to your inbox** that you finish with one
tap. So:

- **DONE, 27 Jul 2026.** Connected via Higgsfield's `tiktok_connect`; its app
  is already audited, so it publishes publicly with no dev work. The diffuser
  carousel went out this way. Caveat found in practice: Higgsfield exposes
  connect and publish but **no read endpoint**, so the metrics half below is
  still worth doing separately.
- **Or:** `python tiktok.py post --url ... --draft`, then one tap on your phone.
- **Later:** apply for TikTok's audit only if that tap becomes annoying.

Also: the TikTok account currently connected through Windsor is
**northpeptidesuk**, not Daisy Maison, so it tells us nothing about this brand.

---

## What we get that we do not have now

The only real engagement figure this repo owns is "5 likes", reported by Max
from his phone. Everything else in here is Shopify revenue or ad spend. Once
these are connected, `PUBLISH_LOG.md`'s result columns get filled from the
platforms instead of from memory, and Alan's daily read stops having to say
"gap: no organic data".

## Rules that still apply

Publishing is still **propose, never publish** — every `post-*` command stops
and asks before it sends, and `--yes` is for when Max has said go in the
conversation. No customer PII in any caption.
