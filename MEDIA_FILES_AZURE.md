# Media Files on Azure - Troubleshooting Guide

## Problem
Media files (logos, images uploaded through Django admin) are not showing on Azure deployment but work fine locally.

## Root Cause
Azure App Service doesn't persist files uploaded to the file system. When you upload files via Django admin, they're stored temporarily but may be lost on app restart or container rebuild.

## Solutions

### Solution 1: Use Azure Blob Storage (RECOMMENDED for Production)

Azure Blob Storage provides persistent, scalable storage for media files.

#### Steps:

1. **Install required package:**
   ```bash
   pip install django-storages[azure]
   ```

2. **Create Azure Storage Account:**
   - Go to Azure Portal → Storage Accounts → Create
   - Note down: Account Name and Account Key

3. **Update requirements.txt:**
   ```
   django-storages[azure]>=1.14
   ```

4. **Update settings.py:**
   ```python
   # Add to INSTALLED_APPS
   INSTALLED_APPS = [
       # ...
       'storages',
   ]

   # Configure Azure Blob Storage
   if not DEBUG:
       DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
       AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
       AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
       AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'media')
       AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
       MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'
   ```

5. **Set environment variables in Azure:**
   - AZURE_ACCOUNT_NAME = your_storage_account_name
   - AZURE_ACCOUNT_KEY = your_storage_account_key
   - AZURE_CONTAINER = media

6. **Migrate existing media files:**
   ```bash
   python manage.py collectstatic  # For static files
   # Manually upload media folder to Azure Blob Storage
   ```

### Solution 2: Use Middleware (Current Implementation)

We've implemented a middleware solution that serves media files directly from the Django application. This works but has performance limitations.

**Already Configured:**
- `AzureMediaMiddleware` in `conference/media_middleware.py`
- Added to MIDDLEWARE in settings.py
- Media files served at `/media/` URL

**Limitations:**
- Less efficient than dedicated storage
- Files may be lost on container restart
- Not ideal for high traffic

### Solution 3: Mount Azure File Share

Mount an Azure File Share to persist media files across deployments.

1. Create Azure File Share
2. Mount it to `/home/media` in Azure App Service
3. Update MEDIA_ROOT to point to mounted path

## Current Status

✅ **Implemented:**
- AzureMediaMiddleware for serving media files
- Media URL configuration
- Template tags for media handling
- Management command to check media files

⚠️ **To Do:**
- Configure Azure Blob Storage (recommended)
- OR Set up Azure File Share
- Migrate existing media files

## Debugging Commands

Check if media files exist:
```bash
python manage.py check_media
```

List media directory contents:
```bash
ls -la media/
```

Test media file access:
```bash
curl https://iceims.teamvimarsh.me/media/sponsors/logo.png
```

## Quick Fix for Immediate Issue

If logos are missing right now:

1. **Re-upload logos via Django admin** - they should work temporarily
2. **Check if media directory exists on Azure:**
   ```bash
   # SSH into Azure App Service
   cd /home/site/wwwroot
   ls -la media/
   ```

3. **Verify middleware is working:**
   - Check browser console for 404 errors
   - Test direct media URL access

## Best Practice Recommendation

For production deployment:
1. ✅ Use Azure Blob Storage for media files
2. ✅ Use WhiteNoise for static files (already configured)
3. ✅ Keep database (SQLite) on local filesystem or migrate to Azure SQL/PostgreSQL

## Contact

If issues persist, check:
- Azure App Service logs
- Django logs
- Browser console for 404 errors
- Verify media files exist in database and on filesystem
