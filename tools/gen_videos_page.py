# -*- coding: utf-8 -*-
"""gen_videos_page.py — 生成四语 /videos 频道页。

设计：
- 顶部：主播放器 = 具体视频 ID 内嵌（可靠、可播）。
- 下方：频道「上传播放列表」内嵌（listType=playlist），自动显示频道全部公开视频，并排网格、站内直接播放、以后上传自动出现。
- 「自动轮播」按钮：静音自动循环切换顶部主播放器（已知视频）。
- 订阅 / 看全部 外链（订阅关系与完整浏览必须在 YouTube 上）。
频道 ID：UCw0gqeiGnH_vMeSxGQlBvw
放置：/videos, /en/videos, /ja/videos, /ko/videos
"""
import os

SITE = "https://www.sportsboy.gay"
CHANNEL = "UCw0gqeiGnH_vMeSxGQlBvw"
UPLOADS = "UU" + CHANNEL[2:]   # 上传播放列表 ID（自动含频道全部公开视频）
BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"

# 已知视频（用于顶部主播放器默认 + 自动轮播；其余频道视频由上传播放列表自动展示）
FEATURED = ["zt0PQeRFJkc", "zjlhX0jBhbE"]

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
<style>
#ytRotate.is-on{background:#FF5C39;border-color:#FF5C39}
</style>
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"WebSite", "name":"SportsBoy.gay", "url":"__OGURL__", "inLanguage":"__HTMLLANG__", "description":"__DESC__", "publisher":{ "@type":"Organization", "name":"SportsBoy.gay", "url":"__SITE__/" } }
</script>
</head>
<body>

<header class="site-header" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
    <nav class="nav-links" id="navLinks">
      <a href="/#columns">王牌栏目</a>
      <a href="/#work">首部作品</a>
      <a href="/#flywheel">宇宙</a>
      <a href="/quiz">浓度测试</a>
      <a href="/concentration">浓度分布</a>
      <a href="/videos" class="is-current">__NAVVID__</a>
      <a class="btn btn-primary btn-sm" href="/#join">等 demo 上线</a>
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

    <div class="yt-showcase" style="max-width:760px;margin:24px auto 0">
      <div style="position:relative;width:100%;aspect-ratio:16/9;background:#000;border-radius:14px;overflow:hidden">
        <iframe id="ytMain" src="https://www.youtube.com/embed/__FIRSTID__?rel=0" title="__F1T__" loading="lazy"
          allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen
          style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
      </div>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:14px">
        <button id="ytRotate" class="btn btn-primary btn-sm" type="button">&#9654; __ROTATE__</button>
        <a class="btn btn-ghost btn-sm" href="https://www.youtube.com/@sportsboygay?sub_confirmation=1" target="_blank" rel="noopener">&#9654; __SUB__</a>
        <a class="btn btn-ghost btn-sm" href="https://www.youtube.com/@sportsboygay/videos" target="_blank" rel="noopener">__ALL__</a>
      </div>
    </div>

    <div class="yt-all" style="margin-top:44px">
      <p class="section-desc" style="text-align:center;margin-bottom:14px">__ALL_TITLE__</p>
      <div style="position:relative;width:100%;max-width:960px;margin:0 auto;aspect-ratio:16/9;background:#000;border-radius:14px;overflow:hidden">
        <iframe src="https://www.youtube.com/embed?listType=playlist&amp;list=__UPLOADS__" title="__ALL_TITLE__" loading="lazy"
          allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen
          style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
      </div>
    </div>

    <script>
    (function(){
      var main=document.getElementById('ytMain');
      var ids=__IDS_JS__;
      var idx=0, timer=null, btn=document.getElementById('ytRotate');
      function load(i,auto){
        idx=(i%ids.length+ids.length)%ids.length;
        main.src='https://www.youtube.com/embed/'+ids[idx]+'?rel=0'+(auto?'&autoplay=1&mute=1':'');
      }
      function start(){if(timer)return;btn.classList.add('is-on');timer=setInterval(function(){load(idx+1,true);},22000);}
      function stop(){if(timer){clearInterval(timer);timer=null;}btn.classList.remove('is-on');}
      btn.addEventListener('click',function(){timer?stop():start();});
    })();
    </script>

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
        <a href="/#columns">王牌栏目</a>
        <a href="/#work">首部作品</a>
        <a href="/quiz">浓度测试</a>
        <a href="/concentration">浓度分布</a>
        <a href="/videos">__NAVVID__</a>
      </div>
      <div class="footer-col">
        <h4>社区</h4>
        <a href="https://www.youtube.com/@sportsboygay" target="_blank" rel="noopener">YouTube</a>
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
        "SECDESC": "体育生图鉴、浓度测试、短剧切片——都先在这里更新。上面看精选，下面看频道全部。",
        "SUB": "订阅频道 @sportsboygay", "ROTATE": "自动轮播", "ALL": "频道全部视频", "ALL_TITLE": "频道全部视频",
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
        "SECDESC": "Jock field guides, vibe test, short-drama clips — all updated here first. Featured up top, full channel below.",
        "SUB": "Subscribe @sportsboygay", "ROTATE": "Auto rotate", "ALL": "All on YouTube", "ALL_TITLE": "All channel videos",
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
        "SECDESC": "体育生図鑑、濃度テスト、ショートドラマ——まずここで更新。上は精选、下はチャンネル全動画。",
        "SUB": "チャンネル登録 @sportsboygay", "ROTATE": "自動再生", "ALL": "YouTube で見る", "ALL_TITLE": "チャンネル全動画",
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
        "SECDESC": "운동선수 필드 가이드, 농도 테스트, 숏드라마 클립——모두 여기서 먼저 업데이트. 위는精选, 아래는 채널 전체.",
        "SUB": "채널 구독 @sportsboygay", "ROTATE": "자동 재생", "ALL": "YouTube 에서 보기", "ALL_TITLE": "채널 전체 영상",
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
    t = t.replace("__UPLOADS__", UPLOADS)
    t = t.replace("__SITE__", SITE)
    t = t.replace("__OGURL__", SITE + d["CANON"])
    t = t.replace("__IDS_JS__", str(FEATURED))
    t = t.replace("__FIRSTID__", FEATURED[0])
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
