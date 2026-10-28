# -*- coding: utf-8 -*-
"""gen_almanac.py — 生成「王牌栏目」5 篇图鉴图文页 + 隐私政策页。

修复首页 #columns 五个卡片的死链（/almanac/* 此前未建 → 404）。
页面复用站点 style.css / nav / footer（合规 footer：无爱发电，海外站品牌隔离），
含 canonical + hreflang(zh-CN/x-default)、Vercel Insights 分析 snippet、隐私链接。
放置：/almanac/{slug}.html  +  /privacy/index.html
"""
import os

SITE = "https://www.sportsboy.gay"
BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"

ANALYTICS = """<script>
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
</script>
<script defer src="/_vercel/insights/script.js"></script>"""

# 共享 nav（绝对路径，与 videos 页一致）
NAV = """
    <nav class="nav-links" id="navLinks">
      <a href="/#columns">王牌栏目</a>
      <a href="/#work">首部作品</a>
      <a href="/#flywheel">宇宙</a>
      <a href="/quiz">浓度测试</a>
      <a href="/concentration">浓度分布</a>
      <a href="/videos">视频</a>
      <a class="btn btn-primary btn-sm" href="/#join">等 demo 上线</a>
    </nav>"""

# 合规 footer（海外站：YouTube / itch.io / TikTok / X，禁爱发电）
FOOTER = """
      <div class="footer-col">
        <h4>站点</h4>
        <a href="/#columns">王牌栏目</a>
        <a href="/#work">首部作品</a>
        <a href="/quiz">浓度测试</a>
        <a href="/concentration">浓度分布</a>
        <a href="/videos">视频</a>
        <a href="/privacy">隐私政策</a>
      </div>
      <div class="footer-col">
        <h4>社区</h4>
        <a href="https://www.youtube.com/@sportsboygay" target="_blank" rel="noopener">YouTube</a>
        <a href="#" data-todo="itch.io 页面待 demo 上线后开通">itch.io</a>
        <a href="#" data-todo="社交账号待开通">TikTok / X</a>
      </div>"""

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:image" content="__SITE__/assets/img/og.jpg">
<meta property="og:type" content="article">
<meta property="og:url" content="__OGURL__">
<meta name="theme-color" content="#0E0D0B">
<link rel="icon" href="/assets/img/icon-512.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<link rel="canonical" href="__OGURL__">
<link rel="alternate" hreflang="zh-CN" href="__OGURL__">
<link rel="alternate" hreflang="x-default" href="__OGURL__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<style>
.alm-hero{padding:130px 0 24px}
.alm-hero .alm-tag{color:#FF5C39;font-size:13px;letter-spacing:.12em;text-transform:uppercase}
.alm-hero h1{font-size:34px;line-height:1.18;margin:10px 0 14px}
.alm-lede{font-size:17px;line-height:1.7;color:#cfc9bf;max-width:720px}
.alm-body{max-width:720px;margin:0 auto;padding:8px 0 40px}
.alm-body h2{font-size:22px;margin:34px 0 10px}
.alm-body p{font-size:16px;line-height:1.85;margin:0 0 16px;color:#e7e2d8}
.alm-body .alm-quote{border-left:3px solid #FF5C39;padding:4px 0 4px 16px;color:#cfc9bf;font-style:italic;margin:22px 0}
.alm-tags{display:flex;gap:10px;flex-wrap:wrap;margin:26px 0 8px}
.alm-tags span{background:#16140F;border:1px solid #2a2620;border-radius:999px;padding:6px 14px;font-size:13px;color:#FF5C39}
.alm-cta{background:#16140F;border:1px solid #2a2620;border-radius:14px;padding:22px;margin:30px 0;text-align:center}
.alm-cta a{margin:6px}
</style>
</head>
<body>

<header class="site-header" id="siteHeader">
  <div class="container nav-inner">
    <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>__NAV__
    <div class="nav-side">
      <div class="lang-menu-wrap">
        <button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="langMenu">
          <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
            <circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>
            <path d="M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/>
          </svg>
          <span>中文</span>
        </button>
        <div class="lang-menu" id="langMenu" hidden>
          <a class="lang-opt is-active" href="/" hreflang="zh-CN" lang="zh-CN" aria-current="true">中文<span class="lang-opt-tag">ZH</span></a>
          <a class="lang-opt" href="/en" hreflang="en" lang="en">English<span class="lang-opt-tag">EN</span></a>
          <a class="lang-opt" href="/ja" hreflang="ja" lang="ja">日本語<span class="lang-opt-tag">JA</span></a>
          <a class="lang-opt" href="/ko" hreflang="ko" lang="ko">한국어<span class="lang-opt-tag">KO</span></a>
        </div>
      </div>
      <button class="nav-toggle" aria-label="打开菜单" aria-expanded="false" aria-controls="navLinks">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<main>
  <section class="block alm-hero">
    <div class="container">
      <p class="alm-tag">__TAG__</p>
      <h1>__TITLE__</h1>
      <p class="alm-lede">__LEDE__</p>
    </div>
  </section>
  <article class="block alm-body">
    <div class="container">
__BODY__
      <div class="alm-tags">__TAGS__</div>
      <div class="alm-cta">
        <p style="margin:0 0 12px">看完图鉴，测测你属于哪一种？</p>
        <a class="btn btn-primary" href="/quiz">开始浓度测试</a>
        <a class="btn btn-ghost" href="/videos">看频道视频</a>
      </div>
    </div>
  </article>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">SPORTSBOY<span class="brand-tld">.gay</span></a>
        <p>汗水、肌肉与骄傲，光明正大。</p>
      </div>__FOOTER__
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

__ANALYTICS__
<script src="/assets/js/main.js"></script>
</body>
</html>
"""


def build_article(slug, tag, title, lede, body, tags, desc):
    t = TPL
    t = t.replace("__NAV__", NAV)
    t = t.replace("__FOOTER__", FOOTER)
    t = t.replace("__ANALYTICS__", ANALYTICS)
    t = t.replace("__TAG__", tag)
    t = t.replace("__TITLE__", title)
    t = t.replace("__LEDE__", lede)
    t = t.replace("__BODY__", body)
    t = t.replace("__TAGS__", "".join('<span>#%s</span>' % x for x in tags))
    t = t.replace("__DESC__", desc)
    canon = SITE + "/almanac/" + slug
    t = t.replace("__OGURL__", canon)
    t = t.replace("__SITE__", SITE)
    return t


# ---------- 五篇图鉴 ----------

ARTICLES = {
    "swim-jock": dict(
        tag="图鉴 01 · The Almanac",
        title="泳队体育生图鉴：水感天赋型，湿身是被动技能",
        lede="泳队生不是「会游泳的帅哥」，是一个独立物种。外人看见胸肌和拖鞋，我们看见一套完整的泳池生存哲学。",
        desc="泳队体育生图鉴：人字拖即正装、泳裤晾法是一门玄学、白袜配拖鞋的合法权——一个被低估的体育生物种。",
        tags=["水感天赋", "松弛体面", "慢热但上头"],
        body="""
      <p>判定一个泳队生，不看他练了几年，看他从泳池出来那一刻的体面程度。别人是「刚运动完」，他是「刚从主场撤退」——拖鞋一踩，毛巾一搭，仿佛刚才那场湿身是别人的事。</p>
      <h2>人字拖是他的正装</h2>
      <p>泳队生对拖鞋的虔诚，堪比篮球生对 AJ。不是随便一双，是能踩进更衣室瓷砖缝里也不慌的那一双。岸上的一切正式场合，拖鞋出场即合法。你问他为什么，他只会说「习惯了」——习惯，是这个物种最高级的词汇。</p>
      <div class="alm-quote">泳裤晾哪儿干得比较快，是泳队生认真研究的学术问题，不是玩笑。</div>
      <h2>泳裤晾法是一门玄学</h2>
      <p>阳台朝向、通风时长、有没有被室友的湿毛巾压住——这套决策树，外人看不懂，但每个泳队生闭眼都能排优。它本质上是空间管理天赋在更衣室场景的降维应用。</p>
      <h2>白袜 + 拖鞋的合法权</h2>
      <p>在泳队生的语境里，白袜不是穿搭，是身份认领。上岸套上白袜踩拖鞋，是「我还是体育生」的最低成本声明。后面那篇《白袜研究》会专门拆这个符号，这里先埋个钩子。</p>
      <h2>湿身是被动技能</h2>
      <p>别误会，泳队生不是刻意秀。是他一进水，被动技能就触发了：水感、线条、那种「地球时间暂停」的松弛。追的人以为是氛围，其实是天赋型选手的出厂设置。</p>
        """,
    ),
    "fake-jock": dict(
        tag="图鉴 02 · The Gaze",
        title="假体育生鉴别指南：模板和真人，差在汗碱",
        lede="怎么一眼识破「摆拍型体育生」？不看腹肌照片，看他身上有没有训练留下的诚实痕迹。",
        desc="假体育生鉴别指南：模板体育生 vs 真人，差在护具、汗碱与对装备的虔诚——用 gay 的眼光重新解说体育圈。",
        tags=["火眼", "不拆穿", "看戏心态"],
        body="""
      <p>我们尊重每一种表达，但图鉴讲真伪，得有标准。以下不是批判，是鉴赏——毕竟，能一眼看穿模板，也是一种乐趣。</p>
      <h2>模板型：滤镜腿 + 从不流汗</h2>
      <p>特征高度一致：器械永远崭新，自拍永远 45 度仰角，文案永远「今天也努力」。问题在于，他身上没有任何训练留下的诚实痕迹。汗水是体育生最不会撒谎的证据，而他恰好没有。</p>
      <div class="alm-quote">真人会护具缠身、汗碱留印；模板只会滤镜缠身、文案留白。</div>
      <h2>真人型：护具即勋章</h2>
      <p>篮球生护踝、举重生护腕、泳队生那双磨到起毛的拖鞋——这些不是装备，是时间凭证。真人对装备的虔诚，写在磨损里，不写在标签上。</p>
      <h2>不拆穿，是基本修养</h2>
      <p>鉴别的意义不是去杠，是让自己看得更准、聊得更爽。圈子里最迷人的，永远是那种「我懂但不说破」的默契。看戏心态拉满，图鉴才好玩。</p>
        """,
    ),
    "locker-room": dict(
        tag="图鉴 03 · Locker Room Studies",
        title="更衣室考：体育生的第三空间，也是《体育生》那场雨夜戏的来处",
        lede="更衣室不是换衣服的过道，是体育生的文化现场——有秩序、有黑话、有边界感。",
        desc="更衣室考：从空间秩序与圈层黑话，读懂体育生；这也是《体育生》视觉小说雨夜戏的灵感来处。",
        tags=["空间社会学", "边界感", "兄弟叙事"],
        body="""
      <p>如果只能选一个地方读懂体育生，不是球场，是更衣室。那里浓缩了所有不成文的规则：谁的格子、谁先冲凉、毛巾别拿错——一套默会的礼仪，比任何队规都管用。</p>
      <h2>第三空间，不是更衣间</h2>
      <p>对体育生而言，更衣室介于「赛场」和「生活」之间：可以松一口气的场所，也是关系发酵的地方。很多兄弟叙事的起点，都在这里。我们写《体育生》那条雨夜戏，灵感正来自这种半公开、半私密的张力。</p>
      <div class="alm-quote">更衣室的灯一关，体育生之间那些没说破的东西，才开始说。</div>
      <h2>黑话是入场券</h2>
      <p>「搭子」「保一」「冲个凉」——这些词外人听不懂，圈内人心领神会。黑话的作用从来不是保密，是快速确认「你也是自己人」。</p>
      <h2>边界感才是高级</h2>
      <p>真正写得好的体育生故事，不靠越界博眼球，靠边界感制造张力。尊重空间、尊重人物，反而更有后劲。这也是我们内容方法论的红线：内部视角，不消费。</p>
        """,
    ),
    "white-sock": dict(
        tag="图鉴 04 · White Sock Studies",
        title="白袜研究：为什么白袜是体育生的暗号",
        lede="亚文化考据时间。白袜不是穿搭单品，是体育生身份的最低成本认领符号。",
        desc="白袜研究：亚文化考据，白袜作为体育生身份认领符号与圈层暗号——恋物但不低俗，谈资与分享欲制造机。",
        tags=["符号学", "恋物不低俗", "内部梗"],
        body="""
      <p>先声明：这是亚文化考据，不是 fetish 展柜。我们聊的是符号——一种被圈层心照不宣认领的视觉暗号。</p>
      <h2>最低成本的身份声明</h2>
      <p>不用纹身、不用装备堆砌，一双白袜就够。它便宜、日常、可解释，却能在同好眼里完成一次无声的「我懂」。这种低门槛高识别度的符号，在亚文化里最耐用。</p>
      <div class="alm-quote">白袜的性感不在布，在「我刚好也是这种人」的会心一笑。</div>
      <h2>为什么是白，不是黑</h2>
      <p>白更脆弱、更诚实——脏了、湿了、起球了，都看得见的那种真实。体育生的魅力恰恰在「不修饰的真实」。白袜把这点放大成符号，于是成了暗号。</p>
      <h2>谈资，不是边界</h2>
      <p>我们用它制造谈资和分享欲，但从不把它当作评价他人的尺子。符号好玩的前提，是彼此都知道：人比符号丰富得多。</p>
        """,
    ),
    "basketball": dict(
        tag="图鉴 05 · Basketball Field Guide",
        title="篮球体育生图鉴：把篮球生从「基圈天菜」模板里请出来",
        lede="篮球生被模板化了太久——护踝、AJ、斗牛嘴硬。但真实的那位，比模板有内容得多。",
        desc="篮球体育生图鉴：护踝、球鞋收藏、一身汗底下的内容——把篮球生从「基圈天菜」模板里请出来。",
        tags=["弹跳与盐", "斗牛嘴硬", "收藏家自觉"],
        body="""
      <p>篮球生是体育生里被模板化最严重的一支：一说起来就是 AJ、腹肌、1v1。模板能带来流量，但留不住人。我们想把他请出来，还原成有内容的人。</p>
      <h2>护踝比对象亲</h2>
      <p>这不是段子，是排序。篮球生对护踝、绷带的在意，是训练留下的肌肉记忆。你以为他在意装备，其实他在意的是「还能再打十年」。</p>
      <div class="alm-quote">半场下来球衣能拧出水，但他嘴上说「随便打」——斗牛的浪漫，全在嘴硬。</div>
      <h2>球鞋收藏家的自我修养</h2>
      <p>AJ 不是炫耀，是信仰。每一双都有上脚故事：哪场盖了谁、哪双磨平了底。收藏清单，是这个物种的私人编年史。</p>
      <h2>一身汗底下的内容</h2>
      <p>剥掉模板，篮球生是重感情、讲输赢、对兄弟很仗义的那类人。下次再看到篮球生，别只看腹肌——看他被盖之后那个不服的眼神，那才是正文。</p>
        """,
    ),
}

# ---------- 隐私政策页 ----------

PRIVACY = dict(
    title="隐私政策 · SportsBoy.gay",
    desc="SportsBoy.gay 隐私政策：网站含成人向（BL）内容，说明我们收集的数据、Cookie 用途与你的权利。",
)


def build_privacy():
    body = """
      <p>SportsBoy.gay（以下简称「本站」）是一个面向成年人的体育生文化内容站。本站含 BL（男男）向虚构内容，访问即代表你确认已年满 18 岁或达到你所在司法辖区的法定成年年龄。</p>
      <h2>我们收集什么</h2>
      <p><b>浓度测试（quiz）：</b>你作答时，分数与结果类型仅在你本地浏览器计算与展示，通常不会上传到服务器；结果分享页为公开内容。我们不会将你的具体答案关联到你的身份。</p>
      <p><b>联系与订阅：</b>如未来开通订阅或邮件通知，我们会明确告知并仅在你主动提供时收集邮箱等信息。</p>
      <p><b>匿名分析：</b>我们使用隐私友好的网站分析（Vercel Web Analytics），仅统计匿名访问量、页面停留与事件（如完成测试），<b>不使用 Cookie、不跨站追踪、不出售任何数据</b>。</p>
      <h2>Cookie 与本地存储</h2>
      <p>本站可能在你浏览器本地保存少量数据，用于：记住你的年龄确认状态、语言偏好。这些仅存于你的设备，不涉及身份追踪。</p>
      <h2>第三方内容</h2>
      <p>本站嵌入 YouTube 视频，YouTube 可能按其自身政策处理播放相关数据。相关内容受 YouTube 隐私政策约束。</p>
      <h2>你的权利</h2>
      <p>你有权了解、更正或删除你的个人数据。如有疑问，可通过本站公开渠道联系我们。本站内容均为成年人虚构创作，与现实人物无关。</p>
    """
    t = TPL
    t = t.replace("__NAV__", NAV)
    t = t.replace("__FOOTER__", FOOTER)
    t = t.replace("__ANALYTICS__", ANALYTICS)
    t = t.replace("__TAG__", "说明 · Legal")
    t = t.replace("__TITLE__", PRIVACY["title"])
    t = t.replace("__LEDE__", "本站含成人向（BL）虚构内容。我们收集的数据、Cookie 用途与你的权利，都在这页讲清楚。")
    t = t.replace("__BODY__", body)
    t = t.replace("__TAGS__", "")
    t = t.replace("__DESC__", PRIVACY["desc"])
    t = t.replace("__OGURL__", SITE + "/privacy")
    t = t.replace("__SITE__", SITE)
    return t


def main():
    # almanac 五篇
    out_alm = os.path.join(BASE, "almanac")
    os.makedirs(out_alm, exist_ok=True)
    for slug, d in ARTICLES.items():
        html = build_article(slug, d["tag"], d["title"], d["lede"], d["body"], d["tags"], d["desc"])
        with open(os.path.join(out_alm, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote almanac/%s.html" % slug)
    # privacy
    out_priv = os.path.join(BASE, "privacy")
    os.makedirs(out_priv, exist_ok=True)
    with open(os.path.join(out_priv, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_privacy())
    print("wrote privacy/index.html")
    print("DONE")


if __name__ == "__main__":
    main()
