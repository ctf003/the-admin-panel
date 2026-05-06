# Push to GitHub Script (PowerShell)
# Usage: .\push-to-github.ps1 -Username "myusername" -RepoName "ctf-admin-panel-challenge"

param(
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$true)]
    [string]$RepoName
)

$RemoteUrl = "https://github.com/$Username/$RepoName.git"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Pushing to GitHub" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Repository: $RemoteUrl" -ForegroundColor White
Write-Host ""

# Check if remote already exists
$remotes = git remote
if ($remotes -contains "origin") {
    Write-Host "⚠️  Remote 'origin' already exists. Removing..." -ForegroundColor Yellow
    git remote remove origin
}

# Add remote
Write-Host "📡 Adding remote..." -ForegroundColor Green
git remote add origin $RemoteUrl

# Rename branch to main (if needed)
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "🔄 Renaming branch to 'main'..." -ForegroundColor Green
    git branch -M main
}

# Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Repository URL: https://github.com/$Username/$RepoName" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Visit your repository on GitHub"
    Write-Host "2. Add topics: web, ctf, security, ssti, jinja2"
    Write-Host "3. Set repository visibility (private recommended)"
    Write-Host "4. Review the README.md"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist - create it first at:"
    Write-Host "   https://github.com/new"
    Write-Host "2. Authentication failed - you may need to:"
    Write-Host "   - Use a personal access token"
    Write-Host "   - Set up SSH keys"
    Write-Host "   - Run: git config --global credential.helper wincred"
    Write-Host "3. Permission denied - check repository access"
    Write-Host ""
    exit 1
}
