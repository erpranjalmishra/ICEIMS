# Registration Form Mode - Admin Guide

## Overview
The registration system now supports three flexible modes:
1. **Default Form Only** - Use the built-in Django registration form
2. **Google Form Only** - Embed a Google Form via iframe
3. **Both Forms** - Display both the Google Form and default form on the same page

This gives you complete control over how users register for the conference.

---

## Features Added

### New Model Fields (RegistrationSettings)

**Form Mode Settings:**
- `use_google_form` (Boolean) - Enable Google Form iframe
- `show_default_form` (Boolean) - Show/hide the default Django form
- `google_form_url` (URL) - Google Form embed URL
- `google_form_height` (Integer) - Height of the iframe in pixels (default: 2000)
- `form_mode_message` (Text/HTML) - Message to display above forms

---

## Configuration Modes

### Mode 1: Default Form Only (Original Behavior)
**Settings:**
- `use_google_form` = ❌ False (unchecked)
- `show_default_form` = ✅ True (checked)

**Result:** Only the built-in registration form is displayed. All submissions are stored in your Django database.

**Best For:**
- Full control over registration data
- Custom validation and processing
- Automatic email confirmations
- CSV export from admin panel

---

### Mode 2: Google Form Only
**Settings:**
- `use_google_form` = ✅ True (checked)
- `show_default_form` = ❌ False (unchecked)
- `google_form_url` = Your Google Form embed URL

**Result:** Only the Google Form iframe is displayed. No default form shown.

**Best For:**
- Quick setup without custom development
- Using Google Sheets for data collection
- Leveraging Google Forms advanced features (file uploads, logic branching)
- Teams already using Google Workspace

---

### Mode 3: Both Forms (Hybrid Approach)
**Settings:**
- `use_google_form` = ✅ True (checked)
- `show_default_form` = ✅ True (checked)
- `google_form_url` = Your Google Form embed URL

**Result:** Both forms are displayed on the registration page. Google Form appears first, followed by the default form.

**Best For:**
- Transition period (moving from one system to another)
- Offering multiple registration options
- A/B testing different forms
- Backup registration method

---

## How to Set Up

### Step 1: Access Admin Panel
1. Navigate to Django Admin: `/admin/`
2. Go to **Conference** → **Registration Settings**
3. Scroll to **Form Mode Settings** section (click to expand if collapsed)

### Step 2: Create Your Google Form

