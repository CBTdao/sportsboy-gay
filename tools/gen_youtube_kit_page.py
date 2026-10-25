# -*- coding: utf-8 -*-
"""
gen_youtube_kit_page.py — 生成自包含的 YouTube 频道资料包 HTML（单文件，图片 base64 内嵌）

产物：../../youtube-kit.html（工作区根目录，内部资料，不进官网仓库部署路径）
运行：python tools/gen_youtube_kit_page.py
"""
import base64
import json
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "assets", "img")
OUT = os.path.normpath(os.path.join(ROOT, "..", "youtube-kit.html"))

# ---------- 可复制字段（页面显示与剪贴板同源，零漂移） ----------
FIELDS = [
    ("频道名", "channel_name", "SportsBoy.gay"),
    ("用户号 Handle", "handle", "@sportsboygay（被占用就试 @sportsboy-gay）"),
    ("频道口号", "tagline", "汗水、肌肉与骄傲，光明正大。"),
    ("频道描述", "description",
     "全球体育生文化总部。体育生图鉴、直男观察、浓度测试，和一部叫《体育生》的 BL 视觉小说。每周三更新。\n"
     "官网 → https://www.sportsboy.gay\n"
     "EN: The global HQ of jock culture, through a gay lens."),
    ("频道链接", "link", "https://www.sportsboy.gay"),
    ("视频标题", "video_title", "直男做体育生浓度测试，做到第三题破防了 | SportsBoy.gay"),
    ("视频描述（前两行）", "video_desc",
     "六道题测出你的体育生人格，泳队/篮球/健身房/全能。\n"
     "→ https://www.sportsboy.gay/quiz?utm_source=youtube&utm_medium=social"),
    ("视频标签", "tags", "体育生、jock、gay quiz、BL game、visual novel、直男观察、sportsboy.gay"),
    ("GSC 站点地图", "gsc_sitemap", "https://www.sportsboy.gay/sitemap.xml"),
]

# ---------- 图片物料（base64 内嵌 + 下载按钮） ----------
IMAGES = [
    ("yt-avatar.png", "频道头像", "800×800",
     "珊瑚底黑 S，与站点 favicon 同语言。上传到「自定义 → 品牌形象 → 头像」，YouTube 自动裁圆，居中无压力。"),
    ("yt-banner.jpg", "频道横幅", "2560×1440",
     "暗调淋浴写真 + SPORTSBOY.gay +「汗水、肌肉与骄傲，光明正大。/ 全球体育生文化总部·每周三更新」。文字全部在 1546×423 安全区内，手机/电脑/TV 三端都不会被裁。"),
    ("yt-thumb-template.png", "缩略图母版", "1280×720",
     "以后每条视频的版式。左侧三个文字位（主标题 3-6 字 / 珊瑚钩子 / 落版小字），右侧肖像位。改 tools/gen_first_thumb.py 顶部三行字重跑即可出新图。"),
    ("yt-thumb-shorts01.png", "第一条 Shorts 缩略图", "1280×720",
     "成品直接用。钩子三件套：破防了 / 直男做浓度测试，第三题 / sportsboy.gay/quiz。"),
]

# ---------- 30 秒脚本 ----------
SCRIPT_ROWS = [
    ("0-3s", "直男队友入镜，表情困惑", "“让直男做体育生浓度测试，会发生什么？”"),
    ("3-15s", "测试答题快切，题目大字幕", "Q1“周末最想去哪？”→“篮球场啊，这题有问题？”"),
    ("15-25s", "结果页弹出：篮球体育生 · 浓度 91%", "“……这测试有点东西。”"),
    ("25-30s", "官网 quiz 页 + 珊瑚橙 CTA", "“来测测你的浓度 → sportsboy.gay/quiz”"),
]

# ---------- 注册步骤 ----------
STEPS = [
    "youtube.com → 右上角头像 → 创建频道 → 填上面「四要素」全部字段",
    "频道 → 自定义 → 品牌形象 → 上传头像 + 横幅，上传后点开手机/电脑/电视三种预览，确认文字没被裁",
    "发布第一条 Shorts：标题/描述/标签用上面「上传参数」，缩略图选 yt-thumb-shorts01.png",
    "发布后到评论区置顶放 quiz 链接（https://www.sportsboy.gay/quiz）",
    "顺手把 GSC 站点地图提交也做了（sitemap.xml，25 条 URL）",
]


