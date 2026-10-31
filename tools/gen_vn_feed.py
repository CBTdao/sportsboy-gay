# -*- coding: utf-8 -*-
"""gen_vn_feed.py — 生成《体育生》连载 RSS（追更提醒用）。

输出：
  /vn/feed.xml        中文章节主 feed
  /en/vn/feed.xml     英文读者订阅入口（仍指向中文章节）

读取 content/vn/*.md 的 frontmatter（title/date/summary），按日期升序排列。
运行：python tools/gen_vn_feed.py
"""
import os
import re
import glob

BASE = r"C:/Users/Administrator/WorkBuddy/2026-10-24-20-20-35/sportsboy-site"
SITE = "https://www.sportsboy.gay"


def parse_frontmatter(text):
    meta = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", lines[i])
        if m and i < 30:
            meta[m.group(1).lower()] = m.group(2).strip()
            i += 1
        else:
            break
    return meta


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def build(items):
    items = sorted(items, key=lambda x: (x["date"], x["slug"]))
    entries = []
    for it in items:
        url = "%s/vn/%s" % (SITE, it["slug"])
        entries.append(
            "    <item>\n"
            "      <title>%s</title>\n"
            "      <link>%s</link>\n"
            '      <guid isPermaLink="true">%s</guid>\n'
            "      <pubDate>%s</pubDate>\n"
            "      <description>%s</description>\n"
            "    </item>\n"
            % (esc(it["title"]), url, url, esc(it["date"]), esc(it["summary"]))
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>《体育生》· 免费连载</title>\n"
        "    <link>%s/vn</link>\n"
        '    <atom:link href="%s/vn/feed.xml" rel="self" type="application/rss+xml"/>\n'
        "    <description>首部视觉小说《体育生》剧本逐场公开、免费阅读，每日更新一场。角色全部成年设定。</description>\n"
        "    <language>zh-CN</language>\n"
        "%s"
        "  </channel>\n"
        "</rss>\n"
    ) % (SITE, SITE, "".join(entries))


def main():
    folder = os.path.join(BASE, "content", "vn")
    items = []
    for path in sorted(glob.glob(os.path.join(folder, "*.md"))):
        with open(path, encoding="utf-8") as f:
            meta = parse_frontmatter(f.read())
        items.append({
            "slug": os.path.splitext(os.path.basename(path))[0],
            "title": meta.get("title", ""),
            "date": meta.get("date", ""),
            "summary": meta.get("summary", ""),
        })

    out_zh = os.path.join(BASE, "vn", "feed.xml")
    with open(out_zh, "w", encoding="utf-8") as f:
        f.write(build(items))
    print("wrote", out_zh)

    out_en = os.path.join(BASE, "en", "vn", "feed.xml")
    os.makedirs(os.path.dirname(out_en), exist_ok=True)
    with open(out_en, "w", encoding="utf-8") as f:
        f.write(build(items))
    print("wrote", out_en)


if __name__ == "__main__":
    main()
