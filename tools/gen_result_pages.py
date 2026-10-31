# -*- coding: utf-8 -*-
"""
gen_result_pages.py — 生成 quiz 人格结果分享页（程序化获客）+ 重写 sitemap.xml

输出（16 页）：
  /quiz/result/{swim,basketball,gym,allround}.html
  /en/quiz/result/...  /ja/quiz/result/...  /ko/quiz/result/...

每个页面：
  - index,follow（可索引），canonical 自指，hreflang 四语互指 + x-default（指中文版）
  - og 文案独立："我的结果是泳队体育生 · 浓度 87%"
  - 页面即广告：人格判词 + 浓度分布 + "测测你的浓度" CTA
  - 纯静态无 JS 依赖（main.js 仅用于语言下拉/SW）

数据源与 assets/js/quiz.js 的 I18N.types 保持一致；改动需两边同步。
"""
import os
import html

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = "https://www.sportsboy.gay"

# 语言 → (html lang, 目录前缀, 字体 query, Noto 家族)
LANGS = {
    "zh": ("zh-CN", "", "family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900", "Noto Sans SC"),
    "en": ("en", "en", "family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900", "Noto Sans SC"),
    "ja": ("ja", "ja", "family=Archivo+Black&family=Noto+Sans+JP:wght@400;500;700;900", "Noto Sans JP"),
    "ko": ("ko", "ko", "family=Archivo+Black&family=Noto+Sans+KR:wght@400;500;700;900", "Noto Sans KR"),
}

TYPES = ["swim", "basketball", "gym", "allround"]

# 每种人格的展示用签名浓度（页面 H1/og 用）与非高亮时的影子值（分布图用）
SIGNATURE = {"swim": 87, "basketball": 91, "gym": 84, "allround": 89}
SHADOW = {"swim": 68, "basketball": 74, "gym": 65, "allround": 72}

