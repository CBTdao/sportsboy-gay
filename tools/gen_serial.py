# -*- coding: utf-8 -*-
"""gen_serial.py — 生成官网「文字小说 / 视觉小说连载」两个日更栏目。

设计：
- 源：content/novel/*.md（文字小说）、content/vn/*.md（《体育生》视觉小说免费连载）
  每个 md 顶部为 frontmatter（title/date/episode/summary/tags），空行后为正文。
- 正文为 markdown-lite：段落、#/## 标题、> 引用、**加粗**、--- 分隔线，
  以及对话行「角色：台词」自动渲染为带说话人样式的对话块。
- 输出：
    /<section>/index.html        列表页（最新在前）
    /<section>/<slug>.html       章节/场次详情页（仅中文，带 Article JSON-LD）
    /en|ja|ko/<section>/index.html  四语索引（详情页暂为 zh，附「翻译中」徽标）
- 同步更新 sitemap.xml（追加新 URL 与 hreflang 备用链接）。
- 复用 site 共享 CSS / 导航 / 页脚，符合既有页面风格。

运行：python tools/gen_serial.py  （在 sportsboy-site 仓库根目录或任意位置均可）
"""
import os
import re
import json
import glob
from html import escape

BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"
SITE = "https://www.sportsboy.gay"

SECTIONS = {
    "novel": {
        "slug": "novel",
        "label": {"zh": "文字小说", "en": "Novel", "ja": "小説", "ko": "소설"},
        "badge": {"zh": "文字小说", "en": "NOVEL", "ja": "小説", "ko": "소설"},
        "section_idx": {"zh": "06 / 文字小说", "en": "06 / NOVEL", "ja": "06 / 小説", "ko": "06 / 소설"},
        "h2": {"zh": "文字小说 · 体育生宇宙", "en": "Novel · The SportsBoy Universe",
               "ja": "小説 · SportsBoy ユニバース", "ko": "소설 · SportsBoy 유니버스"},
        "secdesc": {
            "zh": "《体育生》宇宙的散文连载——泳队、白袜、更衣室，一段段被汗水泡软的少年事。每日更新。",
            "en": "Prose serial from the SportsBoy universe. Updated daily.",
            "ja": "SportsBoy ユニバースの散文連載。毎日更新。",
            "ko": "SportsBoy 유니버스의 산문 연재. 매일 업데이트.",
        },
        "cta_h": {"zh": "顺手测测你的体育生浓度", "en": "Test your jock vibe", "ja": "体育生濃度を診断", "ko": "운동선수 농도 테스트"},
        "cta_d": {"zh": "6 道题，30 秒，生成专属人格图鉴——可分享。", "en": "6 questions, 30 seconds, shareable persona chart.",
                  "ja": "6問、30秒、シェア可能な診断チャート。", "ko": "6문제, 30초, 공유 가능한 페르소나 차트."},
        "cta_b": {"zh": "开始测试", "en": "Start", "ja": "診断する", "ko": "시작"},
    },
    "vn": {
        "slug": "vn",
        "label": {"zh": "视觉小说", "en": "Visual Novel", "ja": "ビジュアルノベル", "ko": "비주얼 노벨"},
        "badge": {"zh": "《体育生》免费连载", "en": "FREE SERIAL", "ja": "無料連載", "ko": "무료 연재"},
        "section_idx": {"zh": "07 / 视觉小说", "en": "07 / VISUAL NOVEL", "ja": "07 / ビジュアルノベル", "ko": "07 / 비주얼 노벨"},
        "h2": {"zh": "《体育生》· 免费公开连载", "en": "《体育生》· Free Public Serial",
               "ja": "『体育生』· 無料公開連載", "ko": "『体育生』· 무료 공개 연재"},
        "secdesc": {
            "zh": "首部视觉小说《体育生》剧本逐场公开、免费阅读。每日更新一场，完整版后续上线。角色全部成年设定。",
            "en": "The script of our first visual novel, published scene by scene — free to read. Updated daily.",
            "ja": "処女作ビジュアルノベルの脚本を逐次公開・無料読了。毎日更新。",
            "ko": "첫 비주얼 노벨의 대본을 장면별로 공개·무료 열람. 매일 업데이트.",
        },
        "cta_h": {"zh": "顺手测测你的体育生浓度", "en": "Test your jock vibe", "ja": "体育生濃度を診断", "ko": "운동선수 농도 테스트"},
        "cta_d": {"zh": "6 道题，30 秒，生成专属人格图鉴——可分享。", "en": "6 questions, 30 seconds, shareable persona chart.",
                  "ja": "6問、30秒、シェア可能な診断チャート。", "ko": "6문제, 30초, 공유 가능한 페르소나 차트."},
        "cta_b": {"zh": "开始测试", "en": "Start", "ja": "診断する", "ko": "시작"},
    },
}

