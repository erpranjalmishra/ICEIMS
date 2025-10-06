"""
Management command to verify media files and check for issues
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from conference.models import (
    Sponsor, CommitteeMember, TouristAttraction, HeroSlide, 
    SiteSettings, UniversityGallery, Speaker
)
import os


class Command(BaseCommand):
    help = 'Verify media files exist and check for broken links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix missing media files',
        )

    def handle(self, *args, **options):
        self.stdout.write('Checking media files...\n')
        
        issues = []
        
        # Check Sponsors
        self.stdout.write('Checking sponsors...')
        for sponsor in Sponsor.objects.all():
            if sponsor.logo:
                if not os.path.exists(sponsor.logo.path):
                    issues.append(f"Sponsor '{sponsor.name}' - Logo missing: {sponsor.logo.path}")
        
        # Check Committee Members
        self.stdout.write('Checking committee members...')
        for member in CommitteeMember.objects.all():
            if member.image:
                if not os.path.exists(member.image.path):
                    issues.append(f"Committee member '{member.name}' - Image missing: {member.image.path}")
        
        # Check Tourist Attractions
        self.stdout.write('Checking tourist attractions...')
        for attraction in TouristAttraction.objects.all():
            if attraction.image:
                if not os.path.exists(attraction.image.path):
                    issues.append(f"Attraction '{attraction.name}' - Image missing: {attraction.image.path}")
        
        # Check Hero Slides
        self.stdout.write('Checking hero slides...')
        for slide in HeroSlide.objects.all():
            if slide.image:
                if not os.path.exists(slide.image.path):
                    issues.append(f"Hero slide '{slide.title}' - Image missing: {slide.image.path}")
        
        # Check Site Settings
        self.stdout.write('Checking site settings...')
        try:
            site_settings = SiteSettings.objects.first()
            if site_settings:
                if site_settings.main_logo and not os.path.exists(site_settings.main_logo.path):
                    issues.append(f"Site Settings - Main logo missing: {site_settings.main_logo.path}")
                if site_settings.footer_logo and not os.path.exists(site_settings.footer_logo.path):
                    issues.append(f"Site Settings - Footer logo missing: {site_settings.footer_logo.path}")
        except:
            pass
        
        # Check Speakers
        self.stdout.write('Checking speakers...')
        for speaker in Speaker.objects.all():
            if speaker.photo:
                if not os.path.exists(speaker.photo.path):
                    issues.append(f"Speaker '{speaker.name}' - Photo missing: {speaker.photo.path}")
        
        # Check University Gallery
        self.stdout.write('Checking university gallery...')
        for image in UniversityGallery.objects.all():
            if image.image:
                if not os.path.exists(image.image.path):
                    issues.append(f"Gallery image '{image.title}' - Image missing: {image.image.path}")
        
        # Report results
        if issues:
            self.stdout.write(self.style.WARNING(f'\nFound {len(issues)} issues:'))
            for issue in issues:
                self.stdout.write(self.style.ERROR(f'  - {issue}'))
            
            self.stdout.write(self.style.WARNING(f'\nMedia root: {settings.MEDIA_ROOT}'))
            self.stdout.write(self.style.WARNING(f'Media URL: {settings.MEDIA_URL}'))
            
            if not os.path.exists(settings.MEDIA_ROOT):
                self.stdout.write(self.style.ERROR(f'\nWARNING: Media root directory does not exist!'))
                if options['fix']:
                    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                    self.stdout.write(self.style.SUCCESS('Created media root directory'))
        else:
            self.stdout.write(self.style.SUCCESS('\nAll media files OK!'))
        
        # Check if media directory exists
        if not os.path.exists(settings.MEDIA_ROOT):
            self.stdout.write(self.style.ERROR(f'\nMedia root does not exist: {settings.MEDIA_ROOT}'))
            self.stdout.write(self.style.WARNING('Create it with: python manage.py create_media_dirs'))
        else:
            # List media subdirectories
            self.stdout.write(f'\nMedia subdirectories:')
            for item in os.listdir(settings.MEDIA_ROOT):
                item_path = os.path.join(settings.MEDIA_ROOT, item)
                if os.path.isdir(item_path):
                    file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
                    self.stdout.write(f'  - {item}/ ({file_count} files)')