def b64(name):
    with open(os.path.join(IMG, name), "rb") as f:
        return "data:image/%s;base64,%s" % ("jpeg" if name.endswith(".jpg") else "png", base64.b64encode(f.read()).decode("ascii"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


fields_html = "\n".join(
    '''    <div class="field">
      <div class="field-head"><span class="field-label">%s</span><button class="copy-btn" type="button" data-key="%s">复制</button></div>
      <div class="field-body" id="%s"></div>
    </div>''' % (esc(label), key, key)
    for label, key, _ in FIELDS
)

images_html = "\n".join(
    '''    <div class="asset">
      <div class="asset-imgwrap"><img src="%s" alt="%s" loading="lazy"></div>
      <div class="asset-meta">
        <div class="asset-title">%s <span class="asset-dim">%s</span></div>
        <div class="asset-note">%s</div>
        <a class="dl-btn" href="%s" download="%s">下载图片</a>
      </div>
    </div>''' % (b64(name), esc(title), esc(title), esc(dim), esc(note), b64(name), name)
    for name, title, dim, note in IMAGES
)

script_rows = "\n".join(
    '      <tr><td class="t-time">%s</td><td>%s</td><td class="t-line">%s</td></tr>' % (esc(a), esc(b), esc(c))
    for a, b, c in SCRIPT_ROWS
)

steps_html = "\n".join('      <li>%s</li>' % esc(s) for s in STEPS)

copy_data = json.dumps({k: v for _, k, v in FIELDS}, ensure_ascii=False, indent=2)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube 频道资料包 — SportsBoy.gay</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0E0D0B; --surface: #1B1813; --surface-2: #221E18;
  --line: #2E2A22; --line-soft: #241F19;
  --text: #F4EFE7; --muted: #A79F92;
  --coral: #FF5C2B; --coral-deep: #D85A30; --coral-ink: #1A0D06;
  --display: "Archivo Black", "Noto Sans SC", system-ui, sans-serif;
  --body: "Noto Sans SC", system-ui, -apple-system, sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: var(--body); line-height: 1.7; -webkit-font-smoothing: antialiased; }
::selection { background: var(--coral); color: var(--coral-ink); }
.wrap { width: min(880px, 92vw); margin-inline: auto; padding-block: 4rem 5rem; }
.kicker { display: inline-flex; align-items: center; gap: .8em; font-size: .78rem; font-weight: 700; letter-spacing: .28em; text-transform: uppercase; color: var(--coral); margin-bottom: 1.2rem; }
.kicker::before { content: ""; width: 42px; height: 1px; background: var(--coral); }
h1 { font-family: var(--display); font-size: clamp(2rem, 5vw, 2.8rem); line-height: 1.1; margin-bottom: .8rem; }
.lede { color: var(--muted); max-width: 40em; margin-bottom: 1.4rem; }
.hint { display: inline-block; font-size: .82rem; color: var(--coral); background: var(--surface); border: 1px dashed var(--coral-deep); border-radius: 999px; padding: .4rem 1.1rem; margin-bottom: 3rem; }
h2 { font-family: var(--display); font-size: 1.35rem; margin: 3.2rem 0 1.4rem; padding-top: 1.6rem; border-top: 1px solid var(--line-soft); }
h2 .en { display: block; font-family: var(--body); font-size: .72rem; font-weight: 700; letter-spacing: .22em; text-transform: uppercase; color: var(--coral); margin-top: .4rem; }
/* 字段复制卡 */
.field { background: var(--surface); border: 1px solid var(--line-soft); border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: .9rem; }
.field-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: .5rem; }
.field-label { font-size: .78rem; font-weight: 700; letter-spacing: .12em; color: var(--coral); }
.copy-btn { font-family: var(--body); font-size: .78rem; font-weight: 700; color: var(--text); background: var(--surface-2); border: 1px solid var(--line); border-radius: 8px; padding: .35rem 1rem; cursor: pointer; transition: border-color .2s, color .2s; }
.copy-btn:hover { border-color: var(--coral); color: var(--coral); }
.copy-btn.done { border-color: var(--coral); color: var(--coral); }
.field-body { font-size: .95rem; white-space: pre-wrap; word-break: break-all; color: var(--text); }
/* 图片物料 */
.asset { display: grid; grid-template-columns: 220px 1fr; gap: 1.4rem; background: var(--surface); border: 1px solid var(--line-soft); border-radius: 14px; padding: 1.2rem; margin-bottom: 1rem; align-items: center; }
.asset-imgwrap { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: var(--bg); }
.asset-imgwrap img { display: block; width: 100%; height: auto; }
.asset-title { font-weight: 700; font-size: 1.02rem; margin-bottom: .3rem; }
.asset-dim { font-family: var(--display); font-size: .68rem; color: var(--coral); letter-spacing: .06em; margin-left: .5rem; }
.asset-note { font-size: .85rem; color: var(--muted); margin-bottom: .8rem; }
.dl-btn { display: inline-block; font-size: .8rem; font-weight: 700; color: var(--coral); border: 1px solid var(--coral-deep); border-radius: 8px; padding: .35rem 1.1rem; text-decoration: none; transition: background .2s, color .2s; }
.dl-btn:hover { background: var(--coral); color: var(--coral-ink); }
/* 脚本表 */
table { width: 100%; border-collapse: collapse; font-size: .9rem; }
th { text-align: left; font-size: .75rem; letter-spacing: .14em; color: var(--muted); padding: .6rem .8rem; border-bottom: 1px solid var(--line); }
td { padding: .8rem; border-bottom: 1px solid var(--line-soft); vertical-align: top; }
tr:last-child td { border-bottom: none; }
.t-time { font-family: var(--display); color: var(--coral); white-space: nowrap; font-size: .85rem; }
.t-line { color: var(--text); }
/* 步骤 */
ol.steps { list-style: none; counter-reset: step; }
ol.steps li { counter-increment: step; position: relative; padding: .7rem 0 .7rem 3rem; border-bottom: 1px solid var(--line-soft); font-size: .95rem; }
ol.steps li:last-child { border-bottom: none; }
ol.steps li::before { content: counter(step); position: absolute; left: 0; top: .7rem; width: 2rem; height: 2rem; display: grid; place-items: center; font-family: var(--display); font-size: .85rem; color: var(--coral-ink); background: var(--coral); border-radius: 8px; }
.foot { margin-top: 4rem; padding-top: 1.6rem; border-top: 1px solid var(--line-soft); font-size: .8rem; color: var(--muted); display: flex; flex-wrap: wrap; gap: .4rem 1.4rem; }
@media (max-width: 640px) { .asset { grid-template-columns: 1fr; } .asset-imgwrap { max-width: 300px; } }
</style>
</head>
<body>
<div class="wrap">

  <p class="kicker">SportsBoy.gay · 内部资料</p>
  <h1>YouTube 频道资料包</h1>
  <p class="lede">建频道需要的全部字段、物料和第一条 Shorts 的上传参数，都在这一个文件里。图片已内嵌，单文件拷走就能用。</p>
  <p class="hint">用法：文字字段点「复制」，图片点「下载图片」或右键另存</p>

  <h2>一、频道四要素<span class="en">Channel Setup</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">注册时逐个粘贴。描述建议中文为主，结尾那行英文是吃 jock 关键词的。</p>
