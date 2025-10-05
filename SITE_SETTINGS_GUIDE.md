# Site Settings & Hero Slider Management - Admin Panel

## ✅ New Features Added

### 1. **Site Settings** - Manage Logos & Branding
Control all site-wide settings from one place in the admin panel.

**Features:**
- **Main Logo**: Header/navigation logo
- **Footer Logo**: Different logo for footer (optional)
- **Favicon**: Browser tab icon
- **Site Name & Tagline**: Customizable site title
- **Contact Information**: Email, phone, address
- **Social Media Links**: Facebook, Twitter, LinkedIn, Instagram, YouTube
- **Theme Colors**: Primary and secondary color customization

**Access:** Admin → Site Settings

### 2. **Hero Slides** - Dynamic Homepage Slider
Create beautiful hero sliders with images or videos.

**Slide Types:**

#### Image Slides
- Upload background images (1920x1080px recommended)
- Add title and subtitle overlay
- Customize text position (left/center/right)
- Optional dark overlay for better text readability

#### Video Slides
- **Option 1**: Upload video file (MP4, WebM)
- **Option 2**: Use YouTube/Vimeo embed URL
- Add video thumbnail/poster image
- Auto-play or user-controlled

**Additional Features:**
- Call-to-Action buttons (customizable text, URL, style)
- Display order control
- Active/inactive toggle
- Text color customization
- Multiple positioning options

**Access:** Admin → Hero Slides

### 3. **Slider Settings** - Control Slider Behavior
Fine-tune how the hero slider works.

**Autoplay Controls:**
- ✅ Enable/disable autoplay
- ⏱️ Autoplay speed (milliseconds between slides)
- 🎬 Transition speed (animation duration)
- 🎨 Transition effects: Fade, Slide, Zoom, Slide+Fade

**Navigation:**
- Show/hide previous/next arrows
- Show/hide navigation dots
- Pause on hover option

**Mobile Settings:**
- Separate autoplay control for mobile
- Hide/show arrows on mobile devices
- Custom slider heights for desktop and mobile

**Performance:**
- Lazy loading for better speed
- Preload slides configuration (1-5 slides)

**Access:** Admin → Slider Settings

## 📋 How to Use

### Setting Up Site Logos

1. Go to **Admin Panel** → **Site Settings**
2. Upload your images:
   - **Main Logo**: 200x60px (PNG with transparent background recommended)
   - **Footer Logo**: Same as main or different design
   - **Favicon**: 32x32px or 16x16px ICO/PNG file
3. Click **Save**
4. Logos appear immediately across the entire site

### Creating Hero Slides

1. Go to **Admin Panel** → **Hero Slides** → **Add Hero Slide**

2. **For Image Slide:**
   - Enter title and subtitle
   - Select slide_type: **Image Slide**
   - Upload background image (1920x1080px recommended)
   - Set text position (left/center/right)
   - Optionally add CTA button
   - Set display order (lower numbers appear first)
   - Check "Is active"
   - Click **Save**

