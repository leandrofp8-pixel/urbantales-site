"""Render the localized Google Play feature graphic (1024 x 500) for Urban Tales.

Same campaign as the Apple creative assets: generated landscape photography,
real Urban Tales app capture on the phone, Avenir Next typography.
Drawn at 2x and downscaled. Output: output/localized/play-feature-graphic/
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from render_creative_assets import (
    ASSETS, ORANGE, ROOT, WHITE, brand, composite_shadow, cover, fit_font, font,
    horizontal_shade, phone_layer, vertical_shade,
)

SIZE = (2048, 1000)
OUTPUT = ROOT / "output" / "localized" / "play-feature-graphic"

# Play locale -> copy. Headline matches screenshot 1 of the store set.
COPY = {
    "en-US": ("The city has stories.\nStart walking.", "Your personal audio guide, anywhere."),
    "es-419": ("La ciudad tiene historias.\nEmpieza a caminar.", "Tu audioguía personal, estés donde estés."),
    "es-ES": ("La ciudad tiene historias.\nEmpieza a caminar.", "Tu audioguía personal, estés donde estés."),
    "pt-BR": ("A cidade tem histórias.\nComece a caminhar.", "Seu guia de áudio pessoal, em qualquer lugar."),
    "fr-FR": ("La ville a des histoires.\nCommencez à marcher.", "Votre audioguide personnel, partout."),
    "de-DE": ("Jede Stadt hat Geschichten.\nGeh einfach los.", "Dein persönlicher Audioguide, überall."),
}


def render(headline: str, sub: str) -> Image.Image:
    image = cover(ASSETS / "product-header-base.png", SIZE, focal=(0.5, 0.5))
    horizontal_shade(image, strength=225, end=0.72)
    vertical_shade(image, strength=70, end=0.5)
    brand(image, (110, 110), 84, 38)
    draw = ImageDraw.Draw(image)
    head_font = fit_font(draw, headline, 104, 72, 1180)
    draw.multiline_text((110, 280), headline, font=head_font, fill=WHITE, spacing=6, anchor="la")
    box = draw.multiline_textbbox((110, 280), headline, font=head_font, spacing=6)
    sub_font = fit_font(draw, sub, 46, 34, 1180, weight="medium")
    draw.text((110, box[3] + 44), sub, font=sub_font, fill="#EEE5DB", anchor="la")
    draw.rounded_rectangle((110, box[3] + 128, 330, box[3] + 140), radius=6, fill=ORANGE)
    # Phone bleeds off the bottom edge, map visible above the fold.
    composite_shadow(image, phone_layer(500, angle=-4.0), (1380, 120))
    return image.convert("RGB").resize((1024, 500), Image.Resampling.LANCZOS)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1024 * 2, 500 * 3), "white")
    for i, (locale, (headline, sub)) in enumerate(COPY.items()):
        img = render(headline, sub)
        img.save(OUTPUT / f"feature-graphic-{locale}.png")
        sheet.paste(img, ((i % 2) * 1024, (i // 2) * 500))
        print("rendered", locale)
    sheet.save(OUTPUT / "preview.jpg", quality=85)


if __name__ == "__main__":
    main()
