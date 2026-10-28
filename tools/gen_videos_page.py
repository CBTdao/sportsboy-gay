# -*- coding: utf-8 -*-
"""gen_videos_page.py — 生成四语 /videos 频道页（嵌入 YouTube 频道 + 订阅 + 精选 Shorts + quiz CTA）

频道 ID 来自用户输入：UCw0gqeiGnH_vMeSxGQlBwvw
放置：/videos, /en/videos, /ja/videos, /ko/videos
"""
import os

SITE = "https://www.sportsboy.gay"
CHANNEL = "UCw0gqeiGnH_vMeSxGQlBwvw"
BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"

TPL = """<!DOCTYPE html>
<html lang="__HTMLLANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:image" content="__SITE__/assets/img/og.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="__OGURL__">
<meta name="theme-color" content="#0E0D0B">
<link rel="icon" href="/assets/img/icon-512.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<link rel="canonical" href="__OGURL__">
<link rel="alternate" hreflang="zh-CN" href="__SITE__/videos">
<link rel="alternate" hreflang="en" href="__SITE__/en/videos">
<link rel="alternate" hreflang="ja" href="__SITE__/ja/videos">
<link rel="alternate" hreflang="ko" href="__SITE__/ko/videos">
<link rel="alternate" hreflang="x-default" href="__SITE__/videos">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"WebSite", "name":"SportsBoy.gay", "url":"__OGURL__", "inLanguage":"__HTMLLANG__", "description":"__DESC__", "publisher":{ "@type":"Organization", "name":"SportsBoy.gay", "url":"__SITE__/" } }
</script>
</head>
<body>

<header class="site-header" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
    <nav class="nav-links" id="navLinks">
      <a href="#columns">王牌栏目</a>
      <a href="#work">首部作品</a>
      <a href="#flywheel">宇宙</a>
      <a href="/quiz">浓度测试</a>
      <a href="/concentration">浓度分布</a>
      <a href="__VURL__" class="is-current">__NAVVID__</a>
      <a class="btn btn-primary btn-sm" href="#join">等 demo 上线</a>
    </nav>
    <div class="nav-side">
      <div class="lang-menu-wrap">
        <button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="langMenu">
          <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
            <circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>
            <path d="M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/>
          </svg>
          <span>__LANGLABEL__</span>
        </button>
        <div class="lang-menu" id="langMenu" hidden>
          <a class="lang-opt __ACTIVE_ZH__" href="/videos" hreflang="zh-CN" lang="zh-CN" aria-current="true">中文<span class="lang-opt-tag">ZH</span></a>
          <a class="lang-opt __ACTIVE_EN__" href="/en/videos" hreflang="en" lang="en">English<span class="lang-opt-tag">EN</span></a>
          <a class="lang-opt __ACTIVE_JA__" href="/ja/videos" hreflang="ja" lang="ja">日本語<span class="lang-opt-tag">JA</span></a>
          <a class="lang-opt __ACTIVE_KO__" href="/ko/videos" hreflang="ko" lang="ko">한국어<span class="lang-opt-tag">KO</span></a>
        </div>
      </div>
      <button class="nav-toggle" aria-label="打开菜单" aria-expanded="false" aria-controls="navLinks">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<main>
<section class="block" style="padding-top:140px">
  <div class="container">
    <div class="section-head reveal">
      <p class="section-index">__SECTIONIDX__</p>
      <h2>__H2__</h2>
      <p class="section-desc">__SECDESC__</p>
    </div>
    <div style="position:relative;width:100%;max-width:960px;margin:24px auto 0;aspect-ratio:16/9;background:#000;border-radius:14px;overflow:hidden">
      <iframe src="https://www.youtube.com/embed?listType=channel&amp;list=__CHANNEL__" title="SportsBoy YouTube channel" loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen
        style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
    </div>
    <div class="hero-ctas" style="justify-content:center;margin-top:24px">
      <a class="btn btn-primary" href="https://www.youtube.com/@sportsboygay?sub_confirmation=1" target="_blank" rel="noopener">&#9654; __SUB__</a>
    </div>
    <div class="cards" style="margin-top:48px">
      <a class="card reveal" href="https://www.youtube.com/watch?v=zt0PQeRFJkc&amp;utm_source=sportsboy&amp;utm_medium=site&amp;utm_campaign=videos" target="_blank" rel="noopener">
        <p class="card-num">01</p>
        <h3>__F1T__</h3>
        <p>__F1D__</p>
        <p class="card-go">__WATCH__ &rarr;</p>
      </a>
      <a class="card reveal" href="https://www.youtube.com/watch?v=zjlhX0jBhbE&amp;utm_source=sportsboy&amp;utm_medium=site&amp;utm_campaign=videos" target="_blank" rel="noopener">
        <p class="card-num">02</p>
        <h3>__F2T__</h3>
        <p>__F2D__</p>
        <p class="card-go">__WATCH__ &rarr;</p>
      </a>
    </div>
    <p class="hero-meta" style="text-align:center;margin-top:32px">__AINOTE__</p>
  </div>
</section>

<section class="block block-alt" id="quiz-cta">
  <div class="container">
    <div class="cta-band reveal">
      <div>
        <h2>__QH2__</h2>
        <p>__QD__</p>
      </div>
      <a class="btn btn-dark" href="/quiz?utm_source=sportsboy&amp;utm_medium=site&amp;utm_campaign=videos">__QB__</a>
    </div>
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
        <p>汗水、肌肉与骄傲，光明正大。</p>
      </div>
      <div class="footer-col">
        <h4>站点</h4>
        <a href="#columns">王牌栏目</a>
        <a href="#work">首部作品</a>
        <a href="/quiz">浓度测试</a>
        <a href="/concentration">浓度分布</a>
        <a href="__VURL__">__NAVVID__</a>
      </div>
      <div class="footer-col">
        <h4>社区</h4>
        <a href="https://www.youtube.com/@sportsboygay" target="_blank" rel="noopener">__FOOTER_YT__</a>
        <a href="#" data-todo="itch.io 页面待 demo 上线后开通">itch.io</a>
        <a href="#" data-todo="社交账号待开通">TikTok / X</a>
      </div>
      <div class="footer-col">
        <h4>说明</h4>
        <p>本站含 BL 向内容，角色均为成年人设定。</p>
        <p>内容为虚构创作。</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="year">2026</span> SportsBoy.gay</p>
      <p>Hosted on Vercel</p>
    </div>
  </div>
</footer>

<script src="/assets/js/main.js"></script>
</body>
</html>
"""

