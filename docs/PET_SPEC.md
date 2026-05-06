# Pet Package Spec / 宠物包规范

This repository stores ready-to-use Codex custom pet packages.

本仓库存放可直接使用的 Codex 自定义桌宠包。

## Package Layout / 包结构

Each pet package uses `pet-slug--author-slug` as its folder name.

每个宠物包用 `pet-slug--author-slug` 作为目录名。

```text
pets/<pet-slug>--<author-slug>/
  submission.json
  pet.json
  spritesheet.webp
```

The package directory should contain only these three final files. Generated gallery assets live under `assets/previews/<pet-slug>--<author-slug>/`.

宠物包目录只应包含这三个最终文件。画廊预览会生成到 `assets/previews/<pet-slug>--<author-slug>/`。

## Manifest / 清单文件

`pet.json`:

```json
{
  "id": "my-pet--your-name",
  "displayName": "My Pet",
  "description": "Short description.",
  "spritesheetPath": "spritesheet.webp"
}
```

Rules:

规则：

- `id` must match the folder name.
- `spritesheetPath` should normally be `spritesheet.webp`.
- Keep descriptions short and user-facing.

- `id` 必须与目录名一致。
- `spritesheetPath` 通常应为 `spritesheet.webp`。
- 描述应简短，并面向最终用户。

## Submission Metadata / 投稿元数据

`submission.json` is the source metadata copied into `pets.json` and used by README generation.

`submission.json` 是会同步到 `pets.json`、并用于生成 README 的源元数据。

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

## Spritesheet / 精灵图

```text
Width: 1536 px
Height: 1872 px
Columns: 8
Rows: 9
Cell: 192x208 px
Format: WebP or PNG with alpha
```

Rows:

行动作定义：

| Row | State | Frames |
| --- | --- | --- |
| 0 | `idle` | 6 |
| 1 | `running-right` | 8 |
| 2 | `running-left` | 8 |
| 3 | `waving` | 4 |
| 4 | `jumping` | 5 |
| 5 | `failed` | 8 |
| 6 | `waiting` | 6 |
| 7 | `running` | 6 |
| 8 | `review` | 6 |

Unused cells in each row must be fully transparent.

每行动作中未使用的格子必须完全透明。
