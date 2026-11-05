/* Email capture for quiz results and serial pages.
   Renders its own UI so a single <div data-sb-subscribe> works in all four
   languages. Never stores the address locally. Falls back to the public RSS
   feed when the mailing service has not been configured yet. */
(function () {
  var I18N = {
    "zh-CN": {
      title: "每周一封，连载和图鉴直接送到邮箱",
      desc: "新章、图鉴、创作幕后。不发广告，随时可退订。",
      ph: "你的邮箱地址",
      btn: "订阅追更",
      ok: "订阅成功，请留意确认邮件。",
      busy: "提交中…",
      err: "提交失败，请稍后再试。",
      invalid: "请填写有效的邮箱地址。",
      fallback: "邮件订阅尚未开通，可以先用 RSS 追更：",
      rss: "打开订阅页",
      privacy: "我们只保存你的邮箱用于发送更新，详见",
      privacyLink: "隐私说明"
    },
    en: {
      title: "One email a week: new scenes and field guides",
      desc: "Serial chapters, almanac entries, behind-the-scenes. No ads, unsubscribe anytime.",
      ph: "Your email address",
      btn: "Subscribe",
      ok: "You're in. Check your inbox for a confirmation.",
      busy: "Sending…",
      err: "Something went wrong. Please try again.",
      invalid: "Please enter a valid email address.",
      fallback: "Email delivery is not enabled yet. Follow the RSS feed instead: ",
      rss: "Open the feed page",
      privacy: "We only store your address to send updates. See our ",
      privacyLink: "privacy policy"
    },
    ja: {
      title: "週1通、連載と図鑑をメールでお届け",
      desc: "新章・図鑑・制作裏話。広告なし、いつでも解除できます。",
      ph: "メールアドレス",
      btn: "購読する",
      ok: "登録しました。確認メールをご確認ください。",
      busy: "送信中…",
      err: "送信に失敗しました。しばらくしてからお試しください。",
      invalid: "正しいメールアドレスを入力してください。",
      fallback: "メール配信はまだ有効化されていません。RSS で追跡できます：",
      rss: "購読ページを開く",
      privacy: "更新通知のためにのみメールアドレスを保存します。",
      privacyLink: "プライバシー"
    },
    ko: {
      title: "주 1회, 연재와 도감을 메일로 받기",
      desc: "새 장·도감·제작 비하인드. 광고 없음, 언제든 구독 해지 가능.",
      ph: "이메일 주소",
      btn: "구독하기",
      ok: "완료됐어요. 확인 메일을 확인해 주세요.",
      busy: "전송 중…",
      err: "전송에 실패했습니다. 잠시 후 다시 시도해 주세요.",
      invalid: "올바른 이메일 주소를 입력해 주세요.",
      fallback: "이메일 발송이 아직 활성화되지 않았습니다. RSS 로 구독하세요: ",
      rss: "구독 페이지 열기",
      privacy: "업데이트 발송 목적으로만 주소를 보관합니다. ",
      privacyLink: "개인정보 처리방침"
    }
  };

  var CSS = ".sb-sub{max-width:560px;margin:34px auto 8px;padding:22px 24px;" +
    "background:#16140F;border:1px solid #2a2620;border-radius:14px;text-align:left}" +
    ".sb-sub h3{margin:0 0 8px;font-size:19px;color:#FF5C39}" +
    ".sb-sub p{margin:0 0 14px;font-size:14px;line-height:1.7;color:#cfc7ba}" +
    ".sb-sub form{display:flex;gap:10px;flex-wrap:wrap}" +
    ".sb-sub input{flex:1;min-width:200px;padding:11px 13px;border-radius:8px;" +
    "border:1px solid #3a352c;background:#0E0D0B;color:#f3efe6;font-size:15px}" +
    ".sb-sub button{padding:11px 20px;border-radius:8px;border:0;cursor:pointer;" +
    "background:#FF5C39;color:#fff;font-weight:700;font-size:15px}" +
    ".sb-sub button:disabled{opacity:.6;cursor:wait}" +
    ".sb-sub .msg{margin:12px 0 0;font-size:14px;color:#cfc7ba}" +
    ".sb-sub .fine{margin:12px 0 0;font-size:12px;color:#8b8478}" +
    ".sb-sub a{color:#FF5C39}";

  function init(box) {
    var lang = box.getAttribute("data-lang") || "zh-CN";
    var t = I18N[lang] || I18N["zh-CN"];
    var source = box.getAttribute("data-source") || "site";
    var rss = box.getAttribute("data-rss") || "/vn/subscribe";
    var privacy = box.getAttribute("data-privacy") || "/privacy";

    box.className = "sb-sub";
    box.innerHTML =
      "<h3></h3><p class='lede'></p>" +
      "<form novalidate><input type='email' autocomplete='email' inputmode='email'>" +
      "<button type='submit'></button></form>" +
      "<p class='msg' role='status' aria-live='polite'></p>" +
      "<p class='fine'></p>";
    box.querySelector("h3").textContent = t.title;
    box.querySelector(".lede").textContent = t.desc;
    var input = box.querySelector("input");
    input.placeholder = t.ph;
    input.setAttribute("aria-label", t.ph);
    var btn = box.querySelector("button");
    btn.textContent = t.btn;
    var msg = box.querySelector(".msg");
    var fine = box.querySelector(".fine");
    fine.textContent = t.privacy + " ";
    var a = document.createElement("a");
    a.href = privacy;
    a.textContent = t.privacyLink;
    fine.appendChild(a);

    box.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      var email = input.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/.test(email)) {
        msg.textContent = t.invalid;
        return;
      }
      btn.disabled = true;
      btn.textContent = t.busy;
      msg.textContent = "";
      fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, lang: lang, source: source })
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) {
          return { status: r.status, data: d };
        });
      }).then(function (res) {
        if (res.status === 200 && res.data.ok) {
          msg.textContent = t.ok;
          input.value = "";
        } else if (res.status === 503) {
          msg.textContent = "";
          msg.textContent = t.fallback;
          var link = document.createElement("a");
          link.href = rss;
          link.textContent = t.rss;
          msg.appendChild(link);
        } else {
          msg.textContent = t.err;
        }
      }).catch(function () {
        msg.textContent = t.err;
      }).then(function () {
        btn.disabled = false;
        btn.textContent = t.btn;
      });
    });
  }

  var boxes = document.querySelectorAll("[data-sb-subscribe]");
  if (!boxes.length) return;
  var style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);
  Array.prototype.forEach.call(boxes, init);
})();
