from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse

class Command(BaseCommand):
    help = 'Test blog system functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testing Blog System...'))
        
        # Create a test client
        client = Client()
        
        # Test blog list view
        try:
            response = client.get(reverse('conference:blog_public_list'))
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('   ✅ Blog list view: OK'))
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Blog list view: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Blog list view error: {e}'))
        
        # Test login page
        try:
            response = client.get(reverse('conference:login'))
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('   ✅ Login page: OK'))
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Login page: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Login page error: {e}'))
        
        # Test register page
        try:
            response = client.get(reverse('conference:register'))
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('   ✅ Register page: OK'))
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Register page: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Register page error: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Blog system test completed!'))
        self.stdout.write('📋 Next steps:')
        self.stdout.write('   1. Run: python manage.py runserver')
        self.stdout.write('   2. Visit: http://localhost:8000/blog/')
        self.stdout.write('   3. Login: http://localhost:8000/login/ (admin/admin123)')
        self.stdout.write('   4. Blog Admin: http://localhost:8000/blog-admin/')
        self.stdout.write('   5. Comment Management: http://localhost:8000/blog-admin/comments/')
        self.stdout.write('   6. Django Admin: http://localhost:8000/admin/')