#### Option A: Create New Google Form
1. Go to [Google Forms](https://forms.google.com/)
2. Click **+ Blank** or use a template
3. Add your registration fields:
   - Name
   - Email
   - Organization
   - Registration Category
   - Payment proof upload
   - etc.

#### Option B: Use Existing Form
Skip to Step 3 if you already have a Google Form

### Step 3: Get Google Form Embed URL

**Method 1: Using Send Button**
1. Open your Google Form
2. Click the **Send** button (top right)
3. Click the **<>** (Embed HTML) tab
4. Copy the URL from `src="..."` attribute
5. Example: `https://docs.google.com/forms/d/e/1FAIpQLSc.../viewform?embedded=true`

**Method 2: Using Preview**
1. Click the eye icon (Preview) in Google Forms
2. Copy the URL from browser address bar
3. Add `?embedded=true` at the end
4. Example: `https://docs.google.com/forms/d/e/1FAIpQLSc.../viewform?embedded=true`

### Step 4: Configure in Admin Panel

**For Google Form Only:**
```
✅ Use google form: Checked
❌ Show default form: Unchecked
Google form URL: https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?embedded=true
Google form height: 2000 (adjust based on your form length)
Form mode message: (Optional) "Please fill out the registration form below"
```

**For Both Forms:**
```
✅ Use google form: Checked
✅ Show default form: Checked
Google form URL: https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?embedded=true
Google form height: 2000
Form mode message: (Optional) "You can register using either form below"
```

**For Default Form Only:**
```
❌ Use google form: Unchecked
✅ Show default form: Checked
Google form URL: (leave empty)
```

### Step 5: Save and Test
1. Click **Save** in admin panel
2. Visit `/registration/` to see your changes
3. Test form submission
4. Adjust `google_form_height` if the iframe cuts off content

---

## Form Mode Message Examples

### Example 1: Simple Instruction
```html
Please complete the registration form below to secure your spot at ICEIMS 2026.
```

### Example 2: With HTML Formatting
```html
<p><strong>Note:</strong> Registration will close on <span style="color: red;">October 31, 2025</span>.</p>
<p>Early bird rates available until October 15, 2025.</p>
```

### Example 3: Multiple Options
```html
<div style="background: #e7f3ff; padding: 15px; border-radius: 5px; border-left: 4px solid #0066cc;">
    <h4 style="margin-top: 0;">Registration Options</h4>
    <p>You can register using either:</p>
    <ul>
        <li><strong>Google Form</strong> - Quick and simple (responses in Google Sheets)</li>
        <li><strong>Built-in Form</strong> - Integrated with our system (instant confirmation email)</li>
    </ul>
</div>
```

---

## Adjusting Google Form Height

The default height is **2000 pixels**. Adjust based on your form:

| Form Length | Recommended Height |
|-------------|-------------------|
| Short (5-10 fields) | 1200-1500 |
| Medium (10-20 fields) | 1500-2000 |
| Long (20+ fields) | 2000-3000 |
| With file uploads | +300-500 |

**How to Check:**
1. Preview your Google Form
2. Scroll to the bottom
3. If the form is cut off, increase the height by 500px
4. If there's too much white space, decrease by 200-300px

---

## Google Form Tips

### 1. Required Fields
Mark essential fields as required in Google Forms:
- Name
- Email
- Registration Category
- Payment Method

### 2. Validation
Use Google Forms validation for:
- Email format validation
- Phone number format
- Registration ID format

### 3. File Uploads
Enable file uploads for:
- Payment receipts
- Student ID documents
- IEEE membership certificates

**Note:** File uploads require respondents to be signed in to Google.

### 4. Confirmation Message
Customize the confirmation message in Google Forms:
1. Settings → Presentation
2. Edit "Confirmation message"
3. Example: "Thank you for registering! You will receive a confirmation email within 24 hours."

### 5. Collect Email Addresses
1. Settings → Responses
2. Enable "Collect email addresses"
3. This ensures you can contact registrants

---

## Data Management

### Google Form Responses
- Stored in Google Sheets
- Real-time updates
- Can export to Excel/CSV
- Access: Open form → Responses tab → View in Sheets

### Default Form Submissions
- Stored in Django database
- Accessible via Admin Panel
- Export to CSV from admin
- Path: Admin → Conference Registrations

### Using Both Forms
- Google Form data: Google Sheets
- Default form data: Django admin
- Keep both sources organized
- Consider migrating data periodically

---

## Troubleshooting

### Issue: Google Form Not Displaying
**Solution:**
1. Verify `use_google_form` is checked
2. Ensure URL ends with `?embedded=true`
3. Check URL is from the embed code, not just the form URL
4. Clear browser cache

### Issue: Form Cut Off at Bottom
**Solution:**
1. Increase `google_form_height` by 500px increments
2. Test on different screen sizes
3. Typical range: 1500-3000px

### Issue: Both Forms Showing When Only Google Form Wanted
**Solution:**
1. Uncheck `show_default_form`
2. Save settings
3. Clear cache and refresh page

### Issue: Neither Form Showing
**Solution:**
1. Check `registration_open` is True
2. Verify at least one of `use_google_form` or `show_default_form` is checked
3. Check template for errors

---

## Best Practices

### 1. Test Before Launch
- Submit test registrations
- Check data appears correctly
- Verify confirmation messages
- Test on mobile devices

### 2. Transition Strategy
If switching from default to Google Form:
1. Week 1: Show both forms (`use_google_form=True`, `show_default_form=True`)
2. Add message: "We're transitioning to Google Forms"
3. Week 2-3: Monitor which form gets more use
4. Week 4+: Disable less-used form

### 3. Backup Plan
Always keep `show_default_form` available as backup:
- Google Forms might have downtime
- Some users prefer traditional forms
- Gives you flexibility

### 4. Clear Communication
Use `form_mode_message` to:
- Explain why you're using Google Forms
- Provide contact info for issues
- Set expectations (e.g., "Response within 24 hours")

### 5. Mobile Optimization
- Google Forms are mobile-responsive
- Test iframe height on mobile
- Consider height: 2500-3000px for mobile users

---

## Migration from Default to Google Form

### Week 1: Preparation
1. Create Google Form with all required fields
2. Test form submissions
3. Set up Google Sheets for responses
4. Enable both forms on website

### Week 2: Announcement
1. Add `form_mode_message`: "New registration option available!"
2. Monitor both submission sources
3. Respond to feedback

### Week 3: Evaluation
1. Compare submission rates
2. Check data quality in both systems
3. Decide on primary method

### Week 4: Finalization
1. Disable less-used form
2. Update documentation
3. Archive old submissions

---

## Advanced Configuration

### Custom Styling
Add custom CSS in `form_mode_message`:
```html
<style>
.registration-notice {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
<div class="registration-notice">
    <h3>🎉 Registration Now Open!</h3>
    <p>Choose your preferred registration method below.</p>
</div>
```

### Multiple Google Forms
To offer different forms for different categories:
1. Create separate forms for Authors, Attendees, Students
2. Update `form_mode_message` with links:
```html
<div class="form-selector">
    <h4>Select Your Registration Type:</h4>
    <ul>
        <li><a href="#authors-form">Authors Registration</a></li>
        <li><a href="#attendees-form">Attendees Registration</a></li>
        <li><a href="#students-form">Students Registration</a></li>
    </ul>
</div>
```

### Conditional Display with JavaScript
Show different messages based on time:
```html
<script>
document.addEventListener('DOMContentLoaded', function() {
    const now = new Date();
    const earlyBirdEnd = new Date('2025-10-15');
    
    if (now < earlyBirdEnd) {
        document.getElementById('earlyBirdMessage').style.display = 'block';
    }
});
</script>
<div id="earlyBirdMessage" style="display: none;">
    <strong>⏰ Early Bird Rates Active!</strong>
</div>
```

---

## Summary

### Quick Setup Checklist
- [ ] Create Google Form (optional)
- [ ] Get embed URL with `?embedded=true`
- [ ] Go to Admin → Registration Settings
- [ ] Expand "Form Mode Settings"
- [ ] Check `use_google_form` (if using Google Form)
- [ ] Paste embed URL in `google_form_url`
- [ ] Set appropriate height (1500-3000)
- [ ] Toggle `show_default_form` as needed
- [ ] Add optional message in `form_mode_message`
- [ ] Save and test at `/registration/`

### Available Modes
1. **Default Form Only**: Traditional, database-stored registrations
2. **Google Form Only**: Quick setup, Google Sheets storage
3. **Both Forms**: Maximum flexibility, transition-friendly

Choose the mode that best fits your conference needs!
