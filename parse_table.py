import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import Guideline
from conference.utils.table_parser import parse_table_file

# Get the guideline
g = Guideline.objects.get(id=2)
print(f'Guideline: {g.title}')
print(f'Table File: {g.table_file}')

if g.table_file:
    file_path = g.table_file.path
    print(f'File Path: {file_path}')
    print(f'File Exists: {os.path.exists(file_path)}')
    
    try:
        # Parse the table
        table_data = parse_table_file(file_path, g.table_has_header)
        print(f'\nParsed successfully!')
        print(f'Rows: {table_data.get("total_rows")}')
        print(f'Columns: {table_data.get("total_columns")}')
        print(f'Headers: {table_data.get("headers")}')
        print(f'First 3 rows:')
        for i, row in enumerate(table_data.get("rows", [])[:3]):
            print(f'  Row {i+1}: {row}')
        
        # Save to database
        g.table_data = table_data
        g.save()
        print('\n✅ Table data saved to database!')
        
    except Exception as e:
        print(f'\n❌ Error parsing table: {e}')
        import traceback
        traceback.print_exc()
else:
    print('No table file attached')
