# Deploying to Render

## Quick Setup Steps

1. **Connect Your GitHub Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub account and select `climate-community-platform`

2. **Configure the Service**
   - **Name**: `climate-community-platform` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: `3.11.0` (or leave default)

3. **Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Add `SECRET_KEY` with a secure random value (you can generate one or let Render generate it)

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

## Manual Configuration (if not using render.yaml)

If you prefer manual setup instead of using `render.yaml`:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment**: `Python 3`

## Important Notes

- The app now binds to `0.0.0.0` and uses the `PORT` environment variable (set automatically by Render)
- Gunicorn is included in `requirements.txt` for production WSGI server
- Database will be created automatically on first run
- Make sure to set a secure `SECRET_KEY` in environment variables

## Troubleshooting

### Port Error
If you see "No open ports detected", make sure:
- Start command is: `gunicorn app:app`
- The app binds to `0.0.0.0` (already configured in app.py)

### Database Issues
- SQLite database is created in the app directory
- On Render, the database persists in the filesystem
- For production, consider upgrading to PostgreSQL (Render offers free PostgreSQL)

### Build Failures
- Check that `requirements.txt` includes all dependencies
- Verify Python version compatibility
- Check build logs in Render dashboard

## Updating Your App

After pushing changes to GitHub:
- Render automatically detects changes and redeploys
- Or manually trigger a deploy from the Render dashboard

## Free Tier Limitations

- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading for always-on service

