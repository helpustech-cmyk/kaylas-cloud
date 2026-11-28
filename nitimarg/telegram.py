"""Telegram approval gate (polling, so it works from a plain cron job)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from .config import Config

API = "https://api.telegram.org/bot{token}/{method}"


def _call(cfg: Config, method: str, files: dict | None = None, timeout: float = 60.0,
          **params: Any) -> Any:
    url = API.format(token=cfg.telegram_token, method=method)
    data = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items()}
    with httpx.Client(timeout=timeout) as client:
        res = client.post(url, data=data, files=files) if files else client.post(url, data=data)
    body = res.json()
    if not body.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {body.get('description')}")
    return body["result"]


def enabled(cfg: Config) -> bool:
    return bool(cfg.telegram_token and cfg.telegram_chat_id)


def send_text(cfg: Config, text: str, buttons: list[list[dict]] | None = None) -> Any:
    params: dict[str, Any] = {"chat_id": cfg.telegram_chat_id, "text": text,
                              "disable_web_page_preview": True}
    if buttons:
        params["reply_markup"] = {"inline_keyboard": buttons}
    return _call(cfg, "sendMessage", **params)


def send_video(cfg: Config, path: Path, caption: str, buttons: list[list[dict]] | None = None) -> Any:
    params: dict[str, Any] = {"chat_id": cfg.telegram_chat_id, "caption": caption[:1024],
                              "supports_streaming": True}
    if buttons:
        params["reply_markup"] = {"inline_keyboard": buttons}
    with open(path, "rb") as fh:
        return _call(cfg, "sendVideo", files={"video": (path.name, fh, "video/mp4")}, timeout=600.0,
                     **params)


def approval_buttons(run_id: str) -> list[list[dict]]:
    return [[
        {"text": "✅ Approve & upload", "callback_data": f"nm:approve:{run_id}"},
        {"text": "❌ Reject", "callback_data": f"nm:reject:{run_id}"},
    ], [
        {"text": "🔁 Re-make script", "callback_data": f"nm:redo:{run_id}"},
    ]]


def get_updates(cfg: Config, offset: int) -> list[dict]:
    return _call(cfg, "getUpdates", offset=offset, timeout=0, allowed_updates=["callback_query"])


def answer(cfg: Config, callback_id: str, text: str) -> None:
    _call(cfg, "answerCallbackQuery", callback_query_id=callback_id, text=text[:190])


def parse_callback(update: dict) -> tuple[str, str, str, str] | None:
    """Return (callback_id, action, run_id, chat_id) for Niti Marg buttons."""
    cq = update.get("callback_query")
    if not cq:
        return None
    parts = str(cq.get("data", "")).split(":", 2)
    if len(parts) != 3 or parts[0] != "nm":
        return None
    chat_id = str(cq.get("message", {}).get("chat", {}).get("id", ""))
    return cq["id"], parts[1], parts[2], chat_id
