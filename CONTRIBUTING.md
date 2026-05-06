# Contributing / 投稿指南

Thank you for helping grow this Codex pet collection.

感谢你为这个 Codex 桌宠合集投稿。

## Two Ways To Submit / 两种投稿方式

### 1. Pull Request / 提交 PR

Use this path if you are comfortable with GitHub forks and pull requests.

如果你会使用 GitHub fork 和 PR，推荐使用这个方式。

1. Fork this repository.
2. Add your pet package under `pets/<pet-id>/`.
3. Add a contact sheet under `previews/<pet-id>/contact-sheet.png`.
4. Optionally add state preview videos under `previews/<pet-id>/videos/`.
5. Update `pets.json`.
6. Run validation:

```bash
python -m pip install pillow
python scripts/validate_repo.py
```

1. Fork 本仓库。
2. 把宠物包放到 `pets/<pet-id>/`。
3. 把预览图放到 `previews/<pet-id>/contact-sheet.png`。
4. 可选：把状态预览视频放到 `previews/<pet-id>/videos/`。
5. 更新 `pets.json`。
6. 运行校验：

```bash
python -m pip install pillow
python scripts/validate_repo.py
```

### 2. Issue Upload / Issue 上传

Use this path if you do not want to use Git.

如果你不想使用 Git，可以直接开 Issue 投稿。

Open a "New pet submission" issue and attach a `.zip` file containing:

打开 "New pet submission" Issue，并上传一个 `.zip`，其中包含：

```text
pet.json
spritesheet.webp
contact-sheet.png
videos/                 optional / 可选
```

A maintainer can then validate and merge it.

维护者可以帮你校验并合入仓库。

## Required Pet Package / 必需宠物包结构

```text
pets/<pet-id>/
  pet.json
  spritesheet.webp

previews/<pet-id>/
  contact-sheet.png
  videos/               optional / 可选
```

`pet.json` format:

`pet.json` 格式：

```json
{
  "id": "my-pet",
  "displayName": "My Pet",
  "description": "Short English description.",
  "spritesheetPath": "spritesheet.webp"
}
```

## Asset Requirements / 素材要求

- `spritesheet.webp` must be `1536x1872`.
- It must have alpha transparency.
- The atlas must use 8 columns x 9 rows.
- Each cell is `192x208`.
- Unused cells must be transparent.
- Required rows: `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`.

- `spritesheet.webp` 必须是 `1536x1872`。
- 必须带 alpha 透明通道。
- 图集必须是 8 列 x 9 行。
- 每格尺寸是 `192x208`。
- 未使用的格子必须透明。
- 必需行：`idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running`、`review`。

## Metadata / 元数据

Update `pets.json` with both English and Chinese metadata when possible.

尽量在 `pets.json` 中同时填写英文和中文元数据。

```json
{
  "id": "my-pet",
  "displayName": "My Pet",
  "displayNameEn": "My Pet",
  "description": "Short English description.",
  "descriptionZh": "简短中文描述。",
  "packagePath": "pets/my-pet",
  "previewPath": "previews/my-pet/contact-sheet.png"
}
```

## Rights And Fanwork / 权利与同人说明

Only submit assets you are allowed to share. If your pet is inspired by an existing character, say so in the PR or Issue.

只提交你有权分享的素材。如果桌宠灵感来自已有角色，请在 PR 或 Issue 里说明。

By submitting, you agree that the pet assets can be distributed under `ASSET-LICENSE.md`.

提交即表示你同意宠物素材按 `ASSET-LICENSE.md` 分发。

