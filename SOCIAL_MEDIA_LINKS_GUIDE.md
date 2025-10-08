# Social Media Links - Admin Guide

## 🎯 Overview

You can now customize all social media links displayed in the "Follow Us" section on the contact page through the admin panel.

---

## 📍 Where Social Links Appear

- **Contact Page**: "Follow Us" section (right sidebar)
- **Footer**: Social media icons (if configured)

---

## ⚙️ How to Configure

### Step 1: Access Admin Panel

1. Go to `/admin/` or `/admin-panel/`
2. Navigate to **Website Control** → **Site Settings**

### Step 2: Find Social Media Section

1. Scroll down to **"Social Media Links"** section
2. Click to expand if collapsed

### Step 3: Add Your URLs

Fill in the social media URLs for your conference:

| Field | Example URL |
|-------|-------------|
| **Facebook URL** | `https://facebook.com/iceims2026` |
| **Twitter URL** | `https://twitter.com/iceims2026` |
| **LinkedIn URL** | `https://linkedin.com/company/iceims` |
| **Instagram URL** | `https://instagram.com/iceims2026` |
| **YouTube URL** | `https://youtube.com/@iceims2026` |

### Step 4: Save

Click **Save** at the bottom of the page.

---

## 🔍 Important Notes

### URL Format

✅ **Correct Format**:
```
https://facebook.com/yourpage
https://twitter.com/yourhandle
https://linkedin.com/company/yourcompany
https://instagram.com/yourprofile
https://youtube.com/@yourchannel
```

❌ **Incorrect Format**:
```
facebook.com/yourpage (missing https://)
www.facebook.com/yourpage (use https:// instead)
```

### Auto-Hide Feature

- Only filled social media links will be displayed
- If you leave a field empty, that icon **won't show** on the page
- This allows you to show only the platforms you use

**Example**:
- If you only use LinkedIn and Twitter
- Leave Facebook, Instagram, and YouTube blank
- Only LinkedIn and Twitter icons will appear

---

## 📱 Platform-Specific Tips

### Facebook
```
https://facebook.com/YourPageName
```
- Use your page name or page ID
- Don't use personal profile links

### Twitter (X)
```
https://twitter.com/YourHandle
```
- Use your @handle (without the @)
- Example: `https://twitter.com/iceims2026`

### LinkedIn
```
https://linkedin.com/company/your-company-name
```
- Use company page, not personal profile
- Or use school page: `https://linkedin.com/school/university-name`

### Instagram
```
https://instagram.com/yourprofile
```
- Use your profile username
- Example: `https://instagram.com/iceims2026`

### YouTube
```
https://youtube.com/@yourchannel
```
- Use channel handle (with @)
- Or use: `https://youtube.com/channel/CHANNEL_ID`

---

## 🎨 How It Looks

When configured, the "Follow Us" section on the contact page will display:

```
Follow Us
[LinkedIn] [Twitter] [Facebook] [Instagram] [YouTube]
```

- Icons are clickable
- Opens in new tab
- Shows only platforms you've configured

---

## ✅ Best Practices

1. **Use Official URLs**: Link to your official conference pages
2. **Test Links**: Click each icon after saving to verify
3. **Keep Updated**: Update URLs if you change handles
4. **Consistency**: Use the same branding across all platforms
5. **Professional Pages**: Use conference/organization pages, not personal

---

## 🔧 Troubleshooting

### Links not showing?
- Make sure you've entered the full URL with `https://`
- Click **Save** after entering URLs
- Refresh the contact page (Ctrl+F5)

### Icons not clickable?
- Verify the URL format is correct
- Check for typos in the URL

### Wrong platform opening?
- Double-check you pasted the URL in the correct field
- Each field should match its platform name

---

## 📊 Quick Reference

| What You Want | Where to Go | What to Fill |
|---------------|-------------|--------------|
| Add Facebook link | Social Media Links → Facebook URL | Your FB page URL |
| Add Twitter link | Social Media Links → Twitter URL | Your Twitter profile |
| Add LinkedIn | Social Media Links → LinkedIn URL | Company/School page |
| Add Instagram | Social Media Links → Instagram URL | Your IG profile |
| Add YouTube | Social Media Links → YouTube URL | Your channel URL |
| Hide a platform | Leave that field blank | Empty = Won't show |

---

## 🎓 Example Configuration

```
Facebook URL: https://facebook.com/ICEIMS2026
Twitter URL: https://twitter.com/iceims_conf
LinkedIn URL: https://linkedin.com/company/iceims
Instagram URL: https://instagram.com/iceims2026
YouTube URL: https://youtube.com/@ICEIMS
```

Result: All 5 social icons will appear on the contact page

---

## 💡 Pro Tips

1. **Create Before Linking**: Create your social media pages before adding links
2. **Consistent Branding**: Use similar usernames across platforms
3. **Regular Updates**: Post conference updates on all platforms
4. **Engagement**: Monitor and respond to messages/comments
5. **Analytics**: Use platform analytics to track engagement

---

**Feature**: Dynamic Social Media Links
**Model**: `conference.SiteSettings`
**Template**: `templates/contact.html`
**Status**: ✅ Active
