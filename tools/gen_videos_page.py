# -*- coding: utf-8 -*-
"""gen_videos_page.py — 生成四语 /videos 频道页。

设计：
- 顶部：主播放器 = 具体视频 ID 内嵌（可靠、可播），支持「自动轮播」静音循环切换已知精选。
- 下方：构建期从 YouTube RSS 拉取频道全部公开视频，渲染成缩略图画廊（每个卡片 = 具体视频 ID，
  点击即在站内主播放器播放，不依赖不稳定的 playlist 嵌入）。频道上传新片后，重新生成即更新。
- 订阅 / 看全部 外链（订阅关系与完整浏览必须在 YouTube 上）。
频道 ID：UCw0gqeiGnH_vMeSxGQlBwvw  （注意结尾是 Bwvw，勿漏 w）
放置：/videos, /en/videos, /ja/videos, /ko/videos
"""
import os
import json
import xml.etree.ElementTree as ET
from html import escape
import urllib.request

SITE = "https://www.sportsboy.gay"
CHANNEL = "UCw0gqeiGnH_vMeSxGQlBwvw"          # 真实频道 ID（结尾 Bwvw）
UPLOADS = "UU" + CHANNEL[2:]                   # 上传播放列表 ID（备用）
RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL
BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"

# 已知精选（用于顶部主播放器默认 + 自动轮播）
FEATURED = ["zt0PQeRFJkc", "zjlhX0jBhbE"]

# 离线兜底：RSS 拉取失败时使用（当前频道真实视频，避免空白）
FALLBACK = [
    ("zt0PQeRFJkc", "直男做体育生浓度测试，做到第三题破防了 | SportsBoy"),
    ("zjlhX0jBhbE", "怎么一眼认出篮球体育生？看这四条 | SportsBoy"),
    ("yEs3xaG8o1k", "体育生家族里最安静的一支，靠白袜认领身份"),
    ("52KI4WEheo4", "健身房体育生图鉴：练得最狠，话最少｜SportsBoy 图鉴 02"),
    ("f3kuAUt8xsw", "更衣室文化考：体育生的第三空间｜SportsBoy 图鉴 03"),
    ("3-40xFAVEZU", "篮球体育生图鉴｜球鞋护踝一身汗，模板拼不出活的他"),
]


