"""
Context processors to make data available in all templates
"""

from .models import SiteSettings, SliderSettings, HeroSlide

def site_settings(request):
    """
    Add site settings to all template contexts
    """
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    return {
        'site_settings': settings,
    }

def slider_settings(request):
    """
    Add slider settings and hero slides to all template contexts
    """
    try:
        settings = SliderSettings.objects.first()
        slides = HeroSlide.objects.filter(is_active=True).order_by('display_order')
    except:
        settings = None
        slides = []
    
    return {
        'slider_settings': settings,
        'hero_slides': slides,
    }