# 四语 × 四人格 数据（name/desc 与 quiz.js 保持一致）
DATA = {
    "zh": {
        "types": {
            "swim": ("泳队体育生", "水感天赋型。别人出汗靠练，你出汗靠下水。泳裤晾哪、白袜配什么鞋，是你认真研究的学术问题。泳池就是你的主场，湿身是你的被动技能。"),
            "basketball": ("篮球体育生", "弹跳与汗碱型。球鞋收藏家的自我修养，半场球衣就能透。护踝比对象亲，斗牛时嘴上说着随便打，心里记着每一次被盖。"),
            "gym": ("健身房体育生", "蛋白粉驱动型。体脂率是你的人生 KPI，镜子前的第 108 次展背依然充满热情。组间休息不忘补水，训练计划比恋爱计划详细。"),
            "allround": ("全能体育生", "什么都玩型。操场、球场、泳池、健身房，四处都有你的传说。天赋不知道点在哪，但浓度从来不掉线——真正的体育生，敢于全部都要。"),
        },
        "ui": {
            "kicker": "荷尔蒙编辑部出品 · 浓度测试结果",
            "barsTitle": "浓度分布",
            "ctaPrimary": "测测你的浓度",
            "ctaSecondary": "免费读《体育生》",
            "shareNote": "复制下面的链接发给队友，让他也来对号入座：",
            "shareHint": "已复制，去发给队友吧",
            "concLink": "查看四种体育生浓度分布 →",
            "navBack": "返回首页",
            "navCta": "免费读《体育生》",
            "footerNote": "BL 内容 · 角色全部成年设定",
            "titleTpl": "{name} · 浓度 {p}% — 体育生浓度测试 | SportsBoy.gay",
            "descTpl": "测出你是{name}：{desc_short}来 SportsBoy.gay 做体育生浓度测试，6 道题 30 秒，生成你的人格图鉴。",
            "ogTitleTpl": "我的结果是{name} · 浓度 {p}%",
            "ogDescTpl": "{name}——{desc_short}你来测测自己的浓度。",
            "shareBtn": "分享我的身份卡",
            "peersLabel": "你的同型体育生，都在追《体育生》",
            "langLabel": "中文",
        },
    },
    "en": {
        "types": {
            "swim": ("Swim Jock", "Water-native. Other people sweat to train; you sweat to swim. Where the speedos dry and which shoes go with white socks — you treat both as serious research. The pool is your home turf; being soaked is your passive skill."),
            "basketball": ("Hoop Jock", "Vertical and salt-stained. A sneaker collector's self-cultivation; a half-court jersey goes see-through. Closer to your ankle brace than to your situationship. In 1v1s you say \"whatever\" out loud and remember every single poster."),
            "gym": ("Gym Jock", "Protein-powder driven. Body-fat percentage is your life KPI; back pose #108 in the mirror still fills you with passion. Hydrate between sets. Your training plan is far more detailed than your dating plan."),
            "allround": ("All-Round Jock", "Plays everything. Track, court, pool, gym — legends of you everywhere. You never knew where to spend the talent points, but the concentration never drops. A real jock dares to want it all."),
        },
        "ui": {
            "kicker": "By the Hormone Desk · Test Result",
            "barsTitle": "Concentration breakdown",
            "ctaPrimary": "Take the test",
            "ctaSecondary": "Read free",
            "shareNote": "Copy the link below and send it to your teammate — make him find his type too:",
            "shareHint": "Copied — go send it to your teammate",
            "concLink": "See the full concentration report →",
            "navBack": "Back home",
            "navCta": "Read free",
            "footerNote": "BL content · all characters are adults",
            "titleTpl": "{name} · {p}% Concentration — Jock Concentration Test | SportsBoy.gay",
            "descTpl": "You tested as {name}: {desc_short} Take the 6-question, 30-second jock concentration test at SportsBoy.gay.",
            "ogTitleTpl": "My result: {name} · {p}% Concentration",
            "ogDescTpl": "{name} — {desc_short} Come test your own concentration.",
            "shareBtn": "Share my card",
            "peersLabel": "Your kind of jock is already reading it",
            "langLabel": "English",
        },
    },
    "ja": {
        "types": {
            "swim": ("水泳部体育生", "水感天赋型。他人は汗を流して鍛える、あなたは水に入って汗をかく。競パンの干し場所、白ソックスに合わせる靴——真面目に研究する学问だ。プールはあなたの主场、濡れるのは被动スキル。"),
            "basketball": ("バスケ体育生", "跳跃と汗塩型。スニーカーコレクターのたしなみ、ハーフのユニフォームはもう透ける。サポーターは恋人より近い。1v1では口で「适当にやる」と言いながら、ブロックされた数を全部覚えている。"),
            "gym": ("ジム体育生", "プロテイン驱动型。体脂肪率が人生のKPI、镜の前で108回目の背面ポーズも依然情热満々。セット间の补水は欠かさない。トレーニング計画は恋爱計画より详细。"),
            "allround": ("万能体育生", "何でもこなす型。グラウンド、コート、プール、ジム——四处にあなたの伝说が。天赋の振り先は不明、でも浓度は一度も离线したことがない。本当の体育生は、全部欲しがる勇气を持つ。"),
        },
        "ui": {
            "kicker": "ホルモン编集部 · 浓度テスト结果",
            "barsTitle": "浓度分布",
            "ctaPrimary": "濃度を测ってみる",
            "ctaSecondary": "無料で読む",
            "shareNote": "下のリンクをコピーして队友に送り、同じテストをさせよう：",
            "shareHint": "コピーしました — 队友に送ろう",
            "concLink": "4つの体育生の濃度分布を見る →",
            "navBack": "ホームへ戻る",
            "navCta": "無料で読む",
            "footerNote": "BLコンテンツ · キャラ全員成年設定",
            "titleTpl": "{name} · 浓度 {p}% — 体育生浓度テスト | SportsBoy.gay",
            "descTpl": "あなたの结果は{name}：{desc_short}SportsBoy.gay の体育生浓度テスト、6问30秒で人格図鉴を生成。",
            "ogTitleTpl": "私の结果は{name} · 浓度 {p}%",
            "ogDescTpl": "{name}——{desc_short}あなたの浓度も测ってみて。",
            "shareBtn": "身分カードをシェア",
            "peersLabel": "あなたと同型の体育生はみんな読んでる",
            "langLabel": "日本語",
        },
    },
    "ko": {
        "types": {
            "swim": ("수영부 스포츠맨", "물속 천재형. 남들은 운동해서 땀 흘리고, 너는 물에 들어가서 땀 흘린다. 수영복 말리는 위치, 흰 양말에 어울리는 신발 — 진지하게 연구하는 학문 문제. 풀은 너의 홈그라운드, 젖는 건 패시브 스킬."),
            "basketball": ("농구부 스포츠맨", "점프와 소금 각질형. 농구화 컬렉터의 자기 수양, 하프코트 유니폼은 벌써 비친다. 발목 보호대가 연인보다 가깝다. 1대1에서는 입으로 '아무거나' 하면서 블록당한 횟수를 전부 기억한다."),
            "gym": ("헬스 스포츠맨", "프로틴 구동형. 체지방률이 인생 KPI, 거울 앞 108번째 백 포즈도 여전히 열정 가득. 세트 사이 수분 보충은 필수, 운동 계획이 연애 계획보다 상세하다."),
            "allround": ("만능 스포츠맨", "무엇이든 하는형. 운동장, 코트, 풀, 헬스 — 사방에 너의 전설이 있다. 재능 포인트를 어디 찍었는지는 모르지만 농도는 한 번도 떨어진 적 없다. 진짜 스포츠맨은 전부 가질 용기가 있다."),
        },
        "ui": {
            "kicker": "호르몬 편집부 · 농도 테스트 결과",
            "barsTitle": "농도 분포",
            "ctaPrimary": "농도 측정해보기",
            "ctaSecondary": "무료 연재",
            "shareNote": "아래 링크를 복사해 팀메이트에게 보내, 같은 테스트를 하게 하자:",
            "shareHint": "복사됨 — 팀메이트에게 보내자",
            "concLink": "스포츠맨 농도 분포 보기 →",
            "navBack": "홈으로 돌아가기",
            "navCta": "무료 연재",
            "footerNote": "BL 콘텐츠 · 캐릭터 전원 성인 설정",
            "titleTpl": "{name} · 농도 {p}% — 스포츠맨 농도 테스트 | SportsBoy.gay",
            "descTpl": "당신의 결과는 {name}: {desc_short} SportsBoy.gay 에서 6문제 30초 스포츠맨 농도 테스트를 해보세요.",
            "ogTitleTpl": "내 결과는 {name} · 농도 {p}%",
            "ogDescTpl": "{name} — {desc_short} 당신의 농도도 측정해보세요.",
            "shareBtn": "내 카드 공유",
            "peersLabel": "같은 타입의 스포츠맨은 이미 읽고 있어",
            "langLabel": "한국어",
        },
    },
}

