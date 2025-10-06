# Quick Fix Guide - Logo Not Showing on Azure

## 🚀 QUICK FIX (Do This Now)

### Step 1: Deploy the Changes
```bash
git add .
git commit -m "Fix media files serving on Azure"
git push origin main
```

### Step 2: Wait for Deployment
- Azure will automatically deploy
- Wait 2-3 minutes

### Step 3: Check Debug Page
Visit: https://iceims.teamvimarsh.me/admin-panel/debug/media/

This will show:
- ✅ If media middleware is working
- ✅ Which files are missing
- ✅ Media directory structure

### Step 4: Re-upload Logos
1. Go to Django Admin: https://iceims.teamvimarsh.me/admin/
2. Go to Sponsors section
3. For each sponsor with missing logo:
   - Edit the sponsor
   - Re-upload the logo
   - Save

## 🔍 TROUBLESHOOTING

### Logos Still Not Showing?

**Check 1: Is middleware working?**
```
Visit: /admin-panel/debug/media/
Look for: "Status: OK" or "Status: ISSUES FOUND"
```

**Check 2: Are files being uploaded?**
```
SSH into Azure App Service
cd /home/site/wwwroot/media/sponsors
ls -la
```

**Check 3: Check browser console**
```
Press F12 in browser
Look for 404 errors on logo URLs
```

## 📋 WHAT WAS FIXED

1. ✅ Added middleware to serve media files
2. ✅ Updated settings for Azure compatibility
3. ✅ Created debug tools
4. ✅ Updated startup script to create media directories
5. ✅ Added management command to check media files

## 🎯 WHY LOGOS WEREN'T SHOWING

**Problem:** Azure App Service doesn't persist uploaded files

**Solution:** We added middleware to serve files from Django application

**Long-term:** Use Azure Blob Storage (see MEDIA_FILES_AZURE.md)

## 🛠️ USEFUL COMMANDS

### Check media files status:
```bash
python manage.py check_media
```

### Create media directories:
```bash
mkdir -p media/sponsors media/committee media/attractions
```

### Test media URL:
```
https://iceims.teamvimarsh.me/media/sponsors/logo.png
```

## 📊 VERIFY IT'S WORKING

1. Upload a test logo via admin
2. Go to homepage
3. Check if logo displays
4. If not, check debug page
5. Look at browser console (F12)

## 🆘 STILL NOT WORKING?

### Option 1: Quick Fix
Re-upload all logos via Django admin

### Option 2: Use Static Images (Temporary)
Copy logos to `/static/images/logos/` folder
Update templates to use static path

### Option 3: Azure Blob Storage (Permanent)
See: MEDIA_FILES_AZURE.md for full guide

## 📞 DEBUG URLS

- **Main site:** https://iceims.teamvimarsh.me/
- **Django admin:** https://iceims.teamvimarsh.me/admin/
- **Custom admin:** https://iceims.teamvimarsh.me/admin-panel/
- **Media debug:** https://iceims.teamvimarsh.me/admin-panel/debug/media/

## ✨ EXPECTED RESULT

After deploying:
- ✅ Middleware serves media files
- ✅ Newly uploaded logos display correctly
- ✅ Debug page shows file status
- ✅ Browser console shows no 404 errors

## ⚠️ IMPORTANT NOTES

1. **Temporary Fix:** Current solution works but files may be lost on restart
2. **Permanent Fix:** Implement Azure Blob Storage (see documentation)
3. **Backup:** Keep local copies of all logos
4. **Re-upload:** May need to re-upload after Azure restarts

## 📚 MORE INFO

- Full documentation: MEDIA_FILES_AZURE.md
- Implementation details: AZURE_MEDIA_FIX_SUMMARY.md
