# SportsBoy.gay

全球体育生文化总部——荷尔蒙编辑部官网。纯静态站点（HTML + CSS + 原生 JS），零依赖、零构建，部署到 Vercel。

## 页面（四语：中 / EN / JA / KO）

| 路径 | 内容 |
|---|---|
| `/` | 中文首页：Hero / 王牌栏目 / 首部作品《体育生》/ 浓度测试入口 / IP 飞轮 / 爱发电 CTA |
| `/quiz` | 体育生浓度测试：6 题 → 4 种人格图鉴 → 可复制分享文案（增长钩子） |
| `/en` `/ja` `/ko` | 英 / 日 / 韩首页 |
| `/en/quiz` `/ja/quiz` `/ko/quiz` | 三语测试页（题库见 `assets/js/quiz.js` 内 I18N） |
| `/quiz/result/{swim,basketball,gym,allround}` | 人格结果分享页（程序化获客：可索引 + 独立 og 文案 + "测测你的" CTA；四语各 4 页） |

语言切换：顶栏语言胶囊（中 EN JA KO）。SEO：每页 canonical + hreflang 四语互指 + x-default，`sitemap.xml` 同步（24 URL）。

## 本地预览

```bash
cd sportsboy-site
python -m http.server 8080
# 打开 http://localhost:8080
```

## 部署（GitHub + Vercel）

```bash
# 1. 推送代码（仓库已初始化为本地 git）
git remote add origin git@github-sb:CBTdao/sportsboy-gay.git
git push -u origin main

# 2. Vercel 已绑定本仓库，推 main 自动部署
#    Framework Preset: Other（静态站，无需构建）
```

## 上线前待办（替换占位链接）

- [ ] `index.html` 等页中所有 `data-todo` 占位链接：爱发电主页、itch.io（demo 上线后）、TikTok / X 账号
- [ ] 角色预告图 `assets/img/teaser.webp`：正式立绘出来后替换（母版 `teaser-src.jpg`，去水印已完成）
- [ ] 爱发电三档赞助金额确认后更新首页文案

## 图片资产

`assets/img/`：`hero.webp/jpg`（Hero 背景）、`teaser.webp/jpg`（角色预告）、`og.jpg`（社交分享图 1200×630）、`icon-512.png` / `apple-touch-icon.png`（PWA 图标）。
原图 PNG 已由 `tools/optimize_images.py`（Pillow）压缩转换，勿再提交大图。

## PWA / SEO 基建

- `manifest.json` + `sw.js`（stale-while-revalidate，可安装、离线可用）
- `robots.txt` + `sitemap.xml`（24 URL，含 hreflang）
- 每页 JSON-LD（WebSite / Organization）
- 结果分享页由 `tools/gen_result_pages.py` 生成（人格数据与 `quiz.js` I18N 保持一致，改动需两边同步）

## 设计规范

- 暗色暖黑底 `#0E0D0B`，珊瑚橙强调色 `#FF5C2B`（运动 + 荷尔蒙）
- 展示字体 Archivo Black；正文按语言加载 Noto Sans SC / JP / KR
- 全站响应式，`prefers-reduced-motion` 已适配

## 内容红线（规划既定）

BL 分区明确；角色全部成年设定；虚构创作声明已在页脚。
