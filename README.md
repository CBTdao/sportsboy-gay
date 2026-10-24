# SportsBoy.gay

全球华语体育生文化总部——荷尔蒙编辑部官网。纯静态站点（HTML + CSS + 原生 JS），零依赖、零构建，部署到 Vercel。

## 页面

| 文件 | 内容 |
|---|---|
| `index.html` | 首页：Hero / 王牌栏目 / 首部作品《体育生》/ 浓度测试入口 / IP 飞轮 / 爱发电 CTA |
| `quiz.html` | 体育生浓度测试：6 题 → 4 种人格图鉴 → 可复制分享文案（增长钩子） |

## 本地预览

```bash
cd sportsboy-site
python -m http.server 8080
# 打开 http://localhost:8080
```

## 部署（GitHub + Vercel）

```bash
# 1. 推送代码（仓库已初始化为本地 git）
git remote add origin https://github.com/<你的用户名>/sportsboy-gay.git
git push -u origin main

# 2. 部署：打开 https://vercel.com/new
#    → Import Git Repository → 选择 sportsboy-gay
#    → Framework Preset: Other（静态站，无需构建）
#    → 点 Deploy，约 30 秒上线

# 3. 绑定域名：Vercel 控制台 → Settings → Domains → 添加 sportsboy.gay
#    （DNS 按提示添加 A 记录 76.76.21.21 或 CNAME cname.vercel-dns.com）
```

或者命令行部署（需先 `npx vercel login`）：

```bash
npx vercel --prod
```

## 上线前待办（替换占位链接）

- [ ] `index.html` 中所有 `data-todo` 占位链接：爱发电主页、itch.io（demo 上线后）、TikTok / X 账号
- [ ] 角色预告图 `assets/img/teaser.png`：正式立绘出来后替换（当前为 AI 测试图）
- [ ] 首页 `og:image` 可换成 1200×630 专用分享图
- [ ] 爱发电三档赞助金额确认后更新首页文案

## 设计规范

- 暗色暖黑底 `#0E0D0B`，珊瑚橙强调色 `#FF5C2B`（运动 + 荷尔蒙）
- 展示字体 Archivo Black，中文 Noto Sans SC（900/700/500/400）
- 全站响应式，`prefers-reduced-motion` 已适配

## 内容红线（规划既定）

BL 分区明确；角色全部成年设定；虚构创作声明已在页脚。
