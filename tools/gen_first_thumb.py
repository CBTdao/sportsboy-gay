# -*- coding: utf-8 -*-
"""
gen_first_thumb.py — 第一条 Shorts 的实拍缩略图（基于 yt-thumb-template 同布局换真钩子）

产物：assets/img/yt-thumb-shorts01.png（1280x720）
用法：改下面 MAIN/SUB/TAG 三个变量即可复用同一版式。
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "assets", "img")

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_CJK_B = "C:/Windows/Fonts/msyhbd.ttc"

CORAL = (255, 92, 43)
BG = (14, 13, 11)
TEXT = (244, 239, 231)
MUTED = (167, 159, 146)

# ---- 本条视频的钩子三件套 ----
MAIN = "破防了"                 # 主标题（大字，3-6 字）
SUB = "直男做浓度测试，第三题"   # 钩子补充（珊瑚色）
TAG = "sportsboy.gay/quiz"     # 落版（ muted 小字）

W, H = 1280, 720
tpl = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(tpl)

# 右侧 art 区（teaser 图）
art = Image.open(os.path.join(IMG, "teaser-src.jpg")).convert("RGB")
aw = 470
ascale = max(aw / art.size[0], H / art.size[1])
art = art.resize((int(art.size[0] * ascale) + 1, int(art.size[1] * ascale) + 1), Image.LANCZOS)
ax = (art.size[0] - aw) // 2
art = art.crop((ax, 0, ax + aw, H))
tpl.paste(art, (W - aw, 0))

# 左缘渐变过渡
fade = Image.new("L", (120, 1))
for i in range(120):
    fade.putpixel((i, 0), int(255 * (1 - i / 120)))
fade = fade.resize((120, H))
tpl.paste(Image.new("RGB", (120, H), BG), (W - aw, 0), fade)

# 文字区
f_main = font(FONT_CJK_B, 148)
f_sub = font(FONT_CJK_B, 52)
f_tag = font(FONT_CJK_B, 34)
d.text((56, 130), MAIN, font=f_main, fill=TEXT)
d.text((60, 330), SUB, font=f_sub, fill=CORAL)
d.text((60, 430), TAG, font=f_tag, fill=MUTED)

# 底部珊瑚条 + 品牌字
d.rectangle([0, H - 84, W, H], fill=CORAL)
f_brand = font(FONT_BLACK, 46)
d.text((60, H - 66), "SPORTSBOY", font=f_brand, fill=BG)
wb = d.textlength("SPORTSBOY", font=f_brand)
d.text((60 + wb + 8, H - 66), ".gay", font=f_brand, fill=BG)

out = os.path.join(IMG, "yt-thumb-shorts01.png")
tpl.save(out, "PNG", optimize=True)
print("saved:", os.path.relpath(out, ROOT), os.path.getsize(out) // 1024, "KB")
