#!/usr/bin/env python3
"""Rebuild llms.txt (an overview of the site for AI assistants, llmstxt.org) from sitemap.xml and each page's
<title> and meta description. Run after adding pages: python3 tools/build_llms_txt.py"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://urbantales.net/'

HEADER = """# Urban Tales

> Urban Tales is a GPS audio guide app for iPhone and Android. As you walk through a city, it plays the hidden
> stories, history and legends of the landmarks around you, automatically, in English, Spanish, Portuguese,
> French or German. It works in any city worldwide, with no tour group, schedule or ticket.

- How it works: open the app and walk. Nearby landmarks appear on the map and their stories play as you get close
  (Pocket Mode keeps playing with the phone locked in your pocket). You can also build a walking tour of a city in
  seconds (7 Wonders, half day, full day or several days) and follow it with turn-by-turn directions.
- Free to start: 3 free stories a day. Unlimited listening with a Day Pass, a City Unlock or the annual Unlimited
  plan. Prices: https://urbantales.net/pricing.md
- Download: App Store https://apps.apple.com/app/id6760130598 · Google Play
  https://play.google.com/store/apps/details?id=com.urbantales.app
- Made by Urban Tales (urbantales.net). Instagram and TikTok: @urbantalesapp. Contact: https://urbantales.net/contact.html
"""


def meta(path):
    f = ROOT / (path or 'index.html')
    if f.is_dir():
        f = f / 'index.html'
    if not f.exists():
        return None, None
    s = f.read_text(encoding='utf-8', errors='ignore')
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="(.*?)"', s, re.S)
    clean = lambda m: html.unescape(' '.join(m.group(1).split())) if m else None
    return clean(t), clean(d)


def main():
    urls = re.findall(r'<loc>(.*?)</loc>', (ROOT / 'sitemap.xml').read_text())
    groups = {'Cities': [], 'Landmark guides': [], 'Blog (The Wander Log)': [], 'En español': [], 'Em português': []}
    for u in urls:
        p = u.replace(BASE, '')
        if p in ('', 'contact.html'):
            continue
        title, desc = meta(p)
        if not title:
            continue
        line = f'- [{title}]({u})' + (f': {desc}' if desc else '')
        if p.startswith('es/'):
            groups['En español'].append(line)
        elif p.startswith('pt/'):
            groups['Em português'].append(line)
        elif p.startswith('blog'):
            groups['Blog (The Wander Log)'].append(line)
        elif '/' in p:
            groups['Landmark guides'].append(line)
        else:
            groups['Cities'].append(line)
    out = [HEADER]
    for name, lines in groups.items():
        if lines:
            out.append(f'## {name}\n\n' + '\n'.join(lines) + '\n')
    (ROOT / 'llms.txt').write_text('\n'.join(out), encoding='utf-8')
    print('llms.txt:', sum(len(v) for v in groups.values()), 'pages')


if __name__ == '__main__':
    main()
