# Contact Page Customization - Quick Summary

## ✅ What's Been Added

The contact page is now fully customizable through the admin panel. You can now control:

### 1. **Venue Information** 
- Venue name
- Full address (3 lines)

### 2. **Contact Emails**
- General inquiries email
- Paper submissions email  
- Registration email

### 3. **Phone Numbers**
- Main office phone
- Conference desk phone

### 4. **Office Hours**
- Weekday hours
- Weekend hours
- Timezone

### 5. **Google Form Integration** ⭐ NEW
- Replace default contact form with Google Forms
- Support for any custom form (Typeform, JotForm, etc.)
- Adjustable iframe height
- Easy enable/disable toggle

### 6. **Google Maps**
- Custom map embed URL
- Shows venue location

---

## 🚀 How to Use Google Forms

### Quick Steps:

1. **Create a Google Form** at https://forms.google.com

2. **Get the Embed URL**:
   - Click **Send** → **< >** icon
   - Copy the URL from `src="..."`
   - Example: `https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?embedded=true`

3. **Configure in Admin**:
   - Go to **Admin Panel** → **Site Settings**
   - Scroll to **Contact Page - Form Settings**
   - ✓ Check **"Use custom iframe"**
   - Paste URL in **"Custom form URL"**
   - Set height (default: 800px)
   - Click **Save**

4. **Done!** Visit `/contact/` to see your Google Form

---

## 📍 Where to Find Settings

**Admin Panel** → **Website Control** → **Site Settings**

Sections:
- Contact Page - Venue Details
- Contact Page - Email Addresses
- Contact Page - Phone Numbers
- Contact Page - Office Hours
- Contact Page - Form Settings ⭐
- Contact Page - Map Settings

---

## 🎯 Common Use Cases

### Use Case 1: Update Email Addresses
Navigate to **Contact Page - Email Addresses** → Update fields → Save

### Use Case 2: Change Venue
Navigate to **Contact Page - Venue Details** → Update address → Save

### Use Case 3: Add Google Form
1. Create Google Form
2. Get embed URL
3. **Contact Page - Form Settings** → Check "Use custom iframe"
4. Paste URL → Save

### Use Case 4: Change Map Location
1. Get new Google Maps embed URL
2. **Contact Page - Map Settings** → Paste URL → Save

---

## ⚙️ Toggle Options

| Option | Effect |
|--------|--------|
| **Enable contact form** = ✓ | Shows contact form section |
| **Enable contact form** = ☐ | Hides contact form section |
| **Use custom iframe** = ✓ | Shows Google Form (if URL provided) |
| **Use custom iframe** = ☐ | Shows default built-in form |

---

## 📝 Example Google Form Setup

**Perfect for**:
- Conference inquiries
- Speaker submissions
- Sponsorship requests
- Registration questions
- General contact

**Benefits**:
- Automatic email notifications
- Response collection in Google Sheets
- Easy form customization
- No backend code needed
- Mobile-friendly

---

## 🔗 Default Values

All fields come with sensible defaults:
- Emails: `info@iceims.com`, `submissions@iceims.com`, `registration@iceims.com`
- Venue: Galgotias University, Greater Noida
- Phones: +91 120 458 9500, +91 120 458 9501
- Hours: Mon-Fri 9AM-6PM, Sat 10AM-4PM IST
- Map: Galgotias University location

---

## 💡 Pro Tips

1. **Test Google Form**: Make sure "Anyone can respond" is enabled in form settings
2. **Height Adjustment**: If form is cut off, increase **Custom form height** (try 1000-1200)
3. **Email Consistency**: Use the same email domain across all addresses
4. **Form Fields**: Keep Google Form concise (5-10 questions max)
5. **Mobile Testing**: Always test on mobile after changes

---

## 🆘 Troubleshooting

**Google Form not showing?**
- Check "Use custom iframe" is ✓ checked
- Verify URL contains `/viewform?embedded=true`
- Ensure form is public (not requiring sign-in)

**Form too small/large?**
- Adjust **Custom form height** value
- Standard range: 600-1200 pixels

**Emails not clickable?**
- They are! Click them on the live website
- Admin panel just shows text

---

## 📊 Migration Info

- **Migration**: `0037_sitesettings_conference_phone_and_more`
- **Model**: `conference.SiteSettings`
- **Template**: `templates/contact.html`
- **Status**: ✅ Applied and Ready

---

## 🎓 Full Documentation

For detailed instructions, see: `CONTACT_PAGE_ADMIN_GUIDE.md`

---

**All changes are live!** Visit `/contact/` to see the current configuration.
