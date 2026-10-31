# -*- coding: utf-8 -*-
"""
gen_concentration.py — 生成「体育生浓度分布」原创数据页（AI 引用硬通货）

复用 gen_result_pages 的 SIGNATURE / SHADOW / TYPES / DATA，保证与 quiz 同步。
产物：
  /concentration.html  (zh)
  /en/concentration.html  /ja/concentration.html  /ko/concentration.html
  /assets/data/concentration.json  （机器可读源数据）
  sitemap.xml 重写（24 → 28 URL，新增 4 条浓度页 + hreflang 簇）

运行：python gen_concentration.py  （在 tools/ 目录）
"""
import os
import json

from gen_result_pages import (
    SITE, LANGS, LANG_TAGS, LANG_ORDER, TYPES, SIGNATURE, SHADOW, DATA,
    short_desc,
)

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# 各语言叙事文案（数据数字来自导入的 SIGNATURE/SHADOW，保持单一数据源）
NARR = {
    "zh": {
        "kicker": "荷尔蒙编辑部 · 原创数据",
        "title": "体育生浓度分布报告",
        "lead": "我们用一套 6 题量表，把「体育生」拆成四种人格，并给每种标定了一个浓度值。这不是心理测验的科学结论，而是一份带着态度的文化坐标——你可以用它快速对号入座，也可以拿去当谈资。",
        "chartTitle": "四种体育生，浓度怎么排",
        "tableTitle": "完整数据表",
        "th": ["人格", "签名浓度", "影子浓度", "一句话判词"],
        "tableNote": "签名浓度＝你属于该型的标定浓度；影子浓度＝你在其他三型上的平均残留值。浓度不是比赛，是自我对号入座的坐标。",
        "methodTitle": "这套数据怎么来的",
        "method": "SportsBoy 浓度测试 v1.0：6 道单选题，每题指向四种体育生人格之一（泳队 / 篮球 / 健身房 / 全能）。系统按选择聚合出你的主型，并给出主型签名浓度与其余三型的影子浓度。本页数据为该测试体系的标定参考值，由荷尔蒙编辑部基于圈层观察校准，仅作娱乐与文化讨论之用。",
        "ctaTitle": "你是哪一型？",
        "ctaSub": "6 道题，30 秒，生成你的人格图鉴。",
        "ctaBtn": "开始测试",
        "quizLabel": "浓度测试",
        "navCta": "免费读《体育生》",
        "footerNote": "BL 内容 · 角色全部成年设定",
        "langLabel": "中文",
        "datasetName": "SportsBoy 体育生浓度分布模型 v1.0",
        "ldDesc": "四种体育生人格（泳队/篮球/健身房/全能）的标定签名浓度与影子浓度，来自 SportsBoy 6 题浓度测试体系。",
    },
    "en": {
        "kicker": "By the Hormone Desk · Original Data",
        "title": "The Jock Concentration Report",
        "lead": "We took a 6-question scale, broke \"jock\" into four personality types, and gave each a concentration value. This isn't a scientific psychology finding — it's a cultural coordinate with attitude. Use it to place yourself, or as conversation fuel.",
        "chartTitle": "Four jock types, ranked by concentration",
        "tableTitle": "Full data table",
        "th": ["Type", "Signature", "Shadow", "One-line verdict"],
        "tableNote": "Signature = your calibrated concentration for the dominant type; Shadow = your average residual in the other three. Concentration isn't a contest — it's a coordinate for self-placement.",
        "methodTitle": "How this data was built",
        "method": "SportsBoy Concentration Test v1.0: 6 single-choice questions, each pointing to one of four jock types (Swim / Hoop / Gym / All-Round). The system aggregates your picks into a dominant type and returns its signature concentration plus the three shadow values. The figures on this page are the calibration reference for that test, tuned by the Hormone Desk from community observation. For entertainment and cultural discussion only.",
        "ctaTitle": "Which type are you?",
        "ctaSub": "6 questions, 30 seconds, your own personality profile.",
        "ctaBtn": "Take the test",
        "quizLabel": "Take the test",
        "navCta": "Read free",
        "footerNote": "BL content · all characters are adults",
        "langLabel": "English",
        "datasetName": "SportsBoy Jock Concentration Model v1.0",
        "ldDesc": "Calibrated signature and shadow concentrations for four jock types (Swim/Hoop/Gym/All-Round), from the SportsBoy 6-question concentration test.",
    },
    "ja": {
        "kicker": "ホルモン編集部 · オリジナルデータ",
        "title": "体育生濃度分布レポート",
        "lead": "6問の尺度で「体育生」を4つの人格に分解し、それぞれに濃度値を割り当てた。これは心理学の科学的結論ではなく、態度を持ったカルチャーの座標だ。自分の型を当てはめるにも、話題にするにも使える。",
        "chartTitle": "4つの体育生、濃度順",
        "tableTitle": "完全データ表",
        "th": ["人格", "署名濃度", "影濃度", "一言判定"],
        "tableNote": "署名濃度＝主型の标定濃度。影濃度＝他3型への平均残留値。濃度は勝負ではなく、自分を当てはめる座標。",
        "methodTitle": "このデータの作り方",
        "method": "SportsBoy 濃度テスト v1.0：6つの単一選択式質問。各問は4つの体育生人格（水泳部／バスケ／ジム／万能）のいずれかへ紐づく。システムは選択を集計して主型を出し、その署名濃度と他3型の影濃度を返す。本ページの数値は同テストの标定参考値で、ホルモン編集部がコミュニティ観察から校准した。娯楽・カルチャー議論のためのもの。",
        "ctaTitle": "あなたはどの型？",
        "ctaSub": "6問30秒で、あなた専用の人格図鑑を。",
        "ctaBtn": "テストする",
        "quizLabel": "濃度テスト",
        "navCta": "無料で読む",
        "footerNote": "BLコンテンツ · キャラ全員成年設定",
        "langLabel": "日本語",
        "datasetName": "SportsBoy 体育生濃度分布モデル v1.0",
        "ldDesc": "4つの体育生人格（水泳部／バスケ／ジム／万能）の标定署名濃度と影濃度。SportsBoy 6問濃度テスト体系から。",
    },
    "ko": {
        "kicker": "호르몬 편집부 · 오리지널 데이터",
        "title": "스포츠맨 농도 분포 리포트",
        "lead": "6문제 척도로 '스포츠맨'을 4가지 성격으로 나누고, 각각에 농도 값을 매겼다. 이건 심리학적 과학 결론이 아니라 태도를 담은 컬처 좌표다. 자신의 형을 찾거나 화제 거리로 써먹기 좋다.",
        "chartTitle": "스포츠맨 4형, 농도 순",
        "tableTitle": "전체 데이터 표",
        "th": ["성격", "서명 농도", "그림자 농도", "한 줄 판정"],
        "tableNote": "서명 농도＝주형의 보정 농도. 그림자 농도＝나머지 3형에 대한 평균 잔류값. 농도는 승부가 아니라 자신을 둘러보는 좌표.",
        "methodTitle": "이 데이터는 어떻게 만들었나",
        "method": "SportsBoy 농도 테스트 v1.0: 6개 단일 선택 문항. 각 문항은 4가지 스포츠맨 성격(수영부/농구부/헬스/만능) 중 하나에 연결된다. 시스템은 선택을 집계해 주형을 정하고, 그 서명 농도와 나머지 3형의 그림자 농도를 반환한다. 이 페이지 수치는 해당 테스트의 보정 기준값으로, 호르몬 편집부가 커뮤니티 관찰로 조정했다. 오락 및 컬처 토론용.",
        "ctaTitle": "당신은 어느 형?",
        "ctaSub": "6문제 30초면, 당신 전용 성격 도감이.",
        "ctaBtn": "테스트하기",
        "quizLabel": "농도 테스트",
        "navCta": "무료 연재",
        "footerNote": "BL 콘텐츠 · 캐릭터 전원 성인 설정",
        "langLabel": "한국어",
        "datasetName": "SportsBoy 스포츠맨 농도 분포 모델 v1.0",
        "ldDesc": "4가지 스포츠맨 성격(수영부/농구부/헬스/만능)의 보정 서명 농도와 그림자 농도. SportsBoy 6문제 농도 테스트 체계에서.",
    },
}

