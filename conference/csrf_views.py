from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def csrf_failure(request, reason=""):
    """
    Custom CSRF failure view to provide better error messages
    """
    context = {
        'reason': reason,
        'request': request,
    }
    
    # If it's an AJAX request, return JSON response
    if request.headers.get('Content-Type') == 'application/json':
        from django.http import JsonResponse
        return JsonResponse({
            'error': 'CSRF verification failed',
            'reason': reason,
            'reload_required': True
        }, status=403)
    
    # For regular requests, render a user-friendly error page
    return render(request, 'errors/csrf_error.html', context, status=403)