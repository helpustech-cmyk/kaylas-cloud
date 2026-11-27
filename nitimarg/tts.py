"""Voice: ElevenLabs (locked voice) with Edge-TTS as the free fallback."""

from __future__ import annotations

import array
import asyncio
import logging
import math
import os
import subprocess
import wave
from pathlib import Path

import httpx

from .config import Config

log = logging.getLogger(__name__)


def elevenlabs(cfg: Config, text: str, out_mp3: Path) -> None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{cfg.elevenlabs_voice_id}"
    headers = {"xi-api-key": cfg.elevenlabs_api_key, "Accept": "audio/mpeg"}
    body = {
        "text": text,
        "model_id": cfg.elevenlabs_model,
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.2},
    }
    with httpx.Client(timeout=120.0) as client:
        with client.stream("POST", url, headers=headers, json=body) as res:
            res.raise_for_status()
            with open(out_mp3, "wb") as fh:
                for chunk in res.iter_bytes():
                    fh.write(chunk)


def edge(cfg: Config, text: str, out_mp3: Path) -> None:
    import edge_tts  # optional dependency, imported lazily

    async def _run() -> None:
        proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        await edge_tts.Communicate(text, cfg.edge_voice, proxy=proxy).save(str(out_mp3))

    asyncio.run(_run())


def to_wav(src: Path, dst: Path, rate: int = 22050) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(rate),
         "-sample_fmt", "s16", str(dst)],
        check=True,
    )


def preview(text: str, out_wav: Path, rate: int = 22050) -> None:
    """Offline stand-in voice (syllable-like tones) for layout checks.

    Timing follows normal Hinglish speech (~2.6 words a second) so a
    preview render has realistic lengths and lip-sync without any API.
    """
    words = text.split()
    samples = array.array("h")
    for w in words:
        syllables = max(1, sum(ch in "aeiouAEIOU" for ch in w))
        for _ in range(syllables):
            n = int(rate * 0.38 / 1.5)
            for i in range(n):
                env = math.sin(math.pi * i / n)
                samples.append(int(9000 * env * math.sin(2 * math.pi * 190 * i / rate)))
        samples.extend([0] * int(rate * 0.08))
        if w.endswith((".", "?", "!", ",")):
            samples.extend([0] * int(rate * 0.25))
    with wave.open(str(out_wav), "wb") as fh:
        fh.setnchannels(1)
        fh.setsampwidth(2)
        fh.setframerate(rate)
        fh.writeframes(samples.tobytes())


def speak(cfg: Config, text: str, out_wav: Path) -> str:
    """Synthesize ``text`` to a mono 16-bit WAV. Returns the engine used."""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    if os.getenv("NM_TTS") == "preview":
        preview(text, out_wav)
        return "preview"
    mp3 = out_wav.with_suffix(".mp3")
    engine = "edge"
    if cfg.elevenlabs_api_key and cfg.elevenlabs_voice_id:
        try:
            elevenlabs(cfg, text, mp3)
            engine = "elevenlabs"
        except Exception as exc:  # quota, network, bad key: fall back
            log.warning("ElevenLabs failed (%s); using Edge-TTS", exc)
    if engine == "edge":
        edge(cfg, text, mp3)
    to_wav(mp3, out_wav)
    mp3.unlink(missing_ok=True)
    return engine
