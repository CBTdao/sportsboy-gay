(function () {
  var header = document.getElementById("siteHeader");
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("navLinks");

  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 24);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { header.classList.remove("nav-open"); });
    });
  }

  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  document.querySelectorAll("[data-todo]").forEach(function (el) {
    el.addEventListener("click", function (event) {
      event.preventDefault();
      var original = el.textContent;
      el.textContent = el.getAttribute("data-todo");
      setTimeout(function () { el.textContent = original; }, 2200);
    });
  });

  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
    });
  }

  /* 语言菜单：地球按钮 + 下拉（中文主场，其余语言收起） */
  var langToggle = document.querySelector(".lang-toggle");
  var langMenu = document.getElementById("langMenu");
  if (langToggle && langMenu) {
    function closeLangMenu() {
      langMenu.setAttribute("hidden", "");
      langToggle.setAttribute("aria-expanded", "false");
    }
    langToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var willOpen = langMenu.hasAttribute("hidden");
      if (willOpen) {
        langMenu.removeAttribute("hidden");
      } else {
        langMenu.setAttribute("hidden", "");
      }
      langToggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
    });
    document.addEventListener("click", function (event) {
      if (!langMenu.contains(event.target) && !langToggle.contains(event.target)) closeLangMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeLangMenu();
    });
    langMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeLangMenu);
    });
  }
})();

/* 18+ 年龄确认：状态由服务端判定，确认动作签发 HttpOnly Cookie（见 SECURITY.md）。
   前端无法自行标记已确认；敏感正文页另由 vercel.json 的边缘规则门控。 */
(function () {
  if (location.pathname.indexOf("/age-check") === 0) return;
  var css = document.createElement("style");
  css.textContent =
    "#sbAge{position:fixed;inset:0;z-index:9999;background:rgba(8,7,6,.96);" +
    "display:flex;align-items:center;justify-content:center;padding:20px;" +
    "font-family:var(--font-sans,system-ui,sans-serif}" +
    "#sbAge .card{max-width:460px;background:#16140F;border:1px solid #2a2620;border-radius:16px;" +
    "padding:28px 26px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.5)}" +
    "#sbAge h2{font-size:22px;margin:0 0 12px;color:#fff}" +
    "#sbAge p{font-size:15px;line-height:1.7;color:#cfc9bf;margin:0 0 16px}" +
    "#sbAge .acts{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}" +
    "#sbAge a.leave{color:#888;font-size:13px;text-decoration:underline;margin-top:16px;display:inline-block}" +
    "#sbAge .err{color:#FF9B7A;font-size:13px;margin:12px 0 0;min-height:18px}";
  document.head.appendChild(css);

  function show() {
    var ov = document.createElement("div");
    ov.id = "sbAge";
    ov.innerHTML =
      '<div class="card"><h2>18+ 内容提示</h2>' +
      '<p>本站部分栏目含面向成年人的虚构创作内容（BL 向连载与剧本），仅限成年人阅读。' +
      '全部角色均为成年人设定，情节纯属虚构；本站不向未成年人推送相关内容。</p>' +
      '<div class="acts"><button id="sbEnter" class="btn btn-primary">我已满 18 岁，进入</button></div>' +
      '<p class="err" id="sbAgeErr" role="status" aria-live="polite"></p>' +
      '<a class="leave" href="https://www.google.com" target="_blank" rel="noopener">未满 18 岁，离开</a></div>';
    document.body.appendChild(ov);
    document.body.style.overflow = "hidden";
    var btn = document.getElementById("sbEnter");
    var err = document.getElementById("sbAgeErr");
    btn.addEventListener("click", function () {
      btn.disabled = true;
      err.textContent = "";
      fetch("/api/age_verify", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirm: "adult" })
      }).then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.verified) {
            if (ov.parentNode) ov.parentNode.removeChild(ov);
            document.body.style.overflow = "";
          } else {
            err.textContent = "确认失败，请稍后重试。";
            btn.disabled = false;
          }
        }).catch(function () {
          err.textContent = "确认失败，请稍后重试。";
          btn.disabled = false;
        });
    });
  }

  fetch("/api/age_verify", { credentials: "same-origin", cache: "no-store" })
    .then(function (r) { return r.json(); })
    .then(function (d) { if (!d.verified) show(); })
    .catch(function () { /* 端点不可用时保持页面可用；敏感页仍由边缘规则拦截 */ });
})();
