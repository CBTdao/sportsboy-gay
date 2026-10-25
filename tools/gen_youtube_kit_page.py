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

# ---------- 频道四要素（可复制） ----------
FIELDS = [
    ("频道名", "channel_name", "SportsBoy（.gay 落在 handle @sportsboygay、横幅与官网三处，显示名用短名）"),
    ("用户号 Handle", "handle", "@sportsboygay"),
    ("频道口号", "tagline", "汗水、肌肉与骄傲，光明正大。"),
    ("频道描述（四语）", "description",
     "全球体育生文化总部。体育生图鉴、直男观察、浓度测试，和一部叫《体育生》的 BL 视觉小说。每周三更新。\n"
     "→ https://www.sportsboy.gay\n"
     "\n"
     "EN: The global HQ of jock culture, through a gay lens. Almanacs, the gaze, the concentration test, and a BL visual novel called Jocks. New episodes Wednesdays.\n"
     "→ https://www.sportsboy.gay\n"
     "\n"
     "JA: ゲイの目線で見る体育会カルチャー総本部。図鑑、直男観察、濃度テスト、BL ビジュアルノベル『体育生』。毎週水曜更新。\n"
     "→ https://www.sportsboy.gay\n"
     "\n"
     "KO: 게이의 시선으로 보는 스포츠맨 문화 총본부. 도감, 직남 관찰, 농도 테스트, BL 비주얼 노벨 『스포츠맨』. 매주 수요일 업데이트.\n"
     "→ https://www.sportsboy.gay"),
    ("频道链接", "link", "https://www.sportsboy.gay"),
    ("GSC 站点地图", "gsc_sitemap", "https://www.sportsboy.gay/sitemap.xml"),
]

# ---------- 两条 Shorts 的上传参数（可复制） ----------
SHORTS = [
    ("Shorts 01 · 体育生浓度测试", [
        ("标题", "v1_title", "直男做体育生浓度测试，做到第三题破防了 | SportsBoy"),
        ("描述", "v1_desc",
         "六道题测出你的体育生人格，泳队/篮球/健身房/全能。\n"
         "→ https://www.sportsboy.gay/quiz?utm_source=youtube&utm_medium=social\n"
         "#shorts"),
        ("标签", "v1_tags", "体育生、jock、gay quiz、BL game、visual novel、直男观察、sportsboy.gay"),
        ("缩略图文件", "v1_thumb", "yt-thumb-shorts01.png"),
        ("置顶评论", "v1_comment", "测完来评论区报一下你的浓度 → https://www.sportsboy.gay/quiz"),
    ]),
    ("Shorts 02 · 篮球体育生图鉴", [
        ("标题", "v2_title", "怎么一眼认出篮球体育生？看这四条 | SportsBoy"),
        ("描述", "v2_desc",
         "篮球体育生图鉴：鞋柜、脚踝、球衣、记性，四条全中的浓度不低。\n"
         "来测测你的 → https://www.sportsboy.gay/quiz?utm_source=youtube&utm_medium=social\n"
         "#shorts"),
        ("标签", "v2_tags", "篮球体育生、体育生图鉴、jock、basketball jock、gay quiz、BL game、直男观察、sportsboy.gay"),
        ("缩略图文件", "v2_thumb", "yt-thumb-shorts02.png"),
        ("置顶评论", "v2_comment", "你中了几条？ → https://www.sportsboy.gay/quiz"),
    ]),
]

