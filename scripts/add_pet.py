#!/usr/bin/env python3
"""Copy a local Codex pet package into this repository and update pets.json."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PET_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="Pet id, for example remi.")
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--display-name-en", default="")
    parser.add_argument("--description", required=True, help="English description.")
    parser.add_argument("--description-zh", default="")
    parser.add_argument("--source-dir", required=True, help="Directory containing pet.json and spritesheet.webp.")
    parser.add_argument("--contact-sheet", required=True, help="Path to contact-sheet.png.")
    parser.add_argument("--videos-dir", help="Optional directory containing mp4 preview videos.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    pet_id = args.id.strip().lower()
    if not PET_ID_RE.fullmatch(pet_id):
        raise SystemExit("Invalid pet id. Use lowercase letters, numbers, and hyphens only.")

    source_dir = Path(args.source_dir).expanduser().resolve()
    source_manifest = source_dir / "pet.json"
    source_sheet = source_dir / "spritesheet.webp"
    contact_sheet = Path(args.contact_sheet).expanduser().resolve()

    if not source_manifest.is_file() or not source_sheet.is_file():
        raise SystemExit("source-dir must contain pet.json and spritesheet.webp")
    if not contact_sheet.is_file():
        raise SystemExit("contact-sheet does not exist")

    target_pet_dir = ROOT / "pets" / pet_id
    target_preview_dir = ROOT / "previews" / pet_id
    if target_pet_dir.exists() and not args.overwrite:
        raise SystemExit(f"{target_pet_dir} already exists; pass --overwrite to replace it")

    target_pet_dir.mkdir(parents=True, exist_ok=True)
    target_preview_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "id": pet_id,
        "displayName": args.display_name,
        "description": args.description,
        "spritesheetPath": "spritesheet.webp",
    }
    write_json(target_pet_dir / "pet.json", manifest)
    shutil.copy2(source_sheet, target_pet_dir / "spritesheet.webp")
    shutil.copy2(contact_sheet, target_preview_dir / "contact-sheet.png")

    if args.videos_dir:
        videos_dir = Path(args.videos_dir).expanduser().resolve()
        target_videos = target_preview_dir / "videos"
        target_videos.mkdir(parents=True, exist_ok=True)
        for video in sorted(videos_dir.glob("*.mp4")):
            shutil.copy2(video, target_videos / video.name)

    index_path = ROOT / "pets.json"
    index = load_json(index_path)
    pets = index.setdefault("pets", [])
    pets[:] = [entry for entry in pets if entry.get("id") != pet_id]
    pets.append(
        {
            "id": pet_id,
            "displayName": args.display_name,
            "displayNameEn": args.display_name_en or args.display_name,
            "description": args.description,
            "descriptionZh": args.description_zh,
            "packagePath": f"pets/{pet_id}",
            "previewPath": f"previews/{pet_id}/contact-sheet.png",
        }
    )
    pets.sort(key=lambda entry: entry["id"])
    write_json(index_path, index)

    print(f"Added {pet_id}. Run: python scripts/validate_repo.py")


if __name__ == "__main__":
    main()

