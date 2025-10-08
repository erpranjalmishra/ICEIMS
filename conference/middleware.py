from django.middleware.csrf import CsrfViewMiddleware
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
import logging
import hashlib

logger = logging.getLogger(__name__)

class CustomCSRFMiddleware(CsrfViewMiddleware):
    """Custom CSRF middleware to handle CSRF failures more gracefully"""
    
    def process_response(self, request, response):
        # Always ensure CSRF cookie is set for views that need it
        if hasattr(request, 'csrf_cookie_needs_reset'):
            if request.csrf_cookie_needs_reset:
                self._set_token(request)
        
        return super().process_response(request, response)


class VisitorTrackingMiddleware(MiddlewareMixin):
    """Track unique visitors and log detailed page visits"""
    
    def process_request(self, request):
        # Skip tracking for admin, static files, and API calls
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None
        
        try:
            from .models import VisitorCounter, PageVisitLog
            
            # Get visitor information
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
            
            # Create unique session key from IP + User Agent
            session_string = f"{ip_address}_{user_agent}"
            session_key = hashlib.md5(session_string.encode()).hexdigest()
            
            # Get or create visitor record
            visitor, created = VisitorCounter.objects.get_or_create(
                session_key=session_key,
                defaults={
                    'ip_address': ip_address,
                    'user_agent': user_agent,
                }
            )
            
            # Update visit count for returning visitors
            if not created:
                visitor.visit_count += 1
                visitor.save(update_fields=['visit_count', 'last_visit'])
            
            # Log detailed page visit
            browser, os_name, device_type = self.parse_user_agent(user_agent)
            
            PageVisitLog.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                url_path=request.path,
                full_url=request.build_absolute_uri(),
                http_method=request.method,
                referrer=request.META.get('HTTP_REFERER', ''),
                device_type=device_type,
                browser=browser,
                os=os_name,
                session_key=session_key,
                is_authenticated=request.user.is_authenticated if hasattr(request, 'user') else False,
                username=request.user.username if hasattr(request, 'user') and request.user.is_authenticated else '',
            )
            
        except Exception as e:
            logger.error(f"Visitor tracking error: {e}")
        
        return None
    
    def get_client_ip(self, request):
        """Get the client's real IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
    
    def parse_user_agent(self, user_agent):
        """Parse user agent to extract browser, OS, and device type"""
        ua_lower = user_agent.lower()
        
        # Detect browser
        browser = 'Unknown'
        if 'edg/' in ua_lower or 'edge/' in ua_lower:
            browser = 'Microsoft Edge'
        elif 'chrome/' in ua_lower and 'edg/' not in ua_lower:
            browser = 'Google Chrome'
        elif 'firefox/' in ua_lower:
            browser = 'Mozilla Firefox'
        elif 'safari/' in ua_lower and 'chrome' not in ua_lower:
            browser = 'Safari'
        elif 'opera/' in ua_lower or 'opr/' in ua_lower:
            browser = 'Opera'
        elif 'msie' in ua_lower or 'trident/' in ua_lower:
            browser = 'Internet Explorer'
        
        # Detect OS
        os_name = 'Unknown'
        if 'windows nt 10' in ua_lower:
            os_name = 'Windows 10/11'
        elif 'windows nt 6.3' in ua_lower:
            os_name = 'Windows 8.1'
        elif 'windows nt 6.2' in ua_lower:
            os_name = 'Windows 8'
        elif 'windows nt 6.1' in ua_lower:
            os_name = 'Windows 7'
        elif 'windows' in ua_lower:
            os_name = 'Windows'
        elif 'mac os x' in ua_lower or 'macintosh' in ua_lower:
            os_name = 'macOS'
        elif 'linux' in ua_lower:
            os_name = 'Linux'
        elif 'android' in ua_lower:
            os_name = 'Android'
        elif 'iphone' in ua_lower or 'ipad' in ua_lower:
            os_name = 'iOS'
        
        # Detect device type
        device_type = 'Desktop'
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            device_type = 'Mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            device_type = 'Tablet'
        
        return browser, os_name, device_type

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