# ---------- 图片物料（base64 内嵌 + 下载按钮） ----------
IMAGES = [
    ("yt-avatar.png", "频道头像", "800×800",
     "珊瑚底黑 S，与站点 favicon 同语言。上传到「自定义 → 品牌形象 → 头像」，YouTube 自动裁圆，居中无压力。"),
    ("yt-banner.jpg", "频道横幅", "2560×1440",
     "暗调淋浴写真 + SPORTSBOY.gay +「汗水、肌肉与骄傲，光明正大。/ 全球体育生文化总部·每周三更新」。文字全部在 1546×423 安全区内，手机/电脑/TV 三端都不会被裁。"),
    ("yt-thumb-template.png", "缩略图母版", "1280×720",
     "以后每条视频的版式。左侧三个文字位（主标题 3-6 字 / 珊瑚钩子 / 落版小字），右侧肖像位。改 tools/gen_first_thumb.py 顶部三行字重跑即可出新图。"),
    ("yt-thumb-shorts01.png", "Shorts 01 缩略图", "1080×1920 竖版",
     "Shorts 官方缩略图规范是 9:16（1080×1920，上限 2MB），本图 1.0MB。钩子：破防了 / 直男做浓度测试，第三题 / sportsboy.gay/quiz。文字在中央安全区，避开顶部 UI 与底部标题遮挡。16:9 旧版存为 yt-thumb-shorts01-16x9.png 备用。"),
    ("yt-thumb-shorts02.png", "Shorts 02 缩略图", "1080×1920 竖版",
     "同为 9:16 竖版规范。钩子：四条全中 / 你是篮球体育生吗？/ sportsboy.gay/quiz。底图是成片里的篮球场实拍帧。16:9 旧版存为 yt-thumb-shorts02-16x9.png 备用。"),
]

# ---------- 脚本参考（已拍完两条，留档） ----------
SCRIPT_ROWS_01 = [
    ("0-3s", "直男队友入镜，表情困惑", "“让直男做体育生浓度测试，会发生什么？”"),
    ("3-15s", "测试答题快切，题目大字幕", "Q1“周末最想去哪？”→“篮球场啊，这题有问题？”"),
    ("15-25s", "结果页弹出：篮球体育生 · 浓度 91%", "“……这测试有点东西。”"),
    ("25-30s", "官网 quiz 页 + 珊瑚橙 CTA", "“来测测你的浓度 → sportsboy.gay/quiz”"),
]

SCRIPT_ROWS_02 = [
    ("0-4s", "篮球场边缠护踝，抬头笑", "“怎么一眼认出篮球体育生？”"),
    ("4-22s", "四特征卡快切：鞋柜 / 脚踝 / 球衣 / 记性", "“AJ 按赛季排……护踝比对象亲……半场下来后背能透……被盖次数全记着。”"),
    ("22-26s", "收尾卡：四条全中 · 浓度不低", "“四条全中的，浓度不低。来测测你的浓度。”"),
    ("26-30s", "CTA 尾帧", "“sportsboy.gay”"),
]

# ---------- 通用上传设置（每条视频都过一遍） ----------
UPLOAD_SETTINGS = [
    "受众：「否，不是面向儿童」（上传流程必选，BL 内容）",
    "分类：体育；视频语言：中文（简体）",
    "允许嵌入、通知订阅者：都打开",
    "AI 披露：上传流程里勾选「内容经过改动或合成」（画面水印已去除，平台申报走它自己的通道）",
    "播放列表：建一个「SportsBoy.gay Shorts」，两条都放进去",
    "发布节奏：01 立即可见，02 排在周三，兑现简介里的「每周三更新」",
]


