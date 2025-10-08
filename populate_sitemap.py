import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import SitemapLink
from django.urls import reverse

# Clear existing links
SitemapLink.objects.all().delete()

# Create default site links
default_links = [
    {'name': 'Home', 'url': '/home/', 'icon': 'fa-home', 'description': 'Conference homepage with latest updates', 'order': 1},
    {'name': 'About Conference', 'url': '/about/', 'icon': 'fa-info-circle', 'description': 'Learn about ICEIMS 2026', 'order': 2},
    {'name': 'Galgotias University', 'url': '/university/', 'icon': 'fa-university', 'description': 'Explore our world-class campus', 'order': 3},
    {'name': 'Contact Us', 'url': '/contact/', 'icon': 'fa-envelope', 'description': 'Get in touch with us', 'order': 4},
    {'name': 'Conference Tracks', 'url': '/tracks/', 'icon': 'fa-layer-group', 'description': 'Technical program areas', 'order': 5},
    {'name': 'Important Dates', 'url': '/home/#timeline', 'icon': 'fa-calendar-alt', 'description': 'Key deadlines and milestones', 'order': 6},
    {'name': 'Guidelines', 'url': '/guidelines/', 'icon': 'fa-file-alt', 'description': 'Submission and presentation guidelines', 'order': 7},
    {'name': 'Registration', 'url': '/registration/', 'icon': 'fa-user-plus', 'description': 'Register for the conference', 'order': 8},
    {'name': 'Schedule', 'url': '/schedule/', 'icon': 'fa-calendar-week', 'description': 'Conference program schedule', 'order': 9},
    {'name': 'Committee Members', 'url': '/committee/', 'icon': 'fa-users', 'description': 'Organizing committee', 'order': 10},
    {'name': 'Keynote Speakers', 'url': '/keynotes/', 'icon': 'fa-microphone', 'description': 'Featured speakers and presentations', 'order': 11},
    {'name': 'Awards', 'url': '/awards/', 'icon': 'fa-trophy', 'description': 'Conference awards and recognition', 'order': 12},
    {'name': 'Blog', 'url': '/blog/', 'icon': 'fa-blog', 'description': 'Latest news and articles', 'order': 13},
    {'name': 'Downloads', 'url': '/downloads/', 'icon': 'fa-download', 'description': 'Conference documents and resources', 'order': 14},
    {'name': 'Tourist Attractions', 'url': '/attractions/', 'icon': 'fa-map-marked-alt', 'description': 'Explore NCR region', 'order': 15},
    {'name': 'Sponsors & Partners', 'url': '/sponsors/', 'icon': 'fa-handshake', 'description': 'Our supporters', 'order': 16},
    {'name': 'Previous Conference', 'url': '/previous/', 'icon': 'fa-history', 'description': 'Past conference highlights', 'order': 17},
]

# Create links
created_count = 0
for link_data in default_links:
    SitemapLink.objects.create(
        name=link_data['name'],
        url=link_data['url'],
        description=link_data['description'],
        icon=link_data['icon'],
        display_order=link_data['order'],
        is_active=True
    )
    created_count += 1
    print(f"✓ Created: {link_data['name']}")

print(f"\n🎉 Successfully created {created_count} sitemap links!")
print("You can now manage these links from /admin/conference/sitemaplink/")
