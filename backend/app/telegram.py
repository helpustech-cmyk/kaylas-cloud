import os
from datetime import datetime
from typing import Optional

import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def _enabled() -> bool:
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)


async def send_telegram_message(text: str) -> Optional[dict]:
    if not _enabled():
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        res = await client.post(url, json=payload)
        res.raise_for_status()
        return res.json()


def format_lead_alert(name: str, email: str, phone: Optional[str] = None, country_code: Optional[str] = None, company: Optional[str] = None, source: Optional[str] = None, message: Optional[str] = None) -> str:
    lines = [
        "🔔 *New lead on kaylas.cloud*",
        f"*Name:* {name}",
        f"*Email:* {email}",
    ]
    if phone:
        cc = country_code or "+91"
        lines.append(f"*Phone:* {cc} {phone}")
    if company:
        lines.append(f"*Company:* {company}")
    if source:
        lines.append(f"*Source:* {source}")
    if message:
        lines.append(f"*Message:* {message}")
    lines.append(f"_Time: {datetime.utcnow().isoformat()}Z_")
    return "\n".join(lines)
