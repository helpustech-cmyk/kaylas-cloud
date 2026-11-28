"""Ollama (Cloud or local) chat client returning JSON."""

from __future__ import annotations

import json
import re
from typing import Any

import httpx

from .config import Config


def extract_json(text: str) -> dict[str, Any]:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fence:
        text = fence.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Model reply had no JSON object")
    return json.loads(text[start:end + 1])


def chat_json(cfg: Config, system: str, user: str, temperature: float = 0.6) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if cfg.ollama_api_key:
        headers["Authorization"] = f"Bearer {cfg.ollama_api_key}"
    payload = {
        "model": cfg.ollama_model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "stream": False,
        "format": "json",
        "options": {"temperature": temperature},
    }
    with httpx.Client(timeout=300.0) as client:
        res = client.post(f"{cfg.ollama_host.rstrip('/')}/api/chat", headers=headers, json=payload)
        res.raise_for_status()
        return extract_json(res.json()["message"]["content"])
