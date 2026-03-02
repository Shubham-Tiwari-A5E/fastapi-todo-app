# 🚀 Quick Git Commands

## Push to GitHub (First Time)

```bash
# 1. Create repository on GitHub first, then:
cd C:\Users\A5E\Python\FastAPI\Todos

# 2. Update your git config
git config user.name "Your Real Name"
git config user.email "your.email@example.com"

# 3. Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 4. Push to GitHub
git push -u origin main
```

## Daily Git Workflow

```bash
# Check what changed
git status

# Stage all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Useful Commands

```bash
# View commit history
git log --oneline

# See what's changed
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main

# Pull latest changes
git pull origin main
```

## Current Status

✅ Repository initialized
✅ 41 files committed  
✅ 2 commits made
✅ Ready to push

## Authentication

When pushing for first time, use:
- **Username**: Your GitHub username
- **Password**: Personal Access Token (NOT your password)

Get token: https://github.com/settings/tokens
