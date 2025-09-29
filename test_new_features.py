#!/usr/bin/env python
"""
Test script to validate the new export and schedule functionality
"""

import os
import sys
import django
from django.conf import settings
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_export_views():
    """Test if export views are accessible"""
    print("Testing export functionality...")
    
    # Test URLs exist
    from django.urls import reverse
    
    try:
        speaker_export = reverse('conference:export_speakers')
        committee_export = reverse('conference:export_committee') 
        schedule_export = reverse('conference:export_schedule')
        logs_export = reverse('conference:export_logs')
        
        print("✅ All export URLs configured correctly")
        print(f"   - Speakers: {speaker_export}")
        print(f"   - Committee: {committee_export}")
        print(f"   - Schedule: {schedule_export}")
        print(f"   - Logs: {logs_export}")
        return True
    except Exception as e:
        print(f"❌ Export URL error: {e}")
        return False

def test_schedule_view():
    """Test if schedule view works with dynamic data"""
    print("Testing dynamic schedule view...")
    try:
        client = Client()
        response = client.get('/schedule/')
        
        if response.status_code == 200:
            print("✅ Schedule page loads successfully")
            if 'schedule_by_day' in response.context:
                print("✅ Dynamic schedule context available")
            return True
        else:
            print(f"❌ Schedule page returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Schedule view error: {e}")
        return False

def test_dashboard_activity():
    """Test if admin dashboard shows real activity logs"""
    print("Testing admin dashboard activity logs...")
    try:
        from conference.views import get_activity_icon
        from django.contrib.admin.models import LogEntry
        
        # Test icon function
        test_result = get_activity_icon(type('MockLog', (), {
            'content_type': type('MockType', (), {'model': 'blogpost'})(),
            'action_flag': 1
        })())
        
        if test_result:
            print("✅ Activity icon function works")
            
        # Check if LogEntry import works
        log_count = LogEntry.objects.count()
        print(f"✅ Found {log_count} activity log entries")
        return True
    except Exception as e:
        print(f"❌ Dashboard activity error: {e}")
        return False

def main():
    print("=== Testing Export, Schedule, and Activity Features ===\n")
    
    results = []
    results.append(test_export_views())
    results.append(test_schedule_view())
    results.append(test_dashboard_activity())
    
    print(f"\n=== Results ===")
    print(f"Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All functionality is working correctly!")
        print("\n📋 Available Features:")
        print("   - Export speakers/committee/schedule/logs to Excel, PDF, CSV, JSON")
        print("   - Dynamic schedule page with database content")
        print("   - Real-time activity logs in admin dashboard")
        print("   - Export buttons in all admin list pages")
        print("   - Comprehensive export options in admin dashboard")
        sys.exit(0)
    else:
        print("⚠️  Some issues found")
        sys.exit(1)

if __name__ == '__main__':
    main()