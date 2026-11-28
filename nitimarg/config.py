"""All settings come from environment variables (or nitimarg/.env)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(PKG_DIR / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass
class Config:
    # Paths
    data_dir: Path = field(default_factory=lambda: Path(_env("NM_DATA_DIR", str(PKG_DIR / "data"))))
    work_dir: Path = field(default_factory=lambda: Path(_env("NM_WORK_DIR", str(Path.home() / "nitimarg-work"))))
    poses_dir: Path = field(default_factory=lambda: Path(_env("NM_POSES_DIR", str(PKG_DIR / "poses"))))
    character_file: Path = field(default_factory=lambda: PKG_DIR / "characters" / "niti_didi.json")

    # Script model (Ollama Cloud by default; any Ollama host works)
    ollama_host: str = field(default_factory=lambda: _env("NM_OLLAMA_HOST", "https://ollama.com"))
    ollama_api_key: str = field(default_factory=lambda: _env("NM_OLLAMA_API_KEY"))
    ollama_model: str = field(default_factory=lambda: _env("NM_OLLAMA_MODEL", "gpt-oss:120b"))

    # Voice
    elevenlabs_api_key: str = field(default_factory=lambda: _env("NM_ELEVENLABS_API_KEY"))
    elevenlabs_voice_id: str = field(default_factory=lambda: _env("NM_ELEVENLABS_VOICE_ID"))
    elevenlabs_model: str = field(default_factory=lambda: _env("NM_ELEVENLABS_MODEL", "eleven_multilingual_v2"))
    edge_voice: str = field(default_factory=lambda: _env("NM_EDGE_VOICE", "hi-IN-SwaraNeural"))

    # Telegram (use a separate bot: the kaylas-cloud bot runs on a webhook,
    # and getUpdates polling does not work while a webhook is set)
    telegram_token: str = field(default_factory=lambda: _env("NM_TELEGRAM_BOT_TOKEN"))
    telegram_chat_id: str = field(default_factory=lambda: _env("NM_TELEGRAM_CHAT_ID"))

    # YouTube (OAuth refresh token of the channel login)
    yt_client_id: str = field(default_factory=lambda: _env("NM_YT_CLIENT_ID"))
    yt_client_secret: str = field(default_factory=lambda: _env("NM_YT_CLIENT_SECRET"))
    yt_refresh_token: str = field(default_factory=lambda: _env("NM_YT_REFRESH_TOKEN"))
    yt_privacy: str = field(default_factory=lambda: _env("NM_YT_PRIVACY", "public"))
    yt_category_id: str = field(default_factory=lambda: _env("NM_YT_CATEGORY_ID", "27"))  # Education
    teaser_delay_hours: int = field(default_factory=lambda: _int("NM_TEASER_DELAY_HOURS", 6))

    # Rendering (kept small for the 7.8 GB KVM2)
    long_size: tuple[int, int] = (1280, 720)
    short_size: tuple[int, int] = (1080, 1920)
    fps: int = field(default_factory=lambda: _int("NM_FPS", 25))
    mouth_fps: int = field(default_factory=lambda: _int("NM_MOUTH_FPS", 8))
    # The character changes pose / position this often (0 = one pose per beat)
    pose_switch_seconds: float = field(default_factory=lambda: float(_env("NM_POSE_SWITCH_SECONDS", "2.5")))
    ffmpeg_threads: int = field(default_factory=lambda: _int("NM_FFMPEG_THREADS", 2))
    short_max_seconds: int = field(default_factory=lambda: _int("NM_SHORT_MAX_SECONDS", 30))
    teaser_max_seconds: int = field(default_factory=lambda: _int("NM_TEASER_MAX_SECONDS", 15))
    font_title: str = field(default_factory=lambda: _env(
        "NM_FONT_TITLE", "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"))
    font_caption: str = field(default_factory=lambda: _env(
        "NM_FONT_CAPTION", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

    # Content rules
    nri_every: int = field(default_factory=lambda: _int("NM_NRI_EVERY", 5))
    factcheck_strict: bool = field(default_factory=lambda: _env("NM_FACTCHECK_STRICT", "0") == "1")
    website: str = field(default_factory=lambda: _env("NM_WEBSITE", "https://nitimarg.in"))

    @property
    def topics_file(self) -> Path:
        return self.data_dir / "topics.json"

    @property
    def state_file(self) -> Path:
        return self.work_dir / "state.json"


# Brand constants (doc section 10)
BRAND = {
    "channel": "Niti Marg India",
    "tagline": "Aapka Haq, Aapki Yojana",
    "saffron": (255, 153, 51),
    "green": (19, 98, 56),
    "white": (255, 255, 255),
    "red": (220, 38, 38),
}

POSES = [
    "neutral",
    "happy_pointing",
    "worried",
    "explaining",
    "warning",
    "celebrating",
    "thinking",
    "holding_phone",
]

BEATS = ["hook", "problem", "scheme", "update", "eligibility", "apply", "warning", "cta"]