LANGS = ["zh", "en", "ja", "ko"]
HTMLLANG = {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}
LANGLABEL = {"zh": "中文", "en": "English", "ja": "日本語", "ko": "한국어"}
NAV = {
    "columns": {"zh": "王牌栏目", "en": "Columns", "ja": "コラム", "ko": "칼럼"},
    "work": {"zh": "首部作品", "en": "Our VN", "ja": "処女作", "ko": "첫 작품"},
    "flywheel": {"zh": "宇宙", "en": "Universe", "ja": "ユニバース", "ko": "유니버스"},
    "quiz": {"zh": "浓度测试", "en": "Vibe Test", "ja": "濃度テスト", "ko": "농도 테스트"},
    "conc": {"zh": "浓度分布", "en": "Vibe Map", "ja": "分布", "ko": "분포"},
    "videos": {"zh": "视频", "en": "Videos", "ja": "動画", "ko": "영상"},
    "back": {"zh": "← 返回栏目", "en": "← Back", "ja": "← 戻る", "ko": "← 돌아가기"},
}

# ----------------------------------------------------------------------------
# Markdown-lite 渲染
# ----------------------------------------------------------------------------

def parse_frontmatter(text):
    lines = text.split("\n")
    meta = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m and i < 30:
            meta[m.group(1).lower()] = m.group(2).strip()
            i += 1
        else:
            break
    body = "\n".join(lines[i:])
    return meta, body


def render_inline(s):
    s = escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def render_body(body):
    """把 markdown-lite 正文渲染为 HTML 片段。"""
    out = []
    lines = body.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # 分隔线
        if re.match(r"^-{3,}$", line.strip()):
            out.append("<hr>")
            i += 1
            continue
        # 标题
        if line.startswith("## "):
            out.append("<h2>%s</h2>" % render_inline(line[3:].strip()))
            i += 1
            continue
        if line.startswith("# "):
            out.append("<h2>%s</h2>" % render_inline(line[2:].strip()))
            i += 1
            continue
        # 引用块
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % render_inline(" ".join(buf)))
            continue
        # 对话行：角色：台词
        dm = re.match(r"^([^：:]{1,20})[：:]\s*(.*)$", line)
        if dm and not line.startswith(("http", "www")):
            spk = dm.group(1).strip()
            txt = dm.group(2).strip()
            out.append('<p class="dialogue"><span class="speaker">%s</span>%s</p>'
                       % (escape(spk), render_inline(txt)))
            i += 1
            continue
        # 空行
        if not line.strip():
            i += 1
            continue
        # 普通段落：合并连续非空、非特殊行
        buf = [line.strip()]
        i += 1
        while i < n and lines[i].strip() and not lines[i].startswith(("#", ">", "-", "---")):
            if re.match(r"^([^：:]{1,20})[：:]\s*(.*)$", lines[i]) and not lines[i].startswith(("http", "www")):
                break
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % render_inline("".join(buf)))
    return "\n".join(out)


