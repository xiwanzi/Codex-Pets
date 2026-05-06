#!/usr/bin/env python3
"""Copy a local Codex pet package into this repository and update metadata."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*--[a-z0-9]+(?:-[a-z0-9]+)*$")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_catalog() -> list[dict[str, object]]:
    path = ROOT / "pets.json"
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise SystemExit("pets.json must be a list")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="Required format: pet-slug--author-slug.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--name-en", default="")
    parser.add_argument("--description", required=True)
    parser.add_argument("--description-zh", default="")
    parser.add_argument("--author", required=True)
    parser.add_argument("--author-handle", default="")
    parser.add_argument("--author-url", default="")
    parser.add_argument("--category", default="Others")
    parser.add_argument("--category-zh", default="其他")
    parser.add_argument("--license", default="CC BY-NC-SA 4.0")
    parser.add_argument("--source-dir", required=True, help="Directory containing pet.json and spritesheet.webp.")
    parser.add_argument("--contact-sheet", required=True)
    parser.add_argument("--videos-dir", help="Optional directory containing mp4 preview videos.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    slug = args.slug.strip().lower()
    if not SLUG_RE.fullmatch(slug):
        raise SystemExit("Invalid slug. Expected format: pet-slug--author-slug")
    pet_slug, author_slug = slug.split("--", 1)

    source_dir = Path(args.source_dir).expanduser().resolve()
    source_sheet = source_dir / "spritesheet.webp"
    contact_sheet = Path(args.contact_sheet).expanduser().resolve()
    if not (source_dir / "pet.json").is_file() or not source_sheet.is_file():
        raise SystemExit("source-dir must contain pet.json and spritesheet.webp")
    if not contact_sheet.is_file():
        raise SystemExit("contact-sheet does not exist")

    target_pet_dir = ROOT / "pets" / slug
    target_preview_dir = ROOT / "previews" / slug
    if target_pet_dir.exists() and not args.overwrite:
        raise SystemExit(f"{target_pet_dir} already exists; pass --overwrite")

    target_pet_dir.mkdir(parents=True, exist_ok=True)
    target_preview_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "id": slug,
        "displayName": args.name,
        "description": args.description,
        "spritesheetPath": "spritesheet.webp",
    }
    submission = {
        "slug": slug,
        "pet_slug": pet_slug,
        "author_slug": author_slug,
        "name": args.name,
        "name_en": args.name_en or args.name,
        "description": args.description,
        "description_zh": args.description_zh,
        "author": args.author,
        "author_handle": args.author_handle or author_slug,
        "author_url": args.author_url,
        "primary_category": args.category,
        "primary_category_zh": args.category_zh,
        "license": args.license,
    }

    write_json(target_pet_dir / "pet.json", manifest)
    write_json(target_pet_dir / "submission.json", submission)
    shutil.copy2(source_sheet, target_pet_dir / "spritesheet.webp")
    shutil.copy2(contact_sheet, target_preview_dir / "contact-sheet.png")

    if args.videos_dir:
        videos_dir = Path(args.videos_dir).expanduser().resolve()
        target_videos = target_preview_dir / "videos"
        target_videos.mkdir(parents=True, exist_ok=True)
        for video in sorted(videos_dir.glob("*.mp4")):
            shutil.copy2(video, target_videos / video.name)

    catalog = [entry for entry in load_catalog() if entry.get("slug") != slug]
    catalog.append(submission)
    catalog.sort(key=lambda entry: str(entry["slug"]))
    write_json(ROOT / "pets.json", catalog)
    print(f"Added {slug}. Run `python scripts/generate_previews.py` and `python scripts/generate_readmes.py`.")


if __name__ == "__main__":
    main()

