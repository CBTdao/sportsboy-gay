"""SportsBoy.gay YouTube 频道物料生成：头像 / 横幅 / 缩略图模板

产物（800x800 头像、2560x1440 横幅含安全区、1280x720 缩略图模板）：
  assets/img/yt-avatar.png
  assets/img/yt-banner.png
  assets/img/yt-thumb-template.png
运行：python tools/youtube_kit.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "assets", "img")

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
MUTED = (167, 159, 146)

# ---------- 1. 头像 800x800（珊瑚圆角方 + S，与站点 favicon 同语言） ----------
def make_avatar():
    size = 800
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(icon)
    r = int(size * 0.22)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=CORAL + (255,))
    f = font(FONT_BLACK, int(size * 0.58))
    bb = d.textbbox((0, 0), "S", font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - tw) / 2 - bb[0], (size - th) / 2 - bb[1]), "S", font=f, fill=BG + (255,))
    icon.save(os.path.join(IMG, "yt-avatar.png"), "PNG", optimize=True)
    print("yt-avatar.png", os.path.getsize(os.path.join(IMG, "yt-avatar.png")) // 1024, "KB")

# ---------- 2. 横幅 2560x1440（安全区 1546x423 居中，文字只放安全区） ----------
def make_banner():
    W, H = 2560, 1440
    base = Image.open(os.path.join(IMG, "hero-src.jpg")).convert("RGB")
    # 全幅铺底 + 右侧提亮
    bw, bh = base.size
    scale = max(W / bw, H / bh)
    base = base.resize((int(bw * scale) + 1, int(bh * scale) + 1), Image.LANCZOS)
    x = (base.size[0] - W) // 2
    y = (base.size[1] - H) // 2
    base = base.crop((x, y, x + W, y + H))
    # 左到右深色渐变（保证安全区文字可读）
    grad = Image.new("L", (W, 1))
    for i in range(W):
        t = i / W
        # 左侧 62% 几乎不透，右侧透出画面
        a = int(246 - 150 * max(0.0, (t - 0.30) / 0.7))
        grad.putpixel((i, 0), max(60, a))
    grad = grad.resize((W, H))
    overlay = Image.new("RGBA", (W, H), BG + (0,))
    overlay.putalpha(grad)
    base = Image.alpha_composite(base.convert("RGBA"), overlay)

    d = ImageDraw.Draw(base)
    # 安全区中心 x∈[507,2053]，y∈[508,931]；文字组放在安全区偏左
    f_word = font(FONT_BLACK, 210)
    f_tld = font(FONT_BLACK, 210)
    f_cn = font(FONT_CJK_B, 64)
    f_small = font(FONT_CJK, 40)
    tx = 560
    d.text((tx, 560), "SPORTSBOY", font=f_word, fill=TEXT)
    w_word = d.textlength("SPORTSBOY", font=f_word)
    d.text((tx + w_word + 10, 560), ".gay", font=f_tld, fill=CORAL)
    d.text((tx, 830), "汗水、肌肉与骄傲，光明正大。", font=f_cn, fill=TEXT)
    d.text((tx + 4, 930), "全球体育生文化总部 · 每周三更新", font=f_small, fill=MUTED)
    # 顶部珊瑚条 + 底部细条，圈出品牌区
    bar = Image.new("RGBA", (W, 14), CORAL + (255,))
    base.alpha_composite(bar, (0, 0))
    base.alpha_composite(bar, (0, H - 14))
    base.convert("RGB").save(os.path.join(IMG, "yt-banner.png"), "PNG", optimize=True)
    print("yt-banner.png", os.path.getsize(os.path.join(IMG, "yt-banner.png")) // 1024, "KB")

# ---------- 3. 缩略图模板 1280x720（左文右图 + 底部珊瑚条） ----------
def make_thumb_template():
    W, H = 1280, 720
    tpl = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(tpl)
    # 右侧 art 区（teaser 图）
    art = Image.open(os.path.join(IMG, "teaser-src.jpg")).convert("RGB")
    aw = 470
    ah = H
    ascale = max(aw / art.size[0], ah / art.size[1])
    art = art.resize((int(art.size[0] * ascale) + 1, int(art.size[1] * ascale) + 1), Image.LANCZOS)
    ax = (art.size[0] - aw) // 2
    art = art.crop((ax, 0, ax + aw, ah))
    tpl.paste(art, (W - aw, 0))
    # 左缘渐变过渡，避免硬边
    fade = Image.new("L", (120, 1))
    for i in range(120):
        fade.putpixel((i, 0), int(255 * (1 - i / 120)))
    fade = fade.resize((120, H))
    tpl.paste(Image.new("RGB", (120, H), BG), (W - aw, 0), fade)
    # 文字区（左侧 810px）：主标题 + 副题 + 品牌条（中文用黑体，Arial Black 无中文字形）
    f_main = font(FONT_CJK_B, 128)
    f_sub = font(FONT_CJK_B, 52)
    f_tag = font(FONT_CJK_B, 34)
    d.text((60, 150), "主标题", font=f_main, fill=TEXT)
    d.text((64, 320), "3-6 字钩子，一句话", font=f_sub, fill=CORAL)
    d.text((64, 430), "副标题补一刀", font=f_tag, fill=MUTED)
    # 底部珊瑚条 + 品牌字
    d.rectangle([0, H - 84, W, H], fill=CORAL)
    d.text((60, H - 66), "SPORTSBOY", font=font(FONT_BLACK, 46), fill=BG + (255,))
    f_brand = font(FONT_BLACK, 46)
    wb = d.textlength("SPORTSBOY", font=f_brand)
    d.text((60 + wb + 8, H - 66), ".gay", font=f_brand, fill=BG + (255,))
    tpl.save(os.path.join(IMG, "yt-thumb-template.png"), "PNG", optimize=True)
    print("yt-thumb-template.png", os.path.getsize(os.path.join(IMG, "yt-thumb-template.png")) // 1024, "KB")

make_avatar()
make_banner()
make_thumb_template()
print("ALL DONE")