# ----------------------------------------------------------------------------
# 页面模板
# ----------------------------------------------------------------------------

def hreflang_block(zh, en, ja, ko, xdefault=None):
    xd = xdefault or zh
    return (
        '<link rel="alternate" hreflang="zh-CN" href="%s">\n' % zh +
        '<link rel="alternate" hreflang="en" href="%s">\n' % en +
        '<link rel="alternate" hreflang="ja" href="%s">\n' % ja +
        '<link rel="alternate" hreflang="ko" href="%s">\n' % ko +
        '<link rel="alternate" hreflang="x-default" href="%s">' % xd
    )


def build_page(lang, section_key, title, desc, h2, secdesc, section_idx,
               canon, zh_path, en_path, ja_path, ko_path, main_html,
               is_detail=False, ld_json="", active_nav=""):
    sec = SECTIONS[section_key]
    nav_novel_cls = "is-current" if active_nav == "novel" else ""
    nav_vn_cls = "is-current" if active_nav == "vn" else ""
    if is_detail:
        hb = '<link rel="alternate" hreflang="x-default" href="%s">' % canon
    else:
        hb = hreflang_block(zh_path, en_path, ja_path, ko_path)
    t = TPL
    for k, v in {
        "__HTMLLANG__": HTMLLANG[lang],
        "__LANGLABEL__": LANGLABEL[lang],
        "__SITE__": SITE,
        "__OGURL__": canon,
        "__CANON__": canon,
        "__TITLE__": title,
        "__DESC__": desc,
        "__OGTYPE__": "article" if is_detail else "website",
        "__HREFLANG__": hb,
        "__LDJSON__": ld_json,
        "__NAV_COLUMNS__": NAV["columns"][lang],
        "__NAV_WORK__": NAV["work"][lang],
        "__NAV_FLYWHEEL__": NAV["flywheel"][lang],
        "__NAV_QUIZ__": NAV["quiz"][lang],
        "__NAV_CONC__": NAV["conc"][lang],
        "__NAV_VIDEOS__": NAV["videos"][lang],
        "__NAV_NOVEL__": SECTIONS["novel"]["label"][lang],
        "__NAV_VN__": SECTIONS["vn"]["label"][lang],
        "__ACTIVE_NOVEL__": nav_novel_cls,
        "__ACTIVE_VN__": nav_vn_cls,
        "__ACTIVE_ZH__": "is-active" if lang == "zh" else "",
        "__ACTIVE_EN__": "is-active" if lang == "en" else "",
        "__ACTIVE_JA__": "is-active" if lang == "ja" else "",
        "__ACTIVE_KO__": "is-active" if lang == "ko" else "",
        "__ZH_PATH__": zh_path,
        "__EN_PATH__": en_path,
        "__JA_PATH__": ja_path,
        "__KO_PATH__": ko_path,
        "__MAIN__": main_html,
        "__BADGE__": sec["badge"][lang],
        "__SECTIONIDX__": section_idx[lang],
        "__H2__": h2[lang],
        "__SECDESC__": secdesc[lang],
        "__CTA_H__": sec["cta_h"][lang],
        "__CTA_D__": sec["cta_d"][lang],
        "__CTA_B__": sec["cta_b"][lang],
        "__BACK__": NAV["back"][lang],
    }.items():
        t = t.replace(k, v)
    return t


def cta_band(lang, section_key):
    sec = SECTIONS[section_key]
    return (
        '<section class="block block-alt" id="quiz-cta"><div class="container">'
        '<div class="cta-band reveal"><div><h2>__CTA_H__</h2><p>__CTA_D__</p></div>'
        '<a class="btn btn-dark" href="/quiz">__CTA_B__</a></div></div></section>'
    ).replace("__CTA_H__", sec["cta_h"][lang]).replace("__CTA_D__", sec["cta_d"][lang]).replace("__CTA_B__", sec["cta_b"][lang])