LANG_TAGS = {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}
LANG_ORDER = ["zh", "en", "ja", "ko"]


def short_desc(desc):
    """og/description 用短判词：取第一句，截断到 60 字符。"""
    first = re_split_sentence(desc)
    return first if len(first) <= 60 else first[:57] + "…"


def re_split_sentence(text):
    for sep in ("。", ".", "！", "!"):
        idx = text.find(sep)
        if idx != -1:
            return text[: idx + 1]
    return text


def page_url(lang, t):
    prefix = LANGS[lang][1]
    return "%s/%squiz/result/%s" % (SITE, (prefix + "/") if prefix else "", t)


def share_url(lang, t):
    """结果页分享链接：指向 quiz 中枢，自动带 share UTM（campaign=人格类型），让分享带来的人也能归因。"""
    prefix = LANGS[lang][1]
    path = "/%squiz" % ((prefix + "/") if prefix else "")
    return "%s%s?utm_source=share&utm_medium=referral&utm_campaign=%s" % (SITE, path, t)


def head(lang, t):
    html_lang, prefix, font_q, _noto = LANGS[lang]
    ui = DATA[lang]["ui"]
    name, desc = DATA[lang]["types"][t]
    p = SIGNATURE[t]
    self_url = page_url(lang, t)
    alternates = []
    for l in LANG_ORDER:
        alternates.append(
            '  <link rel="alternate" hreflang="%s" href="%s">' % (LANG_TAGS[l], page_url(l, t))
        )
    alternates.append('  <link rel="alternate" hreflang="x-default" href="%s">' % page_url("zh", t))
    return """<!DOCTYPE html>
<html lang="%s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="msvalidate.01" content="83a632faa92c4ae0bd1086de9dc2902a" />
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="index,follow">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="%s/assets/img/og.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="%s">
<meta name="theme-color" content="#0E0D0B">
<link rel="icon" href="/assets/img/icon-512.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<link rel="canonical" href="%s">
%s
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?%s&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="page-quiz">
""" % (
        html_lang,
        ui["titleTpl"].format(name=name, p=p),
        ui["descTpl"].format(name=name, desc_short=short_desc(desc)),
        ui["ogTitleTpl"].format(name=name, p=p),
        ui["ogDescTpl"].format(name=name, desc_short=short_desc(desc)),
        SITE, self_url, self_url,
        "\n".join(alternates),
        font_q,
    )


