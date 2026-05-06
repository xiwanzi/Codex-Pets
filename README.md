# Codex Desktop Pets / Codex 桌宠合集

Ready-to-use custom desktop pets for the Codex desktop app.

这是一个已经打包好的 Codex 桌面宠物合集。下载后可以直接复制到本机 Codex 的 `pets` 目录，不需要重新生成 spritesheet。

## Pets / 宠物列表

| ID | Name / 名称 | Package / 包目录 | Preview / 预览 |
| --- | --- | --- | --- |
| `kanade` | 宵崎奏 / Kanade | `pets/kanade` | `previews/kanade/contact-sheet.png` |
| `remi` | Remi / 蕾米莉亚风格 Remi | `pets/remi` | `previews/remi/contact-sheet.png` |

## Install / 安装

### Windows PowerShell

```powershell
.\scripts\install.ps1
```

Install one pet only:

```powershell
.\scripts\install.ps1 -Pet remi
```

只安装一只宠物：

```powershell
.\scripts\install.ps1 -Pet kanade
```

### macOS / Linux

```bash
bash scripts/install.sh
```

Install one pet only:

```bash
bash scripts/install.sh remi
```

### Manual install / 手动安装

Copy each pet folder under `pets/` into your Codex config directory:

把 `pets/` 下的宠物文件夹复制到 Codex 配置目录：

```text
Windows: %USERPROFILE%\.codex\pets\<pet-id>\
macOS/Linux: ~/.codex/pets/<pet-id>/
```

Each pet folder must contain:

每个宠物目录必须包含：

```text
pet.json
spritesheet.webp
```

Restart Codex after installing if the new pet does not appear immediately.

如果安装后没有立刻显示，重启 Codex。当前 Codex 桌面端有时不会热加载新宠物资源。

## Preview / 预览

Contact sheets:

预览图：

- `previews/kanade/contact-sheet.png`
- `previews/remi/contact-sheet.png`

State preview videos are under:

状态动画预览视频在：

- `previews/kanade/videos/`
- `previews/remi/videos/`

## Format / 格式

These pets follow the current Codex custom pet package shape:

这些宠物遵循当前 Codex 自定义宠物包格式：

- `spritesheet.webp`: `1536x1872`, RGBA, 8 columns x 9 rows.
- `pet.json`: pet id, display name, description, and spritesheet path.
- Cell size: `192x208`.
- Rows: `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`.

## License / 许可证

- Repo docs and install scripts are licensed under MIT. See `LICENSE`.
- Pet artwork, spritesheets, contact sheets, and preview videos are licensed under the asset terms in `ASSET-LICENSE.md`.

- 仓库文档和安装脚本使用 MIT 许可证，见 `LICENSE`。
- 宠物图像、spritesheet、预览图和视频使用 `ASSET-LICENSE.md` 中的素材许可。

## Fanwork notice / 同人声明

Some pets are fan-made, character-inspired assets. This repository is unofficial and is not affiliated with OpenAI, Codex, SEGA, Colorful Palette, Team Shanghai Alice, or any original rights holders.

部分宠物是基于角色印象制作的同人风格素材。本仓库为非官方项目，与 OpenAI、Codex、SEGA、Colorful Palette、上海爱丽丝幻乐团或任何原权利方无关。