def load_items(section_key):
    folder = os.path.join(BASE, "content", section_key)
    items = []
    for path in sorted(glob.glob(os.path.join(folder, "*.md"))):
        with open(path, encoding="utf-8") as f:
            meta, body = parse_frontmatter(f.read())
        slug = os.path.splitext(os.path.basename(path))[0]
        items.append({
            "slug": slug, "meta": meta, "body": body,
            "html": render_body(body),
            "title": meta.get("title", slug),
            "date": meta.get("date", ""),
            "episode": meta.get("episode", ""),
            "summary": meta.get("summary", ""),
            "tags": meta.get("tags", ""),
        })
    # 按日期升序（旧→新），索引页再倒序
    items.sort(key=lambda x: (x["date"], x["slug"]))
    return items


def index_main(lang, section_key, items):
    sec = SECTIONS[section_key]
    cards = []
    for it in reversed(items):  # 最新在前
        cards.append(
            '<a class="serial-card reveal" href="/%s/%s.html">'
            '<h3>%s</h3>'
            '<p class="serial-meta">%s%s</p>'
            '<p>%s</p></a>'
            % (section_key, it["slug"], escape(it["title"]),
               escape(it["date"]), (" · EP%s" % escape(str(it["episode"]))) if it["episode"] else "",
               escape(it["summary"]))
        )
    return (
        '<section class="block" style="padding-top:140px"><div class="container">'
        '<div class="section-head reveal"><p class="section-index">__SECTIONIDX__</p>'
        '<h2>__H2__</h2><p class="section-desc">__SECDESC__</p></div>'
        '<div class="serial-list">%s</div></div></section>' % "\n".join(cards)
    )


def detail_main(lang, section_key, it):
    sec = SECTIONS[section_key]
    return (
        '<section class="block" style="padding-top:140px"><div class="container">'
        '<article class="serial-article"><div class="post-head">'
        '<span class="sec-badge">__BADGE__</span>'
        '<h1>%s</h1><p class="post-meta">%s%s</p></div>'
        '%s'
        '<p style="margin-top:30px"><a href="/%s">__BACK__</a></p>'
        '</article></div></section>'
        % (escape(it["title"]), escape(it["date"]),
           (" · EP%s" % escape(str(it["episode"]))) if it["episode"] else "",
           it["html"], section_key)
    ).replace("__BADGE__", sec["badge"][lang]).replace("__BACK__", NAV["back"][lang])


def article_ldjson(canon, title, date, desc):
    obj = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "datePublished": date, "dateModified": date,
        "description": desc, "inLanguage": "zh-CN",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
        "publisher": {"@type": "Organization", "name": "SportsBoy.gay",
                      "url": SITE + "/"},
    }
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)


def update_sitemap(new_urls):
    """new_urls: list of (zh, en, ja, ko) url tuples（索引页）或 (zh, None, None, None)（详情页 zh）。"""
    sp = os.path.join(BASE, "sitemap.xml")
    with open(sp, encoding="utf-8") as f:
        content = f.read()
    existing = set(re.findall(r"<loc>(.*?)</loc>", content))
    blocks = []
    for zh, en, ja, ko in new_urls:
        if zh in existing:
            continue
        if en and ja and ko:
            alts = (
                '<xhtml:link rel="alternate" hreflang="zh-CN" href="%s"/>' % zh +
                '<xhtml:link rel="alternate" hreflang="en" href="%s"/>' % en +
                '<xhtml:link rel="alternate" hreflang="ja" href="%s"/>' % ja +
                '<xhtml:link rel="alternate" hreflang="ko" href="%s"/>' % ko +
                '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % zh
            )
        else:
            alts = '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % zh
        blocks.append("  <url>\n    <loc>%s</loc>\n    %s\n  </url>" % (zh, alts))
    if blocks:
        content = content.replace("</urlset>", "\n".join(blocks) + "\n</urlset>")
        with open(sp, "w", encoding="utf-8") as f:
            f.write(content)
        print("sitemap: added %d urls" % len(blocks))
    else:
        print("sitemap: no new urls")


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------

