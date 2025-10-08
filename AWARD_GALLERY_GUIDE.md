# Award Gallery Images - Admin Guide

## Overview
The Award Gallery feature allows you to upload and manage custom images for the Awards page. These images can showcase award ceremonies, trophies, winners, events, and more.

## Features Added

### 1. **Award Gallery Model**
A new database model that stores:
- Image files
- Title and description
- Image type (ceremony, trophy, winner, event, banner, other)
- Year association
- Link to specific awards (optional)
- Display settings (active, show on hero, display order)

### 2. **Admin Panel Integration**

#### Standalone Gallery Management
Navigate to: **Admin Panel → Award Gallery Images**

Here you can:
- ✅ Upload new gallery images
- ✅ Edit existing images
- ✅ Set image type and description
- ✅ Control which images are active
- ✅ Mark images to show in hero/banner section
- ✅ Set display order
- ✅ Filter by image type, year, active status
- ✅ Search by title or description
- ✅ Preview images directly in the list view

#### Inline Gallery in Award Editor
When editing an Award, you can now:
- Add gallery images directly from the award edit page
- Images are automatically linked to that specific award
- Manage multiple images per award using the inline form

### 3. **Image Types**
Choose from 6 image types:
- **Award Ceremony**: Photos from award presentation events
- **Trophy/Medal**: Close-up shots of trophies, medals, certificates
- **Winner Photo**: Photos of award recipients
- **Event Photo**: General event/conference photos
- **Banner/Hero Image**: Large promotional banners
- **Other**: Any other type of image

### 4. **Display Settings**

#### Active Status
- **Is Active**: Toggle to show/hide image on website
- Only active images appear on the awards page

#### Show on Hero
- **Show on Hero**: Mark special images to appear in banner/hero sections
- Up to 3 hero images are displayed prominently

#### Display Order
- **Display Order**: Number to control sorting (lower numbers appear first)
- Images with same order are sorted by upload date (newest first)

## How to Use

### Adding Images

#### Method 1: Standalone Upload
1. Go to **Admin Panel → Award Gallery Images**
2. Click **Add Award Gallery Image**
3. Fill in the form:
   - **Title**: Give the image a descriptive title
   - **Image**: Upload the image file (JPG, PNG, WebP recommended)
   - **Image Type**: Select the appropriate category
   - **Description**: Add optional description/caption
   - **Award**: Optionally link to a specific award
   - **Year**: Set conference year (default: 2026)
   - **Is Active**: Check to show on website
   - **Show on Hero**: Check for prominent display
   - **Display Order**: Set sorting priority
4. Click **Save**

#### Method 2: From Award Editor
1. Go to **Admin Panel → Awards**
2. Click on an existing award or create new one
3. Scroll to **Award Gallery Images** inline section
4. Click **Add another Award Gallery Image**
5. Upload image and fill details
6. Save the award

### Managing Images

#### Bulk Edit
From the gallery list view, you can:
- Check multiple images
- Use "Is Active" and "Show on Hero" toggles for quick updates
- Change display order directly in the list

#### Filtering & Search
Use filters to find images:
- Filter by **Image Type**
- Filter by **Year**
- Filter by **Active Status**
- Search by **Title** or **Description**

### Best Practices

#### Image Requirements
- **Recommended Size**: 1200x800px or larger
- **Format**: JPG, PNG, or WebP
- **Aspect Ratio**: 3:2 or 4:3 for best display
- **File Size**: Keep under 2MB for faster loading

#### Naming Convention
Use descriptive titles:
- ✅ "Best Paper Award Ceremony 2025"
- ✅ "Golden Trophy - Innovation Award"
- ❌ "IMG_1234.jpg"

#### Organization Tips
1. **Use Image Types**: Properly categorize each image
2. **Set Display Order**: Organize images logically
3. **Add Descriptions**: Help visitors understand the context
4. **Link to Awards**: Connect images to specific awards when relevant
5. **Hero Images**: Select 2-3 best quality images for hero section

## Frontend Display

### Gallery Section
All active gallery images appear in a dedicated gallery section on the Awards page:
- Responsive grid layout (3 columns on desktop, 2 on tablet, 1 on mobile)
- Hover effect reveals title and description
- Image type badge displayed
- Smooth zoom animation on hover

### Hero Images
Images marked "Show on Hero" may appear:
- In banner/hero sections
- As featured highlights
- In promotional areas

### Mobile Responsive
The gallery is fully responsive:
- Adapts to all screen sizes
- Touch-friendly on mobile devices
- Optimized image loading

## Technical Details

### Database Fields
```python
- title: CharField (max 200 chars)
- image: ImageField (uploads to 'awards/gallery/')
- image_type: Choice field (ceremony/trophy/winner/event/banner/other)
- description: TextField (optional)
- award: ForeignKey to Award (optional)
- year: IntegerField (default 2026)
- display_order: IntegerField (default 0)
- is_active: BooleanField (default True)
- show_on_hero: BooleanField (default False)
- uploaded_at: DateTimeField (auto)
```

### Admin Permissions
Only users with appropriate admin permissions can:
- Add/edit/delete gallery images
- Upload files
- Change display settings

### File Storage
- Images are stored in: `media/awards/gallery/`
- Ensure media folder has proper write permissions
- Configure media URL in Django settings

## Troubleshooting

### Images Not Showing
1. Check **Is Active** is checked
2. Verify correct **Year** is set
3. Ensure image file uploaded successfully
4. Clear browser cache

### Upload Errors
1. Check file size (must be under Django's upload limit)
2. Verify image format (JPG, PNG, WebP supported)
3. Ensure media folder has write permissions
4. Check server disk space

### Display Issues
1. Verify **Display Order** for sorting
2. Check responsive layout on different devices
3. Clear Django cache if needed
4. Reload page without cache (Ctrl+Shift+R)

## Support

For technical issues:
1. Check Django admin logs
2. Review server error logs
3. Verify database migrations are applied
4. Contact system administrator

---

**Last Updated**: October 2025
**Version**: 1.0
**Migration**: 0039_awardgallery.py
