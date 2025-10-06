"""
Template tags for handling media files
"""
from django import template
from django.conf import settings
import os

register = template.Library()


@register.filter
def media_url(value):
    """
    Ensure media URL is properly formatted with full path.
    Usage: {{ object.image|media_url }}
    """
    if not value:
        return ''
    
    # If value already has a URL attribute, use it
    if hasattr(value, 'url'):
        url = value.url
    else:
        url = str(value)
    
    # Ensure URL starts with /media/
    if not url.startswith('/media/') and not url.startswith('http'):
        if not url.startswith('/'):
            url = '/media/' + url
    
    # In production, make it absolute
    if not settings.DEBUG and not url.startswith('http'):
        url = settings.MEDIA_URL.rstrip('/') + '/' + url.lstrip('/')
    
    return url


@register.filter
def has_media(obj, field_name):
    """
    Check if a model instance has a media file.
    Usage: {% if sponsor|has_media:'logo' %}
    """
    if not obj or not field_name:
        return False
    
    try:
        field_value = getattr(obj, field_name)
        if not field_value:
            return False
        
        # Check if file exists
        if hasattr(field_value, 'path'):
            return os.path.exists(field_value.path)
        
        return bool(field_value)
    except:
        return False


@register.simple_tag
def media_or_default(media_field, default_path=''):
    """
    Return media URL or default image path.
    Usage: {% media_or_default sponsor.logo '/static/images/default-logo.png' %}
    """
    if media_field:
        try:
            if hasattr(media_field, 'url'):
                return media_field.url
            return str(media_field)
        except:
            pass
    
    return default_path


@register.filter
def debug_media(value):
    """
    Debug filter to show media path information.
    Usage: {{ object.image|debug_media }}
    """
    if not value:
        return 'No media file'
    
    info = []
    info.append(f"Value: {value}")
    
    if hasattr(value, 'url'):
        info.append(f"URL: {value.url}")
    
    if hasattr(value, 'path'):
        info.append(f"Path: {value.path}")
        info.append(f"Exists: {os.path.exists(value.path)}")
    
    return ' | '.join(info)