CONC_SLUG = "concentration"


def conc_url(lang):
    prefix = LANGS[lang][1]
    return "%s/%s%s" % (SITE, (prefix + "/") if prefix else "", CONC_SLUG)


def ranked_types():
    return sorted(TYPES, key=lambda k: -SIGNATURE[k])


def jsonld(lang):
    dist = []
    for key in ranked_types():
        name, _desc = DATA[lang]["types"][key]
        dist.append({
            "type": key,
            "name": name,
            "signatureConcentration": SIGNATURE[key],
            "shadowConcentration": SHADOW[key],
        })
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": NARR[lang]["datasetName"],
        "description": NARR[lang]["ldDesc"],
        "creator": {"@type": "Organization", "name": "SportsBoy 荷尔蒙编辑部"},
        "datePublished": "2026-10-26",
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "distribution": {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": SITE + "/assets/data/concentration.json",
        },
        "variableMeasured": dist,
    }


def head(lang):
    html_lang, prefix, font_q, _noto = LANGS[lang]
    n = NARR[lang]
    self_url = conc_url(lang)
    alternates = []
    for l in LANG_ORDER:
        alternates.append(
            '  <link rel="alternate" hreflang="%s" href="%s">' % (LANG_TAGS[l], conc_url(l))
        )
    alternates.append('  <link rel="alternate" hreflang="x-default" href="%s">' % conc_url("zh"))
    return """<!DOCTYPE html>
<html lang="%s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="msvalidate.01" content="83a632faa92c4ae0bd1086de9dc2902a" />
<title>%s | SportsBoy.gay</title>
<meta name="description" content="%s">
<meta name="robots" content="index,follow">
<meta property="og:title" content="%s | SportsBoy.gay">
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
<script type="application/ld+json">%s</script>
</head>
<body class="page-concentration">
""" % (
        html_lang,
        n["title"],
        n["lead"][:120],
        n["title"],
        n["ldDesc"],
        SITE, self_url, self_url,
        "\n".join(alternates),
        font_q,
        json.dumps(jsonld(lang), ensure_ascii=False),
    )


