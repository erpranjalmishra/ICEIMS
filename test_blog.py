#!/usr/bin/env python
"""Test blog functionality without running the full server"""

import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User

# Setup Django
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.views import blog_public_list, blog_public_detail
from conference.models import BlogPost

def test_blog_views():
    """Test blog views functionality"""
    
    print("🧪 Testing blog views...")
    
    # Create a request factory
    factory = RequestFactory()
    
    # Test blog list view
    print("\n📝 Testing blog list view...")
    request = factory.get('/blog/')
    request.user = AnonymousUser()
    
    try:
        response = blog_public_list(request)
        print(f"   ✅ Blog list view works (status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Blog list view error: {e}")
        return False
    
    # Test blog detail view (if we have posts)
    posts = BlogPost.objects.filter(status='published')
    if posts.exists():
        print("\n📰 Testing blog detail view...")
        first_post = posts.first()
        request = factory.get(f'/blog/{first_post.slug}/')
        request.user = AnonymousUser()
        
        try:
            response = blog_public_detail(request, first_post.slug)
            print(f"   ✅ Blog detail view works (status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Blog detail view error: {e}")
            return False
    
    print("\n🎉 All blog views are working correctly!")
    return True

def test_urls():
    """Test URL reversals"""
    from django.urls import reverse
    
    print("\n🔗 Testing URL patterns...")
    
    try:
        urls_to_test = [
            'conference:blog_public_list',
            'conference:login',
            'conference:register',
            'conference:newsletter_signup'
        ]
        
        for url_name in urls_to_test:
            url = reverse(url_name)
            print(f"   ✅ {url_name}: {url}")
            
        # Test detail URL with a real post
        posts = BlogPost.objects.filter(status='published')
        if posts.exists():
            detail_url = reverse('conference:blog_public_detail', args=[posts.first().slug])
            print(f"   ✅ blog detail: {detail_url}")
            
    except Exception as e:
        print(f"   ❌ URL test error: {e}")
        return False
    
    print("   🎉 All URLs resolve correctly!")
    return True

if __name__ == '__main__':
    print("🚀 Testing ICEIMS 2026 Blog System")
    print("=" * 40)
    
    success = True
    success &= test_urls()
    success &= test_blog_views()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ All tests passed! Blog system is ready.")
        print("\n📋 Quick Start Guide:")
        print("   1. Run: python manage.py runserver")
        print("   2. Visit: http://localhost:8000/blog/")
        print("   3. Login: http://localhost:8000/login/ (admin/admin123)")
        print("   4. Admin: http://localhost:8000/admin/blog/")
    else:
        print("❌ Some tests failed. Check the errors above.")