def b64(name):
    with open(os.path.join(IMG, name), "rb") as f:
        return "data:image/%s;base64,%s" % ("jpeg" if name.endswith(".jpg") else "png", base64.b64encode(f.read()).decode("ascii"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def field_html(label, key):
    return (
        '    <div class="field">\n'
        '      <div class="field-head"><span class="field-label">%s</span>'
        '<button class="copy-btn" type="button" data-key="%s">复制</button></div>\n'
        '      <div class="field-body" id="%s"></div>\n'
        '    </div>' % (esc(label), key, key)
    )


fields_html = "\n".join(field_html(label, key) for label, key, _ in FIELDS)

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

shorts_blocks = []
for video_name, rows in SHORTS:
    inner = "\n".join(field_html(label, key) for label, key, _ in rows)
    shorts_blocks.append(
        '  <div class="video-block">\n    <h3 class="video-block-title">%s</h3>\n%s\n  </div>'
        % (esc(video_name), inner)
    )
shorts_html = "\n".join(shorts_blocks)

script_rows_01 = "\n".join(
    '      <tr><td class="t-time">%s</td><td>%s</td><td class="t-line">%s</td></tr>' % (esc(a), esc(b), esc(c))
    for a, b, c in SCRIPT_ROWS_01
)
script_rows_02 = "\n".join(
    '      <tr><td class="t-time">%s</td><td>%s</td><td class="t-line">%s</td></tr>' % (esc(a), esc(b), esc(c))
    for a, b, c in SCRIPT_ROWS_02
)

settings_html = "\n".join('      <li>%s</li>' % esc(s) for s in UPLOAD_SETTINGS)

copy_data = json.dumps(
    {k: v for _, k, v in FIELDS} | {k: v for _, rows in SHORTS for _, k, v in rows},
    ensure_ascii=False, indent=2,
)

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
h3.video-block-title { font-size: 1.05rem; margin: 1.6rem 0 .9rem; color: var(--coral); }
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
/* 设置清单 */
ul.settings { list-style: none; }
ul.settings li { position: relative; padding: .7rem 0 .7rem 2.2rem; border-bottom: 1px solid var(--line-soft); font-size: .95rem; }
ul.settings li:last-child { border-bottom: none; }
ul.settings li::before { content: "✓"; position: absolute; left: 0; top: .7rem; width: 1.5rem; height: 1.5rem; display: grid; place-items: center; font-weight: 700; color: var(--coral-ink); background: var(--coral); border-radius: 6px; font-size: .85rem; }
.foot { margin-top: 4rem; padding-top: 1.6rem; border-top: 1px solid var(--line-soft); font-size: .8rem; color: var(--muted); display: flex; flex-wrap: wrap; gap: .4rem 1.4rem; }
@media (max-width: 640px) { .asset { grid-template-columns: 1fr; } .asset-imgwrap { max-width: 300px; } }
</style>
</head>
<body>
<div class="wrap">

  <p class="kicker">SportsBoy.gay · 内部资料</p>
  <h1>YouTube 频道资料包</h1>
  <p class="lede">建频道、发视频需要的全部字段、物料和上传参数，都在这一个文件里。图片已内嵌，单文件拷走就能用。</p>
  <p class="hint">用法：文字字段点「复制」，图片点「下载图片」或右键另存</p>

  <h2>一、频道四要素<span class="en">Channel Setup</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">注册时逐个粘贴。描述是四语版，中文打头、英日韩各一段，每段自带官网链接。</p>
__FIELDS__

  <h2>二、五张物料<span class="en">Assets</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">前两张传频道品牌形象；后三张是缩略图，母版留给以后每条视频，两条 Shorts 的成品直接用。</p>
__IMAGES__

  <h2>三、两条 Shorts 上传参数<span class="en">Upload Settings</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">每条视频五个字段，逐个复制粘贴。缩略图在传视频的同一个页面里上传。</p>
__SHORTS__

  <h2>四、通用上传设置<span class="en">Every Upload</span></h2>
  <ul class="settings">
__SETTINGS__
  </ul>

  <h2>五、脚本参考<span class="en">Scripts</span></h2>
  <p class="lede" style="margin-bottom:1.4rem">已拍完两条的脚本留档，下次拍新视频照着这个格式改。</p>
  <h3 class="video-block-title">Shorts 01 · 体育生浓度测试（30 秒）</h3>
  <div class="field" style="padding:0;overflow:hidden">
    <table>
      <thead><tr><th>时间</th><th>画面</th><th>台词 / 字幕</th></tr></thead>
      <tbody>
__SCRIPT_01__
      </tbody>
    </table>
  </div>
  <h3 class="video-block-title">Shorts 02 · 篮球体育生图鉴（30 秒）</h3>
  <div class="field" style="padding:0;overflow:hidden">
    <table>
      <thead><tr><th>时间</th><th>画面</th><th>台词 / 字幕</th></tr></thead>
      <tbody>
__SCRIPT_02__
      </tbody>
    </table>
  </div>

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
        .replace("__SHORTS__", shorts_html)
        .replace("__SETTINGS__", settings_html)
        .replace("__SCRIPT_01__", script_rows_01)
        .replace("__SCRIPT_02__", script_rows_02)
        .replace("__COPY_DATA__", copy_data))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("saved:", OUT)
print("size: %.1f MB" % (os.path.getsize(OUT) / 1048576))
