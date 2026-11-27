"""Tiny JSON state store: used topics, Telegram offset, pending runs, streak."""

from __future__ import annotations

import fcntl
import json
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterator

DEFAULT_STATE: dict[str, Any] = {
    "videos_made": 0,
    "used_topics": [],
    "tg_offset": 0,
    "runs": {},
    "approved_days": [],
}


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_STATE))
    data = json.loads(path.read_text(encoding="utf-8"))
    for k, v in DEFAULT_STATE.items():
        data.setdefault(k, json.loads(json.dumps(v)))
    return data


def save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


@contextmanager
def single_instance(lock_path: Path) -> Iterator[None]:
    """Render one video at a time (RAM pressure, doc section 9)."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "w") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another Niti Marg job is running") from exc
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def streak(approved_days: list[str], today: date | None = None) -> int:
    """Consecutive days (ending today or yesterday) with an approval."""
    days = {date.fromisoformat(d) for d in approved_days}
    cur = today or date.today()
    if cur not in days:
        cur -= timedelta(days=1)
    count = 0
    while cur in days:
        count += 1
        cur -= timedelta(days=1)
    return count
