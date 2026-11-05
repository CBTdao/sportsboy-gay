#!/usr/bin/env python3
"""Validate internal links in every HTML page.

Catches protocol-relative URLs (href="//x"), missing pages, and missing
local assets. Prints a report and exits 1 on any broken link.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
ASSET_EXT = (".html", ".xml", ".json", ".js", ".css", ".png", ".jpg", ".jpeg",
             ".webp", ".svg", ".ico", ".txt", ".xsl", ".webmanifest")
SKIP_PREFIX = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#")
# Injected by the hosting platform at runtime; no local file exists in the repo.
RUNTIME_PREFIX = ("/_vercel/", "/api/")


def exists_for(path: str) -> bool:
    p = path.lstrip("/")
    if p == "":
        return (ROOT / "index.html").exists()
    if p.endswith(ASSET_EXT):
        return (ROOT / p).is_file()
    return (ROOT / (p + ".html")).is_file() or (ROOT / p / "index.html").is_file()


def main() -> int:
    broken: list[tuple[str, str, str]] = []
    checked = 0
    for page in sorted(ROOT.rglob("*.html")):
        rel = page.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        text = page.read_text(encoding="utf-8", errors="ignore")
        for attr in ("href", "src"):
            for value in re.findall(attr + r'="([^"]*)"', text, flags=re.I):
                raw = value.strip()
                if not raw or raw.startswith(SKIP_PREFIX):
                    continue
                if raw.startswith("//"):
                    broken.append((rel, value, "protocol-relative URL resolves to a different host"))
                    continue
                if raw.startswith(RUNTIME_PREFIX):
                    continue
                path = raw.split("#", 1)[0].split("?", 1)[0]
                if not path:
                    continue
                checked += 1
                if path.startswith("/"):
                    target = unquote(path)
                else:
                    try:
                        target = (page.parent / path).resolve().relative_to(ROOT).as_posix()
                    except ValueError:
                        broken.append((rel, value, "reference escapes the repository"))
                        continue
                    target = "/" + target
                if not exists_for(target):
                    broken.append((rel, value, "target not found"))

    if broken:
        print(f"BROKEN LINKS: {len(broken)} (checked {checked} local references)")
        for page, value, why in broken:
            print(f"  {page}: {value}  -> {why}")
        return 1
    print(f"OK: {checked} local references checked, no broken links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
