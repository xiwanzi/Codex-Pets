#!/usr/bin/env python3
"""Generate bilingual README files from pets.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
RAW_BASE = "https://raw.githubusercontent.com/xiwanzi/Codex-Pets/main"
REPO_URL = "https://github.com/xiwanzi/Codex-Pets"
GALLERY_STATES = [
    ("idle", "Idle", "待机"),
    ("waving", "Waving", "挥手"),
    ("running", "Running", "忙碌"),
    ("waiting", "Waiting", "等待"),
    ("review", "Review", "审阅"),
]


def load_catalog() -> list[dict[str, object]]:
    return json.loads((ROOT / "pets.json").read_text(encoding="utf-8"))


def badge(label: str, message: str, color: str) -> str:
    safe_label = quote(label.replace("-", "--"), safe="")
    safe_message = quote(message.replace("-", "--"), safe="")
    return f"![{label}: {message}](https://img.shields.io/badge/{safe_label}-{safe_message}-{color})"


def author_link(pet: dict[str, object]) -> str:
    handle = pet.get("author_handle") or pet.get("author_slug") or pet.get("author")
    url = pet.get("author_url")
    if isinstance(url, str) and url:
        return f"[@{handle}]({url})"
    return f"@{handle}"


def install_sh(slug: str) -> str:
    return f"curl -fsSL {RAW_BASE}/scripts/install-pet.sh | bash -s -- {slug}"


def install_ps(slug: str) -> str:
    return f'powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr -UseB {RAW_BASE}/scripts/install-pet.ps1 | iex; Install-CodexPet {slug}"'


def pet_table(pet: dict[str, object], lang: str, root_prefix: str) -> str:
    slug = str(pet["slug"])
    name = str(pet["name"] if lang == "zh" else pet.get("name_en") or pet["name"])
    category = str(pet.get("primary_category_zh") if lang == "zh" else pet.get("primary_category"))
    labels = ["名称", "安装", "动作", "预览"] if lang == "zh" else ["Name", "Install", "Action", "Preview"]
    by = "作者" if lang == "zh" else "by"
    state_names = [state[2] if lang == "zh" else state[1] for state in GALLERY_STATES]
    gifs = [
        f'<img src="{root_prefix}/assets/previews/{slug}/gifs/{state[0]}.gif" alt="{name} {state[0]}" width="120" height="130">'
        for state in GALLERY_STATES
    ]
    return "\n".join(
        [
            "<table>",
            f'<tr><th>{labels[0]}</th><td colspan="5"><a href="{root_prefix}/pets/{slug}">{name}</a> · {by} {author_link(pet)} · {category}</td></tr>',
            f"<tr><th>{labels[1]}</th><td colspan=\"5\"><code>{install_sh(slug)}</code></td></tr>",
            f"<tr><th>{labels[2]}</th>{''.join(f'<td><strong>{state}</strong></td>' for state in state_names)}</tr>",
            f"<tr><th>{labels[3]}</th>{''.join(f'<td>{gif}</td>' for gif in gifs)}</tr>",
            "</table>",
        ]
    )


def category_sections(pets: list[dict[str, object]], lang: str, root_prefix: str) -> str:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for pet in pets:
        key = str(pet.get("primary_category_zh") if lang == "zh" else pet.get("primary_category"))
        grouped[key].append(pet)
    blocks: list[str] = []
    for category in sorted(grouped):
        blocks.append(f"### {category}\n\n" + "\n\n".join(pet_table(pet, lang, root_prefix) for pet in grouped[category]))
    return "\n\n".join(blocks)


def english_readme(pets: list[dict[str, object]]) -> str:
    sample = str(pets[0]["slug"]) if pets else "pet-slug--author-slug"
    badges = " ".join(
        [
            badge("pets", str(len(pets)), "2ea44f"),
            badge("languages", "en | zh-CN", "8250df"),
            badge("code", "MIT", "111111"),
            badge("assets", "CC BY-NC-SA 4.0", "f97316"),
            badge("install", "one command", "111111"),
            "[![Validate pets](https://github.com/xiwanzi/Codex-Pets/actions/workflows/validate.yml/badge.svg)](https://github.com/xiwanzi/Codex-Pets/actions/workflows/validate.yml)",
        ]
    )
    return f"""<div align="center">

# Codex Pets

English | [简体中文](./docs/zh-CN/README.md)

{badges}

</div>

A community gallery of ready-to-use custom pets for the Codex desktop app, with generated action previews and one-command installation.

Each pet is a small shareable package:

```text
pets/<pet-slug>--<author-slug>/
├── submission.json
├── pet.json
└── spritesheet.webp
```

Pet folders contain only final package files. Gallery previews are generated into `assets/previews/<pet-id>/`.

## Quick Install

No clone required. Install directly from GitHub:

```bash
{install_sh(sample)}
```

List available pets:

```bash
curl -fsSL {RAW_BASE}/scripts/install-pet.sh | bash -s -- --list
```

Windows PowerShell:

```powershell
{install_ps(sample)}
```

## Pets

{category_sections(pets, "en", ".")}

## Submit a Pet

Use `pet-slug--author-slug` so multiple versions of the same character can coexist. See [CONTRIBUTING.md](./CONTRIBUTING.md) and [docs/PET_SPEC.md](./docs/PET_SPEC.md).

## License

- Code and scripts: [MIT](./LICENSE)
- Pet assets and generated previews: [asset license](./ASSET-LICENSE.md)
"""


def chinese_readme(pets: list[dict[str, object]]) -> str:
    sample = str(pets[0]["slug"]) if pets else "pet-slug--author-slug"
    return f"""<div align="center">

# Codex Pets

[English](../../README.md) | 简体中文

</div>

一个收集 Codex 桌面宠物的社区画廊，带自动生成的动作预览，并支持一条命令快速安装。

每个宠物都是一个很小的可分享包：

```text
pets/<pet-slug>--<author-slug>/
├── submission.json
├── pet.json
└── spritesheet.webp
```

pet 目录只放最终成品文件。预览图会自动生成到 `assets/previews/<pet-id>/`。

## 快速安装

不需要 clone 仓库，直接从 GitHub 安装：

```bash
{install_sh(sample)}
```

查看可安装的 pet：

```bash
curl -fsSL {RAW_BASE}/scripts/install-pet.sh | bash -s -- --list
```

Windows PowerShell：

```powershell
{install_ps(sample)}
```

## Pet 收录

{category_sections(pets, "zh", "../..")}

## 投稿

目录名使用 `pet-slug--author-slug`，这样同一个角色的不同作者版本可以并存。详见 [CONTRIBUTING.md](../../CONTRIBUTING.md) 和 [docs/PET_SPEC.md](../PET_SPEC.md)。

## 许可证

- 代码和脚本：[MIT](../../LICENSE)
- pet 资产和自动生成预览：[素材许可](../../ASSET-LICENSE.md)
"""


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    pets = sorted(load_catalog(), key=lambda pet: str(pet["name_en"]).lower())
    outputs = {
        ROOT / "README.md": english_readme(pets),
        ROOT / "docs" / "zh-CN" / "README.md": chinese_readme(pets),
    }

    changed: list[Path] = []
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        changed.append(path)
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if args.check and changed:
        print("Generated README files are out of date:")
        for path in changed:
            print(f"- {path.relative_to(ROOT).as_posix()}")
        return 1

    print(f"README generation complete ({len(changed)} changed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
