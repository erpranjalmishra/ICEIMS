# Website Control Integration - COMPLETE SETUP

## ✅ What Was Done

### 1. Context Processors Created
**File**: `conference/context_processors.py`
- Added `site_settings()` - makes site settings available globally
- Added `slider_settings()` - makes slider settings available globally

### 2. Settings Updated
**File**: `iccca_website/settings.py`
- Added context processors to TEMPLATES configuration:
  - `'conference.context_processors.site_settings'`
  - `'conference.context_processors.slider_settings'`

### 3. Home View Updated
**File**: `conference/views.py` (line 22-62)
- Updated cache key to `'homepage_data_v3'`
- Added `HeroSlide` import
- Added `hero_slides` query to get active slides
- Passes `hero_slides` to template context

### 4. Base Template Updated
**File**: `templates/base.html`

**Header Logo** (line 60-68):
```html
{% if site_settings and site_settings.main_logo %}
    <img src="{{ site_settings.main_logo.url }}" alt="{{ site_settings.site_name|default:'ICEIMS' }}" class="navbar-logo">
{% else %}
    <img src="{% static 'images/ICEIMS.svg' %}" alt="ICEIMS Logo" class="navbar-logo">
{% endif %}
```

**Footer Logo** (line 156-162):
```html
{% if site_settings and site_settings.footer_logo %}
    <img src="{{ site_settings.footer_logo.url }}" alt="{{ site_settings.site_name|default:'ICEIMS' }}" height="80">
{% else %}
    <img src="{% static 'images/ICEIMS.svg' %}" alt="ICEIMS Logo" height="80">
{% endif %}
```

**Footer Contact Info** (line 163-188):
- Uses `site_settings.contact_email` if available
- Uses `site_settings.contact_address` if available
- Falls back to hardcoded values

## 🔧 What Still Needs To Be Done

### HOME PAGE SLIDER - Manual Update Required

The home page slider code needs to be updated to use the new hero slides. The file `templates/home.html` starting around line 145 needs the carousel section replaced.

**Current Problem**: The slider is using old `slider_images` variable, not the new `hero_slides`.

**Solution**: Replace the entire carousel section (lines 145-193) in `templates/home.html` with the code below.

## 📝 PASTE THIS CODE INTO templates/home.html

**Replace lines 145-193 with:**

