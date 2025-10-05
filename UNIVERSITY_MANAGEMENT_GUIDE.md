# University Management System - Admin Guide

## Overview
The University Management System allows you to dynamically manage all content related to Galgotias University on your conference website, including:
- University information (text, statistics, contact details)
- Gallery images with categorization
- Social media links
- SEO metadata

## Features

### 1. University Information Management
**Location:** Django Admin → University Information

#### What You Can Manage:
- **Basic Info**: University name, tagline, establishment year
- **Content**: 
  - About text (appears on homepage)
  - Full description (appears on dedicated university page)
- **Statistics**: Student count, school count, program count, faculty count, campus area
- **Location**: Address, city, state, country, pincode
- **Contact**: Phone, email, website
- **Social Media**: Facebook, Twitter, LinkedIn, Instagram, YouTube
- **Features & Highlights**: Key features list, accreditations & rankings
- **SEO**: Meta description and keywords
- **Display Settings**: 
  - `is_active`: Only one record should be active
  - `show_on_homepage`: Display on homepage
  - `show_stats`: Show statistics cards

#### How to Use:
1. Go to Django Admin → University Information
2. Edit the existing record or create a new one
3. Fill in all relevant fields
4. Ensure `is_active` is checked for the record you want to display
5. Save changes

**Important Notes:**
- Only one record can be active at a time
- Key features should be entered one per line
- Accreditations should be entered one per line
- The system will automatically display the content on both homepage and dedicated university page

### 2. University Gallery Management
**Location:** Django Admin → University Gallery Images

#### Categories Available:
- Campus
- Facilities
- Laboratories
- Library
- Hostel
- Sports & Recreation
- Events
- Classrooms
- Auditorium
- Infrastructure
- Student Life
- Other

#### Fields:
- **Title**: Image title/caption
- **Description**: Detailed description of the image
- **Image**: Upload image file (will be automatically resized to max 1920x1080)
- **Category**: Select from available categories
- **Is Featured**: Check to show in homepage slider (max 5 recommended)
- **Is Active**: Must be checked for image to be visible
- **Display Order**: Lower numbers appear first
- **Photographer**: Optional credit
- **Photo Date**: When photo was taken

#### How to Add Images:
1. Go to Django Admin → University Gallery Images
2. Click "Add University Gallery Image"
3. Fill in all fields:
   - Title (required)
   - Description (optional but recommended)
   - Upload image
   - Select category
   - Check "Is Featured" if you want it on homepage
   - Set display order
4. Save

**Best Practices:**
- Use high-quality images (recommended: 1920x1080 or similar ratio)
- Write descriptive titles and descriptions
- Mark only 5 images as "featured" for optimal homepage performance
- Use appropriate categories for easy filtering
- Set display order to control appearance sequence

### 3. Homepage Integration

The "About Galgotias University" section on the homepage now:
- Displays dynamic content from University Information
- Shows statistics if enabled
- Displays featured gallery images in rotating slider
- Includes a "Learn More" button linking to dedicated university page

### 4. Dedicated University Page

**URL:** `/university/`

Features:
- Hero section with university name and details
- Statistics cards (students, schools, programs, faculty)
- Full description section
- Key features list
- Accreditations & rankings
- Full gallery with category filters
- Contact information with map
- Social media links
- Lightbox for viewing images

#### Gallery Features on University Page:
- Filter by category
- Lightbox view with navigation
- Keyboard navigation (arrows, ESC)
- Touch/swipe support
- Category badges on images

## Workflow for Updating Content

### Initial Setup:
1. **Create University Info Record:**
   - Go to University Information
   - Click "Add"
   - Fill in all basic information
   - Set statistics
   - Add key features (one per line)
   - Add accreditations (one per line)
   - Add contact details
   - Add social media links
   - Check "is_active", "show_on_homepage", and "show_stats"
   - Save

2. **Add Gallery Images:**
   - Go to University Gallery Images
   - Upload 5-10 featured images for homepage
   - Upload additional images for full gallery
   - Categorize appropriately
   - Set display order
   - Save each image

3. **Clear Cache:**
   - Cache will clear automatically on next pageview
   - Or restart the Django server

### Regular Updates:
1. To update text content → Edit University Information
2. To add new images → Add University Gallery Image
3. To reorder images → Edit display_order field
4. To feature/unfeature images → Toggle "is_featured"
5. To hide images temporarily → Uncheck "is_active"

## Technical Details

### Database Models:
- **UniversityInfo**: Stores all university information
- **UniversityGallery**: Stores gallery images with metadata

### Views:
- **home**: Displays featured content on homepage
- **university**: Dedicated university page with full gallery

### URL:
- Homepage: `/`
- University Page: `/university/`

### Caching:
- Homepage data is cached for 5 minutes
- Cache is automatically cleared when University Info is updated
- Cache key: `homepage_data_v2`

### Image Processing:
- Uploaded images are automatically resized to max 1920x1080
- Quality set to 85% for optimization
- Format preserved (JPEG, PNG, WebP supported)

## Tips & Best Practices

1. **Content Writing:**
   - Keep homepage "about_text" concise (150-200 words)
   - Make "full_description" comprehensive (400-600 words)
   - Use clear, professional language
   - Highlight unique selling points

2. **Images:**
   - Use consistent aspect ratio (16:9 recommended)
   - Ensure good lighting and composition
   - Avoid text-heavy images
   - Maximum 5 featured images for homepage
   - Aim for 20-30 total gallery images across all categories

3. **Statistics:**
   - Keep format consistent (e.g., "30K+", "200+")
   - Update annually or as needed
   - Use approximate numbers for large counts

4. **SEO:**
   - Write unique meta description (150-160 characters)
   - Include relevant keywords
   - Avoid keyword stuffing

5. **Social Media:**
   - Use full URLs for social media
   - Test links before saving
   - Keep profiles active and updated

## Troubleshooting

### Issue: Changes not appearing on website
**Solution:** Clear browser cache or use Ctrl+Shift+R (hard refresh)

### Issue: Images not showing
**Solution:** 
- Check "is_active" is checked
- Verify image was uploaded successfully
- Check file format is supported (JPG, PNG, WebP)

### Issue: Multiple active university records
**Solution:** The system automatically deactivates other records when you activate one. If issues persist, manually ensure only one record has "is_active" checked.

### Issue: Gallery filter not working
**Solution:** Clear browser cache and ensure JavaScript is enabled

## Support

For technical support or questions about the University Management System, contact the development team.

---

**Last Updated:** October 2025
**Version:** 1.0