3. **For Video Slide:**
   - Enter title and subtitle
   - Select slide_type: **Video Slide**
   - **Either:**
     - Upload video file (MP4/WebM, max 50MB recommended)
     - **OR** paste YouTube URL (e.g., https://www.youtube.com/watch?v=xxxxx)
   - Upload video thumbnail (shown while loading)
   - Configure text overlay and CTA
   - Click **Save**

4. **Create multiple slides** - Slider will cycle through all active slides

### Configuring Slider Behavior

1. Go to **Admin Panel** → **Slider Settings**

2. **Autoplay Settings:**
   - Check "Autoplay" to auto-advance slides
   - Set "Autoplay speed": 5000 = 5 seconds per slide
   - Set "Transition speed": 1000 = 1 second transition
   - Choose transition effect (Fade recommended for smooth look)

3. **Navigation:**
   - Check "Show arrows" for prev/next buttons
   - Check "Show dots" for navigation indicators
   - Check "Pause on hover" to pause when mouse hovers

4. **Mobile:**
   - Separate settings for mobile devices
   - Mobile users typically prefer no arrows (saves space)

5. **Dimensions:**
   - Desktop height: 700px (default, full hero section)
   - Mobile height: 500px (default, optimized for phones)

6. Click **Save**

## 🎨 Customization Examples

### Example 1: Conference Promotional Slider

**Slide 1 - Welcome**
- Type: Image
- Image: Conference venue photo
- Title: "Welcome to ICCCA 2026"
- Subtitle: "International Conference on Computing and Applications"
- CTA: "Register Now" → /registration/
- Position: Center

**Slide 2 - Call for Papers**
- Type: Image  
- Image: Research/academic themed
- Title: "Call for Papers Open"
- Subtitle: "Submit your research by December 31, 2025"
- CTA: "Submit Paper" → /submission/
- Position: Left

**Slide 3 - Video Highlight**
- Type: Video
- Video URL: Previous conference highlights from YouTube
- Title: "Experience ICCCA"
- Subtitle: "See highlights from ICCCA 2024"
- CTA: "Watch More" → /gallery/
- Position: Center

**Slider Settings:**
- Autoplay: ✅ Yes
- Speed: 6000ms (6 seconds per slide)
- Transition: Fade
- Arrows: ✅ Show
- Dots: ✅ Show

### Example 2: Fast-Paced Marketing Slider

**Multiple product/feature slides**
- Autoplay: ✅ Yes
- Speed: 3000ms (3 seconds - fast)
- Transition: Slide + Fade
- Arrows: ❌ Hide (let it auto-play)
- Dots: ✅ Show
- Pause on hover: ✅ Yes

### Example 3: Manual Control Slider

**Detailed information slides**
- Autoplay: ❌ No
- Arrows: ✅ Show (users navigate manually)
- Dots: ✅ Show
- Transition: Slide

## 📁 File Upload Guidelines

### Images
- **Format**: JPG, PNG, WebP
- **Hero Slides**: 1920x1080px (Full HD)
- **Logos**: PNG with transparent background
- **File Size**: Under 2MB for fast loading

### Videos
- **Format**: MP4 (H.264), WebM
- **Resolution**: 1920x1080px or 1280x720px
- **File Size**: Under 50MB (larger files slow down page load)
- **Duration**: 15-30 seconds recommended for background videos
- **Alternative**: Use YouTube/Vimeo URLs for large videos

### Recommended Tools
- **Image Optimization**: TinyPNG, Squoosh
- **Video Compression**: HandBrake, FFmpeg
- **Design**: Canva, Photoshop

## 🚀 Technical Details

### Models Created

1. **SiteSettings**
   - Singleton model (only one instance)
   - Stores global site configuration
   - Auto-creates default on first access

2. **HeroSlide**
   - Multiple instances
   - Ordered by display_order field
   - Supports both images and videos
   - Conditional fields based on slide_type

3. **SliderSettings**
   - Singleton model
   - Controls slider JavaScript behavior
   - Mobile-responsive settings

### Database Fields

**SiteSettings:**
- main_logo (ImageField)
- footer_logo (ImageField)  
- favicon (ImageField)
- site_name (CharField)
- contact_email, contact_phone, contact_address
- Social media URLs (Facebook, Twitter, LinkedIn, Instagram, YouTube)
- primary_color, secondary_color (hex codes)

**HeroSlide:**
- title, subtitle (CharField)
- slide_type (image/video)
- image (ImageField)
- video_file (FileField)
- video_url (URLField)
- video_thumbnail (ImageField)
- cta_text, cta_url, cta_style
- text_position, text_color
- display_order, is_active

**SliderSettings:**
- autoplay, autoplay_speed, transition_speed
- transition_effect (fade/slide/zoom/slide-fade)
- show_arrows, show_dots, pause_on_hover
- autoplay_mobile, show_arrows_mobile
- slider_height_desktop, slider_height_mobile
- lazy_load, preload_slides

## 🔧 Admin Interface Features

### Site Settings Admin
- Single instance (no add button after creation)
- Cannot be deleted
- Organized fieldsets for easy navigation
- Inline help text for all fields

### Hero Slide Admin
- List view with thumbnail previews
- Drag-and-drop ordering (via display_order)
- Quick active/inactive toggle
- Bulk actions support
- Collapsible fieldsets for cleaner interface

### Slider Settings Admin
- Single instance
- Organized by functionality sections
- Inline documentation
- Real-time effect preview (coming soon)

## 📱 Responsive Behavior

**Desktop:**
- Full slider height (default 700px)
- Show all navigation controls
- High-quality images

**Tablet:**
- Medium slider height (adjusts automatically)
- All controls visible
- Optimized images

**Mobile:**
- Reduced slider height (default 500px)
- Optional arrow hiding (saves space)
- Touch swipe enabled
- Lazy loading for performance

## ⚡ Performance Optimizations

1. **Lazy Loading**: Images load only when needed
2. **Preloading**: Next slide loads in background
3. **Responsive Images**: Different sizes for different devices
4. **Video Optimization**: Poster images show while video loads
5. **Caching**: Static assets cached in browser

## 🎯 Next Steps

After setting up in admin, the home page will automatically:
1. Use logos from Site Settings
2. Display active Hero Slides in order
3. Apply Slider Settings for behavior
4. Show social media links in footer
5. Use theme colors across the site

**Visit:** http://127.0.0.1:8000/ to see your changes!

---

**Migration Applied:** `0030_heroslide_slidersettings_sitesettings`  
**Status:** ✅ Ready to Use  
**Admin Access:** http://127.0.0.1:8000/admin/
