# -*- coding: utf-8 -*-
"""
gen_thumb_vertical.py — 两条 Shorts 的竖版缩略图（1080x1920，9:16）

规范（2026-10-25 查证）：
  - Shorts 缩略图官方推荐 1080x1920 / 9:16，最大 2MB
  - 安全区：核心内容放中央（避开顶部 10% UI、底部 30% 标题频道名遮挡、右缘点赞按钮）
  - 本设计：成片实拍帧全 bleed 打底 + 中下部暗渐变 + 大字钩子居中偏下

产物（覆盖主文件名，16:9 旧版已存为 *-16x9.png）：
  assets/img/yt-thumb-shorts01.png  破防了（浓度测试）
  assets/img/yt-thumb-shorts02.png  四条全中（篮球图鉴）
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "assets", "img")
SHORTS = os.path.normpath(os.path.join(ROOT, "..", "shorts"))
CLEAN = os.path.join(SHORTS, "clips", "clean")

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_CJK_B = "C:/Windows/Fonts/msyhbd.ttc"

CORAL = (255, 92, 43)
TEXT = (244, 239, 231)
MUTED = (180, 172, 160)

W, H = 1080, 1920


def font(path, size):
    return ImageFont.truetype(path, size)


def grab_frame(clip_prefix, ss, out):
    clip = [f for f in os.listdir(CLEAN) if f.startswith(clip_prefix)][0]
    subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(ss), "-i", os.path.join(CLEAN, clip), "-frames:v", "1", "-y", out],
        check=True,
    )
    return out


def build(frame_path, kicker, main, sub, url, out_name):
    # 1. 全 bleed 底图（768x1344 -> 1080x1920）
    frame = Image.open(frame_path).convert("RGB").resize((W, H), Image.LANCZOS)
    im = frame.copy()
    # 2. 中下部暗渐变（文字可读性；顶部保留画面）
    grad = Image.new("L", (1, H))
    for y in range(H):
        if y < H * 0.42:
            a = 0
        else:
            a = int(235 * min(1.0, (y - H * 0.42) / (H * 0.30)))
        grad.putpixel((0, y), a)
    grad = grad.resize((W, H))
    im.paste(Image.new("RGB", (W, H), (8, 7, 6)), (0, 0), grad)
    d = ImageDraw.Draw(im)
    # 3. 文字栈（居中偏下，约 58%-80% 高度，避开顶部 UI 与底部标题区）
    def centered(cx, y, text, f, fill):
        w = d.textlength(text, font=f)
        d.text((cx - w / 2, y), text, font=f, fill=fill)
    # kicker
    f_kick = font(FONT_CJK_B, 46)
    kw = d.textlength(kicker, font=f_kick)
    # kicker 两侧短线
    kx = (W - kw) / 2
    d.line([(kx - 60, 1120), (kx - 18, 1120)], fill=CORAL, width=4)
    d.line([(kx + kw + 18, 1120), (kx + kw + 60, 1120)], fill=CORAL, width=4)
    centered(W / 2, 1100, kicker, f_kick, CORAL)
    # 主钩子（超大）
    f_main = font(FONT_CJK_B, 210)
    centered(W / 2, 1210, main, f_main, TEXT)
    # 副钩子
    f_sub = font(FONT_CJK_B, 68)
    centered(W / 2, 1480, sub, f_sub, CORAL)
    # 落版
    f_url = font(FONT_CJK_B, 48)
    centered(W / 2, 1600, url, f_url, MUTED)
    out = os.path.join(IMG, out_name)
    im.save(out, "PNG", optimize=True)
    print(out_name, "%.1f MB" % (os.path.getsize(out) / 1048576), "(上限 2MB)")


# Shorts 01：钩子帧（1.5s 困惑看手机）
build(
    grab_frame("Vertical_9_16_video__A_handsom", 1.5, os.path.join(SHORTS, "check", "v01_frame.png")),
    "SPORTSBOY.GAY 浓度测试",
    "破防了",
    "直男做浓度测试，第三题",
    "sportsboy.gay/quiz",
    "yt-thumb-shorts01.png",
)

# Shorts 02：篮球场帧（2s 缠护踝抬头）
build(
    grab_frame("Vertical_9_16_video__Same_athl_2026-10-25T08-08-54", 2, os.path.join(SHORTS, "check", "v02_frame.png")),
    "SPORTSBOY.GAY 体育生图鉴",
    "四条全中",
    "你是篮球体育生吗？",
    "sportsboy.gay/quiz",
    "yt-thumb-shorts02.png",
)
