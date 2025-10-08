# Azure Deployment - Static and Media Files Configuration

## Problem
Images and logos not showing on Azure deployment.

## Solution Steps

### 1. Run collectstatic before deployment
```bash
python manage.py collectstatic --noinput --clear
```

### 2. Verify static files are in repository
The `staticfiles/` folder should be committed to git with all collected static files.

### 3. Azure App Service Configuration

In Azure Portal > Your App Service > Configuration > Application Settings:

Add/Update these settings:
```
DJANGO_SETTINGS_MODULE = iccca_website.settings
WEBSITE_RUN_FROM_PACKAGE = 0
```

### 4. Azure App Service > Configuration > General Settings

Set the startup command:
```bash
bash startup.sh
```

### 5. Enable Application Logging

Azure Portal > Your App Service > App Service Logs:
- Application Logging (Filesystem): On
- Web Server Logging: On
- Detailed Error Messages: On

### 6. Verify Static Files in Deployment

SSH into Azure App Service and check:
```bash
cd /home/site/wwwroot
ls -la staticfiles/
ls -la static/images/
ls -la media/
```

### 7. Check Logs

Azure Portal > Your App Service > Log Stream
Look for errors related to static files.

### 8. URL Rewrite Rules

The web.config includes URL rewrite rules to serve static and media files directly from IIS:
- `/static/*` → serves from `staticfiles/`
- `/media/*` → serves from `media/`

### 9. Troubleshooting Commands

Run these commands locally before deployment:
```bash
# Check static files configuration
python manage.py check_static_media

# Collect static files
python manage.py collectstatic --noinput --clear

# Verify files exist
ls staticfiles/images/
ls static/images/
```

### 10. Common Issues

**Issue**: Logo not showing (iceims-logo.png)
**Fix**: Ensure the file exists in:
- `static/images/iceims-logo.png` (source)
- `staticfiles/images/iceims-logo.png` (collected)

**Issue**: CSS/JS not loading
**Fix**: 
- Clear browser cache (Ctrl+Shift+R)
- Run collectstatic again
- Check STATIC_URL in settings.py

**Issue**: Media files (uploaded images) not showing
**Fix**:
- Verify MEDIA_ROOT and MEDIA_URL in settings.py
- Check file permissions on Azure: `chmod -R 755 media/`
- Consider using Azure Blob Storage for production media files

### 11. Files to Commit

Make sure these are in your git repository:
```
.deployment
deploy.sh
startup.sh
web.config
staticfiles/ (after running collectstatic)
static/images/iceims-logo.png
requirements.txt
```

### 12. Azure Deployment Center

In Azure Portal > Your App Service > Deployment Center:
- Verify the correct branch is deployed
- Check deployment logs for errors
- Re-deploy if needed

## Quick Fix Checklist

✅ Run `python manage.py collectstatic --noinput --clear`
✅ Commit `staticfiles/` folder to git
✅ Push to repository
✅ Verify `startup.sh` runs collectstatic
✅ Check Azure logs for errors
✅ Clear browser cache
✅ Verify files exist on Azure using SSH/Kudu
