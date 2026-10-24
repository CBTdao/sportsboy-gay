"""SportsBoy.gay 图片优化：母版 -> WebP/JPG 衍生 + OG 分享图 + 图标

母版（去水印后的原图，勿删）：
  assets/img/hero-src.jpg   1536x1024  Hero 主视觉
  assets/img/teaser-src.jpg 904x904    角色预告图（q95）
运行：python tools/optimize_images.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_CJK_B = "C:/Windows/Fonts/msyhbd.ttc"
FONT_CJK = "C:/Windows/Fonts/msyh.ttc"

CORAL = (255, 92, 43)
BG = (14, 13, 11)
TEXT = (244, 239, 231)

def cover_crop(img, tw, th):
    w, h = img.size
    scale = max(tw / w, th / h)
    img = img.resize((int(w * scale) + 1, int(h * scale) + 1), Image.LANCZOS)
    x = (img.size[0] - tw) // 2
    y = (img.size[1] - th) // 2
    return img.crop((x, y, x + tw, y + th))

def report(name, path):
    kb = os.path.getsize(path) / 1024
    print(f"{name}: {kb:.0f} KB -> {os.path.basename(path)}")

# ---------- 1. hero-src.jpg -> webp + jpg ----------
hero = cover_crop(Image.open(os.path.join(IMG, "hero-src.jpg")).convert("RGB"), 1536, 1024)
hero.save(os.path.join(IMG, "hero.webp"), "WEBP", quality=80, method=6)
hero.save(os.path.join(IMG, "hero.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
report("hero", os.path.join(IMG, "hero.webp"))
report("hero", os.path.join(IMG, "hero.jpg"))

# ---------- 2. teaser-src.jpg -> webp + jpg ----------
teaser = cover_crop(Image.open(os.path.join(IMG, "teaser-src.jpg")).convert("RGB"), 900, 900)
teaser.save(os.path.join(IMG, "teaser.webp"), "WEBP", quality=80, method=6)
teaser.save(os.path.join(IMG, "teaser.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
report("teaser", os.path.join(IMG, "teaser.webp"))
report("teaser", os.path.join(IMG, "teaser.jpg"))

# ---------- 3. OG 分享图 1200x630（母版无水印，直接出 jpg） ----------
og = cover_crop(Image.open(os.path.join(IMG, "hero-src.jpg")).convert("RGB"), 1200, 630)
overlay = Image.new("RGBA", og.size, BG + (150,))
og = Image.alpha_composite(og.convert("RGBA"), overlay)
d = ImageDraw.Draw(og)
f_brand = font(FONT_BLACK, 118)
f_cn = font(FONT_CJK_B, 46)
f_en = font(FONT_CJK, 30)
f_small = font(FONT_CJK_B, 26)
x = 72
d.text((x, 150), "SPORTSBOY", font=f_brand, fill=TEXT)
w_brand = d.textlength("SPORTSBOY", font=f_brand)
d.text((x + w_brand + 8, 150), ".gay", font=f_brand, fill=CORAL)
d.text((x, 300), "汗水、肌肉与骄傲，光明正大。", font=f_cn, fill=TEXT)
d.text((x, 372), "Sweat. Muscle. Pride.", font=f_en, fill=(255, 150, 110))
d.text((x, 520), "sportsboy.gay", font=f_small, fill=(167, 159, 146))
bar = Image.new("RGBA", (1200, 6), CORAL + (255,))
og.alpha_composite(bar, (0, 0))
og.convert("RGB").save(os.path.join(IMG, "og.jpg"), "JPEG", quality=85, optimize=True, progressive=True)
report("og", os.path.join(IMG, "og.jpg"))

# ---------- 4. 图标 512 + apple 180 ----------
def make_icon(size, path):
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(icon)
    r = int(size * 0.22)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=CORAL + (255,))
    f = font(FONT_BLACK, int(size * 0.56))
    bb = d.textbbox((0, 0), "S", font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - tw) / 2 - bb[0], (size - th) / 2 - bb[1]), "S", font=f, fill=BG + (255,))
    icon.save(path, "PNG", optimize=True)
    report(f"icon{size}", path)

make_icon(512, os.path.join(IMG, "icon-512.png"))
make_icon(180, os.path.join(IMG, "apple-touch-icon.png"))

# ---------- 5. 清理旧的 og.png（og.jpg 已替代） ----------
for f in ["og.png"]:
    p = os.path.join(IMG, f)
    if os.path.exists(p):
        os.remove(p)
        print(f"removed {f} (og.jpg 已替代)")

print("ALL DONE")
