<div align="center">

# Codex Pets

English | [简体中文](./docs/zh-CN/README.md)

![pets: 2](https://img.shields.io/badge/pets-2-2ea44f) ![languages: en | zh-CN](https://img.shields.io/badge/languages-en%20%7C%20zh--CN-8250df) ![code: MIT](https://img.shields.io/badge/code-MIT-111111) ![assets: CC BY-NC-SA 4.0](https://img.shields.io/badge/assets-CC%20BY--NC--SA%204.0-f97316) ![install: one command](https://img.shields.io/badge/install-one%20command-111111) [![Validate pets](https://github.com/xiwanzi/Codex-Pets/actions/workflows/validate.yml/badge.svg)](https://github.com/xiwanzi/Codex-Pets/actions/workflows/validate.yml)

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
curl -fsSL https://raw.githubusercontent.com/xiwanzi/Codex-Pets/main/scripts/install-pet.sh | bash -s -- kanade--xiwanzi
```

List available pets:

```bash
curl -fsSL https://raw.githubusercontent.com/xiwanzi/Codex-Pets/main/scripts/install-pet.sh | bash -s -- --list
```

Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr -UseB https://raw.githubusercontent.com/xiwanzi/Codex-Pets/main/scripts/install-pet.ps1 | iex; Install-CodexPet kanade--xiwanzi"
```

## Pets

### Anime Characters

<table>
<tr><th>Name</th><td colspan="5"><a href="./pets/kanade--xiwanzi">Kanade</a> · by [@xiwanzi](https://github.com/xiwanzi) · Anime Characters</td></tr>
<tr><th>Install</th><td colspan="5"><code>curl -fsSL https://raw.githubusercontent.com/xiwanzi/Codex-Pets/main/scripts/install-pet.sh | bash -s -- kanade--xiwanzi</code></td></tr>
<tr><th>Action</th><td><strong>Idle</strong></td><td><strong>Waving</strong></td><td><strong>Running</strong></td><td><strong>Waiting</strong></td><td><strong>Review</strong></td></tr>
<tr><th>Preview</th><td><img src="./assets/previews/kanade--xiwanzi/gifs/idle.gif" alt="Kanade idle" width="120" height="130"></td><td><img src="./assets/previews/kanade--xiwanzi/gifs/waving.gif" alt="Kanade waving" width="120" height="130"></td><td><img src="./assets/previews/kanade--xiwanzi/gifs/running.gif" alt="Kanade running" width="120" height="130"></td><td><img src="./assets/previews/kanade--xiwanzi/gifs/waiting.gif" alt="Kanade waiting" width="120" height="130"></td><td><img src="./assets/previews/kanade--xiwanzi/gifs/review.gif" alt="Kanade review" width="120" height="130"></td></tr>
</table>

<table>
<tr><th>Name</th><td colspan="5"><a href="./pets/remi--xiwanzi">Remi</a> · by [@xiwanzi](https://github.com/xiwanzi) · Anime Characters</td></tr>
<tr><th>Install</th><td colspan="5"><code>curl -fsSL https://raw.githubusercontent.com/xiwanzi/Codex-Pets/main/scripts/install-pet.sh | bash -s -- remi--xiwanzi</code></td></tr>
<tr><th>Action</th><td><strong>Idle</strong></td><td><strong>Waving</strong></td><td><strong>Running</strong></td><td><strong>Waiting</strong></td><td><strong>Review</strong></td></tr>
<tr><th>Preview</th><td><img src="./assets/previews/remi--xiwanzi/gifs/idle.gif" alt="Remi idle" width="120" height="130"></td><td><img src="./assets/previews/remi--xiwanzi/gifs/waving.gif" alt="Remi waving" width="120" height="130"></td><td><img src="./assets/previews/remi--xiwanzi/gifs/running.gif" alt="Remi running" width="120" height="130"></td><td><img src="./assets/previews/remi--xiwanzi/gifs/waiting.gif" alt="Remi waiting" width="120" height="130"></td><td><img src="./assets/previews/remi--xiwanzi/gifs/review.gif" alt="Remi review" width="120" height="130"></td></tr>
</table>

## Submit a Pet

Use `pet-slug--author-slug` so multiple versions of the same character can coexist. See [CONTRIBUTING.md](./CONTRIBUTING.md) and [docs/PET_SPEC.md](./docs/PET_SPEC.md).

## License

- Code and scripts: [MIT](./LICENSE)
- Pet assets and generated previews: [asset license](./ASSET-LICENSE.md)
