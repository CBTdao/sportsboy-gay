# -*- coding: utf-8 -*-
"""gen_vn_feed.py — 生成《体育生》连载 RSS（追更提醒用）。

输出：
  /vn/feed.xml        中文章节主 feed
  /en/vn/feed.xml     英文读者订阅入口（仍指向中文章节）

读取 content/vn/*.md 的 frontmatter（title/date/summary），按日期升序排列。
运行：python tools/gen_vn_feed.py
"""
import os
import re
import glob

BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"
SITE = "https://www.sportsboy.gay"


def parse_frontmatter(text):
    meta = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", lines[i])
        if m and i < 30:
            meta[m.group(1).lower()] = m.group(2).strip()
            i += 1
        else:
            break
    return meta


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def build(items):
    items = sorted(items, key=lambda x: (x["date"], x["slug"]))
    entries = []
    for it in items:
        url = "%s/vn/%s" % (SITE, it["slug"])
        entries.append(
            "    <item>\n"
            "      <title>%s</title>\n"
            "      <link>%s</link>\n"
            '      <guid isPermaLink="true">%s</guid>\n'
            "      <pubDate>%s</pubDate>\n"
            "      <description>%s</description>\n"
            "    </item>\n"
            % (esc(it["title"]), url, url, esc(it["date"]), esc(it["summary"]))
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<?xml-stylesheet type="text/xsl" href="/assets/xsl/rss.xsl"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>《体育生》· 免费连载</title>\n"
        "    <link>%s/vn</link>\n"
        '    <atom:link href="%s/vn/feed.xml" rel="self" type="application/rss+xml"/>\n'
        "    <description>首部视觉小说《体育生》剧本逐场公开、免费阅读，每日更新一场。角色全部成年设定。</description>\n"
        "    <language>zh-CN</language>\n"
        "%s"
        "  </channel>\n"
        "</rss>\n"
    ) % (SITE, SITE, "".join(entries))


SUB_UI = {
    "zh": {
        "kicker": "SPORTSBOY.gay · 追更",
        "title": "追更《体育生》",
        "lead": "把下方地址添加到任意 RSS 阅读器（Feedly、鲜果、NetNewsWire、手机订阅器均可），之后每发布一场新章都会自动送到你面前。",
        "copy": "复制订阅地址",
        "copied": "已复制 ✓",
        "feedly": "用 Feedly 一键订阅",
        "chapters": "已发布章节",
        "back": "← 返回《体育生》连载首页",
    },
    "en": {
        "kicker": "SPORTSBOY.gay · Follow",
        "title": "Follow《体育生》",
        "lead": "Add the address below to any RSS reader (Feedly, NetNewsWire, your phone's reader). Every new scene will be delivered to you automatically.",
        "copy": "Copy feed URL",
        "copied": "Copied ✓",
        "feedly": "Subscribe with Feedly",
        "chapters": "Published scenes",
        "back": "← Back to《体育生》",
    },
    "ja": {
        "kicker": "SPORTSBOY.gay · 追う",
        "title": "《体育生》を追う",
        "lead": "下のアドレスを任意の RSS リーダー（Feedly、NetNewsWire、スマホのリーダー等）に追加すれば、新しい場面が公開されるたびに自動で届きます。",
        "copy": "フィードURLをコピー",
        "copied": "コピー済み ✓",
        "feedly": "Feedly で購読",
        "chapters": "公開済みの場面",
        "back": "← 《体育生》トップへ",
    },
    "ko": {
        "kicker": "SPORTSBOY.gay · 팔로우",
        "title": "《体育生》 팔로우",
        "lead": "아래 주소를 RSS 리더(Feedly, NetNewsWire, 휴대폰 리더 등)에 추가하면, 새로운 장면이 올라올 때마다 자동으로 전달됩니다.",
        "copy": "피드 주소 복사",
        "copied": "복사됨 ✓",
        "feedly": "Feedly로 구독",
        "chapters": "공개된 장면",
        "back": "← 《体育生》 첫 화로",
    },
}

