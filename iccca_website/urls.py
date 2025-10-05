"""
URL configuration for iccca_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.shortcuts import redirect

# Custom error handlers
handler404 = 'conference.views.custom_404_view'
handler500 = 'conference.views.custom_500_view'

# Override Django admin login to redirect to custom admin dashboard
original_admin_login = admin.site.login

def custom_admin_login(request, extra_context=None):
    """Redirect to custom admin dashboard after successful login"""
    if request.method == 'POST':
        response = original_admin_login(request, extra_context)
        # If login was successful (user is authenticated), redirect to custom admin dashboard
        if request.user.is_authenticated:
            return redirect('conference:admin_dashboard')
        return response
    return original_admin_login(request, extra_context)

# Apply the custom login
admin.site.login = custom_admin_login

# Customize Django admin site
admin.site.site_header = 'ICEIMS 2026 Administration'
admin.site.site_title = 'ICEIMS Admin Portal'
admin.site.index_title = 'Welcome to ICEIMS Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('conference.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
