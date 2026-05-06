param(
    [ValidateSet("all", "kanade", "remi")]
    [string]$Pet = "all",
    [string]$CodexHome = "$env:USERPROFILE\.codex"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repoRoot "pets"
$targetRoot = Join-Path $CodexHome "pets"

if ($Pet -eq "all") {
    $pets = Get-ChildItem -LiteralPath $sourceRoot -Directory | Select-Object -ExpandProperty Name
} else {
    $pets = @($Pet)
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

foreach ($petId in $pets) {
    $source = Join-Path $sourceRoot $petId
    $target = Join-Path $targetRoot $petId
    if (!(Test-Path -LiteralPath (Join-Path $source "pet.json")) -or !(Test-Path -LiteralPath (Join-Path $source "spritesheet.webp"))) {
        throw "Invalid pet package: $source"
    }
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Copy-Item -LiteralPath (Join-Path $source "pet.json") -Destination (Join-Path $target "pet.json") -Force
    Copy-Item -LiteralPath (Join-Path $source "spritesheet.webp") -Destination (Join-Path $target "spritesheet.webp") -Force
    Write-Host "Installed $petId -> $target"
}

Write-Host "Done. Restart Codex if the new pets do not appear immediately."

