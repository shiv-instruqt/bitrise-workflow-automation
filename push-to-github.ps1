# Pushes the Instruqt Labs 2.0 lab to a new public GitHub repo.
#
# Prerequisite: create the empty repo first at https://github.com/new
#   Owner: shiv-instruqt
#   Name:  bitrise-workflow-automation-lab-2.0
#   Visibility: Public
#   Do NOT tick "Add a README file", ".gitignore" or "license" — keep it empty.
#
# Then run this file from inside the lab-2.0 folder:
#   cd C:\Users\ShivTushalS\Downloads\bitrise-workflow-automation\lab-2.0
#   powershell -ExecutionPolicy Bypass -File .\push-to-github.ps1

$ErrorActionPreference = "Stop"

$Owner = "shiv-instruqt"
$Repo  = "bitrise-workflow-automation-lab-2.0"

if (-not (Test-Path ".\main.hcl")) {
    Write-Error "main.hcl not found. Run this from inside the lab-2.0 folder."
}

git init
git branch -M main
git add .
git commit -m "Instruqt Labs 2.0 port of the Bitrise mobile CI/CD track"
git remote add origin "https://github.com/$Owner/$Repo.git"
git push -u origin main

Write-Host ""
Write-Host "Done: https://github.com/$Owner/$Repo" -ForegroundColor Green
