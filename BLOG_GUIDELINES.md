# The Wander Log — writing & publishing guide

This file is the complete brief for whoever (human or agent) writes the next post for
`urbantales.net/blog.html`, "The Wander Log." Read this whole file before drafting anything.
Also read `blog-topics.md` in this same repo to see what's already been covered and what's next in the queue.

## What this blog is for

Urban Tales is a GPS audio guide app — it narrates hidden history automatically as people walk past
landmarks. The blog exists to (1) rank in Google for the kind of searches curious travelers actually
make, and (2) give people a reason to trust the app before they've heard a single narration — by
proving, in writing, that we know real, specific, non-Wikipedia-obvious things about these places.

The blog is deliberately **not** styled like the app's marketing pages. It reads as a separate,
human-run travel blog ("The Wander Log") that happens to be made by the Urban Tales team, with the
app mentioned the way a friend would mention it — not as an ad unit bolted onto content.

## Voice — read this twice

Write like a knowledgeable friend who knows the place well and is telling the reader exactly what to
look for. There is no named individual author (no invented persona, no fake bio, no fake headshot) —
bylines read "Written by the Urban Tales team."

**Never invent a first-hand experience (decided by Leandro, 2026-10-12).** Do not write "we stood
here", "we got there at 8am", "I watched…", or any visit, queue, conversation or moment that did not
happen. Readers trust the blog because what it says is true; a made-up visit is a lie, however vivid.
Turn the same detail into a **tip addressed to the reader**:
- Instead of "We stood at the left edge and finally saw the stone," write "Stand at the fountain's
  left edge and look for the tall stone vase: that's the one the barber story is about."
- Instead of "We got there early and there were already forty people ahead of us," write "Arrive
  before 8am; by mid-morning the crowd is several rows deep."
A first-person anecdote is allowed **only** when Leandro supplies a real one; say so in the PR
description ("anecdote from Leandro's visit, <date>").

**Concrete rules:**
- Open with a specific, surprising fact or scene — never a throat-clearing intro ("When you think of
  Rome, you probably think of..."). Look at `blog-trevi-fountain-secret-history.html` for the pattern:
  a one-sentence hook with a real number or a real name in it.
- Vary sentence length on purpose. Follow a long sentence with a short one. A paragraph that is all
  15-20 word sentences reads like a press release.
- Include at least one detail that only comes from doing real research (and is true today):
  a price, a specific street, a time of day, a smell, a queue length, a specific person's name, an
  exact number. "The fountain collects roughly €3,000 a day" beats "the fountain collects a lot of
  money."
- Practical honesty beats polish: tips can warn about crowds, closures, a steep climb or a
  disappointing angle ("the famous view is from the far side of the square, not the steps"). Only
  state what research supports; when unsure about something time-sensitive (hours, prices), leave
  it out.
- Never use these AI tells: "In today's fast-paced world," "Moreover," "Furthermore," "It's important
  to note that," "Whether you're a X or a Y," "Let's dive in," "In conclusion," rhetorical questions
  used as paragraph transitions ("But what makes this place so special?"), or a closing paragraph that
  just restates the intro.
- Don't structure the whole post as a symmetrical listicle unless the topic genuinely is a list (e.g.
  a walking route with stops in order). Hidden Story posts should read as one continuous piece with
  narrative momentum, using `<h2>` headers only where the story actually turns a corner.
- No invented quotes from named real people (guides, locals, historians) unless you can source them.
  Legends and disputed folklore are fine as long as they're framed as legend/disputed (see the barber
  story in the Trevi post for the pattern: "Historians dispute it. Romans tell it anyway.").

## Keep historical/background info light (added 2026-09-02, after post #2 ran too dense)

Every fact you include should earn its place by adding color to what someone will actually see or
feel — not because it's true and citable. Concretely:

- **One or two sentences of history per stop, max.** If you catch yourself writing a paragraph of
  dates, founders, dynasties, or construction timelines, cut it down to the single most vivid detail
  and move on. The reader is on a walk, not in a lecture.
- **Pick the one fact that changes how a place feels to look at**, and skip the rest. "The cathedral
  is visibly sinking because the whole city sits on a drained lake" is worth a sentence. The lake's
  draining date, the engineers involved, and the exact subsidence rate are not — that's a Wikipedia
  paragraph wearing a blog post as a costume.
- Do not stack multiple practical details in one place — a price *and* an ID requirement *and* a wait
  time *and* opening hours, all in the same paragraph. If a logistic detail is genuinely worth
  including, it's because it would change what the reader actually does; include that one, drop the
  rest. When in doubt, cut the number and keep the feeling.

