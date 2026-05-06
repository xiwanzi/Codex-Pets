# Contributing / 投稿指南

Thank you for helping grow this Codex pet collection.

感谢你为这个 Codex 桌宠合集投稿。

## Two Ways To Submit / 两种投稿方式

### 1. Pull Request / 提交 PR

Use this path if you are comfortable with GitHub forks and pull requests.

如果你会使用 GitHub fork 和 PR，推荐使用这个方式。

1. Fork this repository.
2. Put your package under `pets/<pet-slug>--<author-slug>/`.
3. Include exactly `submission.json`, `pet.json`, and `spritesheet.webp` in that pet package.
4. Add `previews/<pet-slug>--<author-slug>/contact-sheet.png`.
5. Update `pets.json`, or run `python scripts/add_pet.py ...`.
6. Run the build/check commands.

```bash
python -m pip install -r requirements.txt
python scripts/generate_previews.py
python scripts/generate_readmes.py
python scripts/validate_repo.py
```

中文步骤：

1. Fork 本仓库。
2. 把宠物包放到 `pets/<pet-slug>--<author-slug>/`。
3. 宠物包里只保留 `submission.json`、`pet.json`、`spritesheet.webp`。
4. 添加 `previews/<pet-slug>--<author-slug>/contact-sheet.png`。
5. 更新 `pets.json`，也可以使用 `python scripts/add_pet.py ...`。
6. 运行生成和校验命令。

### 2. Issue Upload / Issue 上传

Use this path if you do not want to use Git.

如果你不想使用 Git，可以直接开 Issue 投稿。

Open a "New pet submission" issue and attach a `.zip` file containing:

打开 "New pet submission" Issue，并上传一个 `.zip`，其中包含：

```text
submission.json
pet.json
spritesheet.webp
contact-sheet.png
videos/                 optional / 可选
```

A maintainer can then validate and merge it.

维护者可以帮你校验并合入仓库。

## Package Layout / 宠物包结构

Pet IDs use `pet-slug--author-slug`. This allows several authors to submit different versions of the same character without collisions.

宠物 ID 使用 `pet-slug--author-slug`，这样同一个角色可以有不同作者版本并存。

```text
pets/<pet-slug>--<author-slug>/
  submission.json
  pet.json
  spritesheet.webp

previews/<pet-slug>--<author-slug>/
  contact-sheet.png
  videos/               optional / 可选
```

`pet.json` format:

`pet.json` 格式：

```json
{
  "id": "my-pet--your-name",
  "displayName": "My Pet",
  "description": "Short English description.",
  "spritesheetPath": "spritesheet.webp"
}
```

`submission.json` format:

`submission.json` 格式：

```json
{
  "slug": "my-pet--your-name",
  "pet_slug": "my-pet",
  "author_slug": "your-name",
  "name": "My Pet",
  "name_en": "My Pet",
  "description": "Short English description.",
  "description_zh": "简短中文描述。",
  "author": "Your Name",
  "author_handle": "your-name",
  "author_url": "https://github.com/your-name",
  "primary_category": "Anime Characters",
  "primary_category_zh": "动漫人物",
  "license": "CC BY-NC-SA 4.0"
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
- 必需动作行：`idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running`、`review`。

## Rights And Fanwork / 权利与同人说明

Only submit assets you are allowed to share. If your pet is inspired by an existing character, say so in the PR or Issue.

只提交你有权分享的素材。如果宠物灵感来自已有角色，请在 PR 或 Issue 里说明。

By submitting, you agree that the pet assets can be distributed under `ASSET-LICENSE.md`.

提交即表示你同意宠物素材按 `ASSET-LICENSE.md` 分发。
