import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import Guideline

# Check all guidelines
all_guidelines = Guideline.objects.all()
print(f'=== ALL GUIDELINES ({all_guidelines.count()}) ===')
for g in all_guidelines:
    print(f'\n{g.id}. {g.title}')
    print(f'   Content Type: {g.content_type}')
    print(f'   Downloadable File: {g.downloadable_file or "EMPTY"}')
    print(f'   Table File: {g.table_file or "EMPTY"}')
    print(f'   Table Data exists: {bool(g.table_data)}')
    if g.table_data:
        print(f'   Table rows: {g.table_data.get("total_rows", 0)}')
        print(f'   Table cols: {g.table_data.get("total_columns", 0)}')
    print(f'   Is Published: {g.is_published}')

# Check specifically table type
print('\n\n=== TABLE TYPE GUIDELINES ===')
table_guidelines = Guideline.objects.filter(content_type='table')
print(f'Count: {table_guidelines.count()}')
for g in table_guidelines:
    print(f'\n{g.id}. {g.title}')
    print(f'   Table File: {g.table_file}')
    print(f'   Has table_data: {bool(g.table_data)}')
    if g.table_file:
        file_path = g.table_file.path
        print(f'   File path: {file_path}')
        print(f'   File exists: {os.path.exists(file_path)}')
