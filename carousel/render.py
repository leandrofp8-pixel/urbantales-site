"""
Renders one "Only with Urban Tales" carousel batch to 9 PNGs (1080x1350, IG portrait).

Usage:
    python3 render.py path/to/batch.json

Requires a chosen photo file for each slot (cover.jpg, fact1.jpg .. fact7.jpg) to already exist
in the same directory as the batch JSON. Renders HTML to /tmp then screenshots with headless Chrome.
Output PNGs land next to the batch JSON as slide-1-cover.png .. slide-9-cta.png.

batch.json shape:
{
  "badge_num": 7,
  "city": "VIENNA",
  "flag": "🇦🇹",
  "cta_screenshot": "screen-vienna-hofburg-map.png",   // path relative to repo root, a real app screenshot
  "facts": [
    {"headline": "...", "body_html": "... <b>bold spans</b> ..."},
    ... exactly 7 of these ...
  ]
}
"""
import sys, os, json, subprocess

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SHARED_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700;1,800&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Baloo 2',sans-serif; }
  .badge {
    position:absolute; top:44px; right:44px; z-index:5;
    background:#fdf0e6; color:#c8541f; padding:16px 30px; border-radius:999px;
    font-family:'Playfair Display',serif; font-style:italic; font-weight:700; font-size:29px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
  }
