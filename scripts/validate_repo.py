#!/usr/bin/env python3
"""Validate Codex pet packages, metadata, and generated gallery assets."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as error:
    raise SystemExit("Missing dependency: install Pillow with `python -m pip install -r requirements.txt`.") from error


ROOT = Path(__file__).resolve().parents[1]
ATLAS_WIDTH = 1536
ATLAS_HEIGHT = 1872
CELL_WIDTH = 192
CELL_HEIGHT = 208
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*--[a-z0-9]+(?:-[a-z0-9]+)*$")
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
GALLERY_STATES = ["idle", "waving", "running", "waiting", "review"]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{rel(path)}: invalid JSON: {exc}")
        return None


def alpha_nonzero_count(image: Image.Image) -> int:
    return sum(image.getchannel("A").histogram()[1:])


def validate_atlas(path: Path, slug: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"{slug}: missing {rel(path)}")
        return

    try:
        with Image.open(path) as opened:
            if opened.format not in {"WEBP", "PNG"}:
                errors.append(f"{slug}: spritesheet must be WEBP or PNG, got {opened.format}")
            if opened.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
                errors.append(f"{slug}: spritesheet must be {ATLAS_WIDTH}x{ATLAS_HEIGHT}, got {opened.size}")
            image = opened.convert("RGBA")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{slug}: cannot open spritesheet: {exc}")
        return

    if image.getpixel((0, 0))[3] != 0:
        errors.append(f"{slug}: top-left pixel must be transparent")

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
            pixels = alpha_nonzero_count(cell)
            if column_index < frame_count and pixels < 50:
                errors.append(f"{slug}: {state} frame {column_index} is empty or too sparse")
            if column_index >= frame_count and pixels != 0:
                errors.append(f"{slug}: {state} unused frame {column_index} is not transparent")


def validate_pet(slug: str, catalog_entry: dict[str, object] | None, errors: list[str]) -> None:
    pet_dir = ROOT / "pets" / slug
    if not SLUG_RE.fullmatch(slug):
        errors.append(f"{slug}: folder name must use pet-slug--author-slug")

    allowed = {"submission.json", "pet.json", "spritesheet.webp"}
    for child in pet_dir.iterdir():
        if child.name.startswith("."):
            continue
        if child.name not in allowed:
            errors.append(f"{slug}: unexpected file in pet package: {rel(child)}")

    submission = load_json(pet_dir / "submission.json", errors)
    manifest = load_json(pet_dir / "pet.json", errors)

    if isinstance(submission, dict):
        for key in [
            "slug",
            "pet_slug",
            "author_slug",
            "name",
            "name_en",
            "description",
            "description_zh",
            "author",
            "primary_category",
            "license",
        ]:
            if not submission.get(key):
                errors.append(f"{slug}: submission.json missing {key}")
        if submission.get("slug") != slug:
            errors.append(f"{slug}: submission.json slug must match folder name")

    if isinstance(manifest, dict):
        if manifest.get("id") != slug:
            errors.append(f"{slug}: pet.json id must match folder name")
        if manifest.get("spritesheetPath") != "spritesheet.webp":
            errors.append(f"{slug}: pet.json spritesheetPath must be spritesheet.webp")
        if not manifest.get("displayName"):
            errors.append(f"{slug}: pet.json displayName is required")
        if not manifest.get("description"):
            errors.append(f"{slug}: pet.json description is required")

    validate_atlas(pet_dir / "spritesheet.webp", slug, errors)

    if catalog_entry is None:
        errors.append(f"{slug}: missing from pets.json")
    else:
        if catalog_entry.get("slug") != slug:
            errors.append(f"{slug}: catalog slug mismatch")
        if isinstance(submission, dict):
            for key in ["pet_slug", "author_slug", "name", "name_en", "primary_category", "license"]:
                if catalog_entry.get(key) != submission.get(key):
                    errors.append(f"{slug}: pets.json {key} must match submission.json")

    contact_sheet = ROOT / "previews" / slug / "contact-sheet.png"
    if not contact_sheet.is_file():
        errors.append(f"{slug}: missing {rel(contact_sheet)}")

    for state in GALLERY_STATES:
        gif_path = ROOT / "assets" / "previews" / slug / "gifs" / f"{state}.gif"
        if not gif_path.is_file():
            errors.append(f"{slug}: missing generated preview {rel(gif_path)}")


def main() -> int:
    errors: list[str] = []
    catalog = load_json(ROOT / "pets.json", errors)
    if not isinstance(catalog, list):
        errors.append("pets.json must be a list")
        catalog = []

    catalog_by_slug: dict[str, dict[str, object]] = {}
    for entry in catalog:
        if not isinstance(entry, dict):
            errors.append("pets.json entries must be objects")
            continue
        slug = entry.get("slug")
        if not isinstance(slug, str):
            errors.append("pets.json entry missing slug")
            continue
        if slug in catalog_by_slug:
            errors.append(f"{slug}: duplicate pets.json entry")
        catalog_by_slug[slug] = entry

    pet_dirs = sorted(path.name for path in (ROOT / "pets").iterdir() if path.is_dir())
    for slug in pet_dirs:
        validate_pet(slug, catalog_by_slug.get(slug), errors)

    for slug in sorted(set(catalog_by_slug) - set(pet_dirs)):
        errors.append(f"{slug}: listed in pets.json but missing pets/{slug}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {len(pet_dirs)} pet package(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

