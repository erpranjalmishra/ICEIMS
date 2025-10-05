import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import Guideline, GuidelineCategory
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create a category
category, _ = GuidelineCategory.objects.get_or_create(
    slug='submission',
    defaults={
        'title': 'Paper Submission',
        'icon': 'fas fa-file-upload',
        'color': '#a0352f',
        'description': 'Guidelines for paper submission'
    }
)

# Get admin user
admin_user = User.objects.filter(is_superuser=True).first()

# Delete any existing test guidelines
Guideline.objects.filter(title__startswith='Test Auto-Parse').delete()

# Create a test guideline with table
import time
timestamp = int(time.time())
guideline = Guideline.objects.create(
    category=category,
    title=f'Test Auto-Parse Table {timestamp}',
    slug=f'test-auto-parse-table-{timestamp}',
    short_description='Testing automatic table parsing on save',
    content_type='table',
    table_title='Registration Fees',
    table_has_header=True,
    is_published=True,
    created_by=admin_user
)

# Copy sample file
source_file = 'media/guidelines/tables/registration_fees_sample.xlsx'
if os.path.exists(source_file):
    dest_path = f'media/guidelines/tables/test_auto_parse_{guideline.id}.xlsx'
    shutil.copy(source_file, dest_path)
    
    # Assign the file to the guideline
    guideline.table_file = dest_path.replace('media/', '')
    guideline.save()  # This should trigger auto-parsing
    
    print(f"✅ Created guideline: {guideline.title}")
    print(f"   Table file: {guideline.table_file}")
    print(f"   Table data exists: {bool(guideline.table_data)}")
    
    if guideline.table_data:
        print(f"   ✅ AUTO-PARSING WORKED!")
        print(f"   Rows: {guideline.table_data.get('total_rows')}")
        print(f"   Columns: {guideline.table_data.get('total_columns')}")
    else:
        print(f"   ❌ AUTO-PARSING FAILED - table_data is empty")
else:
    print(f"❌ Sample file not found: {source_file}")
