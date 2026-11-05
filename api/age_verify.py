# -*- coding: utf-8 -*-
"""Server-side age acknowledgement (see SECURITY.md).

GET  /api/age_verify -> {"verified": bool}
POST /api/age_verify -> issues an HttpOnly, Secure, SameSite=Lax cookie

The previous gate stored a flag in localStorage, which any script (or a user
with devtools) could set without any server-side record. Here the
acknowledgement is issued by a serverless function and the cookie is
HttpOnly, so browser code cannot self-authorise.

Edge gating in vercel.json redirects age-gated pages to /age-check when the
cookie is missing. That CDN rule checks presence only; this function performs
the actual issuance and signature verification. Set AGE_GATE_SECRET in the
Vercel project environment to enable HMAC verification.

This is an acknowledgement control, not identity verification. See
SECURITY.md for the remaining limitations and the second-stage requirement.
"""
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlparse
import hashlib
import hmac
import json
import os
import secrets
import time

COOKIE = "sb_age_verified"
VERSION = "v1"
MAX_AGE = 180 * 24 * 60 * 60


def _key() -> bytes:
    return os.environ.get("AGE_GATE_SECRET", "").encode("utf-8")


def _signature(payload: str) -> str:
    key = _key()
    if key:
        return hmac.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()[:32]
    return secrets.token_hex(16)


def _issue() -> str:
    payload = VERSION + "." + str(int(time.time()))
    return payload + "." + _signature(payload)


def _verify(value: str) -> bool:
    parts = (value or "").split(".")
    if len(parts) != 3:
        return False
    version, issued, sig = parts
    if version != VERSION or len(sig) != 32:
        return False
    try:
        age = int(time.time()) - int(issued)
    except ValueError:
        return False
    if age < 0 or age > MAX_AGE:
        return False
    key = _key()
    if key:
        expected = hmac.new(
            key, (version + "." + issued).encode("utf-8"), hashlib.sha256
        ).hexdigest()[:32]
        return hmac.compare_digest(sig, expected)
    return all(c in "0123456789abcdef" for c in sig)


def _cookie_value(headers) -> str:
    try:
        jar = SimpleCookie()
        jar.load(headers.get("Cookie", ""))
        morsel = jar.get(COOKIE)
        return morsel.value if morsel else ""
    except Exception:
        return ""


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
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"verified": _verify(_cookie_value(self.headers))})

    def do_POST(self):
        if not _same_origin(self.headers):
            self._send(403, {"ok": False, "error": "cross-origin"})
            return
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 4096)
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            data = {}
        if data.get("confirm") != "adult":
            self._send(400, {"ok": False, "error": "confirmation required"})
            return
        body = json.dumps({"ok": True, "verified": True}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Set-Cookie",
            f"{COOKIE}={_issue()}; Max-Age={MAX_AGE}; Path=/; "
            "HttpOnly; Secure; SameSite=Lax",
        )
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
