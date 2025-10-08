# Marquee Text Feature Documentation

## Overview
A moving marquee text banner has been added below the homepage slider that can be fully customized through the Django admin panel.

## Features Added

### 1. Database Model (`MarqueeText`)
Location: `conference/models.py`

Fields:
- **text**: The message to display (max 500 characters)
  - Default: "International Conference on Energy and Intelligent Manufacturing Systems 2026 Welcomes You"
- **is_enabled**: Toggle to show/hide the marquee
- **background_color**: Background color in hex format (default: #dc3545 - red)
- **text_color**: Text color in hex format (default: #ffffff - white)
- **animation_speed**: Animation speed in seconds (default: 20s, lower = faster)

### 2. Admin Interface
Location: `conference/admin.py`

Features:
- Easy enable/disable toggle in list view
- Text preview in admin list
- Color and speed customization
- Only ONE marquee instance allowed (prevents multiple entries)
- Cannot be deleted (only disabled)

### 3. Frontend Display
Location: `templates/home.html`

Features:
- Smooth scrolling marquee animation
- Pauses on hover for better readability
- Fully responsive design for mobile/tablet/desktop
- Custom colors and animation speed from admin

## Admin Usage

### Access the Marquee Settings:
1. Go to Django Admin Panel
2. Navigate to **"Marquee Text"** section
3. Click on the existing marquee entry

### Customize the Marquee:
- **Edit Text**: Change the welcome message
- **Enable/Disable**: Toggle the checkbox to show/hide
- **Background Color**: Enter hex color code (e.g., #dc3545, #007bff)
- **Text Color**: Enter hex color code (e.g., #ffffff, #000000)
- **Animation Speed**: Adjust speed in seconds (lower = faster, e.g., 15 for faster, 30 for slower)

### Quick Enable/Disable:
- In the marquee list view, use the checkbox to quickly enable/disable
- Click "Save" to apply changes

## Technical Details

### Migration:
- Migration file: `conference/migrations/0040_marqueetext.py`
- Applied successfully ✅

### Cache Management:
- Homepage cache is automatically updated
- Changes in admin will reflect immediately after saving
- Cache key: `homepage_data_v4`

### CSS Styling:
- Smooth marquee animation with CSS keyframes
- Responsive font sizes for different screen sizes
- Hover effect to pause animation
- Custom colors applied inline from database

### Performance:
- Marquee data is cached with homepage for optimal performance
- No additional database queries per page load
- Lightweight CSS-only animation

## Default Settings
```
Text: "International Conference on Energy and Intelligent Manufacturing Systems 2026 Welcomes You"
Background: Red (#dc3545)
Text Color: White (#ffffff)
Speed: 20 seconds
Status: Enabled
```

## Customization Examples

### Blue Theme:
```
Background Color: #007bff
Text Color: #ffffff
```

### Green Theme:
```
Background Color: #28a745
Text Color: #ffffff
```

### Dark Theme:
```
Background Color: #212529
Text Color: #ffc107
```

### Faster Animation:
```
Animation Speed: 15
```

### Slower Animation:
```
Animation Speed: 30
```

## Notes
- Only one marquee text instance is allowed in the system
- The marquee appears directly below the hero slider on the homepage
- Changes are reflected immediately after saving in admin
- The feature integrates seamlessly with the existing design
