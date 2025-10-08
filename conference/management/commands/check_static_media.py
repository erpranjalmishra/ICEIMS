"""
Django management command to verify static and media files setup
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verify static and media files configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Static & Media Files Configuration ===\n'))
        
        # Static files
        self.stdout.write(f'STATIC_URL: {settings.STATIC_URL}')
        self.stdout.write(f'STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')
        self.stdout.write(f'STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}')
        
        # Check if staticfiles directory exists
        if os.path.exists(settings.STATIC_ROOT):
            file_count = sum([len(files) for r, d, files in os.walk(settings.STATIC_ROOT)])
            self.stdout.write(self.style.SUCCESS(f'✓ STATIC_ROOT exists with {file_count} files'))
        else:
            self.stdout.write(self.style.ERROR(f'✗ STATIC_ROOT does not exist'))
            
        # Media files
        self.stdout.write(f'\nMEDIA_URL: {settings.MEDIA_URL}')
        self.stdout.write(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
        
        # Check if media directory exists
        if os.path.exists(settings.MEDIA_ROOT):
            file_count = sum([len(files) for r, d, files in os.walk(settings.MEDIA_ROOT)])
            self.stdout.write(self.style.SUCCESS(f'✓ MEDIA_ROOT exists with {file_count} files'))
        else:
            self.stdout.write(self.style.ERROR(f'✗ MEDIA_ROOT does not exist'))
            
        # List specific image directories
        self.stdout.write('\n=== Image Directories ===')
        image_dirs = ['images', 'static/images', 'media/site/logos']
        for img_dir in image_dirs:
            full_path = os.path.join(settings.BASE_DIR, img_dir)
            if os.path.exists(full_path):
                files = os.listdir(full_path)
                self.stdout.write(self.style.SUCCESS(f'✓ {img_dir}: {len(files)} files'))
                if files:
                    self.stdout.write(f'  Files: {", ".join(files[:5])}{"..." if len(files) > 5 else ""}')
            else:
                self.stdout.write(self.style.WARNING(f'✗ {img_dir} does not exist'))
                
        self.stdout.write(self.style.SUCCESS('\n=== Configuration Check Complete ===\n'))
