#!/usr/bin/env python3
"""Deterministically rebuild sitemap.xml from the HTML pages in this repo.

Usage:
  python tools/gen_sitemap.py            # regenerate sitemap.xml
  python tools/gen_sitemap.py --check    # CI: fail if sitemap.xml is stale
  python tools/gen_sitemap.py --use-git  # add <lastmod> from git history

Rules:
  - One <url> per existing HTML page, per language.
  - hreflang alternates only point at pages that actually exist.
  - x-default always points at the zh-CN page (or the first available one).
  - Output is sorted, so the file is stable and diff-friendly.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.sportsboy.gay"
LANG_ORDER = ("zh-CN", "en", "ja", "ko")
PREFIX = {"zh-CN": "", "en": "en", "ja": "ja", "ko": "ko"}
EXTRA = ("vn/feed.xml", "en/vn/feed.xml")


def url_for(key: str, lang: str) -> str:
    parts = [p for p in (PREFIX[lang], key) if p]
    return SITE + ("/" + "/".join(parts) if parts else "/")


def collect():
    """Return {page_key: {lang: relative_file_path}}."""
    pages: dict[str, dict[str, str]] = {}
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        parts = rel.split("/")
        lang = "zh-CN"
        if parts[0] in ("en", "ja", "ko"):
            lang = {"en": "en", "ja": "ja", "ko": "ko"}[parts[0]]
            parts = parts[1:]
        name = parts[-1]
        if name == "index.html":
            key = "/".join(parts[:-1])
        elif name.endswith(".html"):
            key = "/".join(parts[:-1] + [name[:-5]])
        else:
            continue
        pages.setdefault(key, {})[lang] = rel
    return pages


def lastmod(rel: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        value = out.stdout.strip()
        return value[:10] if value else None
    except Exception:
        return None


def build(use_git: bool) -> str:
    pages = collect()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    entries = []
    for key, langs in pages.items():
        available = [l for l in LANG_ORDER if l in langs]
        xdefault = "zh-CN" if "zh-CN" in available else available[0]
        for lang in available:
            entries.append((url_for(key, lang), lang, langs, xdefault))
    for extra in EXTRA:
        if (ROOT / extra).exists():
            entries.append((SITE + "/" + extra, None, None, None))

    for loc, lang, langs, xdefault in sorted(entries, key=lambda e: e[0]):
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if lang is None:
            lines.append("  </url>")
            continue
        if use_git:
            stamp = lastmod(langs[lang])
            if stamp:
                lines.append(f"    <lastmod>{stamp}</lastmod>")
        for alt in LANG_ORDER:
            if alt in langs:
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{alt}" '
                    f'href="{url_for(key_for(langs), alt)}"/>'
                )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" '
            f'href="{url_for(key_for(langs), xdefault)}"/>'
        )
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def key_for(langs: dict[str, str]) -> str:
    """Recover the page key from any language's file path."""
    rel = next(iter(langs.values()))
    parts = rel.split("/")
    if parts[0] in ("en", "ja", "ko"):
        parts = parts[1:]
    name = parts[-1]
    if name == "index.html":
        return "/".join(parts[:-1])
    return "/".join(parts[:-1] + [name[:-5]])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="do not write; fail if stale")
    ap.add_argument("--use-git", action="store_true", help="include lastmod from git log")
    args = ap.parse_args()

    generated = build(args.use_git)
    target = ROOT / "sitemap.xml"
    current = target.read_text(encoding="utf-8") if target.exists() else ""

    if args.check:
        if current == generated:
            print("sitemap.xml is up to date")
            return 0
        print("sitemap.xml is STALE - run: python tools/gen_sitemap.py", file=sys.stderr)
        cur = set(current.splitlines())
        gen = set(generated.splitlines())
        for line in sorted(gen - cur):
            if line.strip():
                print("  + " + line.strip(), file=sys.stderr)
        for line in sorted(cur - gen):
            if line.strip():
                print("  - " + line.strip(), file=sys.stderr)
        return 1

    target.write_text(generated, encoding="utf-8", newline="\n")
    print(f"wrote sitemap.xml ({len(generated.splitlines())} lines, "
          f"{generated.count('<loc>')} URLs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
