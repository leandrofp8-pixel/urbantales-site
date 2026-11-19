# "Only with Urban Tales" carousel — content calendar

Tracks which cities have already run in the "Only with Urban Tales #N" IG/TikTok carousel series,
so the next batch never repeats a city. See `carousel/GUIDELINES.md` for the full production process.

## Published

| # | City |
|---|---|
| 1 | Mexico City |
| 2 | Tokyo |
| 3 | Rome |
| 4 | New York |
| 5 | Istanbul |
| 6 | Florence |
| 7 | Paris |
| 8 | Amsterdam |
| 9 | Barcelona |
| 10 | Vienna |
| 11 | Berlin |
| 12 | London |
| 13 | Prague |
| 14 | Marrakech |
| 16 | Bangkok |
| 17 | Venice |
| 18 | Buenos Aires |
| 19 | Lisbon |
| 20 | Chicago |
| 21 | Rio de Janeiro |
| 23 | Kyoto |
| 24 | Budapest |
| 25 | Budapest |
| 26 | Athens |
| 27 | Athens |
| 28 | Seville |
| 29 | Seville |
| 31 | Cairo |
| 33 | Dubai |
| 35 | Edinburgh |
| 37 | Madrid |
| 38 | Seoul |
| 39 | Seoul |
| 40 | Sydney |
| 41 | Sydney |
| 43 | Singapore |
| 45 | Hong Kong |

## Next batch

**#46 — city TBD.** Pick a city not in the Published list above. Prefer one that also has a
`{city}.html` page in the main site repo where possible (bonus, not required — this series is
independent of the blog).

Note (2026-11-18, Hong Kong batch): same renumbering thing happened again — drafted as #44 (no
hong-kong.html page, no screen-hongkong-* screenshot — generic app screen used, flagged in
draft.json; photo sourcing blocked for the same recurring commons.wikimedia.org network-policy
reason as batches #8-#13, #28/#29, #30, #34, #36, #38 and #40/#41/#42/#43, though all 7 facts were
still verified via web search). The finisher then sourced Commons photos, rendered both EN/ES
sets, and bumped the badge to **#45** without removing the draft's #44 Published row (and also
corrected several facts after further verification — see the PR for details). Removed the stale
duplicate #44 row above. #44 is now an unused gap, same as #22, #30, #32, #34, #36 and #42.

Note (2026-11-18): same thing happened with Singapore — drafted as #42, the finisher sourced
Commons photos, rendered both EN/ES sets and bumped it to **#43** (`batch.json`'s `badge_num`),
adding its own Published row without removing the draft's #42 row. Removed the stale duplicate
#42 row above. #42 is now an unused gap, same as #22, #30, #32, #34 and #36.

Note (2026-11-16): Singapore (#42) has no `singapore.html` page in the main site repo and no
`screen-singapore-*-map.png` screenshot — the generic app screen was used for its CTA slide per
GUIDELINES.md. Photo candidates could not be sourced this run — commons.wikimedia.org is denied
by this cloud session's network policy (see `photo_sourcing_note` in `carousel/drafts/singapore/draft.json`),
the same recurring block as batches #8-#13, #28/#29, #30, #34, #36, #38 and #40/#41. This run also
tried requesting commons.wikimedia.org/upload.wikimedia.org be added to the environment's allowed
hosts via `update_environment`, but that needs a live person's approval and this is an unattended
scheduled run, so it was auto-refused — a future run with a person present (or Leandro himself) can
approve it, or just source the photos by hand as happened for Seoul and Sydney.

Note (2026-11-11): Sydney (#40) has no `sydney.html` page in the main site repo and no
`screen-sydney-*-map.png` screenshot — the generic app screen was used for its CTA slide per
GUIDELINES.md. Photo candidates could not be sourced this run — commons.wikimedia.org is denied
by this cloud session's network policy (see `photo_sourcing_note` in `carousel/drafts/sydney/draft.json`),
the same recurring block as batches #8-#13, #28/#29, #30, #34, #36 and #38. This run also tried
requesting a dedicated environment with Commons access via `create_environment`, but that needs a
live person's approval and this is an unattended scheduled run, so it was auto-refused — a future
run with a person present (or Leandro himself) can approve it, or just source the photos by hand
as happened for Seoul.

Note (2026-11-09): Seoul (#38) has no `seoul.html` page in the main site repo and no
`screen-seoul-*-map.png` screenshot — the generic app screen was used for its CTA slide per
GUIDELINES.md. Photo candidates could not be sourced this run — commons.wikimedia.org is denied
by this cloud session's network policy (see `photo_sourcing_note` in `carousel/drafts/seoul/draft.json`),
the same recurring block as batches #8-#13, #28/#29, #30, #34 and #36.

Note (2026-11-02): same thing happened with Madrid — drafted as #36, the finisher bumped it to
**#37** (`batch.json`'s `badge_num`) and added its own Published row without removing the draft's
#36 row. Removed the stale duplicate #36 row above. #36 is now an unused gap, same as #22, #30,
#32 and #34.

Note (2026-10-28): same thing happened with Edinburgh — drafted as #34, the finisher bumped it to
**#35** (`batch.json`'s `badge_num`) and added its own Published row without removing the draft's
#34 row. Removed the stale duplicate #34 row above. #34 is now an unused gap, same as #22, #30 and
#32.

Note (2026-10-14): Kyoto was drafted as #22; the finisher that sourced photos and rendered it
bumped the badge to **#23** instead (reason not stated in its PR comment — no other PR claimed
#22). Removed the stale duplicate #22 row this left in the table above. #22 is now an unused gap
in the numbering; no action needed unless it's worth consolidating later.

Note (2026-10-26): same thing happened with Dubai — drafted as #32, the finisher bumped it to
**#33** (`batch.json`'s `badge_num`) and added its own Published row without removing the draft's
#32 row. Removed the stale duplicate #32 row above. #32 is now an unused gap, same as #22 and #30.

Note (2026-10-23): same thing happened with Cairo — drafted as #30, the finisher bumped it to
**#31** (`batch.json`'s `badge_num`) and added its own Published row without removing the draft's
#30 row. Removed the stale duplicate #30 row above. #30 is now an unused gap, same as #22.
