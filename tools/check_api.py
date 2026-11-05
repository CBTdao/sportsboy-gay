#!/usr/bin/env python3
"""CI unit checks for the serverless helpers (no network, no Vercel needed)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))

import age_verify as a  # noqa: E402
import subscribe as s  # noqa: E402


def main() -> int:
    v = a._issue()
    assert a._verify(v), "a freshly issued cookie must verify"
    assert not a._verify("bogus"), "a malformed cookie must be rejected"
    expired = a.VERSION + ".0." + a._signature(a.VERSION + ".0")
    assert not a._verify(expired), "an expired cookie must be rejected"
    assert a._same_origin({
        "Origin": "https://www.sportsboy.gay", "Host": "www.sportsboy.gay"})
    assert not a._same_origin({
        "Origin": "https://evil.example", "Host": "www.sportsboy.gay"})
    assert s.EMAIL_RE.match("reader@example.com")
    assert not s.EMAIL_RE.match("not-an-email")
    assert not s.EMAIL_RE.match("a@b.c")
    print("OK: age cookie issue/verify/expiry, same-origin guard, email validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