def header(lang, t):
    ui = DATA[lang]["ui"]
    home = "/%s" % LANGS[lang][1] if LANGS[lang][1] else "/"
    quiz = "/%squiz" % ((LANGS[lang][1] + "/") if LANGS[lang][1] else "")
    vnlink = home.rstrip("/") + "/vn"
    opts = []
    for l in LANG_ORDER:
        active = " is-active" if l == lang else ""
        aria = ' aria-current="true"' if l == lang else ""
        opts.append(
            '          <a class="lang-opt%s" href="%s" hreflang="%s" lang="%s"%s>%s<span class="lang-opt-tag">%s</span></a>'
            % (active, page_url(l, t), LANG_TAGS[l], LANG_TAGS[l], aria, DATA[l]["ui"]["langLabel"], LANG_TAGS[l].upper()[:2])
        )
    return """
<header class="site-header is-solid" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="%s">SPORTSBOY<span class="brand-tld">.gay</span></a>
    <nav class="nav-links">
      <a href="%s">%s</a>
      <a class="btn btn-primary btn-sm" href="%s">%s</a>
    </nav>
    <div class="nav-side">
      <div class="lang-menu-wrap">
        <button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="langMenu">
          <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
            <circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>
            <path d="M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/>
          </svg>
          <span>%s</span>
        </button>
        <div class="lang-menu" id="langMenu" hidden>
%s
        </div>
      </div>
    </div>
  </div>
</header>
""" % (home, home, ui["navBack"], vnlink, ui["navCta"], ui["langLabel"], "\n".join(opts))


def result_section(lang, t):
    ui = DATA[lang]["ui"]
    types = DATA[lang]["types"]
    p = SIGNATURE[t]
    name, desc = types[t]
    surl_esc = html.escape(share_url(lang, t))
    bars = []
    for key in TYPES:
        value = SIGNATURE[key] if key == t else SHADOW[key]
        top = " is-top" if key == t else ""
        bars.append(
            '        <div class="quiz-bar-row%s"><span class="quiz-bar-label">%s</span>'
            '<div class="quiz-bar-track"><div class="quiz-bar-fill" style="width:%d%%"></div></div>'
            '<span class="quiz-bar-value">%d%%</span></div>'
            % (top, types[key][0], value, value)
        )
    quiz = "/%squiz" % ((LANGS[lang][1] + "/") if LANGS[lang][1] else "")
    conc = "/%sconcentration" % ((LANGS[lang][1] + "/") if LANGS[lang][1] else "")
    vnlink = "/%svn" % ((LANGS[lang][1] + "/") if LANGS[lang][1] else "")
    conc_label = "浓度" if lang in ("zh", "ja") else ("농도" if lang == "ko" else "Concentration")
    return """
<main class="quiz-main">
  <div class="container quiz-shell">

    <section class="quiz-panel is-active" id="quizResult">
      <div class="quiz-card">
        <p class="kicker">%s</p>
        <h1 class="quiz-result-title">%s · %s %d%%</h1>
        <p class="quiz-result-desc">%s</p>
      </div>
      <p class="quiz-bars-title">%s</p>
      <div class="quiz-bars">
%s
      </div>
      <div class="quiz-share">
        <p class="quiz-share-label">%s</p>
        <div class="quiz-share-row">
          <button class="btn btn-primary btn-sm" id="shareBtn" type="button" data-share="%s">%s</button>
          <div class="quiz-share-text" id="shareText" role="button" tabindex="0" data-share="%s" title="%s">%s</div>
        </div>
        <p class="quiz-share-hint" id="shareHint" hidden>%s</p>
      </div>
      <script>
      (function(){
        var box=document.getElementById('shareText');
        var btn=document.getElementById('shareBtn');
        var hint=document.getElementById('shareHint');
        if(!box)return;
        function done(){ if(hint){hint.hidden=false; setTimeout(function(){hint.hidden=true;},2600);} }
        function fallback(url){ try{ var ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.opacity='0'; document.body.appendChild(ta);ta.focus();ta.select();document.execCommand('copy');document.body.removeChild(ta);}catch(e){} }
        function copy(url){ if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(url).then(done,function(){fallback(url);done();}); } else { fallback(url); done(); } }
        function share(url){ if(navigator.share){ navigator.share({title:document.title,url:url}).then(function(){},function(){}); } else { copy(url); } }
        if(btn){ btn.addEventListener('click',function(){ share(btn.getAttribute('data-share')); }); }
        box.addEventListener('click',function(){ copy(box.getAttribute('data-share')); });
        box.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); copy(box.getAttribute('data-share')); } });
      })();
      </script>
      <div class="quiz-actions">
        <a class="btn btn-primary" href="%s">%s</a>
        <a class="btn btn-ghost" href="%s">%s</a>
      </div>
      <p class="quiz-peers">%s <a href="%s">%s</a></p>
      <a class="quiz-result-page-link" href="%s">%s</a>
    </section>

  </div>
</main>
""" % (
        ui["kicker"],
        name, conc_label, p,
        desc,
        ui["barsTitle"],
        "\n".join(bars),
        ui["shareNote"], surl_esc, ui["shareBtn"], surl_esc, surl_esc, surl_esc, ui["shareHint"],
        quiz, ui["ctaPrimary"], vnlink, ui["ctaSecondary"],
        ui["peersLabel"], vnlink, ui["ctaSecondary"],
        conc, ui["concLink"],
    )