</style>
"""

def render_html_to_png(html, out_png, workdir):
    html_path = os.path.join(workdir, "_tmp_slide.html")
    open(html_path, "w").write(f"<!DOCTYPE html><html><head><meta charset='utf-8'>{SHARED_HEAD}</head><body>{html}</body></html>")
    subprocess.run([
        CHROME, "--headless", "--disable-gpu",
        f"--screenshot={out_png}", "--window-size=1080,1350", "--hide-scrollbars",
        f"file://{html_path}",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(html_path)

def main():
    batch_path = sys.argv[1]
    workdir = os.path.dirname(os.path.abspath(batch_path))
    spec = json.load(open(batch_path))
    badge = spec["badge_num"]
    city = spec["city"]
    flag = spec["flag"]
    facts = spec["facts"]
    assert len(facts) == 7, "need exactly 7 facts"

    # slide 1: cover
    cover = f"""
    <div style="width:1080px;height:1350px;position:relative;">
      <img src="cover.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(8,8,8,0.5) 0%, rgba(8,8,8,0.38) 32%, rgba(8,8,8,0.55) 60%, rgba(8,8,8,0.88) 100%);"></div>
      <div class="badge">Only with Urban Tales #{badge}</div>
      <div style="position:absolute; top:330px; left:0; right:0; text-align:center; padding:0 70px;">
        <div style="font-family:'Playfair Display'; font-style:italic; font-weight:800; font-size:190px; color:#fff; line-height:0.9; text-shadow:0 6px 24px rgba(0,0,0,0.35);">7</div>
        <div style="font-family:'Playfair Display'; font-style:italic; font-weight:700; font-size:60px; color:#fff8f0; line-height:1.22; margin-top:14px; text-shadow:0 4px 18px rgba(0,0,0,0.35);">
          things you only discover when exploring with
        </div>
        <div style="display:inline-block; margin-top:34px; background:#d1531f; color:#fff8f0; font-family:'Playfair Display'; font-style:italic; font-weight:800; font-size:54px; padding:20px 52px; border-radius:22px; box-shadow:0 10px 26px rgba(0,0,0,0.3);">
          Urban Tales
        </div>
      </div>
      <div style="position:absolute; bottom:90px; left:0; right:0; text-align:center;">
        <div style="font-size:52px; line-height:1;">{flag}</div>
        <div style="font-family:'Playfair Display'; font-style:italic; font-weight:800; font-size:46px; color:#fff; letter-spacing:2px; margin-top:14px; text-shadow:0 3px 12px rgba(0,0,0,0.4);">{city.upper()}</div>
      </div>
    </div>
    """
    render_html_to_png(cover, os.path.join(workdir, "slide-1-cover.png"), workdir)
    print("rendered slide-1-cover.png")

    # slides 2-8: facts
    for i, fact in enumerate(facts, start=1):
        img = f"fact{i}.jpg"
        fact_html = f"""
        <div style="width:1080px;height:1350px;background:#fae0cf;position:relative;">
          <div class="badge">Only with Urban Tales #{badge}</div>
          <div style="position:absolute; top:120px; left:64px; right:64px; bottom:70px; display:flex; flex-direction:column;">
            <div style="width:952px; height:520px; flex-shrink:0; border-radius:26px; border:5px solid #d1531f; overflow:hidden; box-shadow:0 14px 30px rgba(0,0,0,0.12);">
              <img src="{img}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:30px; margin-top:36px;">
              <div style="font-family:'Playfair Display'; font-style:italic; font-weight:800; font-size:60px; color:#1c1a17; line-height:1.18;">
                {i}. {fact['headline']}
              </div>
              <div style="width:150px; height:6px; background:#d1531f; border-radius:3px;"></div>
              <div style="font-family:'Baloo 2'; font-weight:500; font-size:44px; color:#231f1a; line-height:1.42;">
                {fact['body_html']}
              </div>
            </div>
          </div>
        </div>
        """
        render_html_to_png(fact_html, os.path.join(workdir, f"slide-{i+1}-fact{i}.png"), workdir)
        print(f"rendered slide-{i+1}-fact{i}.png")

    # slide 9: CTA
    cta_screenshot = spec["cta_screenshot"]
    cta = f"""
    <div style="width:1080px;height:1350px;background:#111110;position:relative;overflow:hidden;">
      <div style="position:absolute; top:50%; left:18%; width:900px; height:900px; transform:translate(-50%,-50%); background:radial-gradient(circle, rgba(209,83,31,0.32) 0%, rgba(209,83,31,0) 62%); pointer-events:none;"></div>
      <div class="badge">Only with Urban Tales #{badge}</div>
      <div style="position:absolute; top:230px; left:70px; width:430px; height:900px; border-radius:52px; border:12px solid #f2ede6; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.5); z-index:2;">
        <img src="{cta_screenshot}" style="width:100%; height:100%; object-fit:cover;">
      </div>
      <div style="position:absolute; top:230px; left:560px; width:450px; height:900px; display:flex; flex-direction:column; justify-content:center; gap:40px; z-index:2;">
        <div style="font-family:'Playfair Display'; font-style:italic; font-weight:800; font-size:56px; color:#f2ede6; line-height:1.26;">
          If you want to explore the cities, not just pass by
        </div>
        <div style="display:flex; align-items:center; gap:22px;">
          <img src="icon.png" style="width:104px; height:104px; border-radius:26px; box-shadow:0 10px 24px rgba(0,0,0,0.4); flex-shrink:0;">
          <div style="font-family:'Playfair Display'; font-style:italic; font-weight:800; font-size:38px; color:#d1531f; line-height:1.22;">
            Turn cities into stories
          </div>
        </div>
        <a style="display:inline-flex; align-items:center; gap:12px; background:#d1531f; color:#fff8f0; font-family:'Baloo 2'; font-weight:700; font-size:32px; padding:22px 34px; border-radius:18px; box-shadow:0 10px 26px rgba(0,0,0,0.35); width:fit-content;">
            urbantales.net <span style="font-size:28px;">&rarr;</span>
        </a>
      </div>
      <div style="position:absolute; bottom:56px; left:0; right:0; text-align:center; z-index:2;">
        <div style="font-family:'Baloo 2'; font-weight:600; font-size:26px; color:#9a8878; letter-spacing:0.04em; text-transform:uppercase;">Link in bio</div>
      </div>
    </div>
    """
    render_html_to_png(cta, os.path.join(workdir, "slide-9-cta.png"), workdir)
    print("rendered slide-9-cta.png")

if __name__ == "__main__":
    main()
