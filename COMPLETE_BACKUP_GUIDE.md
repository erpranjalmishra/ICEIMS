# Complete Project Backup Guide

## Overview
The complete backup system allows superusers to download a full backup of the entire project as a ZIP file directly from the admin panel.

## What's Included in Complete Backup

### 1. **Source Code**
- All Python files (`.py`)
- HTML templates (`.html`)
- CSS stylesheets (`.css`)
- JavaScript files (`.js`)
- Configuration files (`settings.py`, `urls.py`, etc.)

### 2. **Database**
- Complete SQLite database (`db.sqlite3`)
- All tables, data, and relationships

### 3. **Media Files**
- All uploaded images
- User-uploaded documents
- Speaker photos
- Blog images
- Any other media content

### 4. **Static Files**
- Bootstrap CSS/JS
- Custom stylesheets
- Custom JavaScript
- Static images (logos, icons)
- Font files

### 5. **Configuration**
- Django settings
- URL configurations
- Requirements file
- Deployment scripts

## What's Excluded

To keep backup size reasonable and exclude unnecessary files:

- `__pycache__/` directories and `.pyc` files
- `.git/` repository data
- Virtual environments (`.venv/`, `venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Environment variables (`.env`)
- Log files (`.log`)
- Temporary files
- Node modules
- Build/dist directories

## How to Create Backup

### From Admin Panel

1. **Login as Superuser**
   - Only superusers can access backup features
   - Navigate to Admin Panel

2. **Find Backup Section**
   - Scroll to "Export Data" section
   - Look for backup cards

3. **Choose Backup Type**
   
   **Option 1: Complete Backup (Recommended)**
   - Click "Download Complete Backup" button
   - Includes: Code + Database + Media + Static files
   - File format: `full_backup_YYYYMMDD_HHMMSS.zip`
   - Larger file size but complete project
   
   **Option 2: Database Only**
   - Click "Download Database Only" button
   - Includes: Only SQLite database
   - File format: `db_backup_YYYYMMDD_HHMMSS.sqlite3`
   - Smaller, faster download

4. **Confirm Download**
   - Confirm the security warning
   - Download will begin automatically
   - May take 10-30 seconds for complete backup

## File Sizes

### Typical Backup Sizes
- **Database Only**: 5-50 MB (depending on content)
- **Complete Backup**: 50-500 MB (depending on media files)

### Factors Affecting Size
- Number of uploaded images in media/
- Number of blog posts with images
- Size of static assets
- Database record count

## Using Backups

### Restore Complete Backup

1. **Extract ZIP File**
   ```bash
   unzip full_backup_20250108_143022.zip -d /new/location/
   ```

2. **Install Dependencies**
   ```bash
   cd /new/location/
   pip install -r requirements.txt
   ```

3. **Run Migrations** (if needed)
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

5. **Start Server**
   ```bash
   python manage.py runserver
   ```

### Restore Database Only

1. **Replace Database File**
   ```bash
   # Backup current database first
   mv db.sqlite3 db.sqlite3.old
   
   # Copy new database
   cp db_backup_20250108_143022.sqlite3 db.sqlite3
   ```

2. **Restart Application**
   - Restart Django server
   - Changes take effect immediately

## Best Practices

### Backup Frequency
- **Complete Backup**: Weekly or before major changes
- **Database Backup**: Daily or after important data entry
- **Before Deployment**: Always backup before deploying to production

### Storage Recommendations
1. **Multiple Locations**
   - Local computer
   - Cloud storage (Google Drive, Dropbox)
   - External hard drive

2. **Version Control**
   - Keep last 5-10 backups
   - Delete older backups to save space
   - Name backups descriptively if needed

3. **Security**
   - Store in secure, private locations
   - Encrypt sensitive backups
   - Never commit backups to public repositories
   - Don't share backup files publicly

### Backup Schedule Example
```
Monday:    Database backup
Wednesday: Database backup
Friday:    Complete backup
Sunday:    Database backup
```

## Troubleshooting

### Backup Download Fails
**Problem**: Download doesn't start or fails midway

**Solutions**:
1. Check available disk space
2. Try database-only backup first (smaller)
3. Check browser download settings
4. Ensure superuser access
5. Check server logs for errors

### Backup File Too Large
**Problem**: Backup ZIP is very large

**Solutions**:
1. Use database-only backup for quick backups
2. Clean up old media files before backup
3. Remove unused static files
4. Consider splitting media into separate backup

### Cannot Extract Backup
**Problem**: ZIP file appears corrupted

**Solutions**:
1. Re-download the backup
2. Check available disk space during extraction
3. Use different extraction tool
4. Verify ZIP file integrity

### Restore Doesn't Work
**Problem**: Site doesn't work after restore

**Solutions**:
1. Ensure all dependencies installed (`pip install -r requirements.txt`)
2. Run migrations (`python manage.py migrate`)
3. Collect static files (`python manage.py collectstatic`)
4. Check file permissions
5. Verify database file location

## Security Warnings

### ⚠️ Important Security Notes

1. **Sensitive Data**
   - Backups contain ALL user data
   - Includes passwords (hashed), emails, personal info
   - Contains API keys in settings if present

2. **Access Control**
   - Only superusers can download backups
   - Keep admin credentials secure
   - Regularly review superuser accounts

3. **Storage Security**
   - Encrypt backup files if storing on cloud
   - Use strong passwords for cloud storage
   - Enable 2FA on storage accounts
   - Never share backups publicly

4. **Compliance**
   - Check GDPR/data protection requirements
   - Ensure backup storage complies with regulations
   - Document backup procedures
   - Have data retention policy

## Advanced Usage

### Automated Backups
For scheduled backups, create a cron job or scheduled task:

```bash
# Linux/Mac crontab example
# Daily database backup at 2 AM
0 2 * * * cd /path/to/project && python manage.py shell -c "from conference.views import download_database; ..."
```

### Custom Backup Scripts
Create custom management commands for specific backup needs:

```python
# conference/management/commands/backup.py
from django.core.management.base import BaseCommand
import zipfile
from datetime import datetime

class Command(BaseCommand):
    help = 'Create project backup'
    
    def handle(self, *args, **options):
        # Your backup logic here
        self.stdout.write('Backup created successfully')
```

## Support

### Getting Help
If you encounter issues with backups:

1. Check this documentation first
2. Review Django logs for errors
3. Verify file permissions
4. Test with smaller backup (database only)
5. Contact system administrator

### Feature Requests
To request backup features:
- Automated scheduled backups
- Remote backup storage (S3, Azure)
- Incremental backups
- Backup encryption
- Email backup notifications

## File Locations

### Backup Downloads
Backups are downloaded to your browser's default download folder:
- Windows: `C:\Users\YourName\Downloads\`
- Mac: `/Users/YourName/Downloads/`
- Linux: `/home/yourname/Downloads/`

### Project Paths
- Database: `db.sqlite3` (project root)
- Media: `media/` (project root)
- Static: `static/` and `staticfiles/` (project root)
- Templates: `templates/` (project root)
- Source: `conference/`, `iccca_website/` (project root)

## Version History

- **v1.0** (2025-01-08): Initial complete backup system
  - Full project ZIP backup
  - Database-only backup
  - Admin panel integration
  - Automatic exclusion of unnecessary files

---

**Last Updated**: January 8, 2025  
**Version**: 1.0  
**Access Level**: Superuser Only
