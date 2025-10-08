# Contact Page Customization - Admin Guide

This guide explains how to customize the contact page details and integrate Google Forms through the admin panel.

## 📋 Table of Contents
1. [Accessing Contact Page Settings](#accessing-contact-page-settings)
2. [Venue Information](#venue-information)
3. [Email Addresses](#email-addresses)
4. [Phone Numbers](#phone-numbers)
5. [Office Hours](#office-hours)
6. [Google Form Integration](#google-form-integration)
7. [Google Maps Integration](#google-maps-integration)
8. [Tips & Best Practices](#tips--best-practices)

---

## Accessing Contact Page Settings

1. Log in to the admin panel: `/admin/` or `/admin-panel/`
2. Navigate to **Website Control** → **Site Settings**
3. Scroll down to find the Contact Page sections

---

## Venue Information

Configure your conference venue details:

### Fields:
- **Venue Name**: Conference venue name (e.g., "Galgotias University")
- **Address Line 1**: First line of address (e.g., "Plot No. 2, Yamuna Expressway")
- **Address Line 2**: Second line (e.g., "Sector 17A, Greater Noida")
- **Address Line 3**: City, State, Country (e.g., "Uttar Pradesh 203201, India")

### Example:
```
Venue Name: Galgotias University
Address Line 1: Plot No. 2, Yamuna Expressway
Address Line 2: Sector 17A, Greater Noida
Address Line 3: Uttar Pradesh 203201, India
```

---

## Email Addresses

Set up different email addresses for various purposes:

### Fields:
- **General Email**: For general inquiries (e.g., `info@iceims.com`)
- **Submissions Email**: For paper submissions (e.g., `submissions@iceims.com`)
- **Registration Email**: For registration queries (e.g., `registration@iceims.com`)

### Best Practices:
- Use professional domain-based emails (avoid Gmail/Yahoo)
- Create role-based emails (info@, submissions@) rather than personal ones
- Ensure all emails are monitored regularly

---

## Phone Numbers

Configure contact phone numbers:

### Fields:
- **Main Phone**: Primary office contact number
- **Conference Phone**: Dedicated conference desk number

### Format Examples:
```
+91 120 458 9500 (India)
+1 (555) 123-4567 (USA)
+44 20 1234 5678 (UK)
```

---

## Office Hours

Customize your office availability:

### Fields:
- **Weekday Hours**: Monday-Friday hours (e.g., "Monday - Friday: 9:00 AM - 6:00 PM")
- **Weekend Hours**: Saturday/Sunday hours (e.g., "Saturday: 10:00 AM - 4:00 PM")
- **Timezone**: Time zone information (e.g., "Indian Standard Time (IST)")

### Examples:
```
Weekday: Monday - Friday: 9:00 AM - 6:00 PM
Weekend: Saturday: 10:00 AM - 4:00 PM
Timezone: Indian Standard Time (IST)
```

---

## Google Form Integration

Replace the default contact form with a Google Form or any custom iframe.

### Step-by-Step Guide:

#### Option 1: Using Google Forms (Recommended)

1. **Create Your Google Form**:
   - Go to [Google Forms](https://forms.google.com)
   - Create a new form with your desired fields
   - Design it according to your needs

2. **Get the Embed URL**:
   - Click the **Send** button (top-right)
   - Click the **< >** (Embed HTML) icon
   - Copy the URL from the `src` attribute
   
   Example:
   ```html
   <iframe src="https://docs.google.com/forms/d/e/FORM_ID/viewform?embedded=true" ...>
   ```
   
   Copy this part: `https://docs.google.com/forms/d/e/FORM_ID/viewform?embedded=true`

3. **Configure in Admin Panel**:
   - Navigate to **Site Settings** → **Contact Page - Form Settings**
   - Check ☑ **Enable contact form**
   - Check ☑ **Use custom iframe**
   - Paste the URL in **Custom form URL**
   - Set **Custom form height** (default: 800 pixels, adjust as needed)
   - Click **Save**

#### Option 2: Using Other Forms (Typeform, JotForm, etc.)

Same process as Google Forms:
1. Create your form on the platform
2. Get the embed URL
3. Paste it in the **Custom form URL** field
4. Adjust the height as needed

### Settings Explanation:

| Setting | Description | Default |
|---------|-------------|---------|
| **Enable contact form** | Show/hide the contact form section | ✓ Checked |
| **Use custom iframe** | Use Google Form instead of default form | ☐ Unchecked |
| **Custom form URL** | The embed URL from Google Forms | Empty |
| **Custom form height** | Height of the iframe in pixels | 800px |

### Testing Your Form:

1. Save the settings in admin
2. Visit your contact page: `/contact/`
3. Verify the form loads correctly
4. Submit a test entry to ensure it's working

### Troubleshooting:

**Form not showing?**
- Ensure **Enable contact form** is checked
- Ensure **Use custom iframe** is checked
- Verify the URL is the embed URL (contains `/viewform?embedded=true`)
- Check that the form is set to "Anyone can respond" in Google Forms settings

**Form too tall/short?**
- Adjust the **Custom form height** value
- Typical values: 600-1200 pixels
- Test on mobile devices too

**Form showing "Sign in required"?**
- In Google Forms, go to Settings
- Under "Responses", uncheck "Limit to 1 response"
- Make sure "Requires sign in" is NOT checked

---

## Google Maps Integration

Update the location map on your contact page.

### Getting the Embed URL:

1. Go to [Google Maps](https://maps.google.com)
2. Search for your venue
3. Click **Share** button
4. Click **Embed a map** tab
5. Copy the URL from the iframe code

Example iframe code from Google Maps:
```html
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12..." width="600" height="450" ...></iframe>
```

Copy the `src` URL: `https://www.google.com/maps/embed?pb=!1m18!1m12...`

### Updating in Admin:

1. Navigate to **Site Settings** → **Contact Page - Map Settings**
2. Paste the embed URL in **Google maps embed url**
3. Click **Save**

---

## Tips & Best Practices

### 🎯 Contact Information
- Keep all information up-to-date
- Test all phone numbers and email addresses
- Use consistent formatting throughout

### 📧 Email Management
- Set up email forwarding if needed
- Monitor all listed email addresses regularly
- Consider using a ticketing system for inquiries

### 📝 Google Forms
- Keep forms concise (5-10 fields maximum)
- Make only essential fields required
- Enable email notifications for form submissions
- Regularly check and respond to submissions

### 🗺️ Maps
- Ensure the pin is at the exact venue location
- Test the map on mobile devices
- Consider adding a "Get Directions" button

### 📱 Mobile Optimization
- Test all changes on mobile devices
- Keep form height reasonable for mobile screens
- Verify phone numbers are clickable on mobile

### 🔒 Privacy & Security
- Add privacy policy links in forms
- Use HTTPS for all external links
- Don't expose personal contact information

---

## Quick Reference

### To Switch from Default Form to Google Form:
1. Create Google Form → Get embed URL
2. Admin Panel → Site Settings
3. Check "Use custom iframe"
4. Paste URL → Save

### To Switch Back to Default Form:
1. Admin Panel → Site Settings
2. Uncheck "Use custom iframe"
3. Save

### To Hide Contact Form Completely:
1. Admin Panel → Site Settings
2. Uncheck "Enable contact form"
3. Save

---

## Support

For technical issues or questions:
- Check the main documentation
- Contact the development team
- Review Django admin logs

---

**Last Updated**: Migration 0037
**Feature**: Contact Page Customization
**Django App**: conference.SiteSettings