NAV = {
    "zh": dict(quiz="浓度测试", videos="视频", vn="游戏剧本", novel="宇宙散文",
               know="认识男同", cols="王牌栏目", readfree="免费读《体育生》"),
    "en": dict(quiz="Vibe Test", videos="Videos", vn="Visual Novel", novel="Novel",
               know="About Gay", cols="Columns", readfree="Read free"),
    "ja": dict(quiz="濃度テスト", videos="動画", vn="ビジュアルノベル", novel="小説",
               know="ゲイ入門", cols="コラム", readfree="無料で読む"),
    "ko": dict(quiz="농도 테스트", videos="영상", vn="비주얼 노벨", novel="소설",
               know="게이 알기", cols="칼럼", readfree="무료 연재"),
}


def header(lang):
    n = NARR[lang]
    home = "/%s" % LANGS[lang][1] if LANGS[lang][1] else "/"
    nv = NAV[lang]
    vnlink = home.rstrip("/") + "/vn"
    novellink = home.rstrip("/") + "/novel"
    knowlink = home.rstrip("/") + "/knowledge"
    colslink = home.rstrip("/") + "/#columns"
    opts = []
    for l in LANG_ORDER:
        active = " is-active" if l == lang else ""
        aria = ' aria-current="true"' if l == lang else ""
        opts.append(
            '          <a class="lang-opt%s" href="%s" hreflang="%s" lang="%s"%s>%s<span class="lang-opt-tag">%s</span></a>'
            % (active, conc_url(l), LANG_TAGS[l], LANG_TAGS[l], aria, NARR[l]["langLabel"], LANG_TAGS[l].upper()[:2])
        )
    nav_html = (
        '    <nav class="nav-links">\n'
        '      <a href="%s/quiz">%s</a>\n'
        '      <a href="%s/videos">%s</a>\n'
        '      <a href="%s">%s</a>\n'
        '      <a href="%s">%s</a>\n'
        '      <a href="%s">%s</a>\n'
        '      <a href="%s">%s</a>\n'
        '      <a class="btn btn-primary btn-sm" href="%s">%s</a>\n'
        '    </nav>'
        % (home, nv["quiz"], home, nv["videos"], vnlink, nv["vn"],
           novellink, nv["novel"], knowlink, nv["know"],
           colslink, nv["cols"], vnlink, nv["readfree"])
    )
    return """
<header class="site-header is-solid" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="%s">SPORTSBOY<span class="brand-tld">.gay</span></a>
%s
    <div class="nav-side">
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
""" % (home, nav_html, n["langLabel"], "\n".join(opts))


