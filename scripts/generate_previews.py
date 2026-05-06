#!/usr/bin/env python3
"""Generate small GIF previews from pet spritesheets."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CELL_WIDTH = 192
CELL_HEIGHT = 208
STATES = {
    "idle": (0, [280, 110, 110, 140, 140, 320]),
    "waving": (3, [140, 140, 140, 280]),
    "running": (7, [120, 120, 120, 120, 120, 220]),
    "waiting": (6, [150, 150, 150, 150, 150, 260]),
    "review": (8, [150, 150, 150, 150, 150, 280]),
}


def load_catalog() -> list[dict[str, object]]:
    return json.loads((ROOT / "pets.json").read_text(encoding="utf-8"))


def render_frame(atlas: Image.Image, row: int, column: int, scale: int) -> Image.Image:
    frame = atlas.crop(
        (
            column * CELL_WIDTH,
            row * CELL_HEIGHT,
            (column + 1) * CELL_WIDTH,
            (row + 1) * CELL_HEIGHT,
        )
    ).convert("RGBA")
    if scale != 1:
        frame = frame.resize((CELL_WIDTH * scale, CELL_HEIGHT * scale), Image.Resampling.NEAREST)
    return frame


def save_gif(frames: list[Image.Image], durations: list[int], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def generate_for_pet(slug: str, scale: int, output_root: Path) -> list[Path]:
    atlas_path = ROOT / "pets" / slug / "spritesheet.webp"
    output_dir = output_root / slug / "gifs"
    written: list[Path] = []
    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
    for state, (row, durations) in STATES.items():
        frames = [render_frame(atlas, row, column, scale) for column in range(len(durations))]
        output = output_dir / f"{state}.gif"
        save_gif(frames, durations, output)
        written.append(output)
    return written


def collect_existing_outputs() -> dict[str, bytes]:
    outputs: dict[str, bytes] = {}
    for path in (ROOT / "assets" / "previews").glob("*/gifs/*.gif"):
        outputs[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    return outputs


def collect_generated_outputs(output_root: Path) -> dict[str, bytes]:
    outputs: dict[str, bytes] = {}
    for path in output_root.glob("*/gifs/*.gif"):
        outputs[path.relative_to(output_root.parent.parent).as_posix()] = path.read_bytes()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--check", action="store_true", help="Fail if generated previews would change.")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "assets" / "previews"
            for pet in load_catalog():
                generate_for_pet(str(pet["slug"]), args.scale, output_root)
            generated = collect_generated_outputs(output_root)
        if collect_existing_outputs() != generated:
            print("Generated previews are out of date. Run `python scripts/generate_previews.py`.")
            return 1
        print("Generated previews are up to date.")
        return 0

    written: list[Path] = []
    output_root = ROOT / "assets" / "previews"
    for pet in load_catalog():
        written.extend(generate_for_pet(str(pet["slug"]), args.scale, output_root))

    print(f"Generated {len(written)} GIF preview(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
