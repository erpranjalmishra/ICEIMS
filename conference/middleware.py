from django.middleware.csrf import CsrfViewMiddleware
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings

class CustomCSRFMiddleware(CsrfViewMiddleware):
    """Custom CSRF middleware to handle CSRF failures more gracefully"""
    
    def process_response(self, request, response):
        # Always ensure CSRF cookie is set for views that need it
        if hasattr(request, 'csrf_cookie_needs_reset'):
            if request.csrf_cookie_needs_reset:
                self._set_token(request)
        
        return super().process_response(request, response)