def fetch_videos():
    """从 YouTube RSS 拉取频道全部公开视频，返回 [(video_id, title), ...]（最新在前）。"""
    try:
        req = urllib.request.Request(RSS, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=20).read()
        root = ET.fromstring(data)
        ns = {
            "a": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        out = []
        for e in root.findall("a:entry", ns):
            vid = e.find("yt:videoId", ns)
            title = e.find("a:title", ns)
            if vid is not None and vid.text:
                out.append((vid.text, title.text if title is not None else ""))
        if out:
            print("RSS ok, %d videos" % len(out))
            return out
    except Exception as ex:
        print("RSS fetch failed, use fallback:", ex)
    return FALLBACK


def build_gallery(videos):
    cards = []
    for vid, title in videos:
        t = escape(title or vid)
        cards.append(
            '<a class="yt-card" data-vid="%s" href="#ytMainWrap">'
            '<span class="yt-thumb"><img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" '
            'alt="%s" loading="lazy"></span>'
            '<span class="yt-card-title">%s</span></a>' % (vid, vid, t, t)
        )
    return "\n".join(cards)


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
#ytRotate.is-on{background:#11100c;color:#FF5C39;border-color:#FF5C39}
.yt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;max-width:960px;margin:0 auto}
.yt-card{display:block;text-decoration:none;color:inherit;background:#16140F;border:1px solid #2a2620;border-radius:12px;overflow:hidden;transition:.18s;cursor:pointer}
.yt-card:hover{border-color:#FF5C39;transform:translateY(-2px)}
.yt-thumb{display:block;position:relative;aspect-ratio:16/9;background:#000}
.yt-thumb img{width:100%;height:100%;object-fit:cover;display:block}
.yt-thumb:after{content:"\\25B6";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font-size:28px;background:rgba(0,0,0,.25);opacity:0;transition:.18s}
.yt-card:hover .yt-thumb:after{opacity:1}
.yt-card-title{padding:10px 12px;font-size:13px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
#ytMain,#ytMain iframe{position:absolute;inset:0;width:100%!important;height:100%!important;border:0}
</style>
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"WebSite", "name":"SportsBoy.gay", "url":"__OGURL__", "inLanguage":"__HTMLLANG__", "description":"__DESC__", "publisher":{ "@type":"Organization", "name":"SportsBoy.gay", "url":"__SITE__/" } }
</script>
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"VideoObject", "name":"直男做体育生浓度测试，做到第三题破防了 | SportsBoy", "description":"SportsBoy 浓度测试 Shorts——6 道题测测你有多体育生。", "thumbnailUrl":"https://i.ytimg.com/vi/zt0PQeRFJkc/hqdefault.jpg", "uploadDate":"2026-01-01", "contentUrl":"https://www.youtube.com/watch?v=zt0PQeRFJkc", "embedUrl":"https://www.youtube.com/embed/zt0PQeRFJkc", "publisher":{ "@type":"Organization", "name":"SportsBoy.gay", "url":"__SITE__/" } }
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
      <div id="ytMainWrap" style="position:relative;width:100%;aspect-ratio:16/9;background:#000;border-radius:14px;overflow:hidden">
        <div id="ytMain" style="position:absolute;inset:0;width:100%;height:100%"></div>
      </div>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:14px">
        <button id="ytRotate" class="btn btn-primary btn-sm" type="button">&#9654; __ROTATE__</button>
        <a class="btn btn-ghost btn-sm" href="https://www.youtube.com/@sportsboygay?sub_confirmation=1" target="_blank" rel="noopener">&#9654; __SUB__</a>
        <a class="btn btn-ghost btn-sm" href="https://www.youtube.com/@sportsboygay/videos" target="_blank" rel="noopener">__ALL__</a>
      </div>
    </div>

    <div class="yt-all" style="margin-top:44px">
      <p class="section-desc" style="text-align:center;margin-bottom:14px">__ALL_TITLE__</p>
      <div class="yt-grid" id="ytGrid">__GALLERY__</div>
    </div>

    <script>
    (function(){
      var wrap=document.getElementById('ytMainWrap');
      var btn=document.getElementById('ytRotate');
      var grid=document.getElementById('ytGrid');
      var ids=__IDS_JS__;
      var idx=0, timer=null, player=null, ready=false;
      var LABEL_ON='&#9654; __ROTATE__', LABEL_OFF='&#9632; __STOP__';

      function playFeatured(i){
        idx=(i%ids.length+ids.length)%ids.length;
        apiPlay(ids[idx]);
      }
      function apiPlay(id){
        if(ready && player){
          try{ player.unMute(); player.setVolume(100); player.loadVideoById(id); return; }
          catch(e){}
        }
        // 兜底：API 未就绪时退回 iframe src（静音自动播放）
        var f=document.getElementById('ytMain');
        if(f) f.src='https://www.youtube.com/embed/'+id+'?rel=0&autoplay=1&mute=1';
      }
      function start(){
        if(timer) return;
        btn.classList.add('is-on'); btn.innerHTML=LABEL_OFF;
        playFeatured(idx+1);                    // 处于用户点击手势内 → 允许带声播放
        timer=setInterval(function(){ playFeatured(idx+1); },22000);
      }
      function stop(){
        if(timer){clearInterval(timer);timer=null;}
        btn.classList.remove('is-on'); btn.innerHTML=LABEL_ON;
      }
      if(btn){ btn.addEventListener('click',function(){ timer?stop():start(); }); }

      function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
      function buildGallery(videos){
        if(!grid || !videos || !videos.length) return;
        grid.innerHTML = videos.map(function(v){
          var t=esc(v.title||v.id);
          return '<a class="yt-card" data-vid="'+v.id+'" href="#ytMainWrap">'
            +'<span class="yt-thumb"><img src="https://i.ytimg.com/vi/'+v.id+'/hqdefault.jpg" alt="'+t+'" loading="lazy"></span>'
            +'<span class="yt-card-title">'+t+'</span></a>';
        }).join('');
        Array.prototype.forEach.call(grid.querySelectorAll('.yt-card'), function(c){
          c.addEventListener('click', function(ev){
            ev.preventDefault(); stop(); apiPlay(c.getAttribute('data-vid'));
            if(wrap) wrap.scrollIntoView({behavior:'smooth',block:'start'});
          });
        });
      }
      function setFeatured(videos){
        if(videos && videos.length){ ids = videos.slice(0,8).map(function(v){return v.id;}); }
      }
      buildGallery(__GALLERY_JSON__);   // 构建期静态快照（首屏即时可见，无需等待 API）
      setFeatured(__GALLERY_JSON__);
      // 运行时拉取最新频道视频，自动同步 YouTube 上传（/api/videos 服务端代理 RSS）
      fetch('/api/videos').then(function(r){return r.json();}).then(function(j){
        if(j && j.videos && j.videos.length){
          buildGallery(j.videos); setFeatured(j.videos);
          if(ready && player && !timer) player.cueVideoById(ids[0]);
        }
      }).catch(function(){});

      window.onYouTubeIframeAPIReady=function(){
        player=new YT.Player('ytMain',{
          playerVars:{ rel:0, modestbranding:1, playsinline:1 },
          events:{
            onReady:function(){ ready=true; player.cueVideoById(ids[0]); }  // 仅预览，不自动播放
          }
        });
      };
    })();
    </script>
    <script src="https://www.youtube.com/iframe_api"></script>

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
        <a href="https://afdian.com/a/sportsboy" target="_blank" rel="noopener">爱发电（完整版解锁）</a>
        <a href="https://www.youtube.com/@sportsboygay" target="_blank" rel="noopener">YouTube</a>
        <a href="https://cbtdao.itch.io/sportsboy" target="_blank" rel="noopener">itch.io</a>
        <a href="https://x.com/sportsboygay" target="_blank" rel="noopener">X</a>
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
<script>
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
</script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

LANGS = {
    "zh": {
        "HTMLLANG": "zh-CN", "LANGLABEL": "中文", "NAVVID": "视频",
        "TITLE": "SportsBoy.gay — 视频频道", "VURL": "/videos", "CANON": "/videos",
        "DESC": "在 YouTube 追更 SportsBoy：体育生图鉴、浓度测试、短剧切片，每周新作不漏。",
        "SECTIONIDX": "05 / 视频", "H2": "在 YouTube 追更 SportsBoy",
        "SECDESC": "体育生图鉴、浓度测试、短剧切片——都先在这里更新。上面看精选，下面点开看全部。",
        "SUB": "订阅频道 @sportsboygay", "ROTATE": "自动轮播", "STOP": "停止轮播", "ALL": "频道全部视频", "ALL_TITLE": "频道全部视频",
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
        "SECDESC": "Jock field guides, vibe test, short-drama clips — all updated here first. Featured up top, full list below.",
        "SUB": "Subscribe @sportsboygay", "ROTATE": "Auto rotate", "STOP": "Stop", "ALL": "All on YouTube", "ALL_TITLE": "All channel videos",
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
        "SUB": "チャンネル登録 @sportsboygay", "ROTATE": "自動再生", "STOP": "停止", "ALL": "YouTube で見る", "ALL_TITLE": "チャンネル全動画",
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
        "SUB": "채널 구독 @sportsboygay", "ROTATE": "자동 재생", "STOP": "정지", "ALL": "YouTube 에서 보기", "ALL_TITLE": "채널 전체 영상",
        "F1T": "농도 테스트 Shorts", "F1D": "첫 에피소드: 당신은 얼마나 운동선수형?",
        "F2T": "농구 운동선수 가이드", "F2D": "템플릿에서 꺼내는 농구 선수.",
        "WATCH": "YouTube에서 보기", "AINOTE": "영상은 AI 보조 제작 · 모든 캐릭터 성인 설정",
        "QH2": "당신의 운동선수 농도 테스트", "QD": "6문제, 30초, 공유 가능한 페르소나 차트 생성.", "QB": "테스트 시작",
        "FOOTER_YT": "YouTube",
    },
}

videos = fetch_videos()
gallery_html = build_gallery(videos)
gallery_json = json.dumps([{"id": v, "title": t} for v, t in videos], ensure_ascii=False)

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
    t = t.replace("__GALLERY__", gallery_html)
    t = t.replace("__GALLERY_JSON__", gallery_json)
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
