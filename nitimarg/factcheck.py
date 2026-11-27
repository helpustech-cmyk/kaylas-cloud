"""Fact check: every number in the script must appear on the official page."""

from __future__ import annotations

import html
import re
from typing import Any

import httpx

MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december"
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
# Ordinals and list markers like "24vi", "3 steps" are still checked; tiny
# counting numbers (1-3) used for "pehla/doosra/teesra" steps are skipped.
SKIP_SMALL = {"1", "2", "3"}


def page_text(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", raw_html)
    text = re.sub(r"(?s)<[^>]+>", " ", raw_html)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def fetch_source(url: str, timeout: float = 30.0) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; NitiMargBot/0.1)"}
    with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
        res = client.get(url)
        res.raise_for_status()
        return page_text(res.text)


def numbers_in(text: str) -> list[str]:
    found = []
    for m in NUM_RE.findall(text):
        n = m.replace(",", "").rstrip(".")
        if n and n not in SKIP_SMALL and n not in found:
            found.append(n)
    return found


def check(script: dict[str, Any], source_text: str) -> dict[str, Any]:
    """Return {"ok", "checked", "missing", "source_url"}.

    A number counts as found when it appears on the page with or without
    Indian/Western comma grouping.
    """
    source_digits = {n for n in numbers_in(source_text)}
    lines = " ".join(b["line"] + " " + b.get("screen", "") for b in script["beats"])
    checked = numbers_in(lines)
    missing = [n for n in checked if n not in source_digits]
    return {
        "ok": not missing and bool(source_text),
        "checked": checked,
        "missing": missing,
        "source_url": script.get("source_url"),
        "source_fetched": bool(source_text),
    }


def summary(report: dict[str, Any]) -> str:
    if not report["source_fetched"]:
        return "⚠️ Fact check: official page could not be read"
    if report["ok"]:
        return f"✅ Fact check: {len(report['checked'])} numbers found on the official page"
    return "⚠️ Fact check: not found on official page: " + ", ".join(report["missing"])
