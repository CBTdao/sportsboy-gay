#!/usr/bin/env python3
"""CI guard for age gating and email capture (see SECURITY.md).

Verifies:
  - every adult-serial / novel body page has a matching CDN gate rule;
  - every gate rule points at an existing page and the correct destination;
  - RSS feeds and subscribe pages are never gated (they must stay public);
  - every quiz result page and subscribe page carries the capture widget;
  - the age-check interstitial is noindex and does not load the global gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COOKIE = "sb_age_verified"


def page_key(rel: str) -> str:
    parts = rel.split("/")
    name = parts[-1]
    if name == "index.html":
        return "/".join(parts[:-1])
    return "/".join(parts[:-1] + [name[:-5]])


def expected_gates() -> set[str]:
    keys = set()
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "age-check/")):
            continue
        parts = rel.split("/")
        idx = 1 if parts[0] in ("en", "ja", "ko") else 0
        if idx >= len(parts) - 1 or parts[idx] not in ("vn", "novel"):
            continue
        key = page_key(rel)
        if "subscribe" in key:
            continue
        keys.add("/" + key)
    return keys


def main() -> int:
    errors: list[str] = []
    cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    rules = {r.get("source"): r for r in cfg.get("redirects", [])}
    gates = set(rules)

    missing = sorted(expected_gates() - gates)
    stale = sorted(gates - expected_gates())
    if missing:
        errors.append("pages without an age gate: " + ", ".join(missing))
    if stale:
        errors.append("gate rules without a matching page: " + ", ".join(stale))

    public = {
        "/vn/feed.xml", "/en/vn/feed.xml",
        "/vn/subscribe", "/en/vn/subscribe", "/age-check",
    }
    leaked = sorted(public & gates)
    if leaked:
        errors.append("public entry points must not be gated: " + ", ".join(leaked))

    for source, rule in rules.items():
        expected_dest = "/age-check?next=" + str(source)
        if rule.get("destination") != expected_dest:
            errors.append("bad destination for " + str(source))
        cond = rule.get("missing") or []
        if not any(c.get("type") == "cookie" and c.get("key") == COOKIE for c in cond):
            errors.append("missing cookie condition for " + str(source))
        if rule.get("permanent") is not False:
            errors.append("gate redirect must be temporary: " + str(source))

    capture = []
    for d in ("quiz/result", "en/quiz/result", "ja/quiz/result", "ko/quiz/result"):
        capture.extend(sorted((ROOT / d).glob("*.html")))
    for rel in ("vn/subscribe.html", "en/vn/subscribe.html"):
        p = ROOT / rel
        if p.is_file():
            capture.append(p)
    for p in capture:
        s = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT).as_posix()
        if "data-sb-subscribe" not in s:
            errors.append("missing capture widget: " + rel)
        if "subscribe.js" not in s:
            errors.append("missing subscribe.js: " + rel)

    age = (ROOT / "age-check" / "index.html").read_text(encoding="utf-8")
    if "noindex" not in age:
        errors.append("age-check page must be noindex")
    if "main.js" in age:
        errors.append("age-check page must not load main.js")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("OK: %d gated pages, %d capture pages, feeds stay public"
          % (len(gates), len(capture)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
