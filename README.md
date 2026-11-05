# SportsBoy.gay

全球体育生文化总部——荷尔蒙编辑部官网。**运行时**为零依赖、零构建的静态站（HTML + CSS + 原生 JS）+ 一个 `/api/videos` serverless 函数，部署到 Vercel。内容生成脚本（`tools/`）依赖 Pillow，版本锁定在 `requirements.txt`。

## 页面（四语：中 / EN / JA / KO）

| 路径 | 内容 |
|---|---|
| `/` | 中文首页：Hero / 王牌栏目 / 首部作品《体育生》/ 浓度测试入口 / SportsBoy 宇宙（用户视角产品分层）/ 爱发电 CTA |
| `/quiz` | 体育生浓度测试：6 题 → 4 种人格图鉴 → 可复制分享文案（增长钩子） |
| `/en` `/ja` `/ko` | 英 / 日 / 韩首页 |
| `/en/quiz` `/ja/quiz` `/ko/quiz` | 三语测试页（题库见 `assets/js/quiz.js` 内 I18N） |
| `/quiz/result/{swim,basketball,gym,allround}` | 人格结果分享页（可索引 + 独立 og 文案 + "测测你的" CTA；四语各 4 页） |

语言切换：顶栏语言胶囊（中 EN JA KO）。SEO：每页 canonical + hreflang 四语互指 + x-default；`sitemap.xml` 由 `tools/gen_sitemap.py` 从实际页面确定性生成，当前 **94 条 URL（92 个页面 + 2 个 feed）**，无重复、无死链目标。

## 本地预览

```bash
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

## 维护与校验

```bash
# 安装内容生成工具链（Pillow 已锁定版本）
python -m pip install -r requirements.txt

# 新增/删除页面后必须重新生成 sitemap
python tools/gen_sitemap.py
python tools/gen_sitemap.py --check     # CI 幂等校验

# 提交前本地自检
python tools/check_links.py             # 内链 / 协议相对 URL / 缺失资源
bash tools/check_redline.sh             # 公开页面不得出现内部术语
```

`.github/workflows/ci.yml` 会在每次 push / PR 自动运行：依赖漏洞审计（`pip-audit`）、Python 语法、JSON 配置有效性、sitemap 幂等、死链、内容红线。安全基线、CSP 分阶段计划与遗留风险见 [SECURITY.md](SECURITY.md)。

`tools/submit_seo.py` 需要 `BING_API_KEY`：复制 `.env.example` 为 `.env` 后填写，真实 `.env` 已被 `.gitignore` 排除。

## 上线前待办（替换占位链接）

- [ ] `index.html` 等页中所有 `data-todo` 占位链接：爱发电主页、itch.io（demo 上线后）、TikTok / X 账号
- [ ] 角色预告图 `assets/img/teaser.webp`：正式立绘出来后替换（母版 `teaser-src.jpg`，去水印已完成）
- [ ] 爱发电三档赞助金额确认后更新首页文案

## 图片资产

`assets/img/`：`hero.webp/jpg`（Hero 背景）、`teaser.webp/jpg`（角色预告）、`og.jpg`（社交分享图 1200×630）、`icon-512.png` / `apple-touch-icon.png`（PWA 图标）。
原图 PNG 已由 `tools/optimize_images.py`（Pillow）压缩转换，勿再提交大图。`yt-thumb-*.png` 为 YouTube 缩略图源素材，页面运行时实际使用 `i.ytimg.com`，可迁出公开仓库以减小体积。

## PWA / SEO 基建

- `manifest.json` + `sw.js`（stale-while-revalidate，可安装、离线可用）
- `robots.txt` + `sitemap.xml`（94 URL，含 hreflang，由生成器维护）
- 每页 JSON-LD（WebSite / Organization）
- 结果分享页由 `tools/gen_result_pages.py` 生成（人格数据与 `quiz.js` I18N 保持一致，改动需两边同步；CI 的 sitemap / 死链校验可兜底）

## 设计规范

- 暗色暖黑底 `#0E0D0B`，珊瑚橙强调色 `#FF5C2B`（运动 + 荷尔蒙）
- 展示字体 Archivo Black；正文按语言加载 Noto Sans SC / JP / KR
- 全站响应式，`prefers-reduced-motion` 已适配

## 内容红线（规划既定）

BL 分区明确；角色全部成年设定；虚构创作声明已在页脚。`tools/check_redline.sh` 会拦截公开页面上的内部术语。

> `VN-ROADMAP.md` 属内部策略文档（含变现与支付通道尽调），本仓库为公开仓库，建议迁至私有空间。