TPL = r"""<!DOCTYPE html>
<html lang="__HTMLLANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:image" content="__SITE__/assets/img/og.jpg">
<meta property="og:type" content="__OGTYPE__">
<meta property="og:url" content="__OGURL__">
<meta name="theme-color" content="#0E0D0B">
<link rel="icon" href="/assets/img/icon-512.png">
<link rel="manifest" href="/manifest.json">
<link rel="canonical" href="__CANON__">
__HREFLANG__
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<style>
.serial-list{display:grid;gap:18px;margin-top:28px;max-width:760px}
.serial-card{display:block;text-decoration:none;color:inherit;background:#16140F;border:1px solid #2a2620;border-radius:14px;padding:20px 22px;transition:.18s}
.serial-card:hover{border-color:#FF5C39;transform:translateY(-2px)}
.serial-card h3{margin:0 0 6px;font-size:20px}
.serial-meta{color:#a79f92;font-size:13px;margin:0 0 8px}
.serial-card p{margin:0;color:#cfc7ba;font-size:15px;line-height:1.65}
.serial-article{max-width:720px;margin:0 auto;padding-bottom:60px}
.serial-article .post-head{margin:36px 0 8px}
.serial-article h1{font-size:30px;line-height:1.3;margin:0 0 10px}
.serial-article .post-meta{color:#a79f92;font-size:13px;margin-bottom:24px}
.serial-article p{font-size:17px;line-height:1.9;color:#e9e3d8;margin:0 0 20px}
.serial-article h2{font-size:23px;margin:34px 0 12px;color:#fff}
.serial-article blockquote{border-left:3px solid #FF5C39;margin:22px 0;padding:4px 18px;color:#cfc7ba;background:#16140F;border-radius:0 8px 8px 0}
.serial-article .dialogue{margin:0 0 14px;font-size:17px;line-height:1.8;color:#e9e3d8}
.serial-article .speaker{color:#FF5C39;font-weight:700;margin-right:6px}
.serial-article hr{border:none;border-top:1px solid #2a2620;margin:28px 0}
.sec-badge{display:inline-block;font-size:12px;letter-spacing:.08em;color:#FF5C39;border:1px solid #FF5C39;border-radius:999px;padding:3px 10px;margin-bottom:14px}
</style>
__LDJSON__
</head>
<body>
<header class="site-header" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
    <nav class="nav-links" id="navLinks">
      <a href="/#columns">__NAV_COLUMNS__</a>
      <a href="/#work">__NAV_WORK__</a>
      <a href="/#flywheel">__NAV_FLYWHEEL__</a>
      <a href="/quiz">__NAV_QUIZ__</a>
      <a href="/concentration">__NAV_CONC__</a>
      <a href="/videos">__NAV_VIDEOS__</a>
      <a href="/novel" class="__ACTIVE_NOVEL__">__NAV_NOVEL__</a>
      <a href="/vn" class="__ACTIVE_VN__">__NAV_VN__</a>
    </nav>
    <div class="nav-side">
      <div class="lang-menu-wrap">
        <button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="langMenu">
          <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/></svg>
          <span>__LANGLABEL__</span>
        </button>
        <div class="lang-menu" id="langMenu" hidden>
          <a class="lang-opt __ACTIVE_ZH__" href="__ZH_PATH__" hreflang="zh-CN" lang="zh-CN">中文<span class="lang-opt-tag">ZH</span></a>
          <a class="lang-opt __ACTIVE_EN__" href="__EN_PATH__" hreflang="en" lang="en">English<span class="lang-opt-tag">EN</span></a>
          <a class="lang-opt __ACTIVE_JA__" href="__JA_PATH__" hreflang="ja" lang="ja">日本語<span class="lang-opt-tag">JA</span></a>
          <a class="lang-opt __ACTIVE_KO__" href="__KO_PATH__" hreflang="ko" lang="ko">한국어<span class="lang-opt-tag">KO</span></a>
        </div>
      </div>
      <button class="nav-toggle" aria-label="打开菜单" aria-expanded="false" aria-controls="navLinks"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main>
__MAIN__
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
        <p>汗水、肌肉与骄傲，光明正大。</p>
      </div>
      <div class="footer-col"><h4>站点</h4>
        <a href="/#columns">__NAV_COLUMNS__</a>
        <a href="/#work">__NAV_WORK__</a>
        <a href="/quiz">__NAV_QUIZ__</a>
        <a href="/concentration">__NAV_CONC__</a>
        <a href="/videos">__NAV_VIDEOS__</a>
        <a href="/novel">__NAV_NOVEL__</a>
        <a href="/vn">__NAV_VN__</a>
      </div>
      <div class="footer-col"><h4>社区</h4>
        <a href="https://afdian.com/a/sportsboy" target="_blank" rel="noopener">爱发电（完整版解锁）</a>
        <a href="https://cbtdao.itch.io/sportsboy" target="_blank" rel="noopener">itch.io</a>
        <a href="https://x.com/sportsboygay" target="_blank" rel="noopener">X</a>
        <a href="https://www.youtube.com/@sportsboygay" target="_blank" rel="noopener">YouTube</a>
      </div>
      <div class="footer-col"><h4>说明</h4>
        <p>本站含 BL 向内容，角色均为成年人设定。</p>
        <p>内容为虚构创作。</p>
      </div>
    </div>
    <div class="footer-bottom"><p>© <span id="year">2026</span> SportsBoy.gay</p><p>Hosted on Vercel</p></div>
  </div>
</footer>
<script src="/assets/js/main.js"></script>
</body>
</html>"""


