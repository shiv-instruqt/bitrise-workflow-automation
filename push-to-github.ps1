# Pushes the Instruqt Labs 2.0 lab to the public GitHub repo.
#
# PREREQUISITE: the repo must already exist and be empty:
#   https://github.com/shiv-instruqt/bitrise-workflow-automation
#
# Run from inside the lab-2.0 folder:
#   cd C:\Users\ShivTushalS\Downloads\bitrise-workflow-automation\lab-2.0
#   powershell -ExecutionPolicy Bypass -File .\push-to-github.ps1
#
# Safe to re-run: it skips steps that are already done.
#
# Two deliberate details:
#  1. This file is pure ASCII. Windows PowerShell 5.1 reads BOM-less files as
#     Windows-1252, which turns a UTF-8 em dash into a smart quote and breaks
#     string parsing.
#  2. Git arguments are passed as arrays. Passing them bare lets PowerShell
#     bind things like -A as a parameter of the function instead of git's.

$ErrorActionPreference = "Stop"

$Owner     = "shiv-instruqt"
$Repo      = "bitrise-workflow-automation"
$Branch    = "main"
$RemoteUrl = "https://github.com/$Owner/$Repo.git"

# PowerShell does NOT stop on a failing native command, so check $LASTEXITCODE by hand.
function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
}

if (-not (Test-Path ".\main.hcl")) {
    throw "main.hcl not found. Run this from inside the lab-2.0 folder."
}

if (-not (Test-Path ".\.git")) {
    Invoke-Git @('init')
}

Invoke-Git @('add', '-A')

& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    Invoke-Git @('commit', '-m', 'Instruqt Labs 2.0 port of the Bitrise mobile CI/CD track')
} else {
    Write-Host "Nothing new to commit; pushing the existing commit." -ForegroundColor Yellow
}

# Rename after the first commit exists, so the branch ref is real.
Invoke-Git @('branch', '-M', $Branch)

# Point origin at the right URL whether or not it already exists.
& git remote get-url origin *> $null
if ($LASTEXITCODE -eq 0) {
    Invoke-Git @('remote', 'set-url', 'origin', $RemoteUrl)
} else {
    Invoke-Git @('remote', 'add', 'origin', $RemoteUrl)
}

Write-Host "Pushing to $RemoteUrl ..." -ForegroundColor Cyan
& git push -u origin $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "PUSH FAILED with exit code $LASTEXITCODE." -ForegroundColor Red
    Write-Host "If it says 'Repository not found', check the repo exists at:" -ForegroundColor Red
    Write-Host "  https://github.com/$Owner/$Repo" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Pushed OK: https://github.com/$Owner/$Repo" -ForegroundColor Green