```html
<!-- Hero Section with Slider -->
<section id="home" class="hero-section">
    <div id="heroCarousel" class="carousel slide carousel-fade" data-bs-ride="carousel" 
         data-bs-interval="{% if slider_settings %}{{ slider_settings.autoplay_speed }}{% else %}4000{% endif %}">
        <div class="carousel-indicators">
            {% if hero_slides %}
                {% for slide in hero_slides %}
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="{{ forloop.counter0 }}" 
                        {% if forloop.first %}class="active"{% endif %} aria-current="true" 
                        aria-label="Slide {{ forloop.counter }}"></button>
                {% endfor %}
            {% elif slider_images %}
                {% for slide in slider_images %}
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="{{ forloop.counter0 }}" 
                        {% if forloop.first %}class="active"{% endif %} aria-current="true" 
                        aria-label="Slide {{ forloop.counter }}"></button>
                {% endfor %}
            {% else %}
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="0" 
                        class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="1" 
                        aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="2" 
                        aria-label="Slide 3"></button>
            {% endif %}
        </div>
        
        <div class="carousel-inner">
            {% if hero_slides %}
                {% for slide in hero_slides %}
                <div class="carousel-item {% if forloop.first %}active{% endif %}" 
                     data-bs-interval="{% if slider_settings %}{{ slider_settings.autoplay_speed }}{% else %}4000{% endif %}">
                    {% if slide.slide_type == 'image' and slide.image %}
                        <img src="{{ slide.image.url }}" class="d-block w-100" alt="{{ slide.title }}">
                    {% elif slide.slide_type == 'video' and slide.video_file %}
                        <video class="d-block w-100" autoplay muted loop playsinline>
                            <source src="{{ slide.video_file.url }}" type="video/mp4">
                        </video>
                    {% elif slide.slide_type == 'video' and slide.video_url %}
                        <iframe class="d-block w-100" src="{{ slide.video_url }}" frameborder="0" allowfullscreen></iframe>
                    {% endif %}
                    <div class="carousel-overlay"></div>
                    {% if slide.title or slide.subtitle or slide.cta_text %}
                    <div class="carousel-caption d-md-block text-{{ slide.text_position|default:'center' }}">
                        {% if slide.title %}<h2 class="display-4 fw-bold">{{ slide.title }}</h2>{% endif %}
                        {% if slide.subtitle %}<p class="lead">{{ slide.subtitle }}</p>{% endif %}
                        {% if slide.cta_text and slide.cta_url %}
                            <a href="{{ slide.cta_url }}" class="btn btn-lg {% if slide.cta_style == 'outline' %}btn-outline-light{% else %}btn-primary{% endif %}">
                                {{ slide.cta_text }}
                            </a>
                        {% endif %}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            {% elif slider_images %}
                {% for slide in slider_images %}
                <div class="carousel-item {% if forloop.first %}active{% endif %}" data-bs-interval="4000">
                    <img src="{{ slide.image.url }}" class="d-block w-100" alt="{{ slide.title }}">
                    <div class="carousel-overlay"></div>
                </div>
                {% endfor %}
            {% else %}
                <div class="carousel-item active" data-bs-interval="4000">
                    <img src="{% static 'images/m1.jpg' %}" class="d-block w-100" alt="ICEIMS 2026 Conference">
                    <div class="carousel-overlay"></div>
                </div>
                <div class="carousel-item" data-bs-interval="4000">
                    <img src="{% static 'images/m2.jpg' %}" class="d-block w-100" alt="Welcome to ICEIMS">
                    <div class="carousel-overlay"></div>
                </div>
                <div class="carousel-item" data-bs-interval="4000">
                    <img src="{% static 'images/m3.jpeg' %}" class="d-block w-100" alt="Call for Papers">
                    <div class="carousel-overlay"></div>
                </div>
            {% endif %}
        </div>
        
        {% if slider_settings and slider_settings.show_arrows %}
        <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
        </button>
        {% else %}
        <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
        </button>
        {% endif %}
    </div>
</section>
```

## 🚀 After Making Changes

1. **Clear Django Cache**:
   ```bash
   python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Cache cleared!')"
   ```

2. **Restart the development server** (Ctrl+C, then `python manage.py runserver`)

3. **Hard refresh the browser** (Ctrl+Shift+R or Ctrl+F5)

4. **Check that it works**:
   - Logo in header should update
   - Logo in footer should update
   - Contact info in footer should update
   - Hero slider should show your uploaded slides

## 📋 Summary of Integration

| Component | Status | Notes |
|-----------|--------|-------|
| Context Processors | ✅ Created | Makes settings available globally |
| Settings.py | ✅ Updated | Context processors registered |
| Home View | ✅ Updated | Queries hero slides |
| Base Template - Header Logo | ✅ Updated | Uses site_settings.main_logo |
| Base Template - Footer Logo | ✅ Updated | Uses site_settings.footer_logo |
| Base Template - Footer Info | ✅ Updated | Uses site_settings contact info |
| Home Template - Slider | ⚠️ **NEEDS MANUAL UPDATE** | Replace carousel section |

## 🎯 What This Achieves

Once the home template slider is updated:

1. **Logos managed from admin** - Upload/change logos without code changes
2. **Contact info managed from admin** - Update footer contact without code changes  
3. **Hero slides managed from admin** - Add/remove/reorder slides easily
4. **Slider settings configurable** - Control speed, transitions, navigation
5. **Support for images AND videos** - Upload videos or use YouTube/Vimeo URLs
6. **CTA buttons on slides** - Add call-to-action buttons with custom text/links
7. **Text overlay positioning** - Control where text appears on slides

All of this WITHOUT touching code - just use the admin panel!
