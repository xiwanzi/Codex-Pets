#!/usr/bin/env python3
"""Validate Codex pet packages in this repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as error:
    raise SystemExit("Missing dependency: install Pillow with `python -m pip install pillow`.") from error


ROOT = Path(__file__).resolve().parents[1]
ATLAS_WIDTH = 1536
ATLAS_HEIGHT = 1872
CELL_WIDTH = 192
CELL_HEIGHT = 208
ROWS = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
]
PET_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")


def alpha_nonzero_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.histogram()[1:])


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        add_error(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


def validate_atlas(path: Path, pet_id: str, errors: list[str]) -> None:
    if not path.is_file():
        add_error(errors, f"{pet_id}: missing spritesheet {path.relative_to(ROOT)}")
        return

    try:
        with Image.open(path) as opened:
            if opened.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
                add_error(errors, f"{pet_id}: spritesheet must be {ATLAS_WIDTH}x{ATLAS_HEIGHT}, got {opened.size}")
            if opened.format not in {"WEBP", "PNG"}:
                add_error(errors, f"{pet_id}: spritesheet must be WEBP or PNG, got {opened.format}")
            image = opened.convert("RGBA")
    except Exception as exc:  # noqa: BLE001
        add_error(errors, f"{pet_id}: cannot open spritesheet: {exc}")
        return

    if image.getpixel((0, 0))[3] != 0:
        add_error(errors, f"{pet_id}: top-left pixel is not transparent")

    for row_index, (state, frame_count) in enumerate(ROWS):
        for column_index in range(8):
            cell = image.crop(
                (
                    column_index * CELL_WIDTH,
                    row_index * CELL_HEIGHT,
                    (column_index + 1) * CELL_WIDTH,
                    (row_index + 1) * CELL_HEIGHT,
                )
            )
            nontransparent = alpha_nonzero_count(cell)
            if column_index < frame_count and nontransparent < 50:
                add_error(errors, f"{pet_id}: {state} frame {column_index} is empty or too sparse")
            if column_index >= frame_count and nontransparent != 0:
                add_error(errors, f"{pet_id}: {state} unused frame {column_index} is not transparent")


def validate_pet_entry(entry: object, seen_ids: set[str], errors: list[str]) -> None:
    if not isinstance(entry, dict):
        add_error(errors, "pets.json: each pet entry must be an object")
        return

    pet_id = entry.get("id")
    if not isinstance(pet_id, str) or not PET_ID_RE.fullmatch(pet_id):
        add_error(errors, f"pets.json: invalid pet id {pet_id!r}")
        return
    if pet_id in seen_ids:
        add_error(errors, f"pets.json: duplicate pet id {pet_id}")
    seen_ids.add(pet_id)

    package_path = ROOT / str(entry.get("packagePath", ""))
    preview_path = ROOT / str(entry.get("previewPath", ""))
    expected_package = ROOT / "pets" / pet_id
    expected_preview = ROOT / "previews" / pet_id / "contact-sheet.png"

    if package_path != expected_package:
        add_error(errors, f"{pet_id}: packagePath must be pets/{pet_id}")
    if preview_path != expected_preview:
        add_error(errors, f"{pet_id}: previewPath must be previews/{pet_id}/contact-sheet.png")
    if not preview_path.is_file():
        add_error(errors, f"{pet_id}: missing contact sheet {preview_path.relative_to(ROOT)}")

    manifest_path = package_path / "pet.json"
    manifest = load_json(manifest_path, errors)
    if not isinstance(manifest, dict):
        return

    if manifest.get("id") != pet_id:
        add_error(errors, f"{pet_id}: pet.json id must match folder id")
    if not isinstance(manifest.get("displayName"), str) or not manifest["displayName"].strip():
        add_error(errors, f"{pet_id}: pet.json displayName is required")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        add_error(errors, f"{pet_id}: pet.json description is required")
    spritesheet_path = manifest.get("spritesheetPath")
    if not isinstance(spritesheet_path, str) or "/" in spritesheet_path or "\\" in spritesheet_path:
        add_error(errors, f"{pet_id}: spritesheetPath must be a local filename")
        return

    validate_atlas(package_path / spritesheet_path, pet_id, errors)


def main() -> int:
    errors: list[str] = []
    index = load_json(ROOT / "pets.json", errors)
    if not isinstance(index, dict):
        return 1

    if index.get("schemaVersion") != 1:
        add_error(errors, "pets.json: schemaVersion must be 1")
    pets = index.get("pets")
    if not isinstance(pets, list):
        add_error(errors, "pets.json: pets must be a list")
        pets = []

    seen_ids: set[str] = set()
    for entry in pets:
        validate_pet_entry(entry, seen_ids, errors)

    package_ids = {path.name for path in (ROOT / "pets").iterdir() if path.is_dir()}
    missing_from_index = package_ids - seen_ids
    for pet_id in sorted(missing_from_index):
        add_error(errors, f"{pet_id}: package exists but is missing from pets.json")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {len(seen_ids)} pet package(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