__FIELDS__

  <h2>二、四张物料<span class="en">Assets</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">前两张传频道品牌形象，后两张是缩略图：母版留给以后每条视频，成品直接用于第一条。</p>
__IMAGES__

  <h2>三、第一条 Shorts<span class="en">First Shorts</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">30 秒脚本，照着拍。找不到直男队友就用屏录 quiz + edge-tts 配音 + 大字幕，同一脚本剪，“破防”时刻用结果页弹出的浓度数字制造。</p>
  <div class="field" style="padding:0;overflow:hidden">
    <table>
      <thead><tr><th>时间</th><th>画面</th><th>台词 / 字幕</th></tr></thead>
      <tbody>
__SCRIPT_ROWS__
      </tbody>
    </table>
  </div>

  <h2>四、注册步骤<span class="en">Checklist</span></h2>
  <ol class="steps">
__STEPS__
  </ol>

  <div class="foot">
    <span>SportsBoy.gay · 荷尔蒙编辑部</span>
    <span>物料生成器：sportsboy-site/tools/</span>
    <span>2026-10-25</span>
  </div>

</div>

<script>
var COPY_DATA = __COPY_DATA__;
document.querySelectorAll(".copy-btn").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var text = COPY_DATA[btn.getAttribute("data-key")] || "";
    function done() {
      btn.textContent = "已复制";
      btn.classList.add("done");
      setTimeout(function () { btn.textContent = "复制"; btn.classList.remove("done"); }, 1600);
    }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); done(); } catch (e) {}
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(fallback);
    } else {
      fallback();
    }
  });
});
// 字段内容与剪贴板同源渲染
document.querySelectorAll(".field-body").forEach(function (el) {
  var key = el.id;
  if (COPY_DATA[key] !== undefined) el.textContent = COPY_DATA[key];
});
</script>
</body>
</html>
"""

html = (html
        .replace("__FIELDS__", fields_html)
        .replace("__IMAGES__", images_html)
        .replace("__SCRIPT_ROWS__", script_rows)
        .replace("__STEPS__", steps_html)
        .replace("__COPY_DATA__", copy_data))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("saved:", OUT)
print("size: %.1f MB" % (os.path.getsize(OUT) / 1048576))
