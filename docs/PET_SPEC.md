# Pet Package Spec / 宠物包规范

This repository stores ready-to-use Codex custom pet packages.

本仓库存放可直接使用的 Codex 自定义桌宠包。

## Package Layout / 包结构

```text
pets/<pet-id>/
  pet.json
  spritesheet.webp
```

## Manifest / 清单文件

`pet.json`:

```json
{
  "id": "my-pet",
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
- 描述应简短，面向用户。

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

行定义：

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

每行未使用的格子必须完全透明。