SUB_TPL = r"""<!DOCTYPE html>
<html lang="__LANGLANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="msvalidate.01" content="83a632faa92c4ae0bd1086de9dc2902a" />
<title>__TITLE__ · SportsBoy.gay</title>
<meta name="description" content="__LEAD__">
<meta name="theme-color" content="#0E0D0B">
<link rel="icon" href="/assets/img/icon-512.png">
<link rel="manifest" href="/manifest.json">
<link rel="canonical" href="__CANON__">
<link rel="alternate" type="application/rss+xml" title="《体育生》连载" href="__FEEDURL__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<style>
.page-subscribe{background:#0E0D0B;color:#f3efe6;min-height:100vh}
.sub-wrap{max-width:760px;margin:0 auto;padding:120px 20px 80px}
.sub-wrap .kicker{color:#a79f92;font-size:13px;letter-spacing:.08em;margin:0 0 10px}
.sub-wrap h1{font-size:34px;margin:0 0 14px;color:#FF5C39}
.sub-wrap .lead{color:#cfc7ba;font-size:16px;line-height:1.8;margin:0 0 28px}
.sub-box{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:#16140F;border:1px solid #2a2620;border-radius:12px;padding:14px 16px;margin-bottom:14px}
.sub-box code{flex:1;min-width:200px;color:#FF5C39;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;word-break:break-all}
.sub-feedly{display:inline-block;margin-bottom:36px}
.sub-wrap h2{font-size:20px;margin:0 0 16px;border-left:3px solid #FF5C39;padding-left:12px}
.sub-list{display:grid;gap:14px}
.sub-ch{display:block;text-decoration:none;color:inherit;background:#16140F;border:1px solid #2a2620;border-radius:14px;padding:18px 20px;transition:.18s}
.sub-ch:hover{border-color:#FF5C39;transform:translateY(-2px)}
.sub-ch-meta{color:#a79f92;font-size:12px;margin-bottom:6px}
.sub-ch h3{margin:0 0 8px;font-size:19px}
.sub-ch p{margin:0;color:#cfc7ba;font-size:15px;line-height:1.6}
.sub-back{display:inline-block;margin-top:32px;color:#FF5C39;font-weight:700;text-decoration:none;border-bottom:1px dashed #FF5C39}
</style>
</head>
<body class="page-subscribe">
<header class="site-header is-solid" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
    <nav class="nav-links"><a href="/vn" class="is-current">游戏剧本</a><a href="/quiz">浓度测试</a><a href="/videos">视频</a></nav>
  </div>
</header>
<main>
  <div class="sub-wrap">
    <p class="kicker">__KICKER__</p>
    <h1>__TITLE__</h1>
    <p class="lead">__LEAD__</p>
    <div class="sub-box">
      <code id="feedUrl">__FEEDURL__</code>
      <button class="btn btn-primary btn-sm" id="copyBtn" type="button">__COPY__</button>
    </div>
    <a class="btn btn-ghost sub-feedly" href="__FEEDLYURL__" target="_blank" rel="noopener">__FEEDLY__</a>
    <h2>__CHAPTERS__</h2>
    <div class="sub-list">
__CARDS__
    </div>
    <a class="sub-back" href="/vn">__BACK__</a>
  </div>
</main>
<script>
(function(){
  var btn=document.getElementById('copyBtn');
  if(!btn)return;
  var url=document.getElementById('feedUrl').textContent;
  function done(){btn.textContent='__COPIED__';setTimeout(function(){btn.textContent='__COPY__';},2000);}
  function fallback(){var ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.focus();ta.select();try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(ta);}
  btn.addEventListener('click',function(){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(done,function(){fallback();});}else{fallback();}});
})();
</script>
</body>
</html>"""


def build_subscribe(lang, items):
    ui = SUB_UI[lang]
    items = sorted(items, key=lambda x: (x["date"], x["slug"]))
    cards = []
    for it in reversed(items):
        cards.append(
            '<a class="sub-ch" href="/vn/%s"><div class="sub-ch-meta">%s</div>'
            '<h3>%s</h3><p>%s</p></a>'
            % (esc(it["slug"]), esc(it["date"]), esc(it["title"]), esc(it["summary"]))
        )
    feed_url = SITE + "/vn/feed.xml"
    feedly_url = "https://feedly.com/i/subscription/feed/" + feed_url
    canon = SITE + ("/vn/subscribe" if lang == "zh" else "/%s/vn/subscribe" % lang)
    return (SUB_TPL
            .replace("__LANGLANG__", {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}[lang])
            .replace("__KICKER__", ui["kicker"])
            .replace("__TITLE__", ui["title"])
            .replace("__LEAD__", ui["lead"])
            .replace("__COPY__", ui["copy"])
            .replace("__COPIED__", ui["copied"])
            .replace("__FEEDLY__", ui["feedly"])
            .replace("__CHAPTERS__", ui["chapters"])
            .replace("__BACK__", ui["back"])
            .replace("__FEEDURL__", feed_url)
            .replace("__FEEDLYURL__", feedly_url)
            .replace("__CANON__", canon)
            .replace("__CARDS__", "\n".join(cards)))


def main():
    folder = os.path.join(BASE, "content", "vn")
    items = []
    for path in sorted(glob.glob(os.path.join(folder, "*.md"))):
        with open(path, encoding="utf-8") as f:
            meta = parse_frontmatter(f.read())
        items.append({
            "slug": os.path.splitext(os.path.basename(path))[0],
            "title": meta.get("title", ""),
            "date": meta.get("date", ""),
            "summary": meta.get("summary", ""),
        })

    out_zh = os.path.join(BASE, "vn", "feed.xml")
    with open(out_zh, "w", encoding="utf-8") as f:
        f.write(build(items))
    print("wrote", out_zh)

    out_en = os.path.join(BASE, "en", "vn", "feed.xml")
    os.makedirs(os.path.dirname(out_en), exist_ok=True)
    with open(out_en, "w", encoding="utf-8") as f:
        f.write(build(items))
    print("wrote", out_en)

    # 追更落地页（真正的 HTML，不依赖浏览器 XSLT）
    for lang in ("zh", "en", "ja", "ko"):
        out_html = os.path.join(BASE, lang, "vn", "subscribe.html") if lang != "zh" \
            else os.path.join(BASE, "vn", "subscribe.html")
        os.makedirs(os.path.dirname(out_html), exist_ok=True)
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(build_subscribe(lang, items))
        print("wrote", out_html)


if __name__ == "__main__":
    main()
