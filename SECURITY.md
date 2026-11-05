# 安全说明 / SECURITY

## 报告漏洞

请发邮件至 `hello@sportsboy.gay`，标题前缀 `[SECURITY]`。请勿在公开 Issue 中披露未修复的问题。

## 架构与威胁模型

- 站点为 Vercel 上的纯静态 HTML/CSS/原生 JS，**无登录、无表单、无数据库、无用户数据落库**。
- 动态端点共四个（Python serverless）：
  - `/api/videos`：抓取**固定**的 YouTube 频道 RSS，不接受任何用户输入，因此无 SSRF / 注入面。
  - `/api/csp_report`：接收 CSP Report-Only 违规上报，请求体上限 64KB，不落库，只打印违规指令与来源域名。
  - `/api/age_verify`：查询 / 签发年龄确认 Cookie，不写日志、不收集身份信息。
  - `/api/subscribe`：把主动提交的邮箱转发给外部邮件服务；**不保存订阅名单、不把地址写入日志**。未配置服务时返回 503 并引导 RSS。
- 主要风险面是：第三方内容与脚本（YouTube / Google Fonts）、构建工具链依赖、公开仓库中的敏感文档、成年向内容的年龄分级。

## 已实施的基线

| 措施 | 位置 |
|---|---|
| `nosniff` / `X-Frame-Options` / `Referrer-Policy` / HSTS | `vercel.json` + Vercel 平台 |
| `Permissions-Policy`（禁用摄像头/麦克风/定位/USB） | `vercel.json` |
| CSP 第一阶段（强制，含 `'unsafe-inline'` 过渡） | `vercel.json` |
| CSP 第二阶段（Report-Only，严格策略） | `vercel.json` + `api/csp_report.py` |
| RSS 体积上限 1MB、拒绝 DTD/ENTITY、`videoId` 白名单 `^[A-Za-z0-9_-]{11}$`、标题去重 | `api/videos.py` |
| 前端二次校验 `videoId`、标题 `esc()` 转义后才写入 `innerHTML` | `*/videos/index.html` |
| CORS 收紧为生产域 / localhost / Vercel 预览域，且**无条件**发送 `Vary: Origin` | `api/videos.py` |
| **年龄确认服务端化**：HttpOnly + Secure + SameSite=Lax 签名 Cookie，前端无法自行标记 | `api/age_verify.py`、`assets/js/main.js` |
| **边缘门控**：成年向连载 / 小说正文页在缺少确认 Cookie 时 307 到 `/age-check` | `vercel.json` `redirects.missing` |
| RSS feed 与订阅页保持公开、年龄确认页 `noindex` | `vercel.json` + `tools/check_age_gate.py` |
| 密钥忽略规则 | `.gitignore`（`.env*` / `*.pem` / `*.key` / `.workbuddy/`） |
| 依赖锁定 + `pip-audit` + 死链 / sitemap / 红线 / API 路由 / 年龄门覆盖卡点 | `requirements.txt`、`.github/workflows/ci.yml` |

## 年龄分级（重要）

此前 18+ 年龄门仅写入 `localStorage["sb_age_ok"]`，任何脚本都能自行标记，不构成有效的年龄分级控制。现已改为：

1. `vercel.json` 的 `redirects` 使用 `missing` 条件：访问 `/vn/*`、`/novel/*` 等成年向正文页时，若请求**没有** `sb_age_verified` Cookie，则在 CDN 层 307 重定向到 `/age-check`。该页面带 `X-Robots-Tag: noindex`，仅作显著提示。
2. `/age-check` 上用户主动确认后，`POST /api/age_verify` 由服务端签发 `HttpOnly; Secure; SameSite=Lax` Cookie（180 天），再跳回原页。配置了 `AGE_GATE_SECRET` 时 Cookie 带 HMAC 签名。
3. `assets/js/main.js` 启动时通过 `GET /api/age_verify` 判断状态，未确认才显示全站提示层；确认同样走服务端。
4. `tools/check_age_gate.py` 在 CI 中校验：所有成年向正文页都有门控、RSS feed 与订阅页**不得**被门控、每条规则目标正确、年龄确认页不加载全局提示层。

**限制说明**：CDN 规则只检查 Cookie 是否存在，是内容分级门禁而非身份核验；有意伪造 Cookie 仍可绕过。这满足「显著提示、默认不呈现、不向未成年人推送」的要求，但**不足以支撑付费成人内容**。若未来上线付费 / 露骨成人分区，必须引入真实的年龄或身份核验，并重新做法务评估。本报告与本站均不提供绕过平台审核或支付政策的方案。

## CSP 分阶段上线

全站有 **64 处内联 `<script>` 与大量内联 `<style>`**，直接上严格 `script-src 'self'` 会导致白屏。当前配置：

1. **强制策略**保留 `'unsafe-inline'`，先锁定 `object-src`、帧来源、图片/字体/连接来源。
2. **Report-Only 严格策略**同时下发，违规上报到 `/api/csp_report`。Vercel 按文件名路由 serverless 函数，路径必须与 `api/csp_report.py` **逐字一致**；CI 会拦截拼写不一致。
3. 观察 1-2 周报告后，把内联脚本改为外链或为每个内联块计算 `sha256-*` hash，再从强制策略中移除 `'unsafe-inline'`。

## 订阅数据

邮箱订阅框只在你主动填写时提交。`/api/subscribe` 校验格式与同源、把地址转发给 `SUBSCRIBE_ENDPOINT`（HTTPS），本站不落库、不写日志。未配置该变量时返回 503，前端明确提示并提供 RSS 链接，**不会显示虚假的订阅成功**。四语隐私页已同步说明。

## 环境变量

在 Vercel 项目设置中配置（示例见 `.env.example`）：`AGE_GATE_SECRET`（强烈建议）、`SUBSCRIBE_ENDPOINT`、`SUBSCRIBE_TOKEN`、`BING_API_KEY`。**不要把真实值提交到公开仓库**。

## 已知遗留项（需人工决策）

1. **年龄确认为分级提示，非身份核验**：见上文「限制说明」；付费成人分区上线前必须升级。
2. **公开仓库曾包含 `VN-ROADMAP.md`**（变现、支付通道尽调）。当前版本已占位化，但 git 历史仍需单独评估清理。
3. **尚无 LICENSE**：原创图文/剧本的授权状态未声明，商业化前请与版权方确认许可类型后补充。
4. **静态资源无内容哈希**：已把 `/assets/*` 从 `immutable` 一年改为 `max-age=300, must-revalidate`。
5. **Vercel 平台对静态文件默认下发 `Access-Control-Allow-Origin: *`**，属平台默认行为。因无凭证接口、无用户数据，风险可接受；不宜在 `vercel.json` 追加同名头，重复值会破坏 CORS。
6. **邮件服务尚未接入**：配置 `SUBSCRIBE_ENDPOINT` 前，留资表单只提供 RSS 降级，不产生订阅名单。
7. **CSP 移除 `'unsafe-inline'`** 仍需先处理 64 处内联脚本。
