"""Render original Tera raster assets using the backend's existing Pillow dependency."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "front" / "public"
BACKGROUND = "#171717"
ACCENT = "#FF6B35"


def icon(size: int) -> Image.Image:
    image = Image.new("RGB", (size, size), BACKGROUND)
    draw = ImageDraw.Draw(image)
    points = [(14, 16), (50, 16), (50, 26), (37, 26), (37, 50), (27, 50), (27, 26), (14, 26)]
    draw.polygon([(x * size / 64, y * size / 64) for x, y in points], fill=ACCENT)
    return image


def main() -> None:
    mark = icon(256)
    mark.resize((180, 180), Image.Resampling.LANCZOS).save(PUBLIC / "favicon.png")
    mark.save(PUBLIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    share = Image.new("RGB", (1200, 630), BACKGROUND)
    share.paste(icon(192), (80, 80))
    draw = ImageDraw.Draw(share)
    draw.text((90, 300), "Tera", font=ImageFont.load_default(size=100), fill="white")
    draw.text((90, 445), "Open-source restaurant platform", font=ImageFont.load_default(size=36), fill="#D4D4D4")
    draw.text((90, 505), "Menus - Orders - Tables - Reservations", font=ImageFont.load_default(size=28), fill="#D4D4D4")
    share.save(PUBLIC / "og-image.png")

    assert mark.getpixel((128, 128)) == (255, 107, 53)
    assert mark.getpixel((0, 0)) == (23, 23, 23)
    for name, size in [("favicon.png", (180, 180)), ("favicon.ico", (64, 64)), ("og-image.png", (1200, 630))]:
        with Image.open(PUBLIC / name) as saved:
            assert saved.size == size, (name, saved.size)
            saved.verify()
    print("Tera PNG/ICO assets generated and verified")


if __name__ == "__main__":
    main()