## The two content types

Alternate between these — don't publish two of the same type back to back.

**Hidden Stories** — one landmark, one surprising true story behind it (a feud, a mistake, an
origin story, a piece of trivia guides skip because there's a bus waiting). ~800-1100 words.

**City Guides** — this is a walk, not an itinerary spec sheet. Write it the way you'd tell a friend
about a morning you spent somewhere good: loose chronological movement through a few stops, one
engaging observation or small moment at each, historical color kept to the one-or-two-sentence rule
above. It should read as a story about walking somewhere, that happens to leave the reader knowing
where to go — not a checklist that happens to have some anecdotes in it.
  - **Avoid hour-by-hour timestamp headers** ("7:45–8:15am: ...") and avoid turning every stop into
    its own mini-guide with a price, a queue-length, and an ID requirement all listed out. One
    concrete, specific, memorable detail per stop beats an exhaustive one.
  - Use `<h2>`s to mark moments or places, not time blocks — "the cathedral that's sinking," not
    "8:15am: the cathedral."
  - It's fine to skip a stop's practical details entirely if they don't add anything a reader would
    act on. This is meant to feel like reading about a nice walk, not planning a logistics operation.
  - ~700-1000 words — shorter than a Hidden Story, since there's no single deep story to unfold.

Do not write "App Update" or product-announcement posts on this blog — that content doesn't belong
here (decided 2026-09-02).

## SEO checklist — every post, no exceptions

- One primary keyword phrase the post is actually targeting (e.g. "trevi fountain history," "self
  guided mexico city walking tour"). It must appear in: the `<title>`, the meta description, the H1,
  and naturally within the first ~100 words.
- 2-3 secondary/related phrases used naturally in H2s or body copy — don't force them.
- `<title>` under ~60 characters where possible, formatted `{Specific headline} | The Wander Log`.
- Meta description 140-160 characters, written to earn the click (not just summarize).
- `canonical`, `og:title`, `og:description`, `og:url`, `og:type=article` all filled in and matching.
- The `BlogPosting` JSON-LD block filled in with real `datePublished` (today's date, `YYYY-MM-DD`) and
  a `BreadcrumbList` block — copy the structure from the Trevi post exactly, just change the values.
- Internal links: at least 2. One should point to `index.html` or a relevant `{city}.html` page (if
  that city has one — check the repo root for an existing `{city-slug}.html` before assuming), one
  should point to `blog.html`. Related-city posts can link to each other once there are enough posts.
- Headings must nest properly: one `<h1>` (in the hero), then `<h2>`s in order — never skip to `<h3>`
  without an `<h2>` first.
- Slug (filename) is the primary keyword in kebab-case: `blog-{descriptive-keyword-slug}.html`. Keep
  it under ~60 characters.
- Add the new post's URL to `sitemap.xml` with today's date, `changefreq=monthly`, `priority=0.7`.

## The app mention — how to keep it organic (updated 2026-10-12)

Every post connects to the app through **one real walk** — a shared tour in the app that includes the
post's landmark — plus at most one tip. Three touchpoints, no more:

1. **Walk pointer, right under the byline** (class `walk-pointer`). One line naming the stop:
   "The Trevi Fountain is stop 2 of a free 6-stop walk through Baroque Rome. See the route ↓", linking
   to `#walk`. For a City Guide post, "This walk is in the app as a free 6-stop route. See it ↓".
2. **One mid-article "P.S." card** (class `ps-note`) written as a **tip, never as a visit**: something
   the reader can do on the spot that pays off the story ("Stand at the left edge and look for the
   tall stone vase. With Urban Tales running, the barber story plays as you reach the fountain.").
   The label reads "Tip". Place it after the most interesting revelation, not at a random break.
3. **The "Walk this route" card** (`<section class="walk" id="walk">`) at the very end of the
   article, inside `<article class="post">`. It replaces the old `app-cta` box. It holds: the walk's
   name, stop count, distance and time (from the app), the numbered stop list with a one-line true
   hook per stop and the post's own stop marked "This story", an "Open this walk in Urban Tales"
   button linking to the tour's share page, and both store badges. Copy the exact markup from
   `blog-trevi-fountain-secret-history.html`.

**The walk must be real.** Create it in the app with the official content account ("Urban Tales
Team", `tours@urbantales.net`), make it shareable, and use its share link
(`https://urbantales.net/tour.html?id=<tour id>&utm_source=blog&utm_campaign=<post slug>`). Stop names,
order, distance and time come from that tour; never invent a route. If you can't create the tour,
stop and say so in the PR instead of shipping a placeholder.

**No star ratings or review counts** anywhere on the blog until the real store ratings back them
(decided 2026-10-12). No "4.8 rating" lines.

Never add a fourth touchpoint, a popup, a sticky bar, or a banner. Three is the ceiling.

## Images (added 2026-09-02)

Real photos, not CSS gradients. `blog-images.json` at the repo root maps a city slug (matching the
`{city}.html` filename, e.g. `rome`, `mexico-city`, `paris`) to a pre-downloaded photo already
committed to the repo (`blog-img-{slug}.jpg`) plus its Pexels credit info (`photographer`,
`photographer_url`, `pexels_url`).

- **There is no live Pexels API access from this environment — do not attempt to call the Pexels
  API, and never write any API key into a file.** Only use the pre-downloaded pool in
  `blog-images.json` / `blog-img-*.jpg`.
- Look up the new post's city slug in `blog-images.json`. If it's there:
  - Use it as the post's `article-hero` background: replace `<div class="article-hero">` with
    `<div class="article-hero" style="background-image:url('blog-img-{slug}.jpg');background-size:cover;background-position:center;">`
    (see any published post for the exact pattern).
  - Use the same file for the post's card thumbnail in `blog.html`:
    `<div class="post-thumb" style="background-image:url('blog-img-{slug}.jpg');background-size:cover;background-position:center;">`
    (drop the old `thumb-*` gradient class from new cards — it's only a fallback now).
  - Add a small credit line in the post's `article-footer`, immediately before `<div class="share-row">`:
    `<p style="font-size:11.5px;color:var(--ink-faint);margin:0 0 4px;">Photo: <a href="{photographer_url}" target="_blank" rel="noopener" style="color:var(--ink-faint);">{photographer}</a> / <a href="{pexels_url}" target="_blank" rel="noopener" style="color:var(--ink-faint);">Pexels</a></p>`
- If the city slug is **not** in `blog-images.json` (a genuinely new city not yet in the pool),
  fall back to the old `thumb-*` gradient class pattern (reuse the closest-toned existing gradient
  from `blog.html`'s CSS) and note in the PR description that this post is still on a gradient
  placeholder and could use a real photo added to `blog-images.json` later.
- One photo per city is enough — if a second post later covers the same city with a different
  landmark, it's fine to reuse that city's existing photo rather than needing a new one per post.

## Building the post file — steps

1. Read `blog-topics.md`. Pick the next topic from the **Queue** section, respecting the
   Hidden Story / City Guide alternation with the most recently published post. If the queue is
   empty or everything in it has been covered elsewhere on the web extensively already, propose a
   new topic in the same spirit (specific landmark + surprising true story, or a specific practical
   self-guided route) for a city already represented in the repo's `{city}.html` pages where possible
   — that lets the CTA and internal links connect to an existing page.
2. Copy `blog-trevi-fountain-secret-history.html` as your structural template. Keep every CSS class
   name and the overall structure (`app-tie`, `nav`, `article-hero`, `byline`, `walk-pointer`, `ps-note`,
   `walk`, `article-footer`, `footer.site-footer`) identical — only change content, and apply the Images
   section above for the hero/thumbnail background and the `post-tag` label.
3. Write the post following the Voice and SEO sections above.
4. Save it as `blog-{slug}.html` in the repo root (flat, no subfolder — matches every other page here).
5. Add a new card at the **top** of `.post-grid` in `blog.html` (newest first). Demote the previous
   `featured` card to a regular card (remove the `featured` class and restructure it as a standard
   card) and make the new post the `featured` one, OR keep the grid simple with all-equal cards once
   there are more than ~4 posts — use judgment, but newest always leads.
6. Add the new post's URL to `sitemap.xml`.
7. Move the topic from **Queue** to **Published** in `blog-topics.md`, with the date and filename.

## Publishing workflow — approval is required

Do **not** push directly to `main`. Open the changes as a branch + pull request and stop there:

```
git checkout -b blog/{slug}
git add blog-{slug}.html blog.html sitemap.xml blog-topics.md
git commit -m "Add blog post: {headline}"
git push -u origin blog/{slug}
gh pr create --title "Blog: {headline}" --body "New Wander Log post — ready for review. Merge to publish (GitHub Pages deploys straight from main, no build step)."
```

The PR *is* the draft for review. Leandro reviews and merges it himself (or asks for changes) — that
merge is what makes it live. Never merge your own PR. Never push straight to `main`.
