# -*- coding: utf-8 -*-
"""Vercel Python serverless function: /api/videos
代理 YouTube 频道 RSS，返回 JSON 视频列表，供官网 /videos 运行时拉取，
实现"上传即同步"——不再依赖构建期静态生成。

端点：/api/videos
返回：{"videos":[{"id":..., "title":...}], "fallback": bool, "updated": ...}

安全约束（见 SECURITY.md）：
  - RSS 源为固定 HTTPS 地址，不接受任何用户输入，无 SSRF 面。
  - 响应体积设上限、拒绝 DTD/ENTITY，缓解 XML 实体膨胀类 DoS。
  - videoId 必须匹配 11 位白名单字符，避免拼进 DOM/URL 时产生属性注入。
"""
from http.server import BaseHTTPRequestHandler
from datetime import datetime, timezone
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL = "UCw0gqeiGnH_vMeSxGQlBwvw"
RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
MAX_RSS_BYTES = 1_000_000
MAX_TITLE_CHARS = 300

PROD_ORIGIN = "https://www.sportsboy.gay"
PREVIEW_ORIGIN_RE = re.compile(r"^https://[a-z0-9-]+\.vercel\.app$", re.I)

# RSS 拉取失败时的兜底（当前频道已公开视频，保持与 reality 一致）
FALLBACK = [
    ("zt0PQeRFJkc", "直男做体育生浓度测试，做到第三题破防了 | SportsBoy"),
    ("zjlhX0jBhbE", "怎么一眼认出篮球体育生？看这四条 | SportsBoy"),
    ("yEs3xaG8o1k", "体育生家族里最安静的一支，靠白袜认领身份"),
    ("52KI4WEheo4", "健身房体育生图鉴：练得最狠，话最少｜SportsBoy 图鉴 02"),
    ("f3kuAUt8xsw", "更衣室文化考：体育生的第三空间｜SportsBoy 图鉴 03"),
    ("3-40xFAVEZU", "篮球体育生图鉴｜球鞋护踝一身汗，模板拼不出活的他"),
]


def allowed_origin(origin):
    if not origin:
        return None
    if origin == PROD_ORIGIN:
        return origin
    if origin.startswith(("http://localhost:", "http://127.0.0.1:")):
        return origin
    if PREVIEW_ORIGIN_RE.match(origin):
        return origin
    return None


def fetch_videos():
    try:
        req = urllib.request.Request(RSS, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read(MAX_RSS_BYTES + 1)
        if len(data) > MAX_RSS_BYTES:
            raise ValueError("RSS response too large")
        upper = data.upper()
        if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
            raise ValueError("DTD/ENTITY not allowed")
        ns = {
            "a": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        root = ET.fromstring(data)
        out = []
        seen = set()
        for e in root.findall("a:entry", ns):
            vid = e.find("yt:videoId", ns)
            title = e.find("a:title", ns)
            if vid is None or not vid.text:
                continue
            video_id = vid.text.strip()
            if not VIDEO_ID_RE.match(video_id):
                continue
            text = (title.text or "") if title is not None else ""
            # YouTube occasionally republishes a scene with a trailing "-" or
            # extra whitespace; collapse those so the gallery stays clean.
            norm = text[:MAX_TITLE_CHARS].strip().rstrip("- ").strip()
            if norm in seen:
                continue
            seen.add(norm)
            out.append({"id": video_id, "title": text[:MAX_TITLE_CHARS]})
            if len(out) >= 30:
                break
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
        self.send_header("X-Content-Type-Options", "nosniff")
        # Always vary on Origin: a response generated for a disallowed origin
        # carries no ACAO header, and must never be replayed from the Vercel
        # edge cache to a request carrying an allowed Origin (or vice versa).
        self.send_header("Vary", "Origin")
        origin = allowed_origin(self.headers.get("Origin"))
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
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
            "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        self._send(200, json.dumps(resp, ensure_ascii=False))

    def log_message(self, *args):
        pass