def footer(lang):
    ui = DATA[lang]["ui"]
    return """
<footer class="site-footer">
  <div class="container">
    <div class="footer-bottom">
      <p>© <span id="year">2026</span> SportsBoy.gay</p>
      <p>%s</p>
    </div>
  </div>
</footer>

<script src="/assets/js/main.js"></script>
</body>
</html>
""" % ui["footerNote"]


def gen_page(lang, t):
    return head(lang, t) + header(lang, t) + result_section(lang, t) + footer(lang)


def gen_sitemap():
    """8 基础页 + 16 结果页 + N 图鉴栏目文（中文单语），每个 URL 带完整 hreflang 簇。"""
    base_pages = ["/", "/en", "/ja", "/ko", "/quiz", "/en/quiz", "/ja/quiz", "/ko/quiz"]
    result_pages = [page_url(l, t).replace(SITE, "") for l in LANG_ORDER for t in TYPES]
    # 图鉴栏目文：中文单语，只挂 zh-CN + x-default（无 EN/JA/KO 版本）
    almanac_pages = [
        "/almanac/swim-jock", "/almanac/white-sock", "/almanac/locker-room",
        "/almanac/fake-jock", "/almanac/basketball",
    ]

    def alternates_for(url):
        # 同一 hreflang 簇：基础页按目录聚合，结果页按 type 聚合
        if "/quiz/result/" in url:
            t = url.rsplit("/", 1)[-1]
            cluster = [page_url(l, t).replace(SITE, "") for l in LANG_ORDER]
        elif url.endswith("/quiz"):
            cluster = ["/quiz", "/en/quiz", "/ja/quiz", "/ko/quiz"]
        elif "/almanac/" in url:
            return ('    <xhtml:link rel="alternate" hreflang="zh-CN" href="%s%s"/>\n'
                    '    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>') % (SITE, url, SITE, url)
        else:
            cluster = ["/", "/en", "/ja", "/ko"]
        lines = []
        for c, l in zip(cluster, LANG_ORDER):
            lines.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (LANG_TAGS[l], SITE, c))
        lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, cluster[0]))
        return "\n".join(lines)

    blocks = []
    for url in base_pages + result_pages + almanac_pages:
        blocks.append("  <url>\n    <loc>%s%s</loc>\n%s\n  </url>" % (SITE, url, alternates_for(url)))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(blocks)
        + "\n</urlset>\n"
    )


def main():
    count = 0
    for lang in LANG_ORDER:
        prefix = LANGS[lang][1]
        out_dir = os.path.join(ROOT, prefix, "quiz", "result") if prefix else os.path.join(ROOT, "quiz", "result")
        os.makedirs(out_dir, exist_ok=True)
        for t in TYPES:
            path = os.path.join(out_dir, "%s.html" % t)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(gen_page(lang, t))
            count += 1
            print("generated:", os.path.relpath(path, ROOT))

    # 注意：本脚本不再重写 sitemap.xml —— 旧逻辑会把整份 sitemap 覆盖成仅 29 条，
    # 丢失 vn/novel/knowledge/almanac/privacy/videos 等 URL。sitemap 由 gen_serial.py
    # 与已提交的版本统一维护；16 个结果页早已登记在那 55 条 sitemap 中。
    print("done. %d result pages (sitemap.xml left untouched)." % count)


if __name__ == "__main__":
    main()
