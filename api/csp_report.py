# -*- coding: utf-8 -*-
"""CSP violation collector for the Report-Only rollout (see SECURITY.md).

Only logs the violated directive and the blocked origin. Report bodies may
contain user-specific URLs, so they are never written to logs verbatim.
"""
from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 65536)
            data = json.loads(self.rfile.read(length) or b"{}")
            report = data.get("csp-report", data)
            directive = str(report.get("violated-directive", ""))[:120]
            blocked = str(report.get("blocked-uri", ""))[:120]
            print("CSP_REPORT", directive, blocked)
        except Exception:
            print("CSP_REPORT unparsed")
        self.send_response(204)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def log_message(self, *args):
        pass
