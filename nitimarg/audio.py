"""WAV helpers and loudness-based lip-sync (two mouth states per pose)."""

from __future__ import annotations

import array
import math
import wave
from pathlib import Path


def duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def silence(path: Path, seconds: float, rate: int = 22050) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * int(seconds * rate))


def concat(parts: list[Path], out: Path, gap: float = 0.35) -> list[float]:
    """Join mono 16-bit WAVs with a short pause. Returns each part's start time."""
    starts: list[float] = []
    with wave.open(str(parts[0]), "rb") as first:
        rate = first.getframerate()
    pause = b"\x00\x00" * int(gap * rate)
    t = 0.0
    with wave.open(str(out), "wb") as dst:
        dst.setnchannels(1)
        dst.setsampwidth(2)
        dst.setframerate(rate)
        for i, p in enumerate(parts):
            with wave.open(str(p), "rb") as src:
                if src.getframerate() != rate or src.getnchannels() != 1 or src.getsampwidth() != 2:
                    raise ValueError(f"{p} is not mono 16-bit at {rate} Hz")
                starts.append(t)
                n = src.getnframes()
                while True:  # stream in chunks to keep RAM flat
                    chunk = src.readframes(rate)
                    if not chunk:
                        break
                    dst.writeframes(chunk)
                t += n / rate
            if i < len(parts) - 1:
                dst.writeframes(pause)
                t += gap
    return starts


def rms_windows(path: Path, window: float) -> list[float]:
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        size = max(1, int(rate * window))
        out = []
        while True:
            raw = w.readframes(size)
            if not raw:
                break
            samples = array.array("h", raw)
            out.append(math.sqrt(sum(s * s for s in samples) / len(samples)) if samples else 0.0)
    return out


def mouth_track(path: Path, mouth_fps: int, threshold_ratio: float = 0.35) -> list[tuple[bool, float]]:
    """Return [(mouth_open, seconds), ...] runs for the audio file.

    The mouth is open when a window is louder than ``threshold_ratio`` of the
    loud end of the clip (90th percentile), which ignores single peaks.
    """
    window = 1.0 / mouth_fps
    levels = rms_windows(path, window)
    if not levels:
        return []
    ranked = sorted(levels)
    loud = ranked[int(0.9 * (len(ranked) - 1))] or 1.0
    states = [lvl > loud * threshold_ratio for lvl in levels]
    total = duration(path)
    runs: list[tuple[bool, float]] = []
    for i, s in enumerate(states):
        seg = min(window, total - i * window)
        if seg <= 0:
            break
        if runs and runs[-1][0] == s:
            runs[-1] = (s, runs[-1][1] + seg)
        else:
            runs.append((s, seg))
    return runs


def trim(path: Path, seconds: float) -> None:
    """Cut a WAV in place to ``seconds``."""
    with wave.open(str(path), "rb") as src:
        params = src.getparams()
        frames = src.readframes(int(seconds * src.getframerate()))
    with wave.open(str(path), "wb") as dst:
        dst.setparams(params)
        dst.writeframes(frames)
