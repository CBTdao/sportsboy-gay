# -*- coding: utf-8 -*-
"""gen_almanac.py — 生成「王牌栏目」5 篇图鉴图文页 + 隐私政策页，四语（zh/en/ja/ko）。

修复首页 #columns 五个卡片的死链（/almanac/* 此前未建 → 404），并消除非中文用户掉进中文页的缺口：
- 图鉴 5 篇 × 4 语：/almanac/{slug}.html, /en/almanac/{slug}.html, /ja/almanac/{slug}.html, /ko/almanac/{slug}.html
- 隐私页 × 4 语：/privacy, /en/privacy, /ja/privacy, /ko/privacy
页面复用站点 style.css / nav / footer（合规 footer：含爱发电完整版解锁、itch.io、X、YouTube 四入口），
含 canonical + hreflang 四语互指、语言菜单链向同 slug 兄弟页、Vercel Insights 分析 snippet、隐私链接。
"""
import os

SITE = "https://www.sportsboy.gay"
BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"

PREFIX = {"zh": "", "en": "/en", "ja": "/ja", "ko": "/ko"}

ANALYTICS = """<script>
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
</script>
<script defer src="/_vercel/insights/script.js"></script>"""

# 语言级 UI 文案
UI = {
    "zh": dict(
        HTMLLANG="zh-CN", LANGLABEL="中文",
        nav_cols="王牌栏目", nav_work="首部作品", nav_fly="宇宙",
        nav_quiz="浓度测试", nav_conc="浓度分布", nav_vid="视频", nav_join="等 demo 上线",
        nav_serial="连载", nav_know="认识男同", nav_vn="游戏剧本", nav_novel="宇宙散文",
        foot_site="站点", foot_comm="社区", foot_note="说明",
        foot_cols_a="王牌栏目", foot_work="首部作品", foot_quiz="浓度测试",
        foot_conc="浓度分布", foot_vid="视频", foot_priv="隐私政策", foot_afdian="爱发电（完整版解锁）",
        note1="本站含 BL 向内容，角色均为成年人设定。",
        note2="内容为虚构创作。",
        cta_p="看完图鉴，测测你属于哪一种？",
        cta_q="开始浓度测试", cta_v="看频道视频",
        priv_lede="本站含成人向（BL）虚构内容。我们收集的数据、Cookie 用途与你的权利，都在这页讲清楚。",
    ),
    "en": dict(
        HTMLLANG="en", LANGLABEL="English",
        nav_cols="Columns", nav_work="The Work", nav_fly="Universe",
        nav_quiz="Vibe Test", nav_conc="Concentration", nav_vid="Videos", nav_join="demo soon",
        nav_serial="Serial", nav_know="About Gay", nav_vn="Visual Novel", nav_novel="Novel",
        foot_site="Site", foot_comm="Community", foot_note="Note",
        foot_cols_a="Columns", foot_work="The Work", foot_quiz="Vibe Test",
        foot_conc="Concentration", foot_vid="Videos", foot_priv="Privacy", foot_afdian="Afdian (full version)",
        note1="This site contains BL (boy-love) content; all characters are adults.",
        note2="All content is fictional.",
        cta_p="Finished the almanac? Find out which type you are.",
        cta_q="Take the vibe test", cta_v="Watch channel videos",
        priv_lede="This site contains adult (BL) fiction. What we collect, how cookies are used, and your rights — all stated here.",
    ),
    "ja": dict(
        HTMLLANG="ja", LANGLABEL="日本語",
        nav_cols="栏目", nav_work="作品", nav_fly="宇宙",
        nav_quiz="濃度テスト", nav_conc="濃度分布", nav_vid="動画", nav_join="demo 近日",
        nav_serial="連載", nav_know="ゲイ入門", nav_vn="ビジュアルノベル", nav_novel="小説",
        foot_site="サイト", foot_comm="コミュニティ", foot_note="説明",
        foot_cols_a="栏目", foot_work="作品", foot_quiz="濃度テスト",
        foot_conc="濃度分布", foot_vid="動画", foot_priv="プライバシー", foot_afdian="Afdian（完全版）",
        note1="本サイトはBL（ボーイズラブ）向け。全キャラ成人設定。",
        note2="すべてフィクションです。",
        cta_p="図鑑を読んだら、あなたはどの型？",
        cta_q="濃度テストする", cta_v="チャンネル動画を見る",
        priv_lede="本サイトは成人向け（BL）フィクション。収集するデータ、Cookie の用途、あなたの権利をここで説明します。",
    ),
    "ko": dict(
        HTMLLANG="ko", LANGLABEL="한국어",
        nav_cols="栏目", nav_work="작품", nav_fly="유니버스",
        nav_quiz="농도 테스트", nav_conc="농도 분포", nav_vid="영상", nav_join="demo 곧",
        nav_serial="연재", nav_know="게이 알기", nav_vn="비주얼 노벨", nav_novel="소설",
        foot_site="사이트", foot_comm="커뮤니티", foot_note="설명",
        foot_cols_a="栏目", foot_work="작품", foot_quiz="농도 테스트",
        foot_conc="농도 분포", foot_vid="영상", foot_priv="개인정보", foot_afdian="아쥐발전（풀버전）",
        note1="이 사이트는 BL(보이즈러브) 콘텐츠를 포함. 모든 캐릭터는 성인.",
        note2="모든 콘텐츠는 허구입니다.",
        cta_p="도감을 읽었으면, 당신은 어느 형?",
        cta_q="농도 테스트하기", cta_v="채널 영상 보기",
        priv_lede="이 사이트는 성인용(BL) 허구물입니다. 수집하는 데이터, Cookie 용도, 귀하의 권리를 이 페이지에서 설명합니다.",
    ),
}

