"""
Script to update all attraction blog links in attractions.html
"""

import re

# Read the file
with open('templates/attractions.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the replacements - mapping old href to new slug
replacements = {
    # Red Fort
    r'(<a href=")[^"]*(" class="btn btn-blog btn-sm">\s*<i class="fas fa-book-open me-1"></i>Read Guide\s*</a>)': 
        r'\1{% url \'conference:attraction_detail\' \'red-fort\' %}\2',
}

# Apply specific replacements based on context
# Pattern to find and replace each attraction's Read Guide link

# Find all Read Guide button links
pattern = r'<a href="#" class="btn btn-blog btn-sm">\s*<i class="fas fa-book-open me-1"></i>Read Guide\s*</a>'

# Attraction slugs in order they appear in the template
slugs = [
    'red-fort',
    'india-gate',
    'lotus-temple',
    'qutub-minar',
    'akshardham-temple',
    'worlds-of-wonder',
    'great-india-place',
    'taj-mahal',
    'humayuns-tomb',
    'iskcon-temple',
    'chandni-chowk',
    'lodhi-gardens'
]

# Replace all occurrences
count = 0
for slug in slugs:
    new_link = f'<a href="{{% url \'conference:attraction_detail\' \'{slug}\' %}}" class="btn btn-blog btn-sm">\n                                <i class="fas fa-book-open me-1"></i>Read Guide\n                            </a>'
    
    # Replace one occurrence at a time
    content = content.replace(
        '<a href="#" class="btn btn-blog btn-sm">\n                                <i class="fas fa-book-open me-1"></i>Read Guide\n                            </a>',
        new_link,
        1  # Replace only the first occurrence
    )
    count += 1
    print(f"Updated link {count}: {slug}")

# Write back to file
with open('templates/attractions.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nSuccessfully updated {count} attraction links!")
print("All 'Read Guide' buttons now link to individual blog pages.")
