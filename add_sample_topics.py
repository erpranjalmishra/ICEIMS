import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import ConferenceTopic

# Sample conference topics
topics = [
    {
        'title': 'Renewable Energy Systems',
        'description': 'Solar, wind, hydro power and sustainable energy solutions',
        'icon_class': 'fas fa-solar-panel',
        'display_order': 1
    },
    {
        'title': 'Smart Manufacturing',
        'description': 'Industry 4.0, IoT integration and automation technologies',
        'icon_class': 'fas fa-industry',
        'display_order': 2
    },
    {
        'title': 'Artificial Intelligence',
        'description': 'Machine learning, neural networks and intelligent systems',
        'icon_class': 'fas fa-robot',
        'display_order': 3
    },
    {
        'title': 'Advanced Materials',
        'description': 'Nanomaterials, composites and material science innovations',
        'icon_class': 'fas fa-atom',
        'display_order': 4
    },
    {
        'title': 'Energy Storage Solutions',
        'description': 'Battery technologies, grid storage and energy management',
        'icon_class': 'fas fa-battery-full',
        'display_order': 5
    },
    {
        'title': 'Robotics & Automation',
        'description': 'Industrial robots, collaborative systems and autonomous solutions',
        'icon_class': 'fas fa-cog',
        'display_order': 6
    },
]

print("Creating conference topics...")
created_count = 0
updated_count = 0

for topic_data in topics:
    topic, created = ConferenceTopic.objects.get_or_create(
        title=topic_data['title'],
        defaults=topic_data
    )
    if created:
        created_count += 1
        print(f"✓ Created: {topic.title}")
    else:
        updated_count += 1
        print(f"→ Already exists: {topic.title}")

print(f"\n✅ Done! Created {created_count} new topics, {updated_count} already existed.")
print("You can now customize these topics in the admin panel!")
