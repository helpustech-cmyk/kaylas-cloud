"""Assemble videos with FFmpeg from still frames (no animation on the VPS).

Each beat becomes a few PNG frames (caption chunk x mouth open/closed). An
FFmpeg concat list holds how long each frame shows, so the VPS only encodes
one stream of stills plus the voice track.
"""

from __future__ import annotations

import re
import subprocess
import textwrap
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont

from . import audio
from .config import BRAND, Config

FALLBACK_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
GAP = 0.35  # pause between beats, seconds
INTRO_SECONDS = 3.0  # logo sting, no longer (doc section 10)
ENDCARD_SECONDS = 2.0


@lru_cache(maxsize=64)
def font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in [path, *FALLBACK_FONTS]:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


_EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]")


def clean_text(text: str) -> str:
    """Drop emoji (brand fonts have no glyphs for them); keep the rupee sign."""
    return re.sub(r"\s+", " ", _EMOJI.sub("", text)).strip()


def source_label(url: str) -> str:
    host = urlparse(url).netloc or url
    return host.removeprefix("www.")


def caption_chunks(line: str, max_words: int = 12) -> list[str]:
    words = line.split()
    if len(words) <= max_words:
        return [line]
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or (w.endswith((".", "?", "!", ",")) and len(cur) >= max_words // 2):
            chunks.append(" ".join(cur))
            cur = []
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def _text_block(d: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill, width_chars: int,
                anchor_center: bool = False, box_w: int = 0, spacing: int = 10) -> int:
    lines = textwrap.wrap(text, width=width_chars) or [""]
    x, y = xy
    for ln in lines:
        if anchor_center:
            tw = d.textlength(ln, font=fnt)
            d.text((x + (box_w - tw) / 2, y), ln, font=fnt, fill=fill, stroke_width=3, stroke_fill=(0, 0, 0))
        else:
            d.text((x, y), ln, font=fnt, fill=fill, stroke_width=3, stroke_fill=(0, 0, 0))
        y += fnt.size + spacing
    return y


def _paste_pose(canvas: Image.Image, pose_path: Path, box: tuple[int, int, int, int]) -> None:
    pose = Image.open(pose_path).convert("RGBA")
    bw, bh = box[2] - box[0], box[3] - box[1]
    scale = min(bw / pose.width, bh / pose.height)
    pose = pose.resize((int(pose.width * scale), int(pose.height * scale)), Image.LANCZOS)
    x = box[0] + (bw - pose.width) // 2
    y = box[3] - pose.height
    canvas.alpha_composite(pose, (x, y))


def compose_frame(cfg: Config, size: tuple[int, int], pose_path: Path, caption: str, screen: str,
                  source: str) -> Image.Image:
    w, h = size
    caption, screen = clean_text(caption), clean_text(screen)
    img = Image.new("RGBA", size, BRAND["green"] + (255,))
    d = ImageDraw.Draw(img)
    vertical = h > w
    title_font = font(cfg.font_title, int(min(w, h) * (0.11 if vertical else 0.12)))
    cap_font = font(cfg.font_caption, int(min(w, h) * (0.05 if vertical else 0.042)))
    small = font(cfg.font_caption, int(min(w, h) * 0.026))

    # Top bar with channel name
    bar = int(h * (0.05 if vertical else 0.07))
    d.rectangle([0, 0, w, bar], fill=BRAND["saffron"])
    d.text((int(w * 0.03), int(bar * 0.2)), BRAND["channel"], font=small, fill=(0, 0, 0))

    if vertical:
        if screen:
            _text_block(d, (int(w * 0.05), int(h * 0.09)), screen, title_font, BRAND["saffron"], 12,
                        anchor_center=True, box_w=int(w * 0.9))
        _paste_pose(img, pose_path, (int(w * 0.1), int(h * 0.42), int(w * 0.9), int(h * 0.97)))
        band_top = int(h * 0.28)
        d.rounded_rectangle([int(w * 0.04), band_top, int(w * 0.96), band_top + int(h * 0.15)],
                            radius=30, fill=(0, 0, 0, 170))
        _text_block(d, (int(w * 0.07), band_top + 25), caption, cap_font, BRAND["white"], 28,
                    anchor_center=True, box_w=int(w * 0.86))
    else:
        _paste_pose(img, pose_path, (0, bar + 10, int(w * 0.42), h - int(h * 0.2)))
        if screen:
            _text_block(d, (int(w * 0.45), int(h * 0.2)), screen, title_font, BRAND["saffron"], 14)
        band_top = h - int(h * 0.22)
        d.rectangle([0, band_top, w, h], fill=(0, 0, 0, 190))
        _text_block(d, (int(w * 0.04), band_top + 14), caption, cap_font, BRAND["white"], 58)

    if source:
        label = f"Source: {source}"
        tw = d.textlength(label, font=small)
        d.text((w - tw - int(w * 0.02), bar + 8), label, font=small, fill=BRAND["white"])
    return img.convert("RGB")


def sting_frame(cfg: Config, size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, BRAND["green"])
    d = ImageDraw.Draw(img)
    big = font(cfg.font_title, int(min(w, h) * 0.13))
    tag = font(cfg.font_caption, int(min(w, h) * 0.05))
    for text, fnt, color, y in ((BRAND["channel"], big, BRAND["saffron"], 0.38),
                                (BRAND["tagline"], tag, BRAND["white"], 0.55)):
        tw = d.textlength(text, font=fnt)
        d.text(((w - tw) / 2, h * y), text, font=fnt, fill=color, stroke_width=3, stroke_fill=(0, 0, 0))
    return img


def endcard_frame(cfg: Config, size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, BRAND["green"])
    d = ImageDraw.Draw(img)
    fnt = font(cfg.font_title, int(min(w, h) * 0.09))
    _text_block(d, (int(w * 0.05), int(h * 0.4)), "Full video on Niti Marg", fnt, BRAND["saffron"], 14,
                anchor_center=True, box_w=int(w * 0.9))
    return img


def thumbnail(cfg: Config, script: dict[str, Any], out: Path) -> Path:
    """Face left, one big number right, red circle, 3-5 words (doc section 10)."""
    w, h = 1280, 720
    img = Image.new("RGBA", (w, h), BRAND["green"] + (255,))
    d = ImageDraw.Draw(img)
    _paste_pose(img, cfg.poses_dir / "happy_pointing_closed.png", (0, 20, int(w * 0.45), h))
    text = clean_text(script.get("thumbnail_text") or script["title"])
    words = text.split()[:5]
    number = next((x for x in words if any(c.isdigit() for c in x)), "")
    rest = " ".join(x for x in words if x != number)
    if number:
        nf = font(cfg.font_title, 170)
        d.ellipse([int(w * 0.47), 60, int(w * 0.98), 360], outline=BRAND["red"], width=16)
        tw = d.textlength(number, font=nf)
        d.text((int(w * 0.725 - tw / 2), 110), number, font=nf, fill=BRAND["saffron"],
               stroke_width=6, stroke_fill=(0, 0, 0))
    _text_block(d, (int(w * 0.47), 400 if number else 160), rest, font(cfg.font_title, 82),
                BRAND["white"], 13)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, quality=90)
    return out


