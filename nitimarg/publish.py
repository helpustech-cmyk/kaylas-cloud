"""Titles, descriptions, chapters, tags and the website post (doc section 13)."""

from __future__ import annotations

from typing import Any

from .script import CHAPTER_LABELS, slugify

DISCLAIMER = ("Yeh jaankari sirf aam samajh ke liye official sources se li gayi hai. "
              "Yeh sarkari salah nahi hai. Apply karne se pehle official website zaroor dekhein.")
MIN_CHAPTER = 10.0  # YouTube needs chapters of at least 10 seconds


def fmt_ts(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def chapters(chapter_starts: list[tuple[str, float]], total: float) -> list[tuple[str, float]]:
    """Merge chapters shorter than 10s into the previous one; first starts at 0:00."""
    if not chapter_starts:
        return []
    out: list[tuple[str, float]] = [(chapter_starts[0][0], 0.0)]
    for name, start in chapter_starts[1:]:
        if start - out[-1][1] >= MIN_CHAPTER:
            out.append((name, start))
    if len(out) > 1 and total - out[-1][1] < MIN_CHAPTER:
        out.pop()
    return out if len(out) >= 3 else []


def post_url(script: dict[str, Any], website: str) -> str:
    return f"{website.rstrip('/')}/{slugify(script['topic_name'])}"


def description(script: dict[str, Any], chapter_starts: list[tuple[str, float]], total: float,
                website: str) -> str:
    apply = next((b["line"] for b in script["beats"] if b["beat"] == "apply"), "")
    warning = next((b["line"] for b in script["beats"] if b["beat"] == "warning"), "")
    intro = script["description_intro"] or script["title"]
    parts = [
        # Only the first two lines show before the fold: keywords + official link.
        intro.splitlines()[0][:150],
        f"Official site: {script['source_url']}",
        "",
        f"📌 Yojana: {script['topic_name']}",
    ]
    if script.get("eligibility_summary"):
        parts.append(f"✅ Kaun paatra hai: {script['eligibility_summary']}")
    if script.get("amount_summary"):
        parts.append(f"💰 Kitna paisa: {script['amount_summary']}")
    if apply:
        parts.append(f"📝 Apply kaise karein: {apply}")
    if warning:
        parts.append(f"⚠️ Savdhaan: {warning}")
    parts.append(f"🌐 Poori jaankari: {post_url(script, website)}")
    chs = chapters(chapter_starts, total)
    if chs:
        parts += ["", "Chapters:"] + [f"{fmt_ts(t)} {CHAPTER_LABELS.get(n, n)}" for n, t in chs]
    parts += ["", f"Source checked on {script['source_checked']}: {script['source_url']}", DISCLAIMER,
              "", " ".join(script["hashtags"])]
    return "\n".join(parts)


def tags(script: dict[str, Any]) -> list[str]:
    extra = [h.lstrip("#") for h in script.get("extra_hashtags", [])]
    seen, out = set(), []
    for t in [*script["tags"], *extra, "niti marg", "sarkari yojana"]:
        if t.lower() not in seen and sum(len(x) for x in out) + len(t) < 450:
            seen.add(t.lower())
            out.append(t)
    return out


def pinned_comment(script: dict[str, Any]) -> str:
    return f"Official link: {script['source_url']}\n\n{script['pinned_question']}"


def short_title(script: dict[str, Any]) -> str:
    return f"{script['title'][:80]} #Shorts"


def short_description(script: dict[str, Any], long_url: str | None) -> str:
    lines = [script["title"], f"Official site: {script['source_url']}"]
    lines.append(f"Full video on Niti Marg: {long_url}" if long_url else "Full video on Niti Marg")
    return "\n".join(lines + ["", " ".join(script["hashtags"]) + " #Shorts"])


def website_post(script: dict[str, Any], video_id: str | None) -> str:
    """Markdown for the matching nitimarg.in post (website loop, doc section 12)."""
    lines = [
        "---",
        f"title: \"{script['title']}\"",
        f"slug: {slugify(script['topic_name'])}",
        f"category: {script['category']}",
        f"source: {script['source_url']}",
        f"source_checked: {script['source_checked']}",
        f"youtube: {video_id or ''}",
        "---",
        "",
        f"# {script['title']}",
        "",
    ]
    if video_id:
        lines += [f'<iframe src="https://www.youtube.com/embed/{video_id}" width="560" height="315" '
                  'allowfullscreen></iframe>', ""]
    for b in script["beats"]:
        if b["beat"] in ("hook", "cta"):
            continue
        lines += [f"## {CHAPTER_LABELS.get(b['beat'], b['beat'])}", "", b["line"], ""]
    lines += [f"Official source: [{script['source_url']}]({script['source_url']})", "", f"_{DISCLAIMER}_", ""]
    return "\n".join(lines)
