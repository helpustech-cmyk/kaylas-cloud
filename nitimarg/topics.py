"""Topic queue and selection (money-first, NRI roughly one in five)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_topics(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_topics(path: Path, topics: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(topics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pick_topic(topics: list[dict[str, Any]], used: list[str], videos_made: int,
               nri_every: int = 5) -> dict[str, Any]:
    """Pick the next enabled, unused topic.

    Every ``nri_every``-th video is an NRI topic when one is available.
    When every topic has been used, the oldest used one is recycled
    (schemes change, so a refresh video is still useful).
    """
    enabled = [t for t in topics if t.get("enabled", True)]
    if not enabled:
        raise ValueError("No enabled topics in topics.json")

    want_nri = nri_every > 0 and (videos_made + 1) % nri_every == 0
    fresh = [t for t in enabled if t["id"] not in used]
    pool = fresh or sorted(enabled, key=lambda t: used.index(t["id"]) if t["id"] in used else -1)

    def matches(t: dict[str, Any]) -> bool:
        return (t.get("category") == "nri") == want_nri

    preferred = [t for t in pool if matches(t)]
    candidates = preferred or pool
    candidates.sort(key=lambda t: -int(t.get("priority", 0)))
    return candidates[0]
