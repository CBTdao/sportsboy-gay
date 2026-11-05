#!/usr/bin/env python3
"""Build a send-ready newsletter draft from the serial RSS feed.

The site already publishes vn/feed.xml; this tool turns the latest chapters
into an email draft so the RSS audience can be migrated to an owned channel.

Usage:
  python tools/gen_newsletter.py --lang zh-CN
  python tools/gen_newsletter.py --lang en --limit 5 --stdout

By default the HTML is written to ../newsletters/<lang>-<date>.html (outside
the public repo). No network calls, no subscriber data.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.sportsboy.gay"
FEEDS = {
    "zh-CN": "vn/feed.xml",
    "en": "en/vn/feed.xml",
    "ja": "vn/feed.xml",
    "ko": "vn/feed.xml",
}
I18N = {
    "zh-CN": {
        "title": "SportsBoy 每周追更", "lead": "本周新章与图鉴，直接送到你的邮箱。",
        "chapters": "本周更新", "read": "阅读本章", "cta": "测测你的体育生浓度",
        "foot": "全部角色均为成年人设定，内容为虚构创作。你收到这封邮件是因为订阅了 SportsBoy 追更。",
    },
    "en": {
        "title": "SportsBoy weekly", "lead": "New scenes and field guides, straight to your inbox.",
        "chapters": "This week", "read": "Read the chapter", "cta": "Take the jock concentration test",
        "foot": "All characters are adults; all stories are fictional. You received this because you subscribed to SportsBoy.",
    },
    "ja": {
        "title": "SportsBoy 週刊", "lead": "今週の新章と図鑑をメールでお届け。",
        "chapters": "今週の更新", "read": "この章を読む", "cta": "濃度テストを受ける",
        "foot": "登場人物は全員成人設定、物語はフィクションです。SportsBoy の購読者へお送りしています。",
    },
    "ko": {
        "title": "SportsBoy 주간", "lead": "이번 주 새 장과 도감을 메일로 받아보세요.",
        "chapters": "이번 주 업데이트", "read": "장 읽기", "cta": "체육생 농도 테스트",
        "foot": "모든 등장인물은 성인 설정이며 줄거리는 허구입니다. SportsBoy 구독자에게 발송됩니다.",
    },
}


def parse_feed(rel: str, limit: int):
    path = ROOT / rel
    raw = path.read_text(encoding="utf-8")
    if b"<!DOCTYPE" in raw.upper().encode() or "<!ENTITY" in raw.upper():
        raise ValueError("DTD/ENTITY not allowed in feed")
    root = ET.fromstring(raw)
    items = []
    for node in root.findall(".//item"):
        def text(tag: str) -> str:
            el = node.find(tag)
            return (el.text or "").strip() if el is not None else ""
        items.append({
            "title": text("title"),
            "link": text("link"),
            "date": text("pubDate"),
            "desc": re.sub(r"<[^>]+>", "", text("description")),
        })
    return items[:limit]


def render(lang: str, items: list[dict]) -> str:
    t = I18N[lang]
    esc = html.escape
    rows = []
    for it in items:
        link = it["link"] or (SITE + "/vn")
        if link.startswith("/"):
            link = SITE + link
        rows.append(
            '<tr><td style="padding:0 0 22px">'
            '<div style="color:#8b8478;font-size:12px;margin:0 0 6px">%s</div>'
            '<h2 style="margin:0 0 8px;font-size:19px;color:#FF5C39">%s</h2>'
            '<p style="margin:0 0 10px;font-size:14px;line-height:1.7;color:#cfc7ba">%s</p>'
            '<a href="%s" style="color:#FF5C39;font-size:14px">%s →</a>'
            '</td></tr>' % (
                esc(it["date"][:16]), esc(it["title"]), esc(it["desc"]),
                esc(link), esc(t["read"]),
            )
        )
    return (
        '<!DOCTYPE html><html lang="%s"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>%s</title></head>'
        '<body style="margin:0;background:#0E0D0B;padding:32px 16px;'
        'font-family:system-ui,-apple-system,sans-serif">'
        '<table role="presentation" style="max-width:600px;margin:0 auto"><tr><td>'
        '<div style="color:#a79f92;font-size:12px;letter-spacing:.12em;margin:0 0 8px">SPORTSBOY.gay</div>'
        '<h1 style="margin:0 0 10px;font-size:28px;color:#f3efe6">%s</h1>'
        '<p style="margin:0 0 26px;font-size:15px;color:#cfc7ba">%s</p>'
        '<h3 style="font-size:15px;color:#FF5C39;border-left:3px solid #FF5C39;'
        'padding-left:10px;margin:0 0 18px">%s</h3>'
        '<table role="presentation" style="width:100%%">%s</table>'
        '<p style="margin:24px 0"><a href="%s/quiz" style="display:inline-block;'
        'background:#FF5C39;color:#fff;padding:12px 20px;border-radius:8px;'
        'text-decoration:none;font-weight:700">%s</a></p>'
        '<p style="margin:30px 0 0;font-size:12px;line-height:1.7;color:#8b8478">%s</p>'
        '</td></tr></table></body></html>'
    ) % (
        esc(lang), esc(t["title"]), esc(t["title"]), esc(t["lead"]),
        esc(t["chapters"]), "".join(rows), SITE, esc(t["cta"]), esc(t["foot"]),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="zh-CN", choices=sorted(I18N))
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()
    try:
        items = parse_feed(FEEDS[args.lang], max(1, min(args.limit, 20)))
    except Exception as e:
        print("feed error:", e, file=sys.stderr)
        return 1
    if not items:
        print("feed has no items", file=sys.stderr)
        return 1
    out = render(args.lang, items)
    if args.stdout:
        sys.stdout.write(out)
        return 0
    date = re.sub(r"[^0-9-]", "", items[0]["date"])[:10] or "draft"
    dest = ROOT.parent / "newsletters"
    dest.mkdir(exist_ok=True)
    path = dest / ("%s-%s.html" % (args.lang, date))
    path.write_text(out, encoding="utf-8")
    print("WROTE", path)
    print("CHAPTERS", len(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