LANGS = {
    "zh": {
        "HTMLLANG": "zh-CN", "LANGLABEL": "中文", "NAVVID": "视频",
        "TITLE": "SportsBoy.gay — 视频频道", "VURL": "/videos", "CANON": "/videos",
        "DESC": "在 YouTube 追更 SportsBoy：体育生图鉴、浓度测试、短剧切片，每周新作不漏。",
        "SECTIONIDX": "05 / 视频", "H2": "在 YouTube 追更 SportsBoy",
        "SECDESC": "体育生图鉴、浓度测试、短剧切片——都先在这里更新。订阅频道，每周新作不漏。",
        "SUB": "订阅频道 @sportsboygay",
        "F1T": "浓度测试 Shorts", "F1D": "第一条短片：测测你有多体育生。",
        "F2T": "篮球体育生图鉴", "F2D": "把篮球生从「基圈天菜」模板里请出来。",
        "WATCH": "去 YouTube 看", "AINOTE": "视频由 AI 辅助创作 · 角色均为成年人设定",
        "QH2": "测测你的体育生浓度", "QD": "6 道题，30 秒，生成专属人格图鉴——可分享。", "QB": "开始测试",
        "FOOTER_YT": "YouTube",
    },
    "en": {
        "HTMLLANG": "en", "LANGLABEL": "English", "NAVVID": "Videos",
        "TITLE": "SportsBoy.gay — Videos", "VURL": "/en/videos", "CANON": "/en/videos",
        "DESC": "Follow SportsBoy on YouTube: jock field guides, the vibe test, short-drama clips — updated here first.",
        "SECTIONIDX": "05 / VIDEOS", "H2": "Follow SportsBoy on YouTube",
        "SECDESC": "Jock field guides, vibe test, short-drama clips — all updated here first. Subscribe so you never miss a drop.",
        "SUB": "Subscribe @sportsboygay",
        "F1T": "Vibe Test Shorts", "F1D": "Episode one: how jock are you?",
        "F2T": "Basketball Jock Guide", "F2D": "Take the baller out of the template.",
        "WATCH": "Watch on YouTube", "AINOTE": "Videos AI-assisted · all characters adults",
        "QH2": "Test your jock vibe", "QD": "6 questions, 30 seconds, get your shareable persona chart.", "QB": "Start the test",
        "FOOTER_YT": "YouTube",
    },
    "ja": {
        "HTMLLANG": "ja", "LANGLABEL": "日本語", "NAVVID": "動画",
        "TITLE": "SportsBoy.gay — 動画", "VURL": "/ja/videos", "CANON": "/ja/videos",
        "DESC": "SportsBoyをYouTubeで：体育生図鑑、濃度テスト、ショートドラマ。",
        "SECTIONIDX": "05 / 動画", "H2": "SportsBoyをYouTubeでフォロー",
        "SECDESC": "体育生図鑑、濃度テスト、ショートドラマ——まずここで更新。チャンネル登録で新作を見逃さず。",
        "SUB": "チャンネル登録 @sportsboygay",
        "F1T": "濃度テスト Shorts", "F1D": "第1弾：あなたはどれだけ体育生？",
        "F2T": "バスケ体育生図鑑", "F2D": "テンプレートから外すバスケ男子。",
        "WATCH": "YouTubeで見る", "AINOTE": "動画はAI補助制作・全キャラ成人設定",
        "QH2": "あなたの体育生濃度を診断", "QD": "6問、30秒、あなた専用の診断チャートをシェア可能。", "QB": "診断する",
        "FOOTER_YT": "YouTube",
    },
    "ko": {
        "HTMLLANG": "ko", "LANGLABEL": "한국어", "NAVVID": "영상",
        "TITLE": "SportsBoy.gay — 영상", "VURL": "/ko/videos", "CANON": "/ko/videos",
        "DESC": "SportsBoy를 YouTube에서: 운동선수 필드 가이드, 농도 테스트, 숏드라마 클립.",
        "SECTIONIDX": "05 / 영상", "H2": "YouTube에서 SportsBoy 팔로우",
        "SECDESC": "운동선수 필드 가이드, 농도 테스트, 숏드라마 클립——모두 여기서 먼저 업데이트. 구독하고 새 작품 놓치지 마세요.",
        "SUB": "채널 구독 @sportsboygay",
        "F1T": "농도 테스트 Shorts", "F1D": "첫 에피소드: 당신은 얼마나 운동선수형?",
        "F2T": "농구 운동선수 가이드", "F2D": "템플릿에서 꺼내는 농구 선수.",
        "WATCH": "YouTube에서 보기", "AINOTE": "영상은 AI 보조 제작 · 모든 캐릭터 성인 설정",
        "QH2": "당신의 운동선수 농도 테스트", "QD": "6문제, 30초, 공유 가능한 페르소나 차트 생성.", "QB": "테스트 시작",
        "FOOTER_YT": "YouTube",
    },
}

for code, d in LANGS.items():
    t = TPL
    for k, v in d.items():
        t = t.replace("__%s__" % k, v)
    t = t.replace("__CHANNEL__", CHANNEL)
    t = t.replace("__SITE__", SITE)
    t = t.replace("__OGURL__", SITE + d["CANON"])
    # active lang option
    t = t.replace("__ACTIVE_ZH__", "is-active" if code == "zh" else "")
    t = t.replace("__ACTIVE_EN__", "is-active" if code == "en" else "")
    t = t.replace("__ACTIVE_JA__", "is-active" if code == "ja" else "")
    t = t.replace("__ACTIVE_KO__", "is-active" if code == "ko" else "")
    outdir = os.path.join(BASE, code, "videos") if code != "zh" else os.path.join(BASE, "videos")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(t)
    print("wrote", out)
print("DONE")
