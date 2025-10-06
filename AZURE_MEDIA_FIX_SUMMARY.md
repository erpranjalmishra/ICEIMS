# Azure Media Files Fix - Implementation Summary

## Problem
Database images (logos, photos uploaded via Django admin) are not displaying on Azure deployment but work locally.

## Root Cause
Azure App Service uses ephemeral file storage. When containers restart or are redeployed, uploaded media files are lost.

## Solutions Implemented

### 1. ✅ Media Serving Middleware
**File:** `conference/media_middleware.py`

- Custom middleware to serve media files directly from Django
- Handles `/media/` URL requests
- Adds proper caching headers
- Works as temporary solution until proper storage is configured

**Status:** ✅ Implemented and added to MIDDLEWARE

### 2. ✅ Updated Settings
**File:** `iccca_website/settings.py`

Changes made:
- Added Azure media configuration (commented out, ready to enable)
- Ensured MEDIA_ROOT and MEDIA_URL are properly set
- Added middleware to serve media files

### 3. ✅ Updated URL Configuration
**File:** `iccca_website/urls.py`

- Media files now served in both development and production
- Static files configuration maintained

### 4. ✅ Startup Script
**File:** `startup.sh`

Updated to:
- Create all required media directories on startup
- Set proper permissions
- Run media file check command

### 5. ✅ Template Tags for Media Handling
**File:** `conference/templatetags/media_tags.py`

New template filters:
- `media_url` - Ensures proper media URL formatting
- `has_media` - Check if media file exists
- `media_or_default` - Return media URL or fallback
- `debug_media` - Debug media file information

Usage in templates:
```django
{% load media_tags %}

{# Use media_url filter #}
<img src="{{ sponsor.logo|media_url }}" alt="{{ sponsor.name }}">

{# Check if media exists #}
{% if sponsor|has_media:'logo' %}
    <img src="{{ sponsor.logo.url }}" alt="{{ sponsor.name }}">
{% endif %}

{# Use with default fallback #}
{% media_or_default sponsor.logo '/static/images/default-logo.png' as logo_url %}
<img src="{{ logo_url }}" alt="{{ sponsor.name }}">
```

### 6. ✅ Management Command
**File:** `conference/management/commands/check_media.py`

Check media file status:
```bash
python manage.py check_media
```

Features:
- Scans all models with media files
- Reports missing files
- Lists media directory structure
- Can be run on Azure via SSH or startup script

### 7. ✅ Debug View
**File:** `conference/debug_views.py`
**URL:** `/admin-panel/debug/media/`

Features:
- Staff-only access
- Shows media configuration
- Lists all media files and their status
- Identifies missing files
- Available as HTML and JSON

Access: `https://iceims.teamvimarsh.me/admin-panel/debug/media/`

### 8. ✅ Documentation
**File:** `MEDIA_FILES_AZURE.md`

Comprehensive guide covering:
- Problem explanation
- Multiple solution approaches
- Azure Blob Storage setup (recommended)
- Debugging steps
- Best practices

## Updated Requirements
**File:** `requirements.txt`

Added:
```
python-dotenv>=1.0.0
```

Optional (for Azure Blob Storage):
```
django-storages[azure]>=1.14
```

## How to Use

### Immediate Fix (Temporary)
1. ✅ Already done - middleware is active
2. Re-upload logos via Django admin
3. They should now display (until container restart)

### Permanent Fix (Recommended)

#### Option A: Azure Blob Storage (Best for Production)

1. Install package:
```bash
pip install django-storages[azure]
```

2. Add to `requirements.txt`:
```
django-storages[azure]>=1.14
```

3. Create Azure Storage Account in Azure Portal

4. Update `settings.py` (uncomment the Azure Blob Storage section):
```python
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER = 'media'
```

5. Set Azure environment variables:
   - AZURE_ACCOUNT_NAME
   - AZURE_ACCOUNT_KEY
   - AZURE_CONTAINER

6. Upload existing media files to Azure Blob Storage

#### Option B: Azure File Share

1. Create Azure File Share
2. Mount to `/home/media` in Azure App Service
3. Update MEDIA_ROOT in settings

## Debugging

### Check if media files exist:
```bash
# SSH into Azure App Service
cd /home/site/wwwroot
ls -la media/
python manage.py check_media
```

### Check via web:
Visit: `https://iceims.teamvimarsh.me/admin-panel/debug/media/`

### Check browser console:
- Look for 404 errors on image URLs
- Verify image paths are correct

### Test direct access:
Try accessing a logo directly:
```
https://iceims.teamvimarsh.me/media/sponsors/some-logo.png
```

## Files Modified

1. ✅ `conference/media_middleware.py` - NEW
2. ✅ `conference/templatetags/media_tags.py` - NEW
3. ✅ `conference/management/commands/check_media.py` - NEW
4. ✅ `conference/debug_views.py` - NEW
5. ✅ `iccca_website/settings.py` - MODIFIED
6. ✅ `iccca_website/urls.py` - MODIFIED
7. ✅ `conference/urls.py` - MODIFIED
8. ✅ `startup.sh` - MODIFIED
9. ✅ `requirements.txt` - MODIFIED
10. ✅ `MEDIA_FILES_AZURE.md` - NEW

## Next Steps

1. **Immediate:** Deploy current changes
2. **Short-term:** Re-upload logos via admin
3. **Long-term:** Implement Azure Blob Storage

## Testing Checklist

After deployment:
- [ ] Access debug page: `/admin-panel/debug/media/`
- [ ] Check if middleware is serving files
- [ ] Upload a test logo via admin
- [ ] Verify logo displays on homepage
- [ ] Check browser console for 404 errors
- [ ] Run `python manage.py check_media` via SSH

## Support

If issues persist:
1. Check Azure App Service logs
2. Run debug command: `python manage.py check_media`
3. Visit debug page: `/admin-panel/debug/media/`
4. Check browser console for errors

## Recommendation

For production with multiple uploads and high traffic:
**Use Azure Blob Storage** - It's designed for this use case and provides:
- Persistent storage
- Better performance
- CDN integration
- Automatic backups
- Scalability
