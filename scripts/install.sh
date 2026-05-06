#!/usr/bin/env bash
set -euo pipefail

PET="${1:-all}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_ROOT="$REPO_ROOT/pets"
TARGET_ROOT="$CODEX_HOME/pets"

mkdir -p "$TARGET_ROOT"

install_pet() {
  local pet_id="$1"
  local source="$SOURCE_ROOT/$pet_id"
  local target="$TARGET_ROOT/$pet_id"

  if [[ ! -f "$source/pet.json" || ! -f "$source/spritesheet.webp" ]]; then
    echo "Invalid pet package: $source" >&2
    exit 1
  fi

  mkdir -p "$target"
  cp "$source/pet.json" "$target/pet.json"
  cp "$source/spritesheet.webp" "$target/spritesheet.webp"
  echo "Installed $pet_id -> $target"
}

if [[ "$PET" == "all" ]]; then
  for dir in "$SOURCE_ROOT"/*; do
    [[ -d "$dir" ]] || continue
    install_pet "$(basename "$dir")"
  done
else
  install_pet "$PET"
fi

echo "Done. Restart Codex if the new pets do not appear immediately."

