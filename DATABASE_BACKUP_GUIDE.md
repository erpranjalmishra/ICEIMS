# Database Backup Feature Guide

## Overview
The admin panel now includes a database backup download feature that allows superusers to download complete database backups directly from the web interface.

## Access Requirements
- **User Role**: Superuser only
- **Location**: Admin Panel > Export Data section (bottom of page)
- **URL**: `/admin-panel/download-database/`

## Features

### 1. One-Click Download
- Click the "Download Database Backup" button in the admin dashboard
- Confirmation dialog appears to prevent accidental downloads
- Database file is downloaded immediately

### 2. Timestamped Filenames
- Format: `db_backup_YYYYMMDD_HHMMSS.sqlite3`
- Example: `db_backup_20250108_143025.sqlite3`
- Helps maintain organized backup archives

### 3. Security
- Only accessible to superusers
- Requires authentication
- Confirmation dialog before download
- Contains sensitive data - store securely

## Usage Instructions

### For Superusers:
1. Log in to the admin panel at `/admin-panel/`
2. Scroll down to the **Export Data** section
3. Find the **Database Backup** card (red border)
4. Click **Download Database Backup** button
5. Confirm the download in the dialog
6. Save the `.sqlite3` file to a secure location

### Recommended Backup Schedule:
- **Daily**: For production environments
- **Before Deployments**: Always backup before major changes
- **After Bulk Operations**: After importing/updating large amounts of data
- **Weekly**: Minimum for development environments

## File Information

### What's Included:
- All conference data (speakers, committee, tracks, etc.)
- User accounts and profiles
- Blog posts and comments
- Settings and configurations
- Activity logs and analytics
- Email templates and logs
- All other database tables

### File Size:
- Varies based on data volume
- Typically 5-50 MB for moderate-sized conferences
- May be larger with extensive media metadata

## Restoration Process

### To Restore from Backup:
1. Stop the Django application
2. Backup current `db.sqlite3` (if needed)
3. Replace `db.sqlite3` with backup file
4. Rename backup file to `db.sqlite3`
5. Restart the application
6. Verify data integrity

### Example Commands (PowerShell):
```powershell
# Stop application (if running with manage.py)
# Ctrl+C to stop the server

# Backup current database
Copy-Item db.sqlite3 db_old.sqlite3

# Restore from backup
Copy-Item db_backup_20250108_143025.sqlite3 db.sqlite3

# Restart application
python manage.py runserver
```

## Best Practices

### Storage:
- ✅ Store backups in multiple locations
- ✅ Use encrypted storage for sensitive data
- ✅ Keep backups off the production server
- ✅ Use cloud storage with versioning (Google Drive, Dropbox, Azure Blob)
- ❌ Don't store backups in the same directory as the live database
- ❌ Don't commit database files to version control

### Retention:
- **Daily backups**: Keep for 7 days
- **Weekly backups**: Keep for 1 month
- **Monthly backups**: Keep for 1 year
- **Pre-deployment backups**: Keep indefinitely

### Testing:
- Periodically test restoration process
- Verify backup integrity
- Document restoration procedures
- Train team members on backup/restore process

## Troubleshooting

### Issue: "Database file not found" error
**Solution**: 
- Verify database path in `settings.py`
- Check file permissions
- Ensure Django has read access to database file

### Issue: Download interrupted or corrupted
**Solution**:
- Check available disk space
- Verify file integrity after download
- Try download again with stable connection

### Issue: File too large for download
**Solution**:
- Use FTP/SFTP instead for very large databases
- Compress database before download
- Consider server-side backup solutions

### Issue: Permission denied
**Solution**:
- Verify you're logged in as superuser
- Check `is_superuser` flag in user account
- Contact system administrator

## Security Considerations

### Important Notes:
⚠️ **Database backups contain ALL sensitive data including:**
- User passwords (hashed)
- Email addresses
- Personal information
- API keys and secrets (if stored in database)
- Activity logs and analytics

### Security Recommendations:
1. **Encrypt backups** before storing
2. **Limit access** to backup files
3. **Use secure transfer methods** (HTTPS, SFTP)
4. **Audit backup downloads** via activity logs
5. **Delete old backups** securely (don't just move to trash)

## Technical Implementation

### View Function:
- Location: `conference/views.py` - `download_database()`
- Decorator: `@login_required`, `@user_passes_test(lambda u: u.is_superuser)`
- Returns: `FileResponse` with SQLite file

### URL Pattern:
- Pattern: `admin-panel/download-database/`
- Name: `conference:download_database`

### Template:
- File: `templates/admin/dashboard.html`
- Section: Export Data > Database Backup card
- Visibility: Superuser only (`{% if user.is_superuser %}`)

## Migration to Other Databases

If migrating from SQLite to PostgreSQL/MySQL:
1. Export data using Django's `dumpdata` command
2. Configure new database in `settings.py`
3. Run migrations on new database
4. Import data using `loaddata` command

```bash
# Export data
python manage.py dumpdata --natural-foreign --natural-primary > datadump.json

# After configuring new database
python manage.py migrate
python manage.py loaddata datadump.json
```

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Review activity logs in admin panel
- Contact system administrator
- Check `AZURE_STATIC_FILES_FIX.md` for deployment issues

---

**Last Updated**: January 2025
**Version**: 1.0
**Django Version**: 5.2.6
