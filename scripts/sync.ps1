# Daisy Maison OS - multi-computer sync
# One command to pull the latest from GitHub, then push whatever you changed
# on this machine. GitHub stays the single source of truth; this script never
# force-pushes and never overwrites local changes silently.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts\sync.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\sync.ps1 -Message "Update stock report"
#   powershell -ExecutionPolicy Bypass -File scripts\sync.ps1 -PullOnly

param(
    [string]$Message = "",
    [switch]$PullOnly
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Fail($msg) {
    Write-Host $msg -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".git")) {
    Fail "This folder is not the Daisy Maison OS git repository root. Run this from the repo you cloned from GitHub."
}

Write-Host "Pulling latest from GitHub..." -ForegroundColor Cyan
git pull --ff-only
if ($LASTEXITCODE -ne 0) {
    Fail "Pull failed or would not fast-forward (likely a conflict). Stopping - resolve manually before continuing."
}

if ($PullOnly) {
    Write-Host "Pull-only mode: done." -ForegroundColor Green
    exit 0
}

$status = git status --porcelain
if (-not $status) {
    Write-Host "Nothing to push - this machine is already in sync." -ForegroundColor Green
    exit 0
}

Write-Host "Local changes detected:" -ForegroundColor Yellow
git status --short

git add -A

if (-not $Message) {
    $Message = "Sync from $($env:COMPUTERNAME) on $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

git commit -m "$Message"
if ($LASTEXITCODE -ne 0) {
    Fail "Commit failed."
}

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push
if ($LASTEXITCODE -ne 0) {
    Fail "Push failed - most likely someone else pushed first. Run this script again to pull their changes, then retry."
}

Write-Host "Synced. All computers pulling next will see this update." -ForegroundColor Green