def body(lang):
    n = NARR[lang]
    types = DATA[lang]["types"]

    # 排名条形图（复用 .quiz-bars / .quiz-bar-*）
    chart = []
    for key in ranked_types():
        is_top = (key == ranked_types()[0])
        name, _ = types[key]
        chart.append(
            '      <div class="quiz-bar-row%s"><span class="quiz-bar-label">%s</span>'
            '<div class="quiz-bar-track"><div class="quiz-bar-fill" style="width:%d%%"></div></div>'
            '<span class="quiz-bar-value">%d%%</span></div>'
            % (" is-top" if is_top else "", name, SIGNATURE[key], SIGNATURE[key])
        )

    # 数据表
    rows = []
    for key in ranked_types():
        name, desc = types[key]
        rows.append(
            '        <tr><td>%s</td><td class="conc-num">%d%%</td><td class="conc-num">%d%%</td>'
            '<td class="conc-verdict">%s</td></tr>'
            % (name, SIGNATURE[key], SHADOW[key], short_desc(desc))
        )

    return """
<main class="conc-main">
  <div class="container conc-shell">

    <p class="kicker">%s</p>
    <h1 class="conc-title">%s</h1>
    <p class="conc-lead">%s</p>

    <section class="conc-chart-block">
      <p class="conc-block-title">%s</p>
      <div class="conc-chart">
%s
      </div>
    </section>

    <section class="conc-table-block">
      <p class="conc-block-title">%s</p>
      <div class="conc-table-wrap">
        <table class="conc-table">
          <thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead>
          <tbody>
%s
          </tbody>
        </table>
      </div>
      <p class="conc-table-note">%s</p>
    </section>

    <section class="conc-method">
      <p class="conc-block-title">%s</p>
      <p>%s</p>
    </section>

    <section class="conc-cta">
      <div class="cta-band">
        <div>
          <h2>%s</h2>
          <p>%s</p>
        </div>
        <a class="btn btn-dark" href="/%squiz">%s</a>
      </div>
    </section>

  </div>
</main>
""" % (
        n["kicker"], n["title"], n["lead"],
        n["chartTitle"], "\n".join(chart),
        n["tableTitle"], n["th"][0], n["th"][1], n["th"][2], n["th"][3],
        "\n".join(rows),
        n["tableNote"],
        n["methodTitle"], n["method"],
        n["ctaTitle"], n["ctaSub"],
        (LANGS[lang][1] + "/") if LANGS[lang][1] else "",
        n["ctaBtn"],
    )


def footer(lang):
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
""" % NARR[lang]["footerNote"]


def gen_page(lang):
    return head(lang) + header(lang) + body(lang) + footer(lang)


def write_json():
    out = {"schema_version": "1.0", "datePublished": "2026-10-26"}
    for lang in LANG_ORDER:
        out[lang] = {
            "name": NARR[lang]["datasetName"],
            "description": NARR[lang]["ldDesc"],
            "types": [
                {
                    "key": key,
                    "name": DATA[lang]["types"][key][0],
                    "signature": SIGNATURE[key],
                    "shadow": SHADOW[key],
                    "verdict": short_desc(DATA[lang]["types"][key][1]),
                }
                for key in ranked_types()
            ],
        }
    path = os.path.join(ROOT, "assets", "data", "concentration.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return path


def add_to_sitemap():
    """在 gen_result_pages 生成的 24 URL sitemap 基础上，追加 4 条浓度页（含 hreflang 簇）。幂等。"""
    import gen_result_pages as grp
    grp.main()  # 刷新 16 结果页 + 24 URL sitemap，保证与 quiz 同步

    sp = os.path.join(ROOT, "sitemap.xml")
    with open(sp, "r", encoding="utf-8") as f:
        content = f.read()
    if "/concentration" in content:
        return sp, "already present"

    cluster = [(l, conc_url(l)) for l in LANG_ORDER]
    blocks = []
    for l, url in cluster:
        lines = ['    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (LANG_TAGS[ll], conc_url(ll)) for ll in LANG_ORDER]
        lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % conc_url("zh"))
        blocks.append("  <url>\n    <loc>%s</loc>\n%s\n  </url>" % (url, "\n".join(lines)))
    inject = "\n".join(blocks) + "\n</urlset>\n"
    content = content.replace("</urlset>", inject)
    with open(sp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return sp, "appended 4 urls"


def main():
    count = 0
    for lang in LANG_ORDER:
        prefix = LANGS[lang][1]
        out_dir = os.path.join(ROOT, prefix, CONC_SLUG) if prefix else os.path.join(ROOT, CONC_SLUG)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "index.html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(gen_page(lang))
        count += 1
        print("generated:", os.path.relpath(path, ROOT))
    jp = write_json()
    print("json written:", os.path.relpath(jp, ROOT))
    sp, msg = add_to_sitemap()
    print("sitemap:", os.path.relpath(sp, ROOT), "(" + msg + ")")
    print("done. %d concentration pages." % count)


if __name__ == "__main__":
    main()
