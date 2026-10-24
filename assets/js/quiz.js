(function () {
  var TYPES = {
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
  };

  var QUESTIONS = [
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
  ];

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

  function show(panel) {
    [startPanel, playPanel, resultPanel].forEach(function (p) { p.hidden = p !== panel; });
  }

  function renderQuestion() {
    var item = QUESTIONS[state.index];
    stepEl.textContent = "第 " + (state.index + 1) + " / " + QUESTIONS.length + " 题";
    progressBar.style.width = (state.index / QUESTIONS.length) * 100 + "%";
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
        if (state.index < QUESTIONS.length) {
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
      return { key: key, name: TYPES[key].name, value: state.scores[key] };
    }).sort(function (a, b) { return b.value - a.value; });
    var top = entries[0];
    var max = QUESTIONS.length;
    var percent = Math.round((top.value / max) * 100);
    var displayPercent = Math.max(percent, 55);

    resultTitle.textContent = top.name + " · 浓度 " + displayPercent + "%";
    resultDesc.textContent = TYPES[top.key].desc;

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
      value.textContent = entry.value + "/6";
      row.appendChild(label);
      row.appendChild(track);
      row.appendChild(value);
      resultBars.appendChild(row);
      requestAnimationFrame(function () {
        fill.style.width = Math.round((entry.value / max) * 100) + "%";
      });
    });

    shareTextBtn.textContent = "我的体育生浓度测试结果：" + top.name + "，浓度 " + displayPercent + "% —— 来 SportsBoy.gay 测测你的";
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
