"""
Custom template tags for performance optimization
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def lazy_img(src, alt='', css_class='', width='', height=''):
    """
    Generate an image tag with lazy loading
    Usage: {% lazy_img image_url "Alt text" "css-class" "width" "height" %}
    """
    attributes = []
    
    if css_class:
        attributes.append(f'class="{css_class}"')
    
    if width:
        attributes.append(f'width="{width}"')
    
    if height:
        attributes.append(f'height="{height}"')
    
    attributes.append('loading="lazy"')
    attributes.append('decoding="async"')
    
    attrs_str = ' '.join(attributes)
    
    html = f'<img src="{src}" alt="{alt}" {attrs_str}>'
    
    return mark_safe(html)


@register.filter
def add_lazy_loading(html_content):
    """
    Add lazy loading to all images in HTML content
    Usage: {{ content|add_lazy_loading }}
    """
    import re
    
    def add_loading_attr(match):
        img_tag = match.group(0)
        if 'loading=' not in img_tag:
            img_tag = img_tag.replace('<img', '<img loading="lazy" decoding="async"')
        return img_tag
    
    result = re.sub(r'<img[^>]+>', add_loading_attr, html_content)
    return mark_safe(result)
