# -*- coding: utf-8 -*-
"""Vercel Python serverless function: /api/videos
代理 YouTube 频道 RSS，返回 JSON 视频列表，供官网 /videos 运行时拉取，
实现"上传即同步"——不再依赖构建期静态生成。

端点：/api/videos
返回：{"videos":[{"id":..., "title":...}], "fallback": bool, "updated": ...}
"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL = "UCw0gqeiGnH_vMeSxGQlBwvw"
RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL

# RSS 拉取失败时的兜底（当前频道已公开视频，保持与 reality 一致）
FALLBACK = [
    ("zt0PQeRFJkc", "直男做体育生浓度测试，做到第三题破防了 | SportsBoy"),
    ("zjlhX0jBhbE", "怎么一眼认出篮球体育生？看这四条 | SportsBoy"),
    ("yEs3xaG8o1k", "体育生家族里最安静的一支，靠白袜认领身份"),
    ("52KI4WEheo4", "健身房体育生图鉴：练得最狠，话最少｜SportsBoy 图鉴 02"),
    ("f3kuAUt8xsw", "更衣室文化考：体育生的第三空间｜SportsBoy 图鉴 03"),
    ("3-40xFAVEZU", "篮球体育生图鉴｜球鞋护踝一身汗，模板拼不出活的他"),
]


def fetch_videos():
    try:
        req = urllib.request.Request(RSS, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=15).read()
        ns = {
            "a": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        root = ET.fromstring(data)
        out = []
        for e in root.findall("a:entry", ns):
            vid = e.find("yt:videoId", ns)
            title = e.find("a:title", ns)
            if vid is not None and vid.text:
                out.append({"id": vid.text, "title": title.text if title is not None else ""})
        if out:
            return out, False
    except Exception:
        pass
    return [{"id": i, "title": t} for i, t in FALLBACK], True


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = payload.encode("utf-8") if isinstance(payload, str) else payload
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        # Vercel 边缘缓存 10 分钟；上传后最迟 10 分钟官网自动同步
        self.send_header("Cache-Control", "s-maxage=600, stale-while-revalidate=86400")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        videos, fb = fetch_videos()
        resp = {
            "videos": videos,
            "fallback": fb,
            "channel": CHANNEL,
        }
        self._send(200, json.dumps(resp, ensure_ascii=False))

    def log_message(self, *args):
        pass
