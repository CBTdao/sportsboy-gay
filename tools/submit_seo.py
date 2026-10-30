# -*- coding: utf-8 -*-
"""submit_seo.py — 把 sitemap.xml 中的 URL 批量推送给 Bing（URL Submission API）。

为什么只做 Bing：
- Bing 有公开免费的批量提交 API（每次最多 10000 条），适合日更场景。
- Google 已废弃 ping 接口，其 Indexing API 仅支持 JobPosting/Event，普通文章页
  走 Google Search Console 提交 sitemap 即可（见《收录提交指南》）。

用法：
    export BING_API_KEY="你的_bing_webmaster_api_key"
    python tools/submit_seo.py

密钥获取：Bing Webmaster Tools → 你的站点 → 设置 → API 访问 → 复制密钥。
切勿把密钥写进脚本或提交到 git；用环境变量注入。
"""
import os
import re
import sys
import json
import urllib.request

BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"
SITE = "https://www.sportsboy.gay"
SITEMAP = os.path.join(BASE, "sitemap.xml")
API_URL = "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=%s"


def read_urls():
    with open(SITEMAP, encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"<loc>(.*?)</loc>", content)


def submit(urls, api_key):
    body = json.dumps({"siteUrl": SITE, "urlList": urls}).encode("utf-8")
    req = urllib.request.Request(
        API_URL % api_key,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode()
            text = resp.read().decode("utf-8", "replace")
            return code, text
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def main():
    api_key = os.environ.get("BING_API_KEY")
    if not api_key:
        print("ERROR: 未设置 BING_API_KEY 环境变量。")
        print('请先运行：export BING_API_KEY="你的_api_key"')
        sys.exit(2)

    urls = read_urls()
    if not urls:
        print("sitemap 中未找到任何 <loc>，跳过。")
        sys.exit(0)

    print("从 sitemap 读取 %d 条 URL，提交给 Bing…" % len(urls))
    code, text = submit(urls, api_key)
    if code in (200, 204) or (code is None and "成功" in text):
        print("OK: Bing 已接收批量提交（HTTP %s）。" % code)
        print("返回：%s" % text[:300])
        sys.exit(0)
    else:
        print("FAIL: HTTP %s" % code)
        print(text[:800])
        sys.exit(1)


if __name__ == "__main__":
    main()