@dataclass
class Segment:
    image: Path
    seconds: float


def _beat_segments(cfg: Config, size: tuple[int, int], beat: dict[str, Any], idx: int, wav: Path,
                   frames_dir: Path, source: str, trailing_gap: float) -> list[Segment]:
    total = audio.duration(wav)
    chunks = caption_chunks(beat["line"])
    weights = [max(1, len(c.split())) for c in chunks]
    bounds, acc = [], 0.0
    for wgt in weights:
        acc += total * wgt / sum(weights)
        bounds.append(acc)

    runs = audio.mouth_track(wav, cfg.mouth_fps) or [(False, total)]
    if trailing_gap:
        runs = runs + [(False, trailing_gap)]

    cache: dict[tuple[int, bool], Path] = {}

    def frame(ci: int, mouth: bool) -> Path:
        key = (ci, mouth)
        if key not in cache:
            pose = cfg.poses_dir / f"{beat['pose']}_{'open' if mouth else 'closed'}.png"
            path = frames_dir / f"b{idx:02d}_c{ci:02d}_{'o' if mouth else 'c'}.png"
            compose_frame(cfg, size, pose, chunks[ci], beat.get("screen", ""), source).save(path)
            cache[key] = path
        return cache[key]

    segs: list[Segment] = []
    t = 0.0
    for mouth, secs in runs:
        end = t + secs
        while t < end - 1e-6:
            ci = next((i for i, b in enumerate(bounds) if t < b - 1e-6), len(chunks) - 1)
            cut = min(end, bounds[ci]) if ci < len(chunks) - 1 else end
            if cut <= t:
                cut = end
            img = frame(ci, mouth)
            if segs and segs[-1].image == img:
                segs[-1].seconds += cut - t
            else:
                segs.append(Segment(img, cut - t))
            t = cut
    return segs


