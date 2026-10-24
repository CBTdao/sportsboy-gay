(function () {
  /* 语言从 <html lang> 读取：zh-CN / en / ja / ko */
  var lang = (document.documentElement.lang || "zh-CN").split("-")[0].toLowerCase();

  /* 人格结果分享页（程序化获客页，由 tools/gen_result_pages.py 生成） */
  var RESULT_BASE = {
    zh: "/quiz/result/",
    en: "/en/quiz/result/",
    ja: "/ja/quiz/result/",
    ko: "/ko/quiz/result/"
  };

  var I18N = {
    zh: {
      types: {
        swim: {
          name: "泳队体育生",
          desc: "水感天赋型。别人出汗靠练，你出汗靠下水。泳裤晾哪、白袜配什么鞋，是你认真研究的学术问题。泳池就是你的主场，湿身是你的被动技能。"
        },
        basketball: {
          name: "篮球体育生",
          desc: "弹跳与汗碱型。球鞋收藏家的自我修养，半场球衣就能透。护踝比对象亲，斗牛时嘴上说着随便打，心里记着每一次被盖。"
        },
        gym: {
          name: "健身房体育生",
          desc: "蛋白粉驱动型。体脂率是你的人生 KPI，镜子前的第 108 次展背依然充满热情。组间休息不忘补水，训练计划比恋爱计划详细。"
        },
        allround: {
          name: "全能体育生",
          desc: "什么都玩型。操场、球场、泳池、健身房，四处都有你的传说。天赋不知道点在哪，但浓度从来不掉线——真正的体育生，敢于全部都要。"
        }
      },
      questions: [
        {
          q: "周末最想去的场所？",
          options: [
            { text: "游泳馆，水里的时间不属于地球", type: "swim" },
            { text: "篮球场，半场三对三缺一", type: "basketball" },
            { text: "健身房，今天不练腿", type: "gym" },
            { text: "户外，跑步骑行随便走走", type: "allround" }
          ]
        },
        {
          q: "你的鞋柜里最多的是？",
          options: [
            { text: "人字拖，泳池边的合法权", type: "swim" },
            { text: "AJ，收藏是一辈子的事", type: "basketball" },
            { text: "综训鞋，深蹲硬拉都要稳", type: "gym" },
            { text: "跑鞋，磨损程度说明一切", type: "allround" }
          ]
        },
        {
          q: "更衣室里你最在意的是？",
          options: [
            { text: "泳裤晾哪儿干得比较快", type: "swim" },
            { text: "护踝和绷带还在不在", type: "basketball" },
            { text: "护腕有没有汗味", type: "gym" },
            { text: "毛巾别拿错就行", type: "allround" }
          ]
        },
        {
          q: "你的出汗量大概是？",
          options: [
            { text: "刚下水就已经湿了", type: "swim" },
            { text: "半场下来球衣能拧出水", type: "basketball" },
            { text: "组间大汗，训练服常备两套", type: "gym" },
            { text: "匀速微汗，但一天不动浑身刺挠", type: "allround" }
          ]
        },
        {
          q: "理想中的周末约会安排？",
          options: [
            { text: "双人浮潜，水下世界 only we", type: "swim" },
            { text: "1v1 斗牛，输的人请喝水", type: "basketball" },
            { text: "互夸练胸，顺便辅助拉伸", type: "gym" },
            { text: "夜跑五公里，终点是夜市", type: "allround" }
          ]
        },
        {
          q: "你的体育生浓度自评？",
          options: [
            { text: "天赋型，老天爷赏水喝", type: "swim" },
            { text: "努力型，汗水从不骗人", type: "basketball" },
            { text: "氛围型，装备先行的仪式感", type: "gym" },
            { text: "隐藏型，看着松弛其实全沾", type: "allround" }
          ]
        }
      ],
      step: "第 {n} / {total} 题",
      resultTitle: "{name} · 浓度 {p}%",
      share: "我的体育生浓度测试结果：{name}，浓度 {p}% —— 来 SportsBoy.gay 测测你的 {url}",
      resultPageLink: "打开你的结果页（分享给队友）",
      barValue: "{v}/6"
    },

    en: {
      types: {
        swim: {
          name: "Swim Jock",
          desc: "Water-native. Other people sweat to train; you sweat to swim. Where the speedos dry and which shoes go with white socks — you treat both as serious research. The pool is your home turf; being soaked is your passive skill."
        },
        basketball: {
          name: "Hoop Jock",
          desc: "Vertical and salt-stained. A sneaker collector's self-cultivation; a half-court jersey goes see-through. Closer to your ankle brace than to your situationship. In 1v1s you say \"whatever\" out loud and remember every single poster."
        },
        gym: {
          name: "Gym Jock",
          desc: "Protein-powder driven. Body-fat percentage is your life KPI; back pose #108 in the mirror still fills you with passion. Hydrate between sets. Your training plan is far more detailed than your dating plan."
        },
        allround: {
          name: "All-Round Jock",
          desc: "Plays everything. Track, court, pool, gym — legends of you everywhere. You never knew where to spend the talent points, but the concentration never drops. A real jock dares to want it all."
        }
      },
      questions: [
        {
          q: "Where do you most want to be this weekend?",
          options: [
            { text: "The pool — water time isn't earth time", type: "swim" },
            { text: "The court — 3-on-3, one player short", type: "basketball" },
            { text: "The gym — no leg day today", type: "gym" },
            { text: "Outdoors — run, ride, whatever", type: "allround" }
          ]
        },
        {
          q: "What fills your shoe rack?",
          options: [
            { text: "Flip-flops — the legal poolside uniform", type: "swim" },
            { text: "AJs — collecting is a lifetime career", type: "basketball" },
            { text: "Trainers — squats and deadlifts need stability", type: "gym" },
            { text: "Runners — the wear tells the story", type: "allround" }
          ]
        },
        {
          q: "In the locker room, what do you care about most?",
          options: [
            { text: "Where the speedos dry fastest", type: "swim" },
            { text: "Whether the ankle brace and bandages survived", type: "basketball" },
            { text: "Whether the wristbands reek", type: "gym" },
            { text: "Just don't grab the wrong towel", type: "allround" }
          ]
        },
        {
          q: "Roughly how much do you sweat?",
          options: [
            { text: "Wet before you even hit the water", type: "swim" },
            { text: "Half a game and the jersey wrings out", type: "basketball" },
            { text: "Drenched between sets — two shirts on standby", type: "gym" },
            { text: "Light steady sweat, but a day without moving itches", type: "allround" }
          ]
        },
        {
          q: "Your ideal weekend date?",
          options: [
            { text: "Snorkeling for two — underwater, just us", type: "swim" },
            { text: "1v1 — loser buys the water", type: "basketball" },
            { text: "Spotting each other on chest day, then stretching", type: "gym" },
            { text: "Night run, 5K, ending at the night market", type: "allround" }
          ]
        },
        {
          q: "Self-assess your jock concentration:",
          options: [
            { text: "Natural — heaven gave me the water", type: "swim" },
            { text: "Grinder — sweat never lies", type: "basketball" },
            { text: "Vibes — gear first, ritual always", type: "gym" },
            { text: "Hidden — looks relaxed, does everything", type: "allround" }
          ]
        }
      ],
      step: "Question {n} / {total}",
      resultTitle: "{name} · {p}% Concentration",
      share: "My jock concentration result: {name}, {p}% concentration — take the test at SportsBoy.gay {url}",
      resultPageLink: "Open your shareable result page",
      barValue: "{v}/6"
    },

    ja: {
      types: {
        swim: {
          name: "水泳部体育生",
          desc: "水感天赋型。他人は汗を流して鍛える、あなたは水に入って汗をかく。競パンの干し場所、白ソックスに合わせる靴——真面目に研究する学问だ。プールはあなたの主场、濡れるのは被动スキル。"
        },
        basketball: {
          name: "バスケ体育生",
          desc: "跳跃と汗塩型。スニーカーコレクターのたしなみ、ハーフのユニフォームはもう透ける。サポーターは恋人より近い。1v1では口で「适当にやる」と言いながら、ブロックされた数を全部覚えている。"
        },
        gym: {
          name: "ジム体育生",
          desc: "プロテイン驱动型。体脂肪率が人生のKPI、镜の前で108回目の背面ポーズも依然情热満々。セット间の补水は欠かさない。トレーニング計画は恋爱計画より详细。"
        },
        allround: {
          name: "万能体育生",
          desc: "何でもこなす型。グラウンド、コート、プール、ジム——四处にあなたの伝说が。天赋の振り先は不明、でも浓度は一度も离线したことがない。本当の体育生は、全部欲しがる勇气を持つ。"
        }
      },
      questions: [
        {
          q: "週末一番行きたい場所は？",
          options: [
            { text: "プール、水の中の时间は地球外", type: "swim" },
            { text: "コート、ハーフ3on3あと一人", type: "basketball" },
            { text: "ジム、今日は脚やらない", type: "gym" },
            { text: "アウトドア、ランでもライドでも", type: "allround" }
          ]
        },
        {
          q: "靴箱で一番多いのは？",
          options: [
            { text: "ビーサン、プールサイドの正式装备", type: "swim" },
            { text: "AJ、コレクションは一生の事业", type: "basketball" },
            { text: "トレシュー、スクワットとデッドリフトは安定が命", type: "gym" },
            { text: "ランシュー、摩耗具合が全てを物语る", type: "allround" }
          ]
        },
        {
          q: "ロッカールームで一番気になるのは？",
          options: [
            { text: "競パンどこで干かば早いか", type: "swim" },
            { text: "足首サポーターと包帯が无事か", type: "basketball" },
            { text: "リストバンドの汗臭さ", type: "gym" },
            { text: "タオル取り间违えなければOK", type: "allround" }
          ]
        },
        {
          q: "あなたの発汗量は？",
          options: [
            { text: "水に入る前から濡れてる", type: "swim" },
            { text: "ハーフ一本、ユニフォームが绞れる", type: "basketball" },
            { text: "セット间で大汗、ウェアは常に二枚", type: "gym" },
            { text: "マイペース微汗、一日动かないとむず痒い", type: "allround" }
          ]
        },
        {
          q: "理想の週末デートは？",
          options: [
            { text: "二人でシュノーケル、水中世界は仆たちだけ", type: "swim" },
            { text: "1v1、负けた方が水をおごり", type: "basketball" },
            { text: "胸トレで赏賛し合い、ついでにストレッチ", type: "gym" },
            { text: "ナイトラン5km、ゴールは夜市", type: "allround" }
          ]
        },
        {
          q: "自分の体育生浓度自己评価は？",
          options: [
            { text: "天赋型、天から水を授かった", type: "swim" },
            { text: "努力型、汗は里切らない", type: "basketball" },
            { text: "氛围型、ギア先行の仪式感", type: "gym" },
            { text: "隠れ型、弛んで见えて全部やってる", type: "allround" }
          ]
        }
      ],
      step: "第 {n} / {total} 问",
      resultTitle: "{name} · 浓度 {p}%",
      share: "私の体育生浓度テスト结果：{name}、浓度 {p}% —— SportsBoy.gay で测ってみて {url}",
      resultPageLink: "结果ページを開く（チームメイトに共有）",
      barValue: "{v}/6"
    },

    ko: {
      types: {
        swim: {
          name: "수영부 스포츠맨",
          desc: "물속 천재형. 남들은 운동해서 땀 흘리고, 너는 물에 들어가서 땀 흘린다. 수영복 말리는 위치, 흰 양말에 어울리는 신발 — 진지하게 연구하는 학문 문제. 풀은 너의 홈그라운드, 젖는 건 패시브 스킬."
        },
        basketball: {
          name: "농구부 스포츠맨",
          desc: "점프와 소금 각질형. 농구화 컬렉터의 자기 수양, 하프코트 유니폼은 벌써 비친다. 발목 보호대가 연인보다 가깝다. 1대1에서는 입으로 '아무거나' 하면서 블록당한 횟수를 전부 기억한다."
        },
        gym: {
          name: "헬스 스포츠맨",
          desc: "프로틴 구동형. 체지방률이 인생 KPI, 거울 앞 108번째 백 포즈도 여전히 열정 가득. 세트 사이 수분 보충은 필수, 운동 계획이 연애 계획보다 상세하다."
        },
        allround: {
          name: "만능 스포츠맨",
          desc: "무엇이든 하는형. 운동장, 코트, 풀, 헬스 — 사방에 너의 전설이 있다. 재능 포인트를 어디 찍었는지는 모르지만 농도는 한 번도 떨어진 적 없다. 진짜 스포츠맨은 전부 가질 용기가 있다."
        }
      },
      questions: [
        {
          q: "주말에 가장 가고 싶은 곳은?",
          options: [
            { text: "수영장, 물속 시간은 지구 시간이 아냐", type: "swim" },
            { text: "농구코트, 하프코트 3대3 한 명 부족", type: "basketball" },
            { text: "헬스, 오늘은 하체 안 해", type: "gym" },
            { text: "야외, 러닝이든 사이클이든", type: "allround" }
          ]
        },
        {
          q: "신발장에 가장 많은 것은?",
          options: [
            { text: "슬리퍼, 풀사이드 정복", type: "swim" },
            { text: "AJ, 컬렉션은 평생 사업", type: "basketball" },
            { text: "트레이닝화, 스쿼트와 데드리프트는 안정이 생명", type: "gym" },
            { text: "러닝화, 마모 정도가 모든 걸 말해줘", type: "allround" }
          ]
        },
        {
          q: "라커룸에서 가장 신경 쓰는 것은?",
          options: [
            { text: "수영복 어디 말리면 빨리 마르나", type: "swim" },
            { text: "발목 보호대와 붕대가 무사한지", type: "basketball" },
            { text: "손목 보호대에 땀 냄새 나는지", type: "gym" },
            { text: "수건만 안 바꾸면 됐어", type: "allround" }
          ]
        },
        {
          q: "너의 발땀량은?",
          options: [
            { text: "물에 들어가기도 전에 이미 젖었어", type: "swim" },
            { text: "하프코트 한 판이면 유니폼에서 물이 짜여", type: "basketball" },
            { text: "세트 사이 땀 범벅, 웨어는 늘 두 벌", type: "gym" },
            { text: "꾸준한 미열, 하루 안 움직이면 온몸이 근질", type: "allround" }
          ]
        },
        {
          q: "이상적인 주말 데이트는?",
          options: [
            { text: "투명 스노클, 수중 세계는 우리 둘만", type: "swim" },
            { text: "1대1, 지는 사람이 물 사", type: "basketball" },
            { text: "가슴 운동 서로 칭찬, 스트레칭도 겸해서", type: "gym" },
            { text: "야간 런 5km, 결승선은 야시장", type: "allround" }
          ]
        },
        {
          q: "스포츠맨 농도 자기 평가는?",
          options: [
            { text: "천부형, 하늘이 물을 주셨지", type: "swim" },
            { text: "노력형, 땀은 거짓말 안 해", type: "basketball" },
            { text: "분위기형, 장비 먼저 의식", type: "gym" },
            { text: "히든형, 느긋해 보이는데 다 해", type: "allround" }
          ]
        }
      ],
      step: "{n} / {total} 번째 문제",
      resultTitle: "{name} · 농도 {p}%",
      share: "내 스포츠맨 농도 테스트 결과: {name}, 농도 {p}% — SportsBoy.gay 에서 너도 측정해봐 {url}",
      resultPageLink: "결과 페이지 열기 (팀원에게 공유)",
      barValue: "{v}/6"
    }
  };

  var T = I18N[lang] || I18N.zh;

  function fmt(tpl, map) {
    return tpl.replace(/\{(\w+)\}/g, function (_, k) { return map[k]; });
  }

  var state = { index: 0, scores: { swim: 0, basketball: 0, gym: 0, allround: 0 } };

  var startPanel = document.getElementById("quizStart");
  var playPanel = document.getElementById("quizPlay");
  var resultPanel = document.getElementById("quizResult");
  var startBtn = document.getElementById("startBtn");
  var retryBtn = document.getElementById("retryBtn");
  var stepEl = document.getElementById("quizStep");
  var questionEl = document.getElementById("questionText");
  var optionsBox = document.getElementById("optionsBox");
  var progressBar = document.getElementById("progressBar");
  var resultTitle = document.getElementById("resultTitle");
  var resultDesc = document.getElementById("resultDesc");
  var resultBars = document.getElementById("resultBars");
  var shareTextBtn = document.getElementById("shareText");
  var shareHint = document.getElementById("shareHint");
  var resultPageLink = document.getElementById("resultPageLink");

  function show(panel) {
    [startPanel, playPanel, resultPanel].forEach(function (p) { p.hidden = p !== panel; });
  }

  function renderQuestion() {
    var item = T.questions[state.index];
    stepEl.textContent = fmt(T.step, { n: state.index + 1, total: T.questions.length });
    progressBar.style.width = (state.index / T.questions.length) * 100 + "%";
    questionEl.textContent = item.q;
    optionsBox.innerHTML = "";
    item.options.forEach(function (opt) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-option";
      btn.textContent = opt.text;
      btn.addEventListener("click", function () {
        state.scores[opt.type] += 1;
        state.index += 1;
        if (state.index < T.questions.length) {
          renderQuestion();
        } else {
          renderResult();
        }
      });
      optionsBox.appendChild(btn);
    });
  }

  function renderResult() {
    progressBar.style.width = "100%";
    var entries = Object.keys(state.scores).map(function (key) {
      return { key: key, name: T.types[key].name, value: state.scores[key] };
    }).sort(function (a, b) { return b.value - a.value; });
    var top = entries[0];
    var max = T.questions.length;
    var percent = Math.round((top.value / max) * 100);
    var displayPercent = Math.max(percent, 55);

    resultTitle.textContent = fmt(T.resultTitle, { name: top.name, p: displayPercent });
    resultDesc.textContent = T.types[top.key].desc;

    resultBars.innerHTML = "";
    entries.forEach(function (entry) {
      var row = document.createElement("div");
      row.className = "quiz-bar-row" + (entry === top ? " is-top" : "");
      var label = document.createElement("span");
      label.className = "quiz-bar-label";
      label.textContent = entry.name;
      var track = document.createElement("div");
      track.className = "quiz-bar-track";
      var fill = document.createElement("div");
      fill.className = "quiz-bar-fill";
      track.appendChild(fill);
      var value = document.createElement("span");
      value.className = "quiz-bar-value";
      value.textContent = fmt(T.barValue, { v: entry.value });
      row.appendChild(label);
      row.appendChild(track);
      row.appendChild(value);
      resultBars.appendChild(row);
      requestAnimationFrame(function () {
        fill.style.width = Math.round((entry.value / max) * 100) + "%";
      });
    });

    var resultUrl = "https://www.sportsboy.gay" + (RESULT_BASE[lang] || RESULT_BASE.zh) + top.key;
    shareTextBtn.textContent = fmt(T.share, { name: top.name, p: displayPercent, url: resultUrl });
    if (resultPageLink) {
      resultPageLink.textContent = T.resultPageLink;
      resultPageLink.href = resultUrl;
      resultPageLink.hidden = false;
    }
    shareHint.hidden = true;
    show(resultPanel);
  }

  startBtn.addEventListener("click", function () {
    state.index = 0;
    state.scores = { swim: 0, basketball: 0, gym: 0, allround: 0 };
    renderQuestion();
    show(playPanel);
  });

  retryBtn.addEventListener("click", function () {
    state.index = 0;
    state.scores = { swim: 0, basketball: 0, gym: 0, allround: 0 };
    show(startPanel);
  });

  shareTextBtn.addEventListener("click", function () {
    var text = shareTextBtn.textContent;
    function done() { shareHint.hidden = false; }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(fallback);
    } else {
      fallback();
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
  });
})();
