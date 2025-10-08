"""
Signal handlers for automatic cache invalidation.
Ensures admin changes reflect immediately on the website.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

# Set up logger
logger = logging.getLogger('conference.cache')

from .models import (
    CommitteeMember, ConferenceTrack, TouristAttraction,
    ImportantDate, Slider, ConferenceSettings, Sponsor,
    BlogPost, Category, Tag, Notice, UniversityInfo, 
    UniversityGallery, HeroSlide, MarqueeText, ConferenceTopic,
    Timeline, HierarchyLevel
)


def clear_all_caches(model_name=None, action="updated"):
    """Clear all application caches to ensure fresh content"""
    try:
        cache.clear()
        message = f"✅ Cache auto-cleared: {model_name} {action}"
        print(message)
        logger.info(message)
    except Exception as e:
        warning = f"⚠️ Cache clear warning: {e}"
        print(warning)
        logger.warning(warning)


# List of models that should trigger cache clearing
CACHED_MODELS = [
    CommitteeMember,
    ConferenceTrack,
    TouristAttraction,
    ImportantDate,
    Slider,
    ConferenceSettings,
    Sponsor,
    BlogPost,
    Category,
    Tag,
    Notice,
    UniversityInfo,
    UniversityGallery,
    HeroSlide,
    MarqueeText,
    ConferenceTopic,
    Timeline,
    HierarchyLevel,
]


# Register signal handlers for all cached models
for model in CACHED_MODELS:
    
    def make_save_handler(model_class):
        @receiver(post_save, sender=model_class)
        def clear_cache_on_save(sender, instance, created, **kwargs):
            """Clear cache when any content is saved in admin"""
            action = "created" if created else "updated"
            model_name = sender._meta.verbose_name or sender.__name__
            clear_all_caches(model_name=model_name, action=action)
        return clear_cache_on_save
    
    def make_delete_handler(model_class):
        @receiver(post_delete, sender=model_class)
        def clear_cache_on_delete(sender, instance, **kwargs):
            """Clear cache when any content is deleted in admin"""
            model_name = sender._meta.verbose_name or sender.__name__
            clear_all_caches(model_name=model_name, action="deleted")
        return clear_cache_on_delete
    
    # Register the handlers
    make_save_handler(model)
    make_delete_handler(model)


print("🔄 Auto-cache clearing enabled: Admin changes reflect immediately on website")
