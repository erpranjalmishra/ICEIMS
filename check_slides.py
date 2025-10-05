import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccca_website.settings')
django.setup()

from conference.models import HeroSlide

slides = HeroSlide.objects.all()
print(f'\n=== HERO SLIDES ({slides.count()}) ===\n')

for slide in slides:
    print(f'ID: {slide.id}')
    print(f'Title: {slide.title}')
    print(f'Type: {slide.slide_type}')
    print(f'Active: {slide.is_active}')
    print(f'Image: {slide.image.name if slide.image else "❌ NO IMAGE UPLOADED"}')
    if slide.image:
        print(f'Image URL would be: /media/{slide.image.name}')
    print('-' * 50)

print(f'\n✅ Active slides: {HeroSlide.objects.filter(is_active=True).count()}')
print(f'📁 Total slides: {slides.count()}\n')
