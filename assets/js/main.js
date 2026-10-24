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
