"""
Middleware to serve media files on Azure App Service
"""
from django.conf import settings
from django.http import FileResponse, Http404
from django.utils.encoding import filepath_to_uri
import os
import mimetypes


class AzureMediaMiddleware:
    """
    Middleware to serve media files on Azure App Service.
    
    This is a workaround for Azure App Service not serving media files
    like a traditional web server would. In production, consider using
    Azure Blob Storage for better performance and scalability.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this is a media file request
        if request.path.startswith(settings.MEDIA_URL):
            # Get the relative path from MEDIA_URL
            relative_path = request.path[len(settings.MEDIA_URL):]
            
            # Build the absolute file path
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            
            # Check if file exists
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Determine content type
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                # Serve the file
                try:
                    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
                    
                    # Set cache headers for better performance
                    response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
                    
                    return response
                except Exception as e:
                    # Log the error (you can add proper logging here)
                    print(f"Error serving media file {file_path}: {e}")
                    raise Http404("Media file not found")
            else:
                raise Http404("Media file not found")
        
        # Not a media request, continue normally
        response = self.get_response(request)
        return response
