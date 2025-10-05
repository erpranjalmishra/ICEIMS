import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import HeroSlide

slides = HeroSlide.objects.filter(is_active=True).order_by('display_order')
print("=== ACTIVE SLIDES IN DISPLAY ORDER ===\n")
for s in slides:
    has_image = "✅ YES" if s.image else "❌ NO"
    print(f"Order: {s.display_order}")
    print(f"ID: {s.id}")
    print(f"Title: {s.title}")
    print(f"Has Image: {has_image}")
    if s.image:
        print(f"Image: {s.image.url}")
    print("-" * 50)