# 图鉴正文（5 slug × 4 语）
CONTENT = {
    "swim-jock": {
        "zh": dict(
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
        "en": dict(
            tag="Almanac 01 · The Almanac",
            title="Swim-Team Jock Field Guide: the water-gifted type, wetness is a passive skill",
            lede="A swim-team jock isn't 'a hot guy who can swim' — he's a separate species. Outsiders see pecs and slides; we see a complete poolside survival philosophy.",
            desc="Swim-team jock field guide: slides are his formal wear, drying speedos is a dark art, white socks + slides is a legal right — an underrated athletic subspecies.",
            tags=["Water-gifted", "Relaxed but presentable", "Slow burn, addictive"],
            body="""
      <p>You don't size up a swim-team jock by how many years he's trained. You size him up by how put-together he looks the second he steps out of the pool. Everyone else just 'finished a workout'; he just 'retreated from his home court' — slides on, towel slung over a shoulder, as if that whole soaking was somebody else's business.</p>
      <h2>Slides are his formal wear</h2>
      <p>A swim jock's devotion to slides rivals a baller's devotion to his AJs. Not just any pair — the one he can stomp into the locker-room tile cracks without a flinch. On dry land, any 'formal' occasion, slides are automatically valid. Ask him why and he'll say 'habit.' Habit is this species' most advanced word.</p>
      <div class="alm-quote">Where a speedo dries fastest is a question a swim jock researches in earnest — not a joke.</div>
      <h2>Drying speedos is a dark art</h2>
      <p>Balcony orientation, ventilation time, whether a roommate's wet towel landed on it — outsiders can't read this decision tree, but every swim jock can optimize it eyes closed. It's spatial-management talent, dimensionally reduced, applied to the locker-room scenario.</p>
      <h2>The legal right of white socks + slides</h2>
      <p>In the swim jock's world, white socks aren't a fit — they're an identity claim. Step out of the water, pull on white socks and slides: the lowest-cost declaration of 'I'm still a jock.' The White Sock Studies piece later takes apart this sign; for now, a hook.</p>
      <h2>Wetness is a passive skill</h2>
      <p>Don't misread it — a swim jock isn't showing off. The instant he hits the water, a passive skill fires: feel for the water, the lines, that 'earth-time-paused' ease. Chasers call it vibe; it's actually the factory setting of a gifted type.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 01 · The Almanac",
            title="水泳部体育生図鑑：水感の天才型、濡れるはパッシブスキル",
            lede="水泳部の体育生は「泳げるイケメン」ではない。別の種だ。部外者は胸筋とスライダーを見るが、我々は完全なプールサイド生存哲学を見る。",
            desc="水泳部体育生図鑑：スライダーは正装、水着の干し方は奥義、白ソックス＋スライダーは合法権——過小評価された体育生亜種。",
            tags=["水感の才能", "リラックス×身だしなみ", "じわじわハマる"],
            body="""
      <p>水泳部の体育生を測るにあたり、何年やったかではなく、プールを上がった瞬間の身だしなみで測る。他人は「さっき運動した」だが、彼は「本拠地から撤退してきた」だ——スライダー履き、タオル担ぎ、まるで今の濡れは他人事のよう。</p>
      <h2>スライダーは彼の正装</h2>
      <p>水泳部のスライダー愛は、バスケ男子のAJ愛に匹敵する。ただの一足ではない。ロッカーのタイル目地に踏み込んでも動じない一足だ。陸の「フォーマル」な場でも、スライダーは自動的にアリ。なぜか聞けば「クセ」と言う——クセこそこの種の最上位語彙。</p>
      <div class="alm-quote">水着が一番早く乾く場所は、水泳部が真剣に研究する学術的問題だ。冗談ではない。</div>
      <h2>水着の干し方は奥義</h2>
      <p>ベランダの向き、風通しの時間、寮の湿ったタオルが乗っていないか——この決定木は部外者には読めないが、水泳部は目をつぶって最適化できる。それは空間管理の才能がロッカーという場に次元削減されて降臨したものだ。</p>
      <h2>白ソックス＋スライダーの合法権</h2>
      <p>水泳部の文脈では、白ソックスはコーデではなくアイデンティティの宣言だ。水から上がって白ソックスを履きスライダーを履くのは、「俺はまだ体育生だ」という最低コストの意思表示。後編『白ソックス研究』でこのサインを解体する。今はフックだけ。</p>
      <h2>濡れるはパッシブスキル</h2>
      <p>誤解しないで——水泳部は見せびらかしているのではない。水に入った瞬間、パッシブスキルが発動する。水感、ライン、あの「地球の時間が止まった」ような脱力。追う側は雰囲気だと思うが、実は才能型の出荷設定だ。</p>
            """,
        ),
        "ko": dict(
            tag="도감 01 · The Almanac",
            title="수영부 운동선수 도감: 물 감각 천재형, 젖는 건 패시브 스킬",
            lede="수영부 운동선수는 '수영 잘하는 훈남'이 아니다. 별개의 종이다. 외부인은 가슴근육과 슬라이더를 보지만, 우리는 완전한 풀사이드 생존 철학을 본다.",
            desc="수영부 운동선수 도감: 슬라이더는 정장, 수영복 말리는 건 비학, 흰 양말+슬라이더는 합법적 권리——과소평가된 운동선수 아종.",
            tags=["물 감각 천재", "릴렉스×단정", "느리게 하지만 중독성"],
            body="""
      <p>수영부 운동선수를 가를 때 몇 년 했는지가 아니라, 풀에서 올라온 순간의 단정함으로 본다. 남들은 '방금 운동했다'지만, 그는 '홈그라운드에서 철수했다'——슬라이더 신고, 수건 둘러메고, 마치 방금 젖은 게 남의 일인 듯.</p>
      <h2>슬라이더는 그의 정장</h2>
      <p>수영부의 슬라이더 천하는 농구부의 AJ 천하에 필적한다. 아무 신발이 아니다. 로커 타일 틈에 밟고 들어가도 눈 하나 깜짝 안 하는 그 한 켤레다. 육지의 '정장' 자리라도 슬라이더는 자동 합격. 왜 그러냐 묻으면 '습관'이라 답한다——습관은 이 종의 최상위 어휘다.</p>
      <div class="alm-quote">수영복이 가장 빨리 마르는 곳은 수영부가 진지하게 연구하는 학술적 문제다. 농담 아님.</div>
      <h2>수영복 말리기는 비학</h2>
      <p>발코니 방향, 통풍 시간, 룸메이트 젖은 수건이 올라왔는지——이 결정 트리는 외부인은 못 읽지만, 수영부는 눈 감고 최적화한다. 그것은 공간 관리 재능이 로커라는 장면에 차원 축소되어 강림한 것.</p>
      <h2>흰 양말+슬라이더의 합법적 권리</h2>
      <p>수영부 문맥에서 흰 양말은 코디가 아니라 정체성 선언이다. 물에서 올라와 흰 양말 신고 슬라이더 신는 건 '난 아직 운동선수다'라는 최저비용의 의사표시. 후편 '흰 양말 연구'에서 이 사인을 해체한다. 지금은 낚시성 훅만.</p>
      <h2>젖는 건 패시브 스킬</h2>
      <p>오해 마라——수영부가 뽐내는 게 아니다. 물에 들어가는 순간 패시브 스킬이 발동한다. 물 감각, 라인, 그 '지구의 시간이 멈춘' 듯한 이완. 쫓는 이는 분위기라 하지만, 실은 재능형의 출하 설정이다.</p>
            """,
        ),
    },
    "fake-jock": {
        "zh": dict(
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
        "en": dict(
            tag="Almanac 02 · The Gaze",
            title="How to Spot a Fake Jock: templates and real ones differ by the salt-stain",
            lede="How do you spot a 'posed jock' at a glance? Not by abs photos — by whether he carries the honest marks training leaves behind.",
            desc="Fake-jock spotter's guide: template jocks vs real ones, the difference is in gear, salt-stains and devotion to equipment — re-narrating sports through a gay lens.",
            tags=["Sharp eye", "No calling out", "Spectator mode"],
            body="""
      <p>We respect every form of expression, but a field guide needs a standard for real vs fake. This isn't critique — it's connoisseurship. After all, spotting a template at a glance is its own pleasure.</p>
      <h2>Template type: filter legs + never sweats</h2>
      <p>The tells are eerily consistent: equipment always brand new, selfies always at a 45-degree angle, captions always 'tried hard today.' The problem — he carries none of the honest marks training leaves. Sweat is the jock's most honest evidence, and he happens to have none.</p>
      <div class="alm-quote">The real one wraps his gear and wears salt-stains; the template only wraps filters and leaves captions blank.</div>
      <h2>Real type: gear is a medal</h2>
      <p>The baller's ankle guard, the lifter's wrist wrap, the swim jock's frayed slides — these aren't equipment, they're time certificates. A real one's devotion to gear is written in the wear, not the label.</p>
      <h2>Not calling out is basic manners</h2>
      <p>The point of spotting isn't to argue — it's to see sharper and chat better. The most seductive thing in this scene is the unspoken 'I get it but I won't say it.' Max out the spectator mode; that's what makes the guide fun.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 02 · The Gaze",
            title="にせ体育生を見破る指南：テンプレと本物の差は汗じわ",
            lede="『演った体育生』を一瞬で見破るには？腹筋写真ではなく、彼がトレーニングの跡である正直な痕を帯びているかで。",
            desc="にせ体育生鑑別ガイド：テンプレ体育生vs本物、差は防具・汗じわ・装備への信仰——gayの眼でスポーツを再解説。",
            tags=["観察眼", "見破らない", "傍観モード"],
            body="""
      <p>表現は何でも尊重するが、図鑑が真偽を語るなら基準が必要だ。これは批判ではなく、鑑賞である。テンプレを一瞬で見抜けるのも、また一興だから。</p>
      <h2>テンプレ型：フィルタ脚＋汗をかかない</h2>
      <p>特徴は不気味なほど揃う。器具はいつも新品、自撮りはいつも45度、キャプションはいつも『今日も頑張った』。問題は、トレーニングの跡である正直な痕を一つも帯びていないこと。汗は体育生の最も正直な証拠だが、彼にはたまたまそれがない。</p>
      <div class="alm-quote">本物は防具を巻き汗じわを刻む。テンプレはフィルタを巻きキャプションを空白にする。</div>
      <h2>本物型：防具は勲章</h2>
      <p>バスケ男子のアンクルガード、挙重のリストラップ、水泳部のほつれスライダー——これらは装備ではなく、時間の証明書だ。本物の装備への信仰は、ラベルではなく擦り減りに書かれている。</p>
      <h2>見破らないのは基本の作法</h2>
      <p>見抜く意味は言いがかりではなく、より鋭く見て、より楽しく語るためだ。この界隈で最も魅力的なのは、『わかってるけど言わない』という黙契。傍観モードを最大化——それが図鑑を面白くする。</p>
            """,
        ),
        "ko": dict(
            tag="도감 02 · The Gaze",
            title="가짜 운동선수 구별 가이드: 템플릿과 진짜는 땀얼룩으로 갈린다",
            lede="‘연출한 운동선수’를 한눈에 알아보는 법? 복근 사진이 아니라, 훈련이 남긴 정직한 자국을 지녔는지로.",
            desc="가짜 운동선수 감별 가이드: 템플릿 운동선수 vs 진짜, 차이는 보호구·땀얼룩·장비에 대한 신앙——gay의 눈으로 스포츠를 재해설.",
            tags=["관찰안목", "깨지 않는", "구경꾼 모드"],
            body="""
      <p>표현은 무엇이든 존중하지만, 도감이 진위를 논하려면 기준이 필요하다. 이것은 비판이 아니라 감상이다. 템플릿을 한눈에 알아보는 것도 또 다른 즐거움이니까.</p>
      <h2>템플릿형: 필터 다리＋땀 안 흘림</h2>
      <p>특징이 섬뜩할 만큼 일치한다. 기구는 늘 새것, 셀카는 늘 45도, 캡션은 늘 ‘오늘도 열심히’. 문제는 훈련이 남긴 정직한 자국을 하나도 지니지 않았다는 것. 땀은 운동선수의 가장 정직한 증거인데, 그는 마침 그것이 없다.</p>
      <div class="alm-quote">진짜는 보호구를 감고 땀얼룩을 새긴다. 템플릿은 필터를 감고 캡션을 비운다.</div>
      <h2>진짜형: 보호구는 훈장</h2>
      <p>농구부의 발목 보호대, 역도의 손목 밴드, 수영부의 흐트러진 슬라이더——이것들은 장비가 아니라 시간의 증명서다. 진짜의 장비에 대한 신앙은 라벨이 아니라 닳음에 적혀 있다.</p>
      <h2>깨지 않는 건 기본 매너</h2>
      <p>알아보는 의미는 시비가 아니라, 더 날카롭게 보고 더 즐겁게 놀리기 위해서다. 이 동네에서 가장 매력적인 건 ‘알지만 말진 않는’ 침묵의 밀약. 구경꾼 모드를 풀가동——그것이 도감을 재미있게 한다.</p>
            """,
        ),
    },
    "locker-room": {
        "zh": dict(
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
        "en": dict(
            tag="Almanac 03 · Locker Room Studies",
            title="Locker-Room Studies: the jock's third space, and where that rainy-night scene in 'Jocks' came from",
            lede="The locker room isn't a changing corridor — it's the jock's cultural scene: order, slang, a sense of boundaries.",
            desc="Locker-room studies: read the jock through spatial order and in-group slang — also the inspiration for the rainy-night scene in the 'Jocks' visual novel.",
            tags=["Spatial sociology", "Sense of boundaries", "Bromance narrative"],
            body="""
      <p>If you could pick just one place to understand the jock, it isn't the court — it's the locker room. It compresses every unwritten rule: whose cubby, who showers first, don't grab the wrong towel — a tacit etiquette that out-governs any team rule.</p>
      <h2>Third space, not a changing room</h2>
      <p>For the jock, the locker room sits between 'the field' and 'life': a place to exhale, and where relationships ferment. Many a bromance starts here. The rainy-night scene we wrote for 'Jocks' drew exactly from this half-public, half-private tension.</p>
      <div class="alm-quote">When the locker-room lights go off, the things jocks left unsaid finally start speaking.</div>
      <h2>Slang is the entry ticket</h2>
      <p>'Partner-in-crime,' 'spot me,' 'grab a shower' — outsiders don't get these words; insiders read them instantly. Slang never functions to keep secrets; it quickly confirms 'you're one of us.'</p>
      <h2>A sense of boundaries is the advanced part</h2>
      <p>The best-written jock stories don't cross lines for cheap shock — they build tension through boundaries. Respect the space, respect the characters, and it lands harder. That's also a red line in our content method: insider view, no consumption.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 03 · Locker Room Studies",
            title="更衣室考：体育生の第三空間、そして『体育生』雨夜のシーンの出処",
            lede="更衣室は着替えの通路ではない。体育生の文化的現場だ。秩序、隠語、境界感がある。",
            desc="更衣室考：空間秩序と内輪隠語から体育生を読む——これは『体育生』ビジュアルノベルの雨夜のシーンの灵感元でもある。",
            tags=["空間社会学", "境界感", "ブロマンス叙事"],
            body="""
      <p>体育生を読み解く場所を一つだけ選べと言われたら、コートではなく更衣室だ。そこには言わずもがなのルールが凝縮されている。誰のロッカー、誰が先にシャワー、タオルを間違えるな——チーム規則以上に効く暗黙のエチケット。</p>
      <h2>第三空間、着替え場ではない</h2>
      <p>体育生にとって更衣室は『試合』と『生活』の間にある。息をつける場であり、関係が発酵する場でもある。多くのブロマンスはここから始まる。『体育生』の雨夜のシーンは、この半ば公・半ば私の張力から引いた。</p>
      <div class="alm-quote">更衣室の灯りが消えると、体育生たちの言わずじまいのことが、ようやく口を開く。</div>
      <h2>隠語は入場券</h2>
      <p>『相棒』『フォロー頼む』『シャワー浴びる』——これらの言葉は部外者には通じず、内輪は即座に了解する。隠語の役割は秘密にするためではなく、『お前も仲間だ』と素早く確認することだ。</p>
      <h2>境界感こそが上質</h2>
      <p>よく書かれた体育生物語は、境界を越えて安易に煽らない。境界感で張力を作る。空間を、人物を尊重すれば、余韻が残る。それは我々のコンテンツ手法の赤線でもある。内側からの視点、消費しない。</p>
            """,
        ),
        "ko": dict(
            tag="도감 03 · Locker Room Studies",
            title="탈의실 고찰: 운동선수의 제3의 공간, 그리고 『운동선수』 비 오는 밤 장면의 출처",
            lede="탈의실은 옷 갈아입는 복도가 아니다. 운동선수의 문화적 현장이다. 질서, 은어, 경계감이 있다.",
            desc="탈의실 고찰: 공간 질서와 내부 은어로 운동선수를 읽는다——이것은 『운동선수』 비주얼노벨 비 오는 밤 장면의 영감이기도 하다.",
            tags=["공간사회학", "경계감", "브로맨스 서사"],
            body="""
      <p>운동선수를 읽을 장소를 하나만 고르라면, 코트가 아니라 탈의실이다. 말하지 않아도 통하는 규칙이 거기에 응축된다. 누구 사물함, 누가 먼저 샤워, 수건 헷갈리지 마라——팀 규정 이상으로 작동하는 암묵의 에티켓.</p>
      <h2>제3의 공간, 탈의장이 아님</h2>
      <p>운동선수에게 탈의실은 ‘경기’와 ‘삶’ 사이에 있다. 숨 돌릴 곳이자, 관계가 발효하는 곳이기도 하다. 많은 브로맨스는 여기서 시작된다. 『운동선수』의 비 오는 밤 장면은 이 반공·반사적 긴장에서 끌어왔다.</p>
      <div class="alm-quote">탈의실 불이 꺼지면, 운동선수들이 말하지 못한 것들이 비로소 입을 연다.</div>
      <h2>은어는 입장권</h2>
      <p>‘짝꿍’ ‘받쳐줘’ ‘샤워 좀’——이 말들은 외부인에겐 통하지 않고, 내부인은 즉시 납득한다. 은어의 역할은 비밀을 지키는 게 아니라, ‘너도 우리 편’임을 빠르게 확인하는 것이다.</p>
      <h2>경계감이야말로 고급</h2>
      <p>잘 쓰인 운동선수 이야기는 경계를 넘어 싼 충격을 안 판다. 경계감으로 긴장을 만든다. 공간을, 인물을 존중하면 여운이 남는다. 그것은 우리 콘텐츠 방법론의 레드라인이기도 하다. 내부 시선, 소비하지 않음.</p>
            """,
        ),
    },
    "white-sock": {
        "zh": dict(
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
        "en": dict(
            tag="Almanac 04 · White Sock Studies",
            title="White Sock Studies: why white socks are the jock's secret signal",
            lede="Subculture philology time. White socks aren't a fashion item — they're the lowest-cost identity claim of the jock.",
            desc="White sock studies: subculture philology — white socks as the jock's identity claim and in-group signal. Fetish-aware but not vulgar; a conversation-and-share generator.",
            tags=["Semiotics", "Fetish-aware, not vulgar", "In-group meme"],
            body="""
      <p>First, a disclaimer: this is subculture philology, not a fetish display case. We're talking about a sign — a visual signal the in-group claims, knowingly, between themselves.</p>
      <h2>The lowest-cost identity claim</h2>
      <p>No tattoo, no gear-stacking. A pair of white socks is enough. Cheap, everyday, explainable — yet in the eyes of a fellow, it completes a silent 'I get it.' A low-barrier, high-recognition sign is the most durable in subculture.</p>
      <div class="alm-quote">The sexiness of white socks isn't in the cloth — it's in the knowing smile of 'I happen to be that kind of person too.'</div>
      <h2>Why white, not black</h2>
      <p>White is more fragile, more honest — dirty, wet, pilled, all visible, that kind of real. The jock's charm is precisely in 'unretouched real.' White socks amplify that into a sign, and it becomes the signal.</p>
      <h2>Small talk, not a boundary</h2>
      <p>We use it to generate small talk and shareability, but never as a ruler to judge others. The premise of a fun sign is that everyone knows: a person is far richer than any sign.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 04 · White Sock Studies",
            title="白ソックス研究：なぜ白ソックスは体育生の合図なのか",
            lede="亜文化考証の時間。白ソックスはコーデアイテムではない。体育生の最低コストのアイデンティティ宣言だ。",
            desc="白ソックス研究：亜文化考証、体育生のアイデンティティ宣言であり内輪の合図としての白ソックス——フェティッシュを意識しつつ下品ではない、話題と共有欲の生成機。",
            tags=["記号論", "フェティッシュを意識しつつ下品でない", "内輪ネタ"],
            body="""
      <p>まず断っておく。これは亜文化考証であって、フェティッシュ展示ケースではない。我々が語るのはサインだ。内輪が互いに、わかっていて認める視覚的合図。</p>
      <h2>最低コストのアイデンティティ宣言</h2>
      <p>タトゥーも、装備の積み上げもいらない。白ソックス一足で足りる。安く、日常で、言い訳できる——それでいて同好の目には『わかってるね』という無言の完了を果たす。低ハードル・高認識のサインは亜文化で最も長持ちする。</p>
      <div class="alm-quote">白ソックスのセクシーさは布にあるのではない。『俺もたまたまそういう人間だ』という心の中の微笑みにある。</div>
      <h2>なぜ白か、黒ではなく</h2>
      <p>白はより脆く、より正直だ。汚れても、濡れても、毛羽立っても、すべて見える、その種のリアル。体育生の魅力はまさに『修正なしのリアル』にある。白ソックスはそれをサインに増幅し、やがて合図になる。</p>
      <h2>話題であって、境界ではない</h2>
      <p>我々はこれを話題と共有欲に使うが、他人を測るものさしには決してしない。サインが面白い前提は、互いが知っていることだ。人はサインよりずっと豊かだ。</p>
            """,
        ),
        "ko": dict(
            tag="도감 04 · White Sock Studies",
            title="흰 양말 연구: 왜 흰 양말이 운동선수의 암호인가",
            lede="아문화 고증 시간. 흰 양말은 코디 아이템이 아니다. 운동선수의 최저비용 정체성 선언이다.",
            desc="흰 양말 연구: 아문화 고증, 운동선수의 정체성 선언이자 내부 암호로서의 흰 양말——페티시를 의식하되 저속하지 않음, 화제와 공유욕의 생성기.",
            tags=["기호학", "페티시 의식하되 저속하지 않음", "내부 밈"],
            body="""
      <p>먼저 밝힌다. 이것은 아문화 고증이지 페티시 전시케이스가 아니다. 우리가 말하는 건 사인(기호)이다. 내부인이 서로, 알면서도 인정하는 시각적 암호.</p>
      <h2>최저비용의 정체성 선언</h2>
      <p>타투도, 장비 쌓아올리기도 필요 없다. 흰 양말 한 켤레면 충분하다. 싸고, 일상적이고, 변명 가능——그러면서도 동호인의 눈엔 ‘통하지’라는 무언의 완성을 이룬다. 진입장벽 낮고 인식 높은 사인은 아문화에서 가장 오래 간다.</p>
      <div class="alm-quote">흰 양말의 섹시함은 천에 있는 게 아니다. ‘나도 우연히 그런 부류다’라는 속마음의 미소에 있다.</div>
      <h2>왜 흰색인가, 검정이 아니라</h2>
      <p>흰색은 더 무르고, 더 정직하다. 더럽혀도, 젖어도, 보풀 올라와도, 모두 보이는, 그런 리얼. 운동선수의 매력은 바로 ‘수정 없는 리얼’에 있다. 흰 양말은 그것을 사인으로 증폭하고, 결국 암호가 된다.</p>
      <h2>화젯거리이지, 경계가 아니다</h2>
      <p>우리는 이것을 화제와 공유욕에 쓰되, 타인을 재는 자로는决不 쓰지 않는다. 사인이 재미있는 전제는, 서로가 아는 것이다. 사람은 사인보다 훨씬 풍부하다.</p>
            """,
        ),
    },
    "basketball": {
        "zh": dict(
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
        "en": dict(
            tag="Almanac 05 · Basketball Field Guide",
            title="Basketball Jock Field Guide: bring the baller out of the 'gay-fandom eye-candy' template",
            lede="The baller has been templated too long — ankle guards, AJs, trash-talk in pickup. But the real one has far more substance.",
            desc="Basketball jock field guide: ankle guards, sneaker collection, what lives under a body of sweat — bring the baller out of the 'gay-fandom eye-candy' template.",
            tags=["Bounce and salt", "Trash-talk pride", "Collector's self-awareness"],
            body="""
      <p>The baller is the most templated branch of jocks: mention him and it's AJs, abs, 1v1. Templates bring traffic, but they don't keep people. We want to bring him out, restore him as someone with substance.</p>
      <h2>Ankle guard closer than a partner</h2>
      <p>Not a bit — it's a ranking. A baller's care for ankle guards and tape is muscle memory left by training. You think he cares about gear; really he cares about 'being able to play ten more years.'</p>
      <div class="alm-quote">After a half, his jersey can be wrung out — but he says 'just messing around.' That's the romance of pickup: all in the trash-talk.</div>
      <h2>The self-discipline of a sneaker collector</h2>
      <p>AJs aren't bragging, they're faith. Every pair has a story of the feet that wore them: which dunk over whom, which pair went bald at the sole. The collection list is this species' private chronicle.</p>
      <h2>What lives under a body of sweat</h2>
      <p>Strip the template and the baller is the type who feels deeply, plays to win, and is loyal to his brothers. Next time you see a baller, don't just look at the abs — look at the unconvinced eyes after he got stuffed. That's the real text.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 05 · Basketball Field Guide",
            title="バスケ体育生図鑑：バスケ男子を『ゲイ界の美形』テンプレから引き出す",
            lede="バスケ男子はテンプレ化されすぎた——アンクルガード、AJ、ストリートの口の減らなさ。でも本物はテンプレよりずっと厚い。",
            desc="バスケ体育生図鑑：アンクルガード、スニーカー収集、一身の汗の下に住むもの——バスケ男子を『ゲイ界の美形』テンプレから引き出す。",
            tags=["跳躍と塩", "口は減らない", "収集家の自覚"],
            body="""
      <p>バスケ男子は体育生の中で最もテンプレ化された枝だ。名前を出せばAJ、腹筋、1on1。テンプレは流量を呼ぶが、人は残らない。彼を引き出し、厚みのある人として還元したい。</p>
      <h2>アンクルガードは彼氏より親しい</h2>
      <p>冗談ではない、順位だ。バスケ男子のアンクルガードやテープへの執着は、訓練が残した筋肉記憶だ。装備を気にしてるように見えるが、本当は『あと10年はできる』ことを気にしている。</p>
      <div class="alm-quote">ハーフを終えるとジャージを絞れる——でも『適当にやった』と言う。ストリートの浪漫はすべて口の減らなさにある。</div>
      <h2>スニーカー収集家の修養</h2>
      <p>AJは自慢ではなく信仰だ。一足ずつ履いた足の物語がある。誰をダンクしたか、どの底がすり減ったか。収集リストはこの種の私的編年史だ。</p>
      <h2>一身の汗の下に住むもの</h2>
      <p>テンプレを剥ぐと、バスケ男子は感情が深く、勝負にこだわり、兄弟に義理堅い種だ。次にバスケ男子を見たら、腹筋だけ見るな。ブロックされた後のあの納得いかない眼を見よ。それが正文だ。</p>
            """,
        ),
        "ko": dict(
            tag="도감 05 · Basketball Field Guide",
            title="농구 운동선수 도감: 농구부를 ‘게이계 미남’ 템플릿에서 끄집어내기",
            lede="농구부는 너무 일찍 템플릿화됐다——발목 보호대, AJ, 조별의 입바른소리. 하지만 진짜는 템플릿보다 훨씬 두텁다.",
            desc="농구 운동선수 도감: 발목 보호대, 스니커 수집, 한 몸의 땀 아래 사는 것——농구부를 ‘게이계 미남’ 템플릿에서 끄집어내기.",
            tags=["점프와 소금", "입바른소리 자부심", "수집가의 자각"],
            body="""
      <p>농구부는 운동선수 중 가장 템플릿화된 가지다. 이름만 꺼내면 AJ, 복근, 1on1. 템플릿은 트래픽을 부르지만 사람은 남지 않는다. 그를 끄집어내, 두께 있는 사람으로 환원하고 싶다.</p>
      <h2>발목 보호대는 짝보다 가깝다</h2>
      <p>농담이 아니다, 순위다. 농구부의 발목 보호대나 테이프에 대한 집착은 훈련이 남긴 근육 기억이다. 장비를 신경 쓰는 듯 보이지만, 진짜는 ‘앞으로 10년 더 뛸 수 있게’를 신경 쓴다.</p>
      <div class="alm-quote">하프를 마치면 저지를 짜낼 수 있다——근데 ‘그냥 놀았지’라 한다. 조별의 로맨스는 모두 입바른소리에 있다.</div>
      <h2>스니커 수집가의 수양</h2>
      <p>AJ는 자랑이 아니라 신앙이다. 한 켤레마다 신은 발의 이야기가 있다. 누구를 덩크했는지, 어느 밑창이 닳았는지. 수집 목록은 이 종의 사적 편년사다.</p>
      <h2>한 몸의 땀 아래 사는 것</h2>
      <p>템플릿을 벗기면, 농구부는 감정이 깊고, 승부에 집착하며, 형들에게 의리 있는 종이다. 다음에 농구부를 보면 복근만 보지 마라. 블락(블록)당한 후의 그 납득 못 한 눈을 보라. 그것이 본문이다.</p>
            """,
        ),
    },
    "coach-jock": {
        "zh": dict(
            tag="图鉴 06 · The Almanac",
            title="教练体育生图鉴：纪律是出厂设置，哨声是情话",
            lede="教练不是「凶一点的体育老师」。他是被纪律打磨过的人形边界，是场边权威和私下底线的活体反差。",
            desc="教练体育生图鉴：口令即情话、哨声划边界、场边权威与私下底线的反差——体育生宇宙里最上头的 authority 型。",
            tags=["纪律型性感", "权威反差", "慢热压场"],
            body="""
      <p>判定一个教练，别看他的腹肌（虽然通常在线），看他在场边说「再来一组」时的语气。那不是命令，是仪式。他把纪律活成了一种性感，你以为是压迫，其实是被打磨过的专注在发光。</p>
      <h2>口令即情话</h2>
      <p>「看我」「跟上」「别松」——教练的口令短、准、不带废话。听久了你会发现，这些词在另一种语境里全是情话。他不是在管教，他是在用最低成本把一群人拧成一股绳。这种把权威压成关心的本事，是这个物种最致命的出厂设置。</p>
      <div class="alm-quote">哨声一响是边界，哨声停下才是人。教练最性感的那一刻，永远是摘下哨子之后。</div>
      <h2>哨声划边界</h2>
      <p>教练的哨子不是乐器，是分寸。场上他是规则本身，场下他比谁都清楚那条线在哪。追教练的人最容易栽的坑，就是把场上的权威当成私下的态度——错。真正的教练，权威和温柔是分开关的，你得分清哪盏灯亮着。</p>
      <h2>场边权威 vs 私下底线的反差</h2>
      <p>这是 coach-jock 让人上头的核。他在三十个人面前能压住全场，关上门却可能是那个默默帮你收好护具的人。反差不是人设，是被纪律训练出来的克制：能掌控自己的人，才显得性感。看完这篇，去 quiz 测测你是被压的那个，还是压人的那个。</p>
            """,
        ),
        "en": dict(
            tag="Almanac 06 · The Almanac",
            title="Coach Field Guide: discipline is the factory setting, the whistle is a love line",
            lede="A coach isn't 'a PE teacher who's a bit strict.' He's a human-shaped boundary honed by discipline — the live contradiction of sideline authority and private softness.",
            desc="Coach field guide: the command as a love line, the whistle drawing the line, sideline authority vs private softness — the most addictive authority type in the jock universe.",
            tags=["Discipline as seduction", "Authority contrast", "Slow-burn, commanding"],
            body="""
      <p>To size up a coach, don't look at his abs (usually on point) — look at the tone when he says 'one more set' from the sideline. That's not an order, it's a ritual. He's turned discipline into something seductive; what reads as pressure is actually focus, polished.</p>
      <h2>The command is a love line</h2>
      <p>'Watch me.' 'Keep up.' 'Don't drop.' — a coach's commands are short, precise, no filler. Listen long enough and you realize those words are love lines in another context. He isn't disciplining; he's binding a group into one rope at the lowest cost. That knack for compressing authority into care is this species' deadliest factory setting.</p>
      <div class="alm-quote">The whistle blowing is the boundary; the whistle off is the human. A coach is hottest precisely in the moment he takes the whistle off.</div>
      <h2>The whistle draws the line</h2>
      <p>A coach's whistle isn't an instrument, it's proportion. On the field he is the rule itself; off it he knows exactly where that line sits. The trap chasers fall into: reading sideline authority as private attitude. Wrong. A real coach keeps authority and tenderness on separate switches — you have to tell which light is on.</p>
      <h2>Sideline authority vs private softness</h2>
      <p>This is the core that makes coach-jock addictive. He can hold a whole squad of thirty from the touchline, yet behind a closed door he might be the one quietly packing your pads away. The contrast isn't a persona — it's restraint trained by discipline: the man who controls himself is the one who looks seductive. Finished this piece? Take the quiz and find out whether you're the one pressed, or the one pressing.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 06 · The Almanac",
            title="コーチ体育生図鑑：規律は初期装備、ホイッスルは愛の言葉",
            lede="コーチは「少し厳しい体育の先生」ではない。規律に鍛えられた人型の境界線、つまり傍線の権威と私の裏側のギャップそのもの。",
            desc="コーチ体育生図鑑：号令は愛の言葉、ホイッスルが引く一線、傍線の権威と私の裏のギャップ——体育生宇宙で最もハマる authority 型。",
            tags=["規律という性感", "権威のギャップ", "緩やかで圧がある"],
            body="""
      <p>コーチを見る目安は腹筋ではない（それはたいてい完備）。傍線で「もう一回」と言う時のトーンだ。それは命令ではなく儀式。彼は規律を性感に変えていて、あなたが圧力だと思うのは、研ぎ澄まされた集中が光っているだけ。</p>
      <h2>号令は愛の言葉</h2>
      <p>「見て」「ついてこい」「離すな」——コーチの号令は短く、的確で、無駄がない。聞いていると気づく。これらの言葉は別の文脈では愛の言葉だ。彼は説教しているのではない。最小コストで一群を一本の縄に編んでいる。権威を慈しみに圧縮する才能が、この種の最も致命的な初期装備。</p>
      <div class="alm-quote">ホイッスルが鳴るのは境界、鳴りやむのは人間。コーチが最も色っぽいのは、ホイッスルを外した瞬間だ。</div>
      <h2>ホイッスルが引く一線</h2>
      <p>コーチのホイッスルは楽器ではなく分寸。フィールド上では彼が規則そのもの、下ではその線がどこかを誰より知っている。追う側が陥る罠は、傍線の権威を私の態度だと読むこと。違う。本物のコーチは権威と優しさを別のスイッチにしていて、どちらの灯が点いているかを見極めないといけない。</p>
      <h2>傍線の権威と私の裏のギャップ</h2>
      <p>これが coach-jock をハマらせる核。三十人の前で全体を押さえつつ、ドアの裏では黙ってあなたの防具を片づけるかもしれない。ギャップはペルソナではなく、規律で鍛えた抑制だ。自分をコントロールできる者こそ性感に見える。この図鑑を読んだら、quiz で測ってみよう。あなたは押される側か、押す側か。</p>
            """,
        ),
        "ko": dict(
            tag="도감 06 · The Almanac",
            title="코치 운동선수 도감: 규율은 기본 사양, 휘슬은 사랑의 한마디",
            lede="코치는 '조금 엄격한 체육 선생'이 아니다. 규율로 다듬어진 인간형 경계선, 즉 옆선의 권위와 사적인 부드러움의 살아있는 대비다.",
            desc="코치 운동선수 도감: 구호는 사랑의 한마디, 휘슬이 긋는 선, 옆선의 권위와 사적인 부드러움의 대비——스포츠맨 유니버스에서 가장 중독적인 authority형.",
            tags=["규율型 섹시함", "권위 대비", "천천히 압도"],
            body="""
      <p>코치를 보는 척도는 복근이 아니다(보통은 충분하다). 옆선에서 '한 세트 더'라고 할 때의 톤을 봐라. 그것은 명령이 아니라 의식이다. 그는 규율을 섹시함으로 바꿨고, 당신이 압력이라 생각하는 것은 다듬어진 집중이 빛나는 것뿐.</p>
      <h2>구호는 사랑의 한마디</h2>
      <p>'봐' '따라와' '놓치 마'——코치의 구호는 짧고, 정확하고, 잡담이 없다. 듣다 보면 깨닫는다. 이 말들은 다른 맥락에선 사랑의 한마디다. 그는 훈계하는 게 아니라 최소 비용으로 무리를 한 줄기로 묶고 있다. 권위를 보살핌으로 압축하는 재주가 이 종의 가장 치명적인 기본 사양.</p>
      <div class="alm-quote">휘슬이 울리는 건 경계, 울림이 멈추는 건 인간. 코치가 가장 섹시한 건 휘슬을 푸는 순간이다.</div>
      <h2>휘슬이 긋는 선</h2>
      <p>코치의 휘슬은 악기가 아니라 분수. 필드 위에선 그가 규칙 그 자체, 밑에선 그 선이 어딘지 누구보다 잘 안다. 쫓는 이가 빠지는 함정: 옆선의 권위를 사적인 태도로 읽는 것. 틀렸다. 진짜 코치는 권위와 부드러움을 따로 놓는 스위치라, 어떤 불이 켜졌는지 가려야 한다.</p>
      <h2>옆선의 권위 vs 사적인 부드러움</h2>
      <p>이것이 coach-jock을 중독시키는 핵심. 서른 명 앞에선 전체를 누르면서, 문 뒤에선 묵묵히 당신 보호구를 정리하는 이일 수 있다. 대비는 페르소나가 아니라 규율로 단련된 절제다. 자신을 통제하는 자만이 섹시해 보인다. 이 도감을 읽었으면 quiz로 측정해 봐라. 당신은 눌리는 쪽인가, 누르는 쪽인가.</p>
            """,
        ),
    },
    "gym-bro": {
        "zh": dict(
            tag="图鉴 07 · The Almanac",
            title="健身房撸铁怪图鉴：泵感是信仰，镜子是圣坛",
            lede="撸铁怪不是「爱健身的肌肉男」。他是把重量房过成修道院的人——泵感是他的高潮，镜子是他和自己的私会。",
            desc="健身房撸铁怪图鉴：泵感哲学、训练餐苦行、镜子前的自我凝视——体育生宇宙里最虔诚的 gains 型。",
            tags=["泵感信仰", "训练餐苦行", "自我凝视"],
            body="""
      <p>判定一个撸铁怪，不看他卧推多少，看他练完照镜子时的眼神。那不是自恋，是确认。他刚和重量谈了一场恋爱，现在要亲眼看看战利品。镜子对他而言不是 Narcissus 的池塘，是复盘用的圣坛。</p>
      <h2>泵感是信仰</h2>
      <p>撸铁怪说的「泵」不是物理名词，是宗教体验。一组力竭之后血液涌进肌腹的那两分钟，他觉得自己无所不能。这种短暂的神性，是他扛着生活里所有破事还能笑出来的秘密燃料。你笑他上头，他笑你没体验过。</p>
      <div class="alm-quote">训练餐不是节食，是苦行。能把鸡胸和水煮蛋吃成仪式的人，意志力本身就是性感。</div>
      <h2>训练餐的苦行</h2>
      <p>外人看训练餐是受罪，撸铁怪看它是修行。七分吃三分练，他比谁都信。能把一辈子的鸡胸、燕麦、西兰花吃出纪律感的人，对欲望的掌控力远超你的想象。这种「对自己狠」的克制，恰恰是圈里最杀的荷尔蒙。</p>
      <h2>镜子前的自我凝视</h2>
      <p>撸铁怪和镜子的关系，比和大多数人都深。那不是自恋，是长期的、诚实的对视：今天掉了围度吗，线条更利了吗。他在镜前完成的和自己的谈判，比很多关系都认真。看懂这点，你就懂了为什么 gym 是体育生宇宙里最安静也最烈的那块场域。</p>
            """,
        ),
        "en": dict(
            tag="Almanac 07 · The Almanac",
            title="Gym-Bro Field Guide: the pump is faith, the mirror is the altar",
            lede="A gym bro isn't 'a muscular guy who likes fitness.' He's someone who runs the weight room like a monastery — the pump is his climax, the mirror his private meeting with himself.",
            desc="Gym-bro field guide: the philosophy of the pump, the asceticism of the training diet, the self-gaze before the mirror — the most devout gains type in the jock universe.",
            tags=["Pump as faith", "Ascetic training diet", "Self-gaze"],
            body="""
      <p>To size up a gym bro, don't look at his bench press — look at his eyes when he checks the mirror post-set. That isn't vanity, it's confirmation. He just made love to the weights and now wants to see the trophy. The mirror isn't Narcissus' pool to him; it's an altar for review.</p>
      <h2>The pump is faith</h2>
      <p>When a gym bro says 'the pump,' he doesn't mean a physics term — he means a religious experience. Those two minutes after a failure set, when blood floods the muscle belly, he feels capable of anything. That brief divinity is the secret fuel that lets him laugh through every shitty thing life throws. You mock his devotion; he pities you for never feeling it.</p>
      <div class="alm-quote">The training diet isn't restriction, it's asceticism. Whoever turns chicken breast and boiled eggs into ritual — their willpower alone is seductive.</div>
      <h2>The asceticism of the training diet</h2>
      <p>Outsiders see the training diet as suffering; the gym bro sees it as practice. 'Diet is seven parts, training three' — he believes it more than anyone. The man who can eat a lifetime of chicken, oats and broccoli with discipline has a grip on desire you can't imagine. That 'hard on himself' restraint is exactly the hormone that kills in this scene.</p>
      <h2>The self-gaze before the mirror</h2>
      <p>A gym bro's relationship with the mirror runs deeper than with most people. It isn't vanity, it's a long, honest stare: did the circumference drop today, are the lines sharper. The negotiation he completes with himself before the glass is more serious than many relationships. Get this and you understand why the gym is the quietest yet most intense field in the jock universe.</p>
            """,
        ),
        "ja": dict(
            tag="図鑑 07 · The Almanac",
            title="ジムバカ体育生図鑑：パンプは信仰、鏡は祭壇",
            lede="ジムバカは「筋トレ好きの筋肉男」ではない。ウェイトルームを修道院のように生きる者——パンプは絶頂、鏡は自分との密会だ。",
            desc="ジムバカ体育生図鑑：パンプの哲学、トレーニング食の苦行、鏡前の自己凝視——体育生宇宙で最も敬虔な gains 型。",
            tags=["パンプ信仰", "トレ食苦行", "自己凝視"],
            body="""
      <p>ジムバカを見る目安はベンチプレスではない。セット後の鏡の眼だ。それはナルシシズムではなく確認。彼はさっき重量と恋をして、今その戦利品を見たい。鏡は彼にとってナルキッソスの池ではなく、見直しの祭壇。</p>
      <h2>パンプは信仰</h2>
      <p>ジムバカが「パンプ」と言う時、物理用語ではなく宗教体験を指す。力竭後の二分間、血液が筋腹に溢れる時、彼は何でもできる気がする。その一瞬の神性が、人生のあらゆるクソつまらないことを笑って乗り越える秘密の燃料。あなたは熱狂を笑い、彼は経験のないあなたを憐れむ。</p>
      <div class="alm-quote">トレーニング食は制限ではなく苦行。鶏胸肉とゆで卵を儀式に変える者、その意志力こそが性感だ。</div>
      <h2>トレーニング食の苦行</h2>
      <p>部外者にはトレーニング食は苦痛だが、ジムバカには修行。『食事七割、トレ三割』——彼は誰より信じている。鶏肉とオートミールとブロッコリーを一生、規律を持って食べられる者は、欲望への統制力が想像を超える。その『自分に厳しい』抑制こそが、このシーンで最も殺すホルモン。</p>
      <h2>鏡前の自己凝視</h2>
      <p>ジムバカと鏡の関係は、たいていの人より深い。ナルシシズムではなく、長く正直なにらみ合いだ。今日囲みは落ちたか、線は鋭くなったか。ガラスの前で自分と完遂する交渉は、多くの関係より真剣。これがわかれば、なぜジムが体育生宇宙で最も静かで最も激しい場かがわかる。</p>
            """,
        ),
        "ko": dict(
            tag="도감 07 · The Almanac",
            title="헬창 운동선수 도감: 펌프는 신앙, 거울은 제단",
            lede="헬창은 '운동 좋아하는 근육남'이 아니다. 웨이트룸을 수도원처럼 사는 자——펌프는 절정, 거울은 자신과의 밀회다.",
            desc="헬창 운동선수 도감: 펌프의 철학, 식단의 고행, 거울 앞 자기 응시——스포츠맨 유니버스에서 가장 경건한 gains형.",
            tags=["펌프 신앙", "식단 고행", "자기 응시"],
            body="""
      <p>헬창을 보는 척도는 벤치프레스가 아니다. 세트 후 거울을 보는 눈을 봐라. 그것은 자기애가 아니라 확인. 그는 방금 중량과 사랑을 나눴고, 이제 전리품을 보고 싶어 한다. 거울은 그에게 나르시소스의 못이 아니라 점검의 제단.</p>
      <h2>펌프는 신앙</h2>
      <p>헬창이 '펌프'라 할 때 그것은 물리 용어가 아니라 종교적 경험이다. 렙을 채운 후 이분간, 피가 근육 속으로 밀려들 때 그는 뭐든 할 수 있을 것 같다. 그 잠깐의 신성함이 인생의 온갖 빌어먹을 일을 웃어넘기는 비밀 연료. 너는 열광을 비웃고, 그는 느껴본 적 없는 너를 불쌍히 여긴다.</p>
      <div class="alm-quote">식단은 제한이 아니라 고행. 닭가슴살과 삶은 계란을 의식으로 바꾸는 자, 그 의지력 자체가 섹시하다.</div>
      <h2>식단의 고행</h2>
      <p>남에겐 식단이 고통이지만 헬창에겐 수행이다. '식단이 칠할, 운동이 삼할'——그는 누구보다 믿는다. 닭가슴과 오트밀과 브로콜리를 평생 규율로 먹는 자는 욕망에 대한 통제력이 상상 그 이상. 그 '자신에게 매운' 절제야말로 이 씬에서 가장 치명적인 호르몬.</p>
      <h2>거울 앞 자기 응시</h2>
      <p>헬창과 거울의 관계는 대개 사람보다 깊다. 자기애가 아니라 길고 정직한 눈싸움이다. 오늘 둘레가 빠졌나, 선이 더 날카로워졌나. 유리 앞에서 자신과 끝내는 협상은 많은 관계보다 진지하다. 이것을 알면 왜 짐이 스포츠맨 유니버스에서 가장 조용하면서도 가장 뜨거운 장인지 이해하게 된다.</p>
            """,
        ),
    },
}

# 隐私政策正文（4 语）
PRIVACY = {
    "zh": dict(
        tag="说明 · Legal",
        title="隐私政策 · SportsBoy.gay",
        lede="本站含成人向（BL）虚构内容。我们收集的数据、Cookie 用途与你的权利，都在这页讲清楚。",
        desc="SportsBoy.gay 隐私政策：网站含成人向（BL）内容，说明我们收集的数据、Cookie 用途与你的权利。",
        tags=[],
        body="""
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
        """,
    ),
    "en": dict(
        tag="Note · Legal",
        title="Privacy Policy · SportsBoy.gay",
        lede="This site contains adult (BL) fiction. What we collect, how cookies are used, and your rights — all stated here.",
        desc="SportsBoy.gay privacy policy: the site contains adult (BL) content; explains the data we collect, cookie use, and your rights.",
        tags=[],
        body="""
      <p>SportsBoy.gay (hereinafter "the Site") is an adult-oriented jock-culture content site. The Site contains BL (boys' love) fiction; by accessing it you confirm you are at least 18 or the age of majority in your jurisdiction.</p>
      <h2>What we collect</h2>
      <p><b>Vibe test (quiz):</b> your score and result type are computed and shown in your browser locally and are generally not uploaded to our servers; result-share pages are public. We do not tie your specific answers to your identity.</p>
      <p><b>Contact &amp; subscription:</b> if we later enable subscriptions or email notices, we will state so clearly and only collect your email when you provide it voluntarily.</p>
      <p><b>Anonymous analytics:</b> we use a privacy-friendly analytics service (Vercel Web Analytics) that counts only anonymous visits, dwell time, and events (e.g. completing the test). <b>No cookies, no cross-site tracking, no data sold.</b></p>
      <h2>Cookies &amp; local storage</h2>
      <p>The Site may store a small amount of data in your browser locally, to remember your age-confirmation state and language preference. This stays on your device and involves no identity tracking.</p>
      <h2>Third-party content</h2>
      <p>The Site embeds YouTube videos; YouTube may process playback-related data under its own policy. Such content is governed by YouTube's privacy policy.</p>
      <h2>Your rights</h2>
      <p>You have the right to access, correct, or delete your personal data. Questions can be directed through the Site's public channels. All content is adult fiction and unrelated to real persons.</p>
        """,
    ),
    "ja": dict(
        tag="説明 · Legal",
        title="プライバシーポリシー · SportsBoy.gay",
        lede="本サイトは成人向け（BL）フィクション。収集するデータ、Cookie の用途、あなたの権利をここで説明します。",
        desc="SportsBoy.gay プライバシーポリシー：成人向け（BL）コンテンツを含むサイト。収集データ・Cookie 用途・権利を説明。",
        tags=[],
        body="""
      <p>SportsBoy.gay（以下「本サイト」）は成人向けの体育生文化コンテンツサイトです。本サイトはBL（ボーイズラブ）フィクションを含み、アクセスすることで、あなたが18歳以上、または所在法域の成年年齢以上であることを確認したものとします。</p>
      <h2>収集するもの</h2>
      <p><b>濃度テスト（quiz）：</b>スコアと結果型はブラウザ内で計算・表示され、原則サーバーに送信されません。結果共有ページは公開コンテンツです。具体的な回答をあなたの身元に結びつけることはありません。</p>
      <p><b>連絡・購読：</b>今後購読やメール通知を設ける場合、明示し、メール等はあなたが任意に提供した場合のみ収集します。</p>
      <p><b>匿名分析：</b>プライバシーに配慮した分析（Vercel Web Analytics）を使用し、匿名の訪問数・滞在時間・イベント（テスト完了等）のみを計測します。<b>Cookie 不使用、クロスサイト追跡なし、データ販売なし。</b></p>
      <h2>Cookie とローカルストレージ</h2>
      <p>本サイトはブラウザ内に少量のデータを保存し、年齢確認状態や言語設定を記憶する場合があります。これらはあなたの端末にのみ留まり、身元追跡を伴いません。</p>
      <h2>第三者コンテンツ</h2>
      <p>本サイトは YouTube 動画を埋め込みます。YouTube は自らのポリシーに基づき再生関連データを処理する場合があります。該当コンテンツは YouTube のプライバシーポリシーの対象です。</p>
      <h2>あなたの権利</h2>
      <p>あなたはご自身の個人データへのアクセス・訂正・削除を求める権利があります。疑問は本サイトの公開チャネルからお問い合わせください。本コンテンツはすべて成人向けフィクションで、実在の人物とは無関係です。</p>
        """,
    ),
    "ko": dict(
        tag="설명 · Legal",
        title="개인정보 처리방침 · SportsBoy.gay",
        lede="이 사이트는 성인용(BL) 허구물입니다. 수집하는 데이터, Cookie 용도, 귀하의 권리를 여기서 설명합니다.",
        desc="SportsBoy.gay 개인정보 처리방침: 성인용(BL) 콘텐츠 포함 사이트. 수집 데이터·Cookie 용도·권리 설명.",
        tags=[],
        body="""
      <p>SportsBoy.gay(이하 "사이트")는 성인 대상 운동선수 문화 콘텐츠 사이트입니다. 사이트는 BL(보이즈러브) 허구물을 포함하며, 접속 시 귀하가 만 18세 이상이거나 소재 관할의 성년 연령 이상임을 확인한 것으로 봅니다.</p>
      <h2>수집하는 것</h2>
      <p><b>농도 테스트(quiz):</b> 점수와 결과형은 브라우저 내에서 계산·표시되며 원칙적으로 서버로 전송되지 않습니다. 결과 공유 페이지는 공개 콘텐츠입니다. 구체적 답을 귀하의 신원과 연결하지 않습니다.</p>
      <p><b>연락·구독:</b> 향후 구독이나 이메일 알림을 마련할 경우 명시하고, 이메일 등은 귀하가 자발적으로 제공한 경우에만 수집합니다.</p>
      <p><b>익명 분석:</b> 개인정보 보호 친화적 분석(Vercel Web Analytics)을 사용하며, 익명 방문 수·체류 시간·이벤트(테스트 완료 등)만 측정합니다. <b>Cookie 없음, 교차 사이트 추적 없음, 데이터 판매 없음.</b></p>
      <h2>Cookie 및 로컬 저장</h2>
      <p>사이트는 브라우저에 소량의 데이터를 저장해 연령 확인 상태와 언어 설정을 기억할 수 있습니다. 이는 귀하의 기기에만 머물며 신원 추적을 수반하지 않습니다.</p>
      <h2>제3자 콘텐츠</h2>
      <p>사이트는 YouTube 동영상을 임베드합니다. YouTube는 자체 정책에 따라 재생 관련 데이터를 처리할 수 있습니다. 해당 콘텐츠는 YouTube 개인정보 처리방침의 적용을 받습니다.</p>
      <h2>귀하의 권리</h2>
      <p>귀하는 개인데이터에 대한 접근·정정·삭제를 요청할 권리가 있습니다. 문의는 사이트 공개 채널로 연락 주시기 바랍니다. 모든 콘텐츠는 성인 허구물이며 실존 인물과 무관합니다.</p>
        """,
    ),
}


TPL = """<!DOCTYPE html>
<html lang="__HTMLLANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="msvalidate.01" content="83a632faa92c4ae0bd1086de9dc2902a" />
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
__ALT_LINKS__
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
    <a class="brand" href="__HP__/">SPORTSBOY<span class="brand-tld">.gay</span></a>
    <nav class="nav-links" id="navLinks">
      <a href="__HP__/quiz">__NAV_QUIZ__</a>
      <a href="__HP__/videos">__NAV_VID__</a>
      <div class="nav-dropdown">
        <a href="__HP__/vn" class="nav-dropdown-toggle" aria-haspopup="true">__NAV_SERIAL__ <span class="caret">▾</span></a>
        <div class="nav-dropdown-menu">
          <a href="__HP__/vn">__NAV_VN__</a>
          <a href="__HP__/novel">__NAV_NOVEL__</a>
        </div>
      </div>
      <a href="__HP__/knowledge">__NAV_KNOW__</a>
      <a class="btn btn-primary btn-sm" href="__HP__/#join">__NAV_JOIN__</a>
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
          __LANGMENU__
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
__CTA_SECTION__
    </div>
  </article>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="__HP__/">SPORTSBOY<span class="brand-tld">.gay</span></a>
        <p>汗水、肌肉与骄傲，光明正大。</p>
      </div>
      <div class="footer-col">
        <h4>__FOOT_SITE__</h4>
        <a href="__HP__/#columns">__FOOT_COLS__</a>
        <a href="__HP__/#work">__FOOT_WORK__</a>
        <a href="__HP__/quiz">__FOOT_QUIZ__</a>
        <a href="__HP__/concentration">__FOOT_CONC__</a>
        <a href="__HP__/videos">__FOOT_VID__</a>
        <a href="__HP__/privacy">__FOOT_PRIV__</a>
      </div>
      <div class="footer-col">
        <h4>__FOOT_COMM__</h4>
        <a href="https://afdian.com/a/sportsboy" target="_blank" rel="noopener">__FOOT_AFD__</a>
        <a href="https://www.youtube.com/@sportsboygay" target="_blank" rel="noopener">YouTube</a>
        <a href="https://cbtdao.itch.io/sportsboy" target="_blank" rel="noopener">itch.io</a>
        <a href="https://x.com/sportsboygay" target="_blank" rel="noopener">X</a>
      </div>
      <div class="footer-col">
        <h4>__FOOT_NOTE__</h4>
        <p>__NOTE1__</p>
        <p>__NOTE2__</p>
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


def alt_links(base):
    """四语 hreflang 互指（与当前语言无关）。base 形如 /almanac/swim-jock 或 /privacy。"""
    rows = [
        ('zh-CN', '/almanac/' + base.lstrip('/almanac/')) if False else None,  # placeholder, replaced below
    ]
    # 显式构造
    path = base  # e.g. /almanac/swim-jock or /privacy
    hrefs = {
        "zh-CN": SITE + path,
        "en": SITE + "/en" + path,
        "ja": SITE + "/ja" + path,
        "ko": SITE + "/ko" + path,
        "x-default": SITE + path,
    }
    out = []
    for code in ["zh-CN", "en", "ja", "ko", "x-default"]:
        out.append('<link rel="alternate" hreflang="%s" href="%s">' % (code, hrefs[code]))
    return "\n".join(out)


def lang_menu(base, lang):
    opts = [
        ("zh-CN", "/almanac/" + base.lstrip("/almanac/"), "中文", "ZH") if False else None,
    ]
    path = base  # /almanac/slug or /privacy
    entries = [
        ("zh-CN", SITE + path, "中文", "ZH", "zh"),
        ("en", SITE + "/en" + path, "English", "EN", "en"),
        ("ja", SITE + "/ja" + path, "日本語", "JA", "ja"),
        ("ko", SITE + "/ko" + path, "한국어", "KO", "ko"),
    ]
    out = []
    for hl, href, label, tag, code in entries:
        active = ' class="lang-opt is-active" aria-current="true"' if code == lang else ' class="lang-opt"'
        out.append('<a%s href="%s" hreflang="%s" lang="%s">%s<span class="lang-opt-tag">%s</span></a>'
                   % (active, href, hl, hl, label, tag))
    return "\n          ".join(out)


def build(lang, base, d, cta=True):
    ui = UI[lang]
    hp = PREFIX[lang]
    t = TPL
    t = t.replace("__HTMLLANG__", ui["HTMLLANG"])
    t = t.replace("__LANGLABEL__", ui["LANGLABEL"])
    t = t.replace("__HP__", hp)
    t = t.replace("__NAV_COLS__", ui["nav_cols"])
    t = t.replace("__NAV_WORK__", ui["nav_work"])
    t = t.replace("__NAV_FLY__", ui["nav_fly"])
    t = t.replace("__NAV_QUIZ__", ui["nav_quiz"])
    t = t.replace("__NAV_CONC__", ui["nav_conc"])
    t = t.replace("__NAV_VID__", ui["nav_vid"])
    t = t.replace("__NAV_VN__", ui["nav_vn"])
    t = t.replace("__NAV_NOVEL__", ui["nav_novel"])
    t = t.replace("__NAV_SERIAL__", ui["nav_serial"])
    t = t.replace("__NAV_KNOW__", ui["nav_know"])
    t = t.replace("__NAV_JOIN__", ui["nav_join"])
    t = t.replace("__FOOT_SITE__", ui["foot_site"])
    t = t.replace("__FOOT_COLS__", ui["foot_cols_a"])
    t = t.replace("__FOOT_WORK__", ui["foot_work"])
    t = t.replace("__FOOT_QUIZ__", ui["foot_quiz"])
    t = t.replace("__FOOT_CONC__", ui["foot_conc"])
    t = t.replace("__FOOT_VID__", ui["foot_vid"])
    t = t.replace("__FOOT_PRIV__", ui["foot_priv"])
    t = t.replace("__FOOT_COMM__", ui["foot_comm"])
    t = t.replace("__FOOT_AFD__", ui["foot_afdian"])
    t = t.replace("__FOOT_NOTE__", ui["foot_note"])
    t = t.replace("__NOTE1__", ui["note1"])
    t = t.replace("__NOTE2__", ui["note2"])
    t = t.replace("__TITLE__", d["title"])
    t = t.replace("__DESC__", d["desc"])
    t = t.replace("__TAG__", d["tag"])
    t = t.replace("__LEDE__", d["lede"])
    t = t.replace("__BODY__", d["body"])
    t = t.replace("__TAGS__", "".join('<span>#%s</span>' % x for x in d.get("tags", [])))
    t = t.replace("__ANALYTICS__", ANALYTICS)
    t = t.replace("__ALT_LINKS__", alt_links(base))
    t = t.replace("__LANGMENU__", lang_menu(base, lang))
    if cta:
        cta_block = (
            '      <div class="alm-cta">\n'
            '        <p style="margin:0 0 12px">%s</p>\n'
            '        <a class="btn btn-primary" href="%s/quiz">%s</a>\n'
            '        <a class="btn btn-ghost" href="%s/videos">%s</a>\n'
            '      </div>' % (ui["cta_p"], hp, ui["cta_q"], hp, ui["cta_v"])
        )
        t = t.replace("__CTA_SECTION__", cta_block)
    else:
        t = t.replace("__CTA_SECTION__", "")
    canon = SITE + (PREFIX[lang] + base)
    t = t.replace("__OGURL__", canon)
    t = t.replace("__SITE__", SITE)
    return t


def main():
    # 图鉴 5 篇 × 4 语
    for slug in CONTENT.keys():
        base = "/almanac/" + slug
        for lang in PREFIX.keys():
            html = build(lang, base, CONTENT[slug][lang], cta=True)
            outdir = os.path.join(BASE, lang, "almanac") if lang != "zh" else os.path.join(BASE, "almanac")
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8") as f:
                f.write(html)
            print("wrote %s/almanac/%s.html" % (lang, slug))
    # 隐私页 × 4 语
    for lang in PREFIX.keys():
        html = build(lang, "/privacy", PRIVACY[lang], cta=False)
        outdir = os.path.join(BASE, lang, "privacy") if lang != "zh" else os.path.join(BASE, "privacy")
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote %s/privacy/index.html" % lang)
    print("DONE")


if __name__ == "__main__":
    main()
