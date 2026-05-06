# Deploy to GitHub

The repository has been initialized and committed locally. Follow these steps to push to GitHub:

## Option 1: Using GitHub Web Interface

1. Go to https://github.com/new
2. Create a new repository with these settings:
   - **Repository name**: `ctf-admin-panel-challenge` (or your preferred name)
   - **Description**: `CTF Web Challenge - Second-order SSTI with multiple red herrings`
   - **Visibility**: Private (recommended) or Public
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

3. After creating the repository, GitHub will show you commands. Use these:

```bash
cd web-challenge
git remote add origin https://github.com/YOUR_USERNAME/ctf-admin-panel-challenge.git
git branch -M main
git push -u origin main
```

## Option 2: Using GitHub CLI (if installed)

```bash
cd web-challenge
gh repo create ctf-admin-panel-challenge --private --source=. --remote=origin --push
```

## Option 3: Using Git Commands (if you already have a repo)

```bash
cd web-challenge
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Verify Deployment

After pushing, verify:
- All 26 files are present in the repository
- .gitignore is working (no .db, .pyc files)
- README.md displays correctly
- secret-backup.zip is included

## Security Notes

⚠️ **IMPORTANT**: This repository contains a CTF challenge with intentional vulnerabilities.

- Mark the repository as **Private** if you don't want solutions leaked
- Add a clear warning in the README that this is for educational purposes
- Do NOT deploy this to production systems
- The SOLUTION.md file contains the complete walkthrough - consider keeping it in a separate branch

## Repository Structure

```
ctf-admin-panel-challenge/
├── 📁 app/                    # Flask application
├── 📁 nginx/                  # Nginx configuration
├── 🐳 Dockerfile              # Container build
├── 🐳 docker-compose.yml      # Orchestration
├── 📝 README.md               # Overview
├── 📝 DEPLOY.md               # Deployment guide
├── 📝 SOLUTION.md             # Walkthrough (spoilers!)
├── 📝 CHALLENGE.md            # CTF description
└── 🧪 test_challenge.py       # Automated tests
```

## Next Steps

After pushing to GitHub:

1. **Add Topics/Tags**: web, ctf, security, ssti, jinja2, python, flask
2. **Create Releases**: Tag versions for different CTF events
3. **Branch Strategy**:
   - `main` - Production-ready challenge
   - `solution` - Include detailed solutions
   - `dev` - Development and testing
4. **GitHub Actions**: Consider adding CI/CD for automated testing
5. **Security Scanning**: Disable Dependabot alerts (intentional vulns)

## Collaboration

If working with a team:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ctf-admin-panel-challenge.git
cd ctf-admin-panel-challenge

# Create a feature branch
git checkout -b feature/new-red-herring

# Make changes and commit
git add .
git commit -m "Add new red herring"

# Push and create PR
git push origin feature/new-red-herring
```

## Troubleshooting

### Authentication Issues
If you get authentication errors:
```bash
# Use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/REPO.git
```

### Large Files
If secret-backup.zip is too large:
```bash
# Check file size
ls -lh app/static/secret-backup.zip

# If needed, use Git LFS
git lfs install
git lfs track "*.zip"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Branch Name
If you prefer `master` instead of `main`:
```bash
# Already on master, just push
git push -u origin master
```

---

**Current Status**: ✅ Repository initialized and committed locally
**Next Step**: Push to GitHub using one of the options above
