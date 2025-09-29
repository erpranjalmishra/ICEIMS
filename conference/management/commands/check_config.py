from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check Django configuration for production deployment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Django Configuration Check'))
        self.stdout.write('=' * 50)
        
        # Environment detection
        debug_status = "ON" if settings.DEBUG else "OFF"
        production_status = "YES" if getattr(settings, 'IS_PRODUCTION', False) else "NO"
        
        self.stdout.write(f'Debug Mode: {debug_status}')
        self.stdout.write(f'Production Environment: {production_status}')
        self.stdout.write(f'Allowed Hosts: {settings.ALLOWED_HOSTS}')
        
        # Security settings
        self.stdout.write('\n🔒 Security Settings:')
        self.stdout.write(f'CSRF Cookie Secure: {settings.CSRF_COOKIE_SECURE}')
        self.stdout.write(f'Session Cookie Secure: {settings.SESSION_COOKIE_SECURE}')
        self.stdout.write(f'CSRF Trusted Origins: {settings.CSRF_TRUSTED_ORIGINS}')
        
        # Check for required environment variables
        self.stdout.write('\n🌍 Environment Variables:')
        env_vars = ['DEBUG', 'ALLOWED_HOSTS', 'SECRET_KEY']
        for var in env_vars:
            value = os.environ.get(var, 'Not Set')
            if var == 'SECRET_KEY' and value != 'Not Set':
                value = f'{value[:10]}...(hidden)'
            self.stdout.write(f'{var}: {value}')
        
        # Database check
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write('\n✅ Database: Connected')
        except Exception as e:
            self.stdout.write(f'\n❌ Database: Error - {e}')
        
        # Blog system check
        try:
            from conference.models import BlogPost, Category, Comment
            posts_count = BlogPost.objects.count()
            categories_count = Category.objects.count()
            comments_count = Comment.objects.count()
            pending_comments = Comment.objects.filter(status='pending').count()
            
            self.stdout.write('\n📝 Blog System:')
            self.stdout.write(f'Posts: {posts_count}')
            self.stdout.write(f'Categories: {categories_count}')
            self.stdout.write(f'Comments: {comments_count} (Pending: {pending_comments})')
        except Exception as e:
            self.stdout.write(f'\n❌ Blog System: Error - {e}')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('Configuration check completed!'))
        
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING('\n⚠️  Remember to set DEBUG=False in production!'))