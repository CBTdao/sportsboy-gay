/* SportsBoy.gay Service Worker — stale-while-revalidate 静态资源缓存 */
/* v2: hero/teaser/og 去水印后全量换图，旧 v1 缓存（含带水印旧图）在 activate 时删除 */
var CACHE = "sportsboy-v2";
var SHELL = [
  "/",
  "/quiz",
  "/en/",
  "/en/quiz",
  "/ja/",
  "/ja/quiz",
  "/ko/",
  "/ko/quiz",
  "/assets/css/style.css",
  "/assets/js/main.js",
  "/assets/js/quiz.js",
  "/assets/img/hero.webp",
  "/assets/img/hero.jpg",
  "/assets/img/teaser.webp",
  "/assets/img/teaser.jpg",
  "/assets/img/og.jpg",
  "/assets/img/icon-512.png",
  "/manifest.json"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(SHELL.map(function (url) {
        return new Request(url, { cache: "reload" });
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (key) {
        if (key !== CACHE) return caches.delete(key);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var req = event.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  /* 导航请求：网络优先，失败回退缓存（保证内容新鲜） */
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).catch(function () {
        return caches.match(req).then(function (hit) {
          return hit || caches.match("/");
        });
      })
    );
    return;
  }

  /* 静态资源：stale-while-revalidate */
  event.respondWith(
    caches.match(req).then(function (hit) {
      var network = fetch(req).then(function (res) {
        if (res && res.status === 200) {
          var copy = res.clone();
          caches.open(CACHE).then(function (cache) { cache.put(req, copy); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || network;
    })
  );
});