def main():
    new_sitemap = []
    for key in SECTIONS:
        items = load_items(key)
        print("[%s] %d items" % (key, len(items)))
        # 索引页（四语）
        for lang in LANGS:
            main_html = index_main(lang, key, items) + cta_band(lang, key)
            zh_p = "/%s" % key
            en_p = "/en/%s" % key
            ja_p = "/ja/%s" % key
            ko_p = "/ko/%s" % key
            canon = SITE + zh_p
            title = SECTIONS[key]["h2"][lang]
            desc = SECTIONS[key]["secdesc"][lang]
            html = build_page(lang, key, title, desc, SECTIONS[key]["h2"],
                              SECTIONS[key]["secdesc"], SECTIONS[key]["section_idx"],
                              canon, zh_p, en_p, ja_p, ko_p, main_html,
                              active_nav=key)
            outdir = os.path.join(BASE, lang, key) if lang != "zh" else os.path.join(BASE, key)
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            new_sitemap.append((SITE + zh_p, SITE + en_p, SITE + ja_p, SITE + ko_p))
        # 详情页（仅中文）
        for it in items:
            main_html = detail_main("zh", key, it) + cta_band("zh", key)
            canon = SITE + "/%s/%s.html" % (key, it["slug"])
            ld = article_ldjson(canon, it["title"], it["date"], it["summary"])
            html = build_page("zh", key, it["title"], it["summary"], SECTIONS[key]["h2"],
                              SECTIONS[key]["secdesc"], SECTIONS[key]["section_idx"],
                              canon, "/%s" % key, "/en/%s" % key, "/ja/%s" % key, "/ko/%s" % key,
                              main_html, is_detail=True, ld_json=ld, active_nav=key)
            out = os.path.join(BASE, key, it["slug"] + ".html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            new_sitemap.append((canon, None, None, None))
            print("  wrote", out)
    update_sitemap(new_sitemap)
    print("DONE")


if __name__ == "__main__":
    main()
