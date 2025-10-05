from django import template

register = template.Library()

@register.filter
def has_user_permission(user, permission):
    """Check if user has specific permission"""
    if user.is_superuser:
        return True
    if not user.is_authenticated:
        return False
    if not hasattr(user, 'profile') or not user.profile:
        return False
    return user.profile.has_permission(permission)

@register.simple_tag
def can_manage_users(user):
    """Check if user can manage other users"""
    if user.is_superuser:
        return True
    if not hasattr(user, 'profile') or not user.profile:
        return False
    return user.profile.has_permission('can_manage_users')