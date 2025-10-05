from django.middleware.csrf import CsrfViewMiddleware
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
import logging

logger = logging.getLogger(__name__)

class CustomCSRFMiddleware(CsrfViewMiddleware):
    """Custom CSRF middleware to handle CSRF failures more gracefully"""
    
    def process_response(self, request, response):
        # Always ensure CSRF cookie is set for views that need it
        if hasattr(request, 'csrf_cookie_needs_reset'):
            if request.csrf_cookie_needs_reset:
                self._set_token(request)
        
        return super().process_response(request, response)

class MaintenanceMiddleware(MiddlewareMixin):
    """Middleware to handle maintenance mode"""
    
    def process_request(self, request):
        # Define admin-only URLs that should always work during maintenance
        admin_urls = [
            '/admin/',
            '/admin-panel/',
            '/blog-admin/',
            '/login/',
            '/logout/',
            '/static/',
            '/media/',
        ]
        
        # Check if current path is an admin URL
        is_admin_path = any(request.path.startswith(url) for url in admin_urls)
        
        # Allow admin paths for all users (they have their own authentication)
        if is_admin_path:
            return None
        
        try:
            from .models import MaintenanceMode
            
            # Check for site-wide maintenance
            site_maintenance = MaintenanceMode.objects.filter(
                maintenance_type='site',
                is_active=True
            ).first()
            
            if site_maintenance and site_maintenance.is_currently_active():
                return render(request, 'errors/maintenance.html', {
                    'maintenance': site_maintenance
                }, status=503)
            
            # Check for page-specific maintenance
            current_url = request.path
            page_maintenance = MaintenanceMode.objects.filter(
                maintenance_type='page',
                is_active=True,
                page_url=current_url
            ).first()
            
            if page_maintenance and page_maintenance.is_currently_active():
                return render(request, 'errors/maintenance.html', {
                    'maintenance': page_maintenance
                }, status=503)
                
        except Exception as e:
            # If there's any error with maintenance check, continue normally
            logger.error(f"Maintenance middleware error: {e}")
            pass
        
        return None
        
        try:
            from .models import MaintenanceMode
            
            # Check for site-wide maintenance
            site_maintenance = MaintenanceMode.objects.filter(
                maintenance_type='site',
                is_active=True
            ).first()
            
            if site_maintenance and site_maintenance.is_currently_active():
                return render(request, 'errors/maintenance.html', {
                    'maintenance': site_maintenance
                }, status=503)
            
            # Check for page-specific maintenance
            current_url = request.path
            page_maintenance = MaintenanceMode.objects.filter(
                maintenance_type='page',
                is_active=True,
                page_url=current_url
            ).first()
            
            if page_maintenance and page_maintenance.is_currently_active():
                return render(request, 'errors/maintenance.html', {
                    'maintenance': page_maintenance
                }, status=503)
                
        except Exception as e:
            # If there's any error with maintenance check, continue normally
            logger.error(f"Maintenance middleware error: {e}")
            pass
        
        return None

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security and performance headers"""
    
    def process_response(self, request, response):
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add performance headers
        # Enable browser caching for static files
        if request.path.startswith(('/static/', '/media/')):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
        else:
            # For dynamic pages, cache for short time
            response['Cache-Control'] = 'public, max-age=300'  # 5 minutes
        
        # Enable compression hint
        response['Vary'] = 'Accept-Encoding'
        
        return response
        
        return response