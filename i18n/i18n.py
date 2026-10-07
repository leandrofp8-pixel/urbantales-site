#!/usr/bin/env python3
"""Static-site localization for urbantales.net.

English pages at the repo root are the source of truth. Each translated page
has a dictionary at i18n/<lang>/<page>.json mapping every English text
fragment to its translation.

  python3 i18n/i18n.py extract es rome.html   # create/refresh the dictionary
  python3 i18n/i18n.py build es               # write es/*.html for every dictionary
  python3 i18n/i18n.py status es              # show untranslated counts

`build` also adds hreflang alternates and a language switcher to the English
originals and refreshes sitemap.xml. Re-run `extract` after editing an English
page: new fragments appear with an empty translation, existing ones are kept.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://urbantales.net"
LANGS = {
    "es": {"name": "Español", "switch_title": "Leer en español", "play_hl": "es"},
}
EN_SWITCH = {"name": "English", "switch_title": "Read in English"}

SEG = re.compile(
    r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>)",
    re.S | re.I,
)
TEXT_ATTRS = re.compile(r'(\s(?:alt|title|aria-label|placeholder)=")([^"]*)(")', re.I)
META_CONTENT = re.compile(r'(\scontent=")([^"]*)(")', re.I)
META_TRANSLATABLE = re.compile(
    r'(name|property)="(description|keywords|og:title|og:description|twitter:title|twitter:description)"',
    re.I,
)
LD_STRINGS = re.compile(r'("(?:name|text|description)"\s*:\s*")((?:[^"\\]|\\.)*)(")')
URL_ATTRS = re.compile(r'(\s(?:href|src|content)=")([^"]*)(")', re.I)
LD_URLS = re.compile(r'"(https://urbantales\.net/[^"]*)"')


def has_words(s):
    return re.search(r"[A-Za-z]", s) is not None


def walk(html, on_text):
    """Call on_text(fragment) for every translatable fragment; return rewritten html."""
    parts = SEG.split(html)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            m = re.match(r"(\s*)(.*?)(\s*)$", part, re.S)
            lead, core, trail = m.groups()
            core_n = re.sub(r"\s+", " ", core)
            out.append(lead + on_text(core_n) + trail if has_words(core_n) else part)
            continue
        low = part[:40].lower()
        if low.startswith("<script") and "ld+json" in part[: part.find(">")]:
            part = LD_STRINGS.sub(
                lambda m: m.group(1) + on_text(m.group(2)) + m.group(3) if has_words(m.group(2)) else m.group(0),
                part,
            )
        elif low.startswith(("<script", "<style", "<!--", "</")):
            pass
        else:
            part = TEXT_ATTRS.sub(
                lambda m: m.group(1) + on_text(m.group(2)) + m.group(3) if has_words(m.group(2)) else m.group(0),
                part,
            )
            if low.startswith("<meta") and META_TRANSLATABLE.search(part):
                part = META_CONTENT.sub(lambda m: m.group(1) + on_text(m.group(2)) + m.group(3), part)
        out.append(part)
    return "".join(out)


def dict_path(lang, page):
    return ROOT / "i18n" / lang / (page[:-5] + ".json")


def load_dict(lang, page):
    p = dict_path(lang, page)
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def extract(lang, pages):
    for page in pages:
        html = strip_i18n((ROOT / page).read_text("utf-8"))
        seen = []
        walk(html, lambda s: (seen.append(s), s)[1])
        old = load_dict(lang, page)
        new = {s: old.get(s, "") for s in dict.fromkeys(seen)}
        stale = [s for s in old if s not in new]
        p = dict_path(lang, page)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n", "utf-8")
        missing = sum(1 for v in new.values() if not v)
        print(f"{page}: {len(new)} fragments, {missing} untranslated" + (f", {len(stale)} stale dropped" if stale else ""))


def translated_pages(lang):
    return sorted(p.stem + ".html" for p in (ROOT / "i18n" / lang).glob("*.json"))


def canonical(html):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    return m.group(1)


def localize_url(url, lang, pages):
    """Map an English URL to its translated equivalent when one exists."""
    m = re.match(r"https://urbantales\.net/([^#?]*)(.*)$", url)
    if m:
        path, rest = m.groups()
        page = path or "index.html"
        if page in pages:
            return f"{SITE}/{lang}/" + ("" if page == "index.html" else page) + rest
        return url
    if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|#|/)", url) or not url:
        return url
    page, _, rest = url.partition("#")
    rest = "#" + rest if _ else ""
    if page in pages:
        return f"/{lang}/" + ("" if page == "index.html" else page) + rest
    return "/" + url  # shared asset or untranslated page at the site root


def alternates_block(en_url, urls):
    lines = ["  <!-- i18n:alternates -->", f'  <link rel="alternate" hreflang="en" href="{en_url}" />']
    lines += [f'  <link rel="alternate" hreflang="{l}" href="{u}" />' for l, u in urls.items()]
    lines += [f'  <link rel="alternate" hreflang="x-default" href="{en_url}" />', "  <!-- /i18n:alternates -->"]
    return "\n".join(lines) + "\n"


def set_alternates(html, block):
    return html.replace("</head>", block + "</head>", 1)


SWITCH_RE = re.compile(r'\n    <a [^>]*data-i18n="switch"[^>]*>[^<]*</a>')
NAV_WRAP = '<div data-i18n="nav" style="display:flex;align-items:center;gap:28px">'


def strip_i18n(html):
    """Remove what build() injects, so the English source text is never re-extracted from it."""
    html = re.sub(r"  <!-- i18n:alternates -->.*?<!-- /i18n:alternates -->\n", "", html, flags=re.S)
    return SWITCH_RE.sub("", html)


def set_switch(html, href, label, hreflang, title):
    a = (
        f'\n    <a href="{href}" class="lang-switch" data-i18n="switch" hreflang="{hreflang}" lang="{hreflang}" '
        f'title="{title}" style="border:1px solid rgba(255,255,255,0.25);border-radius:999px;'
        f'padding:5px 12px;font-size:12px;letter-spacing:0.04em">{label}</a>'
    )
    html = SWITCH_RE.sub("", html)
    if NAV_WRAP in html:
        i = html.index("</ul>", html.index(NAV_WRAP)) + len("</ul>")
        return html[:i] + a + html[i:]
    # Wrap the top nav's link list so the switcher stays visible when the list
    # is hidden on narrow screens.
    m = re.search(r"(<nav>.*?)(<ul>.*?</ul>)(\s*</nav>)", html, re.S)
    if not m:
        raise SystemExit("top <nav><ul> not found")
    return html[: m.start(2)] + NAV_WRAP + m.group(2) + a + "</div>" + html[m.end(2) :]


def build(lang):
    cfg = LANGS[lang]
    pages = translated_pages(lang)
    problems = []
    for page in pages:
        original = (ROOT / page).read_text("utf-8")
        src = strip_i18n(original)
        tr = load_dict(lang, page)
        missing = []

        def on_text(s):
            t = tr.get(s)
            if not t:
                missing.append(s)
                return s
            return t

        out = walk(src, on_text)
        if missing:
            problems.append(f"{page}: {len(missing)} untranslated, e.g. {missing[0]!r}")
            continue
        out = out.replace('<html lang="en">', f'<html lang="{lang}">', 1)
        out = URL_ATTRS.sub(lambda m: m.group(1) + localize_url(m.group(2), lang, pages) + m.group(3), out)
        out = LD_URLS.sub(lambda m: '"' + localize_url(m.group(1), lang, pages) + '"', out)
        out = out.replace(
            "play.google.com/store/apps/details?id=com.urbantales.app\"",
            f"play.google.com/store/apps/details?id=com.urbantales.app&amp;hl={cfg['play_hl']}\"",
        )
        en_url = canonical(src)
        loc_url = localize_url(en_url, lang, pages)
        block = alternates_block(en_url, {lang: loc_url})
        out = set_switch(set_alternates(out, block), en_url, "EN", "en", EN_SWITCH["switch_title"])
        (ROOT / lang).mkdir(exist_ok=True)
        (ROOT / lang / page).write_text(out, "utf-8")

        en = set_switch(set_alternates(src, block), loc_url, lang.upper(), lang, cfg["switch_title"])
        if en != original:
            (ROOT / page).write_text(en, "utf-8")
        print(f"built {lang}/{page}")
    update_sitemap(lang, [p for p in pages if not any(x.startswith(p + ":") for x in problems)])
    if problems:
        print("\nNOT BUILT:\n  " + "\n  ".join(problems))
        sys.exit(1)


def update_sitemap(lang, pages):
    path = ROOT / "sitemap.xml"
    xml = path.read_text("utf-8")
    xml = re.sub(rf"  <url><loc>{SITE}/{lang}/[^<]*</loc>.*?</url>\n", "", xml)
    today = date.today().isoformat()
    rows = []
    for page in pages:
        loc = f"{SITE}/{lang}/" + ("" if page == "index.html" else page)
        prio = "1.0" if page == "index.html" else "0.8"
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n")
    path.write_text(xml.replace("</urlset>", "".join(rows) + "</urlset>"), "utf-8")


def status(lang):
    for page in translated_pages(lang):
        d = load_dict(lang, page)
        print(f"{page}: {sum(1 for v in d.values() if not v)}/{len(d)} untranslated")


if __name__ == "__main__":
    cmd, lang, *rest = sys.argv[1:]
    if lang not in LANGS:
        raise SystemExit(f"unknown language {lang}; add it to LANGS")
    {"extract": lambda: extract(lang, rest), "build": lambda: build(lang), "status": lambda: status(lang)}[cmd]()