def write_concat(segs: list[Segment], path: Path) -> None:
    lines = ["ffconcat version 1.0"]
    for s in segs:
        lines += [f"file '{s.image.resolve()}'", f"duration {s.seconds:.3f}"]
    lines.append(f"file '{segs[-1].image.resolve()}'")  # concat demuxer needs the last file twice
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def encode(cfg: Config, concat_file: Path, wav: Path, out: Path, max_seconds: float | None = None) -> None:
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat_file),
           "-i", str(wav), "-vf", f"fps={cfg.fps},format=yuv420p", "-c:v", "libx264",
           "-preset", "veryfast", "-crf", "23", "-threads", str(cfg.ffmpeg_threads),
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-shortest"]
    if max_seconds:
        cmd += ["-t", f"{max_seconds:.2f}"]
    subprocess.run(cmd + [str(out)], check=True)


def render(cfg: Config, script: dict[str, Any], beat_wavs: dict[str, Path], out: Path,
           size: tuple[int, int], beats: list[str] | None = None, intro: bool = True,
           endcard: bool = False, max_seconds: float | None = None) -> dict[str, Any]:
    """Render one video. Returns {"path", "duration", "chapters": [(beat, start)]}."""
    work = out.parent / f"{out.stem}_frames"
    work.mkdir(parents=True, exist_ok=True)
    source = source_label(script.get("source_url", ""))
    chosen = [b for b in script["beats"] if beats is None or b["beat"] in beats]
    if not chosen:
        raise ValueError("No beats to render")

    segs: list[Segment] = []
    wavs: list[Path] = []
    chapters: list[tuple[str, float]] = []
    t = 0.0
    if intro:
        sting = work / "sting.png"
        sting_frame(cfg, size).save(sting)
        segs.append(Segment(sting, INTRO_SECONDS))
        silent = work / "intro.wav"
        audio.silence(silent, INTRO_SECONDS - GAP)
        wavs.append(silent)
        t = INTRO_SECONDS
    for i, beat in enumerate(chosen):
        wav = beat_wavs[beat["beat"]]
        last = i == len(chosen) - 1
        chapters.append((beat["beat"], t))
        bsegs = _beat_segments(cfg, size, beat, i, wav, work, source, 0.0 if last else GAP)
        segs += bsegs
        t += sum(s.seconds for s in bsegs)
        wavs.append(wav)
    full_wav = work / "voice.wav"
    body_wav = work / "body.wav"
    audio.concat(wavs, body_wav, gap=GAP)
    # Keep the end card inside the length cap: trim the spoken part instead.
    if max_seconds:
        limit = max_seconds - (ENDCARD_SECONDS if endcard else 0)
        if t > limit:
            segs = trim_segments(segs, limit)
            audio.trim(body_wav, limit)
            t = limit
            chapters = [c for c in chapters if c[1] < limit]
    if endcard:
        card = work / "endcard.png"
        endcard_frame(cfg, size).save(card)
        segs.append(Segment(card, ENDCARD_SECONDS))
        silent = work / "end.wav"
        audio.silence(silent, ENDCARD_SECONDS)
        audio.concat([body_wav, silent], full_wav, gap=0.0)
        t += ENDCARD_SECONDS
    else:
        body_wav.replace(full_wav)

    concat_file = work / "frames.ffconcat"
    write_concat(segs, concat_file)
    encode(cfg, concat_file, full_wav, out)
    return {"path": str(out), "duration": round(t, 2), "chapters": chapters}


def trim_segments(segs: list[Segment], limit: float) -> list[Segment]:
    out: list[Segment] = []
    t = 0.0
    for s in segs:
        if t >= limit:
            break
        out.append(Segment(s.image, min(s.seconds, limit - t)))
        t += s.seconds
    return out
