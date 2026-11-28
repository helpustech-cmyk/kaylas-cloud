"""Prepare real pose art: cut out the plain background, name files for the renderer.

Accepted input names in the source folder (PNG, JPG or WEBP):
  <pose>.png                       one image; the renderer adds a talking head-bob
  <pose>_closed.png + <pose>_open  two mouth states for true lip-sync
Output: transparent PNGs in the poses folder with the same names.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

from .config import POSES

EXTS = (".png", ".jpg", ".jpeg", ".webp")


def cutout(img: Image.Image, tolerance: int = 40) -> Image.Image:
    """Make the background transparent by flood-filling from the image border.

    Only background-coloured pixels connected to the edge are removed, so
    white details inside the character (eyes, phone screen, teeth) stay.
    """
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sorted(c[i] for c in corners)[2] for i in range(3))  # median-ish corner colour

    def is_bg(c: tuple) -> bool:
        return all(abs(c[i] - bg[i]) <= tolerance for i in range(3))

    mask = Image.new("L", (w, h), 255)
    mp = mask.load()
    seen = bytearray(w * h)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        q.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        q.extend(((0, y), (w - 1, y)))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        if not is_bg(px[x, y]):
            continue
        mp[x, y] = 0
        if x > 0:
            q.append((x - 1, y))
        if x < w - 1:
            q.append((x + 1, y))
        if y > 0:
            q.append((x, y - 1))
        if y < h - 1:
            q.append((x, y + 1))
    mask = mask.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.0))  # soft edge
    img.putalpha(mask)
    return img


def _target_name(stem: str) -> str | None:
    for pose in POSES:
        if stem == pose or stem in (f"{pose}_open", f"{pose}_closed"):
            return stem
    return None


def prepare(src_dir: Path, dst_dir: Path, max_height: int = 1000) -> list[Path]:
    dst_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for src in sorted(src_dir.iterdir()):
        if src.suffix.lower() not in EXTS:
            continue
        name = _target_name(src.stem.lower())
        if not name:
            continue
        img = Image.open(src)
        if img.mode != "RGBA" or img.getextrema()[3][0] == 255:  # no real transparency yet
            img = cutout(img)
        if img.height > max_height:
            img = img.resize((int(img.width * max_height / img.height), max_height), Image.LANCZOS)
        dst = dst_dir / f"{name}.png"
        img.save(dst)
        out.append(dst)
    return out


def resolve(poses_dir: Path, pose: str) -> tuple[Path, Path | None]:
    """Return (closed_or_single, open_or_None) for a pose."""
    closed = poses_dir / f"{pose}_closed.png"
    single = poses_dir / f"{pose}.png"
    opened = poses_dir / f"{pose}_open.png"
    base = closed if closed.exists() else single
    if not base.exists():
        base = poses_dir / "neutral.png" if (poses_dir / "neutral.png").exists() else closed
    return base, (opened if opened.exists() else None)
