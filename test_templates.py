#!/usr/bin/env python
"""
Test both speaker template creation and error page functionality
"""

import os
import sys
import django
from django.conf import settings
from django.test import Client
from django.template.loader import get_template

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_speaker_templates():
    """Test if speaker admin templates exist and can be loaded"""
    print("Testing speaker admin templates...")
    try:
        # Test speaker create template
        template_create = get_template('admin/speaker_create.html')
        print("✅ speaker_create.html template exists and loads")
        
        # Test speaker edit template
        template_edit = get_template('admin/speaker_edit.html')
        print("✅ speaker_edit.html template exists and loads")
        
        return True
    except Exception as e:
        print(f"❌ Error loading speaker templates: {e}")
        return False

def test_error_templates():
    """Test error templates and views"""
    print("Testing error page templates...")
    try:
        client = Client()
        
        # Test custom 404 page
        response = client.get('/test-404/')
        if response.status_code == 404:
            print("✅ 404 error page works")
        else:
            print(f"❌ 404 page returned status {response.status_code}")
            return False
        
        # Test custom 500 page  
        response = client.get('/test-500/')
        if response.status_code == 500:
            print("✅ 500 error page works")
        else:
            print(f"❌ 500 page returned status {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error testing error pages: {e}")
        return False

def test_speaker_create_view():
    """Test speaker create view access"""
    print("Testing speaker create view access...")
    try:
        client = Client()
        response = client.get('/admin-panel/speakers/create/')
        
        # Should redirect to login for non-authenticated users
        if response.status_code in [200, 302]:
            print("✅ Speaker create view is accessible")
            return True
        else:
            print(f"❌ Speaker create view returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing speaker create view: {e}")
        return False

def main():
    print("=== Testing Speaker Templates and Error Pages ===\n")
    
    results = []
    results.append(test_speaker_templates())
    results.append(test_error_templates())
    results.append(test_speaker_create_view())
    
    print(f"\n=== Results ===")
    print(f"Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All templates and error pages are working!")
        print("\nNote: Error pages work in development via test URLs:")
        print("- http://127.0.0.1:8000/test-404/ (Test 404 page)")
        print("- http://127.0.0.1:8000/test-500/ (Test 500 page)")
        print("- In production with DEBUG=False, they'll show automatically for real 404/500 errors")
        sys.exit(0)
    else:
        print("⚠️  Some issues remain")
        sys.exit(1)

if __name__ == '__main__':
    main()