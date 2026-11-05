# 安全说明 / SECURITY

## 报告漏洞

请发邮件至 `hello@sportsboy.gay`，标题前缀 `[SECURITY]`。请勿在公开 Issue 中披露未修复的问题。

## 架构与威胁模型

- 站点为 Vercel 上的纯静态 HTML/CSS/原生 JS，**无登录、无表单、无数据库、无用户数据落库**。
- 唯一的动态端点是 `/api/videos`（Python serverless）：抓取**固定**的 YouTube 频道 RSS，不接受任何用户输入，因此无 SSRF / 注入面。
- 主要风险面是：第三方内容与脚本（YouTube / Google Fonts）、构建工具链依赖、公开仓库中的敏感文档。

## 已实施的基线

| 措施 | 位置 |
|---|---|
| `nosniff` / `X-Frame-Options` / `Referrer-Policy` / HSTS | `vercel.json` + Vercel 平台 |
| `Permissions-Policy`（禁用摄像头/麦克风/定位/USB） | `vercel.json` |
| CSP 第一阶段（强制，含 `'unsafe-inline'` 过渡） | `vercel.json` |
| CSP 第二阶段（Report-Only，严格策略） | `vercel.json` + `api/csp_report.py` |
| RSS 体积上限 1MB、拒绝 DTD/ENTITY、`videoId` 白名单 `^[A-Za-z0-9_-]{11}$` | `api/videos.py` |
| 前端二次校验 `videoId`、标题 `esc()` 转义后才写入 `innerHTML` | `*/videos/index.html` |
| CORS 收紧为生产域 / localhost / Vercel 预览域 | `api/videos.py` |
| 密钥忽略规则 | `.gitignore`（`.env*` / `*.pem` / `*.key` / `.workbuddy/`） |
| 依赖锁定 + `pip-audit` + 死链 / sitemap / 红线卡点 | `requirements.txt`、`.github/workflows/ci.yml` |

## CSP 分阶段上线（重要）

全站有 **64 处内联 `<script>` 与大量内联 `<style>`**，直接上严格 `script-src 'self'` 会导致白屏。当前配置：

1. **强制策略**保留 `'unsafe-inline'`，先锁定 `object-src`、帧来源、图片/字体/连接来源，防止外部脚本注入与数据外带。
2. **Report-Only 严格策略**同时下发，违规上报到 `/api/csp-report`（只记录指令与来源域名，不记录完整 URL）。
3. 观察 1-2 周报告后，把内联脚本改为外链或为每个内联块计算 `sha256-*` hash，再从强制策略中移除 `'unsafe-inline'`。此为唯一仍需人工完成的安全项。

## 依赖与密钥

- `requirements.txt` 精确锁定 Pillow；CI 每次运行 `pip-audit`。
- 本地复制 `.env.example` 为 `.env` 后填入 `BING_API_KEY`；**真实 `.env` 严禁提交**。
- 建议在仓库设置中开启 GitHub 的 **Secret scanning + Push protection**（这是平台功能，无法通过工作流开启）。
- 历史上公开仓库中曾出现 `tools/` 生成脚本，请避免在其中写入任何 token。

## 已知遗留项（需人工决策）

1. **18+ 年龄门**仅靠 `localStorage["sb_age_ok"]`，是提示而非安全控制；若上线付费/成人分区，需服务端或边缘层二次校验。
2. **公开仓库包含 `VN-ROADMAP.md`**（变现、支付通道尽调、平台审核对策）。建议迁至私有文档；注意仅删除当前文件**不能**清除 git 历史，需另行评估。
3. **尚无 LICENSE**：原创图文/剧本的授权状态未声明，商业化前请与版权方确认许可类型后补充。
4. **静态资源无内容哈希**：已把 `/assets/*` 从 `immutable` 一年改为 `max-age=300, must-revalidate`。后续若引入 `<name>.<hash>.<ext>` 命名，可恢复长缓存。
