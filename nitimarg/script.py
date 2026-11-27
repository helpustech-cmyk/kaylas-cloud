"""Script generation and validation (story structure, doc section 4)."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from .config import BEATS, POSES, Config
from .llm import chat_json

BEAT_POSE = {
    "hook": "worried",
    "problem": "worried",
    "scheme": "explaining",
    "update": "happy_pointing",
    "eligibility": "explaining",
    "apply": "holding_phone",
    "warning": "warning",
    "cta": "celebrating",
}

CHAPTER_LABELS = {
    "hook": "Shuruaat",
    "problem": "Problem",
    "scheme": "Yojana kya hai",
    "update": "Latest update",
    "eligibility": "Kaun paatra hai",
    "apply": "Apply kaise karein",
    "warning": "Savdhaan",
    "cta": "Agli video",
}


def load_character(cfg: Config) -> dict[str, Any]:
    return json.loads(cfg.character_file.read_text(encoding="utf-8"))


def build_prompt(topic: dict[str, Any], character: dict[str, Any], source_text: str) -> tuple[str, str]:
    system = character["persona_prompt"]
    user = f"""Write one Niti Marg video script as JSON.

Topic: {topic['name']}
Category: {topic.get('category', 'general')}
Official source: {topic['official_url']}
Keywords: {', '.join(topic.get('keywords', []))}

Official source text (use ONLY numbers, dates and rules found here):
---
{source_text[:6000]}
---

Rules:
- Simple Hinglish in Latin script, short sentences, elder-sister tone, never talk down.
- Money first: the hook names money the viewer may be missing.
- Beats in this order: {', '.join(BEATS)} ("update" may be omitted if there is no recent update).
- "apply" gives exactly three steps. "warning" names the common mistake or scam.
- Each beat: 1 to 3 sentences, max about 45 words.
- pose must be one of: {', '.join(POSES)}.
- screen is 1 to 5 words shown big on screen (a number or key word).
- Never invent numbers. If unsure, leave the number out.

JSON shape:
{{
  "title": "Hinglish title under 90 chars, money-first, pattern like 'Sarkar aapko paise de rahi hai, kahin aap chhoot toh nahi gaye?'",
  "thumbnail_text": "3 to 5 words with one big number",
  "beats": [{{"beat": "hook", "pose": "worried", "line": "...", "screen": "..."}}],
  "description_intro": "two lines with the main keywords",
  "eligibility_summary": "...",
  "amount_summary": "...",
  "tags": ["10 to 15 lowercase search tags"],
  "hashtags": ["#Three", "#Hashtags", "#NitiMarg"],
  "pinned_question": "one Hinglish question to start comments",
  "short": {{"hook": "max 22 words, for the 30-second Short", "warning": "max 22 words"}},
  "playlist": "one of: Kisan schemes, Women schemes, Loans and cards, NRI money, PM tenure series"
}}"""
    return system, user


def normalise(script: dict[str, Any], topic: dict[str, Any]) -> dict[str, Any]:
    """Validate and fill defaults so rendering never crashes on model output."""
    beats = []
    for b in script.get("beats", []):
        name = str(b.get("beat", "")).strip().lower()
        line = str(b.get("line", "")).strip()
        if name not in BEATS or not line:
            continue
        pose = str(b.get("pose", "")).strip().lower()
        if pose not in POSES:
            pose = BEAT_POSE.get(name, "neutral")
        beats.append({"beat": name, "pose": pose, "line": line,
                      "screen": str(b.get("screen", "")).strip()[:40]})
    order = {n: i for i, n in enumerate(BEATS)}
    beats.sort(key=lambda b: order[b["beat"]])
    missing = [n for n in ("hook", "scheme", "eligibility", "apply", "warning", "cta")
               if n not in {b["beat"] for b in beats}]
    if missing:
        raise ValueError(f"Script is missing beats: {', '.join(missing)}")

    tags = [str(t).strip().lower() for t in script.get("tags", []) if str(t).strip()]
    hashtags = [h if str(h).startswith("#") else f"#{h}" for h in script.get("hashtags", [])]
    if "#NitiMarg" not in hashtags:
        hashtags.append("#NitiMarg")
    return {
        "topic_id": topic["id"],
        "topic_name": topic["name"],
        "category": topic.get("category", "general"),
        "source_url": topic["official_url"],
        "source_checked": script.get("source_checked") or date.today().isoformat(),
        "title": str(script.get("title", topic["name"])).strip()[:100],
        "thumbnail_text": str(script.get("thumbnail_text", "")).strip(),
        "beats": beats,
        "description_intro": str(script.get("description_intro", "")).strip(),
        "eligibility_summary": str(script.get("eligibility_summary", "")).strip(),
        "amount_summary": str(script.get("amount_summary", "")).strip(),
        "tags": tags[:20],
        "hashtags": hashtags[:3],
        "extra_hashtags": hashtags[3:],
        "pinned_question": str(script.get("pinned_question", "Aapka sawaal comment mein likhein.")).strip(),
        "playlist": str(script.get("playlist", "")).strip(),
        "short_beats": script.get("short_beats") or ["hook", "warning"],
        "short": {k: str(v).strip() for k, v in (script.get("short") or {}).items()
                  if k in ("hook", "warning") and str(v).strip()},
    }


def generate_script(cfg: Config, topic: dict[str, Any], source_text: str) -> dict[str, Any]:
    character = load_character(cfg)
    system, user = build_prompt(topic, character, source_text)
    last_err: Exception | None = None
    for _ in range(2):
        try:
            return normalise(chat_json(cfg, system, user), topic)
        except (ValueError, KeyError) as exc:
            last_err = exc
    raise RuntimeError(f"Script generation failed: {last_err}")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def save_script(script: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
