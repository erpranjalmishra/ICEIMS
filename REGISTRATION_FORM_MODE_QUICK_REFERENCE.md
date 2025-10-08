# Registration Form Mode - Quick Reference

## ✅ Implementation Summary

### Features Added
1. **Toggle Default Form** - Enable/disable the built-in Django registration form
2. **Google Form Integration** - Embed Google Forms via iframe
3. **Flexible Modes** - Use default form only, Google Form only, or both
4. **Custom Messages** - Add HTML messages above forms
5. **Adjustable Height** - Control Google Form iframe height

---

## 🎯 Three Operating Modes

### Mode 1: Default Form Only
```
✅ Show default form
❌ Use google form
```
**Result:** Traditional Django form with database storage

### Mode 2: Google Form Only
```
❌ Show default form
✅ Use google form
+ Google form URL
```
**Result:** Only Google Form iframe displayed

### Mode 3: Both Forms
```
✅ Show default form
✅ Use google form
+ Google form URL
```
**Result:** Google Form appears first, then default form

---

## 🚀 Quick Setup (Google Form Only)

### Step 1: Create Google Form
1. Go to [forms.google.com](https://forms.google.com)
2. Create your registration form
3. Click **Send** → **<>** (Embed)
4. Copy the URL from `src="..."`

### Step 2: Configure Admin
1. Go to `/admin/` → **Registration Settings**
2. Expand **Form Mode Settings**
3. Set:
   - ✅ **Use google form**: Checked
   - ❌ **Show default form**: Unchecked
   - **Google form URL**: Paste your URL
   - **Google form height**: 2000 (adjust as needed)
4. Click **Save**

### Step 3: Test
Visit `/registration/` to see your Google Form

---

## 📊 Database Changes

### New Fields in RegistrationSettings Model:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `use_google_form` | Boolean | False | Enable Google Form iframe |
| `show_default_form` | Boolean | True | Show built-in Django form |
| `google_form_url` | URL | Empty | Google Form embed URL |
| `google_form_height` | Integer | 2000 | Iframe height in pixels |
| `form_mode_message` | Text | Empty | HTML message above forms |

### Migration Applied:
- `0045_registrationsettings_form_mode_message_and_more.py` ✅

---

## 🎨 Admin Panel Location

**Path:** Django Admin → Conference → Registration Settings → **Form Mode Settings**

**Fieldset Description:**
> "Choose between default form and Google Form. You can show both, only one, or switch between them."

---

## 📝 Template Changes

### Updated File: `templates/registration.html`

**Added:**
1. Conditional rendering for `form_mode_message`
2. Google Form iframe section (if enabled)
3. Conditional wrapper for default form
4. Accessibility attributes (title, aria-label)

**Structure:**
```
{% if settings.form_mode_message %}
    <!-- Custom message -->
{% endif %}

{% if settings.use_google_form and settings.google_form_url %}
    <!-- Google Form iframe -->
{% endif %}

{% if settings.show_default_form %}
    <!-- Default Django form -->
{% endif %}
```

---

## 🔧 Common Configurations

### Configuration 1: Transition to Google Form
**Week 1-2:**
```
✅ Use google form: True
✅ Show default form: True
Form mode message: "We're offering two registration options. Choose your preferred method below."
```

**Week 3+:**
```
✅ Use google form: True
❌ Show default form: False
Form mode message: "Registration is now handled via Google Forms."
```

### Configuration 2: Backup Option
```
✅ Use google form: True
✅ Show default form: True
Form mode message: "<strong>Recommended:</strong> Use the Google Form below. If you experience issues, scroll down for the alternative form."
```

### Configuration 3: Default Only (No Changes)
```
❌ Use google form: False
✅ Show default form: True
Form mode message: (empty)
```

---

## 🎯 Google Form URL Format

### Correct Format:
```
https://docs.google.com/forms/d/e/1FAIpQLSc.../viewform?embedded=true
```

### Important:
- Must include `?embedded=true` parameter
- Get from embed code, not browser URL
- Test in admin preview if possible

---

## 📏 Height Recommendations

| Form Complexity | Height (pixels) |
|----------------|-----------------|
| Simple (5-10 fields) | 1200 - 1500 |
| Medium (10-20 fields) | 1500 - 2000 |
| Complex (20+ fields) | 2000 - 3000 |
| With file uploads | Add +500 |

**Tip:** Start with 2000, adjust based on visual appearance

---

## ⚠️ Important Notes

### Google Form Requirements:
- Form must be set to "Anyone can respond" or "Anyone with link"
- For file uploads, users must sign in with Google account
- Responses stored in Google Sheets, not Django database

### Default Form Benefits:
- Data stored in Django database
- CSV export from admin panel
- Automatic email confirmations (if configured)
- Full control over validation and processing

### Both Forms Considerations:
- Users might submit to both (check for duplicates)
- Two separate data sources to manage
- Good for transition periods

---

## 🧪 Testing Checklist

- [ ] Admin panel displays Form Mode Settings section
- [ ] Toggle `use_google_form` on/off works
- [ ] Toggle `show_default_form` on/off works
- [ ] Google Form iframe displays correctly
- [ ] Form height is appropriate (no cutoff)
- [ ] Custom message displays above forms
- [ ] Both forms work simultaneously (if enabled)
- [ ] Only Google Form shows when default disabled
- [ ] Only default form shows when Google Form disabled
- [ ] Mobile responsive (test on phone)

---

## 📂 Files Modified

### Models:
- `conference/models.py` - Added 5 new fields to RegistrationSettings

### Admin:
- `conference/admin.py` - Added Form Mode Settings fieldset

### Templates:
- `templates/registration.html` - Added conditional rendering and iframe

### Migrations:
- `conference/migrations/0045_registrationsettings_form_mode_message_and_more.py`

### Documentation:
- `REGISTRATION_FORM_MODE_GUIDE.md` - Comprehensive guide
- `REGISTRATION_DYNAMIC_CONTENT_SUMMARY.md` - Previous feature docs

---

## 🆘 Troubleshooting

### Google Form not showing?
1. Check `use_google_form` is enabled
2. Verify URL has `?embedded=true`
3. Clear browser cache
4. Check form permissions (public access)

### Form cut off at bottom?
1. Increase `google_form_height` by 500
2. Recommended: 2000-3000 for long forms

### Both forms showing when only want Google?
1. Uncheck `show_default_form`
2. Save and refresh page

### Want to go back to default only?
1. Uncheck `use_google_form`
2. Check `show_default_form`
3. Save

---

## 📞 Support

For detailed instructions, see: `REGISTRATION_FORM_MODE_GUIDE.md`

**Admin Path:** `/admin/conference/registrationsettings/1/change/`

**Frontend Path:** `/registration/`

---

## ✨ Next Steps

1. **Test Current Setup:** Visit `/registration/` with default settings
2. **Create Google Form:** Design your registration form in Google Forms
3. **Get Embed URL:** Copy the embed URL with `?embedded=true`
4. **Configure Admin:** Set up Form Mode Settings in admin panel
5. **Test Integration:** Verify Google Form displays correctly
6. **Adjust Height:** Fine-tune iframe height as needed
7. **Go Live:** Enable your preferred mode and start accepting registrations!

---

**Feature Status:** ✅ Fully Implemented and Ready to Use
