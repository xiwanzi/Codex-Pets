#!/usr/bin/env bash
set -euo pipefail

PET="${1:-all}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_ROOT="$REPO_ROOT/pets"
TARGET_ROOT="$CODEX_HOME/pets"

install_pet() {
  local pet_id="$1"
  local source="$SOURCE_ROOT/$pet_id"
  local target="$TARGET_ROOT/$pet_id"

  if [[ ! "$pet_id" =~ ^[a-z0-9]+(-[a-z0-9]+)*--[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "Invalid pet id: $pet_id" >&2
    echo "Expected format: pet-slug--author-slug" >&2
    exit 1
  fi

  if [[ ! -f "$source/pet.json" || ! -f "$source/spritesheet.webp" ]]; then
    echo "Invalid pet package: $source" >&2
    exit 1
  fi

  mkdir -p "$target"
  cp "$source/pet.json" "$target/pet.json"
  cp "$source/spritesheet.webp" "$target/spritesheet.webp"
  echo "Installed $pet_id -> $target"
}

mkdir -p "$TARGET_ROOT"

if [[ "$PET" == "all" ]]; then
  for dir in "$SOURCE_ROOT"/*; do
    [[ -d "$dir" ]] || continue
    install_pet "$(basename "$dir")"
  done
else
  install_pet "$PET"
fi

echo "Done. Restart Codex if the new pets do not appear immediately."
