"""Draw simple flat placeholder poses so the pipeline runs before real art exists.

Real poses replace these files one-to-one: ``poses/<pose>_open.png`` and
``poses/<pose>_closed.png``, transparent PNG, 800x1000.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from .config import BRAND, POSES

W, H = 800, 1000
SKIN = (176, 110, 72)
HAIR = (25, 20, 20)
OUTLINE = (30, 20, 20)
KURTA = BRAND["saffron"]
DUPATTA = BRAND["green"]

# Arm end points (left hand, right hand) per pose, relative to the canvas.
ARMS = {
    "neutral": ((250, 820), (550, 820)),
    "happy_pointing": ((250, 820), (720, 470)),
    "worried": ((330, 560), (470, 560)),
    "explaining": ((150, 640), (650, 640)),
    "warning": ((250, 820), (600, 360)),
    "celebrating": ((170, 330), (630, 330)),
    "thinking": ((250, 820), (470, 520)),
    "holding_phone": ((250, 820), (560, 620)),
}


def _limb(d: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int]) -> None:
    d.line([start, end], fill=OUTLINE, width=52)
    d.line([start, end], fill=KURTA, width=40)
    x, y = end
    d.ellipse([x - 30, y - 30, x + 30, y + 30], fill=SKIN, outline=OUTLINE, width=6)


def draw_pose(pose: str, mouth_open: bool) -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Body (kurta) and dupatta
    d.rounded_rectangle([210, 560, 590, 1000], radius=120, fill=KURTA, outline=OUTLINE, width=8)
    d.polygon([(240, 600), (330, 600), (560, 1000), (470, 1000)], fill=DUPATTA, outline=OUTLINE)
    # Neck, head, bun
    d.rectangle([360, 480, 440, 580], fill=SKIN, outline=OUTLINE, width=6)
    d.ellipse([310, 70, 490, 210], fill=HAIR, outline=OUTLINE, width=6)  # bun
    d.ellipse([230, 150, 570, 520], fill=SKIN, outline=OUTLINE, width=8)  # face
    d.chord([225, 140, 575, 420], 180, 360, fill=HAIR, outline=OUTLINE, width=6)  # hair
    # Eyes and round glasses
    worried = pose in ("worried", "thinking")
    for cx in (330, 470):
        d.ellipse([cx - 52, 280, cx + 52, 384], outline=OUTLINE, width=8)
        d.ellipse([cx - 20, 312, cx + 20, 352], fill=OUTLINE)
        d.ellipse([cx - 8, 318, cx + 4, 330], fill=(255, 255, 255))
        brow_y = 262 if not worried else 250
        tilt = 10 if worried else 0
        d.line([cx - 40, brow_y + (tilt if cx < 400 else -tilt),
                cx + 40, brow_y - (tilt if cx < 400 else -tilt)], fill=HAIR, width=10)
    d.line([382, 330, 418, 330], fill=OUTLINE, width=6)  # glasses bridge
    d.ellipse([392, 262, 408, 278], fill=BRAND["red"])  # bindi
    # Mouth
    if mouth_open:
        d.ellipse([360, 420, 440, 480], fill=(120, 30, 40), outline=OUTLINE, width=6)
    elif worried:
        d.arc([360, 440, 440, 490], 200, 340, fill=OUTLINE, width=8)
    else:
        d.arc([350, 400, 450, 460], 20, 160, fill=OUTLINE, width=8)
    # Arms
    left, right = ARMS.get(pose, ARMS["neutral"])
    _limb(d, (250, 640), left)
    _limb(d, (550, 640), right)
    if pose == "holding_phone":
        x, y = right
        d.rounded_rectangle([x - 40, y - 110, x + 40, y + 10], radius=12, fill=(40, 40, 60),
                            outline=OUTLINE, width=6)
    if pose == "warning":
        x, y = right
        d.rounded_rectangle([x - 12, y - 110, x + 12, y], radius=10, fill=SKIN, outline=OUTLINE, width=5)
    return img


def ensure_poses(poses_dir: Path, overwrite: bool = False) -> list[Path]:
    """Create any missing pose files. Existing (real) art is never replaced."""
    poses_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for pose in POSES:
        for state in ("open", "closed"):
            path = poses_dir / f"{pose}_{state}.png"
            if path.exists() and not overwrite:
                continue
            draw_pose(pose, state == "open").save(path)
            made.append(path)
    return made
