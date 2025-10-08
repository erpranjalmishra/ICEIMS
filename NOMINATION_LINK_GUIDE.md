# Submit Nomination Button - Admin Guide

## Overview
You can now add custom links to the "Submit Nomination" buttons on the Awards page through the Django admin panel.

## How to Add Nomination Link

### Step 1: Access Admin Panel
1. Go to: `https://iceims.teamvimarsh.me/admin/` (Django Admin)
   OR `https://iceims.teamvimarsh.me/admin-panel/` (Custom Admin)
2. Log in with your admin credentials

### Step 2: Navigate to Awards
1. Click on **"Awards"** in the admin menu
2. Select the award you want to edit, or create a new one

### Step 3: Add Nomination Link
1. Scroll to the **"Nomination Settings"** section
2. Find the **"Nomination link"** field
3. Enter the URL where you want the Submit Nomination button to redirect
   
   **Examples:**
   - Google Form: `https://forms.google.com/your-form-id`
   - Microsoft Form: `https://forms.office.com/your-form-id`
   - External submission page: `https://your-submission-portal.com`
   - Email link: `mailto:submissions@conference.com`

4. Click **"Save"** or **"Save and continue editing"**

### Step 4: Verify
1. Go to the Awards page on your website
2. Find the award you edited
3. The "Submit Nomination" button should now link to your specified URL

## Features

### Automatic Display
The Submit Nomination button will automatically appear when:
- The award has a nomination link set
- The award status is "Open for Nominations"

### Where It Appears
The nomination button shows up in:
1. **Featured Awards Section** - Top of the awards page
2. **Open Nominations Section** - For all awards with open nominations
3. **Award Categories Section** - Within each category

## Field Details

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Nomination Link | URL | Optional | URL for Submit Nomination button |

### Help Text
"URL for Submit Nomination button (e.g., Google Form, external submission page)"

## Use Cases

### Google Forms
Perfect for collecting nomination submissions:
```
https://forms.google.com/forms/d/e/your-form-id/viewform
```

### External Portal
Link to your submission management system:
```
https://submissions.yourconference.com/awards/best-paper
```

### Email Submission
Open email client for direct submissions:
```
mailto:awards@yourconference.com?subject=Award Nomination
```

### Multi-step Process
Link to a landing page with detailed instructions:
```
https://yourconference.com/awards/nomination-process
```

## Tips

1. **Test the Link**: Always test your nomination link before making it public
2. **Keep it Updated**: Update or remove the link when nominations close
3. **Use HTTPS**: Always use secure HTTPS URLs for external links
4. **Short URLs**: Consider using URL shorteners for long links (e.g., bit.ly)
5. **Track Submissions**: Use Google Forms or similar tools to track and manage nominations

## Status-Based Display

The Submit Nomination button shows based on award status:

| Status | Button Displayed? |
|--------|-------------------|
| Upcoming | ❌ No |
| Open for Nominations | ✅ Yes (if link provided) |
| Nominations Closed | ❌ No |
| Winner Announced | ❌ No |

## Example Configuration

### Best Paper Award
- **Title**: Best Paper Award
- **Status**: Open for Nominations
- **Nomination Link**: `https://forms.google.com/best-paper-2026`
- **Nomination Start**: January 1, 2026
- **Nomination End**: October 15, 2026

**Result**: Visitors will see a "Submit Nomination" button that opens the Google Form

## Troubleshooting

### Button Not Showing?
Check:
- ✅ Award status is set to "Open for Nominations"
- ✅ Nomination link field is filled
- ✅ Award is active and published
- ✅ Award year matches current conference year

### Wrong Link?
- Edit the award in admin panel
- Update the Nomination Link field
- Save changes
- Refresh the awards page

### Link Opens Email Instead?
- Make sure you're using `https://` not `mailto:` unless you want email
- Check for typos in the URL

## Admin Panel Locations

### Django Admin
1. Login: `/admin/`
2. Navigate: **Conference → Awards**
3. Edit award
4. Find: **Nomination Settings** section
5. Field: **Nomination link**

### Custom Admin Panel
1. Login: `/admin-panel/`
2. Dashboard may have quick links to Awards management

## Migration Applied

A database migration has been created and applied:
- Migration: `0035_award_nomination_link.py`
- Field: `nomination_link` (URLField)
- Applied: ✅ Successfully

## Need Help?

If you encounter any issues:
1. Check Django admin logs
2. Verify the award status is correct
3. Test the URL in a new browser tab
4. Clear browser cache
5. Contact technical support

---

**Last Updated**: October 7, 2025
**Feature**: Submit Nomination Button Link Configuration
**Status**: ✅ Active and Working
