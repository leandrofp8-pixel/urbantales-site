# "Only with Urban Tales" carousel — production guide

This is a 9-slide IG/TikTok carousel series: 1 cover + 7 numbered "only discover" facts about a
city + 1 app CTA. Read `topics.md` in this folder first to see which cities are already published
and which city is next.

**This is a draft-only step.** Your job is to research, write, and source *candidate* photos —
not to pick final photos or render final images. Leandro picks the photo for each slot himself from
the candidates you provide; final rendering happens afterward, separately. Do not run `render.py`
in this step.

## Voice — this is not the blog

This is punchy social copy, not the long-form Wander Log voice. Look at any existing batch's facts
for the exact register: short, surprising, verifiable claims with the punchiest phrase or number
wrapped in `<b>`. One or two sentences per fact, never more. It's fine — good — to end on the
detail that makes someone want to see it in person ("the bridge still sells only gold today").

Every fact must be a real, checkable claim (web search it). Legend/disputed folklore is fine if
framed that way in the text itself, same rule as the blog.

## Caption (added 2026-09-04, revised same day — minimalist)

Every batch needs an Instagram caption too, not just the 9 slides. Write one and put it in
`draft.json` as `"caption"`. **Minimalist and comment-bait — not informative, not a pitch.** The
app CTA already lives on slide 9; the caption's only job is to make someone stop and comment.
Two lines, then hashtags — nothing else:

1. **Hook** — one short, slightly provocative line built around the single most surprising fact
   from the set (usually the same one that makes the best cover-slide teaser). Withhold the
   answer — "hiding something 99% of visitors never notice," not "here's what's hiding." The
   curiosity gap is the whole point; do not resolve it in the caption.
2. **Comment bait** — one line, a direct prompt to comment, almost always a guess/reaction
   question tied to the hook ("Comment which one shocked you most 👇", "Comment your guess before
   you swipe ⬇️"). Never "double tap if you agree," never "link in bio" (that's the last slide's
   job, not the caption's).
3. **Hashtag block** — a line of three dots on their own (`.`) repeated 3 times (standard IG
   spacing convention to push hashtags below the fold), then ONE line of 6-8 hashtags: the city
   (`#Paris`), a city+travel tag (`#ParisTravel`), 2-3 niche/interest tags (`#HiddenGems`,
   `#TravelFacts`), one landmark-specific tag tied to the hook fact (`#NotreDame`), and
   `#UrbanTales`. Never more than 8 — a wall of tags reads as spam, not reach.

Total caption (excluding hashtags) should read in under 3 seconds. If it takes a beat to parse,
cut it down. See `carousel/drafts/paris/caption.md` for a full worked example.

## What to produce for one batch

1. **Pick the next city.** Read `topics.md`'s Published table, pick something not on it. Check the
   main repo root for a matching `{city}.html` page (bonus for later cross-linking, not required).
2. **Research and write 7 facts** about that city, each with:
   - `headline`: short punchy title (e.g. "A clockmaker built the world's largest dome")
   - `body_html`: 1-2 sentences, key phrases wrapped in `<b>...</b>`, matching the voice above
3. **Source photo candidates for 8 slots** — `cover` (a skyline/aerial shot of the city) plus
   `fact1` through `fact7` (each must show the SPECIFIC landmark/scene that fact is about, not a
   generic city photo). Use the **Wikimedia Commons API — no key needed**:
   ```
   curl -s "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={URL-ENCODED QUERY}&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1400&format=json"
   ```
   Use a specific query per slot (the landmark name, not just the city — e.g. "Florence Duomo dome",
   not "Florence"). Each result's `imageinfo[0].thumburl` is a direct, downloadable image URL; no
   auth, no rate-limit key. `extmetadata` includes `LicenseShortName` and `Artist` — capture both.
   - For each candidate, **look at the downloaded image** before including it and note in one line
     whether it actually matches the described subject (this caught a real miss with Pexels once: a
     Neptune Fountain photo returned for a "David statue" query — don't trust the search query alone).
   - Prefer Public Domain / CC0 candidates when quality is comparable; CC-BY / CC-BY-SA is fine
     otherwise but note it — a credit line may be needed in the IG caption for those.
   - Download 2-3 candidates per slot into `carousel/drafts/{slug}/candidates/{slot}-{n}.jpg`
     (e.g. `cover-1.jpg`, `cover-2.jpg`, `fact3-1.jpg`, `fact3-2.jpg`, `fact3-3.jpg`).
   - If Commons genuinely has nothing usable for a slot, Pexels search (`https://api.pexels.com/v1/search`)
     is a fallback — but no Pexels API key is available in this environment, so only use it if you
     have some other way to query it; otherwise note the gap in the PR rather than blocking.
4. **Pick a real app screenshot** for the CTA slide from the repo root (files like
   `screen-{city}-*-map.png`) showing the "Now Playing" panel if possible — see how the Florence
   batch used `screen-florence-duomo-map.png`. If this city has no existing screenshot, note that
   in the PR and use the closest available city's screenshot as a placeholder.
5. **Write the caption** per the Caption section above.
6. **Write `carousel/drafts/{slug}/draft.json`**:
   ```json
   {
     "badge_num": 7,
     "city": "VIENNA",
     "flag": "🇦🇹",
     "cta_screenshot": "screen-vienna-hofburg-map.png",
     "caption": "... the full caption text, formatted per the Caption section above ...",
     "facts": [
       {"slot": "fact1", "headline": "...", "body_html": "...",
        "candidates": [
          {"file": "candidates/fact1-1.jpg", "source_url": "...", "license": "CC0", "artist": "...", "note": "matches — clear shot of X"},
          {"file": "candidates/fact1-2.jpg", "source_url": "...", "license": "CC-BY-SA-4.0", "artist": "...", "note": "matches, different angle"}
        ]},
       ... one entry per fact, in order ...
     ],
     "cover_candidates": [
       {"file": "candidates/cover-1.jpg", "source_url": "...", "license": "...", "artist": "...", "note": "..."},
       {"file": "candidates/cover-2.jpg", "source_url": "...", "license": "...", "artist": "...", "note": "..."}
     ]
   }
   ```
7. **Move the topic entry** in `topics.md` from "Next batch" into the Published table with the new
   batch number and city, and set the following batch number as TBD.

## Publishing — same rule as the blog: PR, never push to main

```
git checkout -b carousel/{slug}
git add carousel/drafts/{slug} carousel/topics.md
git commit -m "Carousel batch #{n}: {city} — candidates for review"
git push -u origin carousel/{slug}
gh pr create --title "Carousel #{n}: {city} — photo picks needed" --body "..."
```

In the PR body, show every candidate image so Leandro can review without checking out the branch —
embed each one as `https://raw.githubusercontent.com/leandrofp8-pixel/urbantales-site/carousel/{slug}/carousel/drafts/{slug}/candidates/{file}`
(a plain markdown image link works directly in a GitHub PR body). Group them by slot, in order
(cover, fact1..fact7), with each fact's headline/body text directly above its candidates so the PR
reads top-to-bottom like the finished carousel will. List your visual-match note under each
candidate. Include the full caption (from `draft.json`) in its own section near the top of the PR
body, in a code block so line breaks/hashtags render exactly as they'll post. End the PR body with:
"Reply with your picks (e.g. \"cover: 2, fact1: 1, fact3: 3\") and any caption edits, and the final
render happens after." Never merge your own PR, never push to `main` directly.
