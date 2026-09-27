# Website rendering repairs — 2026-09-24

User-supplied affiliate profiles, agency details, traveler names, referral names and account/event data are escaped before insertion into the affected dashboard and portal HTML. Button arguments are serialized as JavaScript values and then encoded for their HTML attribute, preserving apostrophes and quotes without treating names as code. The invitation page inserts the referral code through textContent inside the trusted localized markup.

Run `node tests/rendering-security.cjs` for executable rendering regressions. The tests cover malicious profile names, button argument round trips, promo editing, agency details, vouchers and invitation codes. Changed inline scripts were also parsed for syntax errors. These are renderer tests, not a complete authenticated browser or production audit.

This branch is the site portion of the first security repair batch. It requires no backend API change and is ready for review independently. Deploy through the normal reviewed GitHub Pages process.
