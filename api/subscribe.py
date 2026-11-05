# -*- coding: utf-8 -*-
"""Email subscription relay (see SECURITY.md and the growth strategy brief).

No subscriber data is written to logs or stored in this repository. Delivery
is delegated to an external mailing service configured through environment
variables:

  SUBSCRIBE_ENDPOINT  HTTPS URL that accepts {"email", "lang", "source"}
  SUBSCRIBE_TOKEN     optional bearer token forwarded to that endpoint

When SUBSCRIBE_ENDPOINT is not configured, the function returns 503 with an
explicit RSS fallback. The UI then offers the public feed instead of pretending
a signup succeeded.
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import re
import urllib.request

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$")
LANGS = ("zh-CN", "en", "ja", "ko", "")
SOURCES = ("quiz-result", "vn-subscribe", "site", "")


def _same_origin(headers) -> bool:
    origin = headers.get("Origin")
    if not origin:
        return True
    parsed = urlparse(origin)
    if parsed.hostname in ("localhost", "127.0.0.1"):
        return True
    host = headers.get("Host", "").split(":")[0]
    return bool(host) and parsed.hostname == host


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not _same_origin(self.headers):
            self._send(403, {"ok": False, "error": "cross-origin"})
            return
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 4096)
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            self._send(400, {"ok": False, "error": "invalid body"})
            return
        email = str(data.get("email", "")).strip().lower()
        lang = str(data.get("lang", ""))
        source = str(data.get("source", ""))
        if lang not in LANGS:
            lang = ""
        if source not in SOURCES:
            source = ""
        if len(email) > 254 or not EMAIL_RE.match(email):
            self._send(400, {"ok": False, "error": "invalid email"})
            return

        endpoint = os.environ.get("SUBSCRIBE_ENDPOINT", "").strip()
        if not urlparse(endpoint).scheme == "https":
            self._send(503, {
                "ok": False,
                "fallback": "/vn/subscribe",
                "error": "mailing service not configured",
            })
            return

        payload = json.dumps({"email": email, "lang": lang, "source": source}).encode("utf-8")
        headers = {"Content-Type": "application/json", "User-Agent": "SportsBoy/1.0"}
        token = os.environ.get("SUBSCRIBE_TOKEN", "").strip()
        if token:
            headers["Authorization"] = "Bearer " + token
        try:
            req = urllib.request.Request(endpoint, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                if not 200 <= resp.status < 300:
                    raise ValueError("upstream status")
                resp.read(1024)
        except Exception:
            self._send(502, {"ok": False, "error": "mailing service unavailable"})
            return
        print("SUBSCRIBE_OK", lang or "-", source or "-")
        self._send(200, {"ok": True})

    def log_message(self, *args):
        pass
