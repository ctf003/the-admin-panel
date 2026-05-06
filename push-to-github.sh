#!/bin/bash

# Push to GitHub Script
# Usage: ./push-to-github.sh <github-username> <repo-name>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <github-username> <repo-name>"
    echo "Example: $0 myusername ctf-admin-panel-challenge"
    exit 1
fi

USERNAME=$1
REPO=$2
REMOTE_URL="https://github.com/${USERNAME}/${REPO}.git"

echo "================================================"
echo "Pushing to GitHub"
echo "================================================"
echo "Repository: ${REMOTE_URL}"
echo ""

# Check if remote already exists
if git remote | grep -q "^origin$"; then
    echo "⚠️  Remote 'origin' already exists. Removing..."
    git remote remove origin
fi

# Add remote
echo "📡 Adding remote..."
git remote add origin "${REMOTE_URL}"

# Rename branch to main (if needed)
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Renaming branch to 'main'..."
    git branch -M main
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Successfully pushed to GitHub!"
    echo "================================================"
    echo "Repository URL: https://github.com/${USERNAME}/${REPO}"
    echo ""
    echo "Next steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Add topics: web, ctf, security, ssti, jinja2"
    echo "3. Set repository visibility (private recommended)"
    echo "4. Review the README.md"
    echo ""
else
    echo ""
    echo "================================================"
    echo "❌ Push failed!"
    echo "================================================"
    echo "Common issues:"
    echo "1. Repository doesn't exist - create it first at:"
    echo "   https://github.com/new"
    echo "2. Authentication failed - set up SSH keys or use:"
    echo "   git config --global credential.helper store"
    echo "3. Permission denied - check repository access"
    echo ""
    exit 1
fi
