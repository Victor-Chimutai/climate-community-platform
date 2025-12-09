# Deploying to GitHub

Your repository is ready to be pushed to GitHub! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `climate-community-platform`)
5. Choose public or private
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git push -u origin main
```

Or if you prefer SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

## Step 3: Verify

Visit your GitHub repository page to verify all files are uploaded correctly.

## Important Notes

- The `.gitignore` file is configured to exclude:
  - Database files (`*.db`, `*.sqlite`)
  - Python cache files (`__pycache__/`)
  - Virtual environments (`venv/`, `env/`)
  - Environment variables (`.env`)
  - Uploaded files in `static/uploads/`

- **Security**: Before deploying to production:
  - Change the `SECRET_KEY` in `app.py` (line 15)
  - Use environment variables for sensitive configuration
  - Never commit the database file with real user data

## Optional: GitHub Pages (Static Site)

This is a Flask application and requires a server to run. For static hosting, you would need to:
- Use a platform like Heroku, Railway, Render, or PythonAnywhere
- Or convert to a static site generator (not recommended for this dynamic app)

## Deployment Platforms

For deploying the Flask app:

1. **Render** (Recommended - Free tier available)
   - Connect your GitHub repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app.py`
   - Add environment variable: `SECRET_KEY=your-secret-key`

2. **Railway**
   - Connect GitHub repo
   - Auto-detects Flask apps
   - Add `SECRET_KEY` environment variable

3. **Heroku**
   - Requires `Procfile` and `runtime.txt`
   - More complex setup

4. **PythonAnywhere**
   - Good for beginners
   - Free tier available
   - Manual